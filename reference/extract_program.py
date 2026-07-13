#!/usr/bin/env python3
"""Extract program.html DATA into JSON and Markdown."""

from __future__ import annotations

import json
import re
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML_PATH = ROOT / "program.html"
JSON_PATH = ROOT / "program_data.json"
MD_PATH = ROOT / "COURSE_PROGRAM_DRAFT.md"

SUBJECT_LABELS = {
    "mathematics": "Математика (M)",
    "programming": "Программирование (P)",
    "ml": "ML (L)",
}

SECTION_LABELS = {
    "mathematics": "Математика",
    "programming": "Программирование",
    "ml": "ML",
    "other": "Прочее",
    "Олимпиадные тренировки и календарь олимпиад": "Олимпиадные тренировки и календарь олимпиад",
    "Научно-исследовательская работа (статьи)": "Научно-исследовательская работа (статьи)",
    "Проекты и стажировки": "Проекты и стажировки",
    "ML (другие домены обзорно)": "ML (другие домены обзорно)",
}


def load_data() -> dict:
    text = HTML_PATH.read_text(encoding="utf-8")
    match = re.search(r"const DATA = (\{.*?\});\s*\n", text, re.DOTALL)
    if not match:
        raise RuntimeError("DATA block not found in program.html")
    return json.loads(match.group(1))


def fmt_text(text: str) -> str:
    text = unescape(text or "")
    text = re.sub(r"==([^=]+)==", r"**\1**", text)
    text = re.sub(r"~~([^~]+)~~", r"~~\1~~", text)
    return text.strip()


def codes_suffix(codes: list[str]) -> str:
    if not codes:
        return ""
    return " `" + "`, `".join(codes) + "`"


def extract_backlog(html: str) -> list[str]:
    match = re.search(
        r'<div class="panel backlog-panel">.*?<ul>(.*?)</ul>',
        html,
        re.DOTALL,
    )
    if not match:
        return []
    items = re.findall(r"<li>(.*?)</li>", match.group(1), re.DOTALL)
    out = []
    for item in items:
        item = re.sub(r"<[^>]+>", "", item)
        item = unescape(re.sub(r"\s+", " ", item)).strip()
        if item:
            out.append(item)
    return out


def render_blocks(blocks: list[dict], include_hidden: bool = True) -> list[str]:
    lines: list[str] = []
    for block in blocks:
        if block.get("hidden") and not include_hidden:
            continue
        kind = block.get("kind", "paragraph")
        text = fmt_text(block.get("text", ""))
        suffix = codes_suffix(block.get("codes") or [])
        hidden = " *(скрытый блок в HTML)*" if block.get("hidden") else ""

        if kind == "subheading":
            level = min(4, 2 + int(block.get("level") or 1))
            lines.append(f"{'#' * level} {text}{suffix}{hidden}")
            lines.append("")
        elif kind == "bullet":
            lines.append(f"- {text}{suffix}{hidden}")
        else:
            if text:
                lines.append(f"{text}{suffix}{hidden}")
                lines.append("")
    return lines


def render_grade_module(module: dict) -> list[str]:
    lines = [f"## {module.get('title') or module.get('grade')}", ""]
    blocks = module.get("blocks") or []

    by_section: dict[str, list[dict]] = {}
    order: list[str] = []
    for block in blocks:
        section = block.get("section") or "other"
        if section not in by_section:
            by_section[section] = []
            order.append(section)
        by_section[section].append(block)

    for section in order:
        label = SECTION_LABELS.get(section, section)
        lines.append(f"### {label}")
        lines.append("")
        lines.extend(render_blocks(by_section[section]))
        lines.append("")

    return lines


def render_registries(registries: list[dict]) -> list[str]:
    lines = ["## Приложение: карта абстракций (реестр кодов)", ""]
    current_subject = None
    for item in sorted(registries, key=lambda x: (x.get("subject", ""), x.get("code", ""))):
        subject = item.get("subject")
        if subject != current_subject:
            current_subject = subject
            lines.extend(["", f"### {SUBJECT_LABELS.get(subject, subject)}", ""])
        code = item.get("code", "")
        name = item.get("name", "")
        summary = item.get("summary", "")
        first = item.get("first_grade_text") or item.get("first_grade") or "?"
        prereqs = ", ".join(item.get("prereqs") or []) or "—"
        lines.append(f"- **{code} — {name}** (первое появление: {first} класс; пререквизиты: {prereqs})")
        if summary:
            lines.append(f"  {summary}")
    lines.append("")
    return lines


def build_markdown(data: dict, backlog: list[str]) -> str:
    lines: list[str] = [
        "# Черновик черновика программы курса",
        "",
        "> **Источник:** [aguschin/ai-school-program — program.html](https://github.com/aguschin/ai-school-program/blob/main/program.html)",
        f"> **Извлечено из:** `{data.get('source', 'program.html')}`",
        "> **Статус:** справочный черновик; не часть операционного мануала. Не согласован с Foundation.",
        "> **Назначение:** исходный материал для проектирования профиля «Машинное обучение» (Летово).",
        "",
        "---",
        "",
        "## Обзор",
        "",
        "Профильная школьная программа по ИИ и машинному обучению (7–11 класс): единая траектория от программирования и анализа данных к ML.",
        "",
        "### Три предметные линии",
        "",
        "- **Математика (M)** — число, функция, вероятность, распределение, вектор, матрица, производная, оптимизация, энтропия.",
        "- **Программирование (P)** — Python и инструменты: типы, функции, структуры данных, файлы, библиотеки, API, Git, окружение.",
        "- **ML (L)** — объект/признак/таргет, выборка и валидация, модель и loss, линейные модели, ансамбли, оптимизация, нейросети, CV, NLP.",
        "",
        "### Принципы (из исходника)",
        "",
        "- Спиральность: от интуиции к строгости.",
        "- Табличные данные раньше CV/NLP.",
        "- Валидация важнее сложности модели.",
        "- Инженерная дисциплина и воспроизводимость.",
        "- Этика и риски ИИ — в контексте тем, не отдельным блоком.",
        "",
        "### Стадии по классам (кратко)",
        "",
    ]

    for stage in data.get("stages") or []:
        level = fmt_text(stage.get("level") or "")
        focus = fmt_text(stage.get("focus") or "")
        lines.append(f"- **{stage.get('stage')}** — {level}: {focus}")
    lines.extend(["", "---", "", "# Полный текст тем и модулей", ""])

    for module in data.get("grade_modules") or []:
        lines.extend(render_grade_module(module))

    spec = data.get("spec_module")
    if spec:
        lines.extend(["---", "", f"# Спецкурс: {spec.get('title')}", ""])
        lines.extend(render_blocks(spec.get("blocks") or []))

    if backlog:
        lines.extend(["---", "", "## Бэклог — обсудить (из исходника)", ""])
        for item in backlog:
            lines.append(f"- {item}")
        lines.append("")

    violations = data.get("violations") or []
    lines.extend(["---", "", "## Нарушения пререквизитов", ""])
    if violations:
        for v in violations:
            lines.append(f"- {v}")
    else:
        lines.append("Нарушений не зафиксировано в исходных данных.")
    lines.append("")

    lines.extend(render_registries(data.get("registries") or []))
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    data = load_data()
    backlog = extract_backlog(html)

    JSON_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    MD_PATH.write_text(build_markdown(data, backlog), encoding="utf-8")
    print(f"Wrote {JSON_PATH.name} ({JSON_PATH.stat().st_size} bytes)")
    print(f"Wrote {MD_PATH.name} ({MD_PATH.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
