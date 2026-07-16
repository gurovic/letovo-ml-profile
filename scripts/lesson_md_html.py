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


def prepare_lesson_md_for_canvas_teacher(markdown_text: str) -> str:
    """Teacher plan for Canvas: conduct the pair, not design the course.

    Keeps zones A–C (scenario / flow / if stuck). Drops D (design) and E (§13 export).
    Softens the Canvas ID row. Repo-only relative links (UNIT, KTP, other LESSON)
    become plain labels so the wiki does not show broken paths.
    """
    md = markdown_text
    # Draft 5: D / E
    md = strip_md_sections_matching(md, r"[DE]\..*")
    # Legacy orientation LESSON (pair 1): author blocks, not live teaching script
    md = strip_md_sections(
        md,
        {
            "2. Зачем существует урок",
            "3. Центральная идея",
            "5. Профессиональный контекст",
            "7. Решения учащегося",
        },
    )

    out_lines: list[str] = []
    for line in md.splitlines():
        if re.match(r"\|\s*\*\*Canvas\*\*\s*\|", line) or re.match(
            r"\|\s*Canvas\s*\|", line
        ):
            out_lines.append(
                "| **В модуле** | Ниже плана: «Ноутбук урока» и «Домашнее задание» "
                "(если есть). «Решения» — скрытый элемент только для преподавателя |"
            )
            continue
        out_lines.append(line)
    md = "\n".join(out_lines)

    # Drop repo-relative links that are useless in Canvas (keep label).
    # Keep bare filenames like lesson.ipynb — rewrite_notebook_links handles those.
    md = re.sub(
        r"\[([^\]]+)\]\((?:\.\./)+[^)]+\)",
        r"\1",
        md,
    )

    # Teacher Canvas page should contain only conduct blocks.
    # For Draft 5 lessons keep B/C; for legacy orientation (pair 1) fallback to
    # operational blocks "6. Структура урока" and "9. Ожидаемые ошибки".
    b_block = re.search(r"(^## B\..*?)(?=^## [A-ZА-Я]\.|\Z)", md, re.MULTILINE | re.DOTALL)
    c_block = re.search(r"(^## C\..*?)(?=^## [A-ZА-Я]\.|\Z)", md, re.MULTILINE | re.DOTALL)
    if b_block and c_block:
        md = b_block.group(1).strip() + "\n\n" + c_block.group(1).strip() + "\n"
    else:
        s6 = re.search(r"(^## 6\..*?)(?=^## \d+\.|\Z)", md, re.MULTILINE | re.DOTALL)
        s9 = re.search(r"(^## 9\..*?)(?=^## \d+\.|\Z)", md, re.MULTILINE | re.DOTALL)
        chunks: list[str] = []
        if s6:
            chunks.append("## B. Ход пары\n\n" + s6.group(1).split("\n", 1)[1].strip())
        if s9:
            chunks.append("## C. Если сбились\n\n" + s9.group(1).split("\n", 1)[1].strip())
        if chunks:
            md = "\n\n".join(chunks) + "\n"

    # Do not publish the "Ориентир времени" table in Canvas teacher plans.
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
    md = "\n".join(filtered)
    return md


def extract_md_subsection(markdown_text: str, heading: str) -> str:
    """Return ``### heading`` block (including heading) or empty string."""
    pattern = re.compile(
        rf"(^### {re.escape(heading)}\s*\n.*?)(?=^### |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    m = pattern.search(markdown_text)
    return m.group(1).strip() + "\n" if m else ""


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
