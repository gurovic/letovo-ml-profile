#!/usr/bin/env python3
"""Finish leftovers: find_orders_csv, find_data (Path.open needs download)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = "https://raw.githubusercontent.com/gurovic/letovo-ml-profile/main/modules"

FIND_ORDERS = '''def find_orders_csv():
    for path in (
        Path("orders_slim.csv"),
        Path("../orders_slim.csv"),
        Path("../../data/orders_slim.csv"),
        Path("../data/orders_slim.csv"),
        Path("../../../data/orders_slim.csv"),
    ):
        if path.exists():
            return path.resolve()
    return (
        "https://raw.githubusercontent.com/gurovic/letovo-ml-profile/main/"
        "modules/08_05_shop_feature_engineering/data/orders_slim.csv"
    )
'''

FIND_DATA_09 = '''def find_data(name):
    import urllib.request
    for path in (
        Path(name),
        Path("../") / name,
        Path("../../data") / name,
        Path("../data") / name,
        Path("../../../data") / name,
    ):
        if path.exists():
            return path.resolve()
    url = (
        "https://raw.githubusercontent.com/gurovic/letovo-ml-profile/main/"
        "modules/08_09_courier_dp/data/" + name
    )
    dest = Path(name)
    urllib.request.urlretrieve(url, dest)
    return dest.resolve()
'''

FIND_ORDERS_08 = FIND_ORDERS  # same URL (canonical slim in 08_05)


def to_nb_source(text: str) -> list[str]:
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    return lines


def replace_func(src: str, func_name: str, new_body: str) -> str | None:
    pat = re.compile(
        rf"def {re.escape(func_name)}\([^)]*\)[^\n]*:\n"
        rf"(?:    .*\n)+?",
        re.MULTILINE,
    )
    m = pat.search(src)
    if not m:
        return None
    # extend to include multi-line raise
    end = m.end()
    # if raise continues with paren, include until closing paren line
    rest = src[end:]
    if rest.lstrip().startswith('"') or rest.lstrip().startswith("'"):
        # part of multi-line raise already in match? 
        pass
    # Match may stop before multi-line raise closing. Re-scan fuller:
    pat2 = re.compile(
        rf"def {re.escape(func_name)}\([^)]*\)[^\n]*:\n"
        rf"(?:.*\n)*?"
        rf"    raise FileNotFoundError\([\s\S]*?\)\n",
        re.MULTILINE,
    )
    m2 = pat2.search(src)
    if not m2:
        # try without requiring raise (already partially patched)
        return None
    return src[: m2.start()] + new_body + src[m2.end() :]


def patch_nb(path: Path, kind: str) -> bool:
    nb = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for cell in nb["cells"]:
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source", []))
        new = src
        if kind == "orders" and "def find_orders_csv" in src and "raw.githubusercontent.com" not in src:
            out = replace_func(src, "find_orders_csv", FIND_ORDERS)
            if out:
                new = out
        if kind == "dp" and "def find_data" in src and "urlretrieve" not in src:
            out = replace_func(src, "find_data", FIND_DATA_09)
            if out:
                new = out
        if new != src:
            cell["source"] = to_nb_source(new)
            changed = True
    if changed:
        path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("patched", path)
    return changed


def patch_generators() -> None:
    # 08_08
    for mod, pattern, repl in (
        (
            "08_08_logistics_clustering",
            r"def find_orders_csv\(\)[^\n]*:\n(?:.*\n)*?    raise FileNotFoundError\([\s\S]*?\)\n",
            FIND_ORDERS,
        ),
        (
            "08_09_courier_dp",
            r"def find_data\(name\)[^\n]*:\n(?:.*\n)*?    raise FileNotFoundError\([^\n]+\)\n",
            FIND_DATA_09,
        ),
        (
            "08_03_titanic_eda",
            r"def find_orders_csv\(\)[^\n]*:\n(?:.*\n)*?    raise FileNotFoundError\([\s\S]*?\)\n",
            FIND_ORDERS,
        ),
        (
            "08_10_churn_logreg",
            r"def find_csv\(name\)[^\n]*:\n(?:.*\n)*?    raise FileNotFoundError\([^\n]+\)\n",
            None,
        ),
    ):
        gen = ROOT / "modules" / mod / "generate_notebooks.py"
        if not gen.exists():
            continue
        text = gen.read_text(encoding="utf-8")
        if repl is None:
            continue
        text2, n = re.subn(pattern, repl, text, count=1)
        if n:
            gen.write_text(text2, encoding="utf-8")
            print("patched gen", mod)


def main() -> None:
    roots = [
        (ROOT / "modules/08_03_titanic_eda/lessons/07_kmeans_dbscan_eda", "orders"),
        (ROOT / "modules/08_08_logistics_clustering/lessons", "orders"),
        (ROOT / "modules/08_09_courier_dp/lessons", "dp"),
    ]
    for root, kind in roots:
        for nb in root.rglob("*.ipynb"):
            if "_archive" in nb.parts:
                continue
            patch_nb(nb, kind)
    patch_generators()

    # leftover check
    left = []
    for mod in (ROOT / "modules").glob("08_*"):
        for nb in mod.rglob("*.ipynb"):
            if "_archive" in nb.parts:
                continue
            data = json.loads(nb.read_text(encoding="utf-8"))
            for c in data["cells"]:
                src = "".join(c.get("source", []))
                if "raise FileNotFoundError" in src and ".csv" in src and "raw.githubusercontent.com" not in src and "urlretrieve" not in src:
                    left.append(str(nb.relative_to(ROOT / "modules")))
                    break
    print("LEFT", len(left))
    for x in left:
        print(x)


if __name__ == "__main__":
    main()
