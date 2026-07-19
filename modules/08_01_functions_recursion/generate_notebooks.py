#!/usr/bin/env python3
"""Generate lesson notebooks: one pair KTP = one lesson.ipynb (pairs 2–7)."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

LESSON_02_DATA = (
    "# Площадь (м²) и фактическая цена (млн руб.) — одна квартира на один индекс\n"
    "AREAS_SQM = [28, 32, 45, 55, 60]\n"
    "PRICES_MLN = [3.9, 4.2, 5.8, 6.5, 7.1]\n"
)

LESSON_03_DATA = (
    "# Баллы экзамена (10 учеников)\n"
    "EXAM_SCORES = [40, 55, 62, 75, 88, 91, 48, 100, 33, 67]\n"
    "# Площади квартир — те же, что на паре 2\n"
    "AREAS_SQM = [28, 32, 45, 55, 60]\n"
)

LESSON_04_DATA = (
    "# Лабораторные баллы (8 работ) — другая выборка, не EXAM_SCORES\n"
    "LAB_SCORES = [72, 81, 55, 90, 44, 38, 92, 58]\n"
    "AREAS_SQM = [28, 32, 45, 55, 60]\n"
    "ROOMS_COUNTS = [1, 1, 2, 2, 3]  # число комнат у квартиры с тем же индексом\n"
)

LESSON_05_DATA = (
    "# Предсказания и метки (0/1) — 10 объектов\n"
    "PREDICTIONS = [1, 0, 1, 1, 0, 1, 1, 0, 1, 0]\n"
    "LABELS =      [1, 0, 1, 0, 0, 1, 1, 0, 1, 1]\n"
    "# Баллы (для predict_pass на паре)\n"
    "SCORES = [72, 55, 88, 44, 61, 90, 77, 48, 83, 58]\n"
)

LESSON_07_DATA = (
    "# Вложенный список (без dict)\n"
    "NESTED_LIST = [1, [2, [3, 4]], 5]\n"
    "# Простое дерево: (name, children)\n"
    "CATEGORY_TREE = (\n"
    "    'root',\n"
    "    [\n"
    "        ('electronics', [('phones', []), ('laptops', [])]),\n"
    "        ('books', []),\n"
    "    ],\n"
    ")\n"
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
    "lessons/03_parameters_and_return/lesson.ipynb": nb(
        md("# Параметры и return — describe, scale, контракт transform"),
        code(LESSON_03_DATA),
        md(
            "## 1. Proto-EDA: `describe_numbers`\n\n"
            "Список чисел → кортеж `(mean, min, max, count)`. Результат нужен следующей функции — используйте `return`."
        ),
        code(
            "def describe_numbers(values):\n"
            '    """Вернуть (mean, min, max, count)."""\n'
            "    pass\n\n\n"
            "assert describe_numbers([10, 20, 30])[0] == 20\n"
            "assert describe_numbers([10, 20, 30])[3] == 3\n"
            "print(describe_numbers(EXAM_SCORES))"
        ),
        md(
            "## 2. Min-max scale\n\n"
            "Приведите список к диапазону [0, 1]: `(x - min) / (max - min)`. "
            "Если `min == max`, верните список нулей той же длины."
        ),
        code(
            "def min_max_scale(values):\n"
            '    """Min-max scaling списка чисел."""\n'
            "    pass\n\n\n"
            "scaled = min_max_scale(AREAS_SQM)\n"
            "assert abs(min(scaled) - 0) < 1e-9 and abs(max(scaled) - 1) < 1e-9\n"
            "print(scaled)"
        ),
        md("## 3. Clip выброса\n\nОграничьте одно число границами `low` и `high`. Сравните mean до и после clip для одного «дикого» балла."),
        code(
            "def clip_outlier(x, low, high):\n"
            "    return max(low, min(high, x))\n\n\n"
            "wild = EXAM_SCORES[7]  # 100\n"
            "print('до clip:', describe_numbers(EXAM_SCORES))\n"
            "clipped_one = clip_outlier(wild, 0, 95)\n"
            "print('clip(100, 0, 95) =', clipped_one)"
        ),
        md(
            "## 4. Опасный default\n\n"
            "Запустите `collect_outliers_bad` дважды. Почему список растёт? Исправьте через `bucket=None`."
        ),
        code(
            "def collect_outliers_bad(x, bucket=[]):\n"
            "    if x > 100:\n"
            "        bucket.append(x)\n"
            "    return bucket\n\n\n"
            "print(collect_outliers_bad(105))\n"
            "print(collect_outliers_bad(110))\n\n\n"
            "def collect_outliers_ok(x, bucket=None):\n"
            "    if bucket is None:\n"
            "        bucket = []\n"
            "    if x > 100:\n"
            "        bucket.append(x)\n"
            "    return bucket\n\n\n"
            "assert collect_outliers_ok(105) == [105]\n"
            "assert collect_outliers_ok(110) == [110]"
        ),
        md(
            "## 5. Порог сдачи\n\n"
            "`grade_stats(scores, pass_threshold=60)` → `(mean, passed_count, failed_count)`."
        ),
        code(
            "def grade_stats(scores, pass_threshold=60):\n"
            '    """(mean, passed_count, failed_count)."""\n'
            "    pass\n\n\n"
            "mean, passed, failed = grade_stats(EXAM_SCORES)\n"
            "assert passed + failed == len(EXAM_SCORES)\n"
            "print(mean, passed, failed)"
        ),
    ),
    "lessons/04_practice_transform/lesson.ipynb": nb(
        md("# Практика: transform на новых данных"),
        code(LESSON_04_DATA),
        md(
            "## 1. Опора\n\n"
            "Вставьте **рабочие** функции с [пары 3](../03_parameters_and_return/lesson.ipynb): "
            "`describe_numbers`, `min_max_scale`, `clip_outlier`, `grade_stats`. "
            "Без заготовок `pass` — только ваш код."
        ),
        code(
            "# describe_numbers, min_max_scale, clip_outlier, grade_stats — вставьте сюда\n"
            "# Проверка:\n"
            "# assert describe_numbers([1, 2, 3])[0] == 2\n"
        ),
        md(
            "## 2. Другая выборка\n\n"
            "Вычислите `describe_numbers(LAB_SCORES)`. "
            "Запишите в комментарии: сколько работ (`count`) и средний балл (`mean`)."
        ),
        code(
            "stats = describe_numbers(LAB_SCORES)\n"
            "print(stats)\n"
            "# count = ..., mean = ...\n"
            "assert stats[3] == len(LAB_SCORES)"
        ),
        md(
            "## 3. Два признака\n\n"
            "Масштабируйте **отдельно** `AREAS_SQM` и `ROOMS_COUNTS` в [0, 1]. "
            "Почему нельзя просто сложить сырые площадь и число комнат?"
        ),
        code(
            "scaled_areas = min_max_scale(AREAS_SQM)\n"
            "scaled_rooms = min_max_scale(ROOMS_COUNTS)\n"
            "assert abs(min(scaled_areas) - 0) < 1e-9 and abs(max(scaled_areas) - 1) < 1e-9\n"
            "assert abs(min(scaled_rooms) - 0) < 1e-9 and abs(max(scaled_rooms) - 1) < 1e-9\n"
            "print('areas', scaled_areas)\n"
            "print('rooms', scaled_rooms)"
        ),
        md(
            "## 4. Порог: ровно k сдавших\n\n"
            "Найдите целый `pass_threshold`, при котором на `LAB_SCORES` **ровно 4** сдавших "
            "(`score >= threshold`). Запишите порог и проверьте через `grade_stats`.\n\n"
            "*Не то же самое, что «доля ≈ 50%» в ДЗ пары 3.*"
        ),
        code(
            "TARGET_PASSED = 4\n"
            "# перебор порогов; best_threshold = ...\n"
            "# mean, passed, failed = grade_stats(LAB_SCORES, best_threshold)\n"
            "# assert passed == TARGET_PASSED\n"
            "# print(f'порог = {best_threshold}, passed = {passed}')"
        ),
        md(
            "## 5. Цепочка transform\n\n"
            "Напишите `apply_transform(values, fn)` — вернуть `fn(values)`. "
            "Получите кортеж describe **после** `min_max_scale(LAB_SCORES)`."
        ),
        code(
            "def apply_transform(values, fn):\n"
            '    """Применить fn к списку values и вернуть результат."""\n'
            "    pass\n\n\n"
            "scaled_lab = apply_transform(LAB_SCORES, min_max_scale)\n"
            "after_stats = describe_numbers(scaled_lab)\n"
            "assert abs(after_stats[1] - 0) < 1e-9 and abs(after_stats[2] - 1) < 1e-9\n"
            "print('describe после scale:', after_stats)"
        ),
    ),
    "lessons/05_scope_and_debugging/lesson.ipynb": nb(
        md("# Scope и отладка — метрика как функция"),
        code(LESSON_05_DATA),
        md(
            "## 1. Эталон accuracy\n\n"
            "Accuracy = доля верных предсказаний (`pred == label`). "
            "Прочитайте эталон и вычислите значение на `PREDICTIONS` / `LABELS`."
        ),
        code(
            "def accuracy(preds, labels):\n"
            "    if len(preds) != len(labels):\n"
            "        return None\n"
            "    correct = sum(p == y for p, y in zip(preds, labels))\n"
            "    return correct / len(labels)\n\n\n"
            "REF_ACCURACY = accuracy(PREDICTIONS, LABELS)\n"
            "print('эталон accuracy =', REF_ACCURACY)"
        ),
        md(
            "## 2. Своя accuracy\n\n"
            "Напишите `my_accuracy(preds, labels)` **с нуля** (не копируйте тело эталона). "
            "При разной длине списков верните `None`."
        ),
        code(
            "def my_accuracy(preds, labels):\n"
            '    """Доля верных предсказаний или None."""\n'
            "    pass\n\n\n"
            "assert abs(my_accuracy(PREDICTIONS, LABELS) - REF_ACCURACY) < 1e-9\n"
            "assert my_accuracy([1], [1, 0]) is None"
        ),
        md(
            "## 3. Баг: нет return\n\n"
            "Запустите `accuracy_buggy`. Почему результат `None`? "
            "Исправьте функцию (или объясните в комментарии и допишите `accuracy_fixed`)."
        ),
        code(
            "def accuracy_buggy(preds, labels):\n"
            "    correct = 0\n"
            "    for i in range(len(preds)):\n"
            "        if preds[i] == labels[i]:\n"
            "            correct += 1\n"
            "    # баг: нет return\n\n\n"
            "print('buggy:', accuracy_buggy(PREDICTIONS, LABELS))\n\n\n"
            "def accuracy_fixed(preds, labels):\n"
            "    pass\n\n\n"
            "# assert abs(accuracy_fixed(PREDICTIONS, LABELS) - REF_ACCURACY) < 1e-9"
        ),
        md(
            "## 4. Подсчёт без global\n\n"
            "Напишите `count_correct(preds, labels)` — число совпадений в цикле. "
            "**Без** `global`. Подсказка: накопитель в цикле, `return` в конце."
        ),
        code(
            "def count_correct(preds, labels):\n"
            "    pass\n\n\n"
            "assert count_correct(PREDICTIONS, LABELS) == round(REF_ACCURACY * len(PREDICTIONS))"
        ),
        md(
            "## 5. predict без return\n\n"
            "Исправьте `predict_pass`: вернуть `1`, если `score >= threshold`, иначе `0`."
        ),
        code(
            "def predict_pass_buggy(score, threshold=60):\n"
            "    if score >= threshold:\n"
            "        1\n"
            "    else:\n"
            "        0\n\n\n"
            "def predict_pass(score, threshold=60):\n"
            "    pass\n\n\n"
            "assert predict_pass(72) == 1\n"
            "assert predict_pass(55) == 0\n"
            "assert predict_pass_buggy(72) is None"
        ),
    ),
    "lessons/06_practice_metrics/lesson.ipynb": nb(
        md("# Практика: confusion_counts и журнал отладки"),
        code(LESSON_05_DATA),
        md(
            "## 1. Опора\n\n"
            "Вставьте с [пары 5](../05_scope_and_debugging/lesson.ipynb): `count_correct` и `my_accuracy`."
        ),
        code("# count_correct, my_accuracy\n"),
        md(
            "## 2. confusion_counts\n\n"
            "Один проход по `zip(preds, labels)`. Верните `(tp, fp, fn, tn)` для меток 0/1."
        ),
        code(
            "def confusion_counts(preds, labels):\n"
            '    """(tp, fp, fn, tn)."""\n'
            "    pass\n\n\n"
            "tp, fp, fn, tn = confusion_counts(PREDICTIONS, LABELS)\n"
            "assert tp + fp + fn + tn == len(PREDICTIONS)\n"
            "print(tp, fp, fn, tn)"
        ),
        md(
            "## 3. Сверка вручную\n\n"
            "На **первых 4** парах `PREDICTIONS`/`LABELS` посчитайте tp, fp, fn, tn вручную "
            "и сравните с `confusion_counts(PREDICTIONS[:4], LABELS[:4])`."
        ),
        code(
            "# ручной подсчёт\n"
            "manual = confusion_counts(PREDICTIONS[:4], LABELS[:4])\n"
            "print('функция на 4:', manual)\n"
            "# assert manual == (..., ..., ..., ...)"
        ),
        md(
            "## 4. Журнал отладки\n\n"
            "Добавьте **markdown-ячейку**: таблица **3** багов с пары 5 "
            "(функция | симптом | причина | исправление)."
        ),
    ),


}


SOLUTIONS = {
    "lessons/03_parameters_and_return/solutions.ipynb": nb(
        md(
            "# Решения: параметры и return\n\n"
            "**Для преподавателя.** Все задачи из `lesson.ipynb` и `homework.ipynb`."
        ),
        code(
            "EXAM_SCORES = [40, 55, 62, 75, 88, 91, 48, 100, 33, 67]\n"
            "AREAS_SQM = [28, 32, 45, 55, 60]\n"
            "ROW_AREAS = [28, 45, 60, 32]\n"
            "ROW_ROOMS = [1, 2, 3, 1]\n"
            "ROW_FLOORS = [3, 7, 12, 2]\n"
        ),
        md("## Урок. 1. `describe_numbers`"),
        code(
            "def describe_numbers(values):\n"
            "    if not values:\n"
            "        return (0.0, 0.0, 0.0, 0)\n"
            "    return (sum(values) / len(values), min(values), max(values), len(values))\n\n\n"
            "assert describe_numbers([10, 20, 30])[0] == 20"
        ),
        md("## Урок. 2. `min_max_scale`"),
        code(
            "def min_max_scale(values):\n"
            "    if not values:\n"
            "        return []\n"
            "    lo, hi = min(values), max(values)\n"
            "    if lo == hi:\n"
            "        return [0.0] * len(values)\n"
            "    return [(x - lo) / (hi - lo) for x in values]\n\n\n"
            "scaled = min_max_scale(AREAS_SQM)\n"
            "assert abs(min(scaled) - 0) < 1e-9 and abs(max(scaled) - 1) < 1e-9"
        ),
        md("## Урок. 3. `clip_outlier`"),
        code(
            "def clip_outlier(x, low, high):\n"
            "    return max(low, min(high, x))"
        ),
        md("## Урок. 4. mutable default"),
        code(
            "def collect_outliers_ok(x, bucket=None):\n"
            "    if bucket is None:\n"
            "        bucket = []\n"
            "    if x > 100:\n"
            "        bucket.append(x)\n"
            "    return bucket\n\n\n"
            "assert collect_outliers_ok(105) == [105]\n"
            "assert collect_outliers_ok(110) == [110]"
        ),
        md("## Урок. 5. `grade_stats`"),
        code(
            "def grade_stats(scores, pass_threshold=60):\n"
            "    passed = sum(1 for s in scores if s >= pass_threshold)\n"
            "    failed = len(scores) - passed\n"
            "    mean = sum(scores) / len(scores) if scores else 0.0\n"
            "    return (mean, passed, failed)\n\n\n"
            "mean, passed, failed = grade_stats(EXAM_SCORES)\n"
            "assert passed + failed == len(EXAM_SCORES)"
        ),
        md("## ДЗ. 1. Напоминание — функции урока выше"),
        md("## ДЗ. 2. Clip всей выборки"),
        code(
            "def clip_scores(scores, low, high):\n"
            "    return [clip_outlier(s, low, high) for s in scores]\n\n\n"
            "before = describe_numbers(EXAM_SCORES)\n"
            "clipped = clip_scores(EXAM_SCORES, 50, 95)\n"
            "after = describe_numbers(clipped)\n"
            "print('mean до:', before[0], 'после:', after[0])"
        ),
        md("## ДЗ. 3. `row_numeric_stats`"),
        code(
            "def row_numeric_stats(area, rooms, floor):\n"
            "    nums = [area, rooms, floor]\n"
            "    return (sum(nums) / len(nums), max(nums))\n\n\n"
            "assert abs(row_numeric_stats(ROW_AREAS[0], ROW_ROOMS[0], ROW_FLOORS[0])[0] - 10.666666) < 1e-5"
        ),
        md("## ДЗ. 4. Подбор порога"),
        code(
            "best = None\n"
            "for threshold in range(40, 96):\n"
            "    _, passed, failed = grade_stats(EXAM_SCORES, threshold)\n"
            "    rate = passed / len(EXAM_SCORES)\n"
            "    diff = abs(rate - 0.5)\n"
            "    if best is None or diff < best[0]:\n"
            "        best = (diff, threshold, rate)\n"
            "print(f'лучший порог = {best[1]}, доля сдавших = {best[2]:.2f}')"
        ),
    ),
    "lessons/04_practice_transform/solutions.ipynb": nb(
        md(
            "# Решения: практика transform\n\n"
            "**Для преподавателя.** Все задачи из `lesson.ipynb` и `homework.ipynb`."
        ),
        code(
            "LAB_SCORES = [72, 81, 55, 90, 44, 38, 92, 58]\n"
            "AREAS_SQM = [28, 32, 45, 55, 60]\n"
            "ROOMS_COUNTS = [1, 1, 2, 2, 3]\n"
            "FEATURE_ROWS = [\n"
            "    (28, 1, 3, 'north'),\n"
            "    (45, 2, 7, 'center'),\n"
            "    (60, 3, 12, 'south'),\n"
            "    (32, 1, 2, 'west'),\n"
            "]\n\n\n"
            "def describe_numbers(values):\n"
            "    if not values:\n"
            "        return (0.0, 0.0, 0.0, 0)\n"
            "    return (sum(values) / len(values), min(values), max(values), len(values))\n\n\n"
            "def min_max_scale(values):\n"
            "    if not values:\n"
            "        return []\n"
            "    lo, hi = min(values), max(values)\n"
            "    if lo == hi:\n"
            "        return [0.0] * len(values)\n"
            "    return [(x - lo) / (hi - lo) for x in values]\n\n\n"
            "def clip_outlier(x, low, high):\n"
            "    return max(low, min(high, x))\n\n\n"
            "def grade_stats(scores, pass_threshold=60):\n"
            "    passed = sum(1 for s in scores if s >= pass_threshold)\n"
            "    failed = len(scores) - passed\n"
            "    mean = sum(scores) / len(scores) if scores else 0.0\n"
            "    return (mean, passed, failed)\n"
        ),
        md("## Урок. 2. Describe `LAB_SCORES`"),
        code(
            "stats = describe_numbers(LAB_SCORES)\n"
            "assert stats[3] == 8\n"
            "print(stats)"
        ),
        md("## Урок. 3. Два scale"),
        code(
            "scaled_areas = min_max_scale(AREAS_SQM)\n"
            "scaled_rooms = min_max_scale(ROOMS_COUNTS)\n"
            "assert abs(max(scaled_areas) - 1) < 1e-9\n"
            "assert abs(max(scaled_rooms) - 1) < 1e-9"
        ),
        md("## Урок. 4. Порог для k=4"),
        code(
            "TARGET_PASSED = 4\n"
            "best_threshold = None\n"
            "for threshold in range(0, 101):\n"
            "    _, passed, _ = grade_stats(LAB_SCORES, threshold)\n"
            "    if passed == TARGET_PASSED:\n"
            "        best_threshold = threshold\n"
            "        break\n"
            "assert best_threshold == 59\n"
            "print('порог =', best_threshold)"
        ),
        md("## Урок. 5. `apply_transform`"),
        code(
            "def apply_transform(values, fn):\n"
            "    return fn(values)\n\n\n"
            "after_stats = describe_numbers(apply_transform(LAB_SCORES, min_max_scale))\n"
            "assert abs(after_stats[1] - 0) < 1e-9 and abs(after_stats[2] - 1) < 1e-9"
        ),
        md("## ДЗ. 2. `numeric_stats_from_row`"),
        code(
            "def numeric_stats_from_row(row):\n"
            "    nums = [x for x in row if isinstance(x, (int, float))]\n"
            "    return describe_numbers(nums)[0], max(nums)\n\n\n"
            "mean, mx = numeric_stats_from_row(FEATURE_ROWS[0])\n"
            "assert abs(mean - 10.666666) < 1e-5 and mx == 28"
        ),
        md("## ДЗ. 3. `transform_pipeline`"),
        code(
            "def clip_scores(scores, low, high):\n"
            "    return [clip_outlier(s, low, high) for s in scores]\n\n\n"
            "def transform_pipeline(values, *fns):\n"
            "    result = values\n"
            "    for fn in fns:\n"
            "        result = fn(result)\n"
            "    return result\n\n\n"
            "only_scale = describe_numbers(min_max_scale(LAB_SCORES))[0]\n"
            "clip_then_scale = describe_numbers(\n"
            "    transform_pipeline(LAB_SCORES, lambda xs: clip_scores(xs, 50, 95), min_max_scale)\n"
            ")[0]\n"
            "print('mean: только scale', only_scale, '; clip→scale', clip_then_scale)"
        ),
        md("## ДЗ. 4. Сравнение preprocess"),
        code(
            "before = describe_numbers(LAB_SCORES)[0]\n"
            "after_clip = describe_numbers(clip_scores(LAB_SCORES, 50, 95))[0]\n"
            "print('mean до:', before, 'после clip [50,95]:', after_clip)"
        ),
    ),
    "lessons/05_scope_and_debugging/solutions.ipynb": nb(
        md(
            "# Решения: scope и отладка\n\n"
            "**Для преподавателя.** Все задачи из `lesson.ipynb` и `homework.ipynb`."
        ),
        code(
            "PREDICTIONS = [1, 0, 1, 1, 0, 1, 1, 0, 1, 0]\n"
            "LABELS =      [1, 0, 1, 0, 0, 1, 1, 0, 1, 1]\n"
            "SCORES = [72, 55, 88, 44, 61, 90, 77, 48, 83, 58]\n"
        ),
        md("## Урок. 1–2. accuracy / my_accuracy"),
        code(
            "def accuracy(preds, labels):\n"
            "    if len(preds) != len(labels):\n"
            "        return None\n"
            "    correct = sum(p == y for p, y in zip(preds, labels))\n"
            "    return correct / len(labels)\n\n\n"
            "REF_ACCURACY = accuracy(PREDICTIONS, LABELS)\n\n\n"
            "def my_accuracy(preds, labels):\n"
            "    if len(preds) != len(labels):\n"
            "        return None\n"
            "    if not preds:\n"
            "        return 0.0\n"
            "    correct = 0\n"
            "    for p, y in zip(preds, labels):\n"
            "        if p == y:\n"
            "            correct += 1\n"
            "    return correct / len(labels)\n\n\n"
            "assert abs(my_accuracy(PREDICTIONS, LABELS) - REF_ACCURACY) < 1e-9"
        ),
        md("## Урок. 3. accuracy_fixed"),
        code(
            "def accuracy_fixed(preds, labels):\n"
            "    correct = 0\n"
            "    for i in range(len(preds)):\n"
            "        if preds[i] == labels[i]:\n"
            "            correct += 1\n"
            "    return correct / len(preds) if preds else 0.0"
        ),
        md("## Урок. 4. count_correct"),
        code(
            "def count_correct(preds, labels):\n"
            "    total = 0\n"
            "    for p, y in zip(preds, labels):\n"
            "        if p == y:\n"
            "            total += 1\n"
            "    return total\n\n\n"
            "assert count_correct(PREDICTIONS, LABELS) == 7"
        ),
        md("## Урок. 5. predict_pass"),
        code(
            "def predict_pass(score, threshold=60):\n"
            "    return 1 if score >= threshold else 0\n\n\n"
            "assert predict_pass(72) == 1"
        ),
        md("## ДЗ. 2. batch_predict_pass"),
        code(
            "def batch_predict_pass(scores, threshold=60):\n"
            "    return [predict_pass(s, threshold) for s in scores]\n\n\n"
            "preds = batch_predict_pass(SCORES, 60)\n"
            "assert len(preds) == len(SCORES)"
        ),
        md("## ДЗ. 4. shadowing"),
        code(
            "def accuracy_shadow_bug(preds, labels):\n"
            "    labels = 0  # затёрли аргумент!\n"
            "    correct = sum(p == labels for p in preds)\n"
            "    return correct / len(preds)\n\n\n"
            "def accuracy_shadow_ok(preds, labels):\n"
            "    correct = sum(p == y for p, y in zip(preds, labels))\n"
            "    return correct / len(preds)\n\n\n"
            "assert abs(accuracy_shadow_ok(PREDICTIONS, LABELS) - REF_ACCURACY) < 1e-9"
        ),
    ),
    "lessons/06_practice_metrics/solutions.ipynb": nb(
        md("# Решения: практика метрик\n\n**Для преподавателя.**"),
        code(
            "PREDICTIONS = [1, 0, 1, 1, 0, 1, 1, 0, 1, 0]\n"
            "LABELS =      [1, 0, 1, 0, 0, 1, 1, 0, 1, 1]\n"
        ),
        md("## Урок. confusion_counts"),
        code(
            "def confusion_counts(preds, labels):\n"
            "    tp = fp = fn = tn = 0\n"
            "    for p, y in zip(preds, labels):\n"
            "        if p == 1 and y == 1:\n"
            "            tp += 1\n"
            "        elif p == 1 and y == 0:\n"
            "            fp += 1\n"
            "        elif p == 0 and y == 1:\n"
            "            fn += 1\n"
            "        elif p == 0 and y == 0:\n"
            "            tn += 1\n"
            "    return tp, fp, fn, tn\n\n\n"
            "assert confusion_counts(PREDICTIONS[:4], LABELS[:4]) == (2, 1, 0, 1)"
        ),
        md("## ДЗ. counter"),
        code(
            "def increment(counter):\n"
            "    return counter + 1\n\n\n"
            "def reset_and_count(items):\n"
            "    total = 0\n"
            "    for x in items:\n"
            "        total += x\n"
            "    return total\n\n\n"
            "c = 0\n"
            "c = increment(c)\n"
            "assert c == 1\n"
            "assert reset_and_count([1, 2, 3]) == 6"
        ),
    ),
    "lessons/02_function_as_mapping/solutions.ipynb": nb(
        md(
            "# Решения: функция-предсказатель\n\n"
            "**Для преподавателя.** Все задачи из `lesson.ipynb` и `homework.ipynb`."
        ),
        code(
            "AREAS_SQM = [28, 32, 45, 55, 60]\n"
            "PRICES_MLN = [3.9, 4.2, 5.8, 6.5, 7.1]\n"
            "ROOMS = [1, 1, 2, 2, 3]\n"
        ),
        md("## Урок. 1. `predict_price`"),
        code(
            "def predict_price(area_sqm, intercept=1.5, coef=0.09):\n"
            "    return intercept + coef * area_sqm\n\n\n"
            "assert predict_price(0) == 1.5\n"
            "assert abs(predict_price(50) - 6.0) < 1e-9"
        ),
        md("## Урок. 2. print vs return"),
        code(
            "def predict_print(area_sqm):\n"
            "    print(predict_price(area_sqm))\n\n\n"
            "def predict_return(area_sqm):\n"
            "    return predict_price(area_sqm)\n\n\n"
            "print('predict_print(45) + 1 →', end=' ')\n"
            "try:\n"
            "    print(predict_print(45) + 1)\n"
            "except TypeError:\n"
            "    print('ошибка: print не возвращает значение (None)')\n\n"
            "print('predict_return(45) + 1 =', predict_return(45) + 1)"
        ),
        md("## Урок. 3. `batch_predict`"),
        code(
            "def batch_predict(values, predict_fn):\n"
            "    return [predict_fn(v) for v in values]\n\n\n"
            "areas = list(AREAS_SQM)\n"
            "preds = batch_predict(areas, predict_price)\n"
            "assert len(preds) == len(areas)\n"
            "assert batch_predict([], predict_price) == []"
        ),
        md(
            "## Урок. 4. `mae`\n\n"
            "При разной длине списков — `ValueError`: метрика не определена."
        ),
        code(
            "def mae(preds, facts):\n"
            "    if len(preds) != len(facts):\n"
            "        raise ValueError('preds и facts должны быть одной длины')\n"
            "    if not preds:\n"
            "        return 0.0\n"
            "    return sum(abs(p - f) for p, f in zip(preds, facts)) / len(preds)\n\n\n"
            "assert mae([2, 5], [3, 3]) == 1.5\n"
            "print('MAE на паре:', mae(preds, PRICES_MLN))"
        ),
        md(
            "## Урок. 5. Выбор коэффициента\n\n"
            "`coef=coef` в аргументах по умолчанию — иначе замыкание в цикле даст один и тот же coef."
        ),
        code(
            "results = []\n\n"
            "for coef_percent in range(5, 16):\n"
            "    coef = coef_percent / 100\n\n"
            "    def candidate(area_sqm, coef=coef):\n"
            "        return predict_price(area_sqm, intercept=1.5, coef=coef)\n\n"
            "    predictions = batch_predict(AREAS_SQM, candidate)\n"
            "    error = mae(predictions, PRICES_MLN)\n"
            "    results.append((error, coef, predictions))\n\n"
            "best_error, best_coef, best_predictions = min(results)\n"
            "print(f'Лучший коэффициент: {best_coef:.2f}; MAE: {best_error:.3f}')"
        ),
        md("## ДЗ. 1. Базовые функции — см. ячейки урока выше"),
        md("## ДЗ. 2. `predict_room_price`"),
        code(
            "def predict_room_price(area_sqm, rooms, intercept=1.5, coef=0.09):\n"
            "    room_bonus = max(rooms - 1, 0) * 0.3\n"
            "    return predict_price(area_sqm, intercept, coef) + room_bonus\n\n\n"
            "assert abs(predict_room_price(45, 2) - 5.85) < 1e-9\n"
            "print('строка 2:', predict_room_price(AREAS_SQM[2], ROOMS[2]))"
        ),
        md("## ДЗ. 3. Устойчивость при удалении точки"),
        code(
            "idx_max = max(range(len(AREAS_SQM)), key=lambda i: AREAS_SQM[i])\n"
            "areas_sub = [a for i, a in enumerate(AREAS_SQM) if i != idx_max]\n"
            "prices_sub = [p for i, p in enumerate(PRICES_MLN) if i != idx_max]\n\n"
            "sub_results = []\n"
            "for coef_percent in range(5, 16):\n"
            "    coef = coef_percent / 100\n\n"
            "    def candidate(area_sqm, coef=coef):\n"
            "        return predict_price(area_sqm, intercept=1.5, coef=coef)\n\n"
            "    predictions = batch_predict(areas_sub, candidate)\n"
            "    sub_results.append((mae(predictions, prices_sub), coef))\n\n"
            "best_sub_error, best_sub_coef = min(sub_results)\n"
            "print(f'Убрали {AREAS_SQM[idx_max]} м²: coef={best_sub_coef:.2f}, MAE={best_sub_error:.3f}')\n"
            "print(\n"
            "    'На этих данных лучший coef совпал (0.09), но MAE чуть ниже — '\n"
            "    'одна точка влияет на метрику.'\n"
            ")"
        ),
        md("## ДЗ. 4. Сетка intercept × coef"),
        code(
            "grid = []\n"
            "for intercept in [0.5, 1.0, 1.5, 2.0]:\n"
            "    for coef_percent in range(5, 16):\n"
            "        coef = coef_percent / 100\n\n"
            "        def candidate(area_sqm, intercept=intercept, coef=coef):\n"
            "            return predict_price(area_sqm, intercept, coef)\n\n"
            "        preds = batch_predict(AREAS_SQM, candidate)\n"
            "        grid.append((mae(preds, PRICES_MLN), intercept, coef))\n\n"
            "top3 = sorted(grid)[:3]\n"
            "for error, intercept, coef in top3:\n"
            "    print(f'MAE={error:.3f}, intercept={intercept}, coef={coef:.2f}')"
        ),
    ),



}


HOMEWORKS = {
    "lessons/03_parameters_and_return/homework.ipynb": nb(
        md("# Домашнее задание: параметры и return"),
        code(
            "EXAM_SCORES = [40, 55, 62, 75, 88, 91, 48, 100, 33, 67]\n"
            "AREAS_SQM = [28, 32, 45, 55, 60]\n"
            "# Одна «строка» признаков — три числа с одним индексом\n"
            "ROW_AREAS = [28, 45, 60, 32]\n"
            "ROW_ROOMS = [1, 2, 3, 1]\n"
            "ROW_FLOORS = [3, 7, 12, 2]\n"
        ),
        md(
            "## 1. Напоминание с пары\n\n"
            "Скопируйте из `lesson.ipynb` (или напишите заново): "
            "`describe_numbers`, `min_max_scale`, `clip_outlier`, `grade_stats`."
        ),
        code(
            "def describe_numbers(values):\n"
            "    pass\n\n\n"
            "def min_max_scale(values):\n"
            "    pass\n\n\n"
            "def clip_outlier(x, low, high):\n"
            "    pass\n\n\n"
            "def grade_stats(scores, pass_threshold=60):\n"
            "    pass\n"
        ),
        md(
            "## 2. Clip всей выборки\n\n"
            "Напишите `clip_scores(scores, low, high)` — список с clip каждого балла. "
            "Обрежьте `EXAM_SCORES` в [50, 95]. Сравните `mean` до и после (через `describe_numbers`)."
        ),
        code(
            "def clip_scores(scores, low, high):\n"
            "    pass\n\n\n"
            "# before, after, вывод mean\n"
        ),
        md(
            "## 3. Статистика по строке признаков\n\n"
            "`row_numeric_stats(area, rooms, floor)` → `(mean, max)` по трём числам. "
            "Проверьте на `ROW_*[0]`."
        ),
        code(
            "def row_numeric_stats(area, rooms, floor):\n"
            "    pass\n\n\n"
            "# assert на ROW_AREAS[0], ROW_ROOMS[0], ROW_FLOORS[0]\n"
        ),
        md(
            "## 4. Подбор порога\n\n"
            "Переберите `pass_threshold` от 40 до 95. Найдите порог, при котором доля сдавших "
            "ближе всего к 0.5. Запишите порог и долю."
        ),
        code("# перебор; print('лучший порог = ...')\n"),
    ),
    "lessons/04_practice_transform/homework.ipynb": nb(
        md("# Домашнее задание: практика transform"),
        code(
            "LAB_SCORES = [72, 81, 55, 90, 44, 38, 92, 58]\n"
            "# Строка признаков: числа + название района (строка не входит в статистику)\n"
            "FEATURE_ROWS = [\n"
            "    (28, 1, 3, 'north'),\n"
            "    (45, 2, 7, 'center'),\n"
            "    (60, 3, 12, 'south'),\n"
            "    (32, 1, 2, 'west'),\n"
            "]\n"
        ),
        md(
            "## 1. Опора\n\n"
            "Скопируйте с пары 3–4: `describe_numbers`, `min_max_scale`, `clip_outlier`, "
            "`grade_stats`, `apply_transform`."
        ),
        code(
            "# ваши функции\n"
        ),
        md(
            "## 2. `numeric_stats_from_row`\n\n"
            "Для кортежа `row` верните `(mean, max)` только по **числовым** элементам "
            "(подсказка: `isinstance(x, (int, float))`). Проверьте на `FEATURE_ROWS[0]`."
        ),
        code(
            "def numeric_stats_from_row(row):\n"
            "    pass\n\n\n"
            "# assert numeric_stats_from_row(FEATURE_ROWS[0]) == (...)\n"
        ),
        md(
            "## 3. `transform_pipeline`\n\n"
            "Напишите `transform_pipeline(values, *fns)` — последовательно применить все функции. "
            "Сравните `describe_numbers(min_max_scale(LAB_SCORES))` и цепочку "
            "`clip [50,95] → scale` через pipeline (mean до и после в комментарии)."
        ),
        code(
            "def clip_scores(scores, low, high):\n"
            "    pass\n\n\n"
            "def transform_pipeline(values, *fns):\n"
            "    pass\n\n\n"
            "# сравнение mean\n"
        ),
        md(
            "## 4. Обоснование preprocess\n\n"
            "Добавьте **markdown-ячейку** (3–4 предложения): на `LAB_SCORES` что сильнее меняет смысл `mean` — "
            "только `min_max_scale` или сначала clip в [50, 95], потом scale? Опирайтесь на числа из §3."
        ),
    ),
    "lessons/05_scope_and_debugging/homework.ipynb": nb(
        md("# Домашнее задание: scope и отладка"),
        code(
            "PREDICTIONS = [1, 0, 1, 1, 0, 1, 1, 0, 1, 0]\n"
            "LABELS =      [1, 0, 1, 0, 0, 1, 1, 0, 1, 1]\n"
            "SCORES = [72, 55, 88, 44, 61, 90, 77, 48, 83, 58]\n"
        ),
        md(
            "## 1. Опора\n\n"
            "Скопируйте с пары: `my_accuracy`, `count_correct`, `predict_pass`."
        ),
        code("# ваши функции\n"),
        md(
            "## 2. `batch_predict_pass`\n\n"
            "`batch_predict_pass(scores, threshold)` → список 0/1 для каждого балла. "
            "Проверьте длину на `SCORES`."
        ),
        code(
            "def batch_predict_pass(scores, threshold=60):\n"
            "    pass\n\n\n"
            "# assert len(batch_predict_pass(SCORES)) == len(SCORES)\n"
        ),
        md(
            "## 3. Журнал отладки\n\n"
            "Добавьте **markdown-ячейку**: таблица из **двух** багов с пары "
            "(симптом → причина → исправление)."
        ),
        md(
            "## 4. Shadowing\n\n"
            "Исправьте `accuracy_shadow_bug`: переменная `labels` внутри функции "
            "затирает аргумент. Напишите `accuracy_shadow_ok`."
        ),
        code(
            "def accuracy_shadow_bug(preds, labels):\n"
            "    labels = 0\n"
            "    correct = sum(p == labels for p in preds)\n"
            "    return correct / len(preds)\n\n\n"
            "def accuracy_shadow_ok(preds, labels):\n"
            "    pass\n\n\n"
            "# assert abs(accuracy_shadow_ok(PREDICTIONS, LABELS) - 0.7) < 1e-9\n"
        ),
    ),
    "lessons/06_practice_metrics/homework.ipynb": nb(
        md("# Домашнее задание: отладка счётчика"),
        md(
            "## 1. `increment` без global\n\n"
            "Перепишите так, чтобы счётчик передавался аргументом и возвращался новое значение "
            "(как в `homework_counter.py`, но **без** `global`)."
        ),
        code(
            "def increment(counter):\n"
            "    pass\n\n\n"
            "c = 0\n"
            "c = increment(c)\n"
            "c = increment(c)\n"
            "# assert c == 2\n"
        ),
        md("## 2. `reset_and_count`\n\nСумма списка — не забудьте `return`."),
        code(
            "def reset_and_count(items):\n"
            "    total = 0\n"
            "    for x in items:\n"
            "        total += x\n"
            "    pass\n\n\n"
            "# assert reset_and_count([1, 2, 3]) == 6\n"
        ),
        md(
            "## 3. Журнал\n\n"
            "Markdown-ячейка: для **каждой** из двух функций выше — "
            "симптом → причина → исправление (как на паре)."
        ),
        md(
            "## 4. precision и recall (по желанию)\n\n"
            "Из `confusion_counts` с пары: `precision = tp / (tp + fp)`, "
            "`recall = tp / (tp + fn)`. Посчитайте на `PREDICTIONS`/`LABELS`."
        ),
        code(
            "PREDICTIONS = [1, 0, 1, 1, 0, 1, 1, 0, 1, 0]\n"
            "LABELS =      [1, 0, 1, 0, 0, 1, 1, 0, 1, 1]\n"
            "# tp, fp, fn, tn = ...\n"
            "# precision, recall\n"
        ),
    ),
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


# Pair 7 (merged recursion+pipeline): source of truth = ipynb on disk (edit files, then regenerate).
NOTEBOOKS['lessons/07_recursion_pipeline/lesson.ipynb'] = json.loads((ROOT / 'lessons/07_recursion_pipeline/lesson.ipynb').read_text(encoding='utf-8'))
HOMEWORKS['lessons/07_recursion_pipeline/homework.ipynb'] = json.loads((ROOT / 'lessons/07_recursion_pipeline/homework.ipynb').read_text(encoding='utf-8'))
SOLUTIONS['lessons/07_recursion_pipeline/solutions.ipynb'] = json.loads((ROOT / 'lessons/07_recursion_pipeline/solutions.ipynb').read_text(encoding='utf-8'))

if __name__ == "__main__":
    for rel, notebook in NOTEBOOKS.items():
        write(rel, notebook)
    for rel, notebook in HOMEWORKS.items():
        write(rel, notebook)
    for rel, notebook in SOLUTIONS.items():
        write(rel, notebook)
