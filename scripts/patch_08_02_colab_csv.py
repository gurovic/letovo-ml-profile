#!/usr/bin/env python3
"""Patch 08_02 notebooks: listings.csv local → raw GitHub (Colab)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "modules/08_02_carsharing_pandas_lr"

OLD_FIND = """def find_listings_csv() -> Path:
    for p in (Path('listings.csv'), Path('../../data/listings.csv'), Path('../data/listings.csv')):
        if p.exists():
            return p.resolve()
    raise FileNotFoundError('listings.csv не найден')


LISTINGS_PATH = find_listings_csv()
df = pd.read_csv(LISTINGS_PATH)"""

NEW_FIND = """LISTINGS_URL = (
    "https://raw.githubusercontent.com/gurovic/letovo-ml-profile/main/"
    "modules/08_02_carsharing_pandas_lr/data/listings.csv"
)


def find_listings_csv():
    for p in (
        Path("listings.csv"),
        Path("../listings.csv"),
        Path("../../data/listings.csv"),
        Path("../../../data/listings.csv"),
        Path("../data/listings.csv"),
    ):
        if p.exists():
            return p.resolve()
    return LISTINGS_URL


LISTINGS_PATH = find_listings_csv()
df = pd.read_csv(LISTINGS_PATH)"""

# try/except lesson: path discovery without find_listings_csv
OLD_LOOP = """LISTINGS_PATH = None
for p in (Path('listings.csv'), Path('../../data/listings.csv'), Path('../data/listings.csv')):
    if p.exists():
        LISTINGS_PATH = p.resolve()
        break
assert LISTINGS_PATH is not None"""

NEW_LOOP = """LISTINGS_URL = (
    "https://raw.githubusercontent.com/gurovic/letovo-ml-profile/main/"
    "modules/08_02_carsharing_pandas_lr/data/listings.csv"
)
LISTINGS_PATH = None
for p in (
    Path("listings.csv"),
    Path("../listings.csv"),
    Path("../../data/listings.csv"),
    Path("../../../data/listings.csv"),
    Path("../data/listings.csv"),
):
    if p.exists():
        LISTINGS_PATH = p.resolve()
        break
if LISTINGS_PATH is None:
    LISTINGS_PATH = LISTINGS_URL
assert LISTINGS_PATH is not None"""

LOAD_DATA_NEW = (
    "from pathlib import Path\n"
    "import pandas as pd\n\n\n"
    + NEW_FIND
    + "\n"
)


def patch_source(src: str) -> str:
    out = src
    if "LISTINGS_URL" not in out and "find_listings_csv" in out and "raise FileNotFoundError" in out:
        out = out.replace(OLD_FIND, NEW_FIND)
        # notebooks may use double-quote variants already — also try normalized
    if "LISTINGS_URL" not in out and "find_listings_csv" in out:
        # flexible replace via regex
        out2 = re.sub(
            r"def find_listings_csv\(\)[^\n]*:\n"
            r"(?:    .*\n)+?"
            r"    raise FileNotFoundError\([^\n]+\)\n\n\n"
            r"LISTINGS_PATH = find_listings_csv\(\)\n"
            r"df = pd\.read_csv\(LISTINGS_PATH\)",
            NEW_FIND,
            out,
            count=1,
        )
        if out2 != out:
            out = out2
    if "LISTINGS_URL" not in out and "LISTINGS_PATH = None" in out and "for p in" in out:
        out = out.replace(OLD_LOOP, NEW_LOOP)
        if "LISTINGS_URL" not in out:
            out2 = re.sub(
                r"LISTINGS_PATH = None\n"
                r"for p in \([^)]+\):\n"
                r"    if p\.exists\(\):\n"
                r"        LISTINGS_PATH = p\.resolve\(\)\n"
                r"        break\n"
                r"assert LISTINGS_PATH is not None",
                NEW_LOOP,
                out,
                count=1,
            )
            out = out2
    return out


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
        new = patch_source(src)
        if new != src:
            cell["source"] = to_nb_source(new)
            changed = True
    if changed:
        path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("patched", path.relative_to(ROOT))
    return changed


def patch_generator() -> None:
    gen = MODULE / "generate_notebooks.py"
    text = gen.read_text(encoding="utf-8")
    if "LISTINGS_URL" in text and "raw.githubusercontent.com" in text.split("LOAD_DATA")[1][:800]:
        print("generate_notebooks.py already patched LOAD_DATA")
    else:
        old = (
            "LOAD_DATA = (\n"
            '    "from pathlib import Path\\n"\n'
            '    "import pandas as pd\\n\\n\\n"\n'
            '    "def find_listings_csv() -> Path:\\n"\n'
            '    "    for p in (Path(\'listings.csv\'), Path(\'../../data/listings.csv\'), Path(\'../data/listings.csv\')):\\n"\n'
            '    "        if p.exists():\\n"\n'
            '    "            return p.resolve()\\n"\n'
            '    "    raise FileNotFoundError(\'listings.csv не найден\')\\n\\n\\n"\n'
            '    "LISTINGS_PATH = find_listings_csv()\\n"\n'
            '    "df = pd.read_csv(LISTINGS_PATH)\\n"\n'
            ")"
        )
        # Build from LOAD_DATA_NEW
        lines = []
        for line in LOAD_DATA_NEW.splitlines(keepends=True):
            escaped = line.replace("\\", "\\\\").replace('"', '\\"')
            lines.append(f'    "{escaped}"')
        new = "LOAD_DATA = (\n" + "\n".join(lines) + "\n)"
        if old in text:
            text = text.replace(old, new)
            print("patched LOAD_DATA in generate_notebooks.py")
        else:
            # looser: replace from LOAD_DATA = to closing ) before IMPORTS_MPL
            m = re.search(r"LOAD_DATA = \([\s\S]*?\n\)\n\nIMPORTS_MPL", text)
            if m:
                text = text[: m.start()] + new + "\n\nIMPORTS_MPL" + text[m.end() :]
                print("patched LOAD_DATA (loose) in generate_notebooks.py")
            else:
                print("WARN: could not patch LOAD_DATA")

    # try/except path loop in generator
    if OLD_LOOP.replace("'", "'") in text or "LISTINGS_PATH = None\\n" in text:
        text2 = text.replace(
            '        "LISTINGS_PATH = None\\n"\n'
            '        "for p in (Path(\'listings.csv\'), Path(\'../../data/listings.csv\'), Path(\'../data/listings.csv\')):\\n"\n'
            '        "    if p.exists():\\n"\n'
            '        "        LISTINGS_PATH = p.resolve()\\n"\n'
            '        "        break\\n"\n'
            '        "assert LISTINGS_PATH is not None\\n"',
            "\n".join(
                f'        "{line}\\n"'
                for line in NEW_LOOP.splitlines()
            ),
        )
        if text2 != text:
            text = text2
            print("patched try/except LISTINGS_PATH loop in generate_notebooks.py")
        else:
            # homework variant without trailing df=
            text2 = re.sub(
                r'        "LISTINGS_PATH = None\\n"\n'
                r'        "for p in \(Path\(\'listings\.csv\'\), Path\(\'\.\./\.\./data/listings\.csv\'\), Path\(\'\.\./data/listings\.csv\'\)\):\\n"\n'
                r'        "    if p\.exists\(\):\\n"\n'
                r'        "        LISTINGS_PATH = p\.resolve\(\)\\n"\n'
                r'        "        break\\n"\n'
                r'        "assert LISTINGS_PATH is not None\\n"',
                "\n".join(f'        "{line}\\n"' for line in NEW_LOOP.splitlines()),
                text,
            )
            if text2 != text:
                text = text2
                print("patched try/except loop via regex")
            else:
                print("WARN: try/except loop not found as expected")

    gen.write_text(text, encoding="utf-8")


def main() -> None:
    n = 0
    for path in sorted(MODULE.rglob("*.ipynb")):
        if patch_nb(path):
            n += 1
    print(f"notebooks changed: {n}")
    patch_generator()


if __name__ == "__main__":
    main()
