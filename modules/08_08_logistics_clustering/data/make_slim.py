#!/usr/bin/env python3
"""Собрать slim CSV для модуля 08_08 (пары 49-54).

Если в data/raw есть реальные файлы Olist -> собрать срез из них.
Иначе сгенерировать classroom synthetic с Olist-подобной схемой
и целевой меткой is_late.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
OUT = ROOT / "orders_slim.csv"
SEED = 808


def build_from_olist() -> bool:
    orders_p = RAW / "olist_orders_dataset.csv"
    items_p = RAW / "olist_order_items_dataset.csv"
    cust_p = RAW / "olist_customers_dataset.csv"
    sellers_p = RAW / "olist_sellers_dataset.csv"
    if not (orders_p.exists() and items_p.exists() and cust_p.exists() and sellers_p.exists()):
        return False

    orders = pd.read_csv(
        orders_p,
        parse_dates=[
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    )
    items = pd.read_csv(items_p)
    customers = pd.read_csv(cust_p)[["customer_id", "customer_state"]]
    sellers = pd.read_csv(sellers_p)[["seller_id", "seller_state"]]

    delivered = orders[orders["order_status"] == "delivered"].copy()
    delivered = delivered.dropna(
        subset=["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"]
    )

    item_agg = (
        items.groupby("order_id", as_index=False)
        .agg(
            seller_id=("seller_id", "first"),
            freight_value=("freight_value", "sum"),
            price=("price", "sum"),
        )
    )
    slim = delivered.merge(item_agg, on="order_id", how="inner")
    slim = slim.merge(customers, on="customer_id", how="left")
    slim = slim.merge(sellers, on="seller_id", how="left")

    slim["delivery_days"] = (slim["order_delivered_customer_date"] - slim["order_purchase_timestamp"]).dt.days
    slim["estimated_days"] = (slim["order_estimated_delivery_date"] - slim["order_purchase_timestamp"]).dt.days
    slim["delay_days"] = slim["delivery_days"] - slim["estimated_days"]
    slim["is_late"] = (slim["delay_days"] > 0).astype(int)

    cols = [
        "order_id",
        "seller_id",
        "seller_state",
        "customer_state",
        "order_purchase_timestamp",
        "order_estimated_delivery_date",
        "order_delivered_customer_date",
        "freight_value",
        "price",
        "delivery_days",
        "estimated_days",
        "delay_days",
        "is_late",
    ]
    slim = slim[cols].sort_values("order_purchase_timestamp").tail(12000).reset_index(drop=True)
    slim.to_csv(OUT, index=False)
    print("wrote from real Olist:", OUT, "rows:", len(slim))
    return True


def build_synthetic() -> None:
    rng = np.random.default_rng(SEED)
    n = 240
    seller_states = np.array(["SP", "RJ", "MG", "PR", "SC", "BA"])
    customer_states = np.array(["SP", "RJ", "MG", "RS", "PR", "BA", "PE", "GO"])

    start = np.datetime64("2018-01-01")
    purchase_day = rng.integers(0, 120, size=n)
    purchase = start + purchase_day.astype("timedelta64[D]")

    estimated_days = rng.integers(5, 18, size=n)
    state_penalty = rng.choice([0, 0, 1, 2, 3], size=n, p=[0.45, 0.2, 0.2, 0.1, 0.05])
    random_noise = rng.normal(0, 2, size=n).round().astype(int)
    delivery_days = np.clip(estimated_days + state_penalty + random_noise, 2, 35)
    delay_days = delivery_days - estimated_days

    freight_base = rng.normal(32, 8, size=n)
    freight = np.clip(freight_base + 1.7 * np.maximum(delay_days, 0), 7, 110).round(2)
    price = np.clip(rng.lognormal(mean=4.4, sigma=0.5, size=n), 25, 1400).round(2)

    df = pd.DataFrame(
        {
            "order_id": [f"ol_{i:05d}" for i in range(n)],
            "seller_id": [f"sl_{i:04d}" for i in rng.integers(1, 65, size=n)],
            "seller_state": rng.choice(seller_states, size=n, p=[0.45, 0.18, 0.12, 0.1, 0.08, 0.07]),
            "customer_state": rng.choice(customer_states, size=n, p=[0.35, 0.16, 0.12, 0.1, 0.1, 0.07, 0.06, 0.04]),
            "order_purchase_timestamp": pd.to_datetime(purchase),
            "order_estimated_delivery_date": pd.to_datetime(purchase + estimated_days.astype("timedelta64[D]")),
            "order_delivered_customer_date": pd.to_datetime(purchase + delivery_days.astype("timedelta64[D]")),
            "freight_value": freight,
            "price": price,
            "delivery_days": delivery_days,
            "estimated_days": estimated_days,
            "delay_days": delay_days,
            "is_late": (delay_days > 0).astype(int),
        }
    )

    # Добавляем явные аномалии для пар 53-54.
    idx = rng.choice(df.index, size=6, replace=False)
    df.loc[idx, "freight_value"] = (df.loc[idx, "freight_value"] * 2.3).round(2)
    df.loc[idx, "delivery_days"] = df.loc[idx, "delivery_days"] + rng.integers(8, 16, size=len(idx))
    df.loc[idx, "delay_days"] = df.loc[idx, "delivery_days"] - df.loc[idx, "estimated_days"]
    df.loc[idx, "is_late"] = 1
    df["order_delivered_customer_date"] = df["order_purchase_timestamp"] + pd.to_timedelta(df["delivery_days"], unit="D")

    df = df.sort_values("order_purchase_timestamp").reset_index(drop=True)
    df.to_csv(OUT, index=False)
    print("wrote synthetic classroom slim:", OUT, "rows:", len(df))


def main() -> None:
    if build_from_olist():
        return
    build_synthetic()


if __name__ == "__main__":
    main()
