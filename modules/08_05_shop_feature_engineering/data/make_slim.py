#!/usr/bin/env python3
"""Собрать slim CSV модуля 5 (схема Olist: orders / customers / payments).

Если в data/raw/ лежат настоящие файлы Olist — режем их.
Иначе строим воспроизводимый classroom-slim с теми же именами столбцов
(seed=42), чтобы ноутбуки работали офлайн без Kaggle.

Запуск из каталога data/:
    python make_slim.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
OUT_ORDERS = ROOT / "orders_slim.csv"
OUT_CUSTOMERS = ROOT / "customers_slim.csv"
OUT_PAYMENTS = ROOT / "payments_slim.csv"

N_CUSTOMERS = 800
N_ORDERS = 3500
SEED = 42


def from_olist() -> bool:
    orders_p = RAW / "olist_orders_dataset.csv"
    cust_p = RAW / "olist_customers_dataset.csv"
    pay_p = RAW / "olist_order_payments_dataset.csv"
    if not (orders_p.exists() and cust_p.exists() and pay_p.exists()):
        return False

    orders = pd.read_csv(orders_p, parse_dates=["order_purchase_timestamp"])
    customers = pd.read_csv(cust_p)
    payments = pd.read_csv(pay_p)

    orders = orders[orders["order_status"] == "delivered"].copy()
    # последние ~15k заказов по времени покупки
    orders = orders.sort_values("order_purchase_timestamp").tail(15000)
    keep_ids = set(orders["order_id"])
    payments = payments[payments["order_id"].isin(keep_ids)]
    customers = customers[customers["customer_id"].isin(set(orders["customer_id"]))]

    orders[
        [
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp",
            "order_delivered_customer_date",
        ]
    ].to_csv(OUT_ORDERS, index=False)
    customers[["customer_id", "customer_unique_id", "customer_state"]].to_csv(
        OUT_CUSTOMERS, index=False
    )
    payments[["order_id", "payment_type", "payment_value"]].to_csv(OUT_PAYMENTS, index=False)
    print("wrote from real Olist:", OUT_ORDERS, OUT_CUSTOMERS, OUT_PAYMENTS)
    return True


def synthetic() -> None:
    rng = np.random.default_rng(SEED)
    states = ["SP", "RJ", "MG", "RS", "PR", "BA", "SC", "PE", "GO", "DF"]
    pay_types = ["credit_card", "boleto", "voucher", "debit_card"]

    cust_ids = [f"c{i:04d}" for i in range(N_CUSTOMERS)]
    unique_ids = [f"u{i:04d}" for i in range(N_CUSTOMERS)]
    customers = pd.DataFrame(
        {
            "customer_id": cust_ids,
            "customer_unique_id": unique_ids,
            "customer_state": rng.choice(states, size=N_CUSTOMERS, p=[0.4, 0.15, 0.12, 0.08, 0.07, 0.05, 0.04, 0.03, 0.03, 0.03]),
        }
    )

    # число заказов на клиента ~ Poisson, минимум 1 у части клиентов
    n_per = rng.poisson(3.5, size=N_CUSTOMERS) + 1
    # урежем до N_ORDERS
    rows = []
    oid = 0
    start = pd.Timestamp("2017-01-01")
    end = pd.Timestamp("2018-08-31")
    span_days = (end - start).days
    for cid, n in zip(cust_ids, n_per):
        for _ in range(int(n)):
            if oid >= N_ORDERS:
                break
            day = int(rng.integers(0, span_days + 1))
            ts = start + pd.Timedelta(days=day, hours=int(rng.integers(0, 24)))
            delivered = ts + pd.Timedelta(days=int(rng.integers(2, 25)))
            rows.append(
                {
                    "order_id": f"o{oid:05d}",
                    "customer_id": cid,
                    "order_status": "delivered",
                    "order_purchase_timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
                    "order_delivered_customer_date": delivered.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
            oid += 1
        if oid >= N_ORDERS:
            break

    orders = pd.DataFrame(rows)
    used = set(orders["customer_id"])
    customers = customers[customers["customer_id"].isin(used)].reset_index(drop=True)

    pay_rows = []
    for _, r in orders.iterrows():
        value = float(np.round(rng.lognormal(mean=4.2, sigma=0.55), 2))
        ptype = rng.choice(pay_types, p=[0.7, 0.18, 0.08, 0.04])
        pay_rows.append(
            {
                "order_id": r["order_id"],
                "payment_type": ptype,
                "payment_value": value,
            }
        )
    payments = pd.DataFrame(pay_rows)

    orders.to_csv(OUT_ORDERS, index=False)
    customers.to_csv(OUT_CUSTOMERS, index=False)
    payments.to_csv(OUT_PAYMENTS, index=False)
    print(
        "wrote synthetic classroom slim:",
        OUT_ORDERS.name,
        len(orders),
        "orders;",
        OUT_CUSTOMERS.name,
        len(customers),
        "customers;",
        OUT_PAYMENTS.name,
        len(payments),
        "payments",
    )


def main() -> None:
    if from_olist():
        return
    synthetic()


if __name__ == "__main__":
    main()
