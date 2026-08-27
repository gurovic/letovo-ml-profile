#!/usr/bin/env python3
"""Patch all grade-8 modules: CSV load local → raw GitHub (Colab).

Skips 08_01 (module_datasets already patched) and notebooks under _archive.
Updates generate_notebooks.py LOAD blocks where present.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "modules"
RAW = "https://raw.githubusercontent.com/gurovic/letovo-ml-profile/main/modules"

# module_dir → path under modules/ for raw URL (data lives in module/data/)
MODULE_DATA_PREFIX = {
    "08_03_titanic_eda": "08_03_titanic_eda/data",
    "08_04_mnist_knn": "08_04_mnist_knn/data",
    "08_05_shop_feature_engineering": "08_05_shop_feature_engineering/data",
    "08_06_ab_startup": "08_06_ab_startup/data",
    "08_07_bank_arrays_search": "08_07_bank_arrays_search/data",
    "08_08_logistics_clustering": "08_08_logistics_clustering/data",
    "08_09_courier_dp": "08_09_courier_dp/data",
    "08_10_churn_logreg": "08_10_churn_logreg/data",
}

# 08_03 kmeans uses orders_slim from shop module in some copies — prefer local,
# then 08_03 data if present, else 08_05 data URL (handled via name→prefix map)
CSV_URL_OVERRIDE = {
    # name → full modules/.../data/file path after modules/
    "orders_slim.csv": None,  # resolve per-module below
}


def data_url(module_dir: str, name: str) -> str:
    # orders_slim in titanic kmeans lesson: file often next to notebook or from 08_05
    if name == "orders_slim.csv" and module_dir == "08_03_titanic_eda":
        # prefer 08_05 canonical slim if not in 08_03/data
        local = MODULES / "08_03_titanic_eda" / "data" / name
        if local.exists():
            return f"{RAW}/08_03_titanic_eda/data/{name}"
        return f"{RAW}/08_05_shop_feature_engineering/data/{name}"
    prefix = MODULE_DATA_PREFIX[module_dir]
    return f"{RAW}/{prefix}/{name}"


LOCAL_PATHS_SNIPPET = '''(
        Path(name),
        Path("../") / name,
        Path("../../data") / name,
        Path("../data") / name,
        Path("../../../data") / name,
    )'''


def make_find_csv_generic(module_dir: str) -> str:
    # URL built at runtime from name; base path fixed
    prefix = MODULE_DATA_PREFIX[module_dir]
    if module_dir == "08_03_titanic_eda":
        return f'''def find_csv(name):
    for path in (
        Path(name),
        Path("../") / name,
        Path("../../data") / name,
        Path("../data") / name,
        Path("../../../data") / name,
    ):
        if path.exists():
            return path.resolve()
    if name == "orders_slim.csv":
        return (
            "{RAW}/08_05_shop_feature_engineering/data/orders_slim.csv"
        )
    return "{RAW}/{prefix}/" + name
'''
    return f'''def find_csv(name):
    for path in (
        Path(name),
        Path("../") / name,
        Path("../../data") / name,
        Path("../data") / name,
        Path("../../../data") / name,
    ):
        if path.exists():
            return path.resolve()
    return "{RAW}/{prefix}/" + name
'''


def patch_find_named(src: str, module_dir: str, func_name: str, filename: str, path_var: str) -> str | None:
    """Replace find_<x>_csv / similar single-file finder."""
    if "raw.githubusercontent.com" in src and filename in src and "return" in src:
        # already has URL fallback somewhere — still rewrite if raise FileNotFound remains for this file
        if f"raise FileNotFoundError" not in src or filename not in src:
            return None
    url = data_url(module_dir, filename)
    # Match common patterns
    pat = re.compile(
        rf"def {re.escape(func_name)}\([^)]*\)[^\n]*:\n"
        rf"(?:    .*\n)+?"
        rf"    raise FileNotFoundError\([^\n]+\)\n",
        re.MULTILINE,
    )
    m = pat.search(src)
    if not m:
        return None
    replacement = (
        f"DATA_URL = (\n"
        f'    "{url}"\n'
        f")\n\n\n"
        f"def {func_name}():\n"
        f"    for p in (\n"
        f'        Path("{filename}"),\n'
        f'        Path("../{filename}"),\n'
        f'        Path("../../data/{filename}"),\n'
        f'        Path("../data/{filename}"),\n'
        f'        Path("../../../data/{filename}"),\n'
        f"    ):\n"
        f"        if p.exists():\n"
        f"            return p.resolve()\n"
        f"    return DATA_URL\n"
    )
    return src[: m.start()] + replacement + src[m.end() :]


def patch_find_csv_fn(src: str, module_dir: str) -> str | None:
    if "def find_csv(" not in src and "def _find(" not in src:
        return None
    if "raw.githubusercontent.com" in src and "raise FileNotFoundError" not in src:
        return None
    # replace any find_csv / _find that raises FileNotFoundError
    pat = re.compile(
        r"def (find_csv|_find)\(([^)]*)\)[^\n]*:\n"
        r"(?:    .*\n)+?"
        r"    raise FileNotFoundError\([^\n]+\)\n",
        re.MULTILINE,
    )
    m = pat.search(src)
    if not m:
        return None
    fname = m.group(1)
    args = m.group(2)
    # keep parameter name
    param = args.split(":")[0].strip() or "name"
    prefix = MODULE_DATA_PREFIX[module_dir]
    if module_dir == "08_03_titanic_eda":
        body = (
            f"def {fname}({param}):\n"
            f"    for path in (\n"
            f"        Path({param}),\n"
            f"        Path(\"../\") / {param},\n"
            f"        Path(\"../../data\") / {param},\n"
            f"        Path(\"../data\") / {param},\n"
            f"        Path(\"../../../data\") / {param},\n"
            f"    ):\n"
            f"        if path.exists():\n"
            f"            return path.resolve()\n"
            f"    if {param} == \"orders_slim.csv\":\n"
            f"        return \"{RAW}/08_05_shop_feature_engineering/data/orders_slim.csv\"\n"
            f"    return \"{RAW}/{prefix}/\" + {param}\n"
        )
    else:
        body = (
            f"def {fname}({param}):\n"
            f"    for path in (\n"
            f"        Path({param}),\n"
            f"        Path(\"../\") / {param},\n"
            f"        Path(\"../../data\") / {param},\n"
            f"        Path(\"../data\") / {param},\n"
            f"        Path(\"../../../data\") / {param},\n"
            f"    ):\n"
            f"        if path.exists():\n"
            f"            return path.resolve()\n"
            f"    return \"{RAW}/{prefix}/\" + {param}\n"
        )
    return src[: m.start()] + body + src[m.end() :]


def patch_inline_orders_finder(src: str, module_dir: str) -> str | None:
    """08_08 / 08_10 style: def find... with hardcoded filename in loop."""
    if "raise FileNotFoundError" not in src:
        return None
    if "raw.githubusercontent.com" in src and "return" in src.split("raise FileNotFoundError")[0][-200:]:
        pass
    # Hardcoded single-file finders without generic name
    for filename, func_guess in (
        ("orders_slim.csv", None),
        ("bank_marketing_slim.csv", None),
        ("titanic.csv", "find_titanic_csv"),
        ("digits.csv", "find_digits_csv"),
        ("startup_ab.csv", None),
    ):
        if filename not in src:
            continue
        # try named function first
        for func in (
            "find_titanic_csv",
            "find_digits_csv",
            "find_csv",
            "_find",
            "find_orders_csv",
            "find_data_csv",
        ):
            out = patch_find_named(src, module_dir, func, filename, "PATH")
            if out is not None:
                return out
        # anonymous: for path in (Path("orders_slim.csv"), ...) raise
        pat = re.compile(
            rf"(def \w+\([^)]*\)[^\n]*:\n"
            rf"(?:    .*\n)*?"
            rf"    for path in \([^\)]*{re.escape(filename)}[^\)]*\):\n"
            rf"(?:        .*\n)+?"
            rf"    raise FileNotFoundError\([^\n]+\)\n)",
            re.MULTILINE,
        )
        m = pat.search(src)
        if m:
            # extract def name
            dm = re.match(r"def (\w+)\(", m.group(1))
            func = dm.group(1) if dm else "find_csv"
            url = data_url(module_dir, filename)
            if func in ("find_csv", "_find"):
                return patch_find_csv_fn(src, module_dir)
            replacement = (
                f"DATA_URL = \"{url}\"\n\n\n"
                f"def {func}():\n"
                f"    for path in (\n"
                f'        Path("{filename}"),\n'
                f'        Path("../{filename}"),\n'
                f'        Path("../../data/{filename}"),\n'
                f'        Path("../data/{filename}"),\n'
                f'        Path("../../../data/{filename}"),\n'
                f"    ):\n"
                f"        if path.exists():\n"
                f"            return path.resolve()\n"
                f"    return DATA_URL\n"
            )
            return src[: m.start()] + replacement + src[m.end() :]
    return None


def patch_data_path_only(src: str, module_dir: str, filename: str) -> str | None:
    """DATA_PATH = Path('bank_marketing_slim.csv') → with URL fallback helper."""
    if "raw.githubusercontent.com" in src:
        return None
    if f'Path("{filename}")' not in src and f"Path('{filename}')" not in src:
        return None
    if "def find" in src or "for path in" in src or "for p in" in src:
        return None
    url = data_url(module_dir, filename)
    needle_dq = f'DATA_PATH = Path("{filename}")'
    needle_sq = f"DATA_PATH = Path('{filename}')"
    block = (
        f"_DATA_URL = \"{url}\"\n"
        f"DATA_PATH = next(\n"
        f"    (p for p in (\n"
        f'        Path("{filename}"),\n'
        f'        Path("../../data/{filename}"),\n'
        f'        Path("../data/{filename}"),\n'
        f"    ) if p.exists()),\n"
        f"    _DATA_URL,\n"
        f")\n"
    )
    if needle_dq in src:
        return src.replace(needle_dq, block.rstrip("\n"), 1)
    if needle_sq in src:
        return src.replace(needle_sq, block.rstrip("\n"), 1)
    return None


def patch_cell(src: str, module_dir: str) -> str:
    if "raw.githubusercontent.com" in src and "raise FileNotFoundError" not in src:
        return src
    original = src
    # Order of attempts
    for func, filename in (
        ("find_titanic_csv", "titanic.csv"),
        ("find_digits_csv", "digits.csv"),
    ):
        out = patch_find_named(src, module_dir, func, filename, "PATH")
        if out:
            src = out
    out = patch_find_csv_fn(src, module_dir)
    if out:
        src = out
    out = patch_inline_orders_finder(src, module_dir)
    if out:
        src = out
    for filename in (
        "bank_marketing_slim.csv",
        "orders_slim.csv",
        "startup_ab.csv",
        "titanic.csv",
        "digits.csv",
    ):
        out = patch_data_path_only(src, module_dir, filename)
        if out:
            src = out
            break
    # Last resort: replace raise FileNotFoundError after for-loop with return URL
    # for cells that still raise and mention .csv
    if src == original and "raise FileNotFoundError" in src and ".csv" in src:
        src2 = patch_raise_to_url_fallback(src, module_dir)
        if src2:
            src = src2
    return src


def patch_raise_to_url_fallback(src: str, module_dir: str) -> str | None:
    """Generic: after for-loop looking for files, raise → return URL constructed from name/literal."""
    # Case: for p in (Path('x.csv'), ...): ... raise FileNotFoundError('x.csv...')
    m = re.search(
        r"for p in \((.*?)\):\n(?:    .*\n)+?    raise FileNotFoundError\(([^\n]+)\)\n",
        src,
        re.DOTALL,
    )
    if not m:
        m = re.search(
            r"for path in \((.*?)\):\n(?:    .*\n)+?    raise FileNotFoundError\(([^\n]+)\)\n",
            src,
            re.DOTALL,
        )
        var = "path"
    else:
        var = "p"
    if not m:
        return None
    # Detect filename from Path('file.csv') in the for-list
    files = re.findall(r"Path\(['\"]([^'\"]+\.csv)['\"]\)", m.group(1))
    if not files:
        # Path(name) or Path(f'../../data/{name}')
        if "name" in m.group(1) or "{name}" in m.group(1):
            # already handled by find_csv
            return None
        return None
    filename = files[0]
    url = data_url(module_dir, filename)
    old = m.group(0)
    new = old.replace(
        f"raise FileNotFoundError({m.group(2)})\n",
        f"return \"{url}\"\n" if "def " in src[max(0, m.start() - 80) : m.start()] else f"{var}_FALLTHROUGH\n",
    )
    # If inside a function that should return path, use return URL
    before = src[max(0, m.start() - 120) : m.start()]
    if "def " in before:
        new = re.sub(
            r"raise FileNotFoundError\([^\n]+\)\n",
            f'return "{url}"\n',
            old,
        )
        return src[: m.start()] + new + src[m.end() :]
    # Not in function — replace raise with assignment to URL for path var used next
    # e.g. LISTINGS style already handled
    new = re.sub(
        r"raise FileNotFoundError\([^\n]+\)\n",
        f'    # Colab fallback\n    pass\n',
        old,
    )
    # Better: inject after loop
    return None


def to_nb_source(text: str) -> list[str]:
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    return lines


def patch_notebook(path: Path, module_dir: str) -> bool:
    nb = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source", []))
        if "raise FileNotFoundError" not in src and "DATA_PATH = Path(" not in src:
            continue
        new = patch_cell(src, module_dir)
        if new != src:
            cell["source"] = to_nb_source(new)
            changed = True
    if changed:
        path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return changed


def patch_generator_load_block(gen: Path, module_dir: str) -> bool:
    """Replace LOAD_DATA / LOAD / similar string constants that still raise FileNotFound."""
    text = gen.read_text(encoding="utf-8")
    if "raw.githubusercontent.com" in text and "raise FileNotFoundError" not in text:
        return False
    changed = False

    # 08_03 titanic
    if module_dir == "08_03_titanic_eda":
        url = data_url(module_dir, "titanic.csv")
        new_load = f'''LOAD_DATA = \'\'\'from pathlib import Path
import pandas as pd


DATA_URL = (
    "{url}"
)


def find_titanic_csv():
    for p in (
        Path("titanic.csv"),
        Path("../titanic.csv"),
        Path("../../data/titanic.csv"),
        Path("../data/titanic.csv"),
        Path("../../../data/titanic.csv"),
    ):
        if p.exists():
            return p.resolve()
    return DATA_URL


TITANIC_PATH = find_titanic_csv()
df = pd.read_csv(TITANIC_PATH)
\'\'\'
'''
        text2, n = re.subn(
            r"LOAD_DATA = \([\s\S]*?\n\)\n",
            new_load + "\n",
            text,
            count=1,
        )
        if n:
            text = text2
            changed = True

    if module_dir == "08_04_mnist_knn":
        url = data_url(module_dir, "digits.csv")
        new_load = f'''LOAD_DATA = \'\'\'from pathlib import Path
import pandas as pd


DATA_URL = (
    "{url}"
)


def find_digits_csv():
    for p in (
        Path("digits.csv"),
        Path("../digits.csv"),
        Path("../../data/digits.csv"),
        Path("../data/digits.csv"),
        Path("../../../data/digits.csv"),
    ):
        if p.exists():
            return p.resolve()
    return DATA_URL


DIGITS_PATH = find_digits_csv()
df = pd.read_csv(DIGITS_PATH)
\'\'\'
'''
        text2, n = re.subn(r"LOAD_DATA = \([\s\S]*?\n\)\n", new_load + "\n", text, count=1)
        if n:
            text = text2
            changed = True

    if module_dir == "08_05_shop_feature_engineering":
        new_load = f'''LOAD = \'\'\'from pathlib import Path
import pandas as pd
import numpy as np

def find_csv(name):
    for path in (
        Path(name),
        Path("../") / name,
        Path("../../data") / name,
        Path("../data") / name,
        Path("../../../data") / name,
    ):
        if path.exists():
            return path.resolve()
    return "{RAW}/08_05_shop_feature_engineering/data/" + name

orders = pd.read_csv(find_csv("orders_slim.csv"), parse_dates=["order_purchase_timestamp", "order_delivered_customer_date"])
customers = pd.read_csv(find_csv("customers_slim.csv"))
payments = pd.read_csv(find_csv("payments_slim.csv"))
assert len(orders) and len(customers) and len(payments)
assert orders["order_id"].is_unique and customers["customer_id"].is_unique
print(f"orders={{len(orders)}}, customers={{len(customers)}}, payments={{len(payments)}}")
\'\'\'
'''
        text2, n = re.subn(r"LOAD = \"\"\"[\s\S]*?\"\"\"\n", new_load + "\n", text, count=1)
        if n:
            text = text2
            changed = True

    if module_dir == "08_06_ab_startup":
        url = data_url(module_dir, "startup_ab.csv")
        new_load = f'''LOAD_DATA = \'\'\'from pathlib import Path
import numpy as np
import pandas as pd


def _find(name: str):
    for p in (Path(name), Path(f"../../data/{{name}}"), Path(f"../data/{{name}}"), Path(f"../../../data/{{name}}")):
        if p.exists():
            return p.resolve()
    return "{RAW}/08_06_ab_startup/data/" + name


CSV_PATH = _find("startup_ab.csv")
df = pd.read_csv(CSV_PATH)
df["variant_b"] = (df["variant"] == "B").astype(int)
\'\'\'
'''
        text2, n = re.subn(r"LOAD_DATA = \([\s\S]*?\n\)\n", new_load + "\n", text, count=1)
        if n:
            text = text2
            changed = True

    if module_dir == "08_07_bank_arrays_search":
        # LOAD may be embedded differently — patch find_csv in triple quotes if present
        text2 = re.sub(
            r"def find_csv\(name\):\n(?:    .*\n)+?    raise FileNotFoundError\([^\n]+\)\n",
            make_find_csv_generic(module_dir),
            text,
            count=0,
        )
        if text2 != text:
            text = text2
            changed = True

    if module_dir in ("08_08_logistics_clustering", "08_10_churn_logreg", "08_09_courier_dp"):
        text2 = re.sub(
            r"def find_csv\(name\):\n(?:    .*\n)+?    raise FileNotFoundError\([^\n]+\)\n",
            make_find_csv_generic(module_dir),
            text,
            count=0,
        )
        if text2 != text:
            text = text2
            changed = True
        # also single-file finders in triple-quoted LOAD
        for filename in ("orders_slim.csv", "bank_marketing_slim.csv"):
            url = data_url(module_dir, filename)
            text3 = re.sub(
                rf"(for path in \([^\)]*{re.escape(filename)}[^\)]*\):\n(?:    .*\n)+?)    raise FileNotFoundError\([^\n]+\)\n",
                rf'\1    return "{url}"\n',
                text,
            )
            if text3 != text:
                text = text3
                changed = True

    if changed:
        gen.write_text(text, encoding="utf-8")
    return changed


def update_gists_for_module(module_dir: str) -> None:
    map_path = MODULES / module_dir / "canvas_gist_map.json"
    if not map_path.exists():
        print(f"  no gist map for {module_dir}")
        return
    mapping = json.loads(map_path.read_text(encoding="utf-8"))
    lessons = MODULES / module_dir / "lessons"
    # pair → folder by reading LESSON.md Пара КТП
    folders = sorted(
        d for d in lessons.iterdir() if d.is_dir() and not d.name.startswith("_") and (d / "LESSON.md").exists()
    )
    # Use map keys as pair numbers; match folder order by pair in LESSON
    pair_to_folder: dict[int, Path] = {}
    for d in folders:
        text = (d / "LESSON.md").read_text(encoding="utf-8")
        m = re.search(r"Пара КТП\s*\|\s*\*?\*?(\d+)", text)
        if m:
            pair_to_folder[int(m.group(1))] = d
    for pair_s, meta in mapping.items():
        pair = int(pair_s)
        gist_id = meta["gist_id"] if isinstance(meta, dict) else meta
        folder = pair_to_folder.get(pair)
        if not folder:
            print(f"  skip gist pair {pair}: no folder")
            continue
        print(f"  gist pair {pair} {folder.name}")
        for name in ("lesson.ipynb", "homework.ipynb", "solutions.ipynb"):
            path = folder / name
            if path.exists():
                cmd = ["gh", "gist", "edit", gist_id, str(path), "-f", name]
                r = subprocess.run(cmd, capture_output=True, text=True)
                if r.returncode != 0:
                    print("   ", r.stderr or r.stdout, file=sys.stderr)


def main() -> None:
    do_gists = "--gists" in sys.argv
    total_nb = 0
    for module_dir, _prefix in MODULE_DATA_PREFIX.items():
        mod = MODULES / module_dir
        if not mod.exists():
            continue
        print("===", module_dir)
        n = 0
        for nb in sorted(mod.rglob("*.ipynb")):
            if "_archive" in nb.parts:
                continue
            if patch_notebook(nb, module_dir):
                n += 1
                print("  patched", nb.relative_to(mod))
        total_nb += n
        gen = mod / "generate_notebooks.py"
        if gen.exists():
            if patch_generator_load_block(gen, module_dir):
                print("  patched generate_notebooks.py")
            else:
                # still try generic raise→return in generator
                text = gen.read_text(encoding="utf-8")
                text2 = text
                for filename in ("titanic.csv", "digits.csv", "orders_slim.csv", "bank_marketing_slim.csv", "startup_ab.csv"):
                    url = data_url(module_dir, filename)
                    text2 = re.sub(
                        rf"(for p(?:ath)? in \([^\)]*{re.escape(filename)}[^\)]*\):\n(?:    .*\n)+?)    raise FileNotFoundError\([^\n]+\)\n",
                        rf'\1    return "{url}"\n',
                        text2,
                    )
                text2 = re.sub(
                    r"def find_csv\(name\):\n(?:    .*\n)+?    raise FileNotFoundError\([^\n]+\)\n",
                    make_find_csv_generic(module_dir),
                    text2,
                )
                text2 = re.sub(
                    r"def _find\(name[^\)]*\):\n(?:    .*\n)+?    raise FileNotFoundError\([^\n]+\)\n",
                    make_find_csv_generic(module_dir).replace("def find_csv(name):", "def _find(name: str):"),
                    text2,
                )
                if text2 != text:
                    gen.write_text(text2, encoding="utf-8")
                    print("  patched generate_notebooks.py (fallback)")
        if do_gists:
            update_gists_for_module(module_dir)
    print("TOTAL notebooks patched:", total_nb)


if __name__ == "__main__":
    main()
