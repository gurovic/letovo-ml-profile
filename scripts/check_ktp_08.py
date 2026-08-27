#!/usr/bin/env python3
"""Consistency check: KTP Draft 4 ↔ modules (core M1–M10 + optional M11 DP)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# (folder, pairs, start, end, optional)
EXPECTED = {
    1: ("08_01_functions_recursion", 8, 1, 8, False),
    2: ("08_02_carsharing_pandas_lr", 8, 9, 16, False),
    3: ("08_03_titanic_eda", 8, 17, 24, False),
    4: ("08_04_mnist_knn", 6, 25, 30, False),
    5: ("08_05_shop_feature_engineering", 7, 31, 37, False),
    6: ("08_06_ab_startup", 6, 38, 43, False),
    7: ("08_07_bank_arrays_search", 4, 44, 47, False),
    8: ("08_08_logistics_clustering", 3, 48, 50, False),
    9: ("08_10_churn_logreg", 4, 51, 54, False),
    10: ("08_11_virtual_polygon", 4, 55, 58, False),
    11: ("08_09_courier_dp", 5, 59, 63, True),
}

CORE_PAIRS = 58
OPT_PAIRS = 5
SCHEDULED = CORE_PAIRS + OPT_PAIRS  # 63
CAPACITY = 68


def main() -> int:
    issues: list[str] = []
    ktp = (REPO / "docs/ktp/08.md").read_text(encoding="utf-8")

    grid = re.findall(
        r"\| M(\d+) \| (\d+) \| (\d+)–(\d+) \| ([^|]+) \|", ktp
    )
    if len(grid) != 11:
        issues.append(f"FAIL: grid rows={len(grid)} (want 11)")
    else:
        expect = 1
        total = 0
        for m, c, a, b, flag in grid:
            m, c, a, b = int(m), int(c), int(a), int(b)
            total += c
            optional = "доп" in flag.lower()
            if a != expect:
                issues.append(f"FAIL: M{m} starts {a}, expected {expect}")
            if b - a + 1 != c:
                issues.append(f"FAIL: M{m} range {a}-{b} != count {c}")
            folder, ec, ea, eb, eopt = EXPECTED[m]
            if (c, a, b, optional) != (ec, ea, eb, eopt):
                issues.append(
                    f"FAIL: M{m} {(c, a, b, optional)} != expected {(ec, ea, eb, eopt)}"
                )
            path = REPO / "modules" / folder
            if not path.is_dir():
                issues.append(f"FAIL: missing module dir {folder}")
            expect = b + 1
        if total != SCHEDULED or int(grid[-1][3]) != SCHEDULED:
            issues.append(f"FAIL: grid total/last = {total}/{grid[-1][3]} (want {SCHEDULED})")
        else:
            print(f"OK grid 11 modules → {SCHEDULED} pairs (core {CORE_PAIRS} + opt {OPT_PAIRS})")

    if "дополнительный" not in ktp.lower() and "доп." not in ktp.lower():
        issues.append("FAIL: optional DP not marked in 08.md")

    head = ktp.split("## Карта инструментов")[0].split("## Резерв")[0]
    theme_nums = [int(x) for x in re.findall(r"^\| (\d+) \| ", head, re.M)]
    seq = [n for n in theme_nums if 1 <= n <= CAPACITY]
    # drop grid M counts that appear as small numbers in first table — keep lesson rows
    # Lesson rows are under module sections; grid also has counts 8,8,... — filter consecutive 1..63
    out: list[int] = []
    for n in seq:
        if not out and n != 1:
            continue
        if out and n == out[-1]:
            continue
        if out and n != out[-1] + 1:
            # skip non-sequential (grid table noise)
            if n < out[-1]:
                continue
            if n != out[-1] + 1:
                # restart only if we haven't finished
                continue
        out.append(n)
        if out and out[-1] == SCHEDULED:
            break
    # Simpler: unique sorted theme numbers that form 1..63 in module theme tables
    themes = []
    for line in head.splitlines():
        m = re.match(r"\| (\d+) \| .+ \|", line)
        if not m:
            continue
        n = int(m.group(1))
        if themes and n == themes[-1]:
            continue
        if not themes:
            if n == 1:
                themes.append(n)
            continue
        if n == themes[-1] + 1:
            themes.append(n)
    if themes != list(range(1, SCHEDULED + 1)):
        issues.append(
            f"FAIL: theme sequence len={len(themes)} first={themes[:3]} last={themes[-3:]}"
        )
    else:
        print(f"OK themes 1..{SCHEDULED}")

    if issues:
        print("\n".join(issues))
        return 1
    print("OK check_ktp_08 Draft 4")
    return 0


if __name__ == "__main__":
    sys.exit(main())
