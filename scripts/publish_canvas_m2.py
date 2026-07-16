#!/usr/bin/env python3
"""Publish module 08_02 (pairs 12-21) to Canvas course 6465."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "modules/08_02_carsharing_pandas_lr"
LESSONS = MODULE / "lessons"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from canvas_api import canvas_get, canvas_post, canvas_put  # noqa: E402
from lesson_md_html import lesson_md_to_canvas_html, prepare_lesson_md_for_canvas_teacher  # noqa: E402
from publish_canvas_lesson import (  # noqa: E402
    HOMEWORK_ITEM_TITLE,
    LESSON_ITEM_TITLE,
    PLAN_ITEM_TITLE,
    SOLUTIONS_ITEM_TITLE,
    add_homework_assignment_item,
    add_module_item,
    add_solutions_item,
    upsert_lesson_page,
)

GIST_USER = "gurovic"
COURSE_DEFAULT = 6465
MODULE_NAME = "Модуль 2. Каршеринг: pandas и линейная регрессия"


@dataclass(frozen=True)
class Pair:
    ktp: int
    folder: str
    subheader: str
    page_url: str
    lesson_gist: str | None = None
    homework_gist: str | None = None
    solutions_gist: str | None = None
    skip_homework: bool = False

    @property
    def lesson_md(self) -> Path:
        return LESSONS / self.folder / "LESSON.md"

    def colab(self, gist_id: str, filename: str) -> str:
        return f"https://colab.research.google.com/gist/{GIST_USER}/{gist_id}/{filename}"


PAIRS: dict[int, Pair] = {
    12: Pair(12, "01_pandas_dataframe", "Пара 12. pandas: DataFrame, feature / target", "para-12-plan-uroka-dlia-priepodavatielia"),
    13: Pair(13, "02_practice_filters", "Пара 13. Практика: фильтры и типы", "para-13-plan-uroka-dlia-priepodavatielia"),
    14: Pair(14, "03_eda_scatter", "Пара 14. EDA: describe и scatter", "para-14-plan-uroka-dlia-priepodavatielia"),
    15: Pair(15, "04_train_test_lr", "Пара 15. train/test и LinearRegression", "para-15-plan-uroka-dlia-priepodavatielia"),
    16: Pair(16, "05_practice_metrics", "Пара 16. Практика: MSE и R²", "para-16-plan-uroka-dlia-priepodavatielia"),
    17: Pair(17, "06_try_except_csv", "Пара 17. try/except при загрузке CSV", "para-17-plan-uroka-dlia-priepodavatielia"),
    18: Pair(18, "07_practice_features", "Пара 18. Практика: сравнение признаков", "para-18-plan-uroka-dlia-priepodavatielia"),
    19: Pair(19, "08_multifeature_overview", "Пара 19. Несколько признаков (обзор)", "para-19-plan-uroka-dlia-priepodavatielia"),
    20: Pair(20, "09_report_draft", "Пара 20. Мини-отчёт — черновик", "para-20-plan-uroka-dlia-priepodavatielia"),
    21: Pair(
        21,
        "10_report_submit",
        "Пара 21. Сдача отчёта",
        "para-21-plan-uroka-dlia-priepodavatielia",
        skip_homework=True,
    ),
}


def ensure_module(course_id: int) -> int:
    modules = canvas_get(f"courses/{course_id}/modules", paginate=True)
    for m in modules:
        if m.get("name") == MODULE_NAME:
            return int(m["id"])
    created = canvas_post(
        f"courses/{course_id}/modules",
        {"module[name]": MODULE_NAME, "module[published]": "true"},
    )
    return int(created["id"])


def publish_pair(
    course_id: int,
    module_id: int,
    pair: Pair,
    *,
    page_only: bool = False,
    gists: dict[str, str] | None = None,
) -> dict:
    gists = gists or {}
    lesson_gist = pair.lesson_gist or gists.get("lesson") or gists.get("gist_id")
    homework_gist = pair.homework_gist or gists.get("homework") or lesson_gist
    solutions_gist = pair.solutions_gist or gists.get("solutions") or lesson_gist

    lesson_url = pair.colab(lesson_gist, "lesson.ipynb") if lesson_gist else ""
    homework_url = (
        pair.colab(homework_gist, "homework.ipynb")
        if homework_gist and not pair.skip_homework
        else ""
    )
    solutions_url = pair.colab(solutions_gist, "solutions.ipynb") if solutions_gist else ""

    page = upsert_lesson_page(
        course_id,
        title=f"Пара {pair.ktp} — план урока (для преподавателя)",
        markdown_path=pair.lesson_md,
        page_url=pair.page_url,
        lesson_colab_url=lesson_url,
        homework_colab_url=homework_url,
    )
    result: dict = {"page": {"url": page.get("url"), "page_id": page.get("page_id")}}
    if page_only:
        return result

    add_module_item(
        course_id,
        module_id,
        {
            "module_item[title]": pair.subheader,
            "module_item[type]": "SubHeader",
            "module_item[published]": "true",
        },
    )
    add_module_item(
        course_id,
        module_id,
        {
            "module_item[title]": PLAN_ITEM_TITLE,
            "module_item[type]": "Page",
            "module_item[page_url]": pair.page_url,
            "module_item[indent]": "1",
            "module_item[published]": "false",
        },
    )
    if lesson_url:
        add_module_item(
            course_id,
            module_id,
            {
                "module_item[title]": LESSON_ITEM_TITLE,
                "module_item[type]": "ExternalUrl",
                "module_item[external_url]": lesson_url,
                "module_item[indent]": "1",
                "module_item[published]": "true",
                "module_item[new_tab]": "true",
            },
        )
    if solutions_url:
        add_solutions_item(course_id, module_id, solutions_url)
    if homework_url and not pair.skip_homework:
        hw = add_homework_assignment_item(
            course_id, module_id, homework_colab_url=homework_url
        )
        result["homework"] = hw
    return result


def load_gist_map(path: Path) -> dict[int, dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {int(k): v for k, v in data.items()}


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish M2 to Canvas")
    parser.add_argument("--course-id", type=int, default=COURSE_DEFAULT)
    parser.add_argument("--module-id", type=int, default=None)
    parser.add_argument("--pair", type=int, default=None, help="KTP pair 12-21")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--update-page-only", action="store_true")
    parser.add_argument(
        "--gist-map",
        type=Path,
        default=MODULE / "canvas_gist_map.json",
        help="JSON: {\"12\": {\"gist_id\": \"...\"}, ...}",
    )
    args = parser.parse_args()

    module_id = args.module_id or ensure_module(args.course_id)
    gist_map = load_gist_map(args.gist_map) if args.gist_map.exists() else {}

    pairs = list(PAIRS.values()) if args.all else [PAIRS[args.pair]] if args.pair else None
    if not pairs:
        raise SystemExit("Pass --pair N or --all")

    out = {"module_id": module_id, "pairs": {}}
    for pair in pairs:
        g = gist_map.get(pair.ktp, {})
        out["pairs"][pair.ktp] = publish_pair(
            args.course_id,
            module_id,
            pair,
            page_only=args.update_page_only,
            gists=g,
        )
        print(f"pair {pair.ktp}: ok")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
