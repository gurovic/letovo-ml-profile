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
)
from lesson_md_html import (  # noqa: E402
    lesson_md_to_canvas_html,
    prepare_lesson_md_for_canvas_teacher,
)

PLAN_ITEM_TITLE = "План урока (для преподавателя)"
SOLUTIONS_ITEM_TITLE = "Решения (для преподавателя)"
LESSON_ITEM_TITLE = "Ноутбук урока"
HOMEWORK_ITEM_TITLE = "Домашнее задание"
ARTIFACT_MATERIALS_TITLE = "Материалы артефакта"
ARTIFACT_PROJECT_ITEM_TITLE = "Задание: text_stats"
ARTIFACT_STARTER_README_ITEM_TITLE = "Как делать (шаги)"
ARTIFACT_STARTER_CODE_ITEM_TITLE = "Стартовый код (zip)"
ARTIFACT_SUBMIT_TITLE = "Сдача артефакта text_stats"
GIST_USER = "gurovic"
ARTIFACT_ROOT = ROOT / "modules/08_01_functions_recursion/artifact"
ARTIFACT_PROJECT_SLUG = "artifact-project"
ARTIFACT_STARTER_README_SLUG = "artifact-starter-readme"
ARTIFACT_STARTER_CODE_SLUG = "artifact-starter-code"
ARTIFACT_ZIP_NAME = "text_stats_starter.zip"


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
        lesson_gist="cfc377717ba193c512a9e88593405ab8",
        homework_gist="15255de29367ddc86fb8d141f63b5cfd",
        solutions_gist="d6626c4ad9ebc6f8c1366f31d4ab39a1",
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
        subheader="Пара 5. Scope и отладка — метрика как функция",
        page_title="Пара 5 — план урока (для преподавателя)",
        page_url="para-5-plan-uroka-dlia-priepodavatielia",
        lesson_dir="05_scope_and_debugging",
        lesson_gist="02894e0df1c20220b44e6b451ba96f2d",
        homework_gist="02894e0df1c20220b44e6b451ba96f2d",
        solutions_gist="02894e0df1c20220b44e6b451ba96f2d",
    ),
    6: PairPreset(
        subheader="Пара 6. Практика: confusion_counts и журнал отладки",
        page_title="Пара 6 — план урока (для преподавателя)",
        page_url="para-6-plan-uroka-dlia-priepodavatielia",
        lesson_dir="06_practice_metrics",
        lesson_gist="223bec34de44132ae35d97bffc5f612d",
        homework_gist="223bec34de44132ae35d97bffc5f612d",
        solutions_gist="223bec34de44132ae35d97bffc5f612d",
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
        subheader="Пара 8. Практика: рекурсия, lambda, apply_pipeline",
        page_title="Пара 8 — план урока (для преподавателя)",
        page_url="para-8-plan-uroka-dlia-priepodavatielia",
        lesson_dir="08_practice_pipeline",
        lesson_gist="83ac6b1d22b4385e6ee4a424a243f7dd",
        homework_gist="83ac6b1d22b4385e6ee4a424a243f7dd",
        solutions_gist="83ac6b1d22b4385e6ee4a424a243f7dd",
    ),
    9: PairPreset(
        subheader="Пара 9. Артефакт text_stats — проектирование и реализация",
        page_title="Пара 9 — план урока (для преподавателя)",
        page_url="para-9-plan-uroka-dlia-priepodavatielia",
        lesson_dir="09_artifact_build",
        artifact=True,
    ),
    10: PairPreset(
        subheader="Пара 10. Сдача артефакта text_stats",
        page_title="Пара 10 — план урока (для преподавателя)",
        page_url="para-10-plan-uroka-dlia-priepodavatielia",
        lesson_dir="10_artifact_submit",
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
    payload = {
        "wiki_page[title]": title,
        "wiki_page[body]": body,
        "wiki_page[published]": "false",
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


def create_text_homework_assignment(course_id: int, *, points: float = 1.0) -> dict:
    payload = {
        "assignment[name]": HOMEWORK_ITEM_TITLE,
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
    position: int | None = None,
    assignment_id: int | None = None,
) -> dict:
    assignment = (
        {"id": assignment_id}
        if assignment_id
        else create_text_homework_assignment(course_id)
    )
    payload = {
        "module_item[title]": HOMEWORK_ITEM_TITLE,
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


def create_homework_assignment(course_id: int, *, homework_colab_url: str, points: float = 1.0) -> dict:
    payload = {
        "assignment[name]": HOMEWORK_ITEM_TITLE,
        "assignment[description]": homework_assignment_description(homework_colab_url),
        "assignment[submission_types][]": "online_upload",
        "assignment[allowed_extensions][]": "ipynb",
        "assignment[published]": "true",
        "assignment[points_possible]": str(points),
        "assignment[grading_type]": "points",
    }
    return canvas_post(f"courses/{course_id}/assignments", payload)


def update_homework_assignment(course_id: int, assignment_id: int, *, homework_colab_url: str) -> dict:
    payload = {
        "assignment[name]": HOMEWORK_ITEM_TITLE,
        "assignment[description]": homework_assignment_description(homework_colab_url),
    }
    return canvas_put(f"courses/{course_id}/assignments/{assignment_id}", payload)


def add_module_item(course_id: int, module_id: int, payload: dict) -> dict:
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
    homework_colab_url: str,
    position: int | None = None,
    assignment_id: int | None = None,
) -> dict:
    assignment = (
        {"id": assignment_id}
        if assignment_id
        else create_homework_assignment(course_id, homework_colab_url=homework_colab_url)
    )
    payload = {
        "module_item[title]": HOMEWORK_ITEM_TITLE,
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
        homework_item = add_homework_assignment_item(
            course_id,
            module_id,
            homework_colab_url=homework_nb_url,
        )

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
    """Student-facing assignment brief for Canvas (not the teacher PROJECT.md)."""
    return r"""# Задание: библиотека `text_stats`

Соберите небольшой модуль на Python: частоты слов в коротких отзывах и простой классификатор «позитив / негатив». **Без** `pandas` и `sklearn`.

Данные отзывов (`TEXTS_POSITIVE`, `TEXTS_NEGATIVE`) лежат в архиве [Стартовый код (zip)](canvas:artifact-starter-code).  
Порядок работы на парах — в [Как делать (шаги)](canvas:artifact-starter-readme).

---

## Что должно получиться

1. Разбить текст на слова и посчитать, как часто каждое встречается.
2. Сравнить два набора отзывов и найти «маркерные» слова класса.
3. По маркерам угадать класс нового текста.

Сдать: `text_stats.py`, свой `README.md`, строка `All 10 manual tests passed.`

---

## Обозначения

- **список** — `list`, например `["hello", "world"]`
- **словарь** — `dict`, пары «ключ → значение», например `{"a": 2, "b": 1}`
- **кортеж** — `tuple`, например `("two", 2)` (слово и его частота)
- стрелка **→** значит «функция возвращает»

Фигурные скобки `{…}` в примерах ниже — всегда **словарь**, не множество.

---

## Функции

| Функция | Вход | Выход | Смысл |
|---|---|---|---|
| `tokenize(text)` | строка | **список** строк (слова в нижнем регистре) | разрезать текст на слова |
| `word_frequencies(tokens)` | **список** слов | **словарь** «слово → сколько раз» | частоты |
| `filter_tokens(tokens, min_len=3)` | **список** слов; `min_len` — мин. длина (по умолчанию 3) | **список** слов длины ≥ `min_len` | отбросить короткие |
| `top_n(freq, n=5)` | **словарь** частот; `n` — сколько взять (по умолчанию 5) | **список кортежей** `(слово, частота)` по убыванию частоты | самые частые |
| `count_char_recursive(s, ch)` | две строки: текст `s` и один символ `ch` | целое число | сколько раз символ `ch` встречается в `s`; считать **рекурсией** (без цикла по символам) |
| `analyze_text(text)` | строка | **словарь** с тремя ключами (см. ниже) | краткая сводка по тексту |
| `apply_pipeline(data, steps)` | стартовое значение `data` и **список функций** `steps` | результат последней функции | см. раздел про pipeline |
| `aggregate_frequencies(texts)` | **список** строк | **словарь** «слово → суммарная частота» | частоты по классу отзывов |
| `compare_class_frequencies(texts_a, texts_b, ratio=2.0)` | два **списка** строк + порог `ratio` (по умолчанию 2.0) | **словарь** «слово → метка» | маркеры классов |
| `naive_classify(text, texts_a, texts_b)` | строка + два **списка** отзывов | одна строка: `"positive"`, `"negative"` или `"unknown"` | угадать класс |

`count_words(tokens)` — по желанию: на вход **список**, на выход целое. Удобно вызывать из `analyze_text`.

### `analyze_text` — какой словарь вернуть

| Ключ | Тип значения | Что положить |
|---|---|---|
| `"word_count"` | целое | сколько слов после `tokenize` |
| `"unique_words"` | целое | сколько **разных** слов |
| `"top3"` | **список** из до трёх **кортежей** `(слово, частота)` | как `top_n(..., 3)` |

Пример для `"one two two three"`:

```python
{
    "word_count": 4,
    "unique_words": 3,
    "top3": [("two", 2), ("one", 1), ("three", 1)],
}
```

В тесте обязательно: `top3[0] == ("two", 2)` (слово `two` самое частое).

### `apply_pipeline` — что с параметрами

`steps` — список **готовых функций**. Каждая вызывается **с одним аргументом**: текущим значением.

1. `result = data`
2. для каждой функции `f` из `steps`: `result = f(result)`
3. вернуть `result`

Первая функция получает исходные `data`, каждая следующая — то, что вернула предыдущая.  
Отдельные «лишние» параметры в `apply_pipeline` не передаются.

Если нужен второй параметр (как `min_len` у `filter_tokens`), зафиксируйте его в `lambda`:

```python
pipeline = [
    tokenize,
    lambda tokens: filter_tokens(tokens, 3),
    word_frequencies,
]
apply_pipeline("отличный фильм", pipeline)
```

### `compare_class_frequencies` — какой словарь вернуть

Это **словарь** (не множество): ключ — слово, значение — строка `"positive"` или `"negative"`.

Слово попадает в словарь, если его частота в одном классе **не меньше** чем в `ratio` раз больше, чем в другом (по умолчанию `ratio = 2.0`).

Пример фрагмента: `{"отличный": "positive", "скучный": "negative"}`.

### `count_char_recursive`

Пример: `count_char_recursive("banana", "a")` → `3` (три буквы «a»).  
Считать рекурсией по строке: пустая строка → `0`; иначе проверить первый символ и вызвать себя для хвоста.

---

## Пример целиком

Из папки со стартовыми файлами:

```python
from text_stats import apply_pipeline, tokenize, filter_tokens, word_frequencies, naive_classify
from data.module_datasets import TEXTS_POSITIVE, TEXTS_NEGATIVE

pipeline = [tokenize, lambda t: filter_tokens(t, 3), word_frequencies]
freq_one = apply_pipeline("отличный фильм", pipeline)

naive_classify("отличный фильм рекомендую", TEXTS_POSITIVE, TEXTS_NEGATIVE)
# ожидается: "positive"
```

---

## Критерии готовности

| # | Критерий |
|---|---|
| 1 | `python manual_tests.py` → все 10 тестов без ошибок |
| 2 | `compare_class_frequencies` на demo-данных даёт **словарь** с ≥2 маркерами (`отличный` → `"positive"`, `скучный` → `"negative"`) |
| 3 | `naive_classify` — ≥4 из 5 верных на **ваших** фразах (таблица в README) |
| 4 | у `analyze_text("one two two three")`: `word_count == 4`, `unique_words == 3`, `top3[0] == ("two", 2)` |
| 5 | `count_char_recursive("banana", "a") == 3` |
| 6 | README: ваш pipeline, правило при ничьей в `naive_classify`, короткий абзац про анализ текстов |

---

## Что зафиксировать в README

1. Как считаете суммарные частоты по списку текстов (`aggregate_frequencies`).
2. Какой `ratio` для маркеров (по умолчанию 2.0).
3. Что возвращаете при равном счёте в `naive_classify` (ожидается `"unknown"`).
4. Как `tokenize` обрабатывает пунктуацию (слова через `\w+`, Unicode).

Шаблон — в [Как делать (шаги)](canvas:artifact-starter-readme).

---

## Если тест упал

| Симптом | Что проверить |
|---|---|
| `ModuleNotFoundError: data` | запускать из папки `starter/`, где есть каталог `data/` |
| `NotImplementedError` | функция ещё не написана — нормально в начале |
| падает `compare_class_frequencies` | сначала `tokenize`, `word_frequencies`, `aggregate_frequencies` |
| `naive_classify` всегда `"unknown"` | сначала маркеры; при равном счёте — `"unknown"` |
| не сходится `analyze_text` | для `"one two two three"`: 4 слова, 3 уникальных, чаще всех `two` |
"""


def prepare_artifact_starter_readme_md() -> str:
    """Student-facing steps + README template for Canvas."""
    return r"""# Как делать: `text_stats`

Скачайте [архив стартового кода](canvas:artifact-starter-code), распакуйте папку `text_stats_starter/` и работайте в ней.

Полное задание (входы/выходы простым языком): [Задание: text_stats](canvas:artifact-project).

---

## Порядок шагов

| Шаг | Что сделать | Проверка |
|---|---|---|
| 1 | `tokenize` — строка → **список** слов | `python manual_tests.py` → OK: `test_tokenize` |
| 2 | `count_char_recursive` — сколько раз символ встречается в строке (рекурсия) | → OK: `test_count_char_recursive` |
| 3 | `word_frequencies` (**словарь**), `filter_tokens`, `top_n` (**список кортежей**) | → OK: три теста |
| 4 | `apply_pipeline` — список функций, каждая с **одним** аргументом | → OK: `test_apply_pipeline` |
| 5 | `analyze_text` — **словарь** с ключами `word_count`, `unique_words`, `top3` | → OK: `test_analyze_text` |
| 6 | `aggregate_frequencies`, `compare_class_frequencies` (**словарь** «слово → positive/negative») | → OK: `test_compare_class_frequencies` |
| 7 | `naive_classify` — одна строка-метка | → OK: оба `test_naive_classify_*` |
| 8 | ваш `README.md` | сдача |

**Пара 9:** шаги 1–5. **Пара 10:** шаги 6–8.

Подсказка для `tokenize`: в файле уже есть `import re`;  
`re.findall(r"\w+", text.lower(), flags=re.UNICODE)` (кириллица — тоже слово).

Если тест упал — таблица в [Задании](canvas:artifact-project).

---

## Запуск тестов

```bash
python manual_tests.py
```

Пока функция не готова — `NotImplementedError` на её тесте (это нормально).

Успех: `All 10 manual tests passed.`

---

## Что сдать

1. `text_stats.py`
2. `README.md` по шаблону
3. Зелёные 10 тестов

---

## Шаблон README

```markdown
# text_stats — [ФИО]

## Цепочка шагов (pipeline)

1. tokenize → …
2. …

## Решения

- Порог маркера (ratio): …
- При равном счёте маркеров в naive_classify: …

## 5 моих фраз для naive_classify

| Фраза | Ожидаю | Получилось |
|---|---|---|
| … | positive/negative | … |
(всего 5 строк; нужно ≥4 верных)

## Связь с курсом (1 абзац)

Как частоты слов связаны с анализом текстов / будущим NLP.
```
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
    module_datasets.py   ← отзывы TEXTS_POSITIVE / TEXTS_NEGATIVE
```

Дальше: [Задание](canvas:artifact-project) и [Как делать (шаги)](canvas:artifact-starter-readme).

Запуск тестов из папки `text_stats_starter/`:

```bash
python manual_tests.py
```

Успех: `All 10 manual tests passed.`
"""


def build_artifact_starter_zip() -> Path:
    """Build a standalone student zip (data/ next to tests; no repo paths)."""
    import io
    import zipfile

    text_stats = (ARTIFACT_ROOT / "starter" / "text_stats.py").read_text(encoding="utf-8")
    text_stats = text_stats.replace(
        "Реализовать функции по artifact/PROJECT.md. Тесты: manual_tests.py",
        "Реализовать функции по заданию в Canvas. Тесты: manual_tests.py",
    )
    tests = (ARTIFACT_ROOT / "starter" / "manual_tests.py").read_text(encoding="utf-8")
    tests = tests.replace(
        "sys.path.insert(0, str(Path(__file__).resolve().parent))\n"
        "sys.path.insert(0, str(Path(__file__).resolve().parents[2]))\n",
        "sys.path.insert(0, str(Path(__file__).resolve().parent))\n",
    )
    datasets = (
        '"""Мини-датасет для text_stats (без pandas)."""\n\n'
        "TEXTS_POSITIVE = [\n"
        '    "отличный фильм рекомендую",\n'
        '    "очень понравилось смотреть",\n'
        '    "лучший фильм года",\n'
        "]\n\n"
        "TEXTS_NEGATIVE = [\n"
        '    "скучный фильм не рекомендую",\n'
        '    "потерял время зря",\n'
        '    "очень слабый сценарий",\n'
        "]\n"
    )
    out = ARTIFACT_ROOT / ARTIFACT_ZIP_NAME
    root_name = "text_stats_starter"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{root_name}/text_stats.py", text_stats)
        zf.writestr(f"{root_name}/manual_tests.py", tests)
        zf.writestr(f"{root_name}/data/__init__.py", "")
        zf.writestr(f"{root_name}/data/module_datasets.py", datasets)
    out.write_bytes(buf.getvalue())
    return out


def canvas_file_download_href(course_id: int, file_id: int) -> str:
    return f"/courses/{course_id}/files/{file_id}/download?download_frd=1"


def upload_artifact_starter_zip(course_id: int) -> dict:
    zip_path = build_artifact_starter_zip()
    # Prefer overwriting one course file (avoid duplicates on pair 9 then 10).
    existing = canvas_get(
        f"courses/{course_id}/files",
        {"search_term": ARTIFACT_ZIP_NAME},
        paginate=True,
    )
    if isinstance(existing, list):
        matches = [
            f
            for f in existing
            if (f.get("display_name") or f.get("filename")) == ARTIFACT_ZIP_NAME
        ]
    else:
        matches = []
    uploaded = canvas_upload_course_file(
        course_id,
        zip_path,
        parent_folder_path="/artifact",
        content_type="application/zip",
    )
    file_id = int(uploaded["id"])
    canvas_put(
        f"files/{file_id}",
        {"published": "true", "hidden": "false", "locked": "false"},
    )
    # Remove older same-name copies left from previous publishes.
    for old in matches:
        oid = int(old["id"])
        if oid != file_id:
            try:
                canvas_delete(f"files/{oid}")
            except SystemExit:
                pass
    return {
        "id": file_id,
        "display_name": uploaded.get("display_name") or ARTIFACT_ZIP_NAME,
        "url": uploaded.get("url"),
        "download_href": canvas_file_download_href(course_id, file_id),
        "local_path": str(zip_path),
    }


def artifact_hub_md(pair: int, *, download_href: str) -> str:
    if pair == 9:
        focus = (
            "**Сейчас (пара 9):** шаги **1–5** "
            "(`tokenize` … `analyze_text`). После каждого шага — `python manual_tests.py`."
        )
    else:
        focus = (
            "**Сейчас (пара 10):** шаги **6–8** (маркеры, классификация, README). "
            "К сдаче: `All 10 manual tests passed.`"
        )
    return f"""# Материалы артефакта: `text_stats`

{focus}

| Что открыть | Зачем |
|---|---|
| [{ARTIFACT_ZIP_NAME}]({download_href}) | скачать стартовые файлы одним архивом |
| [Задание: text_stats](canvas:artifact-project) | что написать (входы/выходы функций) |
| [Как делать (шаги)](canvas:artifact-starter-readme) | порядок шагов и шаблон README |

На паре 10 сдайте через Assignment **«Сдача артефакта text_stats»**.
"""


def upsert_artifact_docs(course_id: int) -> dict:
    """Publish student artifact docs + starter zip to Canvas."""
    zip_info = upload_artifact_starter_zip(course_id)
    download_href = zip_info["download_href"]
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
    }
    return {
        "zip": zip_info,
        "pages": {
            slug: {"page_id": p.get("page_id"), "url": p.get("url")}
            for slug, p in pages.items()
        },
        "download_href": download_href,
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
        and item.get("title") == ARTIFACT_MATERIALS_TITLE
        and item.get("type") == "Page"
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

    # Under pair 9 also surface the three shared docs as module items (once).
    doc_items: list[dict] = []
    if pair == 9:
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

    submit_item = None
    if pair == 10:
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
    homework_colab_url: str,
    remove_external_url_item_id: int,
    assignment_id: int,
    assignment_module_item_id: int,
    lesson_module_item_id: int,
) -> dict:
    assignment = update_homework_assignment(
        course_id,
        assignment_id,
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
            "module_item[title]": HOMEWORK_ITEM_TITLE,
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
    args = parser.parse_args()

    if args.migrate_homework_layout:
        homework = args.homework_nb_url or PAIR_PRESETS[2].colab(
            PAIR_PRESETS[2].homework_gist, "homework.ipynb"
        )
        result = migrate_homework_to_assignment(
            args.course_id,
            args.module_id,
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
            raise SystemExit("--add-artifact-extras requires artifact pair preset (9 or 10)")
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
            title=preset.page_title,
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
