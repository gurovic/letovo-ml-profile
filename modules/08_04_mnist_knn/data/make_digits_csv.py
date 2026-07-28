#!/usr/bin/env python3
"""Export the handwritten digits table used by module 08_04 to CSV.

Source: sklearn.datasets.load_digits (UCI Optical Recognition of Handwritten
Digits, 8x8, values 0..16). Bundled with scikit-learn — works offline.

Run from this directory:
    python make_digits_csv.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.datasets import load_digits

OUT = Path(__file__).resolve().parent / "digits.csv"


def main() -> None:
    data = load_digits()
    cols = [f"p{i:02d}" for i in range(data.data.shape[1])]
    df = pd.DataFrame(data.data.astype(int), columns=cols)
    df.insert(0, "label", data.target.astype(int))
    df.to_csv(OUT, index=False)
    print("wrote", OUT, df.shape)


if __name__ == "__main__":
    main()
