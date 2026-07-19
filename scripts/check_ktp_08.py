#!/usr/bin/env python3
"""Consistency check: KTP Draft 3 (68 pairs) ↔ modules 08_01…08_11."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EXPECTED = {
    1: ("08_01_functions_recursion", 8, 1, 8),
    2: ("08_02_carsharing_pandas_lr", 8, 9, 16),
    3: ("08_03_titanic_eda", 7, 17, 23),
    4: ("08_04_mnist_knn", 6, 24, 29),
    5: ("08_05_shop_feature_engineering", 6, 30, 35),
    6: ("08_06_ab_startup", 6, 36, 41),
    7: ("08_07_bank_arrays_search", 7, 42, 48),
    8: ("08_08_logistics_clustering", 6, 49, 54),
    9: ("08_09_courier_dp", 5, 55, 59),
    10: ("08_10_churn_logreg", 5, 60, 64),
    11: ("08_11_virtual_polygon", 4, 65, 68),
}


def main() -> int:
    issues: list[str] = []
    ktp = (REPO / "docs/ktp/08.md").read_text(encoding="utf-8")

    grid = re.findall(r"\| M(\d+) \| (\d+) \| (\d+)–(\d+) \|", ktp)
    if len(grid) != 11:
        issues.append(f"FAIL: grid rows={len(grid)} (want 11)")
    else:
        expect = 1
        total = 0
        for m, c, a, b in grid:
            m, c, a, b = int(m), int(c), int(a), int(b)
            total += c
            if a != expect:
                issues.append(f"FAIL: M{m} starts {a}, expected {expect}")
            if b - a + 1 != c:
                issues.append(f"FAIL: M{m} range {a}-{b} != count {c}")
            exp = EXPECTED[m]
            if (c, a, b) != (exp[1], exp[2], exp[3]):
                issues.append(
                    f"FAIL: M{m} grid {(c, a, b)} != expected {(exp[1], exp[2], exp[3])}"
                )
            expect = b + 1
        if total != 68 or int(grid[-1][3]) != 68:
            issues.append(f"FAIL: grid total/last = {total}/{grid[-1][3]}")
        else:
            print("OK grid 11 modules → 68 pairs")

    # theme numbers in module sections (before tool map)
    head = ktp.split("## Карта инструментов")[0]
    theme_nums = [int(x) for x in re.findall(r"^\| (\d+) \| ", head, re.M)]
    # drop grid table M rows already parsed; keep theme-like 1..68
    seq = [n for n in theme_nums if 1 <= n <= 68]
    # unique consecutive from first 1
    out: list[int] = []
    for n in seq:
        if not out and n == 1:
            out.append(n)
        elif out and n == out[-1] + 1:
            out.append(n)
        elif out and len(out) >= 68:
            break
    if out != list(range(1, 69)):
        issues.append(f"FAIL: theme sequence len={len(out)} last={out[-1] if out else None}")
    else:
        print("OK theme rows 1–68")

    found = (REPO / "docs/00_FOUNDATION.md").read_text(encoding="utf-8")
    if not re.search(r"\|\s*8\s*\|\s*4\s*\|", found):
        issues.append("FAIL: Foundation class 8 hours != 4")
    if "68 пар" not in found:
        issues.append("FAIL: Foundation missing 68 пар")
    else:
        print("OK Foundation load")

    ktp07 = (REPO / "docs/07_KTP.md").read_text(encoding="utf-8")
    if "4 ч/нед" not in ktp07 or "68" not in ktp07:
        issues.append("FAIL: 07_KTP load/pairs")
    else:
        print("OK 07_KTP")

    sm = (REPO / "docs/ktp/08_skills_matrix.md").read_text(encoding="utf-8")
    sm_nums = []
    seen = set()
    for n in (int(x) for x in re.findall(r"^\| (\d+) \|", sm, re.M)):
        if 1 <= n <= 68 and n not in seen:
            seen.add(n)
            sm_nums.append(n)
    if sm_nums != list(range(1, 69)):
        issues.append(f"FAIL: skills_matrix unique pairs={len(sm_nums)}")
    else:
        print("OK skills_matrix 68")

    desc = (REPO / "docs/ktp/08_module_descriptions.md").read_text(encoding="utf-8")
    for m, (_, _, a, b) in EXPECTED.items():
        rng = f"{a}–{b}"
        if f"пары {rng}" not in desc:
            issues.append(f"FAIL: module_descriptions M{m} missing пары {rng}")
    if not any("module_descriptions" in i for i in issues):
        print("OK module_descriptions ranges")

    for mid, (slug, nlessons, a, b) in EXPECTED.items():
        root = REPO / "modules" / slug
        unit = root / "UNIT.md"
        if not unit.exists():
            issues.append(f"FAIL: missing {slug}/UNIT.md")
            continue
        ut = unit.read_text(encoding="utf-8")
        if not re.search(rf"{nlessons}\s*пар", ut):
            issues.append(f"FAIL: M{mid} UNIT missing '{nlessons} пар'")
        rng = f"{a}–{b}"
        if rng not in ut and f"{a}-{b}" not in ut:
            issues.append(f"WARN: M{mid} UNIT missing range {rng}")

        lesson_mds = sorted((root / "lessons").glob("*/LESSON.md")) if (root / "lessons").exists() else []
        if mid <= 3:
            if len(lesson_mds) != nlessons:
                issues.append(
                    f"FAIL: M{mid} LESSON.md count={len(lesson_mds)} want {nlessons}: "
                    + ", ".join(p.parent.name for p in lesson_mds)
                )
            for lm in lesson_mds:
                t = lm.read_text(encoding="utf-8")
                m = re.search(r"Пара КТП\s*\|\s*\*\*(\d+)\*\*", t) or re.search(
                    r"Пара КТП\s*\|\s*(\d+)", t
                )
                if not m:
                    issues.append(f"WARN: {lm.relative_to(REPO)} no Пара КТП")
                else:
                    p = int(m.group(1))
                    if not (a <= p <= b):
                        issues.append(
                            f"FAIL: {lm.relative_to(REPO)} pair {p} outside {a}–{b}"
                        )
            if len(lesson_mds) == nlessons:
                print(f"OK M{mid} lessons={nlessons} pairs {a}–{b}")
        else:
            if lesson_mds:
                issues.append(f"WARN: M{mid} plan-only but has {len(lesson_mds)} LESSON.md")
            if re.search(rf"{nlessons}\s*пар", ut) and (
                rng in ut or f"{a}-{b}" in ut
            ):
                print(f"OK M{mid} plan UNIT {a}–{b}")
            elif re.search(rf"{nlessons}\s*пар", ut):
                print(f"OK M{mid} plan UNIT count (range warn above)")

        for f in root.rglob("*.md"):
            t = f.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"5 ч/нед", t):
                issues.append(f"FAIL: {f.relative_to(REPO)} has 5 ч/нед")
            if re.search(r"85 пар", t):
                issues.append(f"FAIL: {f.relative_to(REPO)} has 85 пар")

    for path in (
        REPO / "docs/ktp/08.md",
        REPO / "docs/ktp/08_module_descriptions.md",
        REPO / "docs/07_KTP.md",
        REPO / "docs/00_FOUNDATION.md",
        REPO / "docs/ktp/08_tech_stack_skills.md",
    ):
        t = path.read_text(encoding="utf-8")
        if re.search(r"5 ч/нед", t):
            issues.append(f"FAIL: {path.relative_to(REPO)} has 5 ч/нед")
        if re.search(r"85 пар", t):
            issues.append(f"FAIL: {path.relative_to(REPO)} has 85 пар")

    bs = (REPO / "scripts/build_ktp_08.py").read_text(encoding="utf-8")
    if not all(
        x in bs
        for x in ("TARGET_PAIRS = 68", "HOURS_PER_WEEK = 4", "WEEKS = 34")
    ):
        issues.append("FAIL: build_ktp_08.py constants")
    else:
        print("OK build_ktp_08.py")

    # stale old ranges in canon docs (not the 'Было' column counts alone)
    stale = [
        "пары 1–10",
        "пары 11–20",
        "пары 21–29",
        "пары 30–37",
        "пары 38–44",
        "пары 45–52",
        "пары 53–61",
        "пары 62–69",
        "пары 70–75",
        "пары 76–81",
        "пары 82–85",
    ]
    for path in (
        REPO / "docs/ktp/08_module_descriptions.md",
        REPO / "docs/07_KTP.md",
    ):
        t = path.read_text(encoding="utf-8")
        for s in stale:
            if s in t:
                issues.append(f"FAIL: {path.relative_to(REPO)} still has {s}")

    print("\n=== ISSUES ===")
    fails = [i for i in issues if i.startswith("FAIL")]
    warns = [i for i in issues if i.startswith("WARN")]
    for i in issues:
        print(i)
    if not issues:
        print("NONE")
    print(f"\nFAIL={len(fails)} WARN={len(warns)}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
