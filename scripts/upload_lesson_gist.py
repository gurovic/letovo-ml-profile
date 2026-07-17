#!/usr/bin/env python3
"""Create a public GitHub gist from lesson notebooks; print Colab URLs."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GIST_USER = "gurovic"


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload lesson notebooks to gist")
    parser.add_argument("lesson_dir", type=Path, help="Path to lessons/NN_slug folder")
    parser.add_argument("--public", action="store_true", default=True)
    args = parser.parse_args()

    lesson_dir = args.lesson_dir.resolve()
    files = []
    for name in ("lesson.ipynb", "homework.ipynb", "solutions.ipynb", "trips.csv", "titanic.csv"):
        path = lesson_dir / name
        if path.exists():
            files.append(path)

    if not files:
        print("No notebooks found", file=sys.stderr)
        sys.exit(1)

    cmd = ["gh", "gist", "create", *[str(f) for f in files], "--desc", lesson_dir.name]
    if args.public:
        cmd.append("--public")

    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        print(result.stderr or result.stdout, file=sys.stderr)
        sys.exit(result.returncode)

    gist_url = result.stdout.strip().splitlines()[-1]
    gist_id = gist_url.rstrip("/").split("/")[-1]

    out = {
        "gist_url": gist_url,
        "gist_id": gist_id,
        "colab": {
            name: f"https://colab.research.google.com/gist/{GIST_USER}/{gist_id}/{name}"
            for name in ("lesson.ipynb", "homework.ipynb", "solutions.ipynb")
            if (lesson_dir / name).exists()
        },
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
