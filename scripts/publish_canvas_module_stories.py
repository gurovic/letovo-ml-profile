#!/usr/bin/env python3
"""Publish module story wiki pages to Canvas (from UNIT.md §1 «Описание сюжета»)."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from canvas_api import canvas_config, canvas_get, canvas_post, canvas_put, require_canvas_auth  # noqa: E402
from lesson_md_html import lesson_md_to_canvas_html  # noqa: E402
from publish_canvas_lesson import add_module_item  # noqa: E402

COURSE_ID = 6465
STORY_ITEM_TITLE = "Сюжет модуля"

MODULES: list[tuple[str, int, str]] = [
    ("08_01_functions_recursion", 1, "modul-1-sujet"),
    ("08_02_carsharing_pandas_lr", 2, "modul-2-sujet"),
    ("08_03_titanic_eda", 3, "modul-3-sujet"),
    ("08_04_mnist_knn", 4, "modul-4-sujet"),
    ("08_05_shop_feature_engineering", 5, "modul-5-sujet"),
    ("08_06_ab_startup", 6, "modul-6-sujet"),
    ("08_07_bank_arrays_search", 7, "modul-7-sujet"),
    ("08_08_logistics_clustering", 8, "modul-8-sujet"),
    ("08_10_churn_logreg", 9, "modul-9-sujet"),
    ("08_11_virtual_polygon", 10, "modul-10-sujet"),
    ("08_09_courier_dp", 11, "modul-11-sujet"),
]


def load_module_ids(path: Path) -> dict[str, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {k: int(v) for k, v in data["modules"].items()}


def extract_story(unit_path: Path) -> tuple[str, str]:
    text = unit_path.read_text(encoding="utf-8-sig")
    tagline_m = re.search(r"\| Сюжет модуля \| (.+?) \|", text)
    tagline = tagline_m.group(1).strip() if tagline_m else unit_path.parent.name
    story_m = re.search(
        r"### Описание сюжета\s*\n\n(.*?)(?=\n---|\n## )",
        text,
        re.DOTALL,
    )
    if not story_m:
        raise SystemExit(f"No «Описание сюжета» in {unit_path}")
    return tagline, story_m.group(1).strip()


def wiki_page_exists(course_id: int, slug: str) -> bool:
    api_url, token = canvas_config()
    url = f"{api_url}/courses/{course_id}/pages/{slug}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=90):
            return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        raise


def upsert_story_page(course_id: int, slug: str, markdown: str) -> dict:
    body = lesson_md_to_canvas_html(markdown, course_id=course_id)
    payload = {
        "wiki_page[title]": slug,
        "wiki_page[body]": body,
        "wiki_page[published]": "true",
        "wiki_page[editing_role]": "teachers",
    }
    if wiki_page_exists(course_id, slug):
        page = canvas_put(f"courses/{course_id}/pages/{slug}", payload)
    else:
        page = canvas_post(f"courses/{course_id}/pages", payload)
    if isinstance(page, dict) and page.get("url") != slug:
        raise SystemExit(f"Canvas changed page url to {page.get('url')!r} (wanted {slug!r})")
    return page


def find_story_item(items: list[dict], page_url: str) -> dict | None:
    for item in items:
        if item.get("title") == STORY_ITEM_TITLE and item.get("type") == "Page":
            return item
        if item.get("page_url") == page_url:
            return item
    return None


def ensure_story_item(
    course_id: int,
    module_id: int,
    page_url: str,
    *,
    position: int = 1,
) -> dict:
    items = canvas_get(f"courses/{course_id}/modules/{module_id}/items", paginate=True)
    existing = find_story_item(items, page_url)
    if existing:
        canvas_put(
            f"courses/{course_id}/modules/{module_id}/items/{existing['id']}",
            {
                "module_item[title]": STORY_ITEM_TITLE,
                "module_item[page_url]": page_url,
                "module_item[published]": "true",
                "module_item[position]": str(position),
            },
        )
        return existing
    return add_module_item(
        course_id,
        module_id,
        {
            "module_item[title]": STORY_ITEM_TITLE,
            "module_item[type]": "Page",
            "module_item[page_url]": page_url,
            "module_item[indent]": "0",
            "module_item[published]": "true",
            "module_item[position]": str(position),
        },
    )


def publish_module(
    course_id: int,
    module_dir: str,
    module_id: int,
    page_url: str,
) -> dict:
    unit_path = ROOT / "modules" / module_dir / "UNIT.md"
    mod_title, story = extract_story(unit_path)
    markdown = f"## {mod_title}\n\n{story}\n"
    page = upsert_story_page(course_id, page_url, markdown)
    item = ensure_story_item(course_id, module_id, page.get("url", page_url))
    return {"module": module_dir, "page": page.get("url", page_url), "item_id": item.get("id")}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--course-id", type=int, default=COURSE_ID)
    parser.add_argument(
        "--map",
        type=Path,
        default=ROOT / "modules" / "canvas_publish_draft4.json",
    )
    args = parser.parse_args()
    require_canvas_auth()
    module_ids = load_module_ids(args.map)
    results = []
    for module_dir, _num, page_url in MODULES:
        mid = module_ids.get(module_dir)
        if not mid:
            raise SystemExit(f"No module_id for {module_dir}")
        print(f"STORY {module_dir} → module {mid} page {page_url}")
        results.append(publish_module(args.course_id, module_dir, mid, page_url))
    out = args.map.parent / "canvas_module_stories.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
