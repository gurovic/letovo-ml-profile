#!/usr/bin/env python3
"""Generate synthetic A/B startup conversion dataset for module 08_06.

Reproducible by fixed seed, no external downloads required.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT_CSV = ROOT / "startup_ab.csv"
SEED = 806
N_ROWS = 3600


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def main() -> None:
    rng = np.random.default_rng(SEED)

    user_id = np.arange(1, N_ROWS + 1)
    day = rng.integers(1, 31, size=N_ROWS)
    variant = rng.choice(["A", "B"], size=N_ROWS, p=[0.5, 0.5])
    device = rng.choice(["desktop", "mobile"], size=N_ROWS, p=[0.42, 0.58])
    traffic_source = rng.choice(
        ["ads", "search", "social", "direct"],
        size=N_ROWS,
        p=[0.34, 0.28, 0.22, 0.16],
    )

    prior_visits_30d = np.clip(rng.poisson(lam=3.0, size=N_ROWS), 0, 15)
    pages_viewed = np.clip(2 + rng.poisson(lam=4.5, size=N_ROWS), 1, 20)
    session_minutes = np.clip(rng.normal(loc=3.7, scale=1.4, size=N_ROWS), 0.4, 12.0)
    discount_pct = rng.choice([0, 5, 10, 15], size=N_ROWS, p=[0.50, 0.30, 0.15, 0.05])
    age = np.clip(rng.normal(loc=31, scale=8.5, size=N_ROWS), 16, 60).round().astype(int)
    is_weekend = ((day % 7) >= 6).astype(int)
    variant_b = (variant == "B").astype(int)
    mobile = (device == "mobile").astype(int)

    src_ads = (traffic_source == "ads").astype(int)
    src_search = (traffic_source == "search").astype(int)
    src_social = (traffic_source == "social").astype(int)
    src_direct = (traffic_source == "direct").astype(int)

    intent = rng.normal(loc=0.0, scale=1.0, size=N_ROWS)
    logit = (
        -2.45
        + 0.22 * variant_b
        + 0.11 * prior_visits_30d
        + 0.08 * pages_viewed
        + 0.06 * session_minutes
        + 0.05 * (discount_pct / 5.0)
        - 0.10 * mobile
        - 0.03 * is_weekend
        + 0.16 * src_search
        + 0.12 * src_direct
        - 0.07 * src_social
        + 0.32 * intent
    )
    conv_proba = sigmoid(logit)
    converted = rng.binomial(n=1, p=conv_proba).astype(int)

    order_value = np.where(converted == 1, rng.gamma(shape=3.0, scale=22.0, size=N_ROWS), 0.0)

    df = pd.DataFrame(
        {
            "user_id": user_id,
            "day": day,
            "variant": variant,
            "device": device,
            "traffic_source": traffic_source,
            "age": age,
            "session_minutes": session_minutes.round(2),
            "pages_viewed": pages_viewed,
            "prior_visits_30d": prior_visits_30d,
            "discount_pct": discount_pct,
            "is_weekend": is_weekend,
            "converted": converted,
            "order_value": order_value.round(2),
        }
    ).sort_values("day", kind="mergesort")

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, index=False, encoding="utf-8")

    conv_a = df.loc[df["variant"] == "A", "converted"].mean()
    conv_b = df.loc[df["variant"] == "B", "converted"].mean()
    print(f"wrote {OUT_CSV}")
    print(f"rows={len(df)}, conversion A={conv_a:.4f}, B={conv_b:.4f}, uplift={conv_b - conv_a:.4f}")


if __name__ == "__main__":
    main()
