#!/usr/bin/env python3
"""Generate lesson notebooks for module 08_07 (KTP pairs 42-48)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
CSV_UNSORTED = DATA_DIR / "bank_transactions_unsorted.csv"
CSV_BY_ID = DATA_DIR / "bank_transactions_sorted_by_txn_id.csv"
CSV_BY_AMOUNT = DATA_DIR / "bank_transactions_sorted_by_amount.csv"
CSV_TINY = DATA_DIR / "bank_transactions_tiny.csv"

SOL_BANNER = (
    "**Для преподавателя.** Эталон к `lesson.ipynb` и `homework.ipynb`. "
    "Не показывать ученикам до сдачи."
)

LOAD_DATA = (
    "from pathlib import Path\n"
    "import time\n"
    "import pandas as pd\n\n\n"
    "def _find(name: str) -> Path:\n"
    "    for p in (Path(name), Path(f'../../data/{name}'), Path(f'../data/{name}')):\n"
    "        if p.exists():\n"
    "            return p.resolve()\n"
    "    raise FileNotFoundError(f'{name} не найден рядом с ноутбуком')\n\n\n"
    "unsorted_df = pd.read_csv(_find('bank_transactions_unsorted.csv'))\n"
    "by_id_df = pd.read_csv(_find('bank_transactions_sorted_by_txn_id.csv'))\n"
    "by_amount_df = pd.read_csv(_find('bank_transactions_sorted_by_amount.csv'))\n"
    "tiny_df = pd.read_csv(_find('bank_transactions_tiny.csv'))\n\n"
    "unsorted_txns = list(unsorted_df[['txn_id', 'amount', 'day', 'risk_score']].itertuples(index=False, name=None))\n"
    "id_txns = list(by_id_df[['txn_id', 'amount', 'day', 'risk_score']].itertuples(index=False, name=None))\n"
    "amount_txns = list(by_amount_df[['txn_id', 'amount', 'day', 'risk_score']].itertuples(index=False, name=None))\n"
    "id_list = [t[0] for t in id_txns]\n"
    "amount_list = [t[1] for t in amount_txns]\n"
)


def md(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "source": source.splitlines(keepends=True),
        "outputs": [],
        "execution_count": None,
    }


def nb(*cells: dict) -> dict:
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": list(cells),
    }


def write(rel_path: str, notebook: dict) -> None:
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", path)


def copy_data(lesson_dir: str) -> None:
    dest_dir = ROOT / lesson_dir
    dest_dir.mkdir(parents=True, exist_ok=True)
    for src in (CSV_UNSORTED, CSV_BY_ID, CSV_BY_AMOUNT, CSV_TINY):
        dest = dest_dir / src.name
        shutil.copy2(src, dest)
        print("copied", src.name, "->", dest)


NOTEBOOKS: dict[str, dict] = {}
LESSON_DIRS = [
    "lessons/01_linear_binary_search",
    "lessons/02_practice_search_logs",
    "lessons/03_selection_merge_quick",
    "lessons/04_practice_sorts",
    "lessons/05_sorted_key_two_pointers",
    "lessons/06_practice_keys_pointers",
    "lessons/07_complexity_integration",
]


def add_lesson01() -> None:
    base = "lessons/01_linear_binary_search"
    lesson = nb(
        md("# Линейный и бинарный поиск в логах банка"),
        code(LOAD_DATA),
        md("## 1. Линейный поиск по `txn_id` в неотсортированном списке"),
        code(
            "def linear_search_txn(txns, target_id):\n"
            "    # вернуть индекс или -1\n"
            "    return None\n\n\n"
            "probe_id = unsorted_txns[25][0]\n"
            "idx = linear_search_txn(unsorted_txns, probe_id)\n"
            "missing = linear_search_txn(unsorted_txns, 999999)\n"
            "assert idx is not None and idx >= 0\n"
            "assert missing == -1\n"
            "print(idx, missing)"
        ),
        md("## 2. Бинарный поиск по `txn_id` в отсортированном списке"),
        code(
            "def binary_search_txn(sorted_ids, target_id):\n"
            "    # вернуть индекс или -1\n"
            "    return None\n\n\n"
            "probe_id = id_list[200]\n"
            "idx_bin = binary_search_txn(id_list, probe_id)\n"
            "miss_bin = binary_search_txn(id_list, 999999)\n"
            "assert idx_bin is not None and idx_bin >= 0\n"
            "assert miss_bin == -1\n"
            "print(idx_bin, miss_bin)"
        ),
        md("## 3. Подсчёт числа сравнений"),
        code(
            "def linear_steps(ids, target):\n"
            "    return None\n\n\n"
            "def binary_steps(ids, target):\n"
            "    return None\n\n\n"
            "target = id_list[700]\n"
            "ls = linear_steps(id_list, target)\n"
            "bs = binary_steps(id_list, target)\n"
            "assert ls is not None and bs is not None\n"
            "assert int(bs) < int(ls)\n"
            "print(ls, bs)"
        ),
        md("## 4. Короткий вывод по сложности"),
        code(
            "COMPLEXITY_NOTE = ''\n"
            "assert len(COMPLEXITY_NOTE) > 120\n"
            "print(COMPLEXITY_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: поиск по `txn_id`"),
        code(LOAD_DATA),
        md("### A. Закрепление\n\n## 1. Первая и последняя транзакция"),
        code(
            "first_id = None\n"
            "last_id = None\n"
            "assert first_id is not None and last_id is not None\n"
            "assert int(first_id) < int(last_id)\n"
            "print(first_id, last_id)"
        ),
        md("## 2. Бинарный поиск 20 случайных id"),
        code(
            "hits = []\n"
            "# добавьте 20 индексов найденных бинарным поиском\n"
            "assert len(hits) == 20\n"
            "assert min(hits) >= 0\n"
            "print(hits[:5])"
        ),
        md("### B. Вызов\n\n## 3. Почему бинарный поиск не работает на неотсортированном списке"),
        code(
            "FAIL_NOTE = ''\n"
            "assert len(FAIL_NOTE) > 130\n"
            "print(FAIL_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: линейный и бинарный поиск\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        code(
            "def linear_search_txn(txns, target_id):\n"
            "    for i, row in enumerate(txns):\n"
            "        if row[0] == target_id:\n"
            "            return i\n"
            "    return -1\n\n\n"
            "def binary_search_txn(sorted_ids, target_id):\n"
            "    left, right = 0, len(sorted_ids) - 1\n"
            "    while left <= right:\n"
            "        mid = (left + right) // 2\n"
            "        if sorted_ids[mid] == target_id:\n"
            "            return mid\n"
            "        if sorted_ids[mid] < target_id:\n"
            "            left = mid + 1\n"
            "        else:\n"
            "            right = mid - 1\n"
            "    return -1\n\n\n"
            "def linear_steps(ids, target):\n"
            "    steps = 0\n"
            "    for x in ids:\n"
            "        steps += 1\n"
            "        if x == target:\n"
            "            return steps\n"
            "    return steps\n\n\n"
            "def binary_steps(ids, target):\n"
            "    left, right = 0, len(ids) - 1\n"
            "    steps = 0\n"
            "    while left <= right:\n"
            "        steps += 1\n"
            "        mid = (left + right) // 2\n"
            "        if ids[mid] == target:\n"
            "            return steps\n"
            "        if ids[mid] < target:\n"
            "            left = mid + 1\n"
            "        else:\n"
            "            right = mid - 1\n"
            "    return steps\n\n\n"
            "probe_id = unsorted_txns[25][0]\n"
            "idx = linear_search_txn(unsorted_txns, probe_id)\n"
            "idx_bin = binary_search_txn(id_list, id_list[200])\n"
            "ls = linear_steps(id_list, id_list[700])\n"
            "bs = binary_steps(id_list, id_list[700])\n"
            "COMPLEXITY_NOTE = (\n"
            "    'Линейный поиск в среднем просматривает значимую часть массива, а бинарный '\n"
            "    'на отсортированных данных каждый шаг делит диапазон пополам.'\n"
            ")\n"
            "first_id = id_list[0]\n"
            "last_id = id_list[-1]\n"
            "hits = [binary_search_txn(id_list, id_list[i * 30]) for i in range(20)]\n"
            "FAIL_NOTE = (\n"
            "    'Бинарный поиск опирается на порядок значений слева и справа от середины. '\n"
            "    'В неотсортированном массиве это условие нарушено, поэтому отбрасывание половины диапазона ошибочно.'\n"
            ")\n"
            "print(idx, idx_bin, ls, bs)\n"
            "print(first_id, last_id)\n"
            "print(hits[:5])"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson02() -> None:
    base = "lessons/02_practice_search_logs"
    lesson = nb(
        md("# Практика: поиск в логах транзакций"),
        code(LOAD_DATA),
        md("## 1. Поиск транзакции и извлечение строки"),
        code(
            "def linear_search_txn(txns, target_id):\n"
            "    return None\n\n\n"
            "target_id = unsorted_txns[40][0]\n"
            "idx = linear_search_txn(unsorted_txns, target_id)\n"
            "row = None\n"
            "assert idx is not None and idx >= 0\n"
            "assert row is not None and row[0] == target_id\n"
            "print(row)"
        ),
        md("## 2. Бинарный поиск и проверка соседей"),
        code(
            "def binary_search_txn(sorted_ids, target_id):\n"
            "    return None\n\n\n"
            "idx = binary_search_txn(id_list, id_list[300])\n"
            "left_ok = None\n"
            "right_ok = None\n"
            "assert idx is not None and idx > 0\n"
            "assert left_ok is True and right_ok is True\n"
            "print(idx, left_ok, right_ok)"
        ),
        md("## 3. Диапазон по сумме через два бинарных поиска"),
        code(
            "def lower_bound(nums, target):\n"
            "    return None\n\n\n"
            "def upper_bound(nums, target):\n"
            "    return None\n\n\n"
            "low = lower_bound(amount_list, 5000)\n"
            "high = upper_bound(amount_list, 12000)\n"
            "subset = amount_txns[low:high]\n"
            "assert low is not None and high is not None\n"
            "assert low < high and len(subset) > 0\n"
            "assert min(x[1] for x in subset) >= 5000\n"
            "assert max(x[1] for x in subset) <= 12000\n"
            "print(low, high, len(subset))"
        ),
        md("## 4. Нота для отчёта"),
        code(
            "RANGE_NOTE = ''\n"
            "assert len(RANGE_NOTE) > 120\n"
            "print(RANGE_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: практикум по поиску"),
        code(LOAD_DATA),
        md("### A. Закрепление\n\n## 1. Число транзакций с суммой <= 10000"),
        code(
            "count_small = None\n"
            "assert count_small is not None and int(count_small) > 0\n"
            "print(count_small)"
        ),
        md("## 2. Найти 10 транзакций в диапазоне [15000, 17000]"),
        code(
            "sample_ids = []\n"
            "assert len(sample_ids) == 10\n"
            "print(sample_ids)"
        ),
        md("### B. Вызов\n\n## 3. Почему диапазонный поиск лучше полного прохода"),
        code(
            "WHY_RANGE = ''\n"
            "assert len(WHY_RANGE) > 130\n"
            "print(WHY_RANGE)"
        ),
    )
    sol = nb(
        md("# Решения: практика поиска\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        code(
            "def linear_search_txn(txns, target_id):\n"
            "    for i, row in enumerate(txns):\n"
            "        if row[0] == target_id:\n"
            "            return i\n"
            "    return -1\n\n\n"
            "def binary_search_txn(sorted_ids, target_id):\n"
            "    left, right = 0, len(sorted_ids) - 1\n"
            "    while left <= right:\n"
            "        mid = (left + right) // 2\n"
            "        if sorted_ids[mid] == target_id:\n"
            "            return mid\n"
            "        if sorted_ids[mid] < target_id:\n"
            "            left = mid + 1\n"
            "        else:\n"
            "            right = mid - 1\n"
            "    return -1\n\n\n"
            "def lower_bound(nums, target):\n"
            "    left, right = 0, len(nums)\n"
            "    while left < right:\n"
            "        mid = (left + right) // 2\n"
            "        if nums[mid] < target:\n"
            "            left = mid + 1\n"
            "        else:\n"
            "            right = mid\n"
            "    return left\n\n\n"
            "def upper_bound(nums, target):\n"
            "    left, right = 0, len(nums)\n"
            "    while left < right:\n"
            "        mid = (left + right) // 2\n"
            "        if nums[mid] <= target:\n"
            "            left = mid + 1\n"
            "        else:\n"
            "            right = mid\n"
            "    return left\n\n\n"
            "target_id = unsorted_txns[40][0]\n"
            "idx = linear_search_txn(unsorted_txns, target_id)\n"
            "row = unsorted_txns[idx]\n"
            "idx2 = binary_search_txn(id_list, id_list[300])\n"
            "left_ok = id_list[idx2 - 1] <= id_list[idx2]\n"
            "right_ok = id_list[idx2] <= id_list[idx2 + 1]\n"
            "low = lower_bound(amount_list, 5000)\n"
            "high = upper_bound(amount_list, 12000)\n"
            "subset = amount_txns[low:high]\n"
            "RANGE_NOTE = (\n"
            "    'Если суммы отсортированы, два бинарных поиска быстро находят границы диапазона, '\n"
            "    'и мы работаем только с нужным фрагментом лога.'\n"
            ")\n"
            "count_small = upper_bound(amount_list, 10000)\n"
            "s_low = lower_bound(amount_list, 15000)\n"
            "s_high = upper_bound(amount_list, 17000)\n"
            "sample_ids = [row[0] for row in amount_txns[s_low:s_low + 10]]\n"
            "WHY_RANGE = (\n"
            "    'Полный проход проверяет все строки, даже если интересует узкий диапазон. '\n"
            "    'На отсортированных данных диапазонный поиск сокращает число сравнений и ускоряет отчёт.'\n"
            ")\n"
            "print(row)\n"
            "print(idx2, left_ok, right_ok)\n"
            "print(low, high, len(subset))"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson03() -> None:
    base = "lessons/03_selection_merge_quick"
    lesson = nb(
        md("# Сортировки: selection, merge и quick (обзор)"),
        code(LOAD_DATA),
        md("## 1. Сортировка выбором списка сумм"),
        code(
            "def selection_sort(nums):\n"
            "    return None\n\n\n"
            "arr = [9, 1, 5, 3, 7]\n"
            "sorted_arr = selection_sort(arr)\n"
            "assert sorted_arr == [1, 3, 5, 7, 9]\n"
            "print(sorted_arr)"
        ),
        md("## 2. Слияние двух отсортированных списков"),
        code(
            "def merge_sorted(a, b):\n"
            "    return None\n\n\n"
            "merged = merge_sorted([1, 4, 9], [2, 3, 7])\n"
            "assert merged == [1, 2, 3, 4, 7, 9]\n"
            "print(merged)"
        ),
        md("## 3. Mergesort рекурсивно"),
        code(
            "def merge_sort(nums):\n"
            "    return None\n\n\n"
            "test = [12, 5, 1, 8, 3, 7]\n"
            "assert merge_sort(test) == sorted(test)\n"
            "print(merge_sort(test))"
        ),
        md("## 4. Quicksort: один шаг partition"),
        code(
            "def partition_once(nums):\n"
            "    # вернуть left, pivot, right\n"
            "    return None\n\n\n"
            "left, pivot, right = partition_once([8, 2, 9, 4, 6])\n"
            "assert all(x <= pivot for x in left)\n"
            "assert all(x > pivot for x in right)\n"
            "print(left, pivot, right)"
        ),
        md("## 5. Нота по сложности"),
        code(
            "SORT_NOTE = ''\n"
            "assert len(SORT_NOTE) > 140\n"
            "print(SORT_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: сортировки"),
        code(LOAD_DATA),
        md("### A. Закрепление\n\n## 1. Сортировка 30 сумм выбором"),
        code(
            "part = [x[1] for x in unsorted_txns[:30]]\n"
            "sorted_part = None\n"
            "assert sorted_part is not None and sorted_part == sorted(part)\n"
            "print(sorted_part[:10])"
        ),
        md("## 2. Mergesort для 120 сумм"),
        code(
            "vals = [x[1] for x in unsorted_txns[:120]]\n"
            "res = None\n"
            "assert res is not None and res == sorted(vals)\n"
            "print(res[:10])"
        ),
        md("### B. Вызов\n\n## 3. Когда quicksort может тормозить"),
        code(
            "QUICK_NOTE = ''\n"
            "assert len(QUICK_NOTE) > 120\n"
            "print(QUICK_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: сортировки\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        code(
            "def selection_sort(nums):\n"
            "    arr = nums[:]\n"
            "    n = len(arr)\n"
            "    for i in range(n):\n"
            "        m = i\n"
            "        for j in range(i + 1, n):\n"
            "            if arr[j] < arr[m]:\n"
            "                m = j\n"
            "        arr[i], arr[m] = arr[m], arr[i]\n"
            "    return arr\n\n\n"
            "def merge_sorted(a, b):\n"
            "    i = 0\n"
            "    j = 0\n"
            "    out = []\n"
            "    while i < len(a) and j < len(b):\n"
            "        if a[i] <= b[j]:\n"
            "            out.append(a[i])\n"
            "            i += 1\n"
            "        else:\n"
            "            out.append(b[j])\n"
            "            j += 1\n"
            "    out.extend(a[i:])\n"
            "    out.extend(b[j:])\n"
            "    return out\n\n\n"
            "def merge_sort(nums):\n"
            "    if len(nums) <= 1:\n"
            "        return nums[:]\n"
            "    mid = len(nums) // 2\n"
            "    left = merge_sort(nums[:mid])\n"
            "    right = merge_sort(nums[mid:])\n"
            "    return merge_sorted(left, right)\n\n\n"
            "def partition_once(nums):\n"
            "    pivot = nums[len(nums) // 2]\n"
            "    left = [x for x in nums if x < pivot]\n"
            "    same = [x for x in nums if x == pivot]\n"
            "    right = [x for x in nums if x > pivot]\n"
            "    return left + same[:-1], pivot, right\n\n\n"
            "arr = [9, 1, 5, 3, 7]\n"
            "sorted_arr = selection_sort(arr)\n"
            "merged = merge_sorted([1, 4, 9], [2, 3, 7])\n"
            "test = [12, 5, 1, 8, 3, 7]\n"
            "left, pivot, right = partition_once([8, 2, 9, 4, 6])\n"
            "SORT_NOTE = (\n"
            "    'Selection sort делает много сравнений и перестановок, поэтому растёт как O(n^2). '\n"
            "    'Mergesort делит массив и сливает отсортированные части, что обычно даёт O(n log n).'\n"
            ")\n"
            "part = [x[1] for x in unsorted_txns[:30]]\n"
            "sorted_part = selection_sort(part)\n"
            "vals = [x[1] for x in unsorted_txns[:120]]\n"
            "res = merge_sort(vals)\n"
            "QUICK_NOTE = (\n"
            "    'Quicksort может замедляться на почти отсортированных данных при неудачном pivot: '\n"
            "    'разбиения становятся неравномерными, и глубина рекурсии растёт.'\n"
            ")\n"
            "print(sorted_arr)\n"
            "print(merged)\n"
            "print(merge_sort(test))\n"
            "print(left, pivot, right)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson04() -> None:
    base = "lessons/04_practice_sorts"
    lesson = nb(
        md("# Практика: реализуем и сравниваем сортировки"),
        code(LOAD_DATA),
        md("## 1. Реализации selection и merge"),
        code(
            "def selection_sort(nums):\n"
            "    return None\n\n\n"
            "def merge_sort(nums):\n"
            "    return None\n\n\n"
            "vals = [x[1] for x in unsorted_txns[:80]]\n"
            "assert selection_sort(vals) == sorted(vals)\n"
            "assert merge_sort(vals) == sorted(vals)\n"
            "print('ok')"
        ),
        md("## 2. Сравнение времени на 3 размерах"),
        code(
            "sizes = [80, 200, 500]\n"
            "bench = []\n"
            "# заполните bench строками [n, t_selection, t_merge]\n"
            "assert len(bench) == 3\n"
            "assert all(len(row) == 3 for row in bench)\n"
            "print(bench)"
        ),
        md("## 3. Проверка монотонности времени"),
        code(
            "n_ok = None\n"
            "assert n_ok is True\n"
            "print(n_ok)"
        ),
        md("## 4. Вывод о выборе алгоритма"),
        code(
            "BENCH_NOTE = ''\n"
            "assert len(BENCH_NOTE) > 120\n"
            "print(BENCH_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: практикум сортировок"),
        code(LOAD_DATA),
        md("### A. Закрепление\n\n## 1. Сортировка по `risk_score`"),
        code(
            "risks = [x[3] for x in unsorted_txns[:150]]\n"
            "risk_sorted = None\n"
            "assert risk_sorted is not None and risk_sorted == sorted(risks)\n"
            "print(risk_sorted[:12])"
        ),
        md("## 2. Сравнение встроенной `sorted` и merge_sort"),
        code(
            "t_builtin = None\n"
            "t_merge = None\n"
            "assert t_builtin is not None and t_merge is not None\n"
            "assert float(t_builtin) > 0 and float(t_merge) > 0\n"
            "print(t_builtin, t_merge)"
        ),
        md("### B. Вызов\n\n## 3. Почему в проде часто используют встроенную сортировку"),
        code(
            "PROD_NOTE = ''\n"
            "assert len(PROD_NOTE) > 140\n"
            "print(PROD_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: практикум сортировок\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        code(
            "def selection_sort(nums):\n"
            "    arr = nums[:]\n"
            "    for i in range(len(arr)):\n"
            "        m = i\n"
            "        for j in range(i + 1, len(arr)):\n"
            "            if arr[j] < arr[m]:\n"
            "                m = j\n"
            "        arr[i], arr[m] = arr[m], arr[i]\n"
            "    return arr\n\n\n"
            "def merge_sorted(a, b):\n"
            "    i = 0\n"
            "    j = 0\n"
            "    out = []\n"
            "    while i < len(a) and j < len(b):\n"
            "        if a[i] <= b[j]:\n"
            "            out.append(a[i]); i += 1\n"
            "        else:\n"
            "            out.append(b[j]); j += 1\n"
            "    out.extend(a[i:]); out.extend(b[j:])\n"
            "    return out\n\n\n"
            "def merge_sort(nums):\n"
            "    if len(nums) <= 1:\n"
            "        return nums[:]\n"
            "    mid = len(nums) // 2\n"
            "    return merge_sorted(merge_sort(nums[:mid]), merge_sort(nums[mid:]))\n\n\n"
            "vals = [x[1] for x in unsorted_txns[:80]]\n"
            "sizes = [80, 200, 500]\n"
            "bench = []\n"
            "for n in sizes:\n"
            "    part = [x[1] for x in unsorted_txns[:n]]\n"
            "    t0 = time.perf_counter(); selection_sort(part); t_sel = time.perf_counter() - t0\n"
            "    t0 = time.perf_counter(); merge_sort(part); t_mer = time.perf_counter() - t0\n"
            "    bench.append([n, t_sel, t_mer])\n"
            "n_ok = (bench[0][1] <= bench[1][1] <= bench[2][1]) and (bench[0][2] <= bench[1][2] <= bench[2][2])\n"
            "BENCH_NOTE = (\n"
            "    'На маленьких объёмах разница умеренная, но с ростом n selection сортировка растёт быстрее. '\n"
            "    'Для больших логов разумнее выбирать алгоритм уровня O(n log n).'\n"
            ")\n"
            "risks = [x[3] for x in unsorted_txns[:150]]\n"
            "risk_sorted = merge_sort(risks)\n"
            "part2 = [x[1] for x in unsorted_txns[:500]]\n"
            "t0 = time.perf_counter(); sorted(part2); t_builtin = time.perf_counter() - t0\n"
            "t0 = time.perf_counter(); merge_sort(part2); t_merge = time.perf_counter() - t0\n"
            "PROD_NOTE = (\n"
            "    'Встроенная сортировка в Python тщательно оптимизирована и надёжно протестирована. '\n"
            "    'Свою реализацию обычно пишут для обучения и для контроля идеи, а не для боевого кода.'\n"
            ")\n"
            "print(bench)\n"
            "print(n_ok)\n"
            "print(t_builtin, t_merge)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson05() -> None:
    base = "lessons/05_sorted_key_two_pointers"
    lesson = nb(
        md("# `sorted(key=...)` и метод двух указателей"),
        code(LOAD_DATA),
        md("## 1. Сортировка записей по `amount` и `risk_score`"),
        code(
            "by_amount_local = None\n"
            "by_risk_local = None\n"
            "assert by_amount_local is not None and by_risk_local is not None\n"
            "assert by_amount_local[0][1] <= by_amount_local[-1][1]\n"
            "assert by_risk_local[0][3] <= by_risk_local[-1][3]\n"
            "print(by_amount_local[:3])"
        ),
        md("## 2. Два указателя: найти пару сумм близко к цели"),
        code(
            "def two_sum_closest(sorted_amounts, target):\n"
            "    # вернуть (a, b, diff)\n"
            "    return None\n\n\n"
            "a, b, diff = two_sum_closest(amount_list, 40000)\n"
            "assert a is not None and b is not None and diff is not None\n"
            "assert a <= b\n"
            "print(a, b, diff)"
        ),
        md("## 3. Два указателя: число пар не ниже порога"),
        code(
            "def count_pairs_ge(sorted_amounts, threshold):\n"
            "    return None\n\n\n"
            "n_pairs = count_pairs_ge(amount_list[:220], 30000)\n"
            "assert n_pairs is not None and int(n_pairs) > 0\n"
            "print(n_pairs)"
        ),
        md("## 4. Нота по применению метода"),
        code(
            "POINTER_NOTE = ''\n"
            "assert len(POINTER_NOTE) > 120\n"
            "print(POINTER_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: ключи сортировки и два указателя"),
        code(LOAD_DATA),
        md("### A. Закрепление\n\n## 1. Топ-15 рискованных транзакций"),
        code(
            "top_risk_ids = []\n"
            "assert len(top_risk_ids) == 15\n"
            "print(top_risk_ids[:5])"
        ),
        md("## 2. Пара сумм ровно на порог или ближайшая выше"),
        code(
            "pair_info = None\n"
            "assert pair_info is not None and len(pair_info) == 3\n"
            "print(pair_info)"
        ),
        md("### B. Вызов\n\n## 3. Почему указатели требуют сортировки"),
        code(
            "SORT_REQ_NOTE = ''\n"
            "assert len(SORT_REQ_NOTE) > 130\n"
            "print(SORT_REQ_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: key и два указателя\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        code(
            "by_amount_local = sorted(unsorted_txns, key=lambda row: row[1])\n"
            "by_risk_local = sorted(unsorted_txns, key=lambda row: row[3])\n\n\n"
            "def two_sum_closest(sorted_amounts, target):\n"
            "    i = 0\n"
            "    j = len(sorted_amounts) - 1\n"
            "    best_a = sorted_amounts[0]\n"
            "    best_b = sorted_amounts[-1]\n"
            "    best_diff = abs(best_a + best_b - target)\n"
            "    while i < j:\n"
            "        cur = sorted_amounts[i] + sorted_amounts[j]\n"
            "        diff = abs(cur - target)\n"
            "        if diff < best_diff:\n"
            "            best_diff = diff\n"
            "            best_a = sorted_amounts[i]\n"
            "            best_b = sorted_amounts[j]\n"
            "        if cur < target:\n"
            "            i += 1\n"
            "        else:\n"
            "            j -= 1\n"
            "    return best_a, best_b, best_diff\n\n\n"
            "def count_pairs_ge(sorted_amounts, threshold):\n"
            "    i = 0\n"
            "    j = len(sorted_amounts) - 1\n"
            "    total = 0\n"
            "    while i < j:\n"
            "        if sorted_amounts[i] + sorted_amounts[j] >= threshold:\n"
            "            total += j - i\n"
            "            j -= 1\n"
            "        else:\n"
            "            i += 1\n"
            "    return total\n\n\n"
            "a, b, diff = two_sum_closest(amount_list, 40000)\n"
            "n_pairs = count_pairs_ge(amount_list[:220], 30000)\n"
            "POINTER_NOTE = (\n"
            "    'Два указателя эффективны, когда массив отсортирован: каждое движение гарантированно '\n"
            "    'сужает пространство поиска без возврата назад.'\n"
            ")\n"
            "top_risk_ids = [x[0] for x in sorted(unsorted_txns, key=lambda row: row[3], reverse=True)[:15]]\n"
            "pair_info = two_sum_closest(amount_list, 50000)\n"
            "SORT_REQ_NOTE = (\n"
            "    'На несортированных данных нельзя выбрать направление движения указателей: '\n"
            "    'неизвестно, как изменение индекса повлияет на сумму и сравнение с порогом.'\n"
            ")\n"
            "print(by_amount_local[:3])\n"
            "print(a, b, diff)\n"
            "print(n_pairs)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson06() -> None:
    base = "lessons/06_practice_keys_pointers"
    lesson = nb(
        md("# Практика: ключи и указатели на логах"),
        code(LOAD_DATA),
        md("## 1. Слияние двух отсортированных фрагментов"),
        code(
            "def merge_rows_by_amount(a_rows, b_rows):\n"
            "    return None\n\n\n"
            "left_rows = amount_txns[:40]\n"
            "right_rows = amount_txns[40:80]\n"
            "merged = merge_rows_by_amount(left_rows, right_rows)\n"
            "assert merged is not None and len(merged) == 80\n"
            "assert all(merged[i][1] <= merged[i + 1][1] for i in range(len(merged) - 1))\n"
            "print(merged[:3])"
        ),
        md("## 2. Два указателя: минимальная разница сумм между двумя окнами"),
        code(
            "def min_gap_between_windows(a_amounts, b_amounts):\n"
            "    return None\n\n\n"
            "w1 = amount_list[50:130]\n"
            "w2 = amount_list[420:500]\n"
            "gap = min_gap_between_windows(w1, w2)\n"
            "assert gap is not None and int(gap) >= 0\n"
            "print(gap)"
        ),
        md("## 3. Поиск id по списку целей"),
        code(
            "targets = [id_list[10], id_list[90], id_list[190], id_list[390]]\n"
            "positions = []\n"
            "assert len(positions) == len(targets)\n"
            "assert min(positions) >= 0\n"
            "print(positions)"
        ),
        md("## 4. Рефлексия практики"),
        code(
            "PRACTICE_NOTE = ''\n"
            "assert len(PRACTICE_NOTE) > 120\n"
            "print(PRACTICE_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: интеграция ключей и указателей"),
        code(LOAD_DATA),
        md("### A. Закрепление\n\n## 1. Отсортировать tiny по двум ключам"),
        code(
            "tiny_rows = list(tiny_df[['txn_id', 'amount', 'day', 'risk_score']].itertuples(index=False, name=None))\n"
            "tiny_sorted = None\n"
            "assert tiny_sorted is not None and len(tiny_sorted) == len(tiny_rows)\n"
            "print(tiny_sorted[:5])"
        ),
        md("## 2. Пары сумм не ниже 45000 в tiny"),
        code(
            "pairs_cnt = None\n"
            "assert pairs_cnt is not None and int(pairs_cnt) >= 0\n"
            "print(pairs_cnt)"
        ),
        md("### B. Вызов\n\n## 3. Короткий мини-отчёт для банка"),
        code(
            "MINI_REPORT = ''\n"
            "assert len(MINI_REPORT) > 170\n"
            "print(MINI_REPORT)"
        ),
    )
    sol = nb(
        md("# Решения: практика key + pointers\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        code(
            "def merge_rows_by_amount(a_rows, b_rows):\n"
            "    i = 0\n"
            "    j = 0\n"
            "    out = []\n"
            "    while i < len(a_rows) and j < len(b_rows):\n"
            "        if a_rows[i][1] <= b_rows[j][1]:\n"
            "            out.append(a_rows[i]); i += 1\n"
            "        else:\n"
            "            out.append(b_rows[j]); j += 1\n"
            "    out.extend(a_rows[i:])\n"
            "    out.extend(b_rows[j:])\n"
            "    return out\n\n\n"
            "def min_gap_between_windows(a_amounts, b_amounts):\n"
            "    i = 0\n"
            "    j = 0\n"
            "    best = abs(a_amounts[0] - b_amounts[0])\n"
            "    while i < len(a_amounts) and j < len(b_amounts):\n"
            "        cur = abs(a_amounts[i] - b_amounts[j])\n"
            "        if cur < best:\n"
            "            best = cur\n"
            "        if a_amounts[i] < b_amounts[j]:\n"
            "            i += 1\n"
            "        else:\n"
            "            j += 1\n"
            "    return best\n\n\n"
            "def binary_search_txn(sorted_ids, target_id):\n"
            "    left, right = 0, len(sorted_ids) - 1\n"
            "    while left <= right:\n"
            "        mid = (left + right) // 2\n"
            "        if sorted_ids[mid] == target_id:\n"
            "            return mid\n"
            "        if sorted_ids[mid] < target_id:\n"
            "            left = mid + 1\n"
            "        else:\n"
            "            right = mid - 1\n"
            "    return -1\n\n\n"
            "left_rows = amount_txns[:40]\n"
            "right_rows = amount_txns[40:80]\n"
            "merged = merge_rows_by_amount(left_rows, right_rows)\n"
            "w1 = amount_list[50:130]\n"
            "w2 = amount_list[420:500]\n"
            "gap = min_gap_between_windows(w1, w2)\n"
            "targets = [id_list[10], id_list[90], id_list[190], id_list[390]]\n"
            "positions = [binary_search_txn(id_list, x) for x in targets]\n"
            "PRACTICE_NOTE = (\n"
            "    'Один и тот же принцип двух указателей помогает и при слиянии, и при поиске близких сумм. '\n"
            "    'Ключевое условие - данные должны быть отсортированы по рабочему признаку.'\n"
            ")\n"
            "tiny_rows = list(tiny_df[['txn_id', 'amount', 'day', 'risk_score']].itertuples(index=False, name=None))\n"
            "tiny_sorted = sorted(tiny_rows, key=lambda row: (row[2], row[1]))\n"
            "tiny_amounts = sorted([x[1] for x in tiny_rows])\n"
            "i = 0\n"
            "j = len(tiny_amounts) - 1\n"
            "pairs_cnt = 0\n"
            "while i < j:\n"
            "    if tiny_amounts[i] + tiny_amounts[j] >= 45000:\n"
            "        pairs_cnt += j - i\n"
            "        j -= 1\n"
            "    else:\n"
            "        i += 1\n"
            "MINI_REPORT = (\n"
            "    'На mini-логе отсортировали транзакции по дню и сумме для операционного просмотра. '\n"
            "    'Двумя указателями оценили число пар крупных операций от 45000, '\n"
            "    'что полезно как быстрый индикатор концентрации больших платежей.'\n"
            ")\n"
            "print(merged[:3])\n"
            "print(gap)\n"
            "print(positions)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson07() -> None:
    base = "lessons/07_complexity_integration"
    lesson = nb(
        md("# Интеграция: O(n^2) vs O(n log n) на банковских логах"),
        code(LOAD_DATA),
        md("## 1. Подготовить функции сортировки"),
        code(
            "def selection_sort(nums):\n"
            "    return None\n\n\n"
            "def merge_sort(nums):\n"
            "    return None\n\n\n"
            "test = [8, 4, 2, 9, 1]\n"
            "assert selection_sort(test) == sorted(test)\n"
            "assert merge_sort(test) == sorted(test)\n"
            "print('ok')"
        ),
        md("## 2. Бенчмарк на 4 размерах"),
        code(
            "sizes = [80, 180, 360, 720]\n"
            "table = []\n"
            "# собрать строки [n, t_selection, t_merge, ratio]\n"
            "assert len(table) == 4\n"
            "assert all(len(row) == 4 for row in table)\n"
            "print(table)"
        ),
        md("## 3. Acceptance checklist"),
        code(
            "acceptance = pd.Series(\n"
            "    [False, False, False, False, False],\n"
            "    index=['correct_impl', 'has_benchmark', 'has_ratio', 'has_conclusion', 'report_ready']\n"
            ")\n"
            "assert bool(acceptance.all())\n"
            "print(acceptance)"
        ),
        md("## 4. Финальный REPORT"),
        code(
            "REPORT = ''\n"
            "READY = False\n"
            "assert len(REPORT) > 320\n"
            "assert READY is True\n"
            "print(REPORT[:300])"
        ),
    )
    hw = nb(
        md("# ДЗ: итог алгоритмического блока"),
        code(LOAD_DATA),
        md("### A. Закрепление\n\n## 1. Повторить бенчмарк на `risk_score`"),
        code(
            "risk_table = []\n"
            "assert len(risk_table) >= 3\n"
            "print(risk_table)"
        ),
        md("## 2. Сравнить с встроенной сортировкой"),
        code(
            "t_builtin = None\n"
            "t_merge = None\n"
            "assert t_builtin is not None and t_merge is not None\n"
            "print(t_builtin, t_merge)"
        ),
        md("### B. Вызов\n\n## 3. Рефлексия блока 42–48"),
        code(
            "REFLECTION = ''\n"
            "assert len(REFLECTION) > 220\n"
            "print(REFLECTION)"
        ),
    )
    sol = nb(
        md("# Решения: интеграция сложности\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        code(
            "def selection_sort(nums):\n"
            "    arr = nums[:]\n"
            "    for i in range(len(arr)):\n"
            "        m = i\n"
            "        for j in range(i + 1, len(arr)):\n"
            "            if arr[j] < arr[m]:\n"
            "                m = j\n"
            "        arr[i], arr[m] = arr[m], arr[i]\n"
            "    return arr\n\n\n"
            "def merge_sorted(a, b):\n"
            "    i = 0\n"
            "    j = 0\n"
            "    out = []\n"
            "    while i < len(a) and j < len(b):\n"
            "        if a[i] <= b[j]:\n"
            "            out.append(a[i]); i += 1\n"
            "        else:\n"
            "            out.append(b[j]); j += 1\n"
            "    out.extend(a[i:]); out.extend(b[j:])\n"
            "    return out\n\n\n"
            "def merge_sort(nums):\n"
            "    if len(nums) <= 1:\n"
            "        return nums[:]\n"
            "    mid = len(nums) // 2\n"
            "    return merge_sorted(merge_sort(nums[:mid]), merge_sort(nums[mid:]))\n\n\n"
            "sizes = [80, 180, 360, 720]\n"
            "table = []\n"
            "for n in sizes:\n"
            "    part = [x[1] for x in unsorted_txns[:n]]\n"
            "    t0 = time.perf_counter(); selection_sort(part); t_sel = time.perf_counter() - t0\n"
            "    t0 = time.perf_counter(); merge_sort(part); t_mer = time.perf_counter() - t0\n"
            "    ratio = t_sel / t_mer if t_mer > 0 else 0.0\n"
            "    table.append([n, t_sel, t_mer, ratio])\n"
            "acceptance = pd.Series(\n"
            "    [True, True, True, True, True],\n"
            "    index=['correct_impl', 'has_benchmark', 'has_ratio', 'has_conclusion', 'report_ready']\n"
            ")\n"
            "REPORT = (\n"
            "    'В модуле 42-48 мы собрали полный алгоритмический цикл на банковских логах: '\n"
            "    'линейный и бинарный поиск, ручные сортировки, sorted(key=...), задачи на два указателя. '\n"
            "    'Бенчмарк на размерах 80-720 показывает рост времени selection сортировки быстрее, '\n"
            "    'чем у mergesort, что согласуется с O(n^2) против O(n log n). '\n"
            "    'Практический вывод: при росте лога выбираем алгоритмы и структуры данных осознанно, '\n"
            "    'а встроенные инструменты используем как надёжный baseline.'\n"
            ")\n"
            "READY = bool(acceptance.all())\n"
            "risk_table = []\n"
            "for n in (100, 300, 600):\n"
            "    part = [x[3] for x in unsorted_txns[:n]]\n"
            "    t0 = time.perf_counter(); selection_sort(part); t_sel = time.perf_counter() - t0\n"
            "    t0 = time.perf_counter(); merge_sort(part); t_mer = time.perf_counter() - t0\n"
            "    risk_table.append([n, t_sel, t_mer])\n"
            "part2 = [x[1] for x in unsorted_txns[:720]]\n"
            "t0 = time.perf_counter(); sorted(part2); t_builtin = time.perf_counter() - t0\n"
            "t0 = time.perf_counter(); merge_sort(part2); t_merge = time.perf_counter() - t0\n"
            "REFLECTION = (\n"
            "    'Алгоритмический блок помог связать идею сложности с реальными данными банка. '\n"
            "    'После практик стало видно, что выбор алгоритма заранее определяет, выдержит ли решение рост объёма лога. '\n"
            "    'Отдельно важен инженерный баланс: понимать ручные реализации и в проде опираться на надёжные стандартные инструменты.'\n"
            ")\n"
            "print(table)\n"
            "print(acceptance)\n"
            "print('READY=', READY)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


BUILDERS = [
    add_lesson01,
    add_lesson02,
    add_lesson03,
    add_lesson04,
    add_lesson05,
    add_lesson06,
    add_lesson07,
]


def main() -> None:
    required = [CSV_UNSORTED, CSV_BY_ID, CSV_BY_AMOUNT, CSV_TINY]
    missing = [p for p in required if not p.exists()]
    if missing:
        raise SystemExit(f"Missing CSV files: {missing}. Run data/make_bank_transactions_csv.py first.")
    for builder in BUILDERS:
        builder()
    for rel_path, notebook in NOTEBOOKS.items():
        write(rel_path, notebook)
    for d in LESSON_DIRS:
        copy_data(d)
    print(f"done: {len(NOTEBOOKS)} notebooks in {len(LESSON_DIRS)} lessons")


if __name__ == "__main__":
    main()
