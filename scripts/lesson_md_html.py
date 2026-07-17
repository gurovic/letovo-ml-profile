#!/usr/bin/env python3
"""Convert Markdown to HTML for Canvas wiki pages (with visible table borders)."""

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


def rewrite_canvas_page_links(markdown_text: str, course_id: int) -> str:
    """Rewrite ``[label](canvas:slug)`` to course-relative wiki URLs."""

    def repl(match: re.Match[str]) -> str:
        label, slug = match.group(1), match.group(2)
        return f"[{label}](/courses/{course_id}/pages/{slug})"

    return re.sub(
        r"\[([^\]]+)\]\(canvas:([a-z0-9\-]+)\)",
        repl,
        markdown_text,
        flags=re.IGNORECASE,
    )


def strip_md_sections(markdown_text: str, headings: set[str]) -> str:
    """Drop ``## Heading`` sections whose heading text is in ``headings``."""
    parts = re.split(r"(?=^## )", markdown_text, flags=re.MULTILINE)
    kept: list[str] = []
    for part in parts:
        first_line = part.split("\n", 1)[0].strip()
        if first_line.startswith("## "):
            title = first_line[3:].strip()
            if title in headings:
                continue
        kept.append(part)
    return "".join(kept)


def strip_md_sections_matching(
    markdown_text: str, pattern: str
) -> str:
    """Drop ``## …`` sections whose title matches a regex (fullmatch on title)."""
    rx = re.compile(pattern)
    parts = re.split(r"(?=^## )", markdown_text, flags=re.MULTILINE)
    kept: list[str] = []
    for part in parts:
        first_line = part.split("\n", 1)[0].strip()
        if first_line.startswith("## "):
            title = first_line[3:].strip()
            if rx.fullmatch(title):
                continue
        kept.append(part)
    return "".join(kept)


def extract_md_subsection(markdown_text: str, heading: str) -> str:
    """Return ``### heading`` block (including heading) or empty string.

    Stops at the next ``#``–``###`` heading (same or higher level).
    """
    # Double braces: raw f-string must not interpolate ``{1,3}`` as an expression.
    pattern = re.compile(
        rf"(^### {re.escape(heading)}\s*\n.*?)(?=^#{{1,3}} |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    m = pattern.search(markdown_text)
    return m.group(1).strip() + "\n" if m else ""


def _drop_table_column(md: str, column_name: str) -> str:
    """Remove a markdown table column by header name (exact cell match)."""
    lines_out: list[str] = []
    col_idx: int | None = None
    for line in md.splitlines():
        if not line.strip().startswith("|"):
            lines_out.append(line)
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c or "") for c in cells):
            if col_idx is not None and 0 <= col_idx < len(cells):
                cells = cells[:col_idx] + cells[col_idx + 1 :]
            lines_out.append("| " + " | ".join(cells) + " |")
            continue
        if col_idx is None:
            for i, c in enumerate(cells):
                if c.replace("*", "") == column_name:
                    col_idx = i
                    break
        if col_idx is not None and 0 <= col_idx < len(cells):
            cells = cells[:col_idx] + cells[col_idx + 1 :]
        lines_out.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines_out)


def prepare_lesson_md_for_canvas_teacher(markdown_text: str) -> str:
    """Teacher plan for Canvas: only A (чего хотим) + B + C.

    Never includes: сценарий-таблица, D, E, «Ориентир времени», прочие ##.
    """
    intro_heading = "A. Чего хотим от пары"
    intro = extract_md_subsection(markdown_text, intro_heading)
    if not intro:
        intro = extract_md_subsection(markdown_text, "Чего хотим от пары")
    if intro:
        intro = re.sub(
            r"^### (?:A\.\s*)?Чего хотим от пары\s*$",
            "## A. Чего хотим от пары",
            intro,
            count=1,
            flags=re.MULTILINE,
        ).strip() + "\n"
        # Only heading + prose paragraphs (no tables / калибровка / «Успех пары»).
        prose: list[str] = []
        for line in intro.splitlines():
            if line.startswith("## "):
                prose.append(line)
                continue
            if line.strip() == "---" or line.strip().startswith("|"):
                break
            if line.strip().lower().startswith("успех пары"):
                break
            if line.startswith("#"):
                break
            prose.append(line)
        intro = "\n".join(prose).strip() + "\n"

    # Take B/C only from the source — ignore everything else (сценарий, D, E…).
    b_block = re.search(
        r"(^## B\..*?)(?=^## [A-ZА-Я]\.|\Z)",
        markdown_text,
        re.MULTILINE | re.DOTALL,
    )
    c_block = re.search(
        r"(^## C\..*?)(?=^## [A-ZА-Я]\.|\Z)",
        markdown_text,
        re.MULTILINE | re.DOTALL,
    )
    chunks: list[str] = []
    if b_block:
        chunks.append(b_block.group(1).strip())
    if c_block:
        chunks.append(c_block.group(1).strip())
    if not chunks:
        s6 = re.search(r"(^## 6\..*?)(?=^## \d+\.|\Z)", markdown_text, re.MULTILINE | re.DOTALL)
        s9 = re.search(r"(^## 9\..*?)(?=^## \d+\.|\Z)", markdown_text, re.MULTILINE | re.DOTALL)
        if s6:
            chunks.append("## B. Ход пары\n\n" + s6.group(1).split("\n", 1)[1].strip())
        if s9:
            chunks.append("## C. Если сбились\n\n" + s9.group(1).split("\n", 1)[1].strip())
    md = ("\n\n".join(chunks) + "\n") if chunks else ""

    md = re.sub(r"\[([^\]]+)\]\((?:\.\./)+[^)]+\)", r"\1", md)

    # Drop «Ориентир времени» if it leaked into B/C, and ~мин column (time budget).
    lines = md.splitlines()
    filtered: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if "ориентир времени" in line.lower():
            i += 1
            while i < len(lines) and (
                lines[i].strip().startswith("|") or not lines[i].strip()
            ):
                i += 1
            continue
        filtered.append(re.sub(r"\s*\(кратко\)", "", line, flags=re.IGNORECASE))
        i += 1
    md = _drop_table_column("\n".join(filtered).strip(), "~мин")

    parts = [p for p in (intro.strip() if intro else "", md) if p]
    result = "\n\n".join(parts) + "\n"
    # Safety: never ship сценарий / D / E headings.
    for banned in (
        "Сценарий пары",
        "Проектирование",
        "Карточка урока",
        "Ориентир времени",
    ):
        if banned.lower() in result.lower() and banned != "Ориентир времени":
            # Strip any leftover ##/### section with banned title
            result = strip_md_sections_matching(
                result, rf".*{re.escape(banned)}.*"
            )
            # also ### level: crude drop
            result = re.sub(
                rf"(^### .*{re.escape(banned)}.*\n.*?)(?=^#{{1,3}} |\Z)",
                "",
                result,
                flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
            )
    return result.strip() + "\n"


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
    course_id: int | None = None,
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
    if course_id is not None:
        md = rewrite_canvas_page_links(md, course_id)
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
