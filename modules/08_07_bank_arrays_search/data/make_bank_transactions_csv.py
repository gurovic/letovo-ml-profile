#!/usr/bin/env python3
"""Generate classroom-sized bank transaction logs for module 08_07."""

from __future__ import annotations

import csv
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
SEED = 80742
N_ROWS = 960

TX_TYPES = ["debit", "credit", "transfer", "cash_out"]
CATEGORIES = ["groceries", "transport", "salary", "utilities", "cafe", "online", "pharmacy", "electronics"]
CITIES = ["Moscow", "Kazan", "Sochi", "Perm", "Tula", "Omsk", "Tomsk"]


def build_rows() -> list[tuple[int, int, int, int, str, str, str, int]]:
    rng = Random(SEED)
    rows: list[tuple[int, int, int, int, str, str, str, int]] = []
    for i in range(N_ROWS):
        txn_id = 100_000 + i * 3 + rng.randint(0, 2)
        account_id = 50_000 + rng.randint(0, 299)
        day = 1 + rng.randint(0, 29)
        amount = 200 + rng.randint(0, 48_000)
        tx_type = TX_TYPES[rng.randint(0, len(TX_TYPES) - 1)]
        category = CATEGORIES[rng.randint(0, len(CATEGORIES) - 1)]
        city = CITIES[rng.randint(0, len(CITIES) - 1)]
        risk_score = 5 + rng.randint(0, 95)
        rows.append((txn_id, account_id, day, amount, tx_type, category, city, risk_score))
    return rows


def write_csv(path: Path, rows: list[tuple[int, int, int, int, str, str, str, int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["txn_id", "account_id", "day", "amount", "tx_type", "merchant_category", "city", "risk_score"]
        )
        writer.writerows(rows)
    print(f"wrote {path}")


def main() -> None:
    rows = build_rows()

    rng = Random(SEED + 1)
    unsorted_rows = rows[:]
    rng.shuffle(unsorted_rows)

    sorted_by_id = sorted(rows, key=lambda t: t[0])
    sorted_by_amount = sorted(rows, key=lambda t: (t[3], t[0]))
    tiny = sorted_by_id[:80]

    write_csv(ROOT / "bank_transactions_unsorted.csv", unsorted_rows)
    write_csv(ROOT / "bank_transactions_sorted_by_txn_id.csv", sorted_by_id)
    write_csv(ROOT / "bank_transactions_sorted_by_amount.csv", sorted_by_amount)
    write_csv(ROOT / "bank_transactions_tiny.csv", tiny)


if __name__ == "__main__":
    main()
