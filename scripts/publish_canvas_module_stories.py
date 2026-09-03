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
from publish_canvas_lesson import add_module_item, clean_canvas_title  # noqa: E402

COURSE_ID = 6465
STORY_ITEM_TITLE = "Сюжет модуля"
DEFAULT_SLUG_RE = re.compile(r"^modul-\d+-sujet$")
TAGLINE_TITLE_DUP_RE = re.compile(r"-\d+$")
LESSON_PAGE_RE = re.compile(r"^para-\d+")
URL_NUM_SUFFIX_RE = re.compile(r"-\d+$")

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

LEGACY_PAGE_SLUGS = frozenset({"siuzhiet-modulia"})


def load_module_ids(path: Path) -> dict[str, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {k: int(v) for k, v in data["modules"].items()}


def load_previous_story_map(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    rows = json.loads(path.read_text(encoding="utf-8"))
    return {row["module"]: row for row in rows if isinstance(row, dict) and "module" in row}


def extract_story(unit_path: Path) -> tuple[str, str]:
    text = unit_path.read_text(encoding="utf-8-sig")
    tagline_m = re.search(r"\| Сюжет модуля \| (.+?) \|", text)
    tagline = clean_canvas_title(tagline_m.group(1).strip()) if tagline_m else unit_path.parent.name
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
    if not slug or not wiki_page_exists(course_id, slug):
        return
    try:
        canvas_delete(f"courses/{course_id}/pages/{slug}")
    except SystemExit:
        pass


def title_is_tagline_duplicate(title: str, tagline: str) -> bool:
    if title == tagline:
        return True
    if title.startswith(tagline) and TAGLINE_TITLE_DUP_RE.match(title[len(tagline) :]):
        return True
    return False


def url_is_tagline_variant(url: str, known: set[str]) -> bool:
    """Только точное совпадение url или дубликат Canvas с суффиксом -2, -3 …"""
    if url in known:
        return True
    base = URL_NUM_SUFFIX_RE.sub("", url)
    for k in known:
        if not k:
            continue
        kb = URL_NUM_SUFFIX_RE.sub("", k)
        if base == kb:
            return True
        if url.startswith(k + "-") and TAGLINE_TITLE_DUP_RE.search(url[len(k) :]):
            return True
    return False


def build_story_url_set(
    course_id: int,
    *,
    slug: str,
    tagline: str,
    previous_url: str | None,
) -> set[str]:
    """URL кандидаты на удаление после успешного upsert (не para-* и не чужие модули)."""
    urls: set[str] = {slug, *LEGACY_PAGE_SLUGS}
    if previous_url:
        urls.add(previous_url)
        urls.add(URL_NUM_SUFFIX_RE.sub("", previous_url))
    pages = canvas_get(f"courses/{course_id}/pages", paginate=True)
    if isinstance(pages, list):
        for page in pages:
            url = str(page.get("url") or "")
            title = str(page.get("title") or "")
            if not url or LESSON_PAGE_RE.match(url):
                continue
            if title_is_tagline_duplicate(title, tagline):
                urls.add(url)
            if previous_url and url_is_tagline_variant(url, {previous_url}):
                urls.add(url)
    return {u for u in urls if u}


def purge_tagline_pages(course_id: int, tagline: str, *, keep_slug: str) -> None:
    """Удалить дубликаты wiki с тем же tagline, кроме активной страницы."""
    pages = canvas_get(f"courses/{course_id}/pages", paginate=True)
    if not isinstance(pages, list):
        return
    for page in pages:
        url = str(page.get("url") or "")
        title = str(page.get("title") or "")
        if not url or url == keep_slug:
            continue
        if title_is_tagline_duplicate(title, tagline):
            delete_wiki_page(course_id, url)


def delete_story_orphans(course_id: int, *, keep_slug: str, story_urls: set[str]) -> None:
    for url in story_urls:
        if url != keep_slug:
            delete_wiki_page(course_id, url)


def resolve_story_page_url(
    course_id: int,
    module_id: int,
    *,
    slug: str,
    previous_url: str | None,
) -> str | None:
    if previous_url and wiki_page_exists(course_id, previous_url):
        return previous_url
    if wiki_page_exists(course_id, slug):
        return slug
    items = canvas_get(f"courses/{course_id}/modules/{module_id}/items", paginate=True)
    for item in items:
        if item.get("title") == STORY_ITEM_TITLE and item.get("page_url"):
            url = str(item["page_url"])
            if wiki_page_exists(course_id, url):
                return url
    return None


def upsert_story_page(
    course_id: int,
    slug: str,
    *,
    tagline: str,
    story_text: str,
    existing_url: str | None = None,
) -> dict:
    """Русский tagline = заголовок wiki (виден при открытии страницы)."""
    if not story_text.strip():
        raise SystemExit("Story text is empty — refusing to publish blank wiki")
    body = lesson_md_to_canvas_html(story_text, course_id=course_id)
    if len(body) < 80:
        raise SystemExit(f"Rendered story HTML too short ({len(body)} chars)")
    payload = {
        "wiki_page[title]": clean_canvas_title(tagline),
        "wiki_page[body]": body,
        "wiki_page[published]": "true",
        "wiki_page[editing_role]": "teachers",
    }
    target = existing_url or (slug if wiki_page_exists(course_id, slug) else None)
    if target:
        page = canvas_put(f"courses/{course_id}/pages/{target}", payload)
    else:
        page = canvas_post(f"courses/{course_id}/pages", payload)
    if not isinstance(page, dict):
        raise SystemExit(f"Unexpected Canvas page response: {page!r}")
    return page


def verify_wiki_body(course_id: int, slug: str, *, min_len: int = 80) -> None:
    page = canvas_get(f"courses/{course_id}/pages/{slug}")
    body = str((page or {}).get("body") or "")
    text = re.sub(r"<[^>]+>", "", body).strip()
    if len(text) < min_len // 4:
        raise SystemExit(
            f"Wiki `{slug}` body empty or too short after publish "
            f"(html={len(body)}, text≈{len(text)})"
        )


def is_story_module_item(
    item: dict,
    *,
    slug: str,
    tagline: str,
    story_urls: set[str],
) -> bool:
    if item.get("type") != "Page":
        return False
    page_url = str(item.get("page_url") or "")
    title = str(item.get("title") or "")
    if LESSON_PAGE_RE.match(page_url):
        return False
    if title == STORY_ITEM_TITLE:
        return True
    if page_url in story_urls or url_is_tagline_variant(page_url, story_urls):
        return True
    if title_is_tagline_duplicate(title, tagline):
        return True
    if page_url == slug or DEFAULT_SLUG_RE.match(page_url):
        return True
    if page_url in LEGACY_PAGE_SLUGS or title in LEGACY_PAGE_SLUGS:
        return True
    # Пункт назван slug'ом страницы (siuzhiet-modulia, analitiki-staylocal-…)
    if title == page_url and page_url and int(item.get("position") or 99) <= 5:
        return True
    return False


def remove_story_module_items(
    course_id: int,
    module_id: int,
    *,
    slug: str,
    tagline: str,
    story_urls: set[str],
) -> None:
    items = canvas_get(f"courses/{course_id}/modules/{module_id}/items", paginate=True)
    for item in items:
        if is_story_module_item(item, slug=slug, tagline=tagline, story_urls=story_urls):
            canvas_delete(f"courses/{course_id}/modules/{module_id}/items/{item['id']}")


def publish_module(
    course_id: int,
    module_dir: str,
    module_id: int,
    slug: str,
    *,
    previous: dict | None,
) -> dict:
    unit_path = ROOT / "modules" / module_dir / "UNIT.md"
    tagline, story = extract_story(unit_path)
    prev_url = str(previous.get("page")) if previous and previous.get("page") else None
    existing_url = resolve_story_page_url(
        course_id, module_id, slug=slug, previous_url=prev_url
    )
    story_urls = build_story_url_set(
        course_id,
        slug=slug,
        tagline=tagline,
        previous_url=prev_url or existing_url,
    )
    remove_story_module_items(
        course_id,
        module_id,
        slug=slug,
        tagline=tagline,
        story_urls=story_urls,
    )
    page = upsert_story_page(
        course_id,
        slug,
        tagline=tagline,
        story_text=story,
        existing_url=existing_url,
    )
    active_slug = str(page.get("url") or existing_url or slug)
    verify_wiki_body(course_id, active_slug)
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
    delete_story_orphans(course_id, keep_slug=active_slug, story_urls=story_urls)
    purge_tagline_pages(course_id, tagline, keep_slug=active_slug)
    return {
        "module": module_dir,
        "page": active_slug,
        "page_title": tagline,
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
    parser.add_argument(
        "--module",
        help="Only publish one module dir, e.g. 08_03_titanic_eda",
    )
    parser.add_argument(
        "--skip-audit",
        action="store_true",
        help="Do not run canvas_controller after publish",
    )
    args = parser.parse_args()
    require_canvas_auth()
    module_ids = load_module_ids(args.map)
    story_map_path = args.map.parent / "canvas_module_stories.json"
    previous_map = load_previous_story_map(story_map_path)
    results = []
    modules = MODULES
    if args.module:
        modules = [m for m in MODULES if m[0] == args.module]
        if not modules:
            raise SystemExit(f"Unknown module {args.module!r}")
    for module_dir, _num, slug in modules:
        mid = module_ids.get(module_dir)
        if not mid:
            raise SystemExit(f"No module_id for {module_dir}")
        print(f"STORY {module_dir} → module {mid} slug {slug}")
        results.append(
            publish_module(
                args.course_id,
                module_dir,
                mid,
                slug,
                previous=previous_map.get(module_dir),
            )
        )
    if args.module and story_map_path.exists():
        merged = previous_map
        for row in results:
            merged[row["module"]] = row
        out = [merged[m[0]] for m in MODULES if m[0] in merged]
        story_map_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        story_map_path.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {story_map_path}")
    if not args.skip_audit:
        from canvas_controller import run_post_publish_audit

        module_dirs = [m[0] for m in modules]
        if not run_post_publish_audit(args.course_id, module_dirs=module_dirs):
            raise SystemExit("Canvas controller: errors after publish (see above)")


if __name__ == "__main__":
    main()
