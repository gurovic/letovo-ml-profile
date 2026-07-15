#!/usr/bin/env python3
"""Publish or update a lesson pair in Canvas (wiki LESSON.md + module items)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from canvas_api import canvas_post, canvas_put  # noqa: E402
from lesson_md_html import lesson_md_to_canvas_html  # noqa: E402


PAGE_TITLE = "Пара 2 — план урока (для преподавателя)"
SUBHEADER = "Пара 2. Функция-предсказатель: от правила к выбору модели"
PLAN_ITEM_TITLE = "Пара 2 — план урока (для преподавателя)"
LESSON_ITEM_TITLE = "Ноутбук урока"
HOMEWORK_ITEM_TITLE = "Домашнее задание"


def upsert_lesson_page(
    course_id: int,
    *,
    title: str,
    markdown_path: Path,
    page_url: str | None = None,
) -> dict:
    md = markdown_path.read_text(encoding="utf-8")
    body = lesson_md_to_canvas_html(md)
    payload = {
        "wiki_page[title]": title,
        "wiki_page[body]": body,
        "wiki_page[published]": "false",
        "wiki_page[editing_role]": "teachers",
    }
    if page_url:
        return canvas_put(f"courses/{course_id}/pages/{page_url}", payload)
    return canvas_post(f"courses/{course_id}/pages", payload)


def publish_pair_2(
    course_id: int,
    module_id: int,
    lesson_md: Path,
    lesson_nb_url: str,
    homework_nb_url: str,
    *,
    page_url: str | None = None,
    items_only: bool = False,
) -> dict:
    page: dict | None = None
    if not items_only:
        page = upsert_lesson_page(
            course_id,
            title=PAGE_TITLE,
            markdown_path=lesson_md,
            page_url=page_url,
        )
    resolved_page_url = (page or {}).get("url", page_url or "m1-p2-lesson")

    if items_only:
        return {
            "course_id": course_id,
            "module_id": module_id,
            "page": {"url": resolved_page_url, "updated": True},
            "items": [],
        }

    payloads = [
        {
            "module_item[title]": SUBHEADER,
            "module_item[type]": "SubHeader",
            "module_item[indent]": "0",
        },
        {
            "module_item[title]": PLAN_ITEM_TITLE,
            "module_item[type]": "Page",
            "module_item[page_url]": resolved_page_url,
            "module_item[indent]": "1",
            "module_item[published]": "false",
        },
        {
            "module_item[title]": LESSON_ITEM_TITLE,
            "module_item[type]": "ExternalUrl",
            "module_item[external_url]": lesson_nb_url,
            "module_item[indent]": "1",
            "module_item[published]": "true",
            "module_item[new_tab]": "true",
        },
        {
            "module_item[title]": HOMEWORK_ITEM_TITLE,
            "module_item[type]": "ExternalUrl",
            "module_item[external_url]": homework_nb_url,
            "module_item[indent]": "1",
            "module_item[published]": "true",
            "module_item[new_tab]": "true",
        },
    ]

    items = []
    for payload in payloads:
        items.append(canvas_post(f"courses/{course_id}/modules/{module_id}/items", payload))

    return {
        "course_id": course_id,
        "module_id": module_id,
        "page": {"page_id": page.get("page_id"), "url": resolved_page_url},
        "items": [
            {"id": item.get("id"), "type": item.get("type"), "title": item.get("title")}
            for item in items
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish lesson pair 2 to Canvas")
    parser.add_argument("--course-id", type=int, default=6465)
    parser.add_argument("--module-id", type=int, default=54688)
    parser.add_argument(
        "--lesson-md",
        type=Path,
        default=ROOT
        / "modules/08_01_functions_recursion/lessons/02_function_as_mapping/LESSON.md",
    )
    parser.add_argument(
        "--lesson-nb-url",
        default="https://colab.research.google.com/gist/gurovic/cfc377717ba193c512a9e88593405ab8/lesson.ipynb",
    )
    parser.add_argument(
        "--homework-nb-url",
        default="https://colab.research.google.com/gist/gurovic/15255de29367ddc86fb8d141f63b5cfd/homework.ipynb",
    )
    parser.add_argument(
        "--page-url",
        help="Update existing wiki page slug instead of creating a new page",
    )
    parser.add_argument(
        "--update-page-only",
        action="store_true",
        help="Only re-render LESSON.md to wiki HTML (no new module items)",
    )
    args = parser.parse_args()

    if args.update_page_only:
        if not args.page_url:
            parser.error("--update-page-only requires --page-url")
        page = upsert_lesson_page(
            args.course_id,
            title=PAGE_TITLE,
            markdown_path=args.lesson_md,
            page_url=args.page_url,
        )
        print(json.dumps({"page": {"url": page.get("url"), "page_id": page.get("page_id")}}, ensure_ascii=False, indent=2))
        return

    result = publish_pair_2(
        args.course_id,
        args.module_id,
        args.lesson_md,
        args.lesson_nb_url,
        args.homework_nb_url,
        page_url=args.page_url,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
