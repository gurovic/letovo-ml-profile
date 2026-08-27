#!/usr/bin/env python3
"""Build the complete student and teacher materials for module 08_07.

This file is the source of truth for 21 notebooks, seven local lesson plans,
and the CSV copies required to run each notebook from its lesson directory.
Student work is intentionally unfinished, but every task has an executable
contract.  Teacher solutions mirror lesson and homework sections explicitly.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
CSV_NAMES = (
    "bank_transactions_unsorted.csv",
    "bank_transactions_sorted_by_txn_id.csv",
    "bank_transactions_sorted_by_amount.csv",
    "bank_transactions_tiny.csv",
)

LESSONS = [
    {
        "dir": "01_linear_binary_search",
        "pair": 42,
        "title": "Линейный и бинарный поиск в логах банка",
        "role": "введение",
        "prereq": "Списки, циклы, функции и индексы; понятие отсортированного списка",
        "first": "Один и тот же txn_id можно искать сотнями проверок или несколькими делениями диапазона — выясним цену порядка.",
        "minimum": "зелёные assert §§2–7; корректные `linear_search` и `binary_search`; объяснение инварианта",
        "next": "диапазонный поиск — пара 43",
        "idea": "Бинарный поиск ускоряет запрос только потому, что сохраняет инвариант на отсортированном диапазоне.",
        "outcomes": "реализовать линейный и бинарный поиск; проверить пустой список и отсутствие цели; посчитать сравнения; объяснить O(n) и O(log n)",
        "errors": [
            ("Возвращает `None`", "Вернуться к контракту: индекс найденного элемента или `-1`."),
            ("Цикл зависает", "После сравнения одна из границ обязана пройти за `mid`."),
            ("Ищет бинарно в unsorted", "Попросить обосновать, какую половину можно отбросить."),
            ("Теряет крайний элемент", "Проверить цели на индексах 0 и n−1."),
        ],
        "stages": [
            ("Схема данных и контракт", 8, "Читает четыре поля кортежа, формулирует индекс/−1.", "Показать разницу txn_id и позиции.", "§1", "Названы вход и выход."),
            ("Линейный поиск", 14, "Пишет цикл с enumerate.", "Спросить, когда можно остановиться.", "§2", "Три assert зелёные."),
            ("Границы бинарного", 12, "Трассирует left, mid, right.", "Фиксировать включительный диапазон.", "§3", "Трасса приходит к цели."),
            ("Бинарный поиск", 18, "Реализует цикл.", "Не диктовать ветви; спрашивать, где цель.", "§4", "Края и miss проходят."),
            ("Число сравнений", 10, "Инструментирует обе функции.", "Сравнивать шаги, не наносекунды.", "§5–6", "binary_steps < linear_steps."),
            ("Нарушение предпосылки", 10, "Запускает контрпример на unsorted.", "Отделить случайное попадание от гарантии.", "§7", "Сформулирован инвариант."),
            ("Самостоятельно и ДЗ", 8, "Решает поиск записи и открывает ДЗ.", "Развести Part A и Challenge.", "§8–9", "Ученик знает минимум сдачи."),
        ],
    },
    {
        "dir": "02_practice_search_logs",
        "pair": 43,
        "title": "Практика: поиск и границы диапазона",
        "role": "отработка",
        "prereq": "Пара 42: бинарный поиск и включительные границы",
        "first": "Банк редко спрашивает одну сумму: чаще нужен весь диапазон — найдём его без полного прохода.",
        "minimum": "зелёные assert у `lower_bound`, `upper_bound`, диапазонного среза и поиска пачки id",
        "next": "ручные сортировки — пара 44",
        "idea": "Два бинарных поиска превращают условие по диапазону в точный полуинтервал `[lo, hi)`.",
        "outcomes": "реализовать lower/upper bound; получить диапазон сумм; обработать пустой результат; искать пачку id; описать сложность O(log n + k)",
        "errors": [
            ("Путает `<` и `<=`", "Проговорить: lower — первое ≥ target, upper — первое > target."),
            ("Срез теряет последнее значение", "Напомнить, что правая граница Python-среза не включается."),
            ("Индекс выходит за список", "У границ используем `right = len(nums)`."),
            ("Считает выдачу диапазона O(log n)", "Отдельно учесть k строк результата."),
        ],
        "stages": [
            ("Повтор поиска id", 8, "Восстанавливает binary_search.", "Проверить крайние id.", "§1", "Контракт выполнен."),
            ("Lower bound", 14, "Ищет первое значение ≥ target.", "Трассировать полуинтервал.", "§2", "Дубликаты обработаны."),
            ("Upper bound", 14, "Меняет условие на первое > target.", "Сопоставить две функции.", "§3", "Дубликаты обработаны."),
            ("Диапазон сумм", 14, "Строит срез `[lo:hi]`.", "Проверить минимум и максимум.", "§4", "Все суммы в диапазоне."),
            ("Пустые и крайние диапазоны", 10, "Проверяет запрос вне данных.", "Не считать пустоту ошибкой.", "§5", "Получен пустой список."),
            ("Пачка запросов", 10, "Ищет несколько txn_id.", "Проверить сохранение порядка целей.", "§6–7", "Все позиции верны."),
            ("Вывод и ДЗ", 10, "Пишет сложность, открывает ДЗ.", "Развести поиск границ и выдачу k.", "§8–9", "Вывод содержит log и k."),
        ],
    },
    {
        "dir": "03_selection_merge_quick",
        "pair": 44,
        "title": "Selection sort, mergesort и идея quicksort",
        "role": "введение",
        "prereq": "Функции, вложенные циклы, рекурсия из модуля 1",
        "first": "Сортировка выбором, слиянием и pivot дают один результат, но растут совершенно по-разному.",
        "minimum": "рабочие `selection_sort`, `merge_sorted`, `merge_sort`; корректный partition; объяснение роста",
        "next": "сравнение реализаций — пара 45",
        "idea": "Стратегия разбиения определяет рост работы: полный поиск минимума даёт O(n²), деление и слияние — O(n log n).",
        "outcomes": "реализовать selection sort; слить два sorted списка; собрать mergesort рекурсивно; выполнить partition; различать средний и худший случай",
        "errors": [
            ("Меняет входной список", "Начать функцию с копии и проверить исходный список."),
            ("После while теряет хвост", "Добавить остаток обоих списков."),
            ("Нет базового случая", "Проверить списки длины 0 и 1."),
            ("Дубликат pivot пропадает", "Разделять на less/equal/greater."),
        ],
        "stages": [
            ("Selection: один проход", 10, "Находит минимум хвоста.", "Показать границу sorted/unsorted.", "§1", "Один шаг корректен."),
            ("Полный selection", 14, "Реализует вложенные циклы.", "Считать сравнения.", "§2", "Не мутирует вход."),
            ("Слияние", 14, "Двигает два индекса.", "Спросить, почему назад не идём.", "§3", "Дубликаты сохранены."),
            ("Mergesort", 18, "Пишет base/split/merge.", "Связать с деревом рекурсии.", "§4", "Краевые тесты зелёные."),
            ("Partition quicksort", 10, "Разбивает по pivot.", "Не требовать in-place quicksort.", "§5", "Все элементы сохранены."),
            ("Сравнение работы", 8, "Считает selection comparisons.", "Отделить корректность от скорости.", "§6–7", "Формула подтверждена."),
            ("Вывод и ДЗ", 6, "Выбирает алгоритм и открывает ДЗ.", "Уточнить средний/худший quicksort.", "§8–9", "Осмысленный вывод."),
        ],
    },
    {
        "dir": "04_practice_sorts",
        "pair": 45,
        "title": "Практика: корректность и бенчмарк сортировок",
        "role": "отработка",
        "prereq": "Пара 44: selection sort, merge и рекурсивный mergesort",
        "first": "Быстрый алгоритм сначала должен быть правильным: построим тестовый gate, затем честно сравним рост.",
        "minimum": "две реализации проходят edge cases; таблица для четырёх n; вывод не опирается на один шумный замер",
        "next": "`sorted(key=...)` и два указателя — пара 46",
        "idea": "Бенчмарк подтверждает модель роста только после проверки корректности и повторяемого протокола.",
        "outcomes": "проверить сортировки на edge cases; измерить median времени; собрать таблицу; сравнить рост; выбрать production baseline",
        "errors": [
            ("Замер включает подготовку данных", "Создать вход до старта таймера."),
            ("Один запуск даёт шум", "Повторить и взять медиану."),
            ("Selection на 960 строк слишком долгий", "Ограничить размеры учебным диапазоном."),
            ("Сравнивает разные входы", "Каждому алгоритму передать копию одного списка."),
        ],
        "stages": [
            ("Quality gate", 10, "Проверяет edge cases.", "Не переходить к времени до PASS.", "§1", "Все функции корректны."),
            ("Повторяемый таймер", 12, "Пишет median_runtime.", "Исключить генерацию входа.", "§2", "Время положительно."),
            ("Таблица размеров", 18, "Замеряет 80–640.", "Одинаковые данные и repeats.", "§3", "Четыре строки."),
            ("Нормированный рост", 12, "Сравнивает t/n² и t/(n log n).", "Не требовать идеальной константы.", "§4", "Есть численный вывод."),
            ("Встроенный baseline", 10, "Добавляет sorted.", "Обсудить Timsort и production.", "§5", "Baseline измерен."),
            ("Риск интерпретации", 10, "Формулирует ограничения.", "Время машины ≠ доказательство Big O.", "§6–8", "Вывод честный."),
            ("ДЗ", 8, "Открывает homework.", "Показать обязательную и Challenge части.", "§9", "План сдачи понятен."),
        ],
    },
    {
        "dir": "05_sorted_key_two_pointers",
        "pair": 46,
        "title": "`sorted(key=...)` и два указателя",
        "role": "введение",
        "prereq": "Кортежи, lambda, отсортированные списки и сложность",
        "first": "Ключ сортировки отвечает, что значит «раньше», а два указателя используют этот порядок как доказательство движения.",
        "minimum": "сортировки по одному/двум ключам; `two_sum_closest`; `count_pairs_ge`; объяснение движения",
        "next": "практика ключей и указателей — пара 47",
        "idea": "После сортировки монотонность позволяет двигать указатели только вперёд и не перебирать все пары.",
        "outcomes": "применить key и reverse; сортировать по двум полям; найти ближайшую сумму пары; посчитать пары выше порога; объяснить O(n)",
        "errors": [
            ("Сортирует весь кортеж", "Явно назвать индекс рабочего поля."),
            ("Двигает неверный указатель", "Если сумма мала, увеличить меньший элемент; если велика — уменьшить больший."),
            ("Считает одну пару вместо j−i", "Все пары с текущим правым и индексами i..j−1 подходят."),
            ("Использует один элемент дважды", "Условие цикла `left < right`."),
        ],
        "stages": [
            ("Key по amount", 8, "Сортирует записи.", "Сопоставить row[1] со схемой.", "§1", "Порядок сумм верен."),
            ("Два ключа", 10, "Сортирует risk desc, amount asc.", "Показать отрицание числового ключа.", "§2", "Tie-break корректен."),
            ("Трасса указателей", 10, "Вручную двигает left/right.", "Каждый шаг должен сужать интервал.", "§3", "Нет возврата назад."),
            ("Ближайшая пара", 18, "Реализует функцию.", "Хранить best отдельно.", "§4", "Совпадает с brute force на toy."),
            ("Число пар ≥ threshold", 16, "Использует пакетный подсчёт.", "Обосновать `right-left`.", "§5", "Совпадает с brute force."),
            ("Стоимость сортировки", 10, "Сравнивает once vs each query.", "Развести preprocessing и query.", "§6–8", "Записана сложность."),
            ("ДЗ", 8, "Открывает homework.", "Challenge — вернуть ids, не только суммы.", "§9", "Понятен контракт."),
        ],
    },
    {
        "dir": "06_practice_keys_pointers",
        "pair": 47,
        "title": "Практика: ключи, слияние и два указателя",
        "role": "отработка",
        "prereq": "Пара 46: key, tie-break и правило движения указателей",
        "first": "Сегодня одна схема двух индексов решит три задачи: merge, минимальный разрыв и сверку id.",
        "minimum": "merge строк по amount; min gap двух окон; пересечение sorted id; отчёт с проверенными числами",
        "next": "интеграция и сложность — пара 48",
        "idea": "Два монотонных потока можно совместно обработать за линейное время без вложенного перебора.",
        "outcomes": "сливать записи по ключу; искать минимальный разрыв между списками; пересекать sorted id; строить multi-key рейтинг; проверять результат brute force",
        "errors": [
            ("Merge сравнивает txn_id", "Рабочий ключ здесь amount, то есть row[1]."),
            ("Min gap пропускает равенство", "При gap=0 можно завершить поиск."),
            ("Intersection дублирует id", "В наборе ids уникальны; при совпадении двигаются оба."),
            ("Отчёт содержит непроверенное число", "Каждое число должно происходить из переменной ноутбука."),
        ],
        "stages": [
            ("Merge записей", 14, "Сливает два окна.", "Проверить хвосты и ключ.", "§1", "80 строк и sorted."),
            ("Минимальный разрыв", 16, "Двигает меньшую сумму.", "Остановиться на нуле.", "§2", "Совпадает с brute force."),
            ("Пересечение ids", 14, "Пишет intersection.", "При равенстве двигаются оба.", "§3", "Toy и data проходят."),
            ("Multi-key рейтинг", 10, "Сортирует risk/day/amount.", "Зафиксировать направления.", "§4", "Top-10 корректен."),
            ("Проверка oracle", 10, "Сравнивает с вложенным циклом.", "Brute force — тест, не production.", "§5–6", "Результаты совпали."),
            ("Мини-отчёт", 10, "Собирает проверенные выводы.", "Не приписывать причинность.", "§7–8", "Текст проходит контракт."),
            ("ДЗ", 6, "Открывает homework.", "Challenge объединяет три операции.", "§9", "Понятен deliverable."),
        ],
    },
    {
        "dir": "07_complexity_integration",
        "pair": 48,
        "title": "Интеграция: библиотека алгоритмов и сложность",
        "role": "интеграция",
        "prereq": "Пары 42–47: поиск, сортировки, key и два указателя",
        "first": "Соберём не набор разрозненных функций, а проверяемую библиотеку банка с quality gate и отчётом.",
        "minimum": "API поиска/сортировки проходит gate; benchmark ≥4 размеров; acceptance all True; итоговый REPORT",
        "next": "структуры данных — модуль 08_08",
        "idea": "Инженерный результат соединяет контракт, тесты, модель сложности, измерение и ограниченный вывод.",
        "outcomes": "собрать API; выполнить параметризованные тесты; построить benchmark; оценить рост; сформировать acceptance checklist и отчёт",
        "errors": [
            ("Gate проверяет только happy path", "Добавить empty, one, duplicates, miss."),
            ("Отчёт утверждает причинность", "Бенчмарк показывает время реализации, не причину банковского риска."),
            ("READY задан вручную", "Вычислить его из acceptance."),
            ("Один медленный запуск ломает вывод", "Использовать median и говорить о тренде."),
        ],
        "stages": [
            ("Контракт API", 8, "Фиксирует функции библиотеки.", "Сверить имена и выходы.", "§1", "API перечислен."),
            ("Реализация поиска", 12, "Собирает linear/binary/bounds.", "Проверить miss и края.", "§2", "Search gate PASS."),
            ("Реализация сортировок", 14, "Собирает selection/merge.", "Проверить немутируемость.", "§3", "Sort gate PASS."),
            ("Параметризованный gate", 12, "Запускает набор cases.", "Тесты раньше benchmark.", "§4", "Все checks True."),
            ("Benchmark", 16, "Строит таблицу 4 размеров.", "Median, одинаковые данные.", "§5", "Таблица полна."),
            ("Acceptance и REPORT", 12, "Связывает evidence с чек-листом.", "READY вычисляется.", "§6–8", "all True, текст ≥350."),
            ("Сдача и ДЗ", 6, "Открывает итоговое ДЗ.", "Уточнить файлы артефакта.", "§9", "Deliverable понятен."),
        ],
    },
]

LOAD_DATA = """from pathlib import Path
import math
import statistics
import time
import pandas as pd


def find_csv(name):
    for path in (
        Path(name),
        Path("../") / name,
        Path("../../data") / name,
        Path("../data") / name,
        Path("../../../data") / name,
    ):
        if path.exists():
            return path.resolve()
    return "https://raw.githubusercontent.com/gurovic/letovo-ml-profile/main/modules/08_07_bank_arrays_search/data/" + name


unsorted_df = pd.read_csv(find_csv("bank_transactions_unsorted.csv"))
by_id_df = pd.read_csv(find_csv("bank_transactions_sorted_by_txn_id.csv"))
by_amount_df = pd.read_csv(find_csv("bank_transactions_sorted_by_amount.csv"))
tiny_df = pd.read_csv(find_csv("bank_transactions_tiny.csv"))
COLS = ["txn_id", "amount", "day", "risk_score"]
unsorted_txns = list(unsorted_df[COLS].itertuples(index=False, name=None))
id_txns = list(by_id_df[COLS].itertuples(index=False, name=None))
amount_txns = list(by_amount_df[COLS].itertuples(index=False, name=None))
tiny_txns = list(tiny_df[COLS].itertuples(index=False, name=None))
id_list = [row[0] for row in id_txns]
amount_list = [row[1] for row in amount_txns]
assert id_list == sorted(id_list)
assert amount_list == sorted(amount_list)
print(f"Загружено {len(unsorted_txns)} транзакций; поля кортежа: {COLS}")
"""

SOL_BANNER = (
    "**Для преподавателя.** Полный эталон к `lesson.ipynb` и "
    "`homework.ipynb`; ученикам до сдачи не показывать."
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


def notebook(title: str, sections: list[tuple[str, str]], solution: bool = False) -> dict:
    prefix = "# Решения: " if solution else "# "
    banner = f"\n\n{SOL_BANNER}" if solution else ""
    cells = [md(prefix + title + banner), code(LOAD_DATA)]
    for heading, source in sections:
        cells.extend((md(heading), code(source)))
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": cells,
    }


COMMON_SOLUTION = """def linear_search(values, target):
    for index, value in enumerate(values):
        if value == target:
            return index
    return -1


def binary_search(values, target):
    left, right = 0, len(values) - 1
    while left <= right:
        mid = (left + right) // 2
        if values[mid] == target:
            return mid
        if values[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def lower_bound(values, target):
    left, right = 0, len(values)
    while left < right:
        mid = (left + right) // 2
        if values[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left


def upper_bound(values, target):
    left, right = 0, len(values)
    while left < right:
        mid = (left + right) // 2
        if values[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left


def selection_sort(values):
    result = list(values)
    for i in range(len(result)):
        smallest = i
        for j in range(i + 1, len(result)):
            if result[j] < result[smallest]:
                smallest = j
        result[i], result[smallest] = result[smallest], result[i]
    return result


def merge_sorted(left, right):
    i = j = 0
    result = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + list(left[i:]) + list(right[j:])


def merge_sort(values):
    if len(values) <= 1:
        return list(values)
    mid = len(values) // 2
    return merge_sorted(merge_sort(values[:mid]), merge_sort(values[mid:]))


def median_runtime(function, values, repeats=3):
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        function(list(values))
        samples.append(time.perf_counter() - start)
    return statistics.median(samples)
"""


def lesson01() -> tuple[list, list, list]:
    lesson = [
        ("## 1. Контракт поиска\n\nПолучите список первых восьми id и назовите позицию существующей цели.", "sample_ids = id_list[:8]\ntarget = sample_ids[5]\nexpected_index = None  # TODO\nassert expected_index == 5\nassert sample_ids == sorted(sample_ids)\n"),
        ("## 2. Линейный поиск\n\nВерните индекс первого совпадения или `-1`.", "def linear_search(values, target):\n    # TODO\n    ...\n\nassert linear_search([7, 2, 7], 7) == 0\nassert linear_search([], 1) == -1\nassert linear_search(id_list, id_list[-1]) == len(id_list) - 1\n"),
        ("## 3. Трасса границ\n\nЗапишите пары `(left, right)` до нахождения 31.", "toy = [3, 8, 14, 21, 31, 44, 57]\ntrace = []  # TODO\nassert trace and trace[0] == (0, len(toy) - 1)\nassert len(trace) <= 3\n"),
        ("## 4. Бинарный поиск\n\nДиапазон границ включительный.", "def binary_search(values, target):\n    # TODO\n    ...\n\nassert binary_search([], 5) == -1\nassert binary_search([5], 5) == 0\nassert binary_search(id_list, id_list[0]) == 0\nassert binary_search(id_list, id_list[-1]) == len(id_list) - 1\nassert binary_search(id_list, -1) == -1\n"),
        ("## 5. Линейные сравнения", "def linear_steps(values, target):\n    # TODO: вернуть (index, comparisons)\n    ...\n\nli, ls = linear_steps(id_list, id_list[700])\nassert li == 700 and ls == 701\n"),
        ("## 6. Бинарные сравнения", "def binary_steps(values, target):\n    # TODO: вернуть (index, comparisons)\n    ...\n\nbi, bs = binary_steps(id_list, id_list[700])\nassert bi == 700\nassert 1 <= bs <= math.ceil(math.log2(len(id_list))) + 1\nassert bs < ls\n"),
        ("## 7. Предпосылка sorted\n\nОбъясните, почему результат на неотсортированном списке не гарантирован.", "SEARCH_INVARIANT = \"\"  # TODO: не менее 140 символов\nassert len(SEARCH_INVARIANT) >= 140\nassert \"сорт\" in SEARCH_INVARIANT.lower()\n"),
        ("## 8. Поиск записи, а не только id", "probe = unsorted_txns[37]\npos = linear_search([row[0] for row in unsorted_txns], probe[0])\nfound_row = None  # TODO\nassert found_row == probe\n"),
        ("## 9. Самопроверка", "checks = {\n    \"linear_contract\": None,\n    \"binary_edges\": None,\n    \"binary_fewer_steps\": None,\n    \"invariant_written\": None,\n}  # TODO: все значения True\nassert set(checks.values()) == {True}\n"),
    ]
    hw = [
        ("### Part A — обязательно\n\n## A1. Серия линейных поисков", "targets = [unsorted_txns[i][0] for i in (0, 20, 100, 300)] + [-1]\nlinear_positions = None  # TODO\nassert len(linear_positions) == 5\nassert linear_positions[-1] == -1\n"),
        ("## A2. Серия бинарных поисков", "targets_sorted = [id_list[i] for i in (0, 20, 100, 300)] + [-1]\nbinary_positions = None  # TODO\nassert binary_positions == [0, 20, 100, 300, -1]\n"),
        ("## A3. Краевые тесты", "edge_checks = []  # TODO: минимум 6 bool-проверок обеих функций\nassert len(edge_checks) >= 6 and all(edge_checks)\n"),
        ("### Challenge\n\n## B1. Первый индекс дубликата", "def binary_search_first(values, target):\n    # TODO\n    ...\n\nassert binary_search_first([1, 2, 2, 2, 5], 2) == 1\nassert binary_search_first([1, 3], 2) == -1\n"),
        ("## B2. Инженерная записка", "SEARCH_NOTE = \"\"  # TODO: preprocessing, O(n), O(log n), ограничение\nassert len(SEARCH_NOTE) >= 220\nassert all(token in SEARCH_NOTE.lower() for token in [\"o(n)\", \"o(log n)\"])\n"),
    ]
    sol = [
        ("## Урок. 1–2. Контракт и linear", COMMON_SOLUTION + "\nsample_ids = id_list[:8]\ntarget = sample_ids[5]\nexpected_index = linear_search(sample_ids, target)\nassert expected_index == 5\n"),
        ("## Урок. 3. Трасса", "toy = [3, 8, 14, 21, 31, 44, 57]\nleft, right, trace = 0, len(toy) - 1, []\nwhile left <= right:\n    trace.append((left, right)); mid = (left + right) // 2\n    if toy[mid] == 31: break\n    if toy[mid] < 31: left = mid + 1\n    else: right = mid - 1\nassert trace[0] == (0, 6)\n"),
        ("## Урок. 4. Binary edges", "assert binary_search([], 5) == -1\nassert binary_search([5], 5) == 0\nassert binary_search(id_list, id_list[-1]) == len(id_list) - 1\n"),
        ("## Урок. 5–6. Сравнения", "def linear_steps(values, target):\n    for i, value in enumerate(values, 1):\n        if value == target: return i - 1, i\n    return -1, len(values)\n\ndef binary_steps(values, target):\n    left, right, steps = 0, len(values) - 1, 0\n    while left <= right:\n        steps += 1; mid = (left + right) // 2\n        if values[mid] == target: return mid, steps\n        if values[mid] < target: left = mid + 1\n        else: right = mid - 1\n    return -1, steps\n\nli, ls = linear_steps(id_list, id_list[700]); bi, bs = binary_steps(id_list, id_list[700])\nassert li == bi == 700 and bs < ls\n"),
        ("## Урок. 7–9. Инвариант и gate", "SEARCH_INVARIANT = \"Бинарный поиск корректен только на отсортированном списке: после сравнения со средним элементом порядок доказывает, в какой половине цель невозможна. Без сортировки отбрасывание половины не обосновано.\"\nprobe = unsorted_txns[37]\npos = linear_search([row[0] for row in unsorted_txns], probe[0]); found_row = unsorted_txns[pos]\nchecks = {\"linear_contract\": linear_search([], 1) == -1, \"binary_edges\": binary_search([5], 5) == 0, \"binary_fewer_steps\": bs < ls, \"invariant_written\": len(SEARCH_INVARIANT) >= 140}\nassert set(checks.values()) == {True}\n"),
        ("## ДЗ. Part A", "targets = [unsorted_txns[i][0] for i in (0, 20, 100, 300)] + [-1]\nlinear_positions = [linear_search([r[0] for r in unsorted_txns], x) for x in targets]\ntargets_sorted = [id_list[i] for i in (0, 20, 100, 300)] + [-1]\nbinary_positions = [binary_search(id_list, x) for x in targets_sorted]\nedge_checks = [linear_search([], 1) == -1, binary_search([], 1) == -1, linear_search([1], 1) == 0, binary_search([1], 1) == 0, linear_search([1], 2) == -1, binary_search([1], 2) == -1]\nassert binary_positions == [0, 20, 100, 300, -1] and all(edge_checks)\n"),
        ("## ДЗ. Challenge", "def binary_search_first(values, target):\n    index = lower_bound(values, target)\n    return index if index < len(values) and values[index] == target else -1\n\nSEARCH_NOTE = \"Линейный поиск работает без preprocessing и стоит O(n) на запрос. Сортировка требует предварительной работы, зато бинарный запрос стоит O(log n). Ограничение: порядок должен поддерживаться после обновлений, иначе индекс становится некорректным.\"\nassert binary_search_first([1, 2, 2, 2, 5], 2) == 1 and len(SEARCH_NOTE) >= 220\n"),
    ]
    return lesson, hw, sol


def lesson02() -> tuple[list, list, list]:
    lesson = [
        ("## 1. Восстановите binary search", "def binary_search(values, target):\n    # TODO\n    ...\n\nassert binary_search(id_list, id_list[321]) == 321\nassert binary_search(id_list, -1) == -1\n"),
        ("## 2. Lower bound: первое `>= target`", "def lower_bound(values, target):\n    # TODO\n    ...\n\nassert lower_bound([1, 3, 3, 7], 3) == 1\nassert lower_bound([1, 3, 3, 7], 4) == 3\nassert lower_bound([], 4) == 0\n"),
        ("## 3. Upper bound: первое `> target`", "def upper_bound(values, target):\n    # TODO\n    ...\n\nassert upper_bound([1, 3, 3, 7], 3) == 3\nassert upper_bound([1, 3, 3, 7], 7) == 4\n"),
        ("## 4. Диапазон сумм `[5000, 12000]`", "lo = None  # TODO\nhi = None  # TODO\nrange_rows = None  # TODO\nassert range_rows == amount_txns[lo:hi]\nassert range_rows and min(r[1] for r in range_rows) >= 5000\nassert max(r[1] for r in range_rows) <= 12000\n"),
        ("## 5. Пустой диапазон", "empty_rows = None  # TODO: суммы выше максимума\nassert empty_rows == []\n"),
        ("## 6. Пачка txn_id", "targets = [id_list[i] for i in (7, 77, 177, 777)] + [-10]\npositions = None  # TODO\nassert positions == [7, 77, 177, 777, -1]\n"),
        ("## 7. Проверка границ по oracle", "probes = [0, 5000, 12000, 50000, 10**9]\nbound_checks = []  # TODO: сравните с фильтрацией/подсчётом\nassert len(bound_checks) == len(probes) and all(bound_checks)\n"),
        ("## 8. Сложность диапазона", "RANGE_NOTE = \"\"  # TODO: O(log n + k), где k — размер ответа\nassert len(RANGE_NOTE) >= 160\nassert \"k\" in RANGE_NOTE.lower() and \"log\" in RANGE_NOTE.lower()\n"),
        ("## 9. Самопроверка", "checks = {\"lower\": None, \"upper\": None, \"slice\": None, \"batch\": None}  # TODO\nassert set(checks.values()) == {True}\n"),
    ]
    hw = [
        ("### Part A — обязательно\n\n## A1. Число сумм не выше 10000", "count_le_10000 = None  # TODO: одна граница\nassert count_le_10000 == sum(x <= 10000 for x in amount_list)\n"),
        ("## A2. Три диапазона", "queries = [(0, 5000), (10000, 15000), (25000, 35000)]\ncounts = []  # TODO\nassert counts == [sum(a <= x <= b for x in amount_list) for a, b in queries]\n"),
        ("## A3. Вернуть txn_id диапазона", "ids_15_17 = None  # TODO\nassert ids_15_17 == [r[0] for r in amount_txns if 15000 <= r[1] <= 17000]\n"),
        ("### Challenge\n\n## B1. Универсальная функция", "def rows_in_amount_range(rows, amounts, low, high):\n    # TODO: включительные границы\n    ...\n\nresult = rows_in_amount_range(amount_txns, amount_list, 15000, 17000)\nassert result == [r for r in amount_txns if 15000 <= r[1] <= 17000]\n"),
        ("## B2. Контракт плохого диапазона", "bad_result = rows_in_amount_range(amount_txns, amount_list, 20, 10)\nRANGE_POLICY = \"\"  # TODO: выбранная политика для low > high\nassert bad_result == []\nassert len(RANGE_POLICY) >= 140\n"),
    ]
    sol = [
        ("## Урок. 1–3. Search и bounds", COMMON_SOLUTION + "\nassert lower_bound([1, 3, 3, 7], 3) == 1\nassert upper_bound([1, 3, 3, 7], 3) == 3\n"),
        ("## Урок. 4–5. Срезы", "lo, hi = lower_bound(amount_list, 5000), upper_bound(amount_list, 12000)\nrange_rows = amount_txns[lo:hi]\ne_lo = lower_bound(amount_list, max(amount_list) + 1); e_hi = upper_bound(amount_list, max(amount_list) + 100)\nempty_rows = amount_txns[e_lo:e_hi]\nassert range_rows and empty_rows == []\n"),
        ("## Урок. 6–7. Batch и oracle", "targets = [id_list[i] for i in (7, 77, 177, 777)] + [-10]\npositions = [binary_search(id_list, target) for target in targets]\nprobes = [0, 5000, 12000, 50000, 10**9]\nbound_checks = [lower_bound(amount_list, x) == sum(v < x for v in amount_list) for x in probes]\nassert positions == [7, 77, 177, 777, -1] and all(bound_checks)\n"),
        ("## Урок. 8–9. Сложность и gate", "RANGE_NOTE = \"Две границы находятся бинарным поиском за O(log n) каждая. Создание ответа требует O(k), где k — число возвращённых строк, поэтому полная стоимость запроса O(log n + k).\"\nchecks = {\"lower\": lower_bound([], 1) == 0, \"upper\": upper_bound([1], 1) == 1, \"slice\": range_rows == [r for r in amount_txns if 5000 <= r[1] <= 12000], \"batch\": positions[-1] == -1}\nassert set(checks.values()) == {True}\n"),
        ("## ДЗ. Part A", "count_le_10000 = upper_bound(amount_list, 10000)\nqueries = [(0, 5000), (10000, 15000), (25000, 35000)]\ncounts = [upper_bound(amount_list, b) - lower_bound(amount_list, a) for a, b in queries]\na, b = lower_bound(amount_list, 15000), upper_bound(amount_list, 17000)\nids_15_17 = [r[0] for r in amount_txns[a:b]]\nassert counts == [sum(a <= x <= b for x in amount_list) for a, b in queries]\n"),
        ("## ДЗ. Challenge", "def rows_in_amount_range(rows, amounts, low, high):\n    if low > high: return []\n    return rows[lower_bound(amounts, low):upper_bound(amounts, high)]\n\nresult = rows_in_amount_range(amount_txns, amount_list, 15000, 17000)\nbad_result = rows_in_amount_range(amount_txns, amount_list, 20, 10)\nRANGE_POLICY = \"При low > high функция возвращает пустой список: допустимых значений нет. Эта политика сохраняет тип результата и удобна для pipeline без отдельного исключения.\"\nassert bad_result == [] and len(RANGE_POLICY) >= 140\n"),
    ]
    return lesson, hw, sol


def lesson03() -> tuple[list, list, list]:
    lesson = [
        ("## 1. Один шаг selection", "values = [9, 1, 5, 3, 7]\nsmallest_index = None  # TODO\none_step = values.copy()  # TODO: переставьте минимум на позицию 0\nassert smallest_index == 1\nassert one_step == [1, 9, 5, 3, 7]\n"),
        ("## 2. Полный selection sort", "def selection_sort(values):\n    # TODO: не менять вход\n    ...\n\nsource = [4, 1, 4, -2, 0]\nassert selection_sort(source) == [-2, 0, 1, 4, 4]\nassert source == [4, 1, 4, -2, 0]\nassert selection_sort([]) == []\n"),
        ("## 3. Merge двух sorted списков", "def merge_sorted(left, right):\n    # TODO\n    ...\n\nassert merge_sorted([1, 4, 4, 9], [2, 4, 7]) == [1, 2, 4, 4, 4, 7, 9]\nassert merge_sorted([], [2]) == [2]\n"),
        ("## 4. Рекурсивный mergesort", "def merge_sort(values):\n    # TODO: base, split, recursive calls, merge\n    ...\n\nfor case in ([], [1], [3, 1, 2], [5, 2, 5, -1]):\n    assert merge_sort(case) == sorted(case)\n"),
        ("## 5. Partition quicksort", "def partition(values, pivot):\n    # TODO: вернуть less, equal, greater\n    ...\n\nless, equal, greater = partition([8, 2, 8, 4, 9, 8], 8)\nassert less == [2, 4] and equal == [8, 8, 8] and greater == [9]\n"),
        ("## 6. Число сравнений selection", "def selection_comparisons(n):\n    # TODO: число сравнений для длины n\n    ...\n\nassert selection_comparisons(0) == 0\nassert selection_comparisons(5) == 10\nassert selection_comparisons(100) == 4950\n"),
        ("## 7. Сортировка банковских сумм", "amounts80 = [r[1] for r in unsorted_txns[:80]]\nselection_result = None  # TODO\nmerge_result = None  # TODO\nassert selection_result == merge_result == sorted(amounts80)\n"),
        ("## 8. Сравнение стратегий", "SORT_NOTE = \"\"  # TODO: O(n²), O(n log n), quicksort worst case\nassert len(SORT_NOTE) >= 200\nassert \"o(n\" in SORT_NOTE.lower()\n"),
        ("## 9. Самопроверка", "checks = {\"copy\": None, \"duplicates\": None, \"empty\": None, \"bank_data\": None}  # TODO\nassert set(checks.values()) == {True}\n"),
    ]
    hw = [
        ("### Part A — обязательно\n\n## A1. Selection для risk_score", "risks = [r[3] for r in unsorted_txns[:120]]\nrisk_selection = None  # TODO\nassert risk_selection == sorted(risks)\n"),
        ("## A2. Mergesort для txn_id", "ids = [r[0] for r in unsorted_txns[:300]]\nid_merge = None  # TODO\nassert id_merge == sorted(ids)\n"),
        ("## A3. Property checks", "cases = [[], [1], [2, 1], [3, 3, 1], list(range(20, -1, -1))]\nproperty_checks = []  # TODO: обе функции для каждого case\nassert len(property_checks) == 2 * len(cases) and all(property_checks)\n"),
        ("### Challenge\n\n## B1. Учебный quicksort", "def quick_sort(values):\n    # TODO: не менять вход, корректно сохранить duplicates\n    ...\n\nassert quick_sort([3, 1, 3, 2, 3]) == [1, 2, 3, 3, 3]\nassert quick_sort([]) == []\n"),
        ("## B2. Худший случай", "QUICK_NOTE = \"\"  # TODO: pivot, неравные части, глубина, O(n²)\nassert len(QUICK_NOTE) >= 180\nassert \"pivot\" in QUICK_NOTE.lower() and \"o(n\" in QUICK_NOTE.lower()\n"),
    ]
    sol = [
        ("## Урок. 1–4. Selection, merge, mergesort", COMMON_SOLUTION + "\nvalues = [9, 1, 5, 3, 7]\nsmallest_index = min(range(len(values)), key=values.__getitem__)\none_step = values.copy(); one_step[0], one_step[smallest_index] = one_step[smallest_index], one_step[0]\nassert one_step == [1, 9, 5, 3, 7]\n"),
        ("## Урок. 5. Partition", "def partition(values, pivot):\n    return ([x for x in values if x < pivot], [x for x in values if x == pivot], [x for x in values if x > pivot])\n\nless, equal, greater = partition([8, 2, 8, 4, 9, 8], 8)\nassert len(less) + len(equal) + len(greater) == 6\n"),
        ("## Урок. 6–7. Работа и банковские данные", "def selection_comparisons(n):\n    return n * (n - 1) // 2\n\namounts80 = [r[1] for r in unsorted_txns[:80]]\nselection_result = selection_sort(amounts80); merge_result = merge_sort(amounts80)\nassert selection_result == merge_result == sorted(amounts80)\n"),
        ("## Урок. 8–9. Вывод и gate", "SORT_NOTE = \"Selection sort на каждом шаге просматривает остаток и делает O(n²) сравнений. Mergesort строит уровни разбиения и слияния за O(n log n). Quicksort в среднем похож по росту, но при неудачном pivot может деградировать до O(n²).\"\nsource = [4, 1, 4, -2, 0]; selection_sort(source)\nchecks = {\"copy\": source == [4, 1, 4, -2, 0], \"duplicates\": merge_sort([2, 2, 1]).count(2) == 2, \"empty\": selection_sort([]) == merge_sort([]) == [], \"bank_data\": selection_result == sorted(amounts80)}\nassert set(checks.values()) == {True}\n"),
        ("## ДЗ. Part A", "risks = [r[3] for r in unsorted_txns[:120]]; risk_selection = selection_sort(risks)\nids = [r[0] for r in unsorted_txns[:300]]; id_merge = merge_sort(ids)\ncases = [[], [1], [2, 1], [3, 3, 1], list(range(20, -1, -1))]\nproperty_checks = [fn(case) == sorted(case) for case in cases for fn in (selection_sort, merge_sort)]\nassert all(property_checks)\n"),
        ("## ДЗ. Challenge", "def quick_sort(values):\n    if len(values) <= 1: return list(values)\n    pivot = values[len(values) // 2]\n    less, equal, greater = partition(values, pivot)\n    return quick_sort(less) + equal + quick_sort(greater)\n\nQUICK_NOTE = \"Если pivot каждый раз оказывается минимумом или максимумом, одна часть почти пуста, глубина рекурсии становится n, а суммарная работа — O(n²). Случайный или медианный pivot уменьшает риск, но не отменяет худший случай.\"\nassert quick_sort([3, 1, 3, 2, 3]) == [1, 2, 3, 3, 3] and len(QUICK_NOTE) >= 180\n"),
    ]
    return lesson, hw, sol


def lesson04() -> tuple[list, list, list]:
    lesson = [
        ("## 1. Quality gate до измерений", "def selection_sort(values):\n    # TODO\n    ...\n\ndef merge_sort(values):\n    # TODO\n    ...\n\ncases = [[], [1], [2, 1], [3, 1, 3], list(range(30, -1, -1))]\ngate = []  # TODO\nassert len(gate) == 2 * len(cases) and all(gate)\n"),
        ("## 2. Median runtime", "def median_runtime(function, values, repeats=3):\n    # TODO: подготовка values уже сделана; вернуть медиану\n    ...\n\nprobe_time = median_runtime(sorted, amount_list[:100])\nassert isinstance(probe_time, float) and probe_time >= 0\n"),
        ("## 3. Таблица четырёх размеров", "sizes = [80, 160, 320, 640]\nrows = []  # TODO: dict n, selection_s, merge_s\nbenchmark = pd.DataFrame(rows)\nassert list(benchmark.columns) == [\"n\", \"selection_s\", \"merge_s\"]\nassert benchmark[\"n\"].tolist() == sizes\nassert (benchmark[[\"selection_s\", \"merge_s\"]] >= 0).all().all()\n"),
        ("## 4. Нормированный рост", "benchmark[\"selection_per_n2\"] = None  # TODO\nbenchmark[\"merge_per_nlogn\"] = None  # TODO\nassert benchmark[[\"selection_per_n2\", \"merge_per_nlogn\"]].notna().all().all()\n"),
        ("## 5. Встроенный baseline", "builtin_s = None  # TODO\nassert isinstance(builtin_s, float) and builtin_s >= 0\n"),
        ("## 6. Рост, а не победитель одного запуска", "growth_selection = None  # TODO: last / first, с защитой от нуля\ngrowth_merge = None  # TODO\nassert growth_selection >= 0 and growth_merge >= 0\n"),
        ("## 7. Повторяемость", "repeat_table = []  # TODO: 5 замеров sorted на одном input\nassert len(repeat_table) == 5\nassert all(value >= 0 for value in repeat_table)\n"),
        ("## 8. Честный вывод", "BENCH_NOTE = \"\"  # TODO: тренд, шум, машина, Big O, production sorted\nassert len(BENCH_NOTE) >= 240\nassert \"o(n\" in BENCH_NOTE.lower()\n"),
        ("## 9. Acceptance", "acceptance = {\"correct\": None, \"four_sizes\": None, \"median\": None, \"baseline\": None, \"honest_note\": None}  # TODO\nassert set(acceptance.values()) == {True}\n"),
    ]
    hw = [
        ("### Part A — обязательно\n\n## A1. Бенчмарк risk_score", "risk_rows = []  # TODO: n=100, 300, 600; selection и merge\nassert len(risk_rows) == 3\nassert all(len(row) == 3 for row in risk_rows)\n"),
        ("## A2. Две формы входа", "ordered = amount_list[:500]\nreversed_values = list(reversed(ordered))\nshape_times = {}  # TODO: merge для ordered/reversed\nassert set(shape_times) == {\"ordered\", \"reversed\"}\nassert all(v >= 0 for v in shape_times.values())\n"),
        ("## A3. Встроенная сортировка", "built_rows = []  # TODO: sorted для тех же трёх n\nassert len(built_rows) == 3\nassert all(t >= 0 for _, t in built_rows)\n"),
        ("### Challenge\n\n## B1. Счётчик сравнений", "def selection_sort_count(values):\n    # TODO: вернуть sorted_values, comparisons\n    ...\n\nresult, comparisons = selection_sort_count([4, 3, 2, 1])\nassert result == [1, 2, 3, 4] and comparisons == 6\n"),
        ("## B2. Методологическая записка", "METHOD_NOTE = \"\"  # TODO: warm-up, repeats, median, одинаковый input, ограничения\nassert len(METHOD_NOTE) >= 240\nassert all(word in METHOD_NOTE.lower() for word in [\"median\", \"input\"])\n"),
    ]
    sol = [
        ("## Урок. 1–2. Gate и таймер", COMMON_SOLUTION + "\ncases = [[], [1], [2, 1], [3, 1, 3], list(range(30, -1, -1))]\ngate = [fn(case) == sorted(case) for case in cases for fn in (selection_sort, merge_sort)]\nprobe_time = median_runtime(sorted, amount_list[:100])\nassert all(gate) and probe_time >= 0\n"),
        ("## Урок. 3–4. Таблица", "sizes = [80, 160, 320, 640]\nrows = []\nfor n in sizes:\n    values = [r[1] for r in unsorted_txns[:n]]\n    rows.append({\"n\": n, \"selection_s\": median_runtime(selection_sort, values), \"merge_s\": median_runtime(merge_sort, values)})\nbenchmark = pd.DataFrame(rows)\nbenchmark[\"selection_per_n2\"] = benchmark[\"selection_s\"] / benchmark[\"n\"].pow(2)\nbenchmark[\"merge_per_nlogn\"] = benchmark[\"merge_s\"] / (benchmark[\"n\"] * benchmark[\"n\"].map(math.log2))\nassert len(benchmark) == 4\n"),
        ("## Урок. 5–7. Baseline и повторы", "builtin_s = median_runtime(sorted, amount_list[:640], 5)\ndef safe_ratio(a, b): return a / b if b else 0.0\ngrowth_selection = safe_ratio(benchmark.iloc[-1].selection_s, benchmark.iloc[0].selection_s)\ngrowth_merge = safe_ratio(benchmark.iloc[-1].merge_s, benchmark.iloc[0].merge_s)\nrepeat_table = [median_runtime(sorted, amount_list[:640], 1) for _ in range(5)]\nassert len(repeat_table) == 5\n"),
        ("## Урок. 8–9. Вывод", "BENCH_NOTE = \"Таблица показывает тренд: ручной selection растёт ближе к O(n²), а merge — к O(n log n). Отдельный замер шумит из-за машины и планировщика, поэтому использована median повторов. Эксперимент согласуется с моделью, но не доказывает Big O. Для production выбираем встроенный sorted как протестированный baseline.\"\nacceptance = {\"correct\": all(gate), \"four_sizes\": len(benchmark) == 4, \"median\": True, \"baseline\": builtin_s >= 0, \"honest_note\": len(BENCH_NOTE) >= 240}\nassert set(acceptance.values()) == {True}\n"),
        ("## ДЗ. Part A", "risk_rows = []\nfor n in (100, 300, 600):\n    values = [r[3] for r in unsorted_txns[:n]]\n    risk_rows.append([n, median_runtime(selection_sort, values), median_runtime(merge_sort, values)])\nordered = amount_list[:500]; reversed_values = list(reversed(ordered))\nshape_times = {\"ordered\": median_runtime(merge_sort, ordered), \"reversed\": median_runtime(merge_sort, reversed_values)}\nbuilt_rows = [(n, median_runtime(sorted, amount_list[:n])) for n in (100, 300, 600)]\nassert len(risk_rows) == len(built_rows) == 3\n"),
        ("## ДЗ. Challenge", "def selection_sort_count(values):\n    result = list(values); comparisons = 0\n    for i in range(len(result)):\n        smallest = i\n        for j in range(i + 1, len(result)):\n            comparisons += 1\n            if result[j] < result[smallest]: smallest = j\n        result[i], result[smallest] = result[smallest], result[i]\n    return result, comparisons\n\nMETHOD_NOTE = \"Перед серией нужен короткий warm-up. Все алгоритмы получают одинаковый input, созданный до таймера; каждый запуск работает с копией. Используются repeats и median, а не минимум одного запуска. Ограничения: фоновые процессы, версия Python и малый диапазон n влияют на числа, поэтому интерпретируем форму роста, а не абсолютный рекорд.\"\nassert selection_sort_count([4, 3, 2, 1])[1] == 6 and len(METHOD_NOTE) >= 240\n"),
    ]
    return lesson, hw, sol


def lesson05() -> tuple[list, list, list]:
    lesson = [
        ("## 1. `key` по amount", "by_amount_local = None  # TODO\nassert by_amount_local == sorted(unsorted_txns, key=lambda row: row[1])\nassert [r[1] for r in by_amount_local] == sorted(r[1] for r in unsorted_txns)\n"),
        ("## 2. Два ключа\n\nRisk по убыванию, при равенстве amount по возрастанию.", "by_risk_amount = None  # TODO\nassert by_risk_amount == sorted(unsorted_txns, key=lambda row: (-row[3], row[1]))\n"),
        ("## 3. Трасса указателей", "toy = [2, 5, 9, 14, 21]\ntarget = 23\npointer_trace = []  # TODO: (left, right, sum) до встречи\nassert pointer_trace and pointer_trace[0] == (0, 4, 23)\n"),
        ("## 4. Ближайшая сумма пары", "def two_sum_closest(sorted_values, target):\n    # TODO: вернуть (left_value, right_value, absolute_difference)\n    ...\n\nassert two_sum_closest([1, 4, 8, 13], 10) == (1, 8, 1)\nresult = two_sum_closest(amount_list, 40000)\nassert len(result) == 3 and result[0] <= result[1] and result[2] >= 0\n"),
        ("## 5. Число пар не ниже порога", "def count_pairs_ge(sorted_values, threshold):\n    # TODO\n    ...\n\ntoy_values = [1, 3, 5, 8]\nassert count_pairs_ge(toy_values, 9) == 3\n"),
        ("## 6. Oracle на малом списке", "small = amount_list[:40]\nthreshold = 12000\nfast_count = None  # TODO\nslow_count = sum(small[i] + small[j] >= threshold for i in range(len(small)) for j in range(i + 1, len(small)))\nassert fast_count == slow_count\n"),
        ("## 7. Несколько целей после одной сортировки", "targets = [20000, 30000, 40000, 50000]\nclosest_rows = []  # TODO\nassert len(closest_rows) == len(targets)\nassert all(len(row) == 4 for row in closest_rows)  # target, a, b, diff\n"),
        ("## 8. Стоимость pipeline", "POINTER_NOTE = \"\"  # TODO: сортировка O(n log n), запрос O(n), повторное использование\nassert len(POINTER_NOTE) >= 200\nassert \"o(n\" in POINTER_NOTE.lower()\n"),
        ("## 9. Самопроверка", "checks = {\"keys\": None, \"closest\": None, \"count_oracle\": None, \"distinct_indices\": None}  # TODO\nassert set(checks.values()) == {True}\n"),
    ]
    hw = [
        ("### Part A — обязательно\n\n## A1. Top-15 risk", "top_risk_ids = None  # TODO\nexpected = [r[0] for r in sorted(unsorted_txns, key=lambda r: (-r[3], r[1]))[:15]]\nassert top_risk_ids == expected\n"),
        ("## A2. Ближайшие пары для трёх целей", "targets = [25000, 45000, 65000]\nanswers = None  # TODO: target -> (a, b, diff)\nassert set(answers) == set(targets)\nassert all(len(value) == 3 for value in answers.values())\n"),
        ("## A3. Пары от 45000", "pairs_45k = None  # TODO\nslow_45k = sum(amount_list[i] + amount_list[j] >= 45000 for i in range(len(amount_list)) for j in range(i + 1, len(amount_list)))\nassert pairs_45k == slow_45k\n"),
        ("### Challenge\n\n## B1. Вернуть id транзакций", "def closest_transaction_pair(rows, target):\n    # TODO: rows сортируются по amount; вернуть два txn_id и diff\n    ...\n\npair = closest_transaction_pair(tiny_txns, 40000)\nassert len(pair) == 3 and pair[0] != pair[1] and pair[2] >= 0\n"),
        ("## B2. Доказательство движения", "MOVE_NOTE = \"\"  # TODO: почему малая сумма двигает left, большая — right\nassert len(MOVE_NOTE) >= 200\nassert all(word in MOVE_NOTE.lower() for word in [\"left\", \"right\"])\n"),
    ]
    sol = [
        ("## Урок. 1–3. Ключи и трасса", "by_amount_local = sorted(unsorted_txns, key=lambda row: row[1])\nby_risk_amount = sorted(unsorted_txns, key=lambda row: (-row[3], row[1]))\ntoy = [2, 5, 9, 14, 21]; target = 23; left, right, pointer_trace = 0, 4, []\nwhile left < right:\n    total = toy[left] + toy[right]; pointer_trace.append((left, right, total))\n    if total < target: left += 1\n    else: right -= 1\nassert pointer_trace[0] == (0, 4, 23)\n"),
        ("## Урок. 4–5. Два указателя", "def two_sum_closest(sorted_values, target):\n    left, right = 0, len(sorted_values) - 1\n    best = (sorted_values[left], sorted_values[right], abs(sorted_values[left] + sorted_values[right] - target))\n    while left < right:\n        total = sorted_values[left] + sorted_values[right]; diff = abs(total - target)\n        if diff < best[2]: best = (sorted_values[left], sorted_values[right], diff)\n        if total < target: left += 1\n        else: right -= 1\n    return best\n\ndef count_pairs_ge(sorted_values, threshold):\n    left, right, count = 0, len(sorted_values) - 1, 0\n    while left < right:\n        if sorted_values[left] + sorted_values[right] >= threshold:\n            count += right - left; right -= 1\n        else: left += 1\n    return count\n\nassert two_sum_closest([1, 4, 8, 13], 10) == (1, 8, 1)\nassert count_pairs_ge([1, 3, 5, 8], 9) == 3\n"),
        ("## Урок. 6–7. Oracle и queries", "small = amount_list[:40]; threshold = 12000\nfast_count = count_pairs_ge(small, threshold)\nslow_count = sum(small[i] + small[j] >= threshold for i in range(len(small)) for j in range(i + 1, len(small)))\ntargets = [20000, 30000, 40000, 50000]\nclosest_rows = [(target, *two_sum_closest(amount_list, target)) for target in targets]\nassert fast_count == slow_count\n"),
        ("## Урок. 8–9. Вывод", "POINTER_NOTE = \"Сначала данные сортируются за O(n log n). После этого один запрос двумя указателями проходит массив за O(n), причём индексы не возвращаются назад. Если запросов много, один и тот же отсортированный список используется повторно, и стоимость preprocessing не платится каждый раз.\"\nchecks = {\"keys\": [row[1] for row in by_amount_local] == amount_list, \"closest\": len(two_sum_closest(amount_list, 40000)) == 3, \"count_oracle\": fast_count == slow_count, \"distinct_indices\": True}\nassert set(checks.values()) == {True}\n"),
        ("## ДЗ. Part A", "top_risk_ids = [r[0] for r in sorted(unsorted_txns, key=lambda r: (-r[3], r[1]))[:15]]\ntargets = [25000, 45000, 65000]\nanswers = {target: two_sum_closest(amount_list, target) for target in targets}\npairs_45k = count_pairs_ge(amount_list, 45000)\nslow_45k = sum(amount_list[i] + amount_list[j] >= 45000 for i in range(len(amount_list)) for j in range(i + 1, len(amount_list)))\nassert pairs_45k == slow_45k\n"),
        ("## ДЗ. Challenge", "def closest_transaction_pair(rows, target):\n    ordered = sorted(rows, key=lambda r: r[1]); left, right = 0, len(ordered) - 1\n    best = (ordered[left][0], ordered[right][0], abs(ordered[left][1] + ordered[right][1] - target))\n    while left < right:\n        total = ordered[left][1] + ordered[right][1]; diff = abs(total - target)\n        if diff < best[2]: best = (ordered[left][0], ordered[right][0], diff)\n        if total < target: left += 1\n        else: right -= 1\n    return best\n\npair = closest_transaction_pair(tiny_txns, 40000)\nMOVE_NOTE = \"Если сумма меньше цели, уменьшение right сделает её ещё меньше, поэтому двигаем left к большему значению. Если сумма больше цели, увеличение left только ухудшит превышение, поэтому двигаем right к меньшему значению. Сортировка делает эти выводы гарантированными.\"\nassert pair[0] != pair[1] and len(MOVE_NOTE) >= 200\n"),
    ]
    return lesson, hw, sol


def lesson06() -> tuple[list, list, list]:
    lesson = [
        ("## 1. Merge строк по amount", "def merge_rows_by_amount(left_rows, right_rows):\n    # TODO\n    ...\n\nleft_rows, right_rows = amount_txns[:40], amount_txns[40:80]\nmerged = merge_rows_by_amount(left_rows, right_rows)\nassert len(merged) == 80\nassert merged == sorted(left_rows + right_rows, key=lambda r: r[1])\n"),
        ("## 2. Минимальный разрыв двух окон", "def min_gap_between_sorted(left_values, right_values):\n    # TODO\n    ...\n\nwindow_a, window_b = amount_list[40:120], amount_list[400:480]\ngap = min_gap_between_sorted(window_a, window_b)\nslow_gap = min(abs(a - b) for a in window_a for b in window_b)\nassert gap == slow_gap\n"),
        ("## 3. Пересечение sorted id", "def intersect_sorted(left_values, right_values):\n    # TODO\n    ...\n\nassert intersect_sorted([1, 2, 4, 8], [2, 3, 4, 9]) == [2, 4]\n"),
        ("## 4. Multi-key рейтинг", "top10 = None  # TODO: risk desc, day asc, amount desc\nexpected = sorted(unsorted_txns, key=lambda r: (-r[3], r[2], -r[1]))[:10]\nassert top10 == expected\n"),
        ("## 5. Oracle для min gap", "toy_cases = [([1], [8]), ([1, 5, 10], [2, 9]), ([1, 2], [2, 3])]\ngap_checks = []  # TODO\nassert len(gap_checks) == len(toy_cases) and all(gap_checks)\n"),
        ("## 6. Два окна id из лога", "first_ids = sorted(r[0] for r in unsorted_txns[:500])\nsecond_ids = sorted(r[0] for r in unsorted_txns[300:800])\nshared_ids = None  # TODO\nassert shared_ids == sorted(set(first_ids) & set(second_ids))\n"),
        ("## 7. Сводка результатов", "summary = {\"merged_rows\": None, \"min_gap\": None, \"shared_ids\": None, \"top_risk\": None}  # TODO\nassert summary[\"merged_rows\"] == 80\nassert summary[\"min_gap\"] == gap\nassert summary[\"shared_ids\"] == len(shared_ids)\n"),
        ("## 8. Мини-отчёт", "MINI_REPORT = \"\"  # TODO: 220+ символов, только проверенные числа, без причинности\nassert len(MINI_REPORT) >= 220\nassert str(gap) in MINI_REPORT and str(len(shared_ids)) in MINI_REPORT\n"),
        ("## 9. Acceptance", "acceptance = {\"merge\": None, \"gap_oracle\": None, \"intersection\": None, \"report\": None}  # TODO\nassert set(acceptance.values()) == {True}\n"),
    ]
    hw = [
        ("### Part A — обязательно\n\n## A1. Tiny по трём ключам", "tiny_sorted = None  # TODO: day asc, risk desc, amount asc\nassert tiny_sorted == sorted(tiny_txns, key=lambda r: (r[2], -r[3], r[1]))\n"),
        ("## A2. Разрыв половин tiny", "left_amounts = sorted(r[1] for r in tiny_txns[:40])\nright_amounts = sorted(r[1] for r in tiny_txns[40:])\ntiny_gap = None  # TODO\nassert tiny_gap == min(abs(a - b) for a in left_amounts for b in right_amounts)\n"),
        ("## A3. Общие id двух выборок", "a_ids = sorted(r[0] for r in unsorted_txns[:250])\nb_ids = sorted(r[0] for r in unsorted_txns[150:400])\ncommon = None  # TODO\nassert common == sorted(set(a_ids) & set(b_ids))\n"),
        ("### Challenge\n\n## B1. Audit function", "def audit_windows(rows_a, rows_b):\n    # TODO: merged_by_amount, min_amount_gap, shared_ids\n    ...\n\nreport = audit_windows(unsorted_txns[:100], unsorted_txns[50:150])\nassert set(report) == {\"merged_by_amount\", \"min_amount_gap\", \"shared_ids\"}\nassert report[\"shared_ids\"] == sorted(set(r[0] for r in unsorted_txns[:100]) & set(r[0] for r in unsorted_txns[50:150]))\n"),
        ("## B2. Ops note", "OPS_NOTE = \"\"  # TODO: что вычислено, сложность, ограничение интерпретации\nassert len(OPS_NOTE) >= 240\nassert \"o(n\" in OPS_NOTE.lower()\n"),
    ]
    sol = [
        ("## Урок. 1. Merge rows", "def merge_rows_by_amount(left_rows, right_rows):\n    i = j = 0; result = []\n    while i < len(left_rows) and j < len(right_rows):\n        if left_rows[i][1] <= right_rows[j][1]: result.append(left_rows[i]); i += 1\n        else: result.append(right_rows[j]); j += 1\n    return result + left_rows[i:] + right_rows[j:]\n\nleft_rows, right_rows = amount_txns[:40], amount_txns[40:80]\nmerged = merge_rows_by_amount(left_rows, right_rows)\nassert merged == sorted(left_rows + right_rows, key=lambda r: r[1])\n"),
        ("## Урок. 2–3. Gap и intersection", "def min_gap_between_sorted(left_values, right_values):\n    i = j = 0; best = math.inf\n    while i < len(left_values) and j < len(right_values):\n        best = min(best, abs(left_values[i] - right_values[j]))\n        if best == 0: return 0\n        if left_values[i] < right_values[j]: i += 1\n        else: j += 1\n    return best\n\ndef intersect_sorted(left_values, right_values):\n    i = j = 0; result = []\n    while i < len(left_values) and j < len(right_values):\n        if left_values[i] == right_values[j]: result.append(left_values[i]); i += 1; j += 1\n        elif left_values[i] < right_values[j]: i += 1\n        else: j += 1\n    return result\n\nwindow_a, window_b = amount_list[40:120], amount_list[400:480]\ngap = min_gap_between_sorted(window_a, window_b)\nassert gap == min(abs(a - b) for a in window_a for b in window_b)\n"),
        ("## Урок. 4–6. Рейтинг и oracles", "top10 = sorted(unsorted_txns, key=lambda r: (-r[3], r[2], -r[1]))[:10]\ntoy_cases = [([1], [8]), ([1, 5, 10], [2, 9]), ([1, 2], [2, 3])]\ngap_checks = [min_gap_between_sorted(a, b) == min(abs(x-y) for x in a for y in b) for a, b in toy_cases]\nfirst_ids = sorted(r[0] for r in unsorted_txns[:500]); second_ids = sorted(r[0] for r in unsorted_txns[300:800])\nshared_ids = intersect_sorted(first_ids, second_ids)\nassert all(gap_checks) and shared_ids == sorted(set(first_ids) & set(second_ids))\n"),
        ("## Урок. 7–9. Summary", "summary = {\"merged_rows\": len(merged), \"min_gap\": gap, \"shared_ids\": len(shared_ids), \"top_risk\": top10[0][0]}\nMINI_REPORT = f\"Слияние сохранило {len(merged)} строк в порядке amount. Минимальный разрыв сумм между окнами равен {gap}; oracle полного перебора дал то же значение. Пересечение окон содержит {len(shared_ids)} txn_id. Это описание структуры выборок, а не доказательство причины риска или поведения клиента.\"\nacceptance = {\"merge\": len(merged) == 80, \"gap_oracle\": all(gap_checks), \"intersection\": shared_ids == sorted(set(first_ids) & set(second_ids)), \"report\": len(MINI_REPORT) >= 220}\nassert set(acceptance.values()) == {True}\n"),
        ("## ДЗ. Part A", "tiny_sorted = sorted(tiny_txns, key=lambda r: (r[2], -r[3], r[1]))\nleft_amounts = sorted(r[1] for r in tiny_txns[:40]); right_amounts = sorted(r[1] for r in tiny_txns[40:])\ntiny_gap = min_gap_between_sorted(left_amounts, right_amounts)\na_ids = sorted(r[0] for r in unsorted_txns[:250]); b_ids = sorted(r[0] for r in unsorted_txns[150:400])\ncommon = intersect_sorted(a_ids, b_ids)\nassert common == sorted(set(a_ids) & set(b_ids))\n"),
        ("## ДЗ. Challenge", "def audit_windows(rows_a, rows_b):\n    left = sorted(rows_a, key=lambda r: r[1]); right = sorted(rows_b, key=lambda r: r[1])\n    return {\"merged_by_amount\": merge_rows_by_amount(left, right), \"min_amount_gap\": min_gap_between_sorted([r[1] for r in left], [r[1] for r in right]), \"shared_ids\": intersect_sorted(sorted(r[0] for r in rows_a), sorted(r[0] for r in rows_b))}\n\nreport = audit_windows(unsorted_txns[:100], unsorted_txns[50:150])\nOPS_NOTE = \"После сортировки каждого окна слияние и пересечение выполняются за O(n + m); минимальный разрыв также требует одного прохода. Audit возвращает воспроизводимые факты о двух выборках. Ограничение: совпадение id и близость amount не объясняют риск и требуют бизнес-контекста.\"\nassert len(OPS_NOTE) >= 240\n"),
    ]
    return lesson, hw, sol


def lesson07() -> tuple[list, list, list]:
    lesson = [
        ("## 1. Контракт библиотеки", "API = [\"linear_search\", \"binary_search\", \"lower_bound\", \"upper_bound\", \"selection_sort\", \"merge_sort\"]\nassert len(API) == len(set(API)) == 6\n"),
        ("## 2. Search API", "def linear_search(values, target):\n    # TODO\n    ...\n\ndef binary_search(values, target):\n    # TODO\n    ...\n\ndef lower_bound(values, target):\n    # TODO\n    ...\n\ndef upper_bound(values, target):\n    # TODO\n    ...\n"),
        ("## 3. Sort API", "def selection_sort(values):\n    # TODO\n    ...\n\ndef merge_sort(values):\n    # TODO\n    ...\n"),
        ("## 4. Параметризованный quality gate", "cases = [[], [1], [2, 1], [3, 1, 3], list(range(25, -1, -1))]\nquality = {\"linear\": None, \"binary\": None, \"bounds\": None, \"selection\": None, \"merge\": None, \"input_preserved\": None}  # TODO\nassert set(quality.values()) == {True}\n"),
        ("## 5. Benchmark четырёх размеров", "sizes = [80, 160, 320, 640]\nbenchmark_rows = []  # TODO: n, selection_s, merge_s, ratio\nbenchmark = pd.DataFrame(benchmark_rows)\nassert len(benchmark) == 4\nassert {\"n\", \"selection_s\", \"merge_s\", \"ratio\"} == set(benchmark.columns)\nassert (benchmark[[\"selection_s\", \"merge_s\", \"ratio\"]] >= 0).all().all()\n"),
        ("## 6. Проверка диапазонного запроса", "lo, hi = None, None  # TODO: 10000..20000\nrange_rows = None  # TODO\nassert range_rows == [r for r in amount_txns if 10000 <= r[1] <= 20000]\n"),
        ("## 7. Acceptance checklist", "acceptance = pd.Series({\"api_complete\": None, \"quality_gate\": None, \"benchmark_4_sizes\": None, \"range_query\": None, \"report_ready\": None})  # TODO\nassert acceptance.index.tolist() == [\"api_complete\", \"quality_gate\", \"benchmark_4_sizes\", \"range_query\", \"report_ready\"]\n"),
        ("## 8. Итоговый REPORT", "REPORT = \"\"  # TODO: ≥350 символов; evidence, O(n²)/O(n log n), sorted baseline, ограничения\nREADY = None  # TODO: вычислить из acceptance\nassert len(REPORT) >= 350\nassert READY is True\nassert all(token in REPORT.lower() for token in [\"o(n\", \"огранич\"])\n"),
        ("## 9. Экспорт артефакта", "artifact_manifest = {\"library\": \"bank_logs.py\", \"benchmark\": \"benchmark.csv\", \"report\": \"REPORT.md\", \"ready\": READY}\nassert artifact_manifest[\"ready\"] is True\nassert set(artifact_manifest) == {\"library\", \"benchmark\", \"report\", \"ready\"}\n"),
    ]
    hw = [
        ("### Part A — обязательно\n\n## A1. Gate на новых случаях", "new_cases = [[0, -1, 0], [5] * 20, list(range(50))]\nnew_gate = []  # TODO: selection и merge\nassert len(new_gate) == 2 * len(new_cases) and all(new_gate)\n"),
        ("## A2. Benchmark risk_score", "risk_rows = []  # TODO: n=100, 300, 600\nassert len(risk_rows) == 3\nassert all(len(row) == 4 for row in risk_rows)\n"),
        ("## A3. Сравнение с sorted", "builtin_rows = []  # TODO: те же n, median runtime sorted\nassert len(builtin_rows) == 3\nassert all(t >= 0 for _, t in builtin_rows)\n"),
        ("### Challenge\n\n## B1. Единая функция аудита", "def audit_algorithms(values, targets):\n    # TODO: sorted copy, позиции targets, quality bool\n    ...\n\nresult = audit_algorithms([5, 1, 3, 3], [1, 3, 9])\nassert result[\"sorted\"] == [1, 3, 3, 5]\nassert result[\"positions\"] == [0, 1, -1]\nassert result[\"quality\"] is True\n"),
        ("## B2. Рефлексия блока", "REFLECTION = \"\"  # TODO: ≥300 символов; поиск, сортировка, pointers, evidence, limitation\nassert len(REFLECTION) >= 300\nassert all(word in REFLECTION.lower() for word in [\"поиск\", \"сорт\", \"указател\", \"огранич\"])\n"),
    ]
    sol = [
        ("## Урок. 1–3. Полный API", COMMON_SOLUTION + "\nAPI = [\"linear_search\", \"binary_search\", \"lower_bound\", \"upper_bound\", \"selection_sort\", \"merge_sort\"]\nassert len(API) == 6\n"),
        ("## Урок. 4. Quality gate", "cases = [[], [1], [2, 1], [3, 1, 3], list(range(25, -1, -1))]\nprobe = [3, 1, 3]; selection_sort(probe); merge_sort(probe)\nquality = {\"linear\": linear_search([1, 2], 3) == -1, \"binary\": binary_search([1, 2], 2) == 1, \"bounds\": lower_bound([1, 2, 2], 2) == 1 and upper_bound([1, 2, 2], 2) == 3, \"selection\": all(selection_sort(c) == sorted(c) for c in cases), \"merge\": all(merge_sort(c) == sorted(c) for c in cases), \"input_preserved\": probe == [3, 1, 3]}\nassert set(quality.values()) == {True}\n"),
        ("## Урок. 5. Benchmark", "sizes = [80, 160, 320, 640]; benchmark_rows = []\nfor n in sizes:\n    values = [r[1] for r in unsorted_txns[:n]]\n    ts = median_runtime(selection_sort, values); tm = median_runtime(merge_sort, values)\n    benchmark_rows.append({\"n\": n, \"selection_s\": ts, \"merge_s\": tm, \"ratio\": ts / tm if tm else 0.0})\nbenchmark = pd.DataFrame(benchmark_rows)\nassert len(benchmark) == 4\n"),
        ("## Урок. 6. Range query", "lo, hi = lower_bound(amount_list, 10000), upper_bound(amount_list, 20000)\nrange_rows = amount_txns[lo:hi]\nassert range_rows == [r for r in amount_txns if 10000 <= r[1] <= 20000]\n"),
        ("## Урок. 7–9. Acceptance и REPORT", "REPORT = \"Библиотека реализует линейный и бинарный поиск, границы диапазона, selection sort и mergesort. Quality gate проверяет пустые списки, дубликаты, отсутствие цели и сохранение входа. Benchmark на четырёх размерах даёт evidence согласованного роста: selection соответствует O(n²), merge — O(n log n), а встроенный sorted остаётся production baseline. Диапазонный запрос проверен прямой фильтрацией. Ограничение: учебные размеры, конкретная машина и шум времени не доказывают асимптотику и не объясняют банковский риск.\"\nacceptance = pd.Series({\"api_complete\": len(API) == 6, \"quality_gate\": all(quality.values()), \"benchmark_4_sizes\": len(benchmark) == 4, \"range_query\": range_rows == [r for r in amount_txns if 10000 <= r[1] <= 20000], \"report_ready\": len(REPORT) >= 350})\nREADY = bool(acceptance.all())\nartifact_manifest = {\"library\": \"bank_logs.py\", \"benchmark\": \"benchmark.csv\", \"report\": \"REPORT.md\", \"ready\": READY}\nassert READY is True\n"),
        ("## ДЗ. Part A", "new_cases = [[0, -1, 0], [5] * 20, list(range(50))]\nnew_gate = [fn(c) == sorted(c) for c in new_cases for fn in (selection_sort, merge_sort)]\nrisk_rows = []\nfor n in (100, 300, 600):\n    values = [r[3] for r in unsorted_txns[:n]]; ts = median_runtime(selection_sort, values); tm = median_runtime(merge_sort, values)\n    risk_rows.append([n, ts, tm, ts / tm if tm else 0.0])\nbuiltin_rows = [(n, median_runtime(sorted, [r[3] for r in unsorted_txns[:n]])) for n in (100, 300, 600)]\nassert all(new_gate) and len(risk_rows) == len(builtin_rows) == 3\n"),
        ("## ДЗ. Challenge", "def audit_algorithms(values, targets):\n    ordered = merge_sort(values)\n    positions = [binary_search(ordered, target) for target in targets]\n    return {\"sorted\": ordered, \"positions\": positions, \"quality\": ordered == sorted(values) and values == list(values)}\n\nresult = audit_algorithms([5, 1, 3, 3], [1, 3, 9])\nREFLECTION = \"Блок связал поиск с предпосылкой порядка: линейный поиск универсален, бинарный использует сортировку. Selection и mergesort показали разный рост, а два указателя превратили порядок в правило движения без вложенного перебора. Решение принимается по evidence тестов и benchmark, не по одному замеру. Ограничение: учебные данные и время машины не заменяют production profiling и бизнес-проверку.\"\nassert result[\"positions\"] == [0, 1, -1] and len(REFLECTION) >= 300\n"),
    ]
    return lesson, hw, sol


BUILDERS = [lesson01, lesson02, lesson03, lesson04, lesson05, lesson06, lesson07]


def lesson_plan(meta: dict) -> str:
    outcomes = [item.strip() for item in meta["outcomes"].split(";")]
    stage_rows = "\n".join(
        f"| {i} | {name} | {minutes} | {student} | {teacher} | `{material}` | {criterion} |"
        for i, (name, minutes, student, teacher, material, criterion) in enumerate(meta["stages"], 1)
    )
    error_rows = "\n".join(f"| {symptom} | {response} |" for symptom, response in meta["errors"])
    outcome_rows = "\n".join(f"{i}. {text[0].upper() + text[1:]}." for i, text in enumerate(outcomes, 1))
    next_link = (
        f"[{meta['next'].split(' — ')[0]}](../{LESSONS[LESSONS.index(meta) + 1]['dir']}/LESSON.md)"
        if meta is not LESSONS[-1]
        else meta["next"]
    )
    return f"""# Lesson Design: {meta["title"]}

## A. Сценарий пары

| Поле | Значение |
|---|---|
| Модуль | Массивы: поиск и сортировка (`08_07`) |
| Название урока | {meta["title"]} |
| Пара КТП | **{meta["pair"]}** |
| Длительность | 2 академических часа (**80 минут**) |
| Роль | {meta["role"]} |
| Пререквизиты | {meta["prereq"]} |
| **Открыть** | [lesson.ipynb](lesson.ipynb) — копия на ученика; первая code-ячейка загружает локальные CSV |
| **Первая фраза** | «{meta["first"]}» |
| **Минимум сдачи** | {meta["minimum"]} |
| **Домашнее задание** | [homework.ipynb](homework.ipynb) — Part A обязательно; Challenge по возможности (~1 ч) |
| **Дальше** | {next_link} |
| **Canvas** | не опубликовано |

### A. Чего хотим от пары

Главное — {meta["idea"][0].lower() + meta["idea"][1:]} Ученик не копирует готовый алгоритм: каждая функция начинается со stub и завершается исполняемым контрактом через `assert`.

Побочно ученик читает банковский лог как массив кортежей `(txn_id, amount, day, risk_score)`. Поля клиента не интерпретируются как причины риска: данные задают реалистичный контекст для алгоритма.

---

## B. Ход пары

| # | Этап | ~мин | Ученик | Учитель | Материал | Критерий закрытия |
|---|---|---:|---|---|---|---|
{stage_rows}

Обязательные этапы для минимума сдачи: **1–6**. Последний этап включает самостоятельную проверку и постановку ДЗ.

---

## C. Если сбились

### Типичные ошибки

| Симптом / мысль ученика | Что сказать или показать |
|---|---|
{error_rows}

### Дифференциация (кратко)

| | |
|---|---|
| Слабее базы | Выполнить §§1–6 с трассировкой на toy-списке; в ДЗ — Part A без Challenge |
| Сильнее базы | Выполнить §§7–9 без подсказок; в ДЗ — оба задания Challenge и дополнительный edge case |

---

## D. Проектирование

### Зачем урок

{meta["idea"]} Это часть сквозного артефакта `bank_logs.py`: результат пары должен переноситься из ноутбука в проверяемую функцию, а не оставаться устным определением.

### Центральная идея

| Поле | Значение |
|---|---|
| Центральная идея | {meta["idea"]} |
| Что поддерживает, но не отвлекает | pandas используется только для чтения CSV; алгоритмы работают со списками и кортежами |
| Данные урока | четыре CSV-копии рядом с ноутбуком; схема и канон — [data/README.md](../../data/README.md) |

### Результаты обучения

{outcome_rows}

### Профессиональный контекст

Поиск идентификатора, диапазонный запрос, сортировка событий и сравнение роста встречаются в preprocessing и инфраструктуре данных. Здесь это алгоритмы в памяти: индексы БД, внешняя сортировка и hash map остаются вне scope модуля.

### Решения учащегося

| # | Какой выбор делает учащийся | На что влияет |
|---|---|---|
| 1 | Какой инвариант и контракт сохранить | Корректность на edge cases и возможность повторного использования |
| 2 | Как проверить результат независимо | Доверие к выводу: `assert`, oracle или benchmark protocol |
| 3 | Как сформулировать ограничение | Различение измерения, асимптотики и бизнес-интерпретации |

### Материалы (зачем каждый)

- [x] [lesson.ipynb](lesson.ipynb) — guided practice, девять секций со stub и assert
- [x] [homework.ipynb](homework.ipynb) — Part A + Challenge
- [x] [solutions.ipynb](solutions.ipynb) — секционный эталон урока и ДЗ (только преподаватель)
- [x] локальные CSV — ноутбук запускается из папки урока
- [ ] презентация — не нужна

### Домашнее задание

| Поле | Значение |
|---|---|
| Назначается | **да** |
| Файл | [homework.ipynb](homework.ipynb) |
| Формулировка | Part A закрепляет контракты пары; Challenge обобщает алгоритм и требует инженерного объяснения |
| Ориентир времени | **~1 ч** (0,5–2 ч) |
| Почему не на уроке | Обобщение, edge cases и письменная аргументация требуют самостоятельного времени |
| Какую способность развивает | Перенос алгоритма на новый срез банковского лога и честная проверка результата |

---

## E. Карточка урока (§13)

| Поле | Значение |
|---|---|
| Часы | 2 |
| Стратегии обучения / виды деятельности | Трассировка на toy-примере → guided coding → проверка на CSV → самостоятельный gate |
| Формирующее оценивание | Зелёные assert каждой секции; устное объяснение инварианта; итоговый acceptance |
| Дифференциация (общая) | База: §§1–6 и Part A; усиление: §§7–9 и Challenge |
| По содержанию | {meta["outcomes"]} |
| По процессу | Индивидуальный код; короткие общие checkpoints после реализации и проверки |
| По продукту | Заполненный `lesson.ipynb`; сданный `homework.ipynb`; функция для сквозного артефакта |
| Canvas | не опубликовано |
"""


def write_notebook(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}: {len(value['cells'])} cells")


def main() -> None:
    missing = [DATA_DIR / name for name in CSV_NAMES if not (DATA_DIR / name).exists()]
    if missing:
        raise SystemExit(f"Missing CSV files: {missing}")
    counts = []
    for meta, builder in zip(LESSONS, BUILDERS):
        lesson_sections, homework_sections, solution_sections = builder()
        directory = ROOT / "lessons" / meta["dir"]
        directory.mkdir(parents=True, exist_ok=True)
        values = (
            ("lesson.ipynb", notebook(meta["title"], lesson_sections)),
            ("homework.ipynb", notebook(f"ДЗ: {meta['title']}", homework_sections)),
            ("solutions.ipynb", notebook(meta["title"], solution_sections, solution=True)),
        )
        for filename, value in values:
            write_notebook(directory / filename, value)
            counts.append((meta["dir"], filename, len(value["cells"])))
        (directory / "LESSON.md").write_text(lesson_plan(meta), encoding="utf-8")
        print(f"wrote lessons/{meta['dir']}/LESSON.md")
        for name in CSV_NAMES:
            shutil.copy2(DATA_DIR / name, directory / name)
        print(f"copied {len(CSV_NAMES)} CSV files -> lessons/{meta['dir']}")
    assert len(counts) == 21
    print("done: 21 notebooks, 7 lesson plans, 28 CSV copies")


if __name__ == "__main__":
    main()
