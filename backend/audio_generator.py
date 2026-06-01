#!/usr/bin/env python3
"""
Audio Generator
Generate MP3 audio from TTS script text using edge-tts (free, no API key needed).
Targets ~5 minutes of audio.
"""

import asyncio
import os
from pathlib import Path
from datetime import datetime

# Available voices at natural-sounding speeds
VOICES = {
    "male_us": "en-US-GuyNeural",
    "female_us": "en-US-JennyNeural",
    "male_uk": "en-GB-RyanNeural",
    "female_uk": "en-GB-SoniaNeural",
    "male_au": "en-AU-WilliamNeural",
    "female_au": "en-AU-NatashaNeural",
}

DEFAULT_VOICE = "en-US-GuyNeural"  # Male US - clear, professional narrator


async def generate_audio(script_text: str, output_path: str, voice: str = None) -> str:
    """
    Generate MP3 audio from text using edge-tts.
    
    Args:
        script_text: The TTS script text
        output_path: Where to save the MP3
        voice: edge-tts voice ID (default: en-US-GuyNeural)
    
    Returns:
        str: Path to generated audio file
    """
    import edge_tts
    
    voice = voice or DEFAULT_VOICE
    
    # edge-tts default speed is ~150 wpm which is perfect for narration
    # We can adjust with rate parameter if needed
    communicate = edge_tts.Communicate(script_text, voice, rate="+0%")
    await communicate.save(output_path)
    
    # Get file size
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Audio generated: {output_path} ({size_mb:.1f} MB)")
    
    return output_path


def generate_audio_sync(script_text: str, output_path: str = None, voice: str = None) -> str:
    """Synchronous wrapper for generate_audio."""
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"/workspace/youtube-research-tool/output/audio/tts_report_{timestamp}.mp3"
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    return asyncio.run(generate_audio(script_text, output_path, voice))


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python audio_generator.py <script_file.txt> [output.mp3]")
        sys.exit(1)
    
    script_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    text = Path(script_file).read_text(encoding="utf-8")
    result = generate_audio_sync(text, output_file)
    print(f"Saved to: {result}")
