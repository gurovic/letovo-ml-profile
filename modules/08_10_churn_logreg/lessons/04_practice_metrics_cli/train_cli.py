#!/usr/bin/env python3
"""CLI training utility for pair 63: metrics + leakage guard."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train LogisticRegression for bank campaign response.")
    parser.add_argument("--data", type=Path, required=True, help="Path to bank_marketing_slim.csv")
    parser.add_argument("--threshold", type=float, default=0.50, help="Probability threshold for positive class")
    parser.add_argument("--test-size", type=float, default=0.25, help="Test split share")
    parser.add_argument("--seed", type=int, default=63, help="Random seed")
    return parser.parse_args()


def train_and_score(data_path: Path, threshold: float, test_size: float, seed: int) -> dict[str, float | bool]:
    df = pd.read_csv(data_path)
    y = (df["y"] == "yes").astype(int)
    feature_columns = [c for c in df.columns if c not in ("y", "duration")]
    assert "duration" not in feature_columns, "duration leakage detected"

    X = pd.get_dummies(df[feature_columns], drop_first=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed, stratify=y
    )

    model = LogisticRegression(max_iter=1200)
    model.fit(X_train, y_train)
    proba = model.predict_proba(X_test)[:, 1]
    pred = (proba >= threshold).astype(int)

    return {
        "threshold": float(threshold),
        "duration_in_features": bool("duration" in feature_columns),
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision": float(precision_score(y_test, pred, zero_division=0)),
        "recall": float(recall_score(y_test, pred, zero_division=0)),
        "f1": float(f1_score(y_test, pred, zero_division=0)),
    }


def main() -> None:
    args = parse_args()
    metrics = train_and_score(args.data, args.threshold, args.test_size, args.seed)
    print(json.dumps(metrics, ensure_ascii=False))


if __name__ == "__main__":
    main()
