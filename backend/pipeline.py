#!/usr/bin/env python3
"""
YouTube Research Pipeline — CLI entry point.
Called by the webhook server with --url and --email arguments.

Usage:
    python pipeline.py --url "https://youtube.com/watch?v=..." --email "user@example.com"
"""

import argparse
import json
import os
import sys
import re
import subprocess
from pathlib import Path
from datetime import datetime

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from html_report import generate_html_report, save_report
from tts_script_generator import generate_tts_script, save_script
from audio_generator import generate_audio_sync


def extract_video_id(url: str) -> str:
    url = url.strip()
    patterns = [
        r'(?:v=|youtu\.be/|shorts/|embed/|live/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    # Strip tracking params if regex didn't match
    url = url.split("?")[0].split("&")[0]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return url


def fetch_transcript(video_id: str) -> str:
    """Fetch transcript text from YouTube."""
    skill_script = Path("/root/.hermes/skills/media/youtube-content/scripts/fetch_transcript.py")
    if skill_script.exists():
        result = subprocess.run(
            [sys.executable, str(skill_script), video_id, "--text-only"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return result.stdout.strip()
    # Fallback: use the API directly
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        result = api.fetch(video_id)
        return " ".join(s.text for s in result)
    except Exception as e:
        raise RuntimeError(f"Transcript fetch failed: {e}")


def get_video_title(video_id: str) -> str:
    """Get video title via yt-dlp or oembed."""
    try:
        result = subprocess.run(
            ["yt-dlp", "--dump-json", "--no-download", f"https://youtube.com/watch?v={video_id}"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("title", f"Video {video_id}")
    except Exception:
        pass
    # Fallback: oembed
    try:
        import urllib.request
        url = f"https://www.youtube.com/oembed?url=https://youtube.com/watch?v={video_id}&format=json"
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("title", f"Video {video_id}")
    except Exception:
        return f"Video {video_id}"


def send_email(html: str, script: str, audio_path: str, to_email: str):
    """Send email via himalaya CLI."""
    # Build MML message with attachments
    mml_parts = [
        "From: lisakimvirtuals@gmail.com",
        f"To: {to_email}",
        f"Subject: YouTube Research Report — {datetime.now().strftime('%B %d, %Y')}",
        "",
        "<#multipart type=alternative>",
        "Your YouTube research report is attached.",
        "",
        "Files attached:",
        "  1. Research Report (HTML) — Full structured analysis",
        "  2. TTS Narration Script — ~5 min audio script",
        "  3. Audio Report (MP3) — Narrated version",
        "",
        "— Data, your research agent",
        f'<#part type=text/html filename="{html}" name="Research_Report.html"><#/part>',
    ]
    if script:
        mml_parts.append(f'<#part filename="{script}" name="TTS_Script.txt"><#/part>')
    if audio_path and Path(audio_path).exists():
        mml_parts.append(f'<#part filename="{audio_path}" name="Audio_Report.mp3"><#/part>')
    mml_parts.append("<#/multipart>")

    mml = "\n".join(mml_parts)

    result = subprocess.run(
        ["himalaya", "template", "send"],
        input=mml, capture_output=True, text=True, timeout=60
    )
    return result.returncode == 0, result.stderr


def main():
    parser = argparse.ArgumentParser(description="YouTube Research Pipeline")
    parser.add_argument("--url", required=True, help="YouTube video URL")
    parser.add_argument("--email", required=True, help="Recipient email address")
    args = parser.parse_args()

    youtube_url = args.url
    email = args.email

    print(f"Pipeline started: {youtube_url} → {email}")
    print(f"Time: {datetime.now().isoformat()}")

    # Step 1: Extract video ID
    video_id = extract_video_id(youtube_url)
    print(f"[1/6] Video ID: {video_id}")

    # Step 2: Get title
    print("[2/6] Fetching video title...")
    title = get_video_title(video_id)
    print(f"  Title: {title}")

    # Step 3: Fetch transcript
    print("[3/6] Fetching transcript...")
    transcript = fetch_transcript(video_id)
    word_count = len(transcript.split())
    print(f"  Transcript: {len(transcript)} chars, {word_count} words")

    if word_count < 50:
        print("ERROR: Transcript too short or unavailable")
        sys.exit(1)

    # Step 4: Build report data from transcript
    # For now, create a structured report from transcript content
    # TODO: Integrate LLM-based analysis for deeper research
    print("[4/6] Building report...")

    # Extract key topics from transcript (simple keyword extraction)
    from collections import Counter
    words = transcript.lower().split()
    stop_words = {"the","a","an","is","are","was","were","be","been","being","have","has","had","do","does","did","will","would","could","should","may","might","shall","can","to","of","in","for","on","with","at","by","from","as","into","through","during","before","after","above","below","between","out","off","over","under","again","further","then","once","here","there","when","where","why","how","all","each","every","both","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","just","because","but","and","or","if","while","about","up","that","this","it","i","me","my","we","our","you","your","he","she","they","them","his","her","its","their","what","which","who","whom","these","those","am","going","like","really","know","think","get","got","also","well","right","yeah","okay","ok","thing","things","way","much","even","still","back","now","one","two","new","first","last","long","great","little","old","big","high","different","small","large","next","early","young","important","public","bad","good","make","see","come","go","say","said","take","let","us","dont","thats","youre","im","dont","thing","kind","lot","want","need","going","gonna"}
    terms = [w for w in words if len(w) > 4 and w not in stop_words]
    common = Counter(terms).most_common(10)
    key_topics = [t[0] for t in common]

    # Build takeaways from transcript (first 2000 chars as summary)
    summary_text = transcript[:2000].replace("\n", " ")
    if len(transcript) > 2000:
        summary_text += "..."

    report_data = {
        "video_title": title,
        "video_url": youtube_url,
        "video_duration": "Unknown",
        "executive_summary": (
            f"This report analyzes the YouTube video '{title}'. "
            f"The video covers topics including: {', '.join(key_topics[:8])}. "
            f"Full transcript ({word_count} words) was analyzed to produce this report."
        ),
        "key_takeaways": [
            {"point": f"Key topic: {t}", "explanation": f"Mentioned {c} times in the video"}
            for t, c in common[:8]
        ],
        "detailed_analysis": [
            {
                "heading": "Transcript Content",
                "content": summary_text
            }
        ],
        "external_research": [],
        "sources": [youtube_url],
    }

    # Generate HTML
    html = generate_html_report(report_data)
    report_path = save_report(html, title)
    print(f"  Report: {report_path}")

    # Step 5: TTS Script
    print("[5/6] Generating TTS script...")
    tts_script = generate_tts_script(report_data)
    script_path = save_script(tts_script, title)
    wc = len(tts_script.split())
    print(f"  Script: {wc} words (~{wc/150:.1f} min)")

    # Generate audio
    audio_path = None
    try:
        audio_path = generate_audio_sync(tts_script)
        size_mb = os.path.getsize(audio_path) / (1024 * 1024)
        print(f"  Audio: {audio_path} ({size_mb:.1f} MB)")
    except Exception as e:
        print(f"  Audio generation failed: {e}")

    # Step 6: Send email
    print(f"[6/6] Sending email to {email}...")
    success, err = send_email(report_path, script_path, audio_path, email)
    if success:
        print("  ✅ Email sent!")
    else:
        print(f"  ❌ Email failed: {err}")
        sys.exit(1)

    print(f"\nPipeline complete! Report emailed to {email}")


if __name__ == "__main__":
    main()
