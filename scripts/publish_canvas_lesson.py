#!/usr/bin/env python3
"""Publish or update a lesson pair in Canvas (wiki LESSON.md + module items)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_ROOT = ROOT / "modules/08_01_functions_recursion/lessons"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from canvas_api import (  # noqa: E402
    canvas_delete,
    canvas_get,
    canvas_post,
    canvas_put,
    canvas_upload_course_file,
    require_canvas_auth,
)
from lesson_md_html import (  # noqa: E402
    lesson_md_to_canvas_html,
    prepare_lesson_md_for_canvas_teacher,
)

PLAN_ITEM_TITLE = "План урока (для преподавателя)"
SOLUTIONS_ITEM_TITLE = "Решения (для преподавателя)"
LESSON_ITEM_TITLE = "Ноутбук урока"
HOMEWORK_ITEM_TITLE = "Домашнее задание"
HOMEWORK_POINTS = 8.0
HOMEWORK_TITLE_RE = re.compile(r"^Домашнее задание(?:,\s*урок\s+(\d+))?$")
PAIR_NUM_RE = re.compile(r"^Пара\s+(\d+)")


def homework_title(pair: int) -> str:
    """Название Assignment и пункта модуля: «Домашнее задание, урок N»."""
    return f"{HOMEWORK_ITEM_TITLE}, урок {pair}"


def is_homework_title(title: str) -> bool:
    return bool(HOMEWORK_TITLE_RE.match(str(title or "").strip()))


def pair_number_from_subheader(title: str) -> int | None:
    m = PAIR_NUM_RE.match(str(title or "").strip())
    return int(m.group(1)) if m else None
FEEDBACK_ITEM_TITLE = "Опрос перед следующей парой"
FEEDBACK_ITEM_TITLE_LEGACY = "Опрос после пары"
FEEDBACK_ITEM_TITLES = frozenset({FEEDBACK_ITEM_TITLE, FEEDBACK_ITEM_TITLE_LEGACY})
FEEDBACK_INSTRUCTIONS = (
    "Заполните опрос после выполнения домашнего задания, "
    "но до начала следующего урока."
)
FEEDBACK_QUESTIONS: tuple[tuple[str, str, str], ...] = (
    (
        "novelty",
        "multiple_choice",
        "Насколько материал был новым и сложным?",
    ),
    (
        "clarity",
        "multiple_choice",
        "Насколько понятно было на уроке / получилось выполнить ДЗ?",
    ),
    (
        "comment",
        "essay",
        "Что ещё вы бы хотели сказать?",
    ),
)
FEEDBACK_SCALE = (
    "1 — совсем нет",
    "2",
    "3 — средне",
    "4",
    "5 — очень",
)
ARTIFACT_MATERIALS_TITLE = "Материалы артефакта"
ARTIFACT_PROJECT_ITEM_TITLE = "Задание: text_stats"
ARTIFACT_STARTER_README_ITEM_TITLE = "Как делать (шаги)"
ARTIFACT_STARTER_CODE_ITEM_TITLE = "Стартовый код (zip)"
ARTIFACT_TEACHER_ITEM_TITLE = "Решения (для преподавателя): text_stats"
ARTIFACT_SUBMIT_TITLE = "Сдача артефакта text_stats"
GIST_USER = "gurovic"
ARTIFACT_ROOT = ROOT / "modules/08_01_functions_recursion/artifact"
ARTIFACT_PROJECT_SLUG = "artifact-project"
ARTIFACT_STARTER_README_SLUG = "artifact-starter-readme"
ARTIFACT_STARTER_CODE_SLUG = "artifact-starter-code"
ARTIFACT_TEACHER_SLUG = "artifact-teacher-solutions"
ARTIFACT_TEACHER_CODE_SLUG = "artifact-teacher-code"
ARTIFACT_ZIP_NAME = "text_stats_starter.zip"
ARTIFACT_TEACHER_ZIP_NAME = "text_stats_teacher_solutions.zip"


def clean_canvas_title(title: str) -> str:
    """Убрать края ячейки markdown-таблицы (| … |), случайно попавшие в title."""
    return title.strip().strip("|").strip()


@dataclass(frozen=True)
class PairPreset:
    subheader: str
    page_title: str
    page_url: str
    lesson_dir: str
    lesson_gist: str | None = None
    homework_gist: str | None = None
    solutions_gist: str | None = None
    orientation: bool = False
    artifact: bool = False
    insert_at_position: int | None = None
    skip_homework: bool = False

    @property
    def lesson_md(self) -> Path:
        return MODULE_ROOT / self.lesson_dir / "LESSON.md"

    def colab(self, gist_id: str, filename: str) -> str:
        return f"https://colab.research.google.com/gist/{GIST_USER}/{gist_id}/{filename}"


PAIR_PRESETS: dict[int, PairPreset] = {
    1: PairPreset(
        subheader="Пара 1. ИИ, ML и профиль: ориентация",
        page_title="Пара 1 — план урока (для преподавателя)",
        page_url="para-1-plan-uroka-dlia-priepodavatielia",
        lesson_dir="01_intro_profile",
        orientation=True,
        insert_at_position=1,
    ),
    2: PairPreset(
        subheader="Пара 2. Функция-предсказатель: от правила к выбору модели",
        page_title="Пара 2 — план урока (для преподавателя)",
        page_url="para-2-plan-uroka-dlia-priepodavatielia",
        lesson_dir="02_function_as_mapping",
        lesson_gist="0ea316100e0e8b082099240605e8d981",
        homework_gist="0ea316100e0e8b082099240605e8d981",
        solutions_gist="0ea316100e0e8b082099240605e8d981",
    ),
    3: PairPreset(
        subheader="Пара 3. Параметры и return — describe, scale, контракт transform",
        page_title="Пара 3 — план урока (для преподавателя)",
        page_url="para-3-plan-uroka-dlia-priepodavatielia",
        lesson_dir="03_parameters_and_return",
        lesson_gist="005984c15b4303c3eeab4b593d58b32c",
        homework_gist="005984c15b4303c3eeab4b593d58b32c",
        solutions_gist="005984c15b4303c3eeab4b593d58b32c",
    ),
    4: PairPreset(
        subheader="Пара 4. Практика: transform на новых данных",
        page_title="Пара 4 — план урока (для преподавателя)",
        page_url="para-4-plan-uroka-dlia-priepodavatielia",
        lesson_dir="04_practice_transform",
        lesson_gist="b2932e06a264060214da958de1b26ddb",
        homework_gist="b2932e06a264060214da958de1b26ddb",
        solutions_gist="b2932e06a264060214da958de1b26ddb",
    ),
    5: PairPreset(
        subheader="Пара 5. Scope и отладка — accuracy и типы ошибок",
        page_title="Пара 5 — план урока (для преподавателя)",
        page_url="para-5-plan-uroka-dlia-priepodavatielia",
        lesson_dir="05_scope_and_debugging",
        lesson_gist="b5ba1ff726ad2a5b867d31d90aa0b1aa",
        homework_gist="b5ba1ff726ad2a5b867d31d90aa0b1aa",
        solutions_gist="b5ba1ff726ad2a5b867d31d90aa0b1aa",
    ),
    6: PairPreset(
        subheader="Пара 6. Модули и импорт: код в .py, запуск из командной строки",
        page_title="Пара 6 — план урока (для преподавателя)",
        page_url="para-6-plan-uroka-dlia-priepodavatielia",
        lesson_dir="06_modules_cli",
        lesson_gist="bd748e58cb16d953e7ca8e28ba1c1394",
        homework_gist="bd748e58cb16d953e7ca8e28ba1c1394",
        solutions_gist="bd748e58cb16d953e7ca8e28ba1c1394",
    ),
    7: PairPreset(
        subheader="Пара 7. Рекурсия на данных — flatten и дерево категорий",
        page_title="Пара 7 — план урока (для преподавателя)",
        page_url="para-7-plan-uroka-dlia-priepodavatielia",
        lesson_dir="07_recursion",
        lesson_gist="a68c1a099865029657e58a81d56b91bc",
        homework_gist="a68c1a099865029657e58a81d56b91bc",
        solutions_gist="a68c1a099865029657e58a81d56b91bc",
    ),
    8: PairPreset(
        subheader="Пара 8. Итоговая работа text_stats — реализация, README, сдача",
        page_title="Пара 8 — план урока (для преподавателя)",
        page_url="para-8-plan-uroka-dlia-priepodavatielia",
        lesson_dir="08_artifact",
        artifact=True,
    ),
    9: PairPreset(
        subheader="Пара 9. Артефакт text_stats — проектирование и реализация",
        page_title="Пара 9 — план урока (для преподавателя)",
        page_url="para-9-plan-uroka-dlia-priepodavatielia",
        lesson_dir="08_artifact",
        artifact=True,
    ),
    10: PairPreset(
        subheader="Пара 10. Сдача артефакта text_stats",
        page_title="Пара 10 — план урока (для преподавателя)",
        page_url="para-10-plan-uroka-dlia-priepodavatielia",
        lesson_dir="08_artifact",
        artifact=True,
    ),
}


def slugify_page_url(pair: int, title: str) -> str:
    text = f"para-{pair}-plan-" + title.lower()
    text = text.replace("—", "-").replace("–", "-")
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:80] or f"para-{pair}-plan"


def upsert_lesson_page(
    course_id: int,
    *,
    title: str,
    markdown_path: Path,
    page_url: str | None = None,
    lesson_colab_url: str,
    homework_colab_url: str,
) -> dict:
    md = markdown_path.read_text(encoding="utf-8")
    md = prepare_lesson_md_for_canvas_teacher(md)
    body = lesson_md_to_canvas_html(
        md,
        lesson_colab_url=lesson_colab_url or None,
        homework_colab_url=homework_colab_url or None,
    )
    # Wiki published so teachers can open the plan; module item stays unpublished
    # (students do not see «План урока» in the module list — see 08_CANVAS §11.4).
    payload = {
        "wiki_page[title]": clean_canvas_title(title),
        "wiki_page[body]": body,
        "wiki_page[published]": "true",
        "wiki_page[editing_role]": "teachers",
    }
    if page_url:
        return canvas_put(f"courses/{course_id}/pages/{page_url}", payload)
    return canvas_post(f"courses/{course_id}/pages", payload)


def homework_assignment_description(homework_colab_url: str) -> str:
    return (
        f'<p><a href="{homework_colab_url}" target="_blank" rel="noopener">'
        "Открыть ноутбук с заданием в Colab</a></p>"
        "<p>Выполните задание в ноутбуке и сдайте заполненный файл "
        "<code>homework.ipynb</code> (формат <code>.ipynb</code>).</p>"
    )


def homework_text_assignment_description() -> str:
    return (
        "<p><strong>Вводное домашнее задание</strong> (текст, без ноутбука).</p>"
        "<p>По материалам ориентационной пары напишите <strong>3–5 предложений</strong>: "
        "зачем вам этот модуль + <strong>один открытый вопрос</strong> к году. "
        "Сдайте ответ текстом в поле ниже.</p>"
    )


def create_text_homework_assignment(
    course_id: int, *, pair: int, points: float = HOMEWORK_POINTS
) -> dict:
    title = homework_title(pair)
    payload = {
        "assignment[name]": title,
        "assignment[description]": homework_text_assignment_description(),
        "assignment[submission_types][]": "online_text_entry",
        "assignment[published]": "true",
        "assignment[points_possible]": str(points),
        "assignment[grading_type]": "points",
    }
    return canvas_post(f"courses/{course_id}/assignments", payload)


def add_homework_text_assignment_item(
    course_id: int,
    module_id: int,
    *,
    pair: int,
    position: int | None = None,
    assignment_id: int | None = None,
) -> dict:
    title = homework_title(pair)
    assignment = (
        {"id": assignment_id}
        if assignment_id
        else create_text_homework_assignment(course_id, pair=pair)
    )
    if assignment_id:
        canvas_put(
            f"courses/{course_id}/assignments/{assignment_id}",
            {"assignment[name]": title},
        )
    payload = {
        "module_item[title]": title,
        "module_item[type]": "Assignment",
        "module_item[content_id]": str(assignment["id"]),
        "module_item[indent]": "1",
        "module_item[published]": "true",
    }
    if position is not None:
        payload["module_item[position]"] = str(position)
    item = add_module_item(course_id, module_id, payload)
    return {
        "assignment_id": assignment["id"],
        "id": item.get("id"),
        "type": item.get("type"),
        "title": item.get("title"),
        "published": item.get("published"),
    }


def create_homework_assignment(
    course_id: int, *, pair: int, homework_colab_url: str, points: float = HOMEWORK_POINTS
) -> dict:
    payload = {
        "assignment[name]": homework_title(pair),
        "assignment[description]": homework_assignment_description(homework_colab_url),
        "assignment[submission_types][]": "online_upload",
        "assignment[allowed_extensions][]": "ipynb",
        "assignment[published]": "true",
        "assignment[points_possible]": str(points),
        "assignment[grading_type]": "points",
    }
    return canvas_post(f"courses/{course_id}/assignments", payload)


def update_homework_assignment(
    course_id: int,
    assignment_id: int,
    *,
    pair: int,
    homework_colab_url: str,
) -> dict:
    payload = {
        "assignment[name]": homework_title(pair),
        "assignment[description]": homework_assignment_description(homework_colab_url),
    }
    return canvas_put(f"courses/{course_id}/assignments/{assignment_id}", payload)


def add_module_item(course_id: int, module_id: int, payload: dict) -> dict:
    title_key = "module_item[title]"
    if title_key in payload and payload[title_key]:
        payload = {**payload, title_key: clean_canvas_title(str(payload[title_key]))}
    return canvas_post(f"courses/{course_id}/modules/{module_id}/items", payload)


def add_solutions_item(
    course_id: int,
    module_id: int,
    solutions_nb_url: str,
    *,
    position: int | None = None,
) -> dict:
    payload = {
        "module_item[title]": SOLUTIONS_ITEM_TITLE,
        "module_item[type]": "ExternalUrl",
        "module_item[external_url]": solutions_nb_url,
        "module_item[indent]": "1",
        "module_item[published]": "false",
        "module_item[new_tab]": "true",
    }
    if position is not None:
        payload["module_item[position]"] = str(position)
    item = add_module_item(course_id, module_id, payload)
    return {
        "id": item.get("id"),
        "type": item.get("type"),
        "title": item.get("title"),
        "published": item.get("published"),
    }


def add_homework_assignment_item(
    course_id: int,
    module_id: int,
    *,
    pair: int,
    homework_colab_url: str,
    position: int | None = None,
    assignment_id: int | None = None,
) -> dict:
    title = homework_title(pair)
    assignment = (
        {"id": assignment_id}
        if assignment_id
        else create_homework_assignment(
            course_id, pair=pair, homework_colab_url=homework_colab_url
        )
    )
    if assignment_id:
        canvas_put(
            f"courses/{course_id}/assignments/{assignment_id}",
            {"assignment[name]": title},
        )
    payload = {
        "module_item[title]": title,
        "module_item[type]": "Assignment",
        "module_item[content_id]": str(assignment["id"]),
        "module_item[indent]": "1",
        "module_item[published]": "true",
    }
    if position is not None:
        payload["module_item[position]"] = str(position)
    item = add_module_item(course_id, module_id, payload)
    return {
        "assignment_id": assignment["id"],
        "id": item.get("id"),
        "type": item.get("type"),
        "title": item.get("title"),
        "published": item.get("published"),
    }


def is_feedback_item(item: dict) -> bool:
    title = str(item.get("title") or "")
    if title in FEEDBACK_ITEM_TITLES:
        return True
    return item.get("type") == "Quiz" and title.startswith("Опрос")


def split_module_into_pair_blocks(
    items: list[dict],
) -> list[tuple[dict, list[dict]]]:
    """Блоки «Пара …»: (SubHeader, пункты блока включая SubHeader)."""
    sorted_items = sorted(items, key=lambda x: int(x.get("position") or 0))
    headers = [
        it
        for it in sorted_items
        if it.get("type") == "SubHeader"
        and str(it.get("title") or "").startswith("Пара ")
    ]
    blocks: list[tuple[dict, list[dict]]] = []
    for i, header in enumerate(headers):
        h_pos = int(header.get("position") or 0)
        next_pos = (
            int(headers[i + 1].get("position") or 0) if i + 1 < len(headers) else None
        )
        if next_pos is not None:
            block = [
                it
                for it in sorted_items
                if h_pos <= int(it.get("position") or 0) < next_pos
            ]
        else:
            block = [
                it for it in sorted_items if h_pos <= int(it.get("position") or 0)
            ]
        blocks.append((header, block))
    return blocks


def feedback_target_position(block_items: list[dict]) -> int:
    """Позиция опроса: сразу после ДЗ или после последнего материала блока."""
    content = [
        it
        for it in block_items
        if it.get("type") != "SubHeader" and not is_feedback_item(it)
    ]
    if not content:
        header = next(it for it in block_items if it.get("type") == "SubHeader")
        return int(header.get("position") or 0) + 1
    homework = [
        it for it in content if is_homework_title(str(it.get("title") or ""))
    ]
    if homework:
        return max(int(it.get("position") or 0) for it in homework) + 1
    return max(int(it.get("position") or 0) for it in content) + 1


def is_pair_subheader(item: dict) -> bool:
    return (
        item.get("type") == "SubHeader"
        and str(item.get("title") or "").startswith("Пара ")
    )


def plan_module_feedback_layout(
    items: list[dict],
) -> tuple[list[dict], list[dict], list[str]]:
    """Желаемый порядок: в каждом блоке пары опрос последним. Возвращает (desired, delete, missing_headers)."""
    sorted_items = sorted(items, key=lambda x: int(x.get("position") or 0))
    first_pair = next(
        (i for i, it in enumerate(sorted_items) if is_pair_subheader(it)),
        None,
    )
    if first_pair is None:
        return sorted_items, [], []

    prefix = sorted_items[:first_pair]
    pair_items = sorted_items[first_pair:]
    desired: list[dict] = list(prefix)
    to_delete: list[dict] = []
    missing_headers: list[str] = []

    i = 0
    while i < len(pair_items):
        it = pair_items[i]
        if not is_pair_subheader(it):
            desired.append(it)
            i += 1
            continue

        header_title = str(it.get("title") or "")
        block_content = [it]
        i += 1
        feedback_items: list[dict] = []
        while i < len(pair_items) and not is_pair_subheader(pair_items[i]):
            cur = pair_items[i]
            if is_feedback_item(cur):
                feedback_items.append(cur)
            else:
                block_content.append(cur)
            i += 1

        if len(feedback_items) > 1:
            feedback_items.sort(key=lambda x: int(x.get("position") or 0))
            to_delete.extend(feedback_items[:-1])
            feedback_items = [feedback_items[-1]]

        desired.extend(block_content)
        if feedback_items:
            desired.append(feedback_items[0])
        else:
            missing_headers.append(header_title)

    return desired, to_delete, missing_headers


def _simulate_module_move(
    positions: dict[int, int],
    item_id: int,
    new_pos: int,
) -> dict[int, int]:
    old_pos = positions[item_id]
    if old_pos == new_pos:
        return positions
    out = dict(positions)
    if new_pos > old_pos:
        for iid, pos in list(out.items()):
            if old_pos < pos <= new_pos:
                out[iid] = pos - 1
    else:
        for iid, pos in list(out.items()):
            if new_pos <= pos < old_pos:
                out[iid] = pos + 1
    out[item_id] = new_pos
    return out


def apply_module_item_order(
    course_id: int,
    module_id: int,
    desired: list[dict],
) -> int:
    """Переставить пункты модуля в заданном порядке (с конца, без refetch)."""
    desired_ids = [int(it["id"]) for it in desired if it.get("id")]
    if not desired_ids:
        return 0

    items = canvas_get(f"courses/{course_id}/modules/{module_id}/items", paginate=True)
    if not isinstance(items, list):
        return 0

    positions = {int(it["id"]): int(it.get("position") or 0) for it in items if it.get("id")}
    moves = 0

    for target_pos in range(len(desired_ids), 0, -1):
        item_id = desired_ids[target_pos - 1]
        if item_id not in positions:
            continue
        current_pos = positions[item_id]
        if current_pos == target_pos:
            continue
        canvas_put(
            f"courses/{course_id}/modules/{module_id}/items/{item_id}",
            {"module_item[position]": str(target_pos)},
        )
        positions = _simulate_module_move(positions, item_id, target_pos)
        moves += 1

    return moves


def feedback_quiz_description() -> str:
    return f"<p>{FEEDBACK_INSTRUCTIONS}</p>"


def create_feedback_quiz(course_id: int) -> dict:
    quiz = canvas_post(
        f"courses/{course_id}/quizzes",
        {
            "quiz[title]": FEEDBACK_ITEM_TITLE,
            "quiz[description]": feedback_quiz_description(),
            "quiz[quiz_type]": "survey",
            "quiz[published]": "false",
            "quiz[points_possible]": "0",
            "quiz[scoring_policy]": "keep_highest",
            "quiz[hide_results]": "always",
            "quiz[allowed_attempts]": "1",
            "quiz[shuffle_answers]": "false",
        },
    )
    quiz_id = quiz["id"]
    for position, (_key, qtype, text) in enumerate(FEEDBACK_QUESTIONS, start=1):
        payload: dict[str, str] = {
            "question[question_name]": text,
            "question[question_text]": f"<p>{text}</p>",
            "question[points_possible]": "0",
            "question[position]": str(position),
        }
        if qtype == "essay":
            payload["question[question_type]"] = "essay_question"
        else:
            payload["question[question_type]"] = "multiple_choice_question"
            for i, label in enumerate(FEEDBACK_SCALE):
                payload[f"question[answers][{i}][answer_text]"] = label
                payload[f"question[answers][{i}][answer_weight]"] = "0"
        canvas_post(f"courses/{course_id}/quizzes/{quiz_id}/questions", payload)
    return quiz


def add_feedback_quiz_item(
    course_id: int,
    module_id: int,
    *,
    position: int | None = None,
    quiz_id: int | None = None,
) -> dict:
    if quiz_id:
        canvas_put(
            f"courses/{course_id}/quizzes/{quiz_id}",
            {
                "quiz[title]": FEEDBACK_ITEM_TITLE,
                "quiz[published]": "false",
            },
        )
        quiz = {"id": quiz_id}
    else:
        quiz = create_feedback_quiz(course_id)
    payload = {
        "module_item[title]": FEEDBACK_ITEM_TITLE,
        "module_item[type]": "Quiz",
        "module_item[content_id]": str(quiz["id"]),
        "module_item[indent]": "1",
        "module_item[published]": "false",
    }
    if position is not None:
        payload["module_item[position]"] = str(position)
    item = add_module_item(course_id, module_id, payload)
    canvas_put(
        f"courses/{course_id}/modules/{module_id}/items/{item['id']}",
        {"module_item[published]": "false"},
    )
    return {
        "quiz_id": quiz["id"],
        "id": item.get("id"),
        "type": item.get("type"),
        "title": item.get("title"),
        "published": False,
    }


def publish_pair(
    course_id: int,
    module_id: int,
    preset: PairPreset,
    *,
    lesson_nb_url: str,
    homework_nb_url: str,
    solutions_nb_url: str | None = None,
    page_url: str | None = None,
    items_only: bool = False,
) -> dict:
    page: dict | None = None
    resolved_page_url = page_url or preset.page_url
    if not items_only:
        page = upsert_lesson_page(
            course_id,
            title=preset.page_title,
            markdown_path=preset.lesson_md,
            page_url=resolved_page_url,
            lesson_colab_url=lesson_nb_url,
            homework_colab_url=homework_nb_url,
        )
        resolved_page_url = page.get("url", resolved_page_url)

    if items_only:
        return {
            "course_id": course_id,
            "module_id": module_id,
            "pair": preset.lesson_dir,
            "page": {"url": resolved_page_url, "updated": True},
            "items": [],
        }

    payloads = [
        {
            "module_item[title]": preset.subheader,
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
    ]
    if solutions_nb_url:
        payloads.append(
            {
                "module_item[title]": SOLUTIONS_ITEM_TITLE,
                "module_item[type]": "ExternalUrl",
                "module_item[external_url]": solutions_nb_url,
                "module_item[indent]": "1",
                "module_item[published]": "false",
                "module_item[new_tab]": "true",
            }
        )
    payloads.extend(
        [
            {
                "module_item[title]": LESSON_ITEM_TITLE,
                "module_item[type]": "ExternalUrl",
                "module_item[external_url]": lesson_nb_url,
                "module_item[indent]": "1",
                "module_item[published]": "true",
                "module_item[new_tab]": "true",
            },
        ]
    )

    items = []
    for payload in payloads:
        item = add_module_item(course_id, module_id, payload)
        if payload.get("module_item[title]") == LESSON_ITEM_TITLE:
            item = canvas_put(
                f"courses/{course_id}/modules/{module_id}/items/{item['id']}",
                {"module_item[published]": "true"},
            )
        items.append(item)

    homework_item = None
    if not preset.skip_homework:
        pair_num = pair_number_from_subheader(preset.subheader)
        if pair_num is None:
            raise SystemExit(f"Cannot parse pair number from subheader: {preset.subheader!r}")
        homework_item = add_homework_assignment_item(
            course_id,
            module_id,
            pair=pair_num,
            homework_colab_url=homework_nb_url,
        )
    feedback_item = add_feedback_quiz_item(course_id, module_id)

    return {
        "course_id": course_id,
        "module_id": module_id,
        "pair": preset.lesson_dir,
        "page": {"page_id": (page or {}).get("page_id"), "url": resolved_page_url},
        "items": [
            {"id": item.get("id"), "type": item.get("type"), "title": item.get("title")}
            for item in items
        ],
        "homework_item": homework_item,
        "feedback_item": feedback_item,
    }


def artifact_materials_page_url(pair: int) -> str:
    return f"para-{pair}-artifact-materialy"


def upsert_wiki_md_page(
    course_id: int,
    *,
    slug: str,
    markdown_text: str,
    published: bool = True,
) -> dict:
    """Publish MD as Canvas wiki. Title must equal slug (Canvas transliterates titles)."""
    body = lesson_md_to_canvas_html(markdown_text, course_id=course_id)
    payload = {
        "wiki_page[title]": slug,
        "wiki_page[body]": body,
        "wiki_page[published]": "true" if published else "false",
        "wiki_page[editing_role]": "teachers",
    }
    page = canvas_put(f"courses/{course_id}/pages/{slug}", payload)
    if page.get("url") != slug:
        raise SystemExit(
            f"Canvas changed page url to {page.get('url')!r} (wanted {slug!r})"
        )
    return page


def prepare_artifact_project_md() -> str:
    """Student-facing assignment: one coherent brief from artifact/ASSIGNMENT.md."""
    assignment = (ARTIFACT_ROOT / "ASSIGNMENT.md").read_text(encoding="utf-8")
    return assignment.strip() + "\n"


def prepare_artifact_starter_readme_md() -> str:
    """Thin pointer page — full brief is in Задание."""
    return """# Как делать: `text_stats`

Весь текст задания, шаги, критерии и шаблон README — в одном документе:

**[Задание: text_stats](canvas:artifact-project)**

Стартовые файлы: [Стартовый код (zip)](canvas:artifact-starter-code).
"""


def prepare_artifact_starter_code_md(*, download_href: str) -> str:
    """Short student page: download zip (no code dump)."""
    return f"""# Стартовый код `text_stats`

Скачайте один архив и распакуйте:

**[{ARTIFACT_ZIP_NAME}]({download_href})**

Внутри папка `text_stats_starter/`:

```text
text_stats_starter/
  text_stats.py          ← пишете код сюда
  manual_tests.py        ← проверка
  data/
    __init__.py
    module_datasets.py   ← отзывы TEXTS_POSITIVE / TEXTS_NEGATIVE (+ датасеты модуля)
```

Дальше откройте **[Задание: text_stats](canvas:artifact-project)** — там полный связный текст: зачем задание, шаги 1–8, контракты функций, критерии и шаблон README.

Запуск тестов из папки `text_stats_starter/`:

```bash
python manual_tests.py
```

Успех: `All 10 manual tests passed.`
"""


def prepare_artifact_teacher_solutions_md(*, teacher_zip_href: str) -> str:
    """Hidden teacher page: solutions brief + download link."""
    body = (ARTIFACT_ROOT / "TEACHER_SOLUTIONS.md").read_text(encoding="utf-8")
    # Ensure zip link points to uploaded file page / direct download
    body = body.replace(
        "[text_stats_teacher_solutions.zip](canvas:artifact-teacher-code)",
        f"[{ARTIFACT_TEACHER_ZIP_NAME}]({teacher_zip_href})",
    )
    return body.strip() + "\n"


def prepare_artifact_teacher_code_md(*, download_href: str) -> str:
    return f"""# Эталон и данные (для преподавателя)

**[{ARTIFACT_TEACHER_ZIP_NAME}]({download_href})**

Скрыто от учеников. Разбор — [Решения для учителя](canvas:artifact-teacher-solutions).
"""


def build_artifact_starter_zip() -> Path:
    """Build a standalone student zip (full module data/ next to tests)."""
    import io
    import zipfile

    text_stats = (ARTIFACT_ROOT / "starter" / "text_stats.py").read_text(encoding="utf-8")
    text_stats = text_stats.replace(
        "Реализовать функции по artifact/PROJECT.md. Тесты: manual_tests.py",
        "Реализовать функции по заданию в Canvas. Тесты: manual_tests.py",
    )
    tests = (ARTIFACT_ROOT / "starter" / "manual_tests.py").read_text(encoding="utf-8")
    # Standalone zip: only local data/, no repo parents on sys.path.
    tests = tests.replace(
        "_MODULE_ROOT = Path(__file__).resolve().parents[2]\n"
        "sys.path.insert(0, str(_MODULE_ROOT))\n\n",
        "",
    )
    datasets = (
        ROOT / "modules/08_01_functions_recursion/data/module_datasets.py"
    ).read_text(encoding="utf-8")
    out = ARTIFACT_ROOT / ARTIFACT_ZIP_NAME
    root_name = "text_stats_starter"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{root_name}/text_stats.py", text_stats)
        zf.writestr(f"{root_name}/manual_tests.py", tests)
        zf.writestr(f"{root_name}/data/__init__.py", "")
        zf.writestr(f"{root_name}/data/module_datasets.py", datasets)
        assignment = (ARTIFACT_ROOT / "ASSIGNMENT.md").read_text(encoding="utf-8")
        # In zip, canvas: links are useless — point to filenames.
        assignment = assignment.replace(
            "[Стартовый код (zip)](canvas:artifact-starter-code)",
            "архив стартового кода (эта же папка)",
        )
        zf.writestr(f"{root_name}/ASSIGNMENT.md", assignment)
    out.write_bytes(buf.getvalue())
    return out


def build_artifact_teacher_zip() -> Path:
    """Teacher zip: solution code + tests + full module datasets + briefs."""
    import io
    import zipfile

    datasets = (
        ROOT / "modules/08_01_functions_recursion/data/module_datasets.py"
    ).read_text(encoding="utf-8")
    solution_py = (ARTIFACT_ROOT / "solution" / "text_stats.py").read_text(encoding="utf-8")
    tests = (ARTIFACT_ROOT / "solution" / "manual_tests.py").read_text(encoding="utf-8")
    tests = tests.replace(
        "_MODULE_ROOT = Path(__file__).resolve().parents[2]\n"
        "sys.path.insert(0, str(_MODULE_ROOT))\n\n",
        "",
    )
    teacher_readme = (ARTIFACT_ROOT / "TEACHER_SOLUTIONS.md").read_text(encoding="utf-8")
    teacher_readme = teacher_readme.replace(
        "[text_stats_teacher_solutions.zip](canvas:artifact-teacher-code)",
        "этот архив",
    ).replace(
        "[Задание: text_stats](canvas:artifact-project)",
        "ASSIGNMENT.md в ученическом архиве / wiki «Задание: text_stats»",
    )
    out = ARTIFACT_ROOT / ARTIFACT_TEACHER_ZIP_NAME
    root_name = "text_stats_teacher"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{root_name}/text_stats.py", solution_py)
        zf.writestr(f"{root_name}/manual_tests.py", tests)
        zf.writestr(f"{root_name}/README.md", teacher_readme)
        zf.writestr(
            f"{root_name}/ASSIGNMENT.md",
            (ARTIFACT_ROOT / "ASSIGNMENT.md").read_text(encoding="utf-8"),
        )
        zf.writestr(f"{root_name}/data/__init__.py", "")
        zf.writestr(f"{root_name}/data/module_datasets.py", datasets)
    out.write_bytes(buf.getvalue())
    return out


def canvas_file_download_href(course_id: int, file_id: int) -> str:
    return f"/courses/{course_id}/files/{file_id}/download?download_frd=1"


def _upload_named_course_zip(
    course_id: int,
    zip_path: Path,
    display_name: str,
    *,
    hidden: bool = False,
) -> dict:
    existing = canvas_get(
        f"courses/{course_id}/files",
        {"search_term": display_name},
        paginate=True,
    )
    matches = []
    if isinstance(existing, list):
        matches = [
            f
            for f in existing
            if (f.get("display_name") or f.get("filename")) == display_name
        ]
    uploaded = canvas_upload_course_file(
        course_id,
        zip_path,
        parent_folder_path="/artifact",
        content_type="application/zip",
    )
    file_id = int(uploaded["id"])
    canvas_put(
        f"files/{file_id}",
        {
            "published": "true",
            "hidden": "true" if hidden else "false",
            "locked": "false",
        },
    )
    for old in matches:
        oid = int(old["id"])
        if oid != file_id:
            try:
                canvas_delete(f"files/{oid}")
            except SystemExit:
                pass
    return {
        "id": file_id,
        "display_name": uploaded.get("display_name") or display_name,
        "url": uploaded.get("url"),
        "download_href": canvas_file_download_href(course_id, file_id),
        "local_path": str(zip_path),
        "hidden": hidden,
    }


def upload_artifact_starter_zip(course_id: int) -> dict:
    return _upload_named_course_zip(
        course_id, build_artifact_starter_zip(), ARTIFACT_ZIP_NAME
    )


def upload_artifact_teacher_zip(course_id: int) -> dict:
    # Hidden in Files browser; module item stays unpublished for students.
    return _upload_named_course_zip(
        course_id,
        build_artifact_teacher_zip(),
        ARTIFACT_TEACHER_ZIP_NAME,
        hidden=True,
    )


def artifact_hub_md(pair: int, *, download_href: str) -> str:
    del pair  # one brief for the whole artifact block
    return f"""# Материалы артефакта: `text_stats`

Итоговая работа модуля 1. Откройте **один** документ задания и скачайте стартовый код.

| Что открыть | Зачем |
|---|---|
| [Задание: text_stats](canvas:artifact-project) | полный текст: смысл, шаги, функции, критерии, README |
| [{ARTIFACT_ZIP_NAME}]({download_href}) | стартовые файлы и данные одним архивом |

Сдача — через Assignment **«Сдача артефакта text_stats»**.
"""


def upsert_artifact_docs(course_id: int) -> dict:
    """Publish student + teacher artifact docs and both zips to Canvas."""
    zip_info = upload_artifact_starter_zip(course_id)
    teacher_zip = upload_artifact_teacher_zip(course_id)
    download_href = zip_info["download_href"]
    teacher_href = teacher_zip["download_href"]
    pages = {
        ARTIFACT_PROJECT_SLUG: upsert_wiki_md_page(
            course_id, slug=ARTIFACT_PROJECT_SLUG, markdown_text=prepare_artifact_project_md()
        ),
        ARTIFACT_STARTER_README_SLUG: upsert_wiki_md_page(
            course_id,
            slug=ARTIFACT_STARTER_README_SLUG,
            markdown_text=prepare_artifact_starter_readme_md(),
        ),
        ARTIFACT_STARTER_CODE_SLUG: upsert_wiki_md_page(
            course_id,
            slug=ARTIFACT_STARTER_CODE_SLUG,
            markdown_text=prepare_artifact_starter_code_md(download_href=download_href),
        ),
        ARTIFACT_TEACHER_SLUG: upsert_wiki_md_page(
            course_id,
            slug=ARTIFACT_TEACHER_SLUG,
            markdown_text=prepare_artifact_teacher_solutions_md(
                teacher_zip_href=teacher_href
            ),
        ),
        ARTIFACT_TEACHER_CODE_SLUG: upsert_wiki_md_page(
            course_id,
            slug=ARTIFACT_TEACHER_CODE_SLUG,
            markdown_text=prepare_artifact_teacher_code_md(download_href=teacher_href),
        ),
    }
    return {
        "zip": zip_info,
        "teacher_zip": teacher_zip,
        "pages": {
            slug: {"page_id": p.get("page_id"), "url": p.get("url")}
            for slug, p in pages.items()
        },
        "download_href": download_href,
        "teacher_download_href": teacher_href,
    }


def upsert_artifact_student_page(
    course_id: int, pair: int, *, download_href: str
) -> dict:
    return upsert_wiki_md_page(
        course_id,
        slug=artifact_materials_page_url(pair),
        markdown_text=artifact_hub_md(pair, download_href=download_href),
    )


def artifact_submit_assignment_description(course_id: int = 6465) -> str:
    project_href = f"/courses/{course_id}/pages/{ARTIFACT_PROJECT_SLUG}"
    code_href = f"/courses/{course_id}/pages/{ARTIFACT_STARTER_CODE_SLUG}"
    steps_href = f"/courses/{course_id}/pages/{ARTIFACT_STARTER_README_SLUG}"
    return (
        "<p><strong>Сдача артефакта</strong> <code>text_stats</code>.</p>"
        f'<p><a href="{project_href}">Задание</a> · '
        f'<a href="{steps_href}">Шаги</a> · '
        f'<a href="{code_href}">Стартовый код (zip)</a></p>'
        "<p>Загрузите:</p><ul>"
        "<li><code>text_stats.py</code></li>"
        "<li><code>README.md</code> (5 своих фраз, pipeline, tie-break)</li>"
        "</ul>"
        "<p>Перед сдачей: <code>python manual_tests.py</code> → "
        "<code>All 10 manual tests passed.</code></p>"
    )


def create_artifact_submit_assignment(course_id: int, *, points: float = 10.0) -> dict:
    payload = {
        "assignment[name]": ARTIFACT_SUBMIT_TITLE,
        "assignment[description]": artifact_submit_assignment_description(course_id),
        "assignment[submission_types][]": "online_upload",
        "assignment[allowed_extensions][]": "py",
        "assignment[allowed_extensions][]": "md",
        "assignment[allowed_extensions][]": "zip",
        "assignment[published]": "true",
        "assignment[points_possible]": str(points),
        "assignment[grading_type]": "points",
    }
    return canvas_post(f"courses/{course_id}/assignments", payload)


def update_artifact_submit_assignment(course_id: int, assignment_id: int) -> dict:
    return canvas_put(
        f"courses/{course_id}/assignments/{assignment_id}",
        {
            "assignment[description]": artifact_submit_assignment_description(course_id),
            "assignment[published]": "true",
        },
    )


def add_artifact_submit_item(
    course_id: int,
    module_id: int,
    *,
    position: int | None = None,
    assignment_id: int | None = None,
) -> dict:
    assignment = (
        {"id": assignment_id}
        if assignment_id
        else create_artifact_submit_assignment(course_id)
    )
    payload = {
        "module_item[title]": ARTIFACT_SUBMIT_TITLE,
        "module_item[type]": "Assignment",
        "module_item[content_id]": str(assignment["id"]),
        "module_item[indent]": "1",
        "module_item[published]": "true",
    }
    if position is not None:
        payload["module_item[position]"] = str(position)
    item = add_module_item(course_id, module_id, payload)
    return {
        "assignment_id": assignment["id"],
        "id": item.get("id"),
        "type": item.get("type"),
        "title": item.get("title"),
        "published": item.get("published"),
    }


def add_artifact_materials_item(
    course_id: int,
    module_id: int,
    *,
    page_url: str,
    position: int | None = None,
    title: str = ARTIFACT_MATERIALS_TITLE,
) -> dict:
    payload = {
        "module_item[title]": title,
        "module_item[type]": "Page",
        "module_item[page_url]": page_url,
        "module_item[indent]": "1",
        "module_item[published]": "true",
    }
    if position is not None:
        payload["module_item[position]"] = str(position)
    item = add_module_item(course_id, module_id, payload)
    return {
        "id": item.get("id"),
        "type": item.get("type"),
        "title": item.get("title"),
        "page_url": page_url,
        "published": item.get("published"),
    }


def _pair_block_bounds(items: list[dict], plan_page_url: str) -> tuple[int, int]:
    """Positions (inclusive start after plan, exclusive end at next SubHeader)."""
    plan_item = next(
        (item for item in items if item.get("page_url") == plan_page_url),
        None,
    )
    if plan_item is None:
        raise SystemExit(f"Plan page not found: {plan_page_url}")
    start = int(plan_item["position"]) + 1
    end = max(int(i["position"]) for i in items) + 1
    for item in items:
        pos = int(item["position"])
        if pos >= start and item.get("type") == "SubHeader":
            end = pos
            break
    return start, end


def add_artifact_extras(
    course_id: int,
    module_id: int,
    pair: int,
    preset: PairPreset,
) -> dict:
    docs = upsert_artifact_docs(course_id)
    download_href = docs["download_href"]
    zip_file_id = int(docs["zip"]["id"])
    page = upsert_artifact_student_page(
        course_id, pair, download_href=download_href
    )
    page_url = artifact_materials_page_url(pair)
    items = canvas_get(f"courses/{course_id}/modules/{module_id}/items", paginate=True)
    start, end = _pair_block_bounds(items, preset.page_url)
    position = start

    materials_in_block = [
        item
        for item in items
        if start <= int(item["position"]) < end
        and item.get("type") == "Page"
        and (
            item.get("title") == ARTIFACT_MATERIALS_TITLE
            or str(item.get("page_url") or "").endswith("artifact-materialy")
        )
    ]
    keep = next(
        (item for item in materials_in_block if item.get("page_url") == page_url),
        None,
    )
    removed: list[int] = []
    for item in materials_in_block:
        if keep is not None and item["id"] == keep["id"]:
            continue
        if keep is None and item is materials_in_block[0]:
            keep = item
            canvas_put(
                f"courses/{course_id}/modules/{module_id}/items/{item['id']}",
                {
                    "module_item[page_url]": page_url,
                    "module_item[title]": ARTIFACT_MATERIALS_TITLE,
                    "module_item[published]": "true",
                    "module_item[position]": str(position),
                },
            )
            continue
        canvas_delete(
            f"courses/{course_id}/modules/{module_id}/items/{item['id']}"
        )
        removed.append(int(item["id"]))

    if keep is None:
        materials_item = add_artifact_materials_item(
            course_id, module_id, page_url=page_url, position=position
        )
    else:
        materials_item = {
            "id": keep.get("id"),
            "page_url": page_url,
            "skipped": True,
            "removed_duplicates": removed,
        }

    # Under the main artifact pair surface shared docs as module items (once).
    doc_items: list[dict] = []
    if pair in (8, 9):
        doc_specs = [
            (ARTIFACT_PROJECT_ITEM_TITLE, ARTIFACT_PROJECT_SLUG, position + 1),
            (ARTIFACT_STARTER_README_ITEM_TITLE, ARTIFACT_STARTER_README_SLUG, position + 2),
        ]
        items = canvas_get(f"courses/{course_id}/modules/{module_id}/items", paginate=True)
        for title, slug, pos in doc_specs:
            existing = next(
                (
                    it
                    for it in items
                    if it.get("page_url") == slug or it.get("title") == title
                ),
                None,
            )
            if existing:
                canvas_put(
                    f"courses/{course_id}/modules/{module_id}/items/{existing['id']}",
                    {
                        "module_item[page_url]": slug,
                        "module_item[title]": title,
                        "module_item[published]": "true",
                        "module_item[position]": str(pos),
                    },
                )
                doc_items.append({"id": existing["id"], "page_url": slug, "skipped": True})
            else:
                doc_items.append(
                    add_artifact_materials_item(
                        course_id,
                        module_id,
                        page_url=slug,
                        position=pos,
                        title=title,
                    )
                )
        # Zip as File module item (not a Page with code dump)
        zip_pos = position + 3
        items = canvas_get(f"courses/{course_id}/modules/{module_id}/items", paginate=True)
        existing_zip = next(
            (
                it
                for it in items
                if it.get("title") == ARTIFACT_STARTER_CODE_ITEM_TITLE
                or (
                    it.get("type") == "File"
                    and it.get("content_id") == zip_file_id
                )
                or it.get("page_url") == ARTIFACT_STARTER_CODE_SLUG
            ),
            None,
        )
        if existing_zip and existing_zip.get("type") == "Page":
            canvas_delete(
                f"courses/{course_id}/modules/{module_id}/items/{existing_zip['id']}"
            )
            existing_zip = None
        if existing_zip and existing_zip.get("type") == "File":
            canvas_put(
                f"courses/{course_id}/modules/{module_id}/items/{existing_zip['id']}",
                {
                    "module_item[content_id]": str(zip_file_id),
                    "module_item[title]": ARTIFACT_STARTER_CODE_ITEM_TITLE,
                    "module_item[published]": "true",
                    "module_item[position]": str(zip_pos),
                },
            )
            doc_items.append(
                {
                    "id": existing_zip["id"],
                    "type": "File",
                    "content_id": zip_file_id,
                    "skipped": True,
                }
            )
        else:
            zip_item = add_module_item(
                course_id,
                module_id,
                {
                    "module_item[title]": ARTIFACT_STARTER_CODE_ITEM_TITLE,
                    "module_item[type]": "File",
                    "module_item[content_id]": str(zip_file_id),
                    "module_item[indent]": "1",
                    "module_item[published]": "true",
                    "module_item[position]": str(zip_pos),
                },
            )
            doc_items.append(
                {
                    "id": zip_item.get("id"),
                    "type": "File",
                    "content_id": zip_file_id,
                    "title": ARTIFACT_STARTER_CODE_ITEM_TITLE,
                }
            )

        # Teacher solutions: unpublished wiki (File module items cannot be unpublished on this Canvas).
        # Zip stays hidden under Files; download link is inside the teacher wiki page.
        teacher_specs = [
            (ARTIFACT_TEACHER_ITEM_TITLE, ARTIFACT_TEACHER_SLUG, "Page", None),
        ]
        # Drop any leftover teacher File module item from earlier publishes.
        items = canvas_get(f"courses/{course_id}/modules/{module_id}/items", paginate=True)
        for it in items:
            title = it.get("title") or ""
            if (
                it.get("type") == "File"
                and ARTIFACT_TEACHER_ITEM_TITLE in title
                and "(zip)" in title
            ):
                canvas_delete(
                    f"courses/{course_id}/modules/{module_id}/items/{it['id']}"
                )
        items = canvas_get(f"courses/{course_id}/modules/{module_id}/items", paginate=True)
        teacher_pos = position + 4
        for title, slug, itype, content_id in teacher_specs:
            existing = next(
                (
                    it
                    for it in items
                    if it.get("title") == title
                    or (slug and it.get("page_url") == slug)
                    or (
                        itype == "File"
                        and it.get("type") == "File"
                        and it.get("content_id") == content_id
                    )
                ),
                None,
            )
            if existing and itype == "File" and existing.get("type") == "Page":
                canvas_delete(
                    f"courses/{course_id}/modules/{module_id}/items/{existing['id']}"
                )
                existing = None
            if existing:
                payload = {
                    "module_item[title]": title,
                    "module_item[published]": "false",
                    "module_item[position]": str(teacher_pos),
                    "module_item[indent]": "1",
                }
                if itype == "Page" and slug:
                    payload["module_item[page_url]"] = slug
                if itype == "File" and content_id is not None:
                    payload["module_item[content_id]"] = str(content_id)
                canvas_put(
                    f"courses/{course_id}/modules/{module_id}/items/{existing['id']}",
                    payload,
                )
                doc_items.append(
                    {
                        "id": existing["id"],
                        "title": title,
                        "type": itype,
                        "published": False,
                        "skipped": True,
                    }
                )
            else:
                payload = {
                    "module_item[title]": title,
                    "module_item[type]": itype,
                    "module_item[indent]": "1",
                    "module_item[published]": "false",
                    "module_item[position]": str(teacher_pos),
                }
                if itype == "Page" and slug:
                    payload["module_item[page_url]"] = slug
                if itype == "File" and content_id is not None:
                    payload["module_item[content_id]"] = str(content_id)
                item = add_module_item(course_id, module_id, payload)
                doc_items.append(
                    {
                        "id": item.get("id"),
                        "title": title,
                        "type": itype,
                        "published": False,
                    }
                )
            teacher_pos += 1

    submit_item = None
    if pair in (8, 10):
        items = canvas_get(
            f"courses/{course_id}/modules/{module_id}/items", paginate=True
        )
        existing_submit = next(
            (item for item in items if item.get("title") == ARTIFACT_SUBMIT_TITLE),
            None,
        )
        if existing_submit:
            aid = existing_submit.get("content_id")
            if aid:
                update_artifact_submit_assignment(course_id, int(aid))
            submit_item = {"skipped": True, "id": existing_submit.get("id"), "assignment_id": aid}
        else:
            submit_item = add_artifact_submit_item(
                course_id, module_id, position=position + 1
            )
    return {
        "pair": pair,
        "docs": docs,
        "page": {"page_id": page.get("page_id"), "url": page_url},
        "materials_item": materials_item,
        "doc_items": doc_items,
        "submit_item": submit_item,
    }


def publish_artifact_pair(
    course_id: int,
    module_id: int,
    pair: int,
    preset: PairPreset,
    *,
    page_url: str | None = None,
    items_only: bool = False,
) -> dict:
    """Артефактные пары: скрытый план + опубликованные материалы starter."""
    base = publish_orientation_pair(
        course_id,
        module_id,
        preset,
        page_url=page_url,
        items_only=items_only,
    )
    if items_only:
        return base
    extras = add_artifact_extras(course_id, module_id, pair, preset)
    return {**base, **extras, "artifact": True}


def publish_orientation_pair(
    course_id: int,
    module_id: int,
    preset: PairPreset,
    *,
    page_url: str | None = None,
    items_only: bool = False,
) -> dict:
    """Вводная пара: только план (wiki, скрыт); без Colab и без ДЗ."""
    resolved_page_url = page_url or preset.page_url
    page: dict | None = None
    if not items_only:
        page = upsert_lesson_page(
            course_id,
            title=preset.page_title,
            markdown_path=preset.lesson_md,
            page_url=resolved_page_url,
            lesson_colab_url="",
            homework_colab_url="",
        )
        resolved_page_url = page.get("url", resolved_page_url)

    if items_only:
        return {
            "course_id": course_id,
            "module_id": module_id,
            "pair": preset.lesson_dir,
            "page": {"url": resolved_page_url, "updated": True},
            "items": [],
        }

    base_pos = preset.insert_at_position
    payloads = [
        {
            "module_item[title]": preset.subheader,
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
    ]
    items = []
    for offset, payload in enumerate(payloads):
        if base_pos is not None:
            payload = {**payload, "module_item[position]": str(base_pos + offset)}
        items.append(add_module_item(course_id, module_id, payload))
    feedback_item = add_feedback_quiz_item(course_id, module_id)

    return {
        "course_id": course_id,
        "module_id": module_id,
        "pair": preset.lesson_dir,
        "orientation": True,
        "page": {"page_id": (page or {}).get("page_id"), "url": resolved_page_url},
        "items": [
            {"id": item.get("id"), "type": item.get("type"), "title": item.get("title")}
            for item in items
        ],
        "feedback_item": feedback_item,
    }


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
    """Backward-compatible wrapper."""
    preset = PAIR_PRESETS[2]
    return publish_pair(
        course_id,
        module_id,
        preset,
        lesson_nb_url=lesson_nb_url,
        homework_nb_url=homework_nb_url,
        solutions_nb_url=preset.colab(preset.solutions_gist, "solutions.ipynb")
        if preset.solutions_gist
        else None,
        page_url=page_url,
        items_only=items_only,
    )


def migrate_homework_to_assignment(
    course_id: int,
    module_id: int,
    *,
    pair: int,
    homework_colab_url: str,
    remove_external_url_item_id: int,
    assignment_id: int,
    assignment_module_item_id: int,
    lesson_module_item_id: int,
) -> dict:
    title = homework_title(pair)
    assignment = update_homework_assignment(
        course_id,
        assignment_id,
        pair=pair,
        homework_colab_url=homework_colab_url,
    )
    canvas_delete(
        f"courses/{course_id}/modules/{module_id}/items/{remove_external_url_item_id}"
    )
    canvas_put(
        f"courses/{course_id}/modules/{module_id}/items/{lesson_module_item_id}",
        {"module_item[position]": "4"},
    )
    module_item = canvas_put(
        f"courses/{course_id}/modules/{module_id}/items/{assignment_module_item_id}",
        {
            "module_item[title]": title,
            "module_item[position]": "5",
        },
    )
    return {
        "assignment": {"id": assignment.get("id"), "name": assignment.get("name")},
        "homework_item": {
            "id": module_item.get("id"),
            "title": module_item.get("title"),
            "position": module_item.get("position"),
        },
        "removed_external_url_item_id": remove_external_url_item_id,
    }


def resolve_urls(
    preset: PairPreset,
    lesson_nb_url: str | None,
    homework_nb_url: str | None,
    solutions_nb_url: str | None,
) -> tuple[str, str, str | None]:
    lesson = lesson_nb_url or (
        preset.colab(preset.lesson_gist, "lesson.ipynb") if preset.lesson_gist else None
    )
    homework = homework_nb_url or (
        preset.colab(preset.homework_gist, "homework.ipynb") if preset.homework_gist else None
    )
    solutions = solutions_nb_url or (
        preset.colab(preset.solutions_gist, "solutions.ipynb") if preset.solutions_gist else None
    )
    if not lesson:
        raise SystemExit(
            f"Pair {preset.lesson_dir}: provide --lesson-nb-url "
            "(or set gist ids in PAIR_PRESETS)"
        )
    if not homework and not preset.skip_homework:
        raise SystemExit(
            f"Pair {preset.lesson_dir}: provide --homework-nb-url and --solutions-nb-url "
            "(or set gist ids in PAIR_PRESETS)"
        )
    return lesson, homework or "", solutions


def run_canvas_controller_after_publish(args: argparse.Namespace) -> None:
    if args.skip_audit:
        return
    from canvas_controller import run_post_publish_audit

    if not run_post_publish_audit(args.course_id):
        raise SystemExit("Canvas controller: errors after publish (see above)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish a lesson pair to Canvas")
    parser.add_argument("--pair", type=int, default=2, help="KTP pair number (1–10)")
    parser.add_argument("--course-id", type=int, default=6465)
    parser.add_argument("--module-id", type=int, default=54688)
    parser.add_argument("--lesson-md", type=Path, default=None)
    parser.add_argument("--lesson-nb-url", default=None)
    parser.add_argument("--homework-nb-url", default=None)
    parser.add_argument("--solutions-nb-url", default=None)
    parser.add_argument("--subheader", default=None)
    parser.add_argument("--page-title", default=None)
    parser.add_argument("--page-url", default=None)
    parser.add_argument("--update-page-only", action="store_true")
    parser.add_argument("--add-solutions-item", action="store_true")
    parser.add_argument("--add-homework-assignment", action="store_true")
    parser.add_argument("--add-artifact-extras", action="store_true")
    parser.add_argument(
        "--migrate-homework-layout",
        action="store_true",
        help="Pair 2 one-off migration",
    )
    parser.add_argument("--solutions-position", type=int, default=3)
    parser.add_argument("--submit-position", type=int, default=None)
    parser.add_argument(
        "--skip-audit",
        action="store_true",
        help="Do not run canvas_controller after publish",
    )
    args = parser.parse_args()
    require_canvas_auth()
    try:
        _main_publish(args)
    finally:
        run_canvas_controller_after_publish(args)


def _main_publish(args: argparse.Namespace) -> None:
    if args.migrate_homework_layout:
        homework = args.homework_nb_url or PAIR_PRESETS[2].colab(
            PAIR_PRESETS[2].homework_gist, "homework.ipynb"
        )
        result = migrate_homework_to_assignment(
            args.course_id,
            args.module_id,
            pair=2,
            homework_colab_url=homework,
            remove_external_url_item_id=486002,
            assignment_id=198690,
            assignment_module_item_id=486005,
            lesson_module_item_id=486001,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    base = PAIR_PRESETS.get(args.pair)
    if base is None and not args.subheader:
        raise SystemExit(f"No preset for pair {args.pair}; pass --subheader and paths")

    if base:
        preset = PairPreset(
            subheader=args.subheader or base.subheader,
            page_title=args.page_title or base.page_title,
            page_url=args.page_url or base.page_url,
            lesson_dir=base.lesson_dir,
            lesson_gist=base.lesson_gist,
            homework_gist=base.homework_gist,
            solutions_gist=base.solutions_gist,
            orientation=base.orientation,
            artifact=base.artifact,
            insert_at_position=base.insert_at_position,
            skip_homework=base.skip_homework,
        )
    else:
        lesson_md = args.lesson_md
        if not lesson_md or not args.subheader:
            raise SystemExit("--lesson-md and --subheader required for unknown pair")
        preset = PairPreset(
            subheader=args.subheader,
            page_title=args.page_title or args.subheader,
            page_url=args.page_url or slugify_page_url(args.pair, args.subheader),
            lesson_dir=lesson_md.parent.name,
        )

    if args.add_artifact_extras:
        if not base or not preset.artifact:
            raise SystemExit("--add-artifact-extras requires artifact pair preset (8, 9 or 10)")
        result = add_artifact_extras(args.course_id, args.module_id, args.pair, preset)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.update_page_only:
        lesson_md_path = args.lesson_md or preset.lesson_md
        lesson_url = (
            args.lesson_nb_url
            or (preset.colab(preset.lesson_gist, "lesson.ipynb") if preset.lesson_gist else "")
        )
        homework_url = (
            args.homework_nb_url
            or (preset.colab(preset.homework_gist, "homework.ipynb") if preset.homework_gist else "")
        )
        page = upsert_lesson_page(
            args.course_id,
            # Keep slug stable: wiki title = page_url (08_CANVAS §11.4).
            title=preset.page_url,
            markdown_path=lesson_md_path,
            page_url=preset.page_url,
            lesson_colab_url=lesson_url,
            homework_colab_url=homework_url,
        )
        print(
            json.dumps(
                {"page": {"url": page.get("url"), "page_id": page.get("page_id")}},
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if preset.artifact:
        result = publish_artifact_pair(
            args.course_id,
            args.module_id,
            args.pair,
            preset,
            page_url=preset.page_url if args.page_url else None,
            items_only=args.update_page_only,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if preset.orientation:
        result = publish_orientation_pair(
            args.course_id,
            args.module_id,
            preset,
            page_url=preset.page_url if args.page_url else None,
            items_only=args.update_page_only,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    lesson_md_path = args.lesson_md or preset.lesson_md
    lesson_url, homework_url, solutions_url = resolve_urls(
        preset, args.lesson_nb_url, args.homework_nb_url, args.solutions_nb_url
    )

    if args.add_homework_assignment:
        item = add_homework_assignment_item(
            args.course_id,
            args.module_id,
            pair=args.pair,
            homework_colab_url=homework_url,
            position=args.submit_position,
        )
        print(json.dumps({"homework_item": item}, ensure_ascii=False, indent=2))
        return

    if args.add_solutions_item:
        if not solutions_url:
            raise SystemExit("Error: --solutions-nb-url is required")
        item = add_solutions_item(
            args.course_id,
            args.module_id,
            solutions_url,
            position=args.solutions_position,
        )
        print(json.dumps({"solutions_item": item}, ensure_ascii=False, indent=2))
        return

    result = publish_pair(
        args.course_id,
        args.module_id,
        preset,
        lesson_nb_url=lesson_url,
        homework_nb_url=homework_url,
        solutions_nb_url=solutions_url,
        page_url=preset.page_url if args.page_url else None,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
