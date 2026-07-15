#!/usr/bin/env python3
"""Convert LESSON.md to HTML for Canvas wiki pages (with visible table borders)."""

from __future__ import annotations

import re
import sys

# Canvas часто вырезает <style>, поэтому бордюры задаём инлайном на каждом теге.
_TABLE_STYLE = "border-collapse:collapse;border:1px solid #a0a0a0;margin:1em 0;"
_CELL_STYLE = "border:1px solid #a0a0a0;padding:6px 10px;text-align:left;vertical-align:top;"
_TH_STYLE = _CELL_STYLE + "background:#f0f0f0;font-weight:bold;"


def _add_inline_borders(html_body: str) -> str:
    html_body = html_body.replace("<table>", f'<table style="{_TABLE_STYLE}">')
    html_body = re.sub(r"<th>", f'<th style="{_TH_STYLE}">', html_body)
    html_body = re.sub(
        r"<th align=\"(left|right|center)\">",
        lambda m: f'<th style="{_TH_STYLE}text-align:{m.group(1)};">',
        html_body,
    )
    html_body = re.sub(r"<td>", f'<td style="{_CELL_STYLE}">', html_body)
    html_body = re.sub(
        r"<td align=\"(left|right|center)\">",
        lambda m: f'<td style="{_CELL_STYLE}text-align:{m.group(1)};">',
        html_body,
    )
    return html_body


def lesson_md_to_canvas_html(markdown_text: str) -> str:
    """Render Markdown (tables, fenced code) to HTML for Canvas wiki body."""
    try:
        import markdown
    except ImportError:
        print(
            "Error: package 'markdown' required. Run: pip install -r scripts/requirements.txt",
            file=sys.stderr,
        )
        raise SystemExit(1) from None

    body = markdown.markdown(
        markdown_text,
        extensions=["tables", "fenced_code", "sane_lists"],
        output_format="html5",
    )
    body = _add_inline_borders(body)
    return (
        '<div class="user_content lesson-md-content" '
        'style="max-width:900px;line-height:1.5;">'
        f"{body}</div>"
    )
