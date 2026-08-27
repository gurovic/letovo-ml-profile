#!/usr/bin/env python3
"""Update all module gists from canvas_gist_map.json with current notebooks."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "modules"


def pair_folders(module_dir: Path) -> dict[int, Path]:
    lessons = module_dir / "lessons"
    out: dict[int, Path] = {}
    if not lessons.exists():
        return out
    for d in lessons.iterdir():
        if not d.is_dir() or d.name.startswith("_"):
            continue
        md = d / "LESSON.md"
        if not md.exists():
            continue
        m = re.search(r"Пара КТП\s*\|\s*\*?\*?(\d+)", md.read_text(encoding="utf-8"))
        if m:
            out[int(m.group(1))] = d
    return out


def edit(gist_id: str, local: Path, remote: str) -> None:
    cmd = ["gh", "gist", "edit", gist_id, str(local), "-f", remote]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  FAIL {remote}: {r.stderr or r.stdout}", file=sys.stderr)


def main() -> None:
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    for map_path in sorted(MODULES.glob("08_*/canvas_gist_map.json")):
        module_dir = map_path.parent
        if only and module_dir.name not in only:
            continue
        print("===", module_dir.name)
        mapping = json.loads(map_path.read_text(encoding="utf-8"))
        folders = pair_folders(module_dir)
        for pair_s, meta in sorted(mapping.items(), key=lambda kv: int(kv[0])):
            pair = int(pair_s)
            gist_id = meta["gist_id"] if isinstance(meta, dict) else meta
            folder = folders.get(pair)
            if not folder:
                print(f"  skip pair {pair}: no folder")
                continue
            print(f"  pair {pair} → {folder.name}")
            for name in ("lesson.ipynb", "homework.ipynb", "solutions.ipynb"):
                path = folder / name
                if path.exists():
                    edit(gist_id, path, name)


if __name__ == "__main__":
    main()
