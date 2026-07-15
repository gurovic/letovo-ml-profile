#!/usr/bin/env python3
"""Convert LESSON.md to HTML for Canvas wiki pages (with visible table borders)."""

from __future__ import annotations

import re
import sys

# Canvas часто вырезает <style>, поэтому бордюры задаём инлайном на каждом теге.
_TABLE_STYLE = "border-collapse:collapse;border:1px solid #a0a0a0;margin:1em 0;"
_CELL_STYLE = "border:1px solid #a0a0a0;padding:6px 10px;text-align:left;vertical-align:top;"
_TH_STYLE = _CELL_STYLE + "background:#f0f0f0;font-weight:bold;"

# Относительные ссылки вида [text](lesson.ipynb) / (./homework.ipynb)
_MD_LINK_RE = re.compile(
    r"\[([^\]]*)\]\((?:\./)?(lesson|homework)\.ipynb\)",
    re.IGNORECASE,
)


def rewrite_notebook_links(
    markdown_text: str,
    *,
    lesson_colab_url: str | None = None,
    homework_colab_url: str | None = None,
) -> str:
    """Replace relative .ipynb markdown links with Colab URLs for Canvas wiki."""

    def repl(match: re.Match[str]) -> str:
        label, kind = match.group(1), match.group(2).lower()
        url = lesson_colab_url if kind == "lesson" else homework_colab_url
        if not url:
            return match.group(0)
        # Человеческий ярлык, если в ссылке было только имя файла
        if label.lower() in {f"{kind}.ipynb", kind}:
            label = "Ноутбук урока" if kind == "lesson" else "Домашнее задание"
        return f"[{label}]({url})"

    return _MD_LINK_RE.sub(repl, markdown_text)


def _add_inline_borders(html_body: str) -> str:
    html_body = html_body.replace("<table>", f'<table style="{_TABLE_STYLE}">')
    html_body = re.sub(r"<th>", f'<th style="{_TH_STYLE}">', html_body)
    html_body = re.sub(
        r'<th align="(left|right|center)">',
        lambda m: f'<th style="{_TH_STYLE}text-align:{m.group(1)};">',
        html_body,
    )
    html_body = re.sub(r"<td>", f'<td style="{_CELL_STYLE}">', html_body)
    html_body = re.sub(
        r'<td align="(left|right|center)">',
        lambda m: f'<td style="{_CELL_STYLE}text-align:{m.group(1)};">',
        html_body,
    )
    return html_body


def lesson_md_to_canvas_html(
    markdown_text: str,
    *,
    lesson_colab_url: str | None = None,
    homework_colab_url: str | None = None,
) -> str:
    """Render Markdown (tables, fenced code) to HTML for Canvas wiki body."""
    try:
        import markdown
    except ImportError:
        print(
            "Error: package 'markdown' required. Run: pip install -r scripts/requirements.txt",
            file=sys.stderr,
        )
        raise SystemExit(1) from None

    md = rewrite_notebook_links(
        markdown_text,
        lesson_colab_url=lesson_colab_url,
        homework_colab_url=homework_colab_url,
    )
    body = markdown.markdown(
        md,
        extensions=["tables", "fenced_code", "sane_lists"],
        output_format="html5",
    )
    body = _add_inline_borders(body)
    return (
        '<div class="user_content lesson-md-content" '
        'style="max-width:900px;line-height:1.5;">'
        f"{body}</div>"
    )
