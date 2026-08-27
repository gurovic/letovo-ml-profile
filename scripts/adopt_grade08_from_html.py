"""Adopt grade-8 program from downloaded ai-school-program HTML into docs/ktp."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TMP = ROOT / "_tmp_ai_program"
OUT_UNIFIED = ROOT / "docs" / "ktp" / "grade-08.unified.ktp.md"
OUT_08 = ROOT / "docs" / "ktp" / "08.md"
OUT_JSON = ROOT / "docs" / "ktp" / "grade-08.modules.json"
BUILD_SCRIPT = ROOT / "scripts" / "build_ktp_08.py"

MODULE_PATHS = {
    1: "modules/08_01_functions_recursion/",
    2: "modules/08_02_carsharing_pandas_lr/",
    3: "modules/08_03_titanic_eda/",
    4: "modules/08_04_mnist_knn/",
    5: "modules/08_05_shop_feature_engineering/",
    6: "modules/08_06_ab_startup/",
    7: "modules/08_07_bank_arrays_search/",
    8: "modules/08_08_logistics_clustering/",
    9: "modules/08_10_churn_logreg/",
    10: "modules/08_11_virtual_polygon/",
}


def load_grade8_blocks() -> list[dict]:
    data = json.loads((TMP / "program_data.json").read_text(encoding="utf-8"))
    gm = next(x for x in data["grade_modules_unified_variants"] if x.get("grade") == 8)
    return gm["blocks"]


def parse_modules(blocks: list[dict]) -> tuple[str, list[dict]]:
    preamble = ""
    modules: list[dict] = []
    cur = None
    for b in blocks:
        kind = b.get("kind")
        text = (b.get("text") or "").strip()
        codes = b.get("codes") or []
        if kind == "paragraph" and not modules and cur is None:
            preamble = text
            continue
        if kind == "subheading" and text.startswith("Модуль"):
            m = re.match(r"Модуль\s+(\d+)\.\s*(.+)", text)
            num = int(m.group(1)) if m else len(modules) + 1
            cur = {
                "num": num,
                "title": text,
                "scenario": "",
                "note": "",
                "themes": [],
                "codes": [],
            }
            modules.append(cur)
            continue
        if cur is None:
            continue
        if kind == "paragraph" and text.startswith("Сюжет:"):
            cur["scenario"] = text.removeprefix("Сюжет:").strip()
            continue
        if kind == "paragraph" and text.startswith("Комментарий:"):
            cur["note"] = text.removeprefix("Комментарий:").strip()
            continue
        if kind == "paragraph" and text:
            cur["themes"].append(text)
            cur["codes"].append(list(codes))
    return preamble, modules


def render_unified(preamble: str, modules: list[dict]) -> str:
    lines = [
        "# 8 класс (4ч в неделю) — тематическое планирование",
        "",
        f"> {preamble}",
        "",
    ]
    for mod in modules:
        lines.append(f"## {mod['title']}")
        lines.append(f"Сюжет: {mod['scenario']}")
        if mod["note"]:
            lines.append(f"Комментарий: {mod['note']}")
        for theme, codes in zip(mod["themes"], mod["codes"]):
            suffix = " {" + " ".join(codes) + "}" if codes else ""
            lines.append(f"{theme}{suffix}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_08_md(preamble: str, modules: list[dict]) -> str:
    total = sum(len(m["themes"]) for m in modules)
    load_pairs = 68
    reserve = load_pairs - total

    grid_rows = []
    pair = 1
    for m in modules:
        n = len(m["themes"])
        end = pair + n - 1
        grid_rows.append(f"| M{m['num']} | {n} | {pair}–{end} |")
        pair = end + 1

    parts = [
        "# КТП: 8 класс",
        "",
        "Статус: Draft 4",
        "",
        "Канонический документ профиля. Источник сетки: `aguschin/ai-school-program` "
        "(`program.html` → `grade_modules_unified_variants`, grade 8). "
        "Справочник `reference/` — только для сравнения, **не редактируется**.",
        "",
        "| Параметр | Значение |",
        "|---|---|",
        "| Нагрузка | 4 ч/нед |",
        "| Учебных недель | 34 |",
        f"| Пар в сетке модулей | **{total}** |",
        f"| Календарная ёмкость | {load_pairs} пар (= 4 × 34 / 2 ч) |",
        f"| Резерв | **{reserve}** пар (олимпиады / углубление / гибкость) |",
        "| Правило | 1 тема = 1 пара = 2 академических часа = **80 минут** проведения |",
        f"| Академических часов (сетка) | {total * 2} (= {total} × 2) |",
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
        "| Модуль | Пар | Диапазон КТП |",
        "|---|---:|---|",
        *grid_rows,
        "",
        "---",
        "",
    ]

    pair = 1
    for m in modules:
        n = len(m["themes"])
        end = pair + n - 1
        path = MODULE_PATHS.get(m["num"], "")
        parts.append(f"## {m['title']} ({n} пар)")
        parts.append("")
        parts.append(f"**Сюжет:** {m['scenario']}")
        parts.append("")
        if m["note"]:
            parts.append(f"*{m['note']}*")
            parts.append("")
        if path:
            parts.append(f"**Материалы:** [{path}](../../{path}) (пары {pair}–{end})")
            parts.append("")
        parts.append("| # | Тема |")
        parts.append("|---|---|")
        for i, theme in enumerate(m["themes"]):
            parts.append(f"| {pair + i} | {theme} |")
        parts.append("")
        pair = end + 1

    parts.extend(
        [
            "---",
            "",
            "## Резерв и вне сетки",
            "",
            f"{reserve} пар календарной ёмкости не закреплены за модулями: олимпиадные задачи "
            "(ВсОШ по ИИ, AI Challenge, НТО и др.), углубление по готовности группы, доработка артефактов.",
            "",
            "Модуль `08_09_courier_dp` (DP и игры) **снят с сетки 8 класса** в программе-источнике; "
            "динамическое программирование остаётся в тематическом бэклоге / 9+ при необходимости. "
            "Папку не удалять без явного решения — материалы могут переехать.",
            "",
            "---",
            "",
            "## Карта инструментов",
            "",
            "Карта инструментов (Draft 3, 11 модулей) устарела по номерам пар и составу. "
            "Обновляется после выравнивания материалов модулей под Draft 4.",
            "",
            "Правило: инструмент появляется не раньше первой пары модуля, где он в теме КТП. "
            "**venv / CLI / bash — 9 класс** (не модуль оттока 8 класса).",
            "",
        ]
    )
    return "\n".join(parts)


BUILD_SCRIPT_BODY = r'''#!/usr/bin/env python3
"""Generate docs/ktp/08.md from docs/ktp/grade-08.modules.json (Draft 4)."""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "docs" / "ktp" / "grade-08.modules.json"
OUT = REPO / "docs" / "ktp" / "08.md"
TARGET_PAIRS = 68


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    preamble = payload["preamble"]
    modules = payload["modules"]
    paths = payload["module_paths"]
    total = sum(len(m["themes"]) for m in modules)
    reserve = TARGET_PAIRS - total

    lines: list[str] = [
        "# КТП: 8 класс",
        "",
        "Статус: Draft 4",
        "",
        "Канонический документ профиля. Источник сетки: `aguschin/ai-school-program` "
        "(`program.html` → unified KTP grade 8). Справочник `reference/` — только для сравнения, "
        "**не редактируется**.",
        "",
        "| Параметр | Значение |",
        "|---|---|",
        "| Нагрузка | 4 ч/нед |",
        "| Учебных недель | 34 |",
        f"| Пар в сетке модулей | **{total}** |",
        f"| Календарная ёмкость | {TARGET_PAIRS} пар (= 4 × 34 / 2 ч) |",
        f"| Резерв | **{reserve}** пар (олимпиады / углубление / гибкость) |",
        "| Правило | 1 тема = 1 пара = 2 академических часа = **80 минут** проведения |",
        f"| Академических часов (сетка) | {total * 2} (= {total} × 2) |",
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
        "| Модуль | Пар | Диапазон КТП |",
        "|---|---:|---|",
    ]
    pair = 1
    for m in modules:
        n = len(m["themes"])
        end = pair + n - 1
        lines.append(f"| M{m['num']} | {n} | {pair}–{end} |")
        pair = end + 1
    lines += ["", "---", ""]

    pair = 1
    for m in modules:
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
        path = paths.get(str(m["num"])) or paths.get(m["num"]) or ""
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
        "## Резерв и вне сетки",
        "",
        f"{reserve} пар календарной ёмкости не закреплены за модулями: олимпиадные задачи "
        "(ВсОШ по ИИ, AI Challenge, НТО и др.), углубление по готовности группы, доработка артефактов.",
        "",
        "Модуль `08_09_courier_dp` (DP и игры) **снят с сетки 8 класса** в программе-источнике; "
        "динамическое программирование остаётся в тематическом бэклоге / 9+ при необходимости. "
        "Папку не удалять без явного решения — материалы могут переехать.",
        "",
        "---",
        "",
        "## Карта инструментов",
        "",
        "Карта инструментов (Draft 3, 11 модулей) устарела по номерам пар и составу. "
        "Обновляется после выравнивания материалов модулей под Draft 4.",
        "",
        "Правило: инструмент появляется не раньше первой пары модуля, где он в теме КТП. "
        "**venv / CLI / bash — 9 класс** (не модуль оттока 8 класса).",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} ({total} content pairs, reserve {reserve})")


if __name__ == "__main__":
    main()
'''


def main() -> None:
    blocks = load_grade8_blocks()
    preamble, modules = parse_modules(blocks)
    assert [m["num"] for m in modules] == list(range(1, 11)), [m["num"] for m in modules]
    total = sum(len(m["themes"]) for m in modules)
    print("modules", len(modules), "pairs", total)
    for m in modules:
        print(f"  M{m['num']}: {len(m['themes'])} — {m['title']}")

    payload = {
        "source": "aguschin/ai-school-program program.html grade_modules_unified_variants grade=8",
        "preamble": preamble,
        "modules": modules,
        "module_paths": {str(k): v for k, v in MODULE_PATHS.items()},
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", OUT_JSON)

    OUT_UNIFIED.write_text(render_unified(preamble, modules), encoding="utf-8")
    print("wrote", OUT_UNIFIED)

    OUT_08.write_text(render_08_md(preamble, modules), encoding="utf-8")
    print("wrote", OUT_08)

    BUILD_SCRIPT.write_text(BUILD_SCRIPT_BODY, encoding="utf-8")
    print("wrote", BUILD_SCRIPT)

    thematic_src = TMP / "grade-08.md"
    thematic_dst = ROOT / "docs" / "ktp" / "08_thematic_program.md"
    header = (
        "# Предметная программа: 8 класс\n\n"
        "Статус: Draft 4\n\n"
        "Источник: `aguschin/ai-school-program` → `data/program/grade-08.md` "
        "(тематический план; операционная сетка пар — [08.md](08.md)).\n\n"
        "---\n\n"
    )
    thematic_dst.write_text(header + thematic_src.read_text(encoding="utf-8"), encoding="utf-8")
    print("wrote", thematic_dst)


if __name__ == "__main__":
    main()
