#!/usr/bin/env python3
"""Publish module 08_02 (pairs 11-20) to Canvas course 6465."""

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
    11: Pair(
        11,
        "01_pandas_dataframe",
        "Пара 11. pandas: DataFrame, feature / target",
        "para-11-plan-uroka-dlia-priepodavatielia",
        lesson_gist="d19afee5ef0dcd2be593ea93d11ba26f",
        homework_gist="d19afee5ef0dcd2be593ea93d11ba26f",
        solutions_gist="d19afee5ef0dcd2be593ea93d11ba26f",
    ),
    12: Pair(
        12,
        "02_practice_filters",
        "Пара 12. Практика: фильтры и типы",
        "para-12-plan-uroka-dlia-priepodavatielia",
        lesson_gist="d7f6297f93377ee22e14e00e3e781cbc",
        homework_gist="d7f6297f93377ee22e14e00e3e781cbc",
        solutions_gist="d7f6297f93377ee22e14e00e3e781cbc",
    ),
    13: Pair(
        13,
        "03_eda_scatter",
        "Пара 13. EDA: describe и scatter",
        "para-13-plan-uroka-dlia-priepodavatielia",
        lesson_gist="195d27b46e4ce375e61e41830e0a3a60",
        homework_gist="195d27b46e4ce375e61e41830e0a3a60",
        solutions_gist="195d27b46e4ce375e61e41830e0a3a60",
    ),
    14: Pair(
        14,
        "04_train_test_lr",
        "Пара 14. train/test и LinearRegression",
        "para-14-plan-uroka-dlia-priepodavatielia",
        lesson_gist="4319bd3960b3b50ebc04ea49b3623ff3",
        homework_gist="4319bd3960b3b50ebc04ea49b3623ff3",
        solutions_gist="4319bd3960b3b50ebc04ea49b3623ff3",
    ),
    15: Pair(
        15,
        "05_practice_metrics",
        "Пара 15. Практика: MSE и R²",
        "para-15-plan-uroka-dlia-priepodavatielia",
        lesson_gist="1b64439fdc5f01fd2ef1f7a9190ebd20",
        homework_gist="1b64439fdc5f01fd2ef1f7a9190ebd20",
        solutions_gist="1b64439fdc5f01fd2ef1f7a9190ebd20",
    ),
    16: Pair(
        16,
        "06_try_except_csv",
        "Пара 16. try/except при загрузке CSV",
        "para-16-plan-uroka-dlia-priepodavatielia",
        lesson_gist="089cdafdda13bf74965ef262a23b511a",
        homework_gist="089cdafdda13bf74965ef262a23b511a",
        solutions_gist="089cdafdda13bf74965ef262a23b511a",
    ),
    17: Pair(
        17,
        "07_practice_features",
        "Пара 17. Практика: сравнение признаков",
        "para-17-plan-uroka-dlia-priepodavatielia",
        lesson_gist="fae97962ced6296b3d92ec0c985243a8",
        homework_gist="fae97962ced6296b3d92ec0c985243a8",
        solutions_gist="fae97962ced6296b3d92ec0c985243a8",
    ),
    18: Pair(
        18,
        "08_multifeature_overview",
        "Пара 18. Несколько признаков (обзор)",
        "para-18-plan-uroka-dlia-priepodavatielia",
        lesson_gist="4a7ce32878ae54ad8a992494cf2d84f2",
        homework_gist="4a7ce32878ae54ad8a992494cf2d84f2",
        solutions_gist="4a7ce32878ae54ad8a992494cf2d84f2",
    ),
    19: Pair(
        19,
        "09_report_draft",
        "Пара 19. Мини-отчёт — черновик",
        "para-19-plan-uroka-dlia-priepodavatielia",
        lesson_gist="7ccd6be939bc2c0c6a745a57c81b1bcd",
        homework_gist="7ccd6be939bc2c0c6a745a57c81b1bcd",
        solutions_gist="7ccd6be939bc2c0c6a745a57c81b1bcd",
    ),
    20: Pair(
        20,
        "10_report_submit",
        "Пара 20. Сдача отчёта",
        "para-20-plan-uroka-dlia-priepodavatielia",
        lesson_gist="2f707a5bf751c9c842849b2a66dacab4",
        solutions_gist="2f707a5bf751c9c842849b2a66dacab4",
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
    parser.add_argument("--pair", type=int, default=None, help="KTP pair 11-20")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--update-page-only", action="store_true")
    parser.add_argument(
        "--gist-map",
        type=Path,
        default=MODULE / "canvas_gist_map.json",
        help="JSON: {\"11\": {\"gist_id\": \"...\"}, ...}",
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
