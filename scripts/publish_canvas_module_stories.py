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

from canvas_api import canvas_config, canvas_delete, canvas_get, canvas_post, canvas_put, require_canvas_auth  # noqa: E402
from lesson_md_html import lesson_md_to_canvas_html  # noqa: E402
from publish_canvas_lesson import add_module_item  # noqa: E402

COURSE_ID = 6465
STORY_ITEM_TITLE = "Сюжет модуля"
DEFAULT_SLUG_RE = re.compile(r"^modul-\d+-sujet$")

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

# Orphan slugs from earlier publishes (M1).
LEGACY_PAGE_SLUGS = frozenset({"siuzhiet-modulia"})


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


def delete_wiki_page(course_id: int, slug: str) -> None:
    if not wiki_page_exists(course_id, slug):
        return
    try:
        canvas_delete(f"courses/{course_id}/pages/{slug}")
    except SystemExit:
        pass


def upsert_story_page(
    course_id: int,
    slug: str,
    *,
    page_title: str,
    story_text: str,
) -> dict:
    """Wiki title = русский tagline; тело = только текст сюжета (без h2)."""
    body = lesson_md_to_canvas_html(story_text, course_id=course_id)
    payload = {
        "wiki_page[title]": page_title,
        "wiki_page[body]": body,
        "wiki_page[published]": "true",
        "wiki_page[editing_role]": "teachers",
    }
    if wiki_page_exists(course_id, slug):
        page = canvas_put(f"courses/{course_id}/pages/{slug}", payload)
    else:
        page = canvas_post(f"courses/{course_id}/pages", payload)
    if not isinstance(page, dict):
        raise SystemExit(f"Unexpected Canvas page response: {page!r}")
    return page


def is_story_module_item(item: dict, default_slug: str) -> bool:
    if item.get("type") != "Page":
        return False
    title = str(item.get("title") or "")
    page_url = str(item.get("page_url") or "")
    if title == STORY_ITEM_TITLE:
        return True
    if page_url == default_slug or title == default_slug:
        return True
    if page_url in LEGACY_PAGE_SLUGS or title in LEGACY_PAGE_SLUGS:
        return True
    if DEFAULT_SLUG_RE.match(page_url) or DEFAULT_SLUG_RE.match(title):
        return True
    return False


def remove_story_module_items(course_id: int, module_id: int, default_slug: str) -> None:
    items = canvas_get(f"courses/{course_id}/modules/{module_id}/items", paginate=True)
    for item in items:
        if is_story_module_item(item, default_slug):
            canvas_delete(f"courses/{course_id}/modules/{module_id}/items/{item['id']}")


def cleanup_legacy_pages(course_id: int, active_slug: str, default_slug: str) -> None:
    for slug in LEGACY_PAGE_SLUGS | {default_slug}:
        if slug != active_slug:
            delete_wiki_page(course_id, slug)


def publish_module(
    course_id: int,
    module_dir: str,
    module_id: int,
    default_slug: str,
) -> dict:
    unit_path = ROOT / "modules" / module_dir / "UNIT.md"
    page_title, story = extract_story(unit_path)
    page = upsert_story_page(
        course_id,
        default_slug,
        page_title=page_title,
        story_text=story,
    )
    active_slug = str(page.get("url") or default_slug)
    remove_story_module_items(course_id, module_id, default_slug)
    item = add_module_item(
        course_id,
        module_id,
        {
            "module_item[title]": STORY_ITEM_TITLE,
            "module_item[type]": "Page",
            "module_item[page_url]": active_slug,
            "module_item[indent]": "0",
            "module_item[published]": "true",
            "module_item[position]": "1",
        },
    )
    cleanup_legacy_pages(course_id, active_slug, default_slug)
    return {
        "module": module_dir,
        "page": active_slug,
        "page_title": page.get("title", page_title),
        "item_id": item.get("id"),
    }


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
        print(f"STORY {module_dir} → module {mid} slug {page_url}")
        results.append(publish_module(args.course_id, module_dir, mid, page_url))
    out = args.map.parent / "canvas_module_stories.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
