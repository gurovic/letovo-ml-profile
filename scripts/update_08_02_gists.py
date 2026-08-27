#!/usr/bin/env python3
"""Update all 08_02 lesson gists from canvas_gist_map.json."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "modules/08_02_carsharing_pandas_lr"
MAP = MODULE / "canvas_gist_map.json"

PAIR_FOLDER = {
    9: "01_pandas_dataframe",
    10: "02_eda_scatter",
    11: "03_train_test_lr",
    12: "04_practice_metrics",
    13: "05_try_except_csv",
    14: "06_practice_features",
    15: "07_report_build",
    16: "08_report_submit",
}


def edit(gist_id: str, local: Path, remote_name: str, *, add: bool = False) -> None:
    cmd = ["gh", "gist", "edit", gist_id, str(local)]
    if add:
        cmd.extend(["-a", remote_name])
    else:
        cmd.extend(["-f", remote_name])
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr or r.stdout, file=sys.stderr)
        raise SystemExit(r.returncode)


def main() -> None:
    mapping = json.loads(MAP.read_text(encoding="utf-8"))
    csv_path = MODULE / "data" / "listings.csv"
    for pair, folder in PAIR_FOLDER.items():
        gist_id = mapping[str(pair)]["gist_id"]
        lesson_dir = MODULE / "lessons" / folder
        print(f"pair {pair} {gist_id}")
        for name in ("lesson.ipynb", "homework.ipynb", "solutions.ipynb"):
            path = lesson_dir / name
            if path.exists():
                edit(gist_id, path, name)
        # keep csv in gist as optional sibling; Colab still uses URL fallback
        edit(gist_id, csv_path, "listings.csv", add=True)


if __name__ == "__main__":
    main()
