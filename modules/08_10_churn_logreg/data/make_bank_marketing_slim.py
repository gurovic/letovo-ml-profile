#!/usr/bin/env python3
"""Build slim CSV for module 08_10 (UCI Bank Marketing first, synthetic fallback)."""

from __future__ import annotations

import io
import zipfile
from pathlib import Path
from urllib.request import urlopen

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT_CSV = ROOT / "bank_marketing_slim.csv"

SELECTED_COLUMNS = [
    "age",
    "job",
    "marital",
    "education",
    "contact",
    "month",
    "campaign",
    "pdays",
    "previous",
    "poutcome",
    "emp.var.rate",
    "cons.price.idx",
    "cons.conf.idx",
    "euribor3m",
    "nr.employed",
    "duration",
    "y",
]


def ensure_required_columns(df: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    """Add missing columns when UCI subset lacks macro features."""
    out = df.copy()
    rng = np.random.default_rng(seed)
    numeric_fallbacks: dict[str, tuple[float, float, int]] = {
        "emp.var.rate": (0.4, 1.2, 2),
        "cons.price.idx": (93.7, 0.5, 3),
        "cons.conf.idx": (-41.2, 4.1, 1),
        "euribor3m": (3.4, 1.0, 3),
        "nr.employed": (5180.0, 55.0, 1),
    }
    for col, (mu, sigma, rnd) in numeric_fallbacks.items():
        if col not in out.columns:
            out[col] = np.round(rng.normal(mu, sigma, size=len(out)), rnd)
    return out


def try_load_uci() -> pd.DataFrame | None:
    """Return UCI bank dataset or None when unavailable."""
    urls = [
        "https://archive.ics.uci.edu/static/public/222/bank+marketing.zip",
        "https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip",
    ]
    for url in urls:
        try:
            with urlopen(url, timeout=30) as response:
                payload = response.read()
            with zipfile.ZipFile(io.BytesIO(payload)) as zf:
                for name in ("bank-full.csv", "bank.csv", "bank/bank-full.csv", "bank/bank.csv"):
                    if name in zf.namelist():
                        with zf.open(name) as handle:
                            df = pd.read_csv(handle, sep=";")
                        return df
        except Exception:
            continue
    return None


def build_synthetic(rows: int = 2400, seed: int = 42) -> pd.DataFrame:
    """Fallback synthetic data with the same feature spirit as UCI."""
    rng = np.random.default_rng(seed)

    jobs = ["admin.", "technician", "services", "management", "blue-collar", "student"]
    marital = ["single", "married", "divorced"]
    education = ["primary", "secondary", "tertiary"]
    contact = ["cellular", "telephone"]
    month = ["mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov"]
    poutcome = ["unknown", "failure", "success"]

    df = pd.DataFrame(
        {
            "age": rng.integers(18, 71, size=rows),
            "job": rng.choice(jobs, size=rows),
            "marital": rng.choice(marital, size=rows, p=[0.3, 0.58, 0.12]),
            "education": rng.choice(education, size=rows, p=[0.22, 0.58, 0.20]),
            "contact": rng.choice(contact, size=rows, p=[0.85, 0.15]),
            "month": rng.choice(month, size=rows),
            "campaign": rng.integers(1, 16, size=rows),
            "pdays": rng.choice([999, 10, 20, 30, 60, 90, 120], size=rows, p=[0.72, 0.06, 0.06, 0.06, 0.04, 0.03, 0.03]),
            "previous": rng.integers(0, 7, size=rows),
            "poutcome": rng.choice(poutcome, size=rows, p=[0.8, 0.12, 0.08]),
            "emp.var.rate": rng.normal(0.4, 1.2, size=rows).round(2),
            "cons.price.idx": rng.normal(93.7, 0.5, size=rows).round(3),
            "cons.conf.idx": rng.normal(-41.2, 4.1, size=rows).round(1),
            "euribor3m": rng.normal(3.4, 1.0, size=rows).clip(0.5, 5.2).round(3),
            "nr.employed": rng.normal(5180, 55, size=rows).round(1),
        }
    )

    logit = (
        -2.1
        - 0.22 * df["campaign"]
        + 0.45 * (df["poutcome"] == "success").astype(int)
        + 0.18 * (df["job"].isin(["student", "management"])).astype(int)
        + 0.26 * (df["contact"] == "cellular").astype(int)
        + 0.15 * (df["month"].isin(["mar", "apr", "sep", "oct"])).astype(int)
        + 0.09 * df["previous"]
    )
    p = 1.0 / (1.0 + np.exp(-logit))
    yes = rng.random(rows) < p

    # Leakage demo: duration сильно коррелирует с y, но этот столбец запрещен в X.
    duration_yes = rng.normal(370, 90, size=rows).clip(60, 780)
    duration_no = rng.normal(190, 70, size=rows).clip(20, 650)
    df["duration"] = np.where(yes, duration_yes, duration_no).round().astype(int)
    df["y"] = np.where(yes, "yes", "no")
    return df


def make_slim(df: pd.DataFrame, rows: int = 1800, seed: int = 42) -> pd.DataFrame:
    """Select columns and produce reproducible slim sample."""
    df = ensure_required_columns(df, seed=seed)
    use = df[SELECTED_COLUMNS].copy()
    if len(use) > rows and use["y"].nunique() == 2:
        frac = rows / len(use)
        chunk_yes = use[use["y"] == "yes"].sample(frac=frac, random_state=seed)
        chunk_no = use[use["y"] == "no"].sample(frac=frac, random_state=seed)
        use = pd.concat([chunk_yes, chunk_no], ignore_index=True)
    use = use.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    return use


def main() -> None:
    raw = try_load_uci()
    source = "uci_bank_marketing"
    if raw is None:
        raw = build_synthetic()
        source = "synthetic_fallback"

    slim = make_slim(raw)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    slim.to_csv(OUT_CSV, index=False)
    yes_share = float((slim["y"] == "yes").mean())

    print(f"source={source}")
    print(f"rows={len(slim)}")
    print(f"yes_share={yes_share:.4f}")
    print(f"csv={OUT_CSV}")


if __name__ == "__main__":
    main()
