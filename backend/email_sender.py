#!/usr/bin/env python3
"""
Email Sender
Sends the HTML report and TTS audio file via email using SMTP.
Supports himalaya CLI or direct smtplib as fallback.
"""

import os
import sys
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import datetime


def send_report_email(
    html_report: str,
    tts_script: str = None,
    audio_path: str = None,
    to_email: str = "cryptosi@protonmail.com",
    from_email: str = "lisakimvirtuals@gmail.com",
    subject: str = None,
    smtp_host: str = "smtp.gmail.com",
    smtp_port: int = 587,
    smtp_password: str = None,
) -> bool:
    """
    Send the research report email with HTML body + optional audio attachment.
    
    Args:
        html_report: Full HTML report string
        tts_script: TTS script text (included as text attachment)
        audio_path: Path to MP3 audio file (attached as audio/mpeg)
        to_email: Recipient email
        from_email: Sender email
        subject: Email subject (auto-generated if None)
        smtp_host: SMTP server
        smtp_port: SMTP port
        smtp_password: App-specific password for Gmail
    
    Returns:
        bool: True if sent successfully
    """
    if not smtp_password:
        smtp_password = os.environ.get("GMAIL_SMTP_PASSWORD", "")
    
    if not subject:
        subject = f"📺 YouTube Research Report - {datetime.now().strftime('%B %d, %Y')}"
    
    # Build the email
    msg = MIMEMultipart("mixed")
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    
    # HTML body
    msg.attach(MIMEText(html_report, "html", "utf-8"))
    
    # Attach TTS script as text file
    if tts_script:
        script_part = MIMEText(tts_script, "plain", "utf-8")
        script_part.add_header(
            "Content-Disposition",
            "attachment",
            filename="TTS_Narration_Script.txt"
        )
        msg.attach(script_part)
    
    # Attach audio file
    if audio_path and Path(audio_path).exists():
        with open(audio_path, "rb") as f:
            audio_data = f.read()
        
        audio_part = MIMEBase("audio", "mpeg")
        audio_part.set_payload(audio_data)
        encoders.encode_base64(audio_part)
        
        audio_filename = Path(audio_path).name
        audio_part.add_header(
            "Content-Disposition",
            "attachment",
            filename=audio_filename
        )
        msg.attach(audio_part)
    
    # Send via SMTP
    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(from_email, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())
        
        print(f"✅ Email sent successfully to {to_email}")
        return True
    
    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP Authentication failed. Check your Gmail app password.", file=sys.stderr)
        print("   In the meantime, check: /workspace/youtube-research-tool/output/", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Email send failed: {e}", file=sys.stderr)
        return False


def send_test_email(to_email: str = "cryptosi@protonmail.com") -> bool:
    """Send a quick test email to verify SMTP is working."""
    smtp_password = os.environ.get("GMAIL_SMTP_PASSWORD", "")
    if not smtp_password:
        print("❌ No GMAIL_SMTP_PASSWORD environment variable set.", file=sys.stderr)
        return False
    
    from_email = "lisakimvirtuals@gmail.com"
    subject = "🔧 YouTube Research Tool — Test Email"
    body = """
    <html>
    <body style="font-family: sans-serif; max-width: 500px; margin: 40px auto;">
        <h2 style="color: #667eea;">✅ Test Successful!</h2>
        <p>Your YouTube Research Tool email pipeline is working correctly.</p>
        <p>From now on, when you send me a YouTube URL, I'll:</p>
        <ol>
            <li>Grab the transcript</li>
            <li>Do deep web research</li>
            <li>Generate a structured HTML report</li>
            <li>Create a ~5 min TTS audio narration</li>
            <li>Email everything to you</li>
        </ol>
        <br>
        <p style="color: #999; font-size: 13px;">— Data, your research agent</p>
    </body>
    </html>
    """
    
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html", "utf-8"))
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(from_email, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())
        
        print(f"✅ Test email sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Test email failed: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Send test email")
    parser.add_argument("--to", default="cryptosi@protonmail.com")
    args = parser.parse_args()
    
    if args.test:
        send_test_email(args.to)
