#!/usr/bin/env python3
"""Ворота качества: прогон эталонов `solutions.ipynb`.

`lesson.ipynb` / `homework.ipynb` содержат stubs — их assert падают по замыслу.
Эталон преподавателя обязан исполняться сверху вниз без ошибок.

Запуск из корня репозитория:

    python scripts/run_solutions.py                       # все модули
    python scripts/run_solutions.py modules/08_04_mnist_knn
"""

from __future__ import annotations

import json
import os
import sys
import traceback
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parent.parent


def code_cells(path: Path) -> list[str]:
    nb = json.loads(path.read_text(encoding="utf-8"))
    return ["".join(c.get("source", [])) for c in nb["cells"] if c["cell_type"] == "code"]


def run_notebook(path: Path) -> tuple[bool, str]:
    cwd = os.getcwd()
    os.chdir(path.parent)
    namespace: dict[str, object] = {"__name__": "__main__"}
    try:
        for i, source in enumerate(code_cells(path), start=1):
            if not source.strip():
                continue
            try:
                exec(compile(source, f"{path.name}:cell{i}", "exec"), namespace)
            except Exception:
                return False, f"cell {i}\n{traceback.format_exc(limit=3)}"
        return True, "ok"
    finally:
        os.chdir(cwd)


def main() -> int:
    targets = [Path(a) for a in sys.argv[1:]] or [ROOT / "modules"]
    notebooks: list[Path] = []
    for target in targets:
        base = target if target.is_absolute() else ROOT / target
        notebooks.extend(sorted(base.rglob("solutions.ipynb")))
    if not notebooks:
        print("solutions.ipynb не найдены")
        return 1
    failed = 0
    for path in notebooks:
        ok, message = run_notebook(path)
        rel = path.relative_to(ROOT).as_posix()
        if ok:
            print(f"PASS {rel}")
        else:
            failed += 1
            print(f"FAIL {rel}: {message}")
    print(f"\n{len(notebooks) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
