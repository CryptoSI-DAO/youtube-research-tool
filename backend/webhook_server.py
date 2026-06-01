#!/usr/bin/env python3
"""
Webhook Server — Receives research job requests from Vercel frontend,
enqueues them, and runs the YouTube research pipeline.

Runs as a background service. Jobs are stored in a simple JSON queue file.
"""

import json
import os
import sys
import time
import uuid
import hashlib
import subprocess
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# ─── Config ───────────────────────────────────────────────────────────────────

PORT = int(os.environ.get("WEBHOOK_PORT", "8765"))
WORKSPACE = Path("/workspace/youtube-research-tool")
QUEUE_FILE = WORKSPACE / "output" / "job_queue.json"
PROCESSED_FILE = WORKSPACE / "output" / "processed_jobs.json"
LOG_FILE = WORKSPACE / "output" / "webhook_server.log"

# Simple access token for webhook auth (set via env var)
WEBHOOK_TOKEN = os.environ.get("WEBHOOK_TOKEN", "")

# ─── Helpers ───────────────────────────────────────────────────────────────────

def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def load_queue() -> list:
    if QUEUE_FILE.exists():
        try:
            return json.loads(QUEUE_FILE.read_text())
        except Exception:
            pass
    return []


def save_queue(queue: list):
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_FILE.write_text(json.dumps(queue, indent=2))


def append_processed(job: dict):
    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
    processed = []
    if PROCESSED_FILE.exists():
        try:
            processed = json.loads(PROCESSED_FILE.read_text())
        except Exception:
            pass
    processed.append(job)
    PROCESSED_FILE.write_text(json.dumps(processed[-100:], indent=2))  # Keep last 100


# ─── Pipeline Runner ──────────────────────────────────────────────────────────

def run_pipeline(job: dict):
    """Run the full research pipeline for a job."""
    job_id = job["id"]
    youtube_url = job["youtube_url"]
    email = job["email"]

    log(f"Starting pipeline for job {job_id} — {youtube_url} → {email}")
    job["status"] = "running"
    job["started_at"] = datetime.now().isoformat()

    try:
        # Run the pipeline script
        env = os.environ.copy()
        env["JOB_ID"] = job_id

        result = subprocess.run(
            [
                sys.executable,
                str(WORKSPACE / "pipeline.py"),
                "--url", youtube_url,
                "--email", email,
            ],
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout
            cwd=str(WORKSPACE),
            env=env,
        )

        if result.returncode == 0:
            job["status"] = "completed"
            job["completed_at"] = datetime.now().isoformat()
            job["output"] = result.stdout[-500:]  # last 500 chars
            log(f"Job {job_id} completed successfully")
        else:
            job["status"] = "failed"
            job["error"] = result.stderr[-500:] or "Unknown error"
            log(f"Job {job_id} FAILED: {job['error']}")

    except subprocess.TimeoutExpired:
        job["status"] = "failed"
        job["error"] = "Pipeline timed out (10 min)"
        log(f"Job {job_id} TIMEOUT")
    except Exception as e:
        job["status"] = "failed"
        job["error"] = str(e)
        log(f"Job {job_id} ERROR: {e}")

    append_processed(job)


# ─── HTTP Handler ─────────────────────────────────────────────────────────────

class WebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Override to use our logger
        log(f"{self.client_address[0]} — {format % args}")

    def do_POST(self):
        if self.path != "/webhook":
            self.send_error(404)
            return

        # Auth check
        auth_header = self.headers.get("Authorization", "")
        expected = f"Bearer {WEBHOOK_TOKEN}"
        if WEBHOOK_TOKEN and auth_header != expected:
            log(f"Unauthorized request from {self.client_address[0]}")
            self.send_error(401, "Unauthorized")
            return

        # Read body
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            self.send_error(400, "Empty body")
            return

        body = self.rfile.read(content_length)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return

        # Validate
        youtube_url = data.get("youtubeUrl", "").strip()
        email = data.get("email", "").strip()

        if not youtube_url or not email:
            self.send_error(400, "Missing youtubeUrl or email")
            return

        # Create job
        job = {
            "id": str(uuid.uuid4())[:8],
            "youtube_url": youtube_url,
            "email": email,
            "source": data.get("source", "unknown"),
            "status": "queued",
            "created_at": datetime.now().isoformat(),
        }

        # Enqueue
        queue = load_queue()
        queue.append(job)
        save_queue(queue)

        log(f"Job {job['id']} queued — {youtube_url} → {email}")

        # Run pipeline in background thread
        thread = threading.Thread(target=run_pipeline, args=(job,))
        thread.daemon = True
        thread.start()

        # Respond immediately
        self.send_response(202)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "success": True,
            "jobId": job["id"],
            "message": "Research job queued. You'll receive an email shortly."
        }).encode())

    def do_GET(self):
        """Health check / queue status."""
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            queue = load_queue()
            self.wfile.write(json.dumps({
                "status": "ok",
                "queued": len([j for j in queue if j["status"] == "queued"]),
                "running": len([j for j in queue if j["status"] == "running"]),
                "port": PORT,
            }).encode())
        elif self.path == "/queue":
            # Show queue (no auth needed for localhost)
            queue = load_queue()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(queue[-20:], indent=2).encode())
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        """CORS preflight."""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    log(f"Starting webhook server on port {PORT}")
    log(f"Workspace: {WORKSPACE}")
    log(f"Queue file: {QUEUE_FILE}")

    server = HTTPServer(("0.0.0.0", PORT), WebhookHandler)
    log(f"Webhook server ready — listening on 0.0.0.0:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("Shutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
