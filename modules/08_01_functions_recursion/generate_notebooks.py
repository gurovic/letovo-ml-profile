#!/usr/bin/env python3
"""Generate lesson notebooks: one pair KTP = one lesson.ipynb (pairs 2–9)."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

LESSON_02_DATA = (
    "# Площадь (м²) и фактическая цена (млн руб.) — одна квартира на один индекс\n"
    "AREAS_SQM = [28, 32, 45, 55, 60]\n"
    "PRICES_MLN = [3.9, 4.2, 5.8, 6.5, 7.1]\n"
)

DATA_IMPORT = (
    "import sys\n"
    "from pathlib import Path\n"
    "sys.path.insert(0, str(Path('../..').resolve()))\n"
    "from data.module_datasets import (\n"
    "    APARTMENTS, EXAM_SCORES, PREDICTIONS, LABELS,\n"
    "    NESTED_API_RESPONSE, CATEGORY_TREE, FEATURE_ROWS,\n"
    "    MODEL_RUNS, FEATURE_POINTS,\n"
    "    PRICE_INTERCEPT, PRICE_COEF_AREA,\n"
    ")\n"
)


def md(source: str):
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source: str):
    return {
        "cell_type": "code",
        "metadata": {},
        "source": source.splitlines(keepends=True),
        "outputs": [],
        "execution_count": None,
    }


def nb(*cells):
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": list(cells),
    }


def write(rel_path: str, notebook: dict):
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", path)


NOTEBOOKS = {
    "lessons/02_function_as_mapping/lesson.ipynb": nb(
        md("# Функция-предсказатель: от правила к выбору модели"),
        code(LESSON_02_DATA),
        md(
            "## 1. Правило без имени\n\n"
            "Формула цены спрятана внутри цикла. Превратите её в функцию, которую можно "
            "проверить отдельно и применить к любому списку площадей."
        ),
        code(
            "for area, price_fact in zip(AREAS_SQM, PRICES_MLN):\n"
            "    price = 1.5 + 0.09 * area\n"
            "    print(f\"{area} м² → {price:.2f} млн (факт: {price_fact})\")\n\n\n"
            "def predict_price(area_sqm, intercept=1.5, coef=0.09):\n"
            "    # Верните предсказанную цену.\n"
            "    pass\n\n\n"
            "assert predict_price(0) == 1.5\n"
            "assert abs(predict_price(50) - 6.0) < 1e-9"
        ),
        md(
            "## 2. Значение или печать?\n\n"
            "Напишите две версии функции: одна печатает цену, другая возвращает. "
            "Попробуйте прибавить 1 к результату каждой и объясните различие."
        ),
        code(
            "def predict_print(area_sqm):\n"
            "    # Напечатайте цену.\n"
            "    pass\n\n\n"
            "def predict_return(area_sqm):\n"
            "    # Верните цену.\n"
            "    pass\n\n\n"
            "# print(predict_print(45) + 1)\n"
            "# print(predict_return(45) + 1)\n"
        ),
        md(
            "## 3. Одна функция — много объектов\n\n"
            "Реализуйте `batch_predict`: она принимает список значений и функцию, "
            "а возвращает список результатов в том же порядке."
        ),
        code(
            "def batch_predict(values, predict_fn):\n"
            "    pass\n\n\n"
            "areas = list(AREAS_SQM)\n"
            "preds = batch_predict(areas, predict_price)\n\n"
            "assert len(preds) == len(areas)\n"
            "assert preds[0] == predict_price(areas[0])\n"
            "assert batch_predict([], predict_price) == []"
        ),
        md(
            "## 4. Как измерить ошибку\n\n"
            "Для каждого объекта найдите абсолютную ошибку `|предсказание − факт|`. "
            "Функция `mae` должна вернуть среднее этих ошибок.\n\n"
            "Сначала решите, что делать, если длины списков различаются."
        ),
        code(
            "def mae(preds, facts):\n"
            "    pass\n\n\n"
            "assert mae([2, 5], [3, 3]) == 1.5\n"
            "assert mae([4], [4]) == 0\n\n"
            "facts = list(PRICES_MLN)\n"
            "print('MAE:', mae(preds, facts))"
        ),
        md(
            "## 5. Выбор модели по данным\n\n"
            "Переберите все коэффициенты от `0.05` до `0.15` с шагом `0.01`. "
            "Для каждого постройте функцию-предсказатель, посчитайте MAE и сохраните "
            "тройку `(MAE, коэффициент, предсказания)`.\n\n"
            "Выберите лучшую тройку. Объясните, почему сравнивать модели по одной квартире ненадёжно."
        ),
        code(
            "results = []\n\n"
            "for coef_percent in range(5, 16):\n"
            "    coef = coef_percent / 100\n"
            "\n"
            "    def candidate(area_sqm, coef=coef):\n"
            "        return predict_price(area_sqm, intercept=1.5, coef=coef)\n"
            "\n"
            "    # Получите predictions, вычислите error и добавьте тройку в results.\n"
            "    pass\n\n\n"
            "# best_error, best_coef, best_predictions = min(results)\n"
            "# print(f'Лучший коэффициент: {best_coef:.2f}; MAE: {best_error:.3f}')"
        ),
    ),
    "lessons/04_parameters_and_return/lesson.ipynb": nb(
        md(
            "# Параметры и return\n\n"
            "**Пара КТП 4** (2 ч) — введение.\n\n"
            "**Идея:** параметры и `return` задают контракт шага над данными.\n\n"
            "**Данные:** `EXAM_SCORES`, `APARTMENTS`."
        ),
        code(DATA_IMPORT),
        md("## 1. Proto-EDA: `describe_numbers`\n\nСписок чисел → кортеж `(mean, min, max, count)`."),
        code(
            "def describe_numbers(values):\n"
            '    """Вернуть (mean, min, max, count)."""\n'
            "    pass\n\n\n"
            "assert describe_numbers([10, 20, 30])[0] == 20\n"
            "print('describe_numbers OK (допишите остальные поля кортежа)')"
        ),
        md(
            "## 2. `min_max_scale` — к диапазону [0, 1]\n\n"
            "Формула: `(x - min) / (max - min)`. Задел под kNN."
        ),
        code(
            "def min_max_scale(values):\n"
            '    """Min-max scaling списка чисел."""\n'
            "    pass\n\n\n"
            "areas = [a['area_sqm'] for a in APARTMENTS]\n"
            "scaled = min_max_scale(areas)\n"
            "assert abs(min(scaled) - 0) < 1e-9 and abs(max(scaled) - 1) < 1e-9\n"
            "print(scaled)"
        ),
        md("## 3. `clip_outlier` — ограничение выброса"),
        code(
            "def clip_outlier(x, low, high):\n"
            "    return max(low, min(high, x))\n\n\n"
            "print(clip_outlier(150, 0, 100))\n"
            "print(clip_outlier(EXAM_SCORES[0], 0, 100))"
        ),
        md("## 4. Опасный default: `bucket=[]`"),
        code(
            "def collect_outliers_bad(x, bucket=[]):\n"
            "    if x > 100:\n"
            "        bucket.append(x)\n"
            "    return bucket\n\n\n"
            "print(collect_outliers_bad(105))\n"
            "print(collect_outliers_bad(110))  # почему список растёт?"
        ),
        code(
            "def collect_outliers_ok(x, bucket=None):\n"
            "    if bucket is None:\n"
            "        bucket = []\n"
            "    if x > 100:\n"
            "        bucket.append(x)\n"
            "    return bucket\n"
        ),
        md("## Итог\n\nДальше — **пара 5**: серия transform-задач (`grade_stats`, порог)."),
    ),
    "lessons/05_practice_transform/lesson.ipynb": nb(
        md(
            "# Практика: transform\n\n"
            "**Пара КТП 5** (2 ч) — отработка.\n\n"
            "Серия: **transform-функции** над списками. Опора — пара 4.\n\n"
            "**Данные:** `EXAM_SCORES`, `APARTMENTS`, `FEATURE_ROWS`."
        ),
        code(DATA_IMPORT),
        md(
            "## Напоминание: допишите, если нет с пары 4\n\n"
            "`describe_numbers`, `min_max_scale` — нужны для задач ниже."
        ),
        code(
            "def describe_numbers(values):\n"
            "    pass\n\n\n"
            "def min_max_scale(values):\n"
            "    pass\n"
        ),
        md("## Задача 1. Описать `EXAM_SCORES`"),
        code("print(describe_numbers(EXAM_SCORES))\n"),
        md("## Задача 2. Масштаб площадей (повтор с проверкой)"),
        code(
            "areas = [a['area_sqm'] for a in APARTMENTS]\n"
            "scaled = min_max_scale(areas)\n"
            "assert abs(min(scaled) - 0) < 1e-9 and abs(max(scaled) - 1) < 1e-9\n"
            "print('scale OK', scaled)"
        ),
        md("## Задача 3. `grade_stats`"),
        code(
            "def grade_stats(scores, pass_threshold=60):\n"
            '    """(mean, passed_count, failed_count)."""\n'
            "    pass\n\n\n"
            "mean, passed, failed = grade_stats(EXAM_SCORES)\n"
            "assert passed + failed == len(EXAM_SCORES)\n"
            "print(mean, passed, failed)"
        ),
        md(
            "## Задача 4. Порог ≈ 50% сдавших\n\n"
            "Подберите `pass_threshold`, при котором доля сдавших близка к 0.5. Запишите порог."
        ),
        code("# перебор порогов; вывод: лучший порог = ...\n"),
        md(
            "## Задача 5 (по желанию). Clip и снова describe\n\n"
            "Обрежьте все баллы в [50, 95], сравните mean до и после."
        ),
        code("# эксперимент\n"),
        md(
            "## Домашнее задание\n\n"
            "`feature_row_stats(row)` → `(mean, max)` по **числовым** значениям словаря. "
            "Проверка: `FEATURE_ROWS[0]`."
        ),
        code("# ваш код\n"),
        md("## Итог\n\nДальше — **пара 6**: отладка метрик (accuracy, scope)."),
    ),
    "lessons/06_scope_and_debugging/lesson.ipynb": nb(
        md(
            "# Scope и отладка\n\n"
            "**Пара КТП 6** (2 ч) — введение.\n\n"
            "**Идея:** метрика — функция; баг в метрике искажает вывод о модели.\n\n"
            "**Данные:** `PREDICTIONS`, `LABELS`."
        ),
        code(DATA_IMPORT),
        md("## 1. Эталон: `accuracy`\n\nAccuracy = доля верных предсказаний (`pred == label`)."),
        code(
            "def accuracy(preds, labels):\n"
            "    if len(preds) != len(labels):\n"
            "        return None\n"
            "    correct = sum(p == y for p, y in zip(preds, labels))\n"
            "    return correct / len(labels)\n\n\n"
            "print('accuracy =', accuracy(PREDICTIONS, LABELS))"
        ),
        md("## 2. Баг: нет `return`"),
        code(
            "def accuracy_buggy(preds, labels):\n"
            "    correct = 0\n"
            "    for i in range(len(preds)):\n"
            "        if preds[i] == labels[i]:\n"
            "            correct += 1\n"
            "    # баг: нет return\n\n\n"
            "print(accuracy_buggy(PREDICTIONS, LABELS))"
        ),
        code(
            "def accuracy_fixed(preds, labels):\n"
            "    # исправьте\n"
            "    pass\n\n\n"
            "assert abs(accuracy_fixed(PREDICTIONS, LABELS) - accuracy(PREDICTIONS, LABELS)) < 1e-9\n"
            "print('accuracy_fixed OK')"
        ),
        md("## 3. Баг: `global` при подсчёте метрики\n\nИсправьте **без** `global`: накопите результат через return или аргумент."),
        code(
            "total_correct = 0\n\n\n"
            "def update_metrics(pred, label):\n"
            "    total_correct = total_correct + (pred == label)  # баг scope\n"
            "    return total_correct\n\n\n"
            "# ваша версия без global\n"
        ),
        md("## 4. Баг: predict без `return`"),
        code(
            "def predict_pass_buggy(score, threshold=60):\n"
            "    if score >= threshold:\n"
            "        1\n"
            "    else:\n"
            "        0\n\n\n"
            "# result = predict_pass_buggy(72)\n"
            "# print(result)  # почему None?\n"
        ),
        md("## Итог\n\nДальше — **пара 7**: серия `confusion_counts` и журнал отладки."),
    ),
    "lessons/07_practice_metrics/lesson.ipynb": nb(
        md(
            "# Практика: метрики\n\n"
            "**Пара КТП 7** (2 ч) — отработка.\n\n"
            "Серия: **метрики и журнал отладки**. Опора — пара 6.\n\n"
            "**Данные:** `PREDICTIONS`, `LABELS`.\n\n"
            "Счётчики: **tp** pred=1 label=1; **fp** pred=1 label=0; "
            "**fn** pred=0 label=1; **tn** pred=0 label=0."
        ),
        code(DATA_IMPORT),
        md("## Задача 1. Накопление correct без `global`"),
        code("# ваш код и проверка\n"),
        md(
            "## Задача 2. `confusion_counts` → `(tp, fp, fn, tn)`\n\n"
            "Метки 0/1."
        ),
        code(
            "def confusion_counts(preds, labels):\n"
            "    pass\n\n\n"
            "print(confusion_counts(PREDICTIONS, LABELS))"
        ),
        md(
            "## Задача 3. Ручная сверка\n\n"
            "На **первых 4** объектах `PREDICTIONS`/`LABELS` посчитайте tp/fp/fn/tn вручную "
            "и сравните с функцией."
        ),
        code("# ручной подсчёт + сравнение\n"),
        md(
            "## Задача 4. Журнал отладки\n\n"
            "Три строки (accuracy_buggy, update_metrics, predict_pass_buggy с пары 6):\n\n"
            "| Функция | Симптом | Причина | Исправление |\n"
            "|---|---|---|---|\n"
            "| | | | |"
        ),
        md(
            "## Домашнее задание\n\n"
            "Исправьте `homework_counter.py` (рядом с этим ноутбуком) и опишите три шага отладки "
            "(симптом → причина → исправление)."
        ),
        md("## Итог\n\nДальше — **пара 8**: рекурсия на вложенных данных."),
    ),
    "lessons/08_recursion/lesson.ipynb": nb(
        md(
            "# Рекурсия\n\n"
            "**Пара КТП 8** (2 ч) — введение. Отработка серии — **пара 9**.\n\n"
            "**Данные:** `NESTED_API_RESPONSE`, `CATEGORY_TREE`."
        ),
        code(DATA_IMPORT),
        md("## 1. `flatten` — развернуть вложенный список"),
        code(
            "def flatten(nested):\n"
            '    """Список любой вложенности → плоский список."""\n'
            "    pass\n\n\n"
            "assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]\n"
            "print('flatten OK')"
        ),
        md("## 2. `extract_ids` — все `id` из вложенных dict"),
        code(
            "def extract_ids(nested):\n"
            '    """Собрать все значения ключа \'id\' рекурсивно."""\n'
            "    pass\n\n\n"
            "# print(extract_ids(NESTED_API_RESPONSE))\n"
        ),
        md("## 3. `walk_categories` — обход дерева с отступом"),
        code(
            "def walk_categories(node, depth=0):\n"
            "    pass\n\n\n"
            "# walk_categories(CATEGORY_TREE)\n"
        ),
        md("## 4. Fibonacci — антипример (дорого для «просто числа»)"),
        code(
            "def fib_recursive(n):\n"
            "    if n <= 1:\n"
            "        return n\n"
            "    return fib_recursive(n - 1) + fib_recursive(n - 2)\n\n\n"
            "def fib_iterative(n):\n"
            "    a, b = 0, 1\n"
            "    for _ in range(n):\n"
            "        a, b = b, a + b\n"
            "    return a\n\n\n"
            "# сравните время для n=25\n"
        ),
        md(
            "## Домашнее задание\n\n"
            "`count_leaves(node)` для `CATEGORY_TREE`. Серия практики — пара 9."
        ),
        code("def count_leaves(node):\n    pass\n"),
        md(
            "## Итог\n\n"
            "Рекурсия — для **вложенных структур**. Дальше — **пара 9**: серия + lambda + pipeline."
        ),
    ),
    "lessons/09_practice_pipeline/lesson.ipynb": nb(
        md(
            "# Практика: рекурсия, lambda, pipeline\n\n"
            "**Пара КТП 9** (2 ч) — отработка.\n\n"
            "Минимум сдачи: A1–A2, B1–B2, C1. Опора — пары 2–8.\n\n"
            "**Данные:** `NESTED_API_RESPONSE`, `CATEGORY_TREE`, `EXAM_SCORES`, "
            "`MODEL_RUNS`, `FEATURE_ROWS`, `FEATURE_POINTS`."
        ),
        code(DATA_IMPORT),
        md("---\n\n# A. Рекурсия\n"),
        md("## A1. `extract_ids`"),
        code(
            "def extract_ids(nested):\n"
            "    pass\n\n\n"
            "# print(extract_ids(NESTED_API_RESPONSE))\n"
        ),
        md("## A2. `walk_categories`"),
        code(
            "def walk_categories(node, depth=0):\n"
            "    pass\n\n\n"
            "# walk_categories(CATEGORY_TREE)\n"
        ),
        md("## A3 (углубление). `count_leaves`"),
        code("def count_leaves(node):\n    pass\n"),
        md("---\n\n# B. Lambda\n"),
        md("## B1. `filter` — аномалии (свой порог)"),
        code(
            "anomalies = list(filter(lambda s: s < 50 or s > 90, EXAM_SCORES))\n"
            "print(anomalies)"
        ),
        md("## B2. Leaderboard `MODEL_RUNS`\n\nСортировка: f1 ↓; при равенстве — id ↑."),
        code(
            "leaderboard = sorted(MODEL_RUNS, key=lambda r: (-r['f1'], r['id']))\n"
            "print([r['id'] for r in leaderboard])\n"
            "# ожидаемый порядок id: 25, 30, 305, 101, 200\n"
        ),
        md("## B3 (углубление). Farthest point"),
        code(
            "# farthest = max(FEATURE_POINTS, key=lambda p: ...)\n"
            "# print(farthest)\n"
        ),
        md("---\n\n# C. Pipeline\n"),
        md("## C1. `apply_pipeline`"),
        code(
            "def apply_pipeline(data, steps):\n"
            "    result = data\n"
            "    for step in steps:\n"
            "        result = step(result)\n"
            "    return result\n"
        ),
        md("## C1. Цепочка для одной квартиры\n\n`dict → area → scale → predict`"),
        code(
            "def extract_area(row):\n"
            "    return row['area_sqm']\n\n\n"
            "def scale_area(area, max_area=60):\n"
            "    return area / max_area\n\n\n"
            "def predict_from_scaled(scaled_area):\n"
            "    return PRICE_INTERCEPT + PRICE_COEF_AREA * (scaled_area * 60)\n\n\n"
            "apt_pipeline = [extract_area, scale_area, predict_from_scaled]\n"
            "pred = apply_pipeline(FEATURE_ROWS[0], apt_pipeline)\n"
            "print('predicted mln:', pred)"
        ),
        md(
            "## Эксперимент: порядок шагов\n\n"
            "Что будет, если вызвать scale до extract? Запишите ошибку/вывод."
        ),
        code("# эксперимент\n"),
        md("## C2 (углубление). Текстовый pipeline"),
        code(
            "text_pipeline = [\n"
            "    lambda s: s.strip().lower(),\n"
            "    lambda s: s.split(),\n"
            "    lambda tokens: [t for t in tokens if len(t) >= 4],\n"
            "]\n\n"
            "print(apply_pipeline('  Data science ML course  ', text_pipeline))"
        ),
        md(
            "## Мост к артефакту\n\n"
            "Пары 10–11: [artifact/PROJECT.md](../../artifact/PROJECT.md) и "
            "[LESSON пары 10](../10_artifact_build/LESSON.md)."
        ),
        md("## Итог\n\n**Pipeline = композиция функций.** Дальше — итоговый модуль `text_stats`."),
    ),
}


HOMEWORKS = {
    "lessons/02_function_as_mapping/homework.ipynb": nb(
        md("# Домашнее задание: функция-предсказатель"),
        code(
            "AREAS_SQM = [28, 32, 45, 55, 60]\n"
            "PRICES_MLN = [3.9, 4.2, 5.8, 6.5, 7.1]\n"
            "ROOMS = [1, 1, 2, 2, 3]  # число комнат у квартиры с тем же индексом\n"
        ),
        md(
            "## 1. Напоминание с пары\n\n"
            "Скопируйте из своего `lesson.ipynb` (или напишите заново) функции "
            "`predict_price`, `batch_predict`, `mae`."
        ),
        code(
            "def predict_price(area_sqm, intercept=1.5, coef=0.09):\n"
            "    pass\n\n\n"
            "def batch_predict(values, predict_fn):\n"
            "    pass\n\n\n"
            "def mae(preds, facts):\n"
            "    pass\n"
        ),
        md(
            "## 2. Второй признак — комнаты\n\n"
            "Напишите `predict_room_price(area_sqm, rooms)`:\n\n"
            "- как `predict_price` по площади;\n"
            "- плюс **0.3 млн** за каждую комнату **сверх одной** (`rooms - 1`, но не меньше нуля).\n\n"
            "Проверьте на трёх примерах своих чисел и на одной строке из таблицы (индекс 0–4)."
        ),
        code(
            "def predict_room_price(area_sqm, rooms, intercept=1.5, coef=0.09):\n"
            "    pass\n\n\n"
            "# assert predict_room_price(45, 2) == ...\n"
            "# print(predict_room_price(AREAS_SQM[2], ROOMS[2]))\n"
        ),
        md(
            "## 3. Устойчивость вывода\n\n"
            "Удалите из `AREAS_SQM` и `PRICES_MLN` квартиру с **самой большой** площадью. "
            "Снова переберите коэффициенты от `0.05` до `0.15` (шаг `0.01`) и найдите лучший по MAE.\n\n"
            "Совпал ли лучший коэффициент с полным набором из пяти квартир? "
            "Запишите **2–3 предложения**: что показал эксперимент."
        ),
        code("# areas_sub, prices_sub, лучший coef, MAE, вывод\n"),
        md(
            "## 4. Два параметра\n\n"
            "Подберите **intercept** и **coef** по сетке:\n\n"
            "- `intercept ∈ {0.5, 1.0, 1.5, 2.0}`\n"
            "- `coef` от `0.05` до `0.15` с шагом `0.01`\n\n"
            "Верните **три** лучшие пары `(MAE, intercept, coef)` по возрастанию MAE."
        ),
        code(
            "top3 = []  # список кортежей (mae, intercept, coef)\n"
            "# заполните и выведите top3\n"
        ),
    ),
}


if __name__ == "__main__":
    for rel, notebook in NOTEBOOKS.items():
        write(rel, notebook)
    for rel, notebook in HOMEWORKS.items():
        write(rel, notebook)
