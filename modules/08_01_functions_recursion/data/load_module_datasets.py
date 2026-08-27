"""Загрузка module_datasets: локальный репозиторий, иначе raw GitHub (Colab)."""

from __future__ import annotations

import importlib.util
import sys
import urllib.request
from pathlib import Path
from types import ModuleType

RAW_MODULE_DATASETS_URL = (
    "https://raw.githubusercontent.com/gurovic/letovo-ml-profile/main/"
    "modules/08_01_functions_recursion/data/module_datasets.py"
)


def import_module_datasets(
    *,
    lesson_relative_roots: tuple[Path, ...] | None = None,
) -> ModuleType:
    """Вернуть модуль с датасетами.

    Порядок:
    1) `…/08_01_functions_recursion/data/module_datasets.py` рядом с уроком / cwd;
    2) скачать файл с raw.githubusercontent.com (среда Colab из gist).
    """
    roots = list(lesson_relative_roots or ())
    roots.extend(
        [
            Path("../..").resolve(),
            Path(".").resolve(),
            Path(__file__).resolve().parent.parent,  # module root when imported as data.*
        ]
    )
    seen: set[Path] = set()
    for root in roots:
        root = root.resolve()
        if root in seen:
            continue
        seen.add(root)
        path = root / "data" / "module_datasets.py"
        if not path.is_file():
            continue
        root_s = str(root)
        if root_s not in sys.path:
            sys.path.insert(0, root_s)
        import data.module_datasets as md  # noqa: WPS433

        return md

    dest = Path("module_datasets.py")
    urllib.request.urlretrieve(RAW_MODULE_DATASETS_URL, dest)
    spec = importlib.util.spec_from_file_location("module_datasets", dest)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {dest}")
    md = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(md)
    return md
