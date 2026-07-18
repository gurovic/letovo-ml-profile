#!/usr/bin/env python3
"""Build concept-rivers viz data from reference + curated taxonomy → docs/ktp/."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "reference" / "program_data.json"
TAX = REPO / "docs" / "ktp" / "concept_taxonomy.json"
OUT_JS = REPO / "docs" / "ktp" / "concept_rivers_data.js"
OUT_JSON = REPO / "docs" / "ktp" / "concept_rivers_data.json"

OUR_M8 = [
    {"id": "08_01", "short": "M1 Функции", "codes": ["P10", "M09", "L01", "L02", "L05", "L06", "P01"]},
    {"id": "08_02", "short": "M2 Pandas/LR", "codes": ["P20", "L03", "L05", "L06", "L09", "M12", "P15"]},
    {"id": "08_03", "short": "M3 Titanic EDA", "codes": ["L03", "M12", "M11", "M27", "P20"]},
    {"id": "08_04", "short": "M4 kNN", "codes": ["L05", "L06", "L09", "L10", "M07", "M16", "P12"]},
    {"id": "08_05", "short": "M5 Features", "codes": ["L04", "P10", "P20", "P15"]},
    {"id": "08_06", "short": "M6 A/B", "codes": ["L07", "L08", "M12", "M27", "M30", "L09"]},
    {"id": "08_07", "short": "M7 Поиск/сорт", "codes": ["P11", "P13", "P14", "M10"]},
    {"id": "08_08", "short": "M8 Структуры", "codes": ["P08", "P09", "L12", "L13", "L03"]},
    {"id": "08_09", "short": "M9 DP", "codes": ["P16", "P10", "M10"]},
    {"id": "08_10", "short": "M10 Логрег", "codes": ["L05", "L06", "L09", "L11", "M09", "M20", "P17"]},
    {"id": "08_11", "short": "M11 Градиент", "codes": ["M21", "M22", "M24", "L14"]},
]


def clean(s: str) -> str:
    if not s:
        return ""
    return s.replace("==", "").replace("~~", "").strip()


def prereq_layers(regs: dict[str, dict]) -> dict[str, int]:
    memo: dict[str, int] = {}

    def depth(code: str, stack: set[str]) -> int:
        if code in memo:
            return memo[code]
        if code in stack or code not in regs:
            return 0
        prereqs = regs[code].get("prereqs") or []
        if not prereqs:
            memo[code] = 0
            return 0
        stack.add(code)
        memo[code] = 1 + max(depth(p, stack) for p in prereqs)
        stack.remove(code)
        return memo[code]

    for code in regs:
        depth(code, set())
    return memo


def main() -> None:
    d = json.loads(SRC.read_text(encoding="utf-8"))
    tax = json.loads(TAX.read_text(encoding="utf-8"))
    regs = {r["code"]: r for r in d["registries"]}
    usage = d.get("usage_map") or {}
    layers = prereq_layers(regs)

    code_to_family: dict[str, dict] = {}
    families = []
    for i, fam in enumerate(tax["families"]):
        entry = {
            "id": fam["id"],
            "subject": fam["subject"],
            "title": fam["title"],
            "blurb": fam.get("blurb") or "",
            "order": i,
            "codes": list(fam["codes"]),
        }
        families.append(entry)
        for code in fam["codes"]:
            if code in code_to_family:
                raise SystemExit(f"code {code} in two families")
            code_to_family[code] = entry

    missing = sorted(set(regs) - set(code_to_family))
    extra = sorted(set(code_to_family) - set(regs))
    if missing:
        raise SystemExit(f"taxonomy missing codes: {missing}")
    if extra:
        raise SystemExit(f"taxonomy unknown codes: {extra}")

    intensity: dict[str, dict[int, int]] = defaultdict(lambda: defaultdict(int))
    snippets: dict[str, dict[int, list[str]]] = defaultdict(lambda: defaultdict(list))
    for code, hits in usage.items():
        for h in hits:
            g = h.get("grade")
            if g is None:
                continue
            g = int(g)
            intensity[code][g] += 1
            text = clean(h.get("text") or "")
            if text and len(snippets[code][g]) < 3:
                snippets[code][g].append(text[:140])

    concepts = []
    for code, r in regs.items():
        fam = code_to_family[code]
        grades = sorted(intensity[code].keys()) or (
            [int(r["first_grade"])] if r.get("first_grade") else []
        )
        first = int(r.get("first_grade") or (grades[0] if grades else 7))
        by_g = {str(g): intensity[code].get(g, 0) for g in range(7, 12)}
        if by_g.get(str(first), 0) == 0:
            by_g[str(first)] = 1
        our = [m["id"] for m in OUR_M8 if code in m["codes"]]
        concepts.append(
            {
                "code": code,
                "name": r["name"],
                "subject": r["subject"],
                "summary": clean(r.get("summary") or ""),
                "prereqs": r.get("prereqs") or [],
                "layer": layers.get(code, 0),
                "first": first,
                "grades": grades if grades else [first],
                "intensity": by_g,
                "snippets": {str(g): snippets[code][g] for g in range(7, 12) if snippets[code][g]},
                "our_modules": our,
                "span": len([g for g in range(7, 12) if by_g.get(str(g), 0) > 0]),
                "family_id": fam["id"],
                "family": fam["title"],
                "family_blurb": fam["blurb"],
                "family_order": fam["order"],
            }
        )

    concepts.sort(key=lambda c: (c["family_order"], c["layer"], c["code"]))
    by_code = {c["code"]: c for c in concepts}

    # Per-grade: which families gain new births (structured map)
    grade_families: dict[str, list[dict]] = {}
    for g in range(7, 12):
        buckets: dict[str, list[str]] = defaultdict(list)
        for c in concepts:
            if c["first"] == g:
                buckets[c["family_id"]].append(c["code"])
        rows = []
        for fam in families:
            codes = buckets.get(fam["id"]) or []
            if not codes:
                continue
            codes.sort(key=lambda code: (by_code[code]["layer"], code))
            rows.append(
                {
                    "id": fam["id"],
                    "title": fam["title"],
                    "blurb": fam["blurb"],
                    "subject": fam["subject"],
                    "order": fam["order"],
                    "birth_codes": codes,
                }
            )
        grade_families[str(g)] = rows

    showcase_codes: list[str] = []
    for subj in ("mathematics", "programming", "ml"):
        pool = [c for c in concepts if c["subject"] == subj]
        pool.sort(key=lambda c: (-c["span"], -sum(c["intensity"].values()), c["code"]))
        showcase_codes.extend(c["code"] for c in pool[:12])

    payload = {
        "title": "Реки концепций",
        "subtitle": "Развитие абстракций M / P / L → модули нашего 8 класса",
        "source": "reference/program_data.json + docs/ktp/concept_taxonomy.json",
        "grades": [7, 8, 9, 10, 11],
        "subjects": {
            "mathematics": {"label": "Математика", "short": "M"},
            "programming": {"label": "Программирование", "short": "P"},
            "ml": {"label": "ML", "short": "L"},
        },
        "families": families,
        "grade_families": grade_families,
        "stages": [
            {
                "grade": s["grade"],
                "level": clean(s.get("level") or ""),
                "focus": clean(s.get("focus") or ""),
            }
            for s in d.get("stages") or []
        ],
        "our_modules": OUR_M8,
        "showcase": showcase_codes,
        "concepts": concepts,
        "stats": {
            "n_concepts": len(concepts),
            "by_subject": dict(Counter(c["subject"] for c in concepts)),
            "n_families": len(families),
        },
    }

    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_JS.write_text(
        "// Generated by scripts/build_concept_rivers_data.py — do not edit by hand.\n"
        "window.CONCEPT_RIVERS = "
        + json.dumps(payload, ensure_ascii=False)
        + ";\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT_JSON.relative_to(REPO)} ({len(concepts)} concepts, {len(families)} families)")
    for g in range(7, 12):
        rows = grade_families[str(g)]
        n = sum(len(r["birth_codes"]) for r in rows)
        print(f"  {g}: {len(rows)} families with births, {n} concepts")


if __name__ == "__main__":
    main()
