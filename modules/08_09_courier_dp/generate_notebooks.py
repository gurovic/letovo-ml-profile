#!/usr/bin/env python3
"""Generate the 15 student/teacher notebooks for module 08_09.

The generator is the source of truth. Student notebooks contain unfinished
work and executable contracts. Every teacher notebook mirrors lesson and
homework section by section.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_FILES = ("coin_change_cases.csv", "route_cost_grid_4x5.csv")
LESSON_DIRS = (
    "lessons/01_memo_dp1d",
    "lessons/02_practice_dp1d",
    "lessons/03_dp2d",
    "lessons/04_practice_dp2d",
    "lessons/05_games_when_dp",
)

SETUP = """from pathlib import Path
import csv


def find_data(name):
    for path in (Path(name), Path("../../data") / name):
        if path.exists():
            return path.resolve()
    raise FileNotFoundError(f"{name} не найден")


def load_coin_cases():
    rows = []
    with find_data("coin_change_cases.csv").open(encoding="utf-8") as file:
        for row in csv.DictReader(file):
            rows.append((
                row["case_id"],
                int(row["amount"]),
                [int(value) for value in row["coins"].split()],
                int(row["expected_min_coins"]),
            ))
    return rows


def load_grid():
    with find_data("route_cost_grid_4x5.csv").open(encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        return [[int(value) for value in row] for row in reader]


COIN_CASES = load_coin_cases()
ROUTE_GRID = load_grid()
assert len(COIN_CASES) == 5
assert len(ROUTE_GRID) == 4 and len(ROUTE_GRID[0]) == 5
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


def nb(cells: list[dict]) -> dict:
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": cells,
    }


def student_notebook(title: str, sections: list[tuple[str, str, str]]) -> dict:
    cells = [md(f"# {title}"), code(SETUP)]
    for heading, stub, _ in sections:
        cells.extend((md(heading), code(stub)))
    return nb(cells)


def solution_notebook(
    title: str,
    lesson_sections: list[tuple[str, str, str]],
    homework_sections: list[tuple[str, str, str]],
) -> dict:
    cells = [md(f"# Решения: {title}\n\n{SOL_BANNER}"), code(SETUP)]
    for heading, _, solution in lesson_sections:
        cells.extend((md(heading.replace("## ", "## Урок. ", 1)), code(solution)))
    for heading, _, solution in homework_sections:
        clean = heading.replace("### Part A — обязательно\n\n", "").replace("### Challenge\n\n", "")
        cells.extend((md(clean.replace("## ", "## ДЗ. ", 1)), code(solution)))
    return nb(cells)


def write(relative: str, notebook: dict) -> None:
    path = ROOT / relative
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {relative}: {len(notebook['cells'])} cells")


def publish(
    index: int,
    title: str,
    lesson_sections: list[tuple[str, str, str]],
    homework_sections: list[tuple[str, str, str]],
) -> None:
    base = LESSON_DIRS[index]
    write(f"{base}/lesson.ipynb", student_notebook(title, lesson_sections))
    write(
        f"{base}/homework.ipynb",
        student_notebook(f"ДЗ: {title}", homework_sections),
    )
    write(
        f"{base}/solutions.ipynb",
        solution_notebook(title, lesson_sections, homework_sections),
    )


def lesson01() -> None:
    title = "Мемоизация и DP 1D: размен и максимум"
    lesson = [
        (
            "## 1. Где рекурсия повторяет работу\n\n"
            "Реализуйте число маршрутов по лестнице с шагами 1 и 2. Счётчик "
            "покажет цену повторного вычисления одинаковых состояний.",
            """plain_calls = 0


def ways_plain(n):
    global plain_calls
    plain_calls += 1
    # TODO: базовые случаи n=0 и n<0; затем два рекурсивных вызова
    ...


assert ways_plain(5) == 8
assert plain_calls > 10
print("вызовов:", plain_calls)
""",
            """plain_calls = 0


def ways_plain(n):
    global plain_calls
    plain_calls += 1
    if n == 0:
        return 1
    if n < 0:
        return 0
    return ways_plain(n - 1) + ways_plain(n - 2)


assert ways_plain(5) == 8
assert plain_calls > 10
print("вызовов:", plain_calls)
""",
        ),
        (
            "## 2. Мемоизация: состояние вычисляется один раз\n\n"
            "Передавайте `cache` явно. Ключ — номер ступени, значение — число "
            "способов добраться до неё.",
            """memo_calls = 0


def ways_memo(n, cache):
    global memo_calls
    memo_calls += 1
    # TODO: базовые случаи, проверка cache, вычисление и запись
    ...


cache = {}
assert ways_memo(10, cache) == 89
assert set(cache) == set(range(1, 11))
print("вычисленных состояний:", len(cache))
""",
            """memo_calls = 0


def ways_memo(n, cache):
    global memo_calls
    memo_calls += 1
    if n == 0:
        return 1
    if n < 0:
        return 0
    if n not in cache:
        cache[n] = ways_memo(n - 1, cache) + ways_memo(n - 2, cache)
    return cache[n]


cache = {}
assert ways_memo(10, cache) == 89
assert set(cache) == set(range(1, 11))
print("вычисленных состояний:", len(cache))
""",
        ),
        (
            "## 3. Сравнение цены двух решений\n\n"
            "Запустите обе версии для `n=18`. Запишите вывод: что именно "
            "ограничивает число содержательных вычислений в memo-версии?",
            """plain_calls = 0
memo_calls = 0
# TODO: вычислите оба ответа
plain_answer = None
memo_answer = None
CALL_NOTE = ""  # TODO: не менее 100 символов
assert plain_answer == memo_answer == 4181
assert plain_calls > memo_calls * 20
assert len(CALL_NOTE) >= 100
print(plain_calls, memo_calls, CALL_NOTE)
""",
            """plain_calls = 0
memo_calls = 0
plain_answer = ways_plain(18)
memo_answer = ways_memo(18, {})
CALL_NOTE = (
    "Без кэша одно состояние вычисляется много раз из разных ветвей рекурсии. "
    "Мемоизация оставляет по одному содержательному вычислению для каждого n; "
    "повторные обращения только читают сохранённое значение."
)
assert plain_answer == memo_answer == 4181
assert plain_calls > memo_calls * 20
assert len(CALL_NOTE) >= 100
print(plain_calls, memo_calls, CALL_NOTE)
""",
        ),
        (
            "## 4. Состояние размена\n\n"
            "Для суммы `s` будем хранить минимум монет в `dp[s]`. Заполните "
            "базовый случай и значение для недостижимого состояния.",
            """amount = 6
coins = [1, 3, 4]
unreachable = None  # TODO: число больше любого возможного ответа
dp = None           # TODO: amount + 1 одинаковых значений
# TODO: базовый случай для суммы 0
assert len(dp) == 7
assert dp[0] == 0
assert all(value > amount for value in dp[1:])
""",
            """amount = 6
coins = [1, 3, 4]
unreachable = amount + 1
dp = [unreachable] * (amount + 1)
dp[0] = 0
assert len(dp) == 7
assert dp[0] == 0
assert all(value > amount for value in dp[1:])
""",
        ),
        (
            "## 5. Минимальный размен\n\n"
            "Реализуйте переход `dp[s] = min(dp[s-coin] + 1)`. Если сумму "
            "набрать нельзя, функция возвращает `-1`.",
            """def min_coins(amount, coins):
    # TODO: таблица amount + 1, заполнение слева направо
    ...


assert min_coins(6, [1, 3, 4]) == 2
assert min_coins(7, [2, 4]) == -1
assert min_coins(0, [2, 5]) == 0
""",
            """def min_coins(amount, coins):
    unreachable = amount + 1
    dp = [unreachable] * (amount + 1)
    dp[0] = 0
    for current in range(1, amount + 1):
        for coin in coins:
            if current >= coin:
                dp[current] = min(dp[current], dp[current - coin] + 1)
    return -1 if dp[amount] == unreachable else dp[amount]


assert min_coins(6, [1, 3, 4]) == 2
assert min_coins(7, [2, 4]) == -1
assert min_coins(0, [2, 5]) == 0
""",
        ),
        (
            "## 6. Контракт на данных кассы\n\n"
            "Прогоните функцию по CSV. Не подгоняйте код под отдельную строку: "
            "одна реализация должна пройти все сочетания сумм и номиналов.",
            """checked = 0
for case_id, amount, coins, expected in COIN_CASES:
    # TODO: вызов, assert с понятным сообщением, увеличение checked
    pass
assert checked == len(COIN_CASES)
print("проверено кейсов:", checked)
""",
            """checked = 0
for case_id, amount, coins, expected in COIN_CASES:
    got = min_coins(amount, coins)
    assert got == expected, (case_id, got, expected)
    checked += 1
assert checked == len(COIN_CASES)
print("проверено кейсов:", checked)
""",
        ),
        (
            "## 7. Максимум без соседних точек\n\n"
            "`dp[i]` — лучший доход на первых `i` точках. Для очередной точки "
            "нужно выбрать: пропустить её или взять вместе с результатом до соседней.",
            """def max_safe_gain(values):
    # TODO: обработайте пустой список и заполните dp длины len(values)+1
    ...


assert max_safe_gain([]) == 0
assert max_safe_gain([8]) == 8
assert max_safe_gain([8, 4, 5, 9, 3, 1, 7]) == 24
""",
            """def max_safe_gain(values):
    if not values:
        return 0
    dp = [0] * (len(values) + 1)
    dp[1] = values[0]
    for i in range(2, len(values) + 1):
        dp[i] = max(dp[i - 1], dp[i - 2] + values[i - 1])
    return dp[-1]


assert max_safe_gain([]) == 0
assert max_safe_gain([8]) == 8
assert max_safe_gain([8, 4, 5, 9, 3, 1, 7]) == 24
""",
        ),
        (
            "## 8. Эксперимент: жадный размен ошибается\n\n"
            "Сравните выбор крупнейшей монеты с DP на суммах 1…12 для номиналов "
            "`[1, 3, 4]`. Найдите первую сумму, где ответы различаются.",
            """def greedy_count(amount, coins):
    # TODO: брать номиналы от большего к меньшему
    ...


first_failure = None
# TODO: перебор сумм и сравнение greedy_count с min_coins
assert first_failure is not None
assert 1 <= first_failure <= 12
print("первый контрпример:", first_failure)
""",
            """def greedy_count(amount, coins):
    count = 0
    for coin in sorted(coins, reverse=True):
        count += amount // coin
        amount %= coin
    return count if amount == 0 else -1


first_failure = None
for amount in range(1, 13):
    if greedy_count(amount, [1, 3, 4]) != min_coins(amount, [1, 3, 4]):
        first_failure = amount
        break
assert first_failure is not None
assert 1 <= first_failure <= 12
print("первый контрпример:", first_failure)
""",
        ),
        (
            "## 9. Самостоятельно: восстановить набор монет\n\n"
            "Верните не только минимум, но и список выбранных монет. Порядок "
            "не важен; сумма и длина списка должны подтверждать оптимум.",
            """def coin_plan(amount, coins):
    # TODO: вместе с dp храните последнюю выбранную монету
    ...


plan = coin_plan(11, [1, 5, 7])
assert sum(plan) == 11
assert len(plan) == 3
assert all(coin in [1, 5, 7] for coin in plan)
""",
            """def coin_plan(amount, coins):
    unreachable = amount + 1
    dp = [unreachable] * (amount + 1)
    previous_coin = [None] * (amount + 1)
    dp[0] = 0
    for current in range(1, amount + 1):
        for coin in coins:
            if current >= coin and dp[current - coin] + 1 < dp[current]:
                dp[current] = dp[current - coin] + 1
                previous_coin[current] = coin
    if dp[amount] == unreachable:
        return []
    result = []
    while amount > 0:
        coin = previous_coin[amount]
        result.append(coin)
        amount -= coin
    return result


plan = coin_plan(11, [1, 5, 7])
assert sum(plan) == 11
assert len(plan) == 3
assert all(coin in [1, 5, 7] for coin in plan)
""",
        ),
    ]
    homework = [
        (
            "### Part A — обязательно\n\n## A1. Число маршрутов с тремя шагами\n\n"
            "Разрешены шаги 1, 2 и 3. Реализуйте табличное DP без рекурсии.",
            """def count_routes(distance):
    # TODO
    ...


assert count_routes(0) == 1
assert count_routes(4) == 7
assert count_routes(6) == 24
""",
            """def count_routes(distance):
    dp = [0] * (distance + 1)
    dp[0] = 1
    for current in range(1, distance + 1):
        for step in (1, 2, 3):
            if current >= step:
                dp[current] += dp[current - step]
    return dp[distance]


assert count_routes(0) == 1
assert count_routes(4) == 7
assert count_routes(6) == 24
""",
        ),
        (
            "## A2. Размен по всем строкам CSV\n\n"
            "Повторите `min_coins` самостоятельно и верните список результатов.",
            """def min_coins_hw(amount, coins):
    # TODO
    ...


answers = [min_coins_hw(amount, coins) for _, amount, coins, _ in COIN_CASES]
assert len(answers) == 5
assert all(isinstance(value, int) and value > 0 for value in answers)
""",
            """def min_coins_hw(amount, coins):
    unreachable = amount + 1
    dp = [unreachable] * (amount + 1)
    dp[0] = 0
    for current in range(1, amount + 1):
        for coin in coins:
            if current >= coin:
                dp[current] = min(dp[current], dp[current - coin] + 1)
    return -1 if dp[amount] == unreachable else dp[amount]


answers = [min_coins_hw(amount, coins) for _, amount, coins, _ in COIN_CASES]
assert answers == [2, 2, 3, 3, 3]
""",
        ),
        (
            "## A3. План безопасных смен\n\n"
            "Верните индексы выбранных несоседних смен с максимальной выручкой.",
            """def safe_shift_plan(values):
    # TODO: dp и обратный проход
    ...


values = [6, 7, 1, 30, 8, 2, 4]
indices = safe_shift_plan(values)
assert all(b - a > 1 for a, b in zip(indices, indices[1:]))
assert sum(values[i] for i in indices) == 41
""",
            """def safe_shift_plan(values):
    dp = [0] * (len(values) + 1)
    if values:
        dp[1] = values[0]
    for i in range(2, len(values) + 1):
        dp[i] = max(dp[i - 1], dp[i - 2] + values[i - 1])
    result = []
    i = len(values)
    while i > 0:
        if dp[i] == dp[i - 1]:
            i -= 1
        else:
            result.append(i - 1)
            i -= 2
    return list(reversed(result))


values = [6, 7, 1, 30, 8, 2, 4]
indices = safe_shift_plan(values)
assert all(b - a > 1 for a, b in zip(indices, indices[1:]))
assert sum(values[i] for i in indices) == 41
""",
        ),
        (
            "### Challenge\n\n## B1. Ограниченный запас монет\n\n"
            "Каждый номинал можно использовать не более заданного числа раз. "
            "Верните минимум монет или `-1`.",
            """def bounded_min_coins(amount, coins, limits):
    # TODO: для каждой монеты обновите копию таблицы
    ...


assert bounded_min_coins(8, [1, 3, 4], [2, 1, 1]) == 3
assert bounded_min_coins(9, [1, 3, 4], [1, 1, 1]) == -1
""",
            """def bounded_min_coins(amount, coins, limits):
    unreachable = amount + 1
    dp = [unreachable] * (amount + 1)
    dp[0] = 0
    for coin, limit in zip(coins, limits):
        next_dp = dp[:]
        for current in range(amount + 1):
            if dp[current] == unreachable:
                continue
            for count in range(1, limit + 1):
                target = current + count * coin
                if target <= amount:
                    next_dp[target] = min(next_dp[target], dp[current] + count)
        dp = next_dp
    return -1 if dp[amount] == unreachable else dp[amount]


assert bounded_min_coins(8, [1, 3, 4], [2, 1, 1]) == 3
assert bounded_min_coins(9, [1, 3, 4], [1, 1, 1]) == -1
""",
        ),
    ]
    publish(0, title, lesson, homework)


def lesson02() -> None:
    title = "Практика DP 1D: состояния, переходы, восстановление"
    lesson = [
        (
            "## 1. Минимум прыжков до адреса\n\n"
            "Курьер перемещается на любое число кварталов из `steps`. "
            "`dp[position]` хранит минимум перемещений.",
            """def min_jumps(distance, steps):
    # TODO: минимум переходов или -1
    ...


assert min_jumps(7, [2, 3]) == 3
assert min_jumps(5, [4]) == -1
assert min_jumps(0, [4]) == 0
""",
            """def min_jumps(distance, steps):
    unreachable = distance + 1
    dp = [unreachable] * (distance + 1)
    dp[0] = 0
    for position in range(1, distance + 1):
        for step in steps:
            if position >= step:
                dp[position] = min(dp[position], dp[position - step] + 1)
    return -1 if dp[distance] == unreachable else dp[distance]


assert min_jumps(7, [2, 3]) == 3
assert min_jumps(5, [4]) == -1
assert min_jumps(0, [4]) == 0
""",
        ),
        (
            "## 2. Сколько оптимальных маршрутов\n\n"
            "Вместе с минимумом храните число способов получить этот минимум. "
            "Более длинные маршруты не учитывайте.",
            """def count_min_jump_plans(distance, steps):
    # TODO: две таблицы — best и count
    ...


assert count_min_jump_plans(4, [1, 2, 3]) == (2, 3)
assert count_min_jump_plans(5, [4]) == (-1, 0)
""",
            """def count_min_jump_plans(distance, steps):
    unreachable = distance + 1
    best = [unreachable] * (distance + 1)
    count = [0] * (distance + 1)
    best[0], count[0] = 0, 1
    for position in range(1, distance + 1):
        for step in steps:
            if position < step:
                continue
            candidate = best[position - step] + 1
            if candidate < best[position]:
                best[position] = candidate
                count[position] = count[position - step]
            elif candidate == best[position]:
                count[position] += count[position - step]
    if best[distance] == unreachable:
        return -1, 0
    return best[distance], count[distance]


assert count_min_jump_plans(4, [1, 2, 3]) == (2, 3)
assert count_min_jump_plans(5, [4]) == (-1, 0)
""",
        ),
        (
            "## 3. Максимальная выручка без соседних смен\n\n"
            "Повторите переход «пропустить или взять» без копирования решения "
            "прошлой пары.",
            """def max_profit(values):
    # TODO
    ...


assert max_profit([6, 7, 1, 30, 8, 2, 4]) == 41
assert max_profit([]) == 0
assert max_profit([9, 1]) == 9
""",
            """def max_profit(values):
    previous_two = 0
    previous_one = 0
    for value in values:
        current = max(previous_one, previous_two + value)
        previous_two, previous_one = previous_one, current
    return previous_one


assert max_profit([6, 7, 1, 30, 8, 2, 4]) == 41
assert max_profit([]) == 0
assert max_profit([9, 1]) == 9
""",
        ),
        (
            "## 4. Восстановить выбранные смены\n\n"
            "Одного оптимального числа недостаточно для диспетчера. Верните "
            "индексы смен, которые дают этот максимум.",
            """def profit_plan(values):
    # TODO: полная таблица и обратный проход
    ...


values = [6, 7, 1, 30, 8, 2, 4]
plan = profit_plan(values)
assert sum(values[i] for i in plan) == 41
assert all(right - left > 1 for left, right in zip(plan, plan[1:]))
""",
            """def profit_plan(values):
    dp = [0] * (len(values) + 1)
    if values:
        dp[1] = values[0]
    for i in range(2, len(values) + 1):
        dp[i] = max(dp[i - 1], dp[i - 2] + values[i - 1])
    plan = []
    i = len(values)
    while i > 0:
        if dp[i] == dp[i - 1]:
            i -= 1
        else:
            plan.append(i - 1)
            i -= 2
    return list(reversed(plan))


values = [6, 7, 1, 30, 8, 2, 4]
plan = profit_plan(values)
assert sum(values[i] for i in plan) == 41
assert all(right - left > 1 for left, right in zip(plan, plan[1:]))
""",
        ),
        (
            "## 5. Маршрут с закрытыми кварталами\n\n"
            "Разрешены шаги 1 и 2, но на позиции из `blocked` вставать нельзя. "
            "Посчитайте число допустимых маршрутов.",
            """def routes_avoiding(distance, blocked):
    # TODO
    ...


assert routes_avoiding(6, {3}) == 4
assert routes_avoiding(3, {1, 2}) == 0
assert routes_avoiding(0, set()) == 1
""",
            """def routes_avoiding(distance, blocked):
    dp = [0] * (distance + 1)
    dp[0] = 1
    for position in range(1, distance + 1):
        if position in blocked:
            continue
        dp[position] = dp[position - 1]
        if position >= 2:
            dp[position] += dp[position - 2]
    return dp[distance]


assert routes_avoiding(6, {3}) == 4
assert routes_avoiding(3, {1, 2}) == 0
assert routes_avoiding(0, set()) == 1
""",
        ),
        (
            "## 6. Минимальная стоимость последовательности остановок\n\n"
            "На каждой позиции есть стоимость. До позиции можно прийти с одной "
            "или двух предыдущих; старт перед первой позицией бесплатный.",
            """def min_service_cost(costs):
    # TODO: стоимость завершения после последней позиции
    ...


assert min_service_cost([4, 1, 7, 2, 3]) == 6
assert min_service_cost([5]) == 5
assert min_service_cost([]) == 0
""",
            """def min_service_cost(costs):
    if not costs:
        return 0
    dp = [0] * (len(costs) + 1)
    dp[1] = costs[0]
    for i in range(2, len(costs) + 1):
        dp[i] = costs[i - 1] + min(dp[i - 1], dp[i - 2])
    return dp[-1]


assert min_service_cost([4, 1, 7, 2, 3]) == 6
assert min_service_cost([5]) == 5
assert min_service_cost([]) == 0
""",
        ),
        (
            "## 7. Память O(1) вместо таблицы\n\n"
            "Для `max_profit` нужны только два предыдущих значения. Реализуйте "
            "rolling-вариант и проверьте его против табличного на разных префиксах.",
            """def max_profit_rolling(values):
    # TODO: две переменные, без списка dp
    ...


sample = [5, 2, 8, 1, 9, 3]
for end in range(len(sample) + 1):
    assert max_profit_rolling(sample[:end]) == max_profit(sample[:end])
""",
            """def max_profit_rolling(values):
    previous_two = 0
    previous_one = 0
    for value in values:
        previous_two, previous_one = previous_one, max(previous_one, previous_two + value)
    return previous_one


sample = [5, 2, 8, 1, 9, 3]
for end in range(len(sample) + 1):
    assert max_profit_rolling(sample[:end]) == max_profit(sample[:end])
""",
        ),
        (
            "## 8. Эксперимент: как меняется оптимальный план\n\n"
            "Изменяйте только доход четвёртой смены от 0 до 40. Найдите первое "
            "значение, при котором эта смена входит в восстановленный план.",
            """base = [6, 7, 1, 0, 8, 2, 4]
threshold = None
# TODO: перебор значения base[3] и вызов profit_plan
assert threshold is not None
assert 0 <= threshold <= 40
print("порог включения:", threshold)
""",
            """base = [6, 7, 1, 0, 8, 2, 4]
threshold = None
for candidate in range(41):
    values = base[:]
    values[3] = candidate
    if 3 in profit_plan(values):
        threshold = candidate
        break
assert threshold is not None
assert 0 <= threshold <= 40
print("порог включения:", threshold)
""",
        ),
        (
            "## 9. Самостоятельно: тариф с ограничением серии\n\n"
            "Нельзя брать три смены подряд. Верните максимальную выручку; "
            "состояние должно различать длину текущей серии.",
            """def max_profit_no_three(values):
    # TODO
    ...


assert max_profit_no_three([5, 6, 7]) == 13
assert max_profit_no_three([5, 6, 7, 8]) == 20
assert max_profit_no_three([]) == 0
""",
            """def max_profit_no_three(values):
    dp = [0] * (len(values) + 1)
    if values:
        dp[1] = values[0]
    if len(values) >= 2:
        dp[2] = values[0] + values[1]
    for i in range(3, len(values) + 1):
        dp[i] = max(
            dp[i - 1],
            dp[i - 2] + values[i - 1],
            dp[i - 3] + values[i - 2] + values[i - 1],
        )
    return dp[-1]


assert max_profit_no_three([5, 6, 7]) == 13
assert max_profit_no_three([5, 6, 7, 8]) == 20
assert max_profit_no_three([]) == 0
""",
        ),
    ]
    homework = [
        (
            "### Part A — обязательно\n\n## A1. Минимум заправок\n\n"
            "До каждой следующей заправки можно проехать расстояние из `jumps`.",
            """def min_refuels(distance, jumps):
    # TODO
    ...


assert min_refuels(10, [3, 4]) == 3
assert min_refuels(5, [2, 4]) == -1
""",
            """def min_refuels(distance, jumps):
    unreachable = distance + 1
    dp = [unreachable] * (distance + 1)
    dp[0] = 0
    for current in range(1, distance + 1):
        for jump in jumps:
            if current >= jump:
                dp[current] = min(dp[current], dp[current - jump] + 1)
    return -1 if dp[distance] == unreachable else dp[distance]


assert min_refuels(10, [3, 4]) == 3
assert min_refuels(5, [2, 4]) == -1
""",
        ),
        (
            "## A2. План выплат без соседних дней\n\n"
            "Верните максимум и один набор индексов дней.",
            """def payout_plan(values):
    # TODO
    ...


values = [8, 4, 5, 9, 3, 1, 7]
best, indices = payout_plan(values)
assert best == sum(values[i] for i in indices)
assert all(b - a > 1 for a, b in zip(indices, indices[1:]))
""",
            """def payout_plan(values):
    dp = [0] * (len(values) + 1)
    if values:
        dp[1] = values[0]
    for i in range(2, len(values) + 1):
        dp[i] = max(dp[i - 1], dp[i - 2] + values[i - 1])
    indices = []
    i = len(values)
    while i > 0:
        if dp[i] == dp[i - 1]:
            i -= 1
        else:
            indices.append(i - 1)
            i -= 2
    indices.reverse()
    return dp[-1], indices


values = [8, 4, 5, 9, 3, 1, 7]
best, indices = payout_plan(values)
assert best == 24
assert best == sum(values[i] for i in indices)
assert all(b - a > 1 for a, b in zip(indices, indices[1:]))
""",
        ),
        (
            "## A3. Число маршрутов через обязательную точку\n\n"
            "Шаги равны 1 или 2. Посчитайте маршруты от 0 до `distance`, "
            "которые обязательно проходят через `checkpoint`.",
            """def routes_via(distance, checkpoint):
    # TODO
    ...


assert routes_via(6, 3) == 9
assert routes_via(5, 0) == 8
""",
            """def routes_via(distance, checkpoint):
    def ways(length):
        dp = [0] * (length + 1)
        dp[0] = 1
        for i in range(1, length + 1):
            dp[i] = dp[i - 1]
            if i >= 2:
                dp[i] += dp[i - 2]
        return dp[length]
    return ways(checkpoint) * ways(distance - checkpoint)


assert routes_via(6, 3) == 9
assert routes_via(5, 0) == 8
""",
        ),
        (
            "### Challenge\n\n## B1. Ровно k смен\n\n"
            "Выберите ровно `k` несоседних смен с максимальной выручкой. "
            "Если выбор невозможен, верните `None`.",
            """def max_exact_k(values, k):
    # TODO: состояние (первые i смен, выбрано j, взята ли последняя)
    ...


assert max_exact_k([6, 7, 1, 30, 8], 2) == 37
assert max_exact_k([5, 4], 2) is None
""",
            """def max_exact_k(values, k):
    impossible = -10**9
    skip = [[impossible] * (k + 1) for _ in range(len(values) + 1)]
    take = [[impossible] * (k + 1) for _ in range(len(values) + 1)]
    skip[0][0] = 0
    for i, value in enumerate(values, start=1):
        for chosen in range(k + 1):
            skip[i][chosen] = max(skip[i - 1][chosen], take[i - 1][chosen])
            if chosen > 0 and skip[i - 1][chosen - 1] != impossible:
                take[i][chosen] = skip[i - 1][chosen - 1] + value
    answer = max(skip[-1][k], take[-1][k])
    return None if answer == impossible else answer


assert max_exact_k([6, 7, 1, 30, 8], 2) == 37
assert max_exact_k([5, 4], 2) is None
""",
        ),
    ]
    publish(1, title, lesson, homework)


def lesson03() -> None:
    title = "DP 2D: стоимость и число маршрутов по сетке"
    lesson = [
        (
            "## 1. Два параметра состояния\n\n"
            "Создайте таблицу того же размера, что и сетка. Ячейка `(row, col)` "
            "будет хранить ответ для маршрута до этой точки.",
            """rows = len(ROUTE_GRID)
cols = len(ROUTE_GRID[0])
dp = None  # TODO: таблица rows × cols, заполненная нулями
assert len(dp) == rows
assert all(len(row) == cols for row in dp)
assert dp[0][0] == 0
""",
            """rows = len(ROUTE_GRID)
cols = len(ROUTE_GRID[0])
dp = [[0] * cols for _ in range(rows)]
assert len(dp) == rows
assert all(len(row) == cols for row in dp)
assert dp[0][0] == 0
""",
        ),
        (
            "## 2. Границы таблицы стоимости\n\n"
            "В первую строку можно прийти только слева, в первый столбец — "
            "только сверху. Заполните эти базовые состояния.",
            """dp = [[0] * cols for _ in range(rows)]
# TODO: (0, 0), первая строка, первый столбец
assert dp[0] == [1, 4, 5, 10, 11]
assert [dp[row][0] for row in range(rows)] == [1, 3, 8, 12]
""",
            """dp = [[0] * cols for _ in range(rows)]
dp[0][0] = ROUTE_GRID[0][0]
for col in range(1, cols):
    dp[0][col] = dp[0][col - 1] + ROUTE_GRID[0][col]
for row in range(1, rows):
    dp[row][0] = dp[row - 1][0] + ROUTE_GRID[row][0]
assert dp[0] == [1, 4, 5, 10, 11]
assert [dp[row][0] for row in range(rows)] == [1, 3, 8, 12]
""",
        ),
        (
            "## 3. Минимальная стоимость маршрута\n\n"
            "Во внутреннюю ячейку можно прийти сверху или слева. Добавьте "
            "стоимость текущей клетки к меньшему из двух предыдущих ответов.",
            """def min_path_cost(grid):
    # TODO: границы и внутренний переход
    ...


assert min_path_cost(ROUTE_GRID) == 11
assert min_path_cost([[7]]) == 7
assert min_path_cost([[1, 2], [3, 4]]) == 7
""",
            """def min_path_cost(grid):
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    for col in range(1, cols):
        dp[0][col] = dp[0][col - 1] + grid[0][col]
    for row in range(1, rows):
        dp[row][0] = dp[row - 1][0] + grid[row][0]
    for row in range(1, rows):
        for col in range(1, cols):
            dp[row][col] = grid[row][col] + min(dp[row - 1][col], dp[row][col - 1])
    return dp[-1][-1]


assert min_path_cost(ROUTE_GRID) == 11
assert min_path_cost([[7]]) == 7
assert min_path_cost([[1, 2], [3, 4]]) == 7
""",
        ),
        (
            "## 4. Вернуть всю таблицу\n\n"
            "Инженеру нужна диагностика, а не только последняя ячейка. "
            "Реализуйте функцию, возвращающую таблицу минимальных стоимостей.",
            """def min_cost_table(grid):
    # TODO
    ...


costs = min_cost_table(ROUTE_GRID)
assert costs[-1][-1] == 11
assert costs[1][2] == 8
assert all(costs[row][col] >= ROUTE_GRID[row][col] for row in range(rows) for col in range(cols))
""",
            """def min_cost_table(grid):
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    for col in range(1, cols):
        dp[0][col] = dp[0][col - 1] + grid[0][col]
    for row in range(1, rows):
        dp[row][0] = dp[row - 1][0] + grid[row][0]
    for row in range(1, rows):
        for col in range(1, cols):
            dp[row][col] = grid[row][col] + min(dp[row - 1][col], dp[row][col - 1])
    return dp


costs = min_cost_table(ROUTE_GRID)
assert costs[-1][-1] == 11
assert costs[1][2] == 8
assert all(costs[row][col] >= ROUTE_GRID[row][col] for row in range(rows) for col in range(cols))
""",
        ),
        (
            "## 5. Восстановить маршрут\n\n"
            "Идите от правого нижнего угла к соседу с меньшей накопленной "
            "стоимостью. Верните координаты от старта до финиша.",
            """def restore_min_path(grid):
    # TODO: min_cost_table и обратный проход
    ...


path = restore_min_path(ROUTE_GRID)
assert path[0] == (0, 0) and path[-1] == (3, 4)
assert len(path) == 8
assert sum(ROUTE_GRID[row][col] for row, col in path) == 11
""",
            """def restore_min_path(grid):
    dp = min_cost_table(grid)
    row, col = len(grid) - 1, len(grid[0]) - 1
    path = [(row, col)]
    while row > 0 or col > 0:
        if row == 0:
            col -= 1
        elif col == 0:
            row -= 1
        elif dp[row - 1][col] <= dp[row][col - 1]:
            row -= 1
        else:
            col -= 1
        path.append((row, col))
    return list(reversed(path))


path = restore_min_path(ROUTE_GRID)
assert path[0] == (0, 0) and path[-1] == (3, 4)
assert len(path) == 8
assert sum(ROUTE_GRID[row][col] for row, col in path) == 11
""",
        ),
        (
            "## 6. Число маршрутов без препятствий\n\n"
            "Теперь значение клетки — количество путей до неё. Стоимости "
            "игнорируются; переход складывает число путей сверху и слева.",
            """def count_paths(rows, cols):
    # TODO
    ...


assert count_paths(4, 5) == 35
assert count_paths(1, 7) == 1
assert count_paths(2, 2) == 2
""",
            """def count_paths(rows, cols):
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = 1
    for row in range(rows):
        for col in range(cols):
            if row == 0 and col == 0:
                continue
            top = dp[row - 1][col] if row > 0 else 0
            left = dp[row][col - 1] if col > 0 else 0
            dp[row][col] = top + left
    return dp[-1][-1]


assert count_paths(4, 5) == 35
assert count_paths(1, 7) == 1
assert count_paths(2, 2) == 2
""",
        ),
        (
            "## 7. Запретные клетки\n\n"
            "Запретная клетка получает ноль путей независимо от соседей. "
            "Проверьте отдельно случай заблокированного старта.",
            """def count_paths_with_blocks(rows, cols, blocks):
    # TODO
    ...


assert count_paths_with_blocks(4, 5, {(1, 1), (2, 3)}) == 7
assert count_paths_with_blocks(2, 2, {(0, 0)}) == 0
assert count_paths_with_blocks(2, 2, set()) == 2
""",
            """def count_paths_with_blocks(rows, cols, blocks):
    dp = [[0] * cols for _ in range(rows)]
    if (0, 0) in blocks:
        return 0
    dp[0][0] = 1
    for row in range(rows):
        for col in range(cols):
            if (row, col) in blocks:
                dp[row][col] = 0
                continue
            if row == 0 and col == 0:
                continue
            top = dp[row - 1][col] if row > 0 else 0
            left = dp[row][col - 1] if col > 0 else 0
            dp[row][col] = top + left
    return dp[-1][-1]


assert count_paths_with_blocks(4, 5, {(1, 1), (2, 3)}) == 7
assert count_paths_with_blocks(2, 2, {(0, 0)}) == 0
assert count_paths_with_blocks(2, 2, set()) == 2
""",
        ),
        (
            "## 8. Эксперимент: чувствительность маршрута\n\n"
            "Увеличивайте стоимость клетки `(2, 2)` от исходной до 20. "
            "Зафиксируйте значения, при которых оптимальный маршрут меняется.",
            """original_path = restore_min_path(ROUTE_GRID)
changes = []
# TODO: копия сетки для каждого значения 1..20; сравнение пути
assert changes
assert all(1 <= value <= 20 for value in changes)
PATH_NOTE = ""  # TODO: почему локальная правка может сменить весь маршрут, >= 100 символов
assert len(PATH_NOTE) >= 100
""",
            """original_path = restore_min_path(ROUTE_GRID)
changes = []
for value in range(1, 21):
    changed = [row[:] for row in ROUTE_GRID]
    changed[2][2] = value
    if restore_min_path(changed) != original_path:
        changes.append(value)
PATH_NOTE = (
    "Таблица хранит лучший результат для каждого префикса маршрута. Изменение "
    "одной клетки меняет все состояния правее и ниже неё, поэтому обратный "
    "проход может выбрать другую цепочку координат."
)
assert changes
assert all(1 <= value <= 20 for value in changes)
assert len(PATH_NOTE) >= 100
""",
        ),
        (
            "## 9. Самостоятельно: максимальная стоимость\n\n"
            "Перенесите тот же 2D-шаблон на критерий максимума. Верните число "
            "и один маршрут, не изменяя допустимые ходы.",
            """def max_path_with_route(grid):
    # TODO
    ...


best, path = max_path_with_route(ROUTE_GRID)
assert best == sum(ROUTE_GRID[row][col] for row, col in path)
assert path[0] == (0, 0) and path[-1] == (3, 4)
assert len(path) == 8
""",
            """def max_path_with_route(grid):
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    for col in range(1, cols):
        dp[0][col] = dp[0][col - 1] + grid[0][col]
    for row in range(1, rows):
        dp[row][0] = dp[row - 1][0] + grid[row][0]
    for row in range(1, rows):
        for col in range(1, cols):
            dp[row][col] = grid[row][col] + max(dp[row - 1][col], dp[row][col - 1])
    row, col = rows - 1, cols - 1
    path = [(row, col)]
    while row > 0 or col > 0:
        if row == 0:
            col -= 1
        elif col == 0:
            row -= 1
        elif dp[row - 1][col] >= dp[row][col - 1]:
            row -= 1
        else:
            col -= 1
        path.append((row, col))
    return dp[-1][-1], list(reversed(path))


best, path = max_path_with_route(ROUTE_GRID)
assert best == 19
assert best == sum(ROUTE_GRID[row][col] for row, col in path)
assert path[0] == (0, 0) and path[-1] == (3, 4)
assert len(path) == 8
""",
        ),
    ]
    homework = [
        (
            "### Part A — обязательно\n\n## A1. Маршруты с препятствиями\n\n"
            "Реализуйте подсчёт для произвольного размера сетки.",
            """def blocked_routes(rows, cols, blocks):
    # TODO
    ...


assert blocked_routes(3, 4, {(1, 1)}) == 4
assert blocked_routes(1, 4, {(0, 2)}) == 0
""",
            """def blocked_routes(rows, cols, blocks):
    dp = [[0] * cols for _ in range(rows)]
    if (0, 0) in blocks:
        return 0
    dp[0][0] = 1
    for row in range(rows):
        for col in range(cols):
            if (row, col) in blocks:
                dp[row][col] = 0
            elif row != 0 or col != 0:
                dp[row][col] = (
                    (dp[row - 1][col] if row > 0 else 0)
                    + (dp[row][col - 1] if col > 0 else 0)
                )
    return dp[-1][-1]


assert blocked_routes(3, 4, {(1, 1)}) == 4
assert blocked_routes(1, 4, {(0, 2)}) == 0
""",
        ),
        (
            "## A2. Самый выгодный маршрут\n\n"
            "Верните максимальную сумму для новой сетки.",
            """def max_path_sum(grid):
    # TODO
    ...


grid = [[4, 1, 2], [7, 0, 3], [2, 8, 1]]
assert isinstance(max_path_sum(grid), int)
assert max_path_sum([[5]]) == 5
""",
            """def max_path_sum(grid):
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    for row in range(rows):
        for col in range(cols):
            if row == 0 and col == 0:
                continue
            top = dp[row - 1][col] if row > 0 else -10**9
            left = dp[row][col - 1] if col > 0 else -10**9
            dp[row][col] = grid[row][col] + max(top, left)
    return dp[-1][-1]


grid = [[4, 1, 2], [7, 0, 3], [2, 8, 1]]
assert max_path_sum(grid) == 22
assert max_path_sum([[5]]) == 5
""",
        ),
        (
            "## A3. Маршрут минимальной стоимости\n\n"
            "Верните координаты и проверьте стоимость по исходной сетке.",
            """def min_route(grid):
    # TODO
    ...


route = min_route(ROUTE_GRID)
assert route[0] == (0, 0) and route[-1] == (3, 4)
assert all((b[0] - a[0], b[1] - a[1]) in {(1, 0), (0, 1)} for a, b in zip(route, route[1:]))
""",
            """def min_route(grid):
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    for row in range(rows):
        for col in range(cols):
            if row == 0 and col == 0:
                continue
            top = dp[row - 1][col] if row > 0 else 10**9
            left = dp[row][col - 1] if col > 0 else 10**9
            dp[row][col] = grid[row][col] + min(top, left)
    row, col = rows - 1, cols - 1
    route = [(row, col)]
    while row or col:
        if row > 0 and (col == 0 or dp[row - 1][col] <= dp[row][col - 1]):
            row -= 1
        else:
            col -= 1
        route.append((row, col))
    return list(reversed(route))


route = min_route(ROUTE_GRID)
assert route[0] == (0, 0) and route[-1] == (3, 4)
assert sum(ROUTE_GRID[row][col] for row, col in route) == 11
assert all((b[0] - a[0], b[1] - a[1]) in {(1, 0), (0, 1)} for a, b in zip(route, route[1:]))
""",
        ),
        (
            "### Challenge\n\n## B1. Сколько оптимальных маршрутов\n\n"
            "Верните минимальную стоимость и число маршрутов с такой стоимостью.",
            """def count_min_cost_paths(grid):
    # TODO: две таблицы
    ...


assert count_min_cost_paths([[1, 1], [1, 1]]) == (3, 2)
cost, count = count_min_cost_paths(ROUTE_GRID)
assert cost > 0 and count > 0
""",
            """def count_min_cost_paths(grid):
    rows, cols = len(grid), len(grid[0])
    cost = [[10**9] * cols for _ in range(rows)]
    count = [[0] * cols for _ in range(rows)]
    cost[0][0], count[0][0] = grid[0][0], 1
    for row in range(rows):
        for col in range(cols):
            if row == 0 and col == 0:
                continue
            candidates = []
            if row > 0:
                candidates.append((cost[row - 1][col], count[row - 1][col]))
            if col > 0:
                candidates.append((cost[row][col - 1], count[row][col - 1]))
            best_previous = min(value for value, _ in candidates)
            cost[row][col] = grid[row][col] + best_previous
            count[row][col] = sum(number for value, number in candidates if value == best_previous)
    return cost[-1][-1], count[-1][-1]


assert count_min_cost_paths([[1, 1], [1, 1]]) == (3, 2)
assert count_min_cost_paths(ROUTE_GRID) == (11, 1)
""",
        ),
    ]
    publish(2, title, lesson, homework)


def lesson04() -> None:
    title = "Практика DP 2D: маршруты и сравнение последовательностей"
    lesson = [
        (
            "## 1. Максимальная сумма по сетке\n\n"
            "Начните серию с известного шаблона: вправо или вниз, но критерий "
            "теперь максимизируется.",
            """def max_path_sum(grid):
    # TODO
    ...


GRID_A = [[4, 1, 2], [7, 0, 3], [2, 8, 1]]
assert max_path_sum(GRID_A) == 22
assert max_path_sum([[5]]) == 5
""",
            """def max_path_sum(grid):
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    for row in range(rows):
        for col in range(cols):
            if row == 0 and col == 0:
                continue
            top = dp[row - 1][col] if row > 0 else -10**9
            left = dp[row][col - 1] if col > 0 else -10**9
            dp[row][col] = grid[row][col] + max(top, left)
    return dp[-1][-1]


GRID_A = [[4, 1, 2], [7, 0, 3], [2, 8, 1]]
assert max_path_sum(GRID_A) == 22
assert max_path_sum([[5]]) == 5
""",
        ),
        (
            "## 2. Восстановить максимальный маршрут\n\n"
            "Верните координаты выбранного маршрута. При равенстве разрешён "
            "любой из оптимальных вариантов.",
            """def max_path_route(grid):
    # TODO
    ...


route = max_path_route(GRID_A)
assert route[0] == (0, 0) and route[-1] == (2, 2)
assert sum(GRID_A[row][col] for row, col in route) == 22
""",
            """def max_path_route(grid):
    rows, cols = len(grid), len(grid[0])
    dp = [[-10**9] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    for row in range(rows):
        for col in range(cols):
            if row == 0 and col == 0:
                continue
            top = dp[row - 1][col] if row > 0 else -10**9
            left = dp[row][col - 1] if col > 0 else -10**9
            dp[row][col] = grid[row][col] + max(top, left)
    row, col = rows - 1, cols - 1
    route = [(row, col)]
    while row or col:
        if row > 0 and (col == 0 or dp[row - 1][col] >= dp[row][col - 1]):
            row -= 1
        else:
            col -= 1
        route.append((row, col))
    return list(reversed(route))


route = max_path_route(GRID_A)
assert route[0] == (0, 0) and route[-1] == (2, 2)
assert sum(GRID_A[row][col] for row, col in route) == 22
""",
        ),
        (
            "## 3. Число максимальных маршрутов\n\n"
            "При равных значениях сверху и слева складывайте количества "
            "оптимальных способов.",
            """def count_max_paths(grid):
    # TODO: вернуть (максимум, количество)
    ...


assert count_max_paths([[1, 1], [1, 1]]) == (3, 2)
best, count = count_max_paths(GRID_A)
assert best == 22 and count >= 1
""",
            """def count_max_paths(grid):
    rows, cols = len(grid), len(grid[0])
    best = [[-10**9] * cols for _ in range(rows)]
    count = [[0] * cols for _ in range(rows)]
    best[0][0], count[0][0] = grid[0][0], 1
    for row in range(rows):
        for col in range(cols):
            if row == 0 and col == 0:
                continue
            candidates = []
            if row > 0:
                candidates.append((best[row - 1][col], count[row - 1][col]))
            if col > 0:
                candidates.append((best[row][col - 1], count[row][col - 1]))
            previous = max(value for value, _ in candidates)
            best[row][col] = grid[row][col] + previous
            count[row][col] = sum(number for value, number in candidates if value == previous)
    return best[-1][-1], count[-1][-1]


assert count_max_paths([[1, 1], [1, 1]]) == (3, 2)
assert count_max_paths(GRID_A) == (22, 1)
""",
        ),
        (
            "## 4. Состояние для сравнения строк\n\n"
            "`dp[i][j]` — длина общей подпоследовательности префиксов "
            "`a[:i]` и `b[:j]`. Создайте таблицу с нулевой рамкой.",
            """a = "COURIER"
b = "CURSOR"
lcs_dp = None  # TODO: (len(a)+1) × (len(b)+1)
assert len(lcs_dp) == len(a) + 1
assert all(len(row) == len(b) + 1 for row in lcs_dp)
assert all(value == 0 for value in lcs_dp[0])
""",
            """a = "COURIER"
b = "CURSOR"
lcs_dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
assert len(lcs_dp) == len(a) + 1
assert all(len(row) == len(b) + 1 for row in lcs_dp)
assert all(value == 0 for value in lcs_dp[0])
""",
        ),
        (
            "## 5. Длина общей подпоследовательности\n\n"
            "Если последние символы равны, используйте диагональ + 1. Иначе "
            "берите максимум сверху и слева.",
            """def lcs_len(a, b):
    # TODO
    ...


assert lcs_len("COURIER", "CURSOR") == 4
assert lcs_len("", "ABC") == 0
assert lcs_len("ABC", "ABC") == 3
""",
            """def lcs_len(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]


assert lcs_len("COURIER", "CURSOR") == 4
assert lcs_len("", "ABC") == 0
assert lcs_len("ABC", "ABC") == 3
""",
        ),
        (
            "## 6. Восстановить общую подпоследовательность\n\n"
            "Пройдите таблицу назад: равные символы входят в ответ, иначе "
            "двигайтесь к соседу с большим значением.",
            """def lcs_value(a, b):
    # TODO: построение таблицы и обратный проход
    ...


value = lcs_value("COURIER", "CURSOR")
assert len(value) == 4
assert all(char in "COURIER" for char in value)
assert all(char in "CURSOR" for char in value)
""",
            """def lcs_value(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    result = []
    i, j = len(a), len(b)
    while i and j:
        if a[i - 1] == b[j - 1]:
            result.append(a[i - 1])
            i, j = i - 1, j - 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(result))


value = lcs_value("COURIER", "CURSOR")
assert len(value) == 4
assert value == "CURR"
""",
        ),
        (
            "## 7. Расстояние редактирования\n\n"
            "Состояние снова задаётся двумя префиксами. Переход выбирает "
            "вставку, удаление или замену одного символа.",
            """def edit_distance(a, b):
    # TODO
    ...


assert edit_distance("route", "routes") == 1
assert edit_distance("cat", "cut") == 1
assert edit_distance("", "abc") == 3
""",
            """def edit_distance(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        dp[i][0] = i
    for j in range(len(b) + 1):
        dp[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            change = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + change,
            )
    return dp[-1][-1]


assert edit_distance("route", "routes") == 1
assert edit_distance("cat", "cut") == 1
assert edit_distance("", "abc") == 3
""",
        ),
        (
            "## 8. Эксперимент: LCS и расстояние отвечают на разные вопросы\n\n"
            "Сравните пары строк. Запишите, почему длинная LCS не всегда означает "
            "малое число правок.",
            """pairs = [("COURIER", "CURSOR"), ("ROUTE", "ROUTES"), ("ABC", "CBA")]
measurements = []  # TODO: кортежи (a, b, lcs, distance)
COMPARE_NOTE = ""  # TODO: не менее 120 символов
assert len(measurements) == 3
assert all(len(item) == 4 for item in measurements)
assert len(COMPARE_NOTE) >= 120
""",
            """pairs = [("COURIER", "CURSOR"), ("ROUTE", "ROUTES"), ("ABC", "CBA")]
measurements = [(a, b, lcs_len(a, b), edit_distance(a, b)) for a, b in pairs]
COMPARE_NOTE = (
    "LCS измеряет сохранённый порядок символов и допускает пропуски, а расстояние "
    "редактирования считает конкретные операции преобразования. Поэтому две строки "
    "могут иметь заметную общую подпоследовательность, но всё равно требовать "
    "нескольких вставок, удалений или замен."
)
assert len(measurements) == 3
assert all(len(item) == 4 for item in measurements)
assert len(COMPARE_NOTE) >= 120
""",
        ),
        (
            "## 9. Самостоятельно: наибольшая общая подстрока\n\n"
            "В отличие от подпоследовательности, символы должны идти подряд. "
            "При несовпадении текущая длина сбрасывается в ноль.",
            """def longest_common_substring(a, b):
    # TODO: вернуть длину и одну подстроку
    ...


length, value = longest_common_substring("COURIER", "CURSOR")
assert length == len(value)
assert value in "COURIER" and value in "CURSOR"
assert longest_common_substring("ABC", "XYZ") == (0, "")
""",
            """def longest_common_substring(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    best_length = 0
    best_end = 0
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > best_length:
                    best_length = dp[i][j]
                    best_end = i
    return best_length, a[best_end - best_length:best_end]


length, value = longest_common_substring("COURIER", "CURSOR")
assert (length, value) == (2, "UR")
assert longest_common_substring("ABC", "XYZ") == (0, "")
""",
        ),
    ]
    homework = [
        (
            "### Part A — обязательно\n\n## A1. Минимальная стоимость новой сетки\n\n"
            "Реализуйте 2D-переход на прямоугольной сетке.",
            """def min_path_cost(grid):
    # TODO
    ...


grid = [[1, 9, 2, 3], [4, 1, 8, 2], [7, 2, 1, 5]]
assert isinstance(min_path_cost(grid), int)
assert min_path_cost([[2]]) == 2
""",
            """def min_path_cost(grid):
    rows, cols = len(grid), len(grid[0])
    dp = [[10**9] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    for row in range(rows):
        for col in range(cols):
            if row == 0 and col == 0:
                continue
            top = dp[row - 1][col] if row > 0 else 10**9
            left = dp[row][col - 1] if col > 0 else 10**9
            dp[row][col] = grid[row][col] + min(top, left)
    return dp[-1][-1]


grid = [[1, 9, 2, 3], [4, 1, 8, 2], [7, 2, 1, 5]]
assert min_path_cost(grid) == 14
assert min_path_cost([[2]]) == 2
""",
        ),
        (
            "## A2. LCS для кодов статусов\n\n"
            "Верните длину общей подпоследовательности.",
            """def lcs_len_hw(a, b):
    # TODO
    ...


assert lcs_len_hw("DELIVERED", "DELAYED") >= 4
assert lcs_len_hw("", "DELAYED") == 0
""",
            """def lcs_len_hw(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]


assert lcs_len_hw("DELIVERED", "DELAYED") == 5
assert lcs_len_hw("", "DELAYED") == 0
""",
        ),
        (
            "## A3. Расстояние между идентификаторами\n\n"
            "Посчитайте минимальное число вставок, удалений и замен.",
            """def edit_distance_hw(a, b):
    # TODO
    ...


assert edit_distance_hw("ORDER", "OLDER") == 1
assert edit_distance_hw("BOX", "") == 3
""",
            """def edit_distance_hw(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        dp[i][0] = i
    for j in range(len(b) + 1):
        dp[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            change = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + change)
    return dp[-1][-1]


assert edit_distance_hw("ORDER", "OLDER") == 1
assert edit_distance_hw("BOX", "") == 3
""",
        ),
        (
            "### Challenge\n\n## B1. Число LCS оптимальной длины\n\n"
            "Для строк без повторяющихся символов верните длину LCS и число "
            "различных путей таблицы, достигающих этой длины.",
            """def count_lcs_paths(a, b):
    # TODO
    ...


length, count = count_lcs_paths("ABC", "ACB")
assert length == 2
assert count >= 2
""",
            """def count_lcs_paths(a, b):
    length = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    count = [[1] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                length[i][j] = length[i - 1][j - 1] + 1
                count[i][j] = count[i - 1][j - 1]
            else:
                length[i][j] = max(length[i - 1][j], length[i][j - 1])
                count[i][j] = 0
                if length[i - 1][j] == length[i][j]:
                    count[i][j] += count[i - 1][j]
                if length[i][j - 1] == length[i][j]:
                    count[i][j] += count[i][j - 1]
    return length[-1][-1], count[-1][-1]


assert count_lcs_paths("ABC", "ACB") == (2, 2)
""",
        ),
    ]
    publish(3, title, lesson, homework)


def lesson05() -> None:
    title = "Игры win/lose и инженерный выбор DP"
    lesson = [
        (
            "## 1. Разметить малые позиции вручную\n\n"
            "Позиция проигрышная, если любой допустимый ход ведёт в выигрышную. "
            "Заполните значения для ходов 1, 3 и 4.",
            """moves = [1, 3, 4]
manual = [False, None, None, None, None, None, None, None]  # TODO
assert all(isinstance(value, bool) for value in manual)
assert manual[0] is False
assert manual[1] is True and manual[2] is False
""",
            """moves = [1, 3, 4]
manual = [False]
for stones in range(1, 8):
    manual.append(any(stones >= move and not manual[stones - move] for move in moves))
assert all(isinstance(value, bool) for value in manual)
assert manual[0] is False
assert manual[1] is True and manual[2] is False
""",
        ),
        (
            "## 2. Таблица выигрышных позиций\n\n"
            "Реализуйте общий алгоритм для любого положительного набора ходов.",
            """def win_table(stones, moves):
    # TODO: список bool длины stones+1
    ...


table = win_table(10, [1, 3, 4])
assert len(table) == 11
assert table[:3] == [False, True, False]
assert table[10] is True
""",
            """def win_table(stones, moves):
    win = [False] * (stones + 1)
    for current in range(1, stones + 1):
        win[current] = any(
            current >= move and not win[current - move]
            for move in moves
        )
    return win


table = win_table(10, [1, 3, 4])
assert len(table) == 11
assert table[:3] == [False, True, False]
assert table[10] is True
""",
        ),
        (
            "## 3. Ответ для одной позиции\n\n"
            "`can_win` использует таблицу и возвращает только состояние, "
            "которое запросил диспетчер.",
            """def can_win(stones, moves):
    # TODO
    ...


assert can_win(1, [1, 3, 4]) is True
assert can_win(2, [1, 3, 4]) is False
assert can_win(10, [1, 3, 4]) is True
""",
            """def can_win(stones, moves):
    return win_table(stones, moves)[stones]


assert can_win(1, [1, 3, 4]) is True
assert can_win(2, [1, 3, 4]) is False
assert can_win(10, [1, 3, 4]) is True
""",
        ),
        (
            "## 4. Найти выигрышный ход\n\n"
            "Верните ход в проигрышную позицию соперника. Если позиция "
            "проигрышная, верните `None`.",
            """def winning_move(stones, moves):
    # TODO
    ...


assert winning_move(2, [1, 3, 4]) is None
move = winning_move(10, [1, 3, 4])
assert move in [1, 3, 4]
assert can_win(10 - move, [1, 3, 4]) is False
""",
            """def winning_move(stones, moves):
    table = win_table(stones, moves)
    for move in moves:
        if stones >= move and not table[stones - move]:
            return move
    return None


assert winning_move(2, [1, 3, 4]) is None
move = winning_move(10, [1, 3, 4])
assert move in [1, 3, 4]
assert can_win(10 - move, [1, 3, 4]) is False
""",
        ),
        (
            "## 5. Симуляция стратегии\n\n"
            "Первый игрок использует `winning_move`, второй берёт первый "
            "допустимый ход. Верните журнал `(игрок, ход, остаток)`.",
            """def play_game(stones, moves):
    # TODO
    ...


log = play_game(10, [1, 3, 4])
assert log
assert log[-1][2] == 0
assert all(move in [1, 3, 4] for _, move, _ in log)
""",
            """def play_game(stones, moves):
    log = []
    player = 1
    while stones > 0:
        move = winning_move(stones, moves)
        if move is None:
            move = next(candidate for candidate in moves if candidate <= stones)
        stones -= move
        log.append((player, move, stones))
        player = 2 if player == 1 else 1
    return log


log = play_game(10, [1, 3, 4])
assert log
assert log[-1][2] == 0
assert all(move in [1, 3, 4] for _, move, _ in log)
""",
        ),
        (
            "## 6. Эксперимент: период проигрышных позиций\n\n"
            "Для двух наборов ходов выпишите проигрышные позиции до 40. "
            "Сравните разности между соседними позициями.",
            """losing_134 = []  # TODO
losing_125 = []  # TODO
PATTERN_NOTE = ""  # TODO: не менее 120 символов, без утверждения общего доказательства
assert losing_134[0] == 0 and losing_125[0] == 0
assert len(losing_134) >= 5 and len(losing_125) >= 5
assert len(PATTERN_NOTE) >= 120
""",
            """losing_134 = [i for i, value in enumerate(win_table(40, [1, 3, 4])) if not value]
losing_125 = [i for i, value in enumerate(win_table(40, [1, 2, 5])) if not value]
PATTERN_NOTE = (
    "На конечном диапазоне проигрышные позиции образуют повторяющийся рисунок, "
    "но таблица до 40 не является доказательством периода для всех n. Набор "
    "разрешённых ходов меняет переход и вместе с ним расположение проигрышных состояний."
)
assert losing_134[0] == 0 and losing_125[0] == 0
assert len(losing_134) >= 5 and len(losing_125) >= 5
assert len(PATTERN_NOTE) >= 120
""",
        ),
        (
            "## 7. Чек-лист применимости DP\n\n"
            "Для задачи размена отметьте четыре проверяемых условия. Рядом "
            "с каждым булевым значением запишите конкретное обоснование.",
            """dp_fit = {
    "compact_state": (None, ""),
    "repeated_subproblems": (None, ""),
    "clear_transition": (None, ""),
    "known_order": (None, ""),
}  # TODO
assert all(flag is True for flag, _ in dp_fit.values())
assert all(len(reason) >= 40 for _, reason in dp_fit.values())
""",
            """dp_fit = {
    "compact_state": (True, "Состояние полностью задаётся текущей суммой от 0 до amount."),
    "repeated_subproblems": (True, "Одна остаточная сумма возникает после выбора разных предыдущих монет."),
    "clear_transition": (True, "Ответ для суммы сравнивает dp[sum-coin] + 1 по номиналам."),
    "known_order": (True, "Суммы заполняются от 0 вверх, зависимости уже рассчитаны."),
}
assert all(flag is True for flag, _ in dp_fit.values())
assert all(len(reason) >= 40 for _, reason in dp_fit.values())
""",
        ),
        (
            "## 8. DP или более простой метод\n\n"
            "Классифицируйте четыре задачи. Используйте только `dp`, `greedy` "
            "или `direct`; затем объясните один спорный выбор.",
            """choices = {
    "min_coins_arbitrary": None,
    "sum_all_costs": None,
    "take_largest_until_full": None,
    "grid_min_path": None,
}  # TODO
CHOICE_NOTE = ""  # TODO: не менее 120 символов
assert set(choices.values()) <= {"dp", "greedy", "direct"}
assert len(set(choices.values())) == 3
assert len(CHOICE_NOTE) >= 120
""",
            """choices = {
    "min_coins_arbitrary": "dp",
    "sum_all_costs": "direct",
    "take_largest_until_full": "greedy",
    "grid_min_path": "dp",
}
CHOICE_NOTE = (
    "Для произвольных номиналов локальный выбор крупнейшей монеты может потерять "
    "глобальный минимум, поэтому нужен DP. Простая сумма не имеет конкурирующих "
    "решений и таблица только усложнит код. Жадный метод допустим там, где условие "
    "задачи прямо требует брать крупнейшие доступные элементы."
)
assert set(choices.values()) <= {"dp", "greedy", "direct"}
assert len(set(choices.values())) == 3
assert len(CHOICE_NOTE) >= 120
""",
        ),
        (
            "## 9. Самостоятельно: артефакт инженерного выбора\n\n"
            "Соберите функцию, которая по краткому описанию признаков задачи "
            "возвращает рекомендацию и список причин. Это не универсальный "
            "автоклассификатор, а явный чек-лист модуля.",
            """def recommend_dp(compact_state, repeated, clear_transition, ordered):
    # TODO: (решение bool, список конкретных причин)
    ...


decision, reasons = recommend_dp(True, True, True, True)
assert decision is True
assert len(reasons) == 4
decision, reasons = recommend_dp(False, True, True, False)
assert decision is False
assert len(reasons) >= 1
""",
            """def recommend_dp(compact_state, repeated, clear_transition, ordered):
    checks = [
        ("состояние компактно", compact_state),
        ("подзадачи повторяются", repeated),
        ("переход определён", clear_transition),
        ("порядок вычисления известен", ordered),
    ]
    failed = [text for text, passed in checks if not passed]
    if failed:
        return False, failed
    return True, [text for text, _ in checks]


decision, reasons = recommend_dp(True, True, True, True)
assert decision is True
assert len(reasons) == 4
decision, reasons = recommend_dp(False, True, True, False)
assert decision is False
assert len(reasons) >= 1
""",
        ),
    ]
    homework = [
        (
            "### Part A — обязательно\n\n## A1. Игра с ходами 1, 2 и 5\n\n"
            "Верните таблицу позиций от 0 до `stones`.",
            """def game_table(stones, moves):
    # TODO
    ...


table = game_table(12, [1, 2, 5])
assert len(table) == 13
assert table[0] is False
assert all(isinstance(value, bool) for value in table)
""",
            """def game_table(stones, moves):
    table = [False] * (stones + 1)
    for current in range(1, stones + 1):
        table[current] = any(
            current >= move and not table[current - move]
            for move in moves
        )
    return table


table = game_table(12, [1, 2, 5])
assert len(table) == 13
assert table == [False, True, True, False, True, True, False, True, True, False, True, True, False]
""",
        ),
        (
            "## A2. Все выигрышные ходы\n\n"
            "Верните список всех ходов, оставляющих сопернику проигрышную позицию.",
            """def all_winning_moves(stones, moves):
    # TODO
    ...


assert all_winning_moves(2, [1, 3, 4]) == []
result = all_winning_moves(10, [1, 3, 4])
assert result and all(move in [1, 3, 4] for move in result)
""",
            """def all_winning_moves(stones, moves):
    table = game_table(stones, moves)
    return [
        move for move in moves
        if move <= stones and not table[stones - move]
    ]


assert all_winning_moves(2, [1, 3, 4]) == []
assert all_winning_moves(10, [1, 3, 4]) == [1, 3]
""",
        ),
        (
            "## A3. Инженерная нота\n\n"
            "Сравните DP с прямым вычислением и жадным выбором на двух задачах. "
            "Укажите состояние, переход, порядок и альтернативу.",
            """ENGINEERING_NOTE = ""  # TODO: не менее 400 символов
required = ["состояни", "переход", "поряд", "альтернатив"]
assert len(ENGINEERING_NOTE) >= 400
assert all(word in ENGINEERING_NOTE.lower() for word in required)
print(ENGINEERING_NOTE)
""",
            """ENGINEERING_NOTE = (
    "Для размена произвольными номиналами состояние — текущая сумма, переход "
    "сравнивает dp[сумма - монета] + 1, а порядок идёт от меньших сумм к большим. "
    "Жадная альтернатива проще, но номиналы 1, 3, 4 дают контрпример на сумме 6: "
    "жадный выбор использует 4 + 1 + 1, а DP находит 3 + 3. "
    "Для суммы всех стоимостей DP не нужен: нет конкурирующих решений и "
    "повторяющихся подзадач. Состояние и переход пришлось бы придумать искусственно, "
    "порядок обычного цикла уже достаточен. Альтернатива — один прямой проход по "
    "списку, который короче, прозрачнее и требует постоянной дополнительной памяти."
)
required = ["состояни", "переход", "поряд", "альтернатив"]
assert len(ENGINEERING_NOTE) >= 400
assert all(word in ENGINEERING_NOTE.lower() for word in required)
print(ENGINEERING_NOTE)
""",
        ),
        (
            "### Challenge\n\n## B1. Период — гипотеза и проверка\n\n"
            "Для ходов 1, 3, 4 найдите кратчайший период последних 60 значений "
            "таблицы до 200. Это вычислительная гипотеза, не доказательство.",
            """def suffix_period(values, suffix_length):
    # TODO: минимальный period, повторяющийся на suffix
    ...


table = game_table(200, [1, 3, 4])
period = suffix_period(table, 60)
assert isinstance(period, int)
assert 1 <= period <= 30
""",
            """def suffix_period(values, suffix_length):
    suffix = values[-suffix_length:]
    for period in range(1, suffix_length // 2 + 1):
        if all(suffix[i] == suffix[i - period] for i in range(period, len(suffix))):
            return period
    return suffix_length


table = game_table(200, [1, 3, 4])
period = suffix_period(table, 60)
assert period == 7
""",
        ),
    ]
    publish(4, title, lesson, homework)


BUILDERS = (lesson01, lesson02, lesson03, lesson04, lesson05)


def main() -> None:
    for name in DATA_FILES:
        source = ROOT / "data" / name
        if not source.exists():
            raise SystemExit(f"missing {source}")
    for base in LESSON_DIRS:
        lesson_dir = ROOT / base
        lesson_dir.mkdir(parents=True, exist_ok=True)
        for name in DATA_FILES:
            source = ROOT / "data" / name
            target = lesson_dir / name
            if not target.exists() or target.read_bytes() != source.read_bytes():
                shutil.copy2(source, target)
    for build in BUILDERS:
        build()
    print("done: 15 notebooks; CSV copied into 5 lesson folders")


if __name__ == "__main__":
    main()
