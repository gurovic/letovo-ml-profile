#!/usr/bin/env python3
"""Generate lesson notebooks for module 08_11 (KTP pairs 65-68).

Source of truth for .ipynb: edit this file, then run it.
Pattern: stubs + asserts in lesson/homework; full solutions.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SOL_BANNER = (
    "**Для преподавателя.** Эталон к `lesson.ipynb` и `homework.ipynb`. "
    "Не показывать ученикам до сдачи."
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
    base = "lessons/01_derivative_intuition"
    intro = (
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n\n"
        "def f(x):\n"
        "    return 0.08 * (x - 3) ** 3 + 0.6 * (x - 3) ** 2 + 2\n\n"
        "xs = np.linspace(-2, 8, 81)\n"
        "ys = f(xs)\n"
    )
    lesson = nb(
        md("# Производная как скорость изменения (интуитивно)\n\nБез формальных доказательств: смотрим, как быстро меняется высота на полигоне."),
        code(intro),
        md("## 1. Средняя скорость изменения на отрезке"),
        code(
            "x1, x2 = 0.0, 2.0\n"
            "avg_speed = None\n"
            "assert avg_speed is not None\n"
            "assert -20 < float(avg_speed) < 20\n"
            "print(round(float(avg_speed), 4))"
        ),
        md("## 2. Численная производная в точке"),
        code(
            "def num_derivative(fun, x, h=1e-3):\n"
            "    return None\n\n\n"
            "d_at_1 = num_derivative(f, 1.0)\n"
            "d_at_3 = num_derivative(f, 3.0)\n"
            "assert d_at_1 is not None and d_at_3 is not None\n"
            "assert -20 < float(d_at_1) < 20\n"
            "assert -20 < float(d_at_3) < 20\n"
            "print(round(float(d_at_1), 4), round(float(d_at_3), 4))"
        ),
        md("## 3. Где склон вверх, где вниз"),
        code(
            "slope_sign = []  # список из 5 элементов: 'up' или 'down'\n"
            "probe_points = [-1.0, 0.0, 2.0, 4.0, 6.0]\n"
            "assert len(slope_sign) == len(probe_points)\n"
            "assert set(slope_sign) <= {'up', 'down', 'flat'}\n"
            "print(list(zip(probe_points, slope_sign)))"
        ),
        md("## 4. Минимальный фрагмент склона"),
        code(
            "window_left = None\n"
            "window_right = None\n"
            "assert window_left is not None and window_right is not None\n"
            "assert float(window_left) < float(window_right)\n"
            "print(window_left, window_right)"
        ),
        md("## 5. Короткое объяснение"),
        code(
            "DERIVATIVE_NOTE = ''\n"
            "assert len(DERIVATIVE_NOTE) > 120\n"
            "print(DERIVATIVE_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: производная как скорость\n\nФункция для домашней тренировки."),
        code(
            "import numpy as np\n\n"
            "def g(x):\n"
            "    return 0.5 * (x + 1) ** 2 + np.sin(1.5 * x)\n\n"
            "def num_derivative(fun, x, h=1e-3):\n"
            "    return None\n"
        ),
        md("### A. Закрепление\n\n## 1. Скорость на отрезке [1, 3]"),
        code(
            "avg_g = None\n"
            "assert avg_g is not None\n"
            "assert -20 < float(avg_g) < 20\n"
            "print(round(float(avg_g), 4))"
        ),
        md("## 2. Производная в точках"),
        code(
            "d0 = None\n"
            "d2 = None\n"
            "assert d0 is not None and d2 is not None\n"
            "print(round(float(d0), 4), round(float(d2), 4))"
        ),
        md("### B. Вызов\n\n## 3. Найдите точку почти горизонтального касания"),
        code(
            "flat_x = None\n"
            "flat_d = None\n"
            "assert flat_x is not None and flat_d is not None\n"
            "assert abs(float(flat_d)) < 0.2\n"
            "print(float(flat_x), float(flat_d))"
        ),
        md("## 4. Рефлексия по языку скорости"),
        code(
            "SPEED_NOTE = ''\n"
            "assert len(SPEED_NOTE) > 140\n"
            "print(SPEED_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: производная как скорость\n\n" + SOL_BANNER),
        code(
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n\n"
            "def f(x):\n"
            "    return 0.08 * (x - 3) ** 3 + 0.6 * (x - 3) ** 2 + 2\n\n"
            "xs = np.linspace(-2, 8, 81)\n"
            "ys = f(xs)\n"
            "x1, x2 = 0.0, 2.0\n"
            "avg_speed = float((f(x2) - f(x1)) / (x2 - x1))\n\n"
            "def num_derivative(fun, x, h=1e-3):\n"
            "    return float((fun(x + h) - fun(x - h)) / (2 * h))\n\n"
            "d_at_1 = num_derivative(f, 1.0)\n"
            "d_at_3 = num_derivative(f, 3.0)\n"
            "probe_points = [-1.0, 0.0, 2.0, 4.0, 6.0]\n"
            "slope_sign = []\n"
            "for p in probe_points:\n"
            "    d = num_derivative(f, p)\n"
            "    if d > 0.05:\n"
            "        slope_sign.append('up')\n"
            "    elif d < -0.05:\n"
            "        slope_sign.append('down')\n"
            "    else:\n"
            "        slope_sign.append('flat')\n"
            "scan = np.linspace(1.5, 5.0, 351)\n"
            "dvals = np.array([abs(num_derivative(f, p)) for p in scan])\n"
            "idx = int(np.argmin(dvals))\n"
            "window_left = float(scan[max(0, idx - 3)])\n"
            "window_right = float(scan[min(len(scan) - 1, idx + 3)])\n"
            "DERIVATIVE_NOTE = (\n"
            "    'Производная здесь читается как мгновенная скорость: плюс — подъем, минус — спуск, '\n"
            "    'почти ноль — горизонтальный участок рядом с локальным минимумом.'\n"
            ")\n\n"
            "def g(x):\n"
            "    return 0.5 * (x + 1) ** 2 + np.sin(1.5 * x)\n\n"
            "avg_g = float((g(3.0) - g(1.0)) / 2.0)\n"
            "d0 = num_derivative(g, 0.0)\n"
            "d2 = num_derivative(g, 2.0)\n"
            "scan2 = np.linspace(-2.0, 3.0, 1001)\n"
            "d2vals = np.array([num_derivative(g, x) for x in scan2])\n"
            "j = int(np.argmin(np.abs(d2vals)))\n"
            "flat_x = float(scan2[j])\n"
            "flat_d = float(d2vals[j])\n"
            "SPEED_NOTE = (\n"
            "    'Язык скорости удобен тем, что не требует тяжелой формализации: по знаку и величине численной производной '\n"
            "    'можно понять, куда двигаться по рельефу и где ждать остановку.'\n"
            ")\n"
            "print(round(avg_speed, 4), round(d_at_1, 4), round(d_at_3, 4))\n"
            "print(list(zip(probe_points, slope_sign)))\n"
            "print(window_left, window_right)\n"
            "print(round(avg_g, 4), round(d0, 4), round(d2, 4), flat_x, flat_d)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson02() -> None:
    base = "lessons/02_practice_gd_1d"
    intro = (
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n\n"
        "def loss(x):\n"
        "    return (x - 2.5) ** 2 + 0.2\n"
    )
    lesson = nb(
        md("# Практика: численный градиентный спуск в 1D"),
        code(intro),
        md("## 1. Численная производная loss"),
        code(
            "def num_derivative(fun, x, h=1e-4):\n"
            "    return None\n\n\n"
            "d0 = num_derivative(loss, 0.0)\n"
            "d3 = num_derivative(loss, 3.0)\n"
            "assert d0 is not None and d3 is not None\n"
            "print(round(float(d0), 4), round(float(d3), 4))"
        ),
        md("## 2. Один шаг градиентного спуска"),
        code(
            "x0 = -1.0\n"
            "eta = 0.2\n"
            "x1 = None\n"
            "assert x1 is not None\n"
            "assert -5 < float(x1) < 5\n"
            "print(float(x1), float(loss(x1)))"
        ),
        md("## 3. Функция gradient_descent_1d"),
        code(
            "def gradient_descent_1d(fun, start, eta=0.1, steps=25):\n"
            "    # вернуть trajectory_x, trajectory_loss\n"
            "    return None, None\n\n\n"
            "traj_x, traj_loss = gradient_descent_1d(loss, start=-1.0, eta=0.2, steps=20)\n"
            "assert traj_x is not None and traj_loss is not None\n"
            "assert len(traj_x) == 21 and len(traj_loss) == 21\n"
            "assert float(traj_loss[-1]) <= float(traj_loss[0])\n"
            "print(traj_x[-1], traj_loss[-1])"
        ),
        md("## 4. Сравнение разных eta"),
        code(
            "etas = [0.03, 0.2, 0.9]\n"
            "eta_report = {}\n"
            "assert set(eta_report.keys()) == set(etas)\n"
            "print(eta_report)"
        ),
        md("## 5. Вывод о размере шага"),
        code(
            "ETA_NOTE = ''\n"
            "assert len(ETA_NOTE) > 130\n"
            "print(ETA_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: устойчивость GD на другой функции"),
        code(
            "import numpy as np\n\n"
            "def h(x):\n"
            "    return 0.15 * (x - 4.0) ** 2 + 0.3 * np.sin(2.2 * x) + 1.0\n\n"
            "def num_derivative(fun, x, h=1e-4):\n"
            "    return None\n\n"
            "def gradient_descent_1d(fun, start, eta=0.08, steps=40):\n"
            "    return None, None\n"
        ),
        md("### A. Закрепление\n\n## 1. Траектория от старта x=-2"),
        code(
            "tx, tl = gradient_descent_1d(h, start=-2.0, eta=0.08, steps=40)\n"
            "assert tx is not None and tl is not None\n"
            "assert len(tx) == 41\n"
            "print(tx[-1], tl[-1])"
        ),
        md("## 2. Траектория от старта x=7"),
        code(
            "tx2, tl2 = gradient_descent_1d(h, start=7.0, eta=0.08, steps=40)\n"
            "assert tx2 is not None and tl2 is not None\n"
            "print(tx2[-1], tl2[-1])"
        ),
        md("### B. Вызов\n\n## 3. Сравнить eta=0.02 и eta=0.25"),
        code(
            "compare = {}\n"
            "assert set(compare.keys()) == {0.02, 0.25}\n"
            "print(compare)"
        ),
        md("## 4. Короткая инженерная рекомендация"),
        code(
            "GD_NOTE = ''\n"
            "assert len(GD_NOTE) > 150\n"
            "print(GD_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: численный GD 1D\n\n" + SOL_BANNER),
        code(
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n\n"
            "def loss(x):\n"
            "    return (x - 2.5) ** 2 + 0.2\n\n"
            "def num_derivative(fun, x, h=1e-4):\n"
            "    return float((fun(x + h) - fun(x - h)) / (2 * h))\n\n"
            "d0 = num_derivative(loss, 0.0)\n"
            "d3 = num_derivative(loss, 3.0)\n"
            "x0 = -1.0\n"
            "eta = 0.2\n"
            "x1 = float(x0 - eta * num_derivative(loss, x0))\n\n"
            "def gradient_descent_1d(fun, start, eta=0.1, steps=25):\n"
            "    x = float(start)\n"
            "    traj_x = [x]\n"
            "    traj_loss = [float(fun(x))]\n"
            "    for _ in range(steps):\n"
            "        grad = num_derivative(fun, x)\n"
            "        x = float(x - eta * grad)\n"
            "        traj_x.append(x)\n"
            "        traj_loss.append(float(fun(x)))\n"
            "    return traj_x, traj_loss\n\n"
            "traj_x, traj_loss = gradient_descent_1d(loss, start=-1.0, eta=0.2, steps=20)\n"
            "etas = [0.03, 0.2, 0.9]\n"
            "eta_report = {}\n"
            "for e in etas:\n"
            "    _, tl = gradient_descent_1d(loss, start=-1.0, eta=e, steps=25)\n"
            "    eta_report[e] = {\n"
            "        'start_loss': round(float(tl[0]), 4),\n"
            "        'final_loss': round(float(tl[-1]), 4),\n"
            "        'improved': bool(tl[-1] < tl[0]),\n"
            "    }\n"
            "ETA_NOTE = (\n"
            "    'Слишком маленький eta движется медленно, слишком большой может колебаться и перескакивать минимум. '\n"
            "    'На учебной функции eta=0.2 дает быстрый и стабильный спад loss.'\n"
            ")\n\n"
            "def h(x):\n"
            "    return 0.15 * (x - 4.0) ** 2 + 0.3 * np.sin(2.2 * x) + 1.0\n\n"
            "tx, tl = gradient_descent_1d(h, start=-2.0, eta=0.08, steps=40)\n"
            "tx2, tl2 = gradient_descent_1d(h, start=7.0, eta=0.08, steps=40)\n"
            "compare = {}\n"
            "for e in (0.02, 0.25):\n"
            "    _, t = gradient_descent_1d(h, start=-2.0, eta=e, steps=40)\n"
            "    compare[e] = {'first': round(float(t[0]), 4), 'last': round(float(t[-1]), 4)}\n"
            "GD_NOTE = (\n"
            "    'Для новой функции лучше сначала протестировать 2-3 значения eta на коротком прогоне и смотреть, '\n"
            "    'убывает ли loss без резких скачков. Это быстрее, чем сразу фиксировать один шаг без проверки.'\n"
            ")\n"
            "print(round(d0, 4), round(d3, 4), round(loss(x1), 4))\n"
            "print(traj_x[-1], traj_loss[-1])\n"
            "print(eta_report)\n"
            "print(tx[-1], tl[-1], tx2[-1], tl2[-1])\n"
            "print(compare)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson03() -> None:
    base = "lessons/03_integral_loss_overview"
    lesson = nb(
        md("# Интеграл обзорно: площадь и накопленный loss"),
        code(
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n\n"
            "def curve(x):\n"
            "    return 1.2 + 0.4 * x + 0.2 * np.sin(1.3 * x)\n\n"
            "xs = np.linspace(0.0, 6.0, 121)\n"
            "ys = curve(xs)\n"
        ),
        md("## 1. Площадь прямоугольниками (левые точки)"),
        code(
            "dx = 0.2\n"
            "area_left = None\n"
            "assert area_left is not None\n"
            "assert 0 < float(area_left) < 30\n"
            "print(round(float(area_left), 4))"
        ),
        md("## 2. Площадь трапециями"),
        code(
            "area_trap = None\n"
            "assert area_trap is not None\n"
            "assert 0 < float(area_trap) < 30\n"
            "print(round(float(area_trap), 4))"
        ),
        md("## 3. История loss по эпохам"),
        code(
            "epoch_loss = np.array([2.4, 2.1, 1.9, 1.7, 1.55, 1.45, 1.38, 1.34, 1.31, 1.29])\n"
            "cum_loss = None\n"
            "assert cum_loss is not None\n"
            "assert float(cum_loss) > 0\n"
            "print(round(float(cum_loss), 4))"
        ),
        md("## 4. Сравнение двух стратегий обучения"),
        code(
            "loss_a = np.array([2.4, 2.1, 1.9, 1.7, 1.55, 1.45, 1.38, 1.34, 1.31, 1.29])\n"
            "loss_b = np.array([2.4, 2.2, 2.0, 1.85, 1.72, 1.62, 1.55, 1.50, 1.46, 1.43])\n"
            "area_a = None\n"
            "area_b = None\n"
            "better = ''\n"
            "assert area_a is not None and area_b is not None\n"
            "assert better in {'A', 'B'}\n"
            "print(area_a, area_b, better)"
        ),
        md("## 5. Объяснение связи с loss"),
        code(
            "INTEGRAL_NOTE = ''\n"
            "assert len(INTEGRAL_NOTE) > 130\n"
            "print(INTEGRAL_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: площадь под кривой и динамика ошибки"),
        code(
            "import numpy as np\n\n"
            "xg = np.linspace(0.0, 5.0, 101)\n"
            "yg = 1.0 + 0.3 * xg + 0.15 * np.cos(1.7 * xg)\n"
        ),
        md("### A. Закрепление\n\n## 1. Площадь трапециями на [0,5]"),
        code(
            "area_hw = None\n"
            "assert area_hw is not None\n"
            "assert 0 < float(area_hw) < 20\n"
            "print(round(float(area_hw), 4))"
        ),
        md("## 2. Накопленный loss модели C"),
        code(
            "loss_c = np.array([3.0, 2.7, 2.5, 2.35, 2.2, 2.1, 2.0, 1.94, 1.9, 1.86])\n"
            "cum_c = None\n"
            "assert cum_c is not None and float(cum_c) > 0\n"
            "print(round(float(cum_c), 4))"
        ),
        md("### B. Вызов\n\n## 3. Сравните C и D по накопленной ошибке"),
        code(
            "loss_d = np.array([3.0, 2.6, 2.35, 2.2, 2.08, 1.98, 1.9, 1.83, 1.79, 1.76])\n"
            "cum_d = None\n"
            "best = ''\n"
            "assert cum_d is not None\n"
            "assert best in {'C', 'D'}\n"
            "print(cum_c, cum_d, best)"
        ),
        md("## 4. Пояснение для одноклассника"),
        code(
            "AREA_NOTE = ''\n"
            "assert len(AREA_NOTE) > 150\n"
            "print(AREA_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: интеграл обзорно\n\n" + SOL_BANNER),
        code(
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n\n"
            "def curve(x):\n"
            "    return 1.2 + 0.4 * x + 0.2 * np.sin(1.3 * x)\n\n"
            "xs = np.linspace(0.0, 6.0, 121)\n"
            "ys = curve(xs)\n"
            "dx = 0.2\n"
            "grid = np.arange(0.0, 6.0 + dx, dx)\n"
            "area_left = float(np.sum(curve(grid[:-1])) * dx)\n"
            "area_trap = float(np.trapezoid(curve(grid), grid))\n"
            "epoch_loss = np.array([2.4, 2.1, 1.9, 1.7, 1.55, 1.45, 1.38, 1.34, 1.31, 1.29])\n"
            "epochs = np.arange(len(epoch_loss), dtype=float)\n"
            "cum_loss = float(np.trapezoid(epoch_loss, epochs))\n"
            "loss_a = np.array([2.4, 2.1, 1.9, 1.7, 1.55, 1.45, 1.38, 1.34, 1.31, 1.29])\n"
            "loss_b = np.array([2.4, 2.2, 2.0, 1.85, 1.72, 1.62, 1.55, 1.50, 1.46, 1.43])\n"
            "area_a = float(np.trapezoid(loss_a, epochs))\n"
            "area_b = float(np.trapezoid(loss_b, epochs))\n"
            "better = 'A' if area_a < area_b else 'B'\n"
            "INTEGRAL_NOTE = (\n"
            "    'Интеграл здесь читается как накопление: чем меньше площадь под кривой loss по эпохам, '\n"
            "    'тем меньше суммарная ошибка, которую модель " 
            "допускала в процессе обучения.'\n"
            ")\n"
            "xg = np.linspace(0.0, 5.0, 101)\n"
            "yg = 1.0 + 0.3 * xg + 0.15 * np.cos(1.7 * xg)\n"
            "area_hw = float(np.trapezoid(yg, xg))\n"
            "loss_c = np.array([3.0, 2.7, 2.5, 2.35, 2.2, 2.1, 2.0, 1.94, 1.9, 1.86])\n"
            "loss_d = np.array([3.0, 2.6, 2.35, 2.2, 2.08, 1.98, 1.9, 1.83, 1.79, 1.76])\n"
            "cum_c = float(np.trapezoid(loss_c, epochs))\n"
            "cum_d = float(np.trapezoid(loss_d, epochs))\n"
            "best = 'C' if cum_c < cum_d else 'D'\n"
            "AREA_NOTE = (\n"
            "    'Площадь под кривой полезна, когда важен не только последний loss, но и весь путь обучения. '\n"
            "    'Модель, которая быстрее опускается вниз, обычно дает меньшую накопленную ошибку.'\n"
            ")\n"
            "print(round(area_left, 4), round(area_trap, 4))\n"
            "print(round(cum_loss, 4), round(area_a, 4), round(area_b, 4), better)\n"
            "print(round(area_hw, 4), round(cum_c, 4), round(cum_d, 4), best)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson04() -> None:
    base = "lessons/04_practice_min_loss_year_reflect"
    lesson = nb(
        md("# Практика: двигаемся к минимуму loss + рефлексия года"),
        code(
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n\n"
            "x_data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])\n"
            "y_data = np.array([2.2, 3.9, 6.1, 8.0, 10.2])\n\n"
            "def mse_for_w(w):\n"
            "    pred = w * x_data\n"
            "    return float(np.mean((pred - y_data) ** 2))\n"
        ),
        md("## 1. Численная производная loss по параметру w"),
        code(
            "def num_derivative(fun, x, h=1e-4):\n"
            "    return None\n\n\n"
            "grad_w1 = num_derivative(mse_for_w, 1.0)\n"
            "assert grad_w1 is not None\n"
            "print(round(float(grad_w1), 4))"
        ),
        md("## 2. Градиентный спуск по w"),
        code(
            "def gd_param(fun, start_w, eta=0.05, steps=60):\n"
            "    return None, None\n\n\n"
            "w_path, loss_path = gd_param(mse_for_w, start_w=0.2, eta=0.05, steps=60)\n"
            "assert w_path is not None and loss_path is not None\n"
            "assert len(w_path) == 61 and len(loss_path) == 61\n"
            "assert float(loss_path[-1]) < float(loss_path[0])\n"
            "print(w_path[-1], loss_path[-1])"
        ),
        md("## 3. Сравнение eta"),
        code(
            "eta_cmp = {}\n"
            "assert set(eta_cmp.keys()) == {0.01, 0.05, 0.2}\n"
            "print(eta_cmp)"
        ),
        md("## 4. Минимум loss и проверка"),
        code(
            "best_w = None\n"
            "best_loss = None\n"
            "assert best_w is not None and best_loss is not None\n"
            "assert 0 < float(best_w) < 5\n"
            "assert float(best_loss) < 2\n"
            "print(best_w, best_loss)"
        ),
        md("## 5. Итог года и мост к 9 классу"),
        code(
            "YEAR_NOTE = ''\n"
            "BRIDGE_NOTE = ''\n"
            "assert len(YEAR_NOTE) > 220\n"
            "assert len(BRIDGE_NOTE) > 160\n"
            "print(YEAR_NOTE)\n"
            "print(BRIDGE_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: финальный мини-отчёт полигона"),
        code(
            "import numpy as np\n\n"
            "x_data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])\n"
            "y_data = np.array([2.2, 3.9, 6.1, 8.0, 10.2])\n\n"
            "def mse_for_w(w):\n"
            "    pred = w * x_data\n"
            "    return float(np.mean((pred - y_data) ** 2))\n\n"
            "def num_derivative(fun, x, h=1e-4):\n"
            "    return None\n\n"
            "def gd_param(fun, start_w, eta=0.05, steps=60):\n"
            "    return None, None\n"
        ),
        md("### A. Закрепление\n\n## 1. Найдите минимум от другого старта"),
        code(
            "w2, l2 = gd_param(mse_for_w, start_w=4.8, eta=0.05, steps=60)\n"
            "assert w2 is not None and l2 is not None\n"
            "assert len(w2) == 61\n"
            "print(w2[-1], l2[-1])"
        ),
        md("## 2. Что будет при eta=0.35"),
        code(
            "w_bad, l_bad = gd_param(mse_for_w, start_w=0.2, eta=0.35, steps=20)\n"
            "assert w_bad is not None and l_bad is not None\n"
            "print(l_bad[:5], l_bad[-1])"
        ),
        md("### B. Вызов\n\n## 3. Короткий отчёт команды"),
        code(
            "REPORT = ''\n"
            "READY = False\n"
            "assert len(REPORT) > 420\n"
            "assert READY is True\n"
            "print(REPORT)"
        ),
        md("## 4. Личная рефлексия за 8 класс"),
        code(
            "PERSONAL_NOTE = ''\n"
            "assert len(PERSONAL_NOTE) > 170\n"
            "print(PERSONAL_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: минимум loss и рефлексия\n\n" + SOL_BANNER),
        code(
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n\n"
            "x_data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])\n"
            "y_data = np.array([2.2, 3.9, 6.1, 8.0, 10.2])\n\n"
            "def mse_for_w(w):\n"
            "    pred = w * x_data\n"
            "    return float(np.mean((pred - y_data) ** 2))\n\n"
            "def num_derivative(fun, x, h=1e-4):\n"
            "    return float((fun(x + h) - fun(x - h)) / (2 * h))\n\n"
            "def gd_param(fun, start_w, eta=0.05, steps=60):\n"
            "    w = float(start_w)\n"
            "    w_path = [w]\n"
            "    loss_path = [float(fun(w))]\n"
            "    for _ in range(steps):\n"
            "        grad = num_derivative(fun, w)\n"
            "        w = float(w - eta * grad)\n"
            "        w_path.append(w)\n"
            "        loss_path.append(float(fun(w)))\n"
            "    return w_path, loss_path\n\n"
            "grad_w1 = num_derivative(mse_for_w, 1.0)\n"
            "w_path, loss_path = gd_param(mse_for_w, start_w=0.2, eta=0.05, steps=60)\n"
            "eta_cmp = {}\n"
            "for e in (0.01, 0.05, 0.2):\n"
            "    wp, lp = gd_param(mse_for_w, start_w=0.2, eta=e, steps=60)\n"
            "    eta_cmp[e] = {'w_last': round(float(wp[-1]), 4), 'loss_last': round(float(lp[-1]), 4)}\n"
            "best_w = float(w_path[-1])\n"
            "best_loss = float(loss_path[-1])\n"
            "YEAR_NOTE = (\n"
            "    'За 8 класс мы прошли путь от функций и первых метрик до осмысленного чтения loss и численного градиентного спуска. '\n"
            "    'Ключевой результат — умение не просто запускать готовый fit, а понимать, как параметры шаг за шагом двигаются к минимуму ошибки '\n"
            "    'и как выбор шага влияет на стабильность обучения.'\n"
            ")\n"
            "BRIDGE_NOTE = (\n"
            "    'В 9 классе эта интуиция перейдет в более строгий язык: многомерные параметры, частные производные и аналитические градиенты. '\n"
            "    'Сейчас база уже есть: знак производной, размер шага и поведение loss на траектории.'\n"
            ")\n"
            "w2, l2 = gd_param(mse_for_w, start_w=4.8, eta=0.05, steps=60)\n"
            "w_bad, l_bad = gd_param(mse_for_w, start_w=0.2, eta=0.35, steps=20)\n"
            "REPORT = (\n"
            "    f'Мы минимизировали loss для модели y=w*x на пяти точках. '\n"
            "    f'Со старта w=0.2 градиентный спуск с eta=0.05 пришел к w={best_w:.4f}, loss={best_loss:.4f}. '\n"
            "    'Траектория loss монотонно снижалась, что подтверждает корректный выбор шага. '\n"
            "    f'Со старта w=4.8 алгоритм пришел к похожему минимуму w={w2[-1]:.4f}, loss={l2[-1]:.4f}, '\n"
            "    'значит точка минимума устойчива для разных стартов в этой задаче. '\n"
            "    f'При слишком большом eta=0.35 траектория стала менее стабильной (финальный loss={l_bad[-1]:.4f}). '\n"
            "    'Вывод: для учебной 1D-задачи работаем через тест нескольких eta и выбираем тот, где loss падает быстро и без скачков.'\n"
            ")\n"
            "READY = True\n"
            "PERSONAL_NOTE = (\n"
            "    'Самое полезное за год — переход от механического кода к инженерному мышлению: проверять входы, '\n"
            "    'сравнивать baseline, анализировать метрики и объяснять ограничения каждого результата.'\n"
            ")\n"
            "print(round(grad_w1, 4), best_w, best_loss)\n"
            "print(eta_cmp)\n"
            "print(w2[-1], l2[-1], l_bad[-1])\n"
            "print('READY=', READY)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


BUILDERS = [add_lesson01, add_lesson02, add_lesson03, add_lesson04]


def main() -> None:
    for builder in BUILDERS:
        builder()
    for rel, notebook in NOTEBOOKS.items():
        write(rel, notebook)
    print(f"done: {len(NOTEBOOKS)} notebooks in {len(BUILDERS)} lessons")


if __name__ == "__main__":
    main()
