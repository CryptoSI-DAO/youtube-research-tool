#!/usr/bin/env python3
"""
HTML Report Generator
Generates a consistently-structured HTML research report from the analysis data.
"""

import json
from datetime import datetime
from pathlib import Path


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Video Research Report - {{video_title}}</title>
<style>
  /* --- Reset & Base --- */
  body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    line-height: 1.7;
    color: #1a1a2e;
    background: #f8f9fc;
    margin: 0;
    padding: 0;
  }
  .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 40px 24px;
  }

  /* --- Header --- */
  .report-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 40px 32px;
    border-radius: 12px 12px 0 0;
    margin: -40px -24px 0;
  }
  .report-header h1 {
    margin: 0 0 8px;
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.5px;
  }
  .report-header .meta {
    font-size: 14px;
    opacity: 0.9;
    margin: 4px 0;
  }
  .report-header .badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 8px;
  }

  /* --- Sections --- */
  .section {
    background: white;
    margin: 20px 0;
    padding: 28px 32px;
    border-radius: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }
  .section h2 {
    color: #667eea;
    font-size: 20px;
    font-weight: 700;
    margin: 0 0 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid #e8ecf4;
  }
  .section h3 {
    color: #333;
    font-size: 16px;
    margin: 20px 0 8px;
  }
  .section p {
    margin: 0 0 12px;
  }

  /* --- Takeaways --- */
  .takeaway-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .takeaway-item {
    display: flex;
    align-items: flex-start;
    margin-bottom: 14px;
    padding: 14px 18px;
    background: #f0f4ff;
    border-left: 4px solid #667eea;
    border-radius: 6px;
  }
  .takeaway-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 28px;
    height: 28px;
    background: #667eea;
    color: white;
    border-radius: 50%;
    font-size: 13px;
    font-weight: 700;
    margin-right: 14px;
    flex-shrink: 0;
  }
  .takeaway-content strong {
    display: block;
    color: #333;
    margin-bottom: 2px;
  }
  .takeaway-content .explanation {
    font-size: 14px;
    color: #555;
  }

  /* --- Analysis --- */
  .analysis-block {
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid #eef0f5;
  }
  .analysis-block:last-child {
    border-bottom: none;
    margin-bottom: 0;
  }
  .analysis-block h3 {
    color: #764ba2;
  }

  /* --- External Research --- */
  .research-card {
    background: #fafbff;
    border: 1px solid #e4e8f2;
    border-radius: 8px;
    padding: 16px 18px;
    margin-bottom: 14px;
  }
  .research-card .topic {
    font-weight: 700;
    color: #4a3f8a;
    margin-bottom: 6px;
  }
  .research-card .source {
    font-size: 12px;
    color: #888;
    margin-top: 8px;
  }
  .research-card .source a {
    color: #667eea;
  }

  /* --- Sources --- */
  .sources-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .sources-list li {
    padding: 8px 0;
    border-bottom: 1px solid #f0f0f5;
    font-size: 14px;
  }
  .sources-list li:last-child {
    border-bottom: none;
  }
  .sources-list a {
    color: #667eea;
    word-break: break-all;
  }

  /* --- Footer --- */
  .report-footer {
    text-align: center;
    padding: 20px;
    color: #999;
    font-size: 13px;
    margin-top: 20px;
  }
</style>
</head>
<body>
<div class="container">

<!-- ========== HEADER ========== -->
<div class="report-header">
  <h1>📺 Video Research Report</h1>
  <div class="meta"><span class="badge">TITLE</span> {{video_title}}</div>
  <div class="meta"><span class="badge">URL</span> <a href="{{video_url}}" style="color:#fff">{{video_url}}</a></div>
  <div class="meta"><span class="badge">DURATION</span> {{video_duration}} &nbsp;|&nbsp; <span class="badge">GENERATED</span> {{generated_at}}</div>
</div>

<!-- ========== EXECUTIVE SUMMARY ========== -->
<div class="section">
  <h2>📋 Executive Summary</h2>
  {{executive_summary_html}}
</div>

<!-- ========== KEY TAKEAWAYS ========== -->
<div class="section">
  <h2>🔑 Key Takeaways</h2>
  <ol class="takeaway-list">
    {{takeaways_html}}
  </ol>
</div>

<!-- ========== DETAILED ANALYSIS ========== -->
<div class="section">
  <h2>🔬 Detailed Analysis</h2>
  {{analysis_html}}
</div>

<!-- ========== EXTERNAL RESEARCH ========== -->
<div class="section">
  <h2>🌐 External Research</h2>
  {{external_research_html}}
</div>

<!-- ========== SOURCES & REFERENCES ========== -->
<div class="section">
  <h2>📚 Sources & References</h2>
  <ul class="sources-list">
    {{sources_html}}
  </ul>
</div>

<div class="report-footer">
  Generated by Data · YouTube Research Tool · {{generated_at}}
</div>

</div>
</body>
</html>
"""


def generate_html_report(report_data: dict) -> str:
    """
    Generate a complete HTML research report.
    
    Args:
        report_data: dict with report sections
    
    Returns:
        str: Complete HTML document
    """
    # Build each section's HTML
    exec_summary_html = _paragraphs_to_html(report_data.get("executive_summary", ""))
    
    takeaways = report_data.get("key_takeaways", [])
    takeaways_html = _build_takeaways(takeaways)
    
    analysis = report_data.get("detailed_analysis", [])
    analysis_html = _build_analysis(analysis)
    
    ext_research = report_data.get("external_research", [])
    ext_research_html = _build_research_cards(ext_research)
    
    sources = report_data.get("sources", [])
    sources_html = _build_sources(sources)
    
    # Fill template
    html = HTML_TEMPLATE
    html = html.replace("{{video_title}}", _escape(report_data.get("video_title", "Unknown")))
    html = html.replace("{{video_url}}", report_data.get("video_url", ""))
    html = html.replace("{{video_duration}}", report_data.get("video_duration", "Unknown"))
    html = html.replace("{{generated_at}}", datetime.now().strftime("%B %d, %Y at %I:%M %p"))
    html = html.replace("{{executive_summary_html}}", exec_summary_html)
    html = html.replace("{{takeaways_html}}", takeaways_html)
    html = html.replace("{{analysis_html}}", analysis_html)
    html = html.replace("{{external_research_html}}", ext_research_html)
    html = html.replace("{{sources_html}}", sources_html)
    
    return html


def _build_takeaways(takeaways: list) -> str:
    if not takeaways:
        return '<li class="takeaway-item"><div class="takeaway-content">No key takeaways identified.</div></li>'
    
    items = []
    for i, t in enumerate(takeaways, 1):
        if isinstance(t, dict):
            point = t.get("point", "")
            explanation = t.get("explanation", "")
        else:
            point = str(t)
            explanation = ""
        
        explain_html = f'<div class="explanation">{_escape(explanation)}</div>' if explanation else ""
        items.append(
            f'<li class="takeaway-item">'
            f'<span class="takeaway-num">{i}</span>'
            f'<div class="takeaway-content"><strong>{_escape(point)}</strong>{explain_html}</div>'
            f'</li>'
        )
    return "\n".join(items)


def _build_analysis(analysis: list) -> str:
    if not analysis:
        return "<p>No detailed analysis available.</p>"
    
    blocks = []
    for section in analysis:
        heading = section.get("heading", section.get("title", "Section"))
        content = section.get("content", "")
        blocks.append(
            f'<div class="analysis-block">'
            f'<h3>{_escape(heading)}</h3>'
            f'{_paragraphs_to_html(content)}'
            f'</div>'
        )
    return "\n".join(blocks)


def _build_research_cards(ext_research: list) -> str:
    if not ext_research:
        return "<p>No additional external research was conducted.</p>"
    
    cards = []
    for item in ext_research:
        topic = item.get("topic", item.get("title", "Topic"))
        findings = item.get("findings", item.get("content", ""))
        source = item.get("source", item.get("url", ""))
        
        source_html = f'<div class="source">Source: <a href="{source}" target="_blank">{_escape(source[:80])}</a></div>' if source else ""
        
        cards.append(
            f'<div class="research-card">'
            f'<div class="topic">{_escape(topic)}</div>'
            f'{_paragraphs_to_html(findings)}'
            f'{source_html}'
            f'</div>'
        )
    return "\n".join(cards)


def _build_sources(sources: list) -> str:
    if not sources:
        return "<li>No sources cited.</li>"
    
    items = []
    for src in sources:
        if isinstance(src, dict):
            title = src.get("title", src.get("name", src.get("url", "Source")))
            url = src.get("url", "")
            items.append(f'<li><a href="{url}" target="_blank">{_escape(title)}</a></li>')
        elif isinstance(src, str):
            if src.startswith("http"):
                items.append(f'<li><a href="{src}" target="_blank">{_escape(src[:100])}</a></li>')
            else:
                items.append(f"<li>{_escape(src)}</li>")
    return "\n".join(items)


def _paragraphs_to_html(text: str) -> str:
    if not text:
        return ""
    # Split on double newlines or just wrap
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if len(paragraphs) == 1 and "\n" not in text:
        return f"<p>{_escape(text)}</p>"
    return "\n".join(f"<p>{_escape(p)}</p>" for p in paragraphs)


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def save_report(html: str, video_title: str) -> str:
    """Save HTML report to file, return path."""
    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in video_title)[:50]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    base = Path("/workspace/youtube-research-tool/output/reports")
    base.mkdir(parents=True, exist_ok=True)
    
    path = base / f"{safe_title}_{timestamp}.html"
    path.write_text(html, encoding="utf-8")
    return str(path)


if __name__ == "__main__":
    print("Load this module and call generate_html_report(report_data)")
