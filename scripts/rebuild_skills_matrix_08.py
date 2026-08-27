#!/usr/bin/env python3
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
data = json.loads((root / "docs/ktp/grade-08.modules.json").read_text(encoding="utf-8"))
lines = [
    "# Матрица навыков: 8 класс",
    "",
    "Статус: Draft 3 (сетка КТП Draft 4 — **58** обяз. + **5** доп. DP)",
    "",
    "По одной строке на пару КТП. Темы — из [08.md](08.md). Ячейки навыков заполнять при design-lesson.",
    "",
    "| # | Модуль | Урок | Узнали EDA | Отработали EDA | Узнали ML | Отработали ML | Узнали Python | Отработали Python | Узнали алг. и стр. данных | Отработали алг. и стр. данных |",
    "|---:|---|---|---|---|---|---|---|---|---|---|",
]
pair = 1
for m in data["modules"] + data.get("optional_modules", []):
    short = re.sub(r"^Модуль\s+\d+( \(доп\))?\.\s*", "", m["title"])
    label = f"M{m['num']}" + (" (доп.)" if m.get("note") else "") + f". {short}"
    for theme in m["themes"]:
        t = theme.replace("|", "/")
        if len(t) > 80:
            t = t[:77] + "…"
        lines.append(f"| {pair} | {label} | {t} | | | | | | | | |")
        pair += 1
lines += ["", "Индекс КТП: [07_KTP.md](../07_KTP.md).", ""]
(root / "docs/ktp/08_skills_matrix.md").write_text("\n".join(lines), encoding="utf-8")
print("rows", pair - 1)
