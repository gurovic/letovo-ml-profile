#!/usr/bin/env python3
"""Generate lesson notebooks for module 08_09 (KTP pairs 55-59).

Source of truth for .ipynb: edit this file, then run it.
Pattern: stubs + asserts in lesson/homework; full solutions.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COINS_CSV = ROOT / "data" / "coin_change_cases.csv"
GRID_CSV = ROOT / "data" / "route_cost_grid_4x5.csv"

SOL_BANNER = (
    "**Для преподавателя.** Эталон к `lesson.ipynb` и `homework.ipynb`. "
    "Не показывать ученикам до сдачи."
)

LOAD_COMMON = (
    "from pathlib import Path\n"
    "import csv\n\n\n"
    "def _find(name: str) -> Path:\n"
    "    for p in (Path(name), Path(f'../../data/{name}'), Path(f'../data/{name}')):\n"
    "        if p.exists():\n"
    "            return p.resolve()\n"
    "    raise FileNotFoundError(f'{name} не найден рядом с ноутбуком')\n\n\n"
    "def load_coin_cases() -> list[dict[str, object]]:\n"
    "    path = _find('coin_change_cases.csv')\n"
    "    rows: list[dict[str, object]] = []\n"
    "    with path.open(encoding='utf-8') as f:\n"
    "        reader = csv.DictReader(f)\n"
    "        for row in reader:\n"
    "            rows.append({\n"
    "                'case_id': row['case_id'],\n"
    "                'amount': int(row['amount']),\n"
    "                'coins': [int(x) for x in row['coins'].split()],\n"
    "                'expected_min_coins': int(row['expected_min_coins']),\n"
    "            })\n"
    "    return rows\n\n\n"
    "def load_grid() -> list[list[int]]:\n"
    "    path = _find('route_cost_grid_4x5.csv')\n"
    "    grid: list[list[int]] = []\n"
    "    with path.open(encoding='utf-8') as f:\n"
    "        reader = csv.reader(f)\n"
    "        next(reader)\n"
    "        for row in reader:\n"
    "            grid.append([int(x) for x in row])\n"
    "    return grid\n"
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


def write(rel_path: str, notebook: dict) -> None:
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", path)


NOTEBOOKS: dict[str, dict] = {}


def add_lesson01() -> None:
    base = "lessons/01_memo_dp1d"
    lesson = nb(
        md("# Мемоизация и DP 1D: размен и максимум"),
        code(LOAD_COMMON),
        md("## 1. Мемоизация: стоимость доставки участка"),
        code(
            "from functools import lru_cache\n\n"
            "calls = 0\n\n"
            "@lru_cache(maxsize=None)\n"
            "def ways(n: int) -> int:\n"
            "    # TODO: число способов добраться до n, шаги 1/2\n"
            "    return 0\n\n"
            "ans = ways(10)\n"
            "assert ans == 89\n"
            "print('ways(10)=', ans)"
        ),
        md("## 2. DP 1D: минимальный размен"),
        code(
            "def min_coins(amount: int, coins: list[int]) -> int:\n"
            "    # TODO: вернуть минимум монет или -1\n"
            "    return -1\n\n"
            "cases = load_coin_cases()\n"
            "for row in cases:\n"
            "    got = min_coins(row['amount'], row['coins'])\n"
            "    assert got == row['expected_min_coins']\n"
            "print('coin cases OK')"
        ),
        md("## 3. DP 1D: максимум на линейном маршруте без соседних точек"),
        code(
            "def max_safe_gain(points: list[int]) -> int:\n"
            "    # TODO: нельзя брать соседние точки\n"
            "    return 0\n\n"
            "route = [8, 4, 5, 9, 3, 1, 7]\n"
            "assert max_safe_gain(route) == 24\n"
            "print('max_safe_gain OK')"
        ),
    )
    hw = nb(
        md("# ДЗ: DP 1D на сценариях курьерской службы"),
        code(LOAD_COMMON),
        md("## 1. Размен для вечерней кассы"),
        code(
            "def min_coins(amount: int, coins: list[int]) -> int:\n"
            "    # TODO\n"
            "    return -1\n\n"
            "assert min_coins(27, [1, 5, 10]) == 5\n"
            "assert min_coins(6, [4, 7]) == -1\n"
            "print('done')"
        ),
        md("## 2. Нота про пользу memoization"),
        code("MEMO_NOTE = ''\nassert len(MEMO_NOTE) > 120\nprint(MEMO_NOTE)"),
    )
    sol = nb(
        md("# Решения: memo + DP 1D\n\n" + SOL_BANNER),
        code(LOAD_COMMON),
        code(
            "from functools import lru_cache\n\n"
            "@lru_cache(maxsize=None)\n"
            "def ways(n: int) -> int:\n"
            "    if n <= 1:\n"
            "        return 1\n"
            "    return ways(n - 1) + ways(n - 2)\n\n"
            "def min_coins(amount: int, coins: list[int]) -> int:\n"
            "    inf = amount + 1\n"
            "    dp = [inf] * (amount + 1)\n"
            "    dp[0] = 0\n"
            "    for s in range(1, amount + 1):\n"
            "        best = inf\n"
            "        for c in coins:\n"
            "            if s - c >= 0 and dp[s - c] + 1 < best:\n"
            "                best = dp[s - c] + 1\n"
            "        dp[s] = best\n"
            "    return -1 if dp[amount] == inf else dp[amount]\n\n"
            "def max_safe_gain(points: list[int]) -> int:\n"
            "    if not points:\n"
            "        return 0\n"
            "    take, skip = 0, 0\n"
            "    for value in points:\n"
            "        new_take = skip + value\n"
            "        skip = max(skip, take)\n"
            "        take = new_take\n"
            "    return max(take, skip)\n\n"
            "cases = load_coin_cases()\n"
            "for row in cases:\n"
            "    got = min_coins(row['amount'], row['coins'])\n"
            "    assert got == row['expected_min_coins']\n\n"
            "assert ways(10) == 89\n"
            "route = [8, 4, 5, 9, 3, 1, 7]\n"
            "assert max_safe_gain(route) == 24\n"
            "assert min_coins(27, [1, 5, 10]) == 5\n"
            "assert min_coins(6, [4, 7]) == -1\n"
            "MEMO_NOTE = (\n"
            "    'Мемоизация убирает повторный пересчёт одинаковых состояний рекурсии. '\n"
            "    'В инженерии это снижает время ответа, когда подзадачи часто повторяются, как в размене и шагах по маршруту.'\n"
            ")\n"
            "print('ways(10)=', ways(10))\n"
            "print('coin cases OK')\n"
            "print('max_safe_gain=', max_safe_gain(route))\n"
            "print(MEMO_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson02() -> None:
    base = "lessons/02_practice_dp1d"
    lesson = nb(
        md("# Практика DP 1D: лимиты топлива и дневные заказы"),
        code(LOAD_COMMON),
        md("## 1. Минимум остановок для покрытия дистанции"),
        code(
            "def min_stops(distance: int, stations: list[int]) -> int:\n"
            "    # TODO: DP 1D, можно ехать на 1..max(stations) за шаг\n"
            "    return -1\n\n"
            "assert min_stops(7, [2, 3]) == 3\n"
            "assert min_stops(5, [4]) == -1\n"
            "print('min_stops OK')"
        ),
        md("## 2. Максимальная выручка по дням без соседних смен"),
        code(
            "def max_profit(days: list[int]) -> int:\n"
            "    # TODO\n"
            "    return 0\n\n"
            "assert max_profit([6, 7, 1, 30, 8, 2, 4]) == 41\n"
            "print('max_profit OK')"
        ),
    )
    hw = nb(
        md("# ДЗ: отработка DP 1D"),
        code(LOAD_COMMON),
        md("## 1. Размен с новыми номиналами"),
        code(
            "def min_coins(amount: int, coins: list[int]) -> int:\n"
            "    # TODO\n"
            "    return -1\n\n"
            "assert min_coins(23, [1, 7, 10]) == 5\n"
            "assert min_coins(5, [4, 6]) == -1\n"
            "print('ok')"
        ),
        md("## 2. Короткий вывод"),
        code("DP1D_NOTE = ''\nassert len(DP1D_NOTE) > 120\nprint(DP1D_NOTE)"),
    )
    sol = nb(
        md("# Решения: практика DP 1D\n\n" + SOL_BANNER),
        code(LOAD_COMMON),
        code(
            "def min_stops(distance: int, stations: list[int]) -> int:\n"
            "    inf = distance + 1\n"
            "    dp = [inf] * (distance + 1)\n"
            "    dp[0] = 0\n"
            "    for pos in range(1, distance + 1):\n"
            "        for step in stations:\n"
            "            if pos - step >= 0 and dp[pos - step] + 1 < dp[pos]:\n"
            "                dp[pos] = dp[pos - step] + 1\n"
            "    return -1 if dp[distance] == inf else dp[distance]\n\n"
            "def max_profit(days: list[int]) -> int:\n"
            "    take, skip = 0, 0\n"
            "    for value in days:\n"
            "        new_take = skip + value\n"
            "        skip = max(skip, take)\n"
            "        take = new_take\n"
            "    return max(take, skip)\n\n"
            "def min_coins(amount: int, coins: list[int]) -> int:\n"
            "    inf = amount + 1\n"
            "    dp = [inf] * (amount + 1)\n"
            "    dp[0] = 0\n"
            "    for s in range(1, amount + 1):\n"
            "        for c in coins:\n"
            "            if s - c >= 0 and dp[s - c] + 1 < dp[s]:\n"
            "                dp[s] = dp[s - c] + 1\n"
            "    return -1 if dp[amount] == inf else dp[amount]\n\n"
            "assert min_stops(7, [2, 3]) == 3\n"
            "assert min_stops(5, [4]) == -1\n"
            "assert max_profit([6, 7, 1, 30, 8, 2, 4]) == 41\n"
            "assert min_coins(23, [1, 7, 10]) == 5\n"
            "assert min_coins(5, [4, 6]) == -1\n"
            "DP1D_NOTE = (\n"
            "    'Для DP 1D важно, что состояние описывается одним числом: сумма, позиция или день. '\n"
            "    'Переходы берут лучшие предыдущие состояния, поэтому решение строится слева направо.'\n"
            ")\n"
            "print('min_stops=', min_stops(7, [2, 3]))\n"
            "print('max_profit=', max_profit([6, 7, 1, 30, 8, 2, 4]))\n"
            "print(DP1D_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson03() -> None:
    base = "lessons/03_dp2d"
    lesson = nb(
        md("# DP 2D: табличный переход на сетке стоимости"),
        code(LOAD_COMMON),
        md("## 1. Минимальная стоимость маршрута вправо/вниз"),
        code(
            "def min_path_cost(grid: list[list[int]]) -> int:\n"
            "    # TODO: заполнить таблицу dp[r][c]\n"
            "    return 0\n\n"
            "grid = load_grid()\n"
            "assert min_path_cost(grid) == 11\n"
            "print('min_path_cost OK')"
        ),
        md("## 2. Сколько путей (без препятствий)"),
        code(
            "def count_paths(rows: int, cols: int) -> int:\n"
            "    # TODO\n"
            "    return 0\n\n"
            "assert count_paths(4, 5) == 35\n"
            "print('count_paths OK')"
        ),
    )
    hw = nb(
        md("# ДЗ: таблица переходов DP 2D"),
        code(LOAD_COMMON),
        md("## 1. Маршрут с запретными ячейками"),
        code(
            "def count_paths_with_blocks(blocks: set[tuple[int, int]], rows: int, cols: int) -> int:\n"
            "    # TODO\n"
            "    return 0\n\n"
            "blocks = {(1, 1), (2, 3)}\n"
            "assert count_paths_with_blocks(blocks, 4, 5) == 7\n"
            "print('ok')"
        ),
        md("## 2. Пояснение по границам таблицы"),
        code("BORDER_NOTE = ''\nassert len(BORDER_NOTE) > 120\nprint(BORDER_NOTE)"),
    )
    sol = nb(
        md("# Решения: DP 2D\n\n" + SOL_BANNER),
        code(LOAD_COMMON),
        code(
            "def min_path_cost(grid: list[list[int]]) -> int:\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "    dp = [[0] * cols for _ in range(rows)]\n"
            "    dp[0][0] = grid[0][0]\n"
            "    for c in range(1, cols):\n"
            "        dp[0][c] = dp[0][c - 1] + grid[0][c]\n"
            "    for r in range(1, rows):\n"
            "        dp[r][0] = dp[r - 1][0] + grid[r][0]\n"
            "    for r in range(1, rows):\n"
            "        for c in range(1, cols):\n"
            "            dp[r][c] = min(dp[r - 1][c], dp[r][c - 1]) + grid[r][c]\n"
            "    return dp[-1][-1]\n\n"
            "def count_paths(rows: int, cols: int) -> int:\n"
            "    dp = [[0] * cols for _ in range(rows)]\n"
            "    for r in range(rows):\n"
            "        dp[r][0] = 1\n"
            "    for c in range(cols):\n"
            "        dp[0][c] = 1\n"
            "    for r in range(1, rows):\n"
            "        for c in range(1, cols):\n"
            "            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]\n"
            "    return dp[-1][-1]\n\n"
            "def count_paths_with_blocks(blocks: set[tuple[int, int]], rows: int, cols: int) -> int:\n"
            "    dp = [[0] * cols for _ in range(rows)]\n"
            "    if (0, 0) in blocks:\n"
            "        return 0\n"
            "    dp[0][0] = 1\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if (r, c) in blocks:\n"
            "                dp[r][c] = 0\n"
            "                continue\n"
            "            if r == 0 and c == 0:\n"
            "                continue\n"
            "            top = dp[r - 1][c] if r > 0 else 0\n"
            "            left = dp[r][c - 1] if c > 0 else 0\n"
            "            dp[r][c] = top + left\n"
            "    return dp[-1][-1]\n\n"
            "grid = load_grid()\n"
            "assert min_path_cost(grid) == 11\n"
            "assert count_paths(4, 5) == 35\n"
            "blocks = {(1, 1), (2, 3)}\n"
            "assert count_paths_with_blocks(blocks, 4, 5) == 7\n"
            "BORDER_NOTE = (\n"
            "    'Границы таблицы задают базовые случаи DP 2D: первая строка и первый столбец. '\n"
            "    'Без корректных базовых ячеек переходы внутри таблицы дают неверный результат.'\n"
            ")\n"
            "print('grid=', grid)\n"
            "print('min_path_cost=', min_path_cost(grid))\n"
            "print('count_paths=', count_paths(4, 5))\n"
            "print('count_paths_with_blocks=', count_paths_with_blocks(blocks, 4, 5))\n"
            "print(BORDER_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson04() -> None:
    base = "lessons/04_practice_dp2d"
    lesson = nb(
        md("# Практика DP 2D: два инженерных шаблона"),
        code(LOAD_COMMON),
        md("## 1. Максимальная сумма пути по сетке"),
        code(
            "def max_path_sum(grid: list[list[int]]) -> int:\n"
            "    # TODO\n"
            "    return 0\n\n"
            "grid = [\n"
            "    [4, 1, 2],\n"
            "    [7, 0, 3],\n"
            "    [2, 8, 1],\n"
            "]\n"
            "assert max_path_sum(grid) == 22\n"
            "print('max_path_sum OK')"
        ),
        md("## 2. LCS: длина общего подпоследовательности"),
        code(
            "def lcs_len(a: str, b: str) -> int:\n"
            "    # TODO\n"
            "    return 0\n\n"
            "assert lcs_len('COURIER', 'CURSOR') == 4\n"
            "print('lcs_len OK')"
        ),
    )
    hw = nb(
        md("# ДЗ: practice DP 2D"),
        code(LOAD_COMMON),
        md("## 1. Минимальная стоимость на другой сетке"),
        code(
            "def min_path_cost(grid: list[list[int]]) -> int:\n"
            "    # TODO\n"
            "    return 0\n\n"
            "grid = [\n"
            "    [1, 9, 2, 3],\n"
            "    [4, 1, 8, 2],\n"
            "    [7, 2, 1, 5],\n"
            "]\n"
            "assert min_path_cost(grid) == 14\n"
            "print('ok')"
        ),
        md("## 2. Нота: когда 2D обязателен"),
        code("DP2D_NOTE = ''\nassert len(DP2D_NOTE) > 120\nprint(DP2D_NOTE)"),
    )
    sol = nb(
        md("# Решения: практика DP 2D\n\n" + SOL_BANNER),
        code(LOAD_COMMON),
        code(
            "def max_path_sum(grid: list[list[int]]) -> int:\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "    dp = [[0] * cols for _ in range(rows)]\n"
            "    dp[0][0] = grid[0][0]\n"
            "    for c in range(1, cols):\n"
            "        dp[0][c] = dp[0][c - 1] + grid[0][c]\n"
            "    for r in range(1, rows):\n"
            "        dp[r][0] = dp[r - 1][0] + grid[r][0]\n"
            "    for r in range(1, rows):\n"
            "        for c in range(1, cols):\n"
            "            dp[r][c] = max(dp[r - 1][c], dp[r][c - 1]) + grid[r][c]\n"
            "    return dp[-1][-1]\n\n"
            "def lcs_len(a: str, b: str) -> int:\n"
            "    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]\n"
            "    for i in range(1, len(a) + 1):\n"
            "        for j in range(1, len(b) + 1):\n"
            "            if a[i - 1] == b[j - 1]:\n"
            "                dp[i][j] = dp[i - 1][j - 1] + 1\n"
            "            else:\n"
            "                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])\n"
            "    return dp[-1][-1]\n\n"
            "def min_path_cost(grid: list[list[int]]) -> int:\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "    dp = [[0] * cols for _ in range(rows)]\n"
            "    dp[0][0] = grid[0][0]\n"
            "    for c in range(1, cols):\n"
            "        dp[0][c] = dp[0][c - 1] + grid[0][c]\n"
            "    for r in range(1, rows):\n"
            "        dp[r][0] = dp[r - 1][0] + grid[r][0]\n"
            "    for r in range(1, rows):\n"
            "        for c in range(1, cols):\n"
            "            dp[r][c] = min(dp[r - 1][c], dp[r][c - 1]) + grid[r][c]\n"
            "    return dp[-1][-1]\n\n"
            "grid_a = [[4, 1, 2], [7, 0, 3], [2, 8, 1]]\n"
            "grid_b = [[1, 9, 2, 3], [4, 1, 8, 2], [7, 2, 1, 5]]\n"
            "assert max_path_sum(grid_a) == 22\n"
            "assert lcs_len('COURIER', 'CURSOR') == 4\n"
            "assert min_path_cost(grid_b) == 14\n"
            "DP2D_NOTE = (\n"
            "    '2D обязательно, когда состояние задаётся двумя параметрами: позиция в сетке или пара индексов строк. '\n"
            "    'Сведение такой задачи к 1D обычно ломает часть зависимостей и ухудшает читаемость переходов.'\n"
            ")\n"
            "print('max_path_sum=', max_path_sum(grid_a))\n"
            "print('lcs_len=', lcs_len('COURIER', 'CURSOR'))\n"
            "print('min_path_cost=', min_path_cost(grid_b))\n"
            "print(DP2D_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson05() -> None:
    base = "lessons/05_games_when_dp"
    lesson = nb(
        md("# Игровая задача win/lose и границы применимости DP"),
        code(LOAD_COMMON),
        md("## 1. Игра с камнями: можно взять 1, 3 или 4"),
        code(
            "def can_win(stones: int, moves: list[int]) -> bool:\n"
            "    # TODO: win/lose DP\n"
            "    return False\n\n"
            "assert can_win(1, [1, 3, 4]) is True\n"
            "assert can_win(2, [1, 3, 4]) is False\n"
            "assert can_win(10, [1, 3, 4]) is True\n"
            "print('can_win OK')"
        ),
        md("## 2. Чек-лист: когда DP уместен"),
        code(
            "dp_fit = {\n"
            "    'overlap': False,\n"
            "    'optimal_substructure': False,\n"
            "    'small_state': False,\n"
            "    'clear_transition': False,\n"
            "}\n"
            "assert all(dp_fit.values())\n"
            "print(dp_fit)"
        ),
    )
    hw = nb(
        md("# ДЗ: игры и инженерный выбор инструмента"),
        code(LOAD_COMMON),
        md("## 1. Игра с ходами 1/2/5"),
        code(
            "def can_win(stones: int, moves: list[int]) -> bool:\n"
            "    # TODO\n"
            "    return False\n\n"
            "assert can_win(7, [1, 2, 5]) is True\n"
            "assert can_win(8, [1, 2, 5]) is True\n"
            "assert can_win(9, [1, 2, 5]) is False\n"
            "print('ok')"
        ),
        md("## 2. Нота: DP vs жадный"),
        code("WHEN_NOTE = ''\nassert len(WHEN_NOTE) > 150\nprint(WHEN_NOTE)"),
    )
    sol = nb(
        md("# Решения: игры и when DP\n\n" + SOL_BANNER),
        code(LOAD_COMMON),
        code(
            "def can_win(stones: int, moves: list[int]) -> bool:\n"
            "    win = [False] * (stones + 1)\n"
            "    for s in range(1, stones + 1):\n"
            "        for move in moves:\n"
            "            prev = s - move\n"
            "            if prev >= 0 and not win[prev]:\n"
            "                win[s] = True\n"
            "                break\n"
            "    return win[stones]\n\n"
            "assert can_win(1, [1, 3, 4]) is True\n"
            "assert can_win(2, [1, 3, 4]) is False\n"
            "assert can_win(10, [1, 3, 4]) is True\n"
            "assert can_win(7, [1, 2, 5]) is True\n"
            "assert can_win(8, [1, 2, 5]) is True\n"
            "assert can_win(9, [1, 2, 5]) is False\n\n"
            "dp_fit = {\n"
            "    'overlap': True,\n"
            "    'optimal_substructure': True,\n"
            "    'small_state': True,\n"
            "    'clear_transition': True,\n"
            "}\n"
            "WHEN_NOTE = (\n"
            "    'DP уместен, когда состояние компактное и подзадачи повторяются; тогда таблица даёт надёжный и проверяемый результат. '\n"
            "    'Если решение строится локально без риска потерять глобальный оптимум, жадный алгоритм проще и дешевле в реализации.'\n"
            ")\n"
            "print('moves 1/3/4, n=10 =>', can_win(10, [1, 3, 4]))\n"
            "print('moves 1/2/5, n=9 =>', can_win(9, [1, 2, 5]))\n"
            "print(dp_fit)\n"
            "print(WHEN_NOTE)"
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
]


def main() -> None:
    if not COINS_CSV.exists():
        raise SystemExit(f"Missing {COINS_CSV}.")
    if not GRID_CSV.exists():
        raise SystemExit(f"Missing {GRID_CSV}.")
    for build in BUILDERS:
        build()
    for rel, content in NOTEBOOKS.items():
        write(rel, content)
    print(f"done: {len(NOTEBOOKS)} notebooks in 5 lessons")


if __name__ == "__main__":
    main()
