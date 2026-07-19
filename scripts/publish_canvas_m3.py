#!/usr/bin/env python3
"""Publish module 08_03 (pairs 17-23) to Canvas course 6465."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "modules/08_03_titanic_eda"
LESSONS = MODULE / "lessons"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from canvas_api import canvas_get, canvas_post, require_canvas_auth  # noqa: E402
from publish_canvas_lesson import (  # noqa: E402
    add_homework_assignment_item,
    add_module_item,
    add_solutions_item,
    upsert_lesson_page,
    LESSON_ITEM_TITLE,
    PLAN_ITEM_TITLE,
)

GIST_USER = "gurovic"
COURSE_DEFAULT = 6465
MODULE_NAME = "Модуль 3. Титаник: EDA и статистика"


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


PAIRS = {
    17: Pair(17, "01_load_inspect_paths", "Пара 17. Загрузка Titanic, осмотр, пути", "para-17-plan-uroka-dlia-priepodavatielia"),
    18: Pair(18, "02_practice_inspect", "Пара 18. Практика: осмотр таблицы", "para-18-plan-uroka-dlia-priepodavatielia"),
    19: Pair(19, "03_mean_median_std", "Пара 19. Среднее, медиана, std", "para-19-plan-uroka-dlia-priepodavatielia"),
    20: Pair(20, "04_practice_boxplot", "Пара 20. Практика: квартили, boxplot", "para-20-plan-uroka-dlia-priepodavatielia"),
    21: Pair(21, "05_bias_clt_missing", "Пара 21. Bias, ЦПТ, пропуски", "para-21-plan-uroka-dlia-priepodavatielia"),
    22: Pair(22, "06_practice_groups", "Пара 22. Практика: группы и пропуски", "para-22-plan-uroka-dlia-priepodavatielia"),
    23: Pair(23, "07_eda_report", "Пара 23. EDA-отчёт — сборка и сдача", "para-23-plan-uroka-dlia-priepodavatielia"),
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
    parser = argparse.ArgumentParser(description="Publish M3 to Canvas")
    parser.add_argument("--course-id", type=int, default=COURSE_DEFAULT)
    parser.add_argument("--module-id", type=int, default=None)
    parser.add_argument("--pair", type=int, default=None, help="KTP pair 17-23")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--update-page-only", action="store_true")
    parser.add_argument(
        "--gist-map",
        type=Path,
        default=MODULE / "canvas_gist_map.json",
    )
    args = parser.parse_args()

    require_canvas_auth()
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
