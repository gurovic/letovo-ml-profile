#!/usr/bin/env python3
"""Generate docs/ktp/08.md from docs/ktp/grade-08.modules.json (Draft 4)."""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "docs" / "ktp" / "grade-08.modules.json"
OUT = REPO / "docs" / "ktp" / "08.md"
OUT_UNIFIED = REPO / "docs" / "ktp" / "grade-08.unified.ktp.md"
TARGET_PAIRS = 68


def _path(paths: dict, num: int) -> str:
    return paths.get(str(num)) or paths.get(num) or ""


def render_08(payload: dict) -> str:
    preamble = payload["preamble"]
    modules = payload["modules"]
    optional = payload.get("optional_modules") or []
    paths = payload["module_paths"]

    core = sum(len(m["themes"]) for m in modules)
    opt = sum(len(m["themes"]) for m in optional)
    scheduled = core + opt
    reserve = TARGET_PAIRS - scheduled

    lines: list[str] = [
        "# КТП: 8 класс",
        "",
        "Статус: Draft 4",
        "",
        "Канонический документ профиля. Источник основной сетки: `aguschin/ai-school-program` "
        "(`program.html` → unified KTP grade 8). Модуль DP сохранён у нас как **дополнительный** "
        "в конце года. Справочник `reference/` — только для сравнения, **не редактируется**.",
        "",
        "| Параметр | Значение |",
        "|---|---|",
        "| Нагрузка | 4 ч/нед |",
        "| Учебных недель | 34 |",
        f"| Пар основной сетки (M1–M10) | **{core}** |",
        f"| Пар доп. модуля DP (M11) | **{opt}** |",
        f"| Пар в расписании модулей | **{scheduled}** |",
        f"| Календарная ёмкость | {TARGET_PAIRS} пар (= 4 × 34 / 2 ч) |",
        f"| Свободный резерв | **{reserve}** пар (олимпиады / гибкость) |",
        "| Правило | 1 тема = 1 пара = 2 академических часа = **80 минут** проведения |",
        f"| Академических часов (расписание) | {scheduled * 2} (= {scheduled} × 2) |",
        "",
        "**Отработка:** строки «Практика: …» — серия задач на уже введённый навык "
        "(Foundation §5 принцип 8, Pedagogy §2). При дефиците часов сокращать число новых тем "
        "и обзорных пар, не практику.",
        "",
        "Индекс КТП: [07_KTP.md](../07_KTP.md).",
        "",
        "**Описания модулей:** [08_module_descriptions.md](08_module_descriptions.md).",
        "",
        "**Предметная программа (не по парам):** [08_thematic_program.md](08_thematic_program.md).",
        "",
        "**Стек после 8 класса:** [08_tech_stack_skills.md](08_tech_stack_skills.md).",
        "",
        f"**Среда (из программы-источника):** {preamble}",
        "",
        "### Сетка модулей",
        "",
        "| Модуль | Пар | Диапазон КТП | Обязательность |",
        "|---|---:|---|---|",
    ]

    pair = 1
    for m in modules:
        n = len(m["themes"])
        end = pair + n - 1
        lines.append(f"| M{m['num']} | {n} | {pair}–{end} | обязательный |")
        pair = end + 1
    for m in optional:
        n = len(m["themes"])
        end = pair + n - 1
        lines.append(f"| M{m['num']} | {n} | {pair}–{end} | **дополнительный** |")
        pair = end + 1

    lines += ["", "---", ""]

    pair = 1
    for m in modules + optional:
        n = len(m["themes"])
        end = pair + n - 1
        lines.append(f"## {m['title']} ({n} пар)")
        lines.append("")
        lines.append(f"**Сюжет:** {m['scenario']}")
        lines.append("")
        note = m.get("note") or ""
        if note:
            lines.append(f"*{note}*")
            lines.append("")
        path = _path(paths, m["num"])
        if path:
            lines.append(f"**Материалы:** [{path}](../../{path}) (пары {pair}–{end})")
            lines.append("")
        lines.append("| # | Тема |")
        lines.append("|---|---|")
        for i, theme in enumerate(m["themes"]):
            lines.append(f"| {pair + i} | {theme} |")
        lines.append("")
        pair = end + 1

    lines += [
        "---",
        "",
        "## Резерв",
        "",
        f"{reserve} пар календарной ёмкости свободны после M1–M11: олимпиадные задачи "
        "(ВсОШ по ИИ, AI Challenge, НТО и др.), углубление, доработка артефактов. "
        "Доп. модуль DP уже занимает часть бывшего резерва — его не вырезать ради «пустого» запаса.",
        "",
        "---",
        "",
        "## Карта инструментов",
        "",
        "Карта инструментов (Draft 3) устарела по номерам пар и составу. "
        "Обновляется после выравнивания материалов модулей под Draft 4.",
        "",
        "Правило: инструмент появляется не раньше первой пары модуля, где он в теме КТП. "
        "**venv / CLI / bash — 9 класс** (не модуль оттока 8 класса).",
        "",
    ]
    return "\n".join(lines)


def render_unified(payload: dict) -> str:
    preamble = payload["preamble"]
    # Keep source preamble, but clarify DP is our optional add-on
    lines = [
        "# 8 класс (4ч в неделю) — тематическое планирование",
        "",
        f"> {preamble} Доп. у нас: модуль DP в конце года (M11), не обязателен.",
        "",
    ]
    for m in payload["modules"] + (payload.get("optional_modules") or []):
        lines.append(f"## {m['title']}")
        lines.append(f"Сюжет: {m['scenario']}")
        if m.get("note"):
            lines.append(f"Комментарий: {m['note']}")
        codes_list = m.get("codes") or [[] for _ in m["themes"]]
        for theme, codes in zip(m["themes"], codes_list):
            suffix = " {" + " ".join(codes) + "}" if codes else ""
            lines.append(f"{theme}{suffix}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    OUT.write_text(render_08(payload), encoding="utf-8")
    OUT_UNIFIED.write_text(render_unified(payload), encoding="utf-8")
    core = sum(len(m["themes"]) for m in payload["modules"])
    opt = sum(len(m["themes"]) for m in payload.get("optional_modules") or [])
    print(f"Wrote {OUT} and {OUT_UNIFIED} (core {core} + optional {opt} = {core + opt})")


if __name__ == "__main__":
    main()
