#!/usr/bin/env python3
"""
TTS Script Generator
Generates a ~5 minute single-narrator script based on the research report.
Output: script text file ready for TTS audio generation.
"""

import json
from datetime import datetime


def generate_tts_script(report_data: dict) -> str:
    """
    Generate a ~5 minute TTS narration script from report data.
    
    Target: ~750 words at natural narration pace (~150 wpm) = ~5 min
    
    Args:
        report_data: dict with keys:
            - video_title, video_url, video_duration
            - executive_summary
            - key_takeaways (list)
            - detailed_analysis (list of {heading, content})
            - external_research (list of {topic, findings, source})
            - sources (list)
    
    Returns:
        str: Formatted TTS script
    """
    script_parts = []
    
    # --- INTRO ---
    video_title = report_data.get("video_title", "the video")
    script_parts.append(
        f"Welcome to today's video research report. "
        f"We've just completed an in-depth analysis of a YouTube video titled: {video_title}. "
        f"Here's everything you need to know.\n"
    )
    
    # --- EXECUTIVE SUMMARY ---
    exec_summary = report_data.get("executive_summary", "")
    if exec_summary:
        script_parts.append(
            f"Executive Summary.\n\n"
            f"{exec_summary}\n"
        )
    
    # --- KEY TAKEAWAYS ---
    takeaways = report_data.get("key_takeaways", [])
    if takeaways:
        script_parts.append(f"Key Takeaways.\n\n")
        for i, t in enumerate(takeaways, 1):
            bullet = t.get("point", t) if isinstance(t, dict) else t
            explanation = t.get("explanation", "") if isinstance(t, dict) else ""
            script_parts.append(f"Number {i}. {bullet}.\n")
            if explanation:
                script_parts.append(f"{explanation}.\n")
            script_parts.append("\n")
    
    # --- DETAILED ANALYSIS (condensed for audio) ---
    analysis = report_data.get("detailed_analysis", [])
    if analysis:
        script_parts.append(f"Detailed Analysis.\n\n")
        for section in analysis:
            heading = section.get("heading", section.get("title", "Section"))
            # Limit each section to keep runtime manageable
            content = section.get("content", "")
            # Take first 3 sentences for each section in audio
            sentences = _first_n_sentences(content, 3)
            if sentences:
                script_parts.append(f"{heading}.\n")
                script_parts.append(f"{sentences}\n\n")
    
    # --- EXTERNAL RESEARCH ---
    ext_research = report_data.get("external_research", [])
    if ext_research:
        script_parts.append(f"Additional Research.\n\n")
        for item in ext_research[:5]:  # Cap at 5 items for time
            topic = item.get("topic", item.get("title", "Topic"))
            findings = item.get("findings", item.get("content", ""))
            source = item.get("source", item.get("url", ""))
            brief = _first_n_sentences(findings, 2)
            if brief:
                script_parts.append(f"On the topic of {topic}:\n")
                script_parts.append(f"{brief}\n")
                if source:
                    script_parts.append(f"Source: {source}.\n")
                script_parts.append("\n")
    
    # --- OUTRO ---
    script_parts.append(
        f"That concludes our research report. "
        f"For the full detailed report with all sources and references, "
        f"check your email for the complete HTML version. "
        f"Happy researching.\n"
    )
    
    full_script = "\n".join(script_parts)
    
    # Word count check for ~5 min target
    word_count = len(full_script.split())
    
    # Trim if too long (some sections can run over)
    if word_count > 900:
        full_script = _trim_to_word_count(full_script, 800)
    
    return full_script


def _first_n_sentences(text: str, n: int) -> str:
    """Extract first N sentences from text."""
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return " ".join(sentences[:n])


def _trim_to_word_count(text: str, max_words: int) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    trimmed = " ".join(words[:max_words])
    # End at a sentence boundary
    last_period = trimmed.rfind(".")
    if last_period > len(trimmed) * 0.7:
        return trimmed[:last_period + 1]
    return trimmed


def save_script(script_text: str, video_title: str) -> str:
    """Save TTS script to file, return path."""
    from pathlib import Path
    
    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in video_title)[:50]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    base = Path("/workspace/youtube-research-tool/output/audio")
    base.mkdir(parents=True, exist_ok=True)
    
    path = base / f"{safe_title}_{timestamp}_script.txt"
    path.write_text(script_text, encoding="utf-8")
    return str(path)


if __name__ == "__main__":
    print("Load this module and call generate_tts_script(report_data)")
