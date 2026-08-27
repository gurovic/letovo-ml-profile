#!/usr/bin/env python3
"""Patch 08_01 notebooks: local data → raw GitHub fallback (Colab)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "modules/08_01_functions_recursion"

DATA_IMPORT_CELL = '''import importlib.util
import sys
import urllib.request
from pathlib import Path

_RAW = (
    "https://raw.githubusercontent.com/gurovic/letovo-ml-profile/main/"
    "modules/08_01_functions_recursion/data/module_datasets.py"
)


def _import_module_datasets():
    for root in (Path("../..").resolve(), Path(".").resolve()):
        path = root / "data" / "module_datasets.py"
        if path.is_file():
            root_s = str(root)
            if root_s not in sys.path:
                sys.path.insert(0, root_s)
            import data.module_datasets as md
            return md
    dest = Path("module_datasets.py")
    urllib.request.urlretrieve(_RAW, dest)
    spec = importlib.util.spec_from_file_location("module_datasets", dest)
    md = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(md)
    return md


_md = _import_module_datasets()
APARTMENTS = _md.APARTMENTS
EXAM_SCORES = _md.EXAM_SCORES
PREDICTIONS = _md.PREDICTIONS
LABELS = _md.LABELS
NESTED_API_RESPONSE = _md.NESTED_API_RESPONSE
CATEGORY_TREE = _md.CATEGORY_TREE
FEATURE_ROWS = _md.FEATURE_ROWS
MODEL_RUNS = _md.MODEL_RUNS
FEATURE_POINTS = _md.FEATURE_POINTS
PRICE_INTERCEPT = _md.PRICE_INTERCEPT
PRICE_COEF_AREA = _md.PRICE_COEF_AREA
'''


def to_nb_source(text: str) -> list[str]:
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    return lines


def patch_nb(path: Path) -> bool:
    nb = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for cell in nb["cells"]:
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source", []))
        if "from data.module_datasets import" in src and "_import_module_datasets" not in src:
            cell["source"] = to_nb_source(DATA_IMPORT_CELL)
            changed = True
        elif "sys.path.insert(0, str(Path('../..')" in src and "module_datasets" in src and "_import_module_datasets" not in src:
            cell["source"] = to_nb_source(DATA_IMPORT_CELL)
            changed = True
    if changed:
        path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("patched", path.relative_to(ROOT))
    return changed


def main() -> None:
    lesson_dir = MODULE / "lessons/07_recursion_pipeline"
    for name in ("lesson.ipynb", "homework.ipynb", "solutions.ipynb"):
        patch_nb(lesson_dir / name)

    # keep generator in sync
    gen = MODULE / "generate_notebooks.py"
    text = gen.read_text(encoding="utf-8")
    old = '''DATA_IMPORT = (
    "import sys\\n"
    "from pathlib import Path\\n"
    "sys.path.insert(0, str(Path('../..').resolve()))\\n"
    "from data.module_datasets import (\\n"
    "    APARTMENTS, EXAM_SCORES, PREDICTIONS, LABELS,\\n"
    "    NESTED_API_RESPONSE, CATEGORY_TREE, FEATURE_ROWS,\\n"
    "    MODEL_RUNS, FEATURE_POINTS,\\n"
    "    PRICE_INTERCEPT, PRICE_COEF_AREA,\\n"
    ")\\n"
)'''
    # Build DATA_IMPORT as concatenation of escaped lines
    escaped_lines = []
    for line in DATA_IMPORT_CELL.splitlines():
        escaped_lines.append(f'    "{line}\\n"')
    new_block = "DATA_IMPORT = (\n" + "\n".join(escaped_lines) + "\n)"
    if "DATA_IMPORT = (" in text and "_import_module_datasets" not in text:
        start = text.index("DATA_IMPORT = (")
        end = text.index(")", start)
        # find closing paren of DATA_IMPORT tuple - first ) after opening that closes it
        depth = 0
        end = start
        for i, ch in enumerate(text[start:], start):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        text = text[:start] + new_block + text[end:]
        gen.write_text(text, encoding="utf-8")
        print("patched generate_notebooks.py")


if __name__ == "__main__":
    main()
