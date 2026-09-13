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
    "import importlib.util\n"
    "import sys\n"
    "import urllib.request\n"
    "from pathlib import Path\n"
    "\n"
    "_RAW = (\n"
    '    "https://raw.githubusercontent.com/gurovic/letovo-ml-profile/main/"\n'
    '    "modules/08_01_functions_recursion/data/module_datasets.py"\n'
    ")\n"
    "\n"
    "\n"
    "def _import_module_datasets():\n"
    '    for root in (Path("../..").resolve(), Path(".").resolve()):\n'
    '        path = root / "data" / "module_datasets.py"\n'
    "        if path.is_file():\n"
    "            root_s = str(root)\n"
    "            if root_s not in sys.path:\n"
    "                sys.path.insert(0, root_s)\n"
    "            import data.module_datasets as md\n"
    "            return md\n"
    '    dest = Path("module_datasets.py")\n'
    "    urllib.request.urlretrieve(_RAW, dest)\n"
    '    spec = importlib.util.spec_from_file_location("module_datasets", dest)\n'
    "    md = importlib.util.module_from_spec(spec)\n"
    "    spec.loader.exec_module(md)\n"
    "    return md\n"
    "\n"
    "\n"
    "_md = _import_module_datasets()\n"
    "APARTMENTS = _md.APARTMENTS\n"
    "EXAM_SCORES = _md.EXAM_SCORES\n"
    "PREDICTIONS = _md.PREDICTIONS\n"
    "LABELS = _md.LABELS\n"
    "NESTED_API_RESPONSE = _md.NESTED_API_RESPONSE\n"
    "CATEGORY_TREE = _md.CATEGORY_TREE\n"
    "FEATURE_ROWS = _md.FEATURE_ROWS\n"
    "MODEL_RUNS = _md.MODEL_RUNS\n"
    "FEATURE_POINTS = _md.FEATURE_POINTS\n"
    "PRICE_INTERCEPT = _md.PRICE_INTERCEPT\n"
    "PRICE_COEF_AREA = _md.PRICE_COEF_AREA\n"
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
            "Для каждого посчитайте предсказания для всех площадей через `predict_price`, затем MAE. "
            "Сохраните тройку `(MAE, коэффициент, предсказания)`.\n\n"
            "Выберите лучшую тройку. Объясните, почему сравнивать модели по одной квартире ненадёжно."
        ),
        code(
            "results = []\n\n"
            "for coef_percent in range(5, 16):\n"
            "    coef = coef_percent / 100\n"
            "    # predictions = []\n"
            "    # for area in AREAS_SQM:\n"
            "    #     predictions.append(predict_price(area, intercept=1.5, coef=coef))\n"
            "    # error = mae(predictions, PRICES_MLN)\n"
            "    # results.append((error, coef, predictions))\n"
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
        md(
            "# Scope и отладка — accuracy и типы ошибок\n\n"
            "**Пара КТП 5** (2 ч). Метрика — такая же функция, как `predict`: "
            "без `return` и с путаницей в переменных она молча врёт.\n\n"
            "Минимум сдачи: `my_accuracy`, `count_correct`, `predict_pass`, `confusion_counts`."
        ),
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
        md(
            "## 6. Типы ошибок: confusion_counts\n\n"
            "Accuracy — одно число: оно не говорит, **как именно** модель ошибается. "
            "Для меток 0/1 есть четыре случая:\n\n"
            "| Код | pred | label | Смысл |\n"
            "|---|---|---|---|\n"
            "| **tp** | 1 | 1 | верно нашли «1» |\n"
            "| **fp** | 1 | 0 | ложная тревога |\n"
            "| **fn** | 0 | 1 | пропустили «1» |\n"
            "| **tn** | 0 | 0 | верно отвергли |\n\n"
            "Напишите `confusion_counts(preds, labels)` — один проход по индексам, "
            "четыре счётчика, `return` кортежа `(tp, fp, fn, tn)`. **Без** `global`."
        ),
        code(
            "def confusion_counts(preds, labels):\n"
            '    """Вернуть (tp, fp, fn, tn) для меток 0/1."""\n'
            "    pass\n\n\n"
            "tp, fp, fn, tn = confusion_counts(PREDICTIONS, LABELS)\n"
            "assert tp + fp + fn + tn == len(PREDICTIONS)\n"
            "assert tp + tn == count_correct(PREDICTIONS, LABELS)\n"
            "print('tp fp fn tn =', tp, fp, fn, tn)"
        ),
        md(
            "## 7. Сверка вручную\n\n"
            "На **первых 4** объектах (`PREDICTIONS[:4]`, `LABELS[:4]`) посчитайте tp, fp, fn, tn "
            "**на бумаге**, впишите в `assert` и только потом запустите ячейку."
        ),
        code(
            "manual = confusion_counts(PREDICTIONS[:4], LABELS[:4])\n"
            "print('функция на первых 4:', manual)\n"
            "# assert manual == (..., ..., ..., ...)"
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
            "def transform_pipeline(values, fn1, fn2=None, fn3=None):\n"
            "    result = fn1(values)\n"
            "    if fn2 is not None:\n"
            "        result = fn2(result)\n"
            "    if fn3 is not None:\n"
            "        result = fn3(result)\n"
            "    return result\n\n\n"
            "def clip_lab(scores):\n"
            "    return clip_scores(scores, 50, 95)\n\n\n"
            "only_scale = describe_numbers(min_max_scale(LAB_SCORES))[0]\n"
            "clip_then_scale = describe_numbers(\n"
            "    transform_pipeline(LAB_SCORES, clip_lab, min_max_scale)\n"
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
            "assert count_correct(PREDICTIONS, LABELS) == 8"
        ),
        md("## Урок. 5. predict_pass"),
        code(
            "def predict_pass(score, threshold=60):\n"
            "    return 1 if score >= threshold else 0\n\n\n"
            "assert predict_pass(72) == 1"
        ),
        md(
            "## Урок. 6–7. confusion_counts\n\n"
            "На всех 10 объектах: `(5, 1, 1, 3)`; на первых 4: `(2, 1, 0, 1)`. "
            "Проверка: `tp + tn == count_correct == 8`."
        ),
        code(
            "def confusion_counts(preds, labels):\n"
            "    tp = 0\n"
            "    fp = 0\n"
            "    fn = 0\n"
            "    tn = 0\n"
            "    for i in range(len(preds)):\n"
            "        p = preds[i]\n"
            "        y = labels[i]\n"
            "        if p == 1 and y == 1:\n"
            "            tp += 1\n"
            "        elif p == 1 and y == 0:\n"
            "            fp += 1\n"
            "        elif p == 0 and y == 1:\n"
            "            fn += 1\n"
            "        else:\n"
            "            tn += 1\n"
            "    return tp, fp, fn, tn\n\n\n"
            "assert confusion_counts(PREDICTIONS, LABELS) == (5, 1, 1, 3)\n"
            "assert confusion_counts(PREDICTIONS[:4], LABELS[:4]) == (2, 1, 0, 1)"
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
        md(
            "## ДЗ. 5. precision и recall (по желанию)\n\n"
            "precision = 5 / (5 + 1) ≈ 0.833; recall = 5 / (5 + 1) ≈ 0.833. "
            "При нулевом знаменателе договариваемся возвращать `None`."
        ),
        code(
            "def precision(tp, fp):\n"
            "    if tp + fp == 0:\n"
            "        return None\n"
            "    return tp / (tp + fp)\n\n\n"
            "def recall(tp, fn):\n"
            "    if tp + fn == 0:\n"
            "        return None\n"
            "    return tp / (tp + fn)\n\n\n"
            "tp, fp, fn, tn = confusion_counts(PREDICTIONS, LABELS)\n"
            "assert abs(precision(tp, fp) - 5 / 6) < 1e-9\n"
            "assert abs(recall(tp, fn) - 5 / 6) < 1e-9"
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
            "printed = predict_print(45)\n"
            "if printed is None:\n"
            "    print('ошибка: print не возвращает значение (None)')\n"
            "else:\n"
            "    print(printed + 1)\n\n"
            "print('predict_return(45) + 1 =', predict_return(45) + 1)"
        ),
        md("## Урок. 3. `batch_predict`"),
        code(
            "def batch_predict(values, predict_fn):\n"
            "    preds = []\n"
            "    for v in values:\n"
            "        preds.append(predict_fn(v))\n"
            "    return preds\n\n\n"
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
        md("## Урок. 5. Выбор коэффициента"),
        code(
            "results = []\n\n"
            "for coef_percent in range(5, 16):\n"
            "    coef = coef_percent / 100\n"
            "    predictions = []\n"
            "    for area in AREAS_SQM:\n"
            "        predictions.append(predict_price(area, intercept=1.5, coef=coef))\n"
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
            "idx_max = 0\n"
            "for i in range(1, len(AREAS_SQM)):\n"
            "    if AREAS_SQM[i] > AREAS_SQM[idx_max]:\n"
            "        idx_max = i\n\n"
            "areas_sub = []\n"
            "prices_sub = []\n"
            "for i in range(len(AREAS_SQM)):\n"
            "    if i != idx_max:\n"
            "        areas_sub.append(AREAS_SQM[i])\n"
            "        prices_sub.append(PRICES_MLN[i])\n\n"
            "sub_results = []\n"
            "for coef_percent in range(5, 16):\n"
            "    coef = coef_percent / 100\n"
            "    predictions = []\n"
            "    for a in areas_sub:\n"
            "        predictions.append(predict_price(a, intercept=1.5, coef=coef))\n"
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
            "        coef = coef_percent / 100\n"
            "        preds = []\n"
            "        for a in AREAS_SQM:\n"
            "            preds.append(predict_price(a, intercept=intercept, coef=coef))\n"
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
            "Напишите `transform_pipeline(values, fn1, fn2=None, fn3=None)` — последовательно применить функции. "
            "Сравните `describe_numbers(min_max_scale(LAB_SCORES))` и цепочку "
            "`clip [50,95] → scale` через pipeline (mean до и после в комментарии)."
        ),
        code(
            "def clip_scores(scores, low, high):\n"
            "    pass\n\n\n"
            "def transform_pipeline(values, fn1, fn2=None, fn3=None):\n"
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
            "# assert abs(accuracy_shadow_ok(PREDICTIONS, LABELS) - 0.8) < 1e-9\n"
        ),
        md(
            "## 5. precision и recall (по желанию)\n\n"
            "Из `confusion_counts` с пары: `precision = tp / (tp + fp)` — какая доля наших «1» "
            "оказалась верной; `recall = tp / (tp + fn)` — какую долю настоящих «1» мы нашли. "
            "Напишите две функции; если знаменатель 0 — верните `None`."
        ),
        code(
            "def precision(tp, fp):\n"
            "    pass\n\n\n"
            "def recall(tp, fn):\n"
            "    pass\n\n\n"
            "# tp, fp, fn, tn = confusion_counts(PREDICTIONS, LABELS)\n"
            "# print(precision(tp, fp), recall(tp, fn))\n"
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


# ---------------------------------------------------------------------------
# Pair 7: modules, import, command line, .py vs .ipynb
# Files are created from Colab cells via %%writefile and run via !python.
# ---------------------------------------------------------------------------

L06_DATA = (
    "# Те же данные, что на паре 5\n"
    "PREDICTIONS = [1, 0, 1, 1, 0, 1, 1, 0, 1, 0]\n"
    "LABELS =      [1, 0, 1, 0, 0, 1, 1, 0, 1, 1]\n"
)

L06_HOWTO = (
    "**Как работать в этом ноутбуке**\n\n"
    "| Ячейка начинается с | Что это |\n"
    "|---|---|\n"
    "| `%%writefile имя.py` | сохранить текст ячейки в файл `имя.py` (сама ячейка не выполняется как код) |\n"
    "| `!python имя.py` | команда **терминала**: запустить файл заново, в отдельном процессе |\n"
    "| `!ls` | команда терминала: показать файлы в папке |\n\n"
    "Если у вас Python и терминал на компьютере — делайте то же в одной папке: "
    "файл в редакторе, команды в терминале **без** `!` (в Windows иногда `py` вместо `python`)."
)

L06_METRICS_STUB = (
    '"""metrics — метрики классификации на списках 0/1 (пара 5)."""\n\n\n'
    "def my_accuracy(preds, labels):\n"
    '    """Доля верных предсказаний или None при разной длине."""\n'
    "    pass\n\n\n"
    "def confusion_counts(preds, labels):\n"
    '    """(tp, fp, fn, tn) для меток 0/1."""\n'
    "    pass\n"
)

L06_METRICS_FULL = (
    '"""metrics — метрики классификации на списках 0/1 (пара 5)."""\n\n\n'
    "def my_accuracy(preds, labels):\n"
    '    """Доля верных предсказаний или None при разной длине."""\n'
    "    if len(preds) != len(labels):\n"
    "        return None\n"
    "    if not preds:\n"
    "        return 0.0\n"
    "    correct = 0\n"
    "    for i in range(len(preds)):\n"
    "        if preds[i] == labels[i]:\n"
    "            correct += 1\n"
    "    return correct / len(preds)\n\n\n"
    "def confusion_counts(preds, labels):\n"
    '    """(tp, fp, fn, tn) для меток 0/1."""\n'
    "    tp = 0\n"
    "    fp = 0\n"
    "    fn = 0\n"
    "    tn = 0\n"
    "    for i in range(len(preds)):\n"
    "        p = preds[i]\n"
    "        y = labels[i]\n"
    "        if p == 1 and y == 1:\n"
    "            tp += 1\n"
    "        elif p == 1 and y == 0:\n"
    "            fp += 1\n"
    "        elif p == 0 and y == 1:\n"
    "            fn += 1\n"
    "        else:\n"
    "            tn += 1\n"
    "    return (tp, fp, fn, tn)\n"
)

L06_SELFCHECK = (
    "\n\nif __name__ == \"__main__\":\n"
    "    # выполняется только при запуске: python metrics.py\n"
    "    print(\"self-check:\", my_accuracy([1, 0], [1, 1]))\n"
)

L06_MAIN = (
    '"""Отчёт по метрикам. Запуск: python main.py"""\n\n'
    "from metrics import my_accuracy, confusion_counts\n\n"
    "PREDICTIONS = [1, 0, 1, 1, 0, 1, 1, 0, 1, 0]\n"
    "LABELS = [1, 0, 1, 0, 0, 1, 1, 0, 1, 1]\n\n"
    "acc = my_accuracy(PREDICTIONS, LABELS)\n"
    "tp, fp, fn, tn = confusion_counts(PREDICTIONS, LABELS)\n"
    'print("accuracy:", acc)\n'
    'print("tp fp fn tn:", tp, fp, fn, tn)\n'
)

L06_TESTS = (
    '"""Тесты модуля metrics. Запуск: python manual_tests.py"""\n\n'
    "from metrics import my_accuracy, confusion_counts\n\n"
    "PREDICTIONS = [1, 0, 1, 1, 0, 1, 1, 0, 1, 0]\n"
    "LABELS = [1, 0, 1, 0, 0, 1, 1, 0, 1, 1]\n\n"
    'assert abs(my_accuracy(PREDICTIONS, LABELS) - 0.8) < 1e-9, "accuracy на 10 объектах"\n'
    'assert my_accuracy([1], [1, 0]) is None, "разная длина → None"\n'
    'assert confusion_counts(PREDICTIONS, LABELS) == (5, 1, 1, 3), "tp fp fn tn"\n'
    'assert sum(confusion_counts(PREDICTIONS, LABELS)) == len(PREDICTIONS), "сумма = число объектов"\n'
    'print("All tests passed")\n'
)

L06_PREDICT_STUB = (
    '"""Запуск: python predict.py БАЛЛ ПОРОГ  → печатает 1 (сдал) или 0"""\n\n'
    "import sys\n\n"
    'print("argv:", sys.argv)  # посмотрите, что здесь, и удалите строку\n\n\n'
    "def predict_pass(score, threshold):\n"
    "    pass\n\n\n"
    "score = None      # int(sys.argv[1])\n"
    "threshold = None  # int(sys.argv[2])\n"
    "print(predict_pass(score, threshold))\n"
)

L06_PREDICT_FULL = (
    '"""Запуск: python predict.py БАЛЛ [ПОРОГ]  → печатает 1 (сдал) или 0"""\n\n'
    "import sys\n\n\n"
    "def predict_pass(score, threshold):\n"
    "    if score >= threshold:\n"
    "        return 1\n"
    "    return 0\n\n\n"
    "if len(sys.argv) < 2:\n"
    '    print("использование: python predict.py БАЛЛ [ПОРОГ]")\n'
    "    sys.exit(1)\n\n"
    "score = int(sys.argv[1])\n"
    "threshold = 60\n"
    "if len(sys.argv) >= 3:\n"
    "    threshold = int(sys.argv[2])\n"
    "print(predict_pass(score, threshold))\n"
)

L06_DATASETS_IMPORT = (
    "import urllib.request\n\n"
    "urllib.request.urlretrieve(\n"
    '    "https://raw.githubusercontent.com/gurovic/letovo-ml-profile/main/"\n'
    '    "modules/08_01_functions_recursion/data/module_datasets.py",\n'
    '    "module_datasets.py",\n'
    ")\n\n"
    "from module_datasets import PREDICTIONS as P_DATA, LABELS as L_DATA\n\n"
    'print("объектов в датасете модуля:", len(P_DATA), len(L_DATA))\n'
)

# ---- homework files ----

HW06_STATS_STUB = (
    '"""stats_tools — описание и масштабирование списка чисел (пара 3)."""\n\n\n'
    "def describe_numbers(values):\n"
    '    """Вернуть (mean, min, max, count)."""\n'
    "    pass\n\n\n"
    "def min_max_scale(values):\n"
    '    """Min-max scaling списка чисел → список от 0 до 1."""\n'
    "    pass\n"
)

HW06_STATS_FULL = (
    '"""stats_tools — описание и масштабирование списка чисел (пара 3)."""\n\n\n'
    "def describe_numbers(values):\n"
    '    """Вернуть (mean, min, max, count)."""\n'
    "    if not values:\n"
    "        return (0.0, 0.0, 0.0, 0)\n"
    "    return (sum(values) / len(values), min(values), max(values), len(values))\n\n\n"
    "def min_max_scale(values):\n"
    '    """Min-max scaling списка чисел → список от 0 до 1."""\n'
    "    if not values:\n"
    "        return []\n"
    "    lo = min(values)\n"
    "    hi = max(values)\n"
    "    if lo == hi:\n"
    "        return [0.0] * len(values)\n"
    "    result = []\n"
    "    for x in values:\n"
    "        result.append((x - lo) / (hi - lo))\n"
    "    return result\n"
)

HW06_STATS_TESTS = (
    '"""Запуск: python manual_tests.py"""\n\n'
    "from stats_tools import describe_numbers, min_max_scale\n\n"
    "EXAM_SCORES = [40, 55, 62, 75, 88, 91, 48, 100, 33, 67]\n\n"
    'assert describe_numbers([10, 20, 30]) == (20, 10, 30, 3), "describe на трёх числах"\n'
    'assert describe_numbers(EXAM_SCORES)[3] == 10, "count = 10"\n'
    "scaled = min_max_scale(EXAM_SCORES)\n"
    'assert abs(min(scaled) - 0) < 1e-9 and abs(max(scaled) - 1) < 1e-9, "границы 0 и 1"\n'
    'print("All tests passed")\n'
)

HW06_DESCRIBE_CLI = (
    '"""Запуск: python describe.py 40 55 62 75"""\n\n'
    "import sys\n\n"
    "from stats_tools import describe_numbers\n\n"
    "values = []\n"
    "for text in sys.argv[1:]:\n"
    "    values.append(float(text))\n\n"
    "if not values:\n"
    '    print("использование: python describe.py ЧИСЛО ЧИСЛО ...")\n'
    "    sys.exit(1)\n\n"
    "mean, lo, hi, count = describe_numbers(values)\n"
    'print("count", count)\n'
    'print("min", lo)\n'
    'print("max", hi)\n'
    'print("mean", mean)\n'
)

HW06_NOISY = (
    '"""noisy — модуль, который шумит при импорте (исправить)."""\n\n\n'
    "def clip(x, low, high):\n"
    "    return max(low, min(high, x))\n\n\n"
    'print("проверка clip:", clip(150, 0, 100))\n'
    'print("проверка clip:", clip(-5, 0, 100))\n'
)

HW06_NOISY_FIXED = (
    '"""noisy — модуль с демонстрацией только при прямом запуске."""\n\n\n'
    "def clip(x, low, high):\n"
    "    return max(low, min(high, x))\n\n\n"
    'if __name__ == "__main__":\n'
    '    print("проверка clip:", clip(150, 0, 100))\n'
    '    print("проверка clip:", clip(-5, 0, 100))\n'
)

HW06_REPORT = (
    '"""Отчёт из двух своих модулей. Запуск: python report.py"""\n\n'
    "from stats_tools import describe_numbers\n"
    "from metrics import my_accuracy\n\n"
    "SCORES = [72, 55, 88, 44, 61, 90, 77, 48, 83, 58]\n"
    "PREDICTIONS = [1, 0, 1, 1, 0, 1, 1, 0, 1, 0]\n"
    "LABELS = [1, 0, 1, 0, 0, 1, 1, 0, 1, 1]\n\n"
    "mean, lo, hi, count = describe_numbers(SCORES)\n"
    'print("баллы: count", count, "min", lo, "max", hi, "mean", mean)\n'
    'print("accuracy:", my_accuracy(PREDICTIONS, LABELS))\n'
)


def wf(name: str, body: str):
    """Code cell that writes `body` into file `name` (Colab %%writefile)."""
    return code(f"%%writefile {name}\n{body}")


NOTEBOOKS["lessons/06_modules_cli/lesson.ipynb"] = nb(
    md(
        "# Модули и импорт: код в `.py`, запуск из командной строки\n\n"
        "**Пара КТП 6** (2 ч). До сих пор функции жили в ячейках ноутбука. "
        "Сегодня они переезжают в **файл-модуль**, который можно импортировать, "
        "запускать из командной строки и проверять отдельным файлом тестов.\n\n"
        "Минимум сдачи: `hello.py`, `metrics.py`, `main.py`, `predict.py`, `manual_tests.py` — "
        "все запускаются командой `python имя.py`."
    ),
    md(L06_HOWTO),
    code(L06_DATA),
    md(
        "## 1. Файл .py и ноутбук .ipynb\n\n"
        "Ноутбук `.ipynb` — это **JSON**: список ячеек с кодом, текстом и сохранёнными выводами. "
        "Примерно так выглядит одна ячейка внутри файла:\n\n"
        "```json\n"
        '{"cell_type": "code", "source": ["print(1 + 1)"], "outputs": [{"text": ["2\\n"]}]}\n'
        "```\n\n"
        "Файл `.py` — **только код**, обычный текст. Python читает его сверху вниз и выполняет. "
        "Такой файл называют **программой** (если его запускают) или **модулем** (если его импортируют).\n\n"
        "Создайте файл и запустите его."
    ),
    wf("hello.py", 'print("hello from file")\n'),
    code("!python hello.py"),
    code("# какие файлы появились в папке?\n!ls"),
    md(
        "**Задание.** Поменяйте текст в `hello.py`, запустите ячейку с `%%writefile` ещё раз, потом — `!python hello.py`. "
        "Что будет, если запустить только `!python hello.py`, не пересохранив файл?"
    ),
    md(
        "## 2. Модуль metrics.py\n\n"
        "**Модуль** — файл с функциями. Имя модуля = имя файла без `.py`.\n\n"
        "Перенесите в файл ниже **свои** `my_accuracy` и `confusion_counts` с пары 5 (вместо `pass`)."
    ),
    wf("metrics.py", L06_METRICS_STUB),
    code(
        "import metrics\n\n"
        "acc = metrics.my_accuracy(PREDICTIONS, LABELS)\n"
        "print(acc)\n"
        "assert abs(acc - 0.8) < 1e-9\n"
    ),
    code(
        "from metrics import confusion_counts\n\n"
        "tp, fp, fn, tn = confusion_counts(PREDICTIONS, LABELS)\n"
        "print(tp, fp, fn, tn)\n"
        "assert (tp, fp, fn, tn) == (5, 1, 1, 3)\n"
    ),
    md(
        "**Ловушка.** Модуль загружается в память **один раз** на процесс. "
        "Если вы исправили `metrics.py`, а `import metrics` в ноутбуке по-прежнему возвращает старое — "
        "перезагрузите модуль ячейкой ниже. Команда `!python main.py` этой проблемы не имеет: "
        "каждый запуск — новый процесс, файл читается заново."
    ),
    code("import importlib\n\nimportlib.reload(metrics)\nprint(metrics.my_accuracy(PREDICTIONS, LABELS))"),
    md(
        "## 3. Программа main.py\n\n"
        "Программа импортирует модуль и печатает отчёт. Данные пока внутри программы."
    ),
    wf("main.py", L06_MAIN),
    code("!python main.py"),
    md(
        "### Эксперимент: код верхнего уровня\n\n"
        "Допишите в **конец** `metrics.py` строку\n\n"
        "```python\n"
        'print("self-check:", my_accuracy([1, 0], [1, 1]))\n'
        "```\n\n"
        "и снова выполните `!python main.py`. Откуда взялась лишняя строка?\n\n"
        "Всё, что в файле **не внутри функций**, выполняется при импорте. "
        "Чтобы проверка работала только при прямом запуске `python metrics.py`, "
        "её прячут под условие `if __name__ == \"__main__\":`. Переменная `__name__` равна "
        "`\"__main__\"`, когда файл запустили как программу, и равна имени модуля (`\"metrics\"`), когда его импортировали.\n\n"
        "Перепишите `metrics.py`: ваши функции + self-check под условием."
    ),
    wf("metrics.py", L06_METRICS_STUB + L06_SELFCHECK),
    code("# прямой запуск: self-check печатается\n!python metrics.py"),
    code("# импорт из программы: self-check молчит\n!python main.py"),
    md(
        "## 4. Аргументы командной строки\n\n"
        "`sys.argv` — список **строк** из командной строки. `sys.argv[0]` — имя файла, дальше — аргументы.\n\n"
        "Напишите `predict.py`: `python predict.py 72 60` печатает `1` (72 ≥ 60), `python predict.py 44 60` — `0`."
    ),
    wf("predict.py", L06_PREDICT_STUB),
    code("!python predict.py 72 60"),
    code("!python predict.py 44 60"),
    md(
        "**Задание.** Запустите `!python predict.py` без аргументов. Какая ошибка? "
        "Сделайте порог необязательным: если его нет — использовать `60`; если нет и балла — напечатать подсказку «использование: …»."
    ),
    code("!python predict.py\n!python predict.py 72"),
    md(
        "## 5. Файл тестов\n\n"
        "Тесты — отдельный файл, который **импортирует** модуль и проверяет его через `assert`. "
        "Последняя строка печатается, только если все проверки прошли."
    ),
    wf("manual_tests.py", L06_TESTS),
    code("!python manual_tests.py"),
    md(
        "### Сломайте и прочитайте traceback\n\n"
        "В `metrics.py` поменяйте местами `fp` и `fn` в `return` (пересохраните файл) и запустите тесты ещё раз.\n\n"
        "Traceback читают **снизу вверх**: последняя строка — тип ошибки и сообщение; выше — `File \"...\", line N` — "
        "файл и строка, где упала проверка.\n\n"
        "Запишите в ячейку ниже: какой файл, какая строка, какое сообщение. Потом верните `metrics.py` в порядок."
    ),
    md("**Ответ:** файл … , строка … , сообщение … "),
    code("# после исправления снова должно быть All tests passed\n!python manual_tests.py"),
    md(
        "## 6. Данные — тоже модуль\n\n"
        "`data/module_datasets.py` из репозитория курса — обычный модуль с константами. "
        "Скачаем файл рядом и импортируем из него данные."
    ),
    code(L06_DATASETS_IMPORT),
    code("!ls"),
    md(
        "### Мост к паре 8\n\n"
        "Стартовый код артефакта устроен точно так же, как ваша папка сейчас:\n\n"
        "```text\n"
        "text_stats_starter/\n"
        "  text_stats.py        ← модуль с функциями (как metrics.py)\n"
        "  manual_tests.py      ← тесты, запуск: python manual_tests.py\n"
        "  data/\n"
        "    module_datasets.py ← данные-модуль\n"
        "```\n\n"
        "Домашнее задание — [homework.ipynb](homework.ipynb): та же структура на функциях пары 3."
    ),
    md(
        "## Итог\n\n"
        "| Понятие | Что запомнить |\n"
        "|---|---|\n"
        "| `.py` vs `.ipynb` | код-текст vs JSON с ячейками и выводами |\n"
        "| модуль | файл с функциями; `import metrics`, `from metrics import f` |\n"
        "| `python file.py` | новый процесс, файл читается заново |\n"
        "| `if __name__ == \"__main__\":` | код только при прямом запуске |\n"
        "| `sys.argv` | аргументы — список строк |\n"
        "| `manual_tests.py` | отдельный файл с `assert` |"
    ),
)

HOMEWORKS["lessons/06_modules_cli/homework.ipynb"] = nb(
    md(
        "# Домашнее задание: свой модуль, тесты и программа с аргументами\n\n"
        "~1 час. Та же структура, что на паре: модуль → тесты → программа. "
        "Уровни A–B обязательны, C–D — по силам.\n\n"
        "Сдаётся этот ноутбук с выполненными ячейками `!python …` "
        "(или папка с файлами, если работали локально)."
    ),
    md(L06_HOWTO),
    md(
        "## 1. Модуль `stats_tools.py` (A)\n\n"
        "Перенесите **свои** `describe_numbers` и `min_max_scale` с пары 3 в файл."
    ),
    wf("stats_tools.py", HW06_STATS_STUB),
    code(
        "from stats_tools import describe_numbers, min_max_scale\n\n"
        "print(describe_numbers([10, 20, 30]))\n"
        "print(min_max_scale([10, 20, 30]))\n"
    ),
    md(
        "## 2. Тесты `manual_tests.py` (A)\n\n"
        "Файл тестов импортирует модуль. Допишите **ещё один** `assert` на `min_max_scale` "
        "(например, для списка из одинаковых чисел)."
    ),
    wf("manual_tests.py", HW06_STATS_TESTS),
    code("!python manual_tests.py"),
    md(
        "## 3. Программа `describe.py` с аргументами (B)\n\n"
        "`python describe.py 40 55 62 75` печатает count, min, max, mean. "
        "Все аргументы `sys.argv[1:]` — строки: превратите их в числа. "
        "Без аргументов — подсказка «использование: …»."
    ),
    wf(
        "describe.py",
        '"""Запуск: python describe.py 40 55 62 75"""\n\n'
        "import sys\n\n"
        "from stats_tools import describe_numbers\n\n"
        "values = []\n"
        "# for text in sys.argv[1:]: ...\n\n"
        "# mean, lo, hi, count = describe_numbers(values)\n"
        "# print(...)\n",
    ),
    code("!python describe.py 40 55 62 75"),
    code("!python describe.py"),
    md(
        "## 4. Модуль, который шумит при импорте (C)\n\n"
        "Файл `noisy.py` печатает две строки при каждом `import noisy`. "
        "Исправьте так, чтобы `import noisy` молчал, а `python noisy.py` по-прежнему показывал проверку. "
        "Объясните в одном предложении, почему печать срабатывала."
    ),
    wf("noisy.py", HW06_NOISY),
    code("import noisy\n\nprint(noisy.clip(150, 0, 100))"),
    code("!python noisy.py"),
    md("**Почему печатало при импорте:** …"),
    md(
        "## 5. Отчёт из двух модулей (D)\n\n"
        "Скопируйте свой `metrics.py` с пары (ячейка ниже) и напишите `report.py`, "
        "который импортирует **оба** модуля — `stats_tools` и `metrics` — и печатает: "
        "описание списка баллов и accuracy предсказаний.\n\n"
        "Затем выполните `!ls __pycache__` и напишите 1–2 предложения: что это за папка и можно ли её удалить."
    ),
    wf("metrics.py", L06_METRICS_STUB),
    wf(
        "report.py",
        '"""Отчёт из двух своих модулей. Запуск: python report.py"""\n\n'
        "# from stats_tools import describe_numbers\n"
        "# from metrics import my_accuracy\n\n"
        "SCORES = [72, 55, 88, 44, 61, 90, 77, 48, 83, 58]\n"
        "PREDICTIONS = [1, 0, 1, 1, 0, 1, 1, 0, 1, 0]\n"
        "LABELS = [1, 0, 1, 0, 0, 1, 1, 0, 1, 1]\n",
    ),
    code("!python report.py"),
    code("!ls __pycache__"),
    md("**`__pycache__` — это:** …"),
)

SOLUTIONS["lessons/06_modules_cli/solutions.ipynb"] = nb(
    md(
        "# Решения: модули и импорт (пара 6)\n\n"
        "Только для преподавателя. Урок и ДЗ. Файлы создаются через `%%writefile`, запуск — `!python`."
    ),
    code(L06_DATA),
    md("## Урок. 1. hello.py"),
    wf("hello.py", 'print("hello from file")\n'),
    code("!python hello.py"),
    md(
        "Без повторного `%%writefile` запуск `!python hello.py` печатает **старый** текст: "
        "файл на диске не изменился."
    ),
    md("## Урок. 2–3. metrics.py (с self-check под `__main__`)"),
    wf("metrics.py", L06_METRICS_FULL + L06_SELFCHECK),
    code(
        "import metrics\n\n"
        "assert abs(metrics.my_accuracy(PREDICTIONS, LABELS) - 0.8) < 1e-9\n"
        "assert metrics.confusion_counts(PREDICTIONS, LABELS) == (5, 1, 1, 3)\n"
        "print(metrics.my_accuracy(PREDICTIONS, LABELS), metrics.confusion_counts(PREDICTIONS, LABELS))\n"
    ),
    wf("main.py", L06_MAIN),
    code("!python metrics.py\n!python main.py"),
    md(
        "Ожидаемо: `python metrics.py` печатает `self-check: 0.5`; `python main.py` — только accuracy и счётчики."
    ),
    md("## Урок. 4. predict.py (с необязательным порогом и подсказкой)"),
    wf("predict.py", L06_PREDICT_FULL),
    code("!python predict.py 72 60\n!python predict.py 44 60\n!python predict.py 72\n!python predict.py"),
    md(
        "Без проверки `len(sys.argv)` запуск без аргументов даёт `IndexError: list index out of range` "
        "на `sys.argv[1]`. Сравнение строки с числом (`\"72\" >= 60`) — `TypeError`."
    ),
    md("## Урок. 5. manual_tests.py и traceback"),
    wf("manual_tests.py", L06_TESTS),
    code("!python manual_tests.py"),
    md(
        "Если поменять `fp` и `fn` местами, падает третья проверка:\n\n"
        "```text\n"
        'Traceback (most recent call last):\n'
        '  File "manual_tests.py", line 10, in <module>\n'
        '    assert confusion_counts(PREDICTIONS, LABELS) == (5, 1, 1, 3), "tp fp fn tn"\n'
        "AssertionError: tp fp fn tn\n"
        "```\n\n"
        "Здесь fp = fn = 1, поэтому подмена **не** ломает тест на этих данных — хороший повод обсудить, "
        "почему тестовые данные должны различать случаи. Сильным: поменять `LABELS` так, чтобы fp ≠ fn, "
        "или сломать `tn`."
    ),
    md("## Урок. 6. Данные как модуль"),
    code(L06_DATASETS_IMPORT),
    md("---\n\n# Домашнее задание"),
    md("## ДЗ 1–2. stats_tools.py и тесты"),
    wf("stats_tools.py", HW06_STATS_FULL),
    wf(
        "manual_tests.py",
        HW06_STATS_TESTS.replace(
            'print("All tests passed")\n',
            'assert min_max_scale([5, 5, 5]) == [0.0, 0.0, 0.0], "одинаковые числа → нули"\n'
            'print("All tests passed")\n',
        ),
    ),
    code("!python manual_tests.py"),
    md("## ДЗ 3. describe.py"),
    wf("describe.py", HW06_DESCRIBE_CLI),
    code("!python describe.py 40 55 62 75\n!python describe.py"),
    md("## ДЗ 4. noisy.py"),
    wf("noisy.py", HW06_NOISY_FIXED),
    code("import importlib\nimport noisy\n\nimportlib.reload(noisy)\nprint(noisy.clip(150, 0, 100))"),
    code("!python noisy.py"),
    md(
        "Печатало при импорте, потому что `print(...)` стоял на верхнем уровне файла: "
        "при `import` выполняется весь файл, не только `def`."
    ),
    md("## ДЗ 5. report.py и `__pycache__`"),
    wf("metrics.py", L06_METRICS_FULL),
    wf("report.py", HW06_REPORT),
    code("!python report.py\n!ls __pycache__"),
    md(
        "`__pycache__` — папка с байткодом (`*.pyc`), который Python сохраняет после импорта модуля, "
        "чтобы в следующий раз загружать быстрее. Её можно удалить: при следующем импорте она создастся заново. "
        "В git её не коммитят."
    ),
)

if __name__ == "__main__":
    import sys

    # Optional filters: substrings of the lesson path (e.g. `05_scope 06_modules`).
    only = sys.argv[1:]
    for table in (NOTEBOOKS, HOMEWORKS, SOLUTIONS):
        for rel, notebook in table.items():
            if only and not any(part in rel for part in only):
                continue
            write(rel, notebook)
