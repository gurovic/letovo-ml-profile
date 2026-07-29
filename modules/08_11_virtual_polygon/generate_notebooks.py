#!/usr/bin/env python3
"""Generate the twelve teaching notebooks for module 08_11.

The generator is the source of truth.  Learner notebooks contain stubs and
contract asserts.  Teacher solutions repeat the same headings and keep one
short code cell per section; they never collapse the lesson into a code dump.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOL_BANNER = (
    "**Для преподавателя.** Ниже по разделам разобраны все задачи "
    "`lesson.ipynb` и `homework.ipynb`. Не выдавать до сдачи."
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


def learner_notebook(title: str, setup: str, sections: list[tuple[str, str, str]]) -> dict:
    cells = [md(f"# {title}"), code(setup)]
    for heading, learner_code, _ in sections:
        cells.extend((md(heading), code(learner_code)))
    return nb(cells)


def solution_notebook(
    title: str,
    setup: str,
    lesson_sections: list[tuple[str, str, str]],
    homework_setup: str,
    homework_sections: list[tuple[str, str, str]],
) -> dict:
    cells = [md(f"# Решения: {title}\n\n{SOL_BANNER}"), code(setup)]
    for heading, _, solution_code in lesson_sections:
        cells.extend((md(heading.replace("## ", "## Урок. ", 1)), code(solution_code)))
    cells.extend((md("## ДЗ. Данные и функции"), code(homework_setup)))
    for heading, _, solution_code in homework_sections:
        clean = heading.replace("## A. ", "").replace("## B. ", "").replace("## C. ", "").replace("## D. ", "")
        cells.extend((md(f"## ДЗ. {clean}"), code(solution_code)))
    return nb(cells)


def write(rel_path: str, notebook: dict) -> None:
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)} ({len(notebook['cells'])} cells)")


def add_bundle(
    base: str,
    title: str,
    setup: str,
    lesson_sections: list[tuple[str, str, str]],
    homework_title: str,
    homework_setup: str,
    homework_sections: list[tuple[str, str, str]],
) -> dict[str, dict]:
    return {
        f"{base}/lesson.ipynb": learner_notebook(title, setup, lesson_sections),
        f"{base}/homework.ipynb": learner_notebook(homework_title, homework_setup, homework_sections),
        f"{base}/solutions.ipynb": solution_notebook(
            title, setup, lesson_sections, homework_setup, homework_sections
        ),
    }


def lesson01() -> dict[str, dict]:
    setup = """import numpy as np
import matplotlib.pyplot as plt

def relief(x):
    return 0.08 * (x - 3) ** 3 + 0.6 * (x - 3) ** 2 + 2

xs = np.linspace(-2, 8, 201)
ys = relief(xs)
"""
    sections = [
        (
            "## 1. Средняя скорость на отрезке",
            """x_left, x_right = 0.0, 2.0
average_rate = None  # (relief(x_right) - relief(x_left)) / ...
assert average_rate is not None
assert np.isfinite(average_rate)
print(round(float(average_rate), 4))
""",
            """x_left, x_right = 0.0, 2.0
average_rate = (relief(x_right) - relief(x_left)) / (x_right - x_left)
assert np.isfinite(average_rate)
print(round(float(average_rate), 4))
""",
        ),
        (
            "## 2. Две оценки производной",
            """def derivative_forward(fun, x, h=1e-3):
    return None

def derivative_central(fun, x, h=1e-3):
    return None

d_forward = derivative_forward(relief, 1.0)
d_central = derivative_central(relief, 1.0)
assert d_forward is not None and d_central is not None
assert abs(float(d_forward) - float(d_central)) < 0.02
print(d_forward, d_central)
""",
            """def derivative_forward(fun, x, h=1e-3):
    return float((fun(x + h) - fun(x)) / h)

def derivative_central(fun, x, h=1e-3):
    return float((fun(x + h) - fun(x - h)) / (2 * h))

d_forward = derivative_forward(relief, 1.0)
d_central = derivative_central(relief, 1.0)
assert abs(d_forward - d_central) < 0.02
print(round(d_forward, 6), round(d_central, 6))
""",
        ),
        (
            "## 3. Эксперимент с шагом h",
            """h_values = [1.0, 0.1, 0.01, 0.001]
estimates = []  # центральная оценка в x=1 для каждого h
assert len(estimates) == len(h_values)
assert all(np.isfinite(value) for value in estimates)
print(list(zip(h_values, estimates)))
""",
            """h_values = [1.0, 0.1, 0.01, 0.001]
estimates = [derivative_central(relief, 1.0, h) for h in h_values]
assert len(estimates) == len(h_values)
print(list(zip(h_values, [round(value, 6) for value in estimates])))
""",
        ),
        (
            "## 4. Карта направлений",
            """probe_points = [-1.0, 0.0, 2.0, 4.0, 6.0]
directions = []  # 'up', 'down' или 'flat'; flat при |d| < 0.05
assert len(directions) == len(probe_points)
assert set(directions) <= {"up", "down", "flat"}
print(list(zip(probe_points, directions)))
""",
            """probe_points = [-1.0, 0.0, 2.0, 4.0, 6.0]
directions = []
for point in probe_points:
    slope = derivative_central(relief, point)
    directions.append("up" if slope > 0.05 else "down" if slope < -0.05 else "flat")
assert len(directions) == len(probe_points)
print(list(zip(probe_points, directions)))
""",
        ),
        (
            "## 5. График рельефа и точек",
            """fig, ax = plt.subplots(figsize=(8, 4))
# Постройте relief(xs), отметьте probe_points и подпишите оси.
assert len(ax.lines) >= 1
assert ax.get_xlabel() and ax.get_ylabel()
plt.show()
""",
            """fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(xs, ys, label="relief(x)")
ax.scatter(probe_points, [relief(x) for x in probe_points], color="crimson", label="probes")
ax.set(xlabel="x", ylabel="height", title="Рельеф виртуального полигона")
ax.legend()
assert len(ax.lines) >= 1 and ax.get_xlabel() and ax.get_ylabel()
plt.show()
""",
        ),
        (
            "## 6. Поиск почти горизонтальной точки",
            """scan = np.linspace(0.0, 7.0, 701)
flat_x = None
flat_slope = None
assert flat_x is not None and flat_slope is not None
assert 0.0 <= float(flat_x) <= 7.0
assert abs(float(flat_slope)) < 0.02
print(flat_x, flat_slope)
""",
            """scan = np.linspace(0.0, 7.0, 701)
scan_slopes = np.array([derivative_central(relief, x) for x in scan])
flat_index = int(np.argmin(np.abs(scan_slopes)))
flat_x = float(scan[flat_index])
flat_slope = float(scan_slopes[flat_index])
assert abs(flat_slope) < 0.02
print(flat_x, flat_slope)
""",
        ),
        (
            "## 7. Минимум или максимум",
            """left_slope = None
right_slope = None
stationary_kind = ""  # 'minimum', 'maximum' или 'neither'
assert left_slope is not None and right_slope is not None
assert stationary_kind in {"minimum", "maximum", "neither"}
print(left_slope, right_slope, stationary_kind)
""",
            """left_slope = derivative_central(relief, flat_x - 0.1)
right_slope = derivative_central(relief, flat_x + 0.1)
if left_slope < 0 < right_slope:
    stationary_kind = "minimum"
elif left_slope > 0 > right_slope:
    stationary_kind = "maximum"
else:
    stationary_kind = "neither"
assert stationary_kind in {"minimum", "maximum", "neither"}
print(round(left_slope, 4), round(right_slope, 4), stationary_kind)
""",
        ),
        (
            "## 8. Открытый эксперимент: когда h слишком мал",
            """tiny_h_values = [1e-3, 1e-6, 1e-9, 1e-12]
tiny_estimates = []  # оценки в x=1
H_NOTE = ""  # 2–4 предложения: что стабильно, а где видна ошибка округления
assert len(tiny_estimates) == len(tiny_h_values)
assert len(H_NOTE) >= 120
print(tiny_estimates)
print(H_NOTE)
""",
            """tiny_h_values = [1e-3, 1e-6, 1e-9, 1e-12]
tiny_estimates = [derivative_central(relief, 1.0, h) for h in tiny_h_values]
H_NOTE = (
    "Уменьшение h сначала почти не меняет оценку. При экстремально малом h вычитаются "
    "почти равные числа, поэтому ошибка округления становится заметной. Малый шаг полезен, "
    "но правило «чем меньше, тем лучше» для численных вычислений неверно."
)
assert len(H_NOTE) >= 120
print(tiny_estimates)
print(H_NOTE)
""",
        ),
        (
            "## 9. Самостоятельно: функция slope_map",
            """def slope_map(fun, points, h=1e-3, tolerance=0.05):
    # Верните список пар (point, direction).
    return None

mapped = slope_map(relief, [-1.0, 3.0, 5.0])
assert mapped is not None and len(mapped) == 3
assert all(len(item) == 2 for item in mapped)
assert all(item[1] in {"up", "down", "flat"} for item in mapped)
print(mapped)
""",
            """def slope_map(fun, points, h=1e-3, tolerance=0.05):
    result = []
    for point in points:
        slope = derivative_central(fun, point, h)
        direction = "up" if slope > tolerance else "down" if slope < -tolerance else "flat"
        result.append((point, direction))
    return result

mapped = slope_map(relief, [-1.0, 3.0, 5.0])
assert len(mapped) == 3
print(mapped)
""",
        ),
    ]
    hw_setup = """import numpy as np

def terrain(x):
    return 0.5 * (x + 1) ** 2 + np.sin(1.5 * x)

def derivative_central(fun, x, h=1e-3):
    return float((fun(x + h) - fun(x - h)) / (2 * h))
"""
    homework = [
        (
            "## A. Закрепление: скорости на новой функции",
            """average_rate = None
slopes = []  # в точках -2, 0, 2
assert average_rate is not None
assert len(slopes) == 3
assert all(np.isfinite(value) for value in slopes)
print(average_rate, slopes)
""",
            """average_rate = (terrain(3.0) - terrain(1.0)) / 2.0
slopes = [derivative_central(terrain, point) for point in (-2.0, 0.0, 2.0)]
assert len(slopes) == 3
print(round(average_rate, 4), [round(value, 4) for value in slopes])
""",
        ),
        (
            "## B. База: стационарные точки",
            """grid = np.linspace(-3.0, 3.0, 1201)
candidate_x = []  # точки, где |производная| < 0.02
assert len(candidate_x) >= 1
assert all(-3.0 <= x <= 3.0 for x in candidate_x)
print(candidate_x[:10])
""",
            """grid = np.linspace(-3.0, 3.0, 1201)
candidate_x = [float(x) for x in grid if abs(derivative_central(terrain, x)) < 0.02]
assert candidate_x
print(candidate_x[:10])
""",
        ),
        (
            "## C. Углубление: устойчивость к h",
            """test_h = [0.5, 0.1, 0.01, 0.001]
flat_by_h = []  # лучшая почти горизонтальная точка для каждого h
assert len(flat_by_h) == len(test_h)
assert all(-3.0 <= x <= 3.0 for x in flat_by_h)
print(list(zip(test_h, flat_by_h)))
""",
            """test_h = [0.5, 0.1, 0.01, 0.001]
flat_by_h = []
for h in test_h:
    values = [abs(derivative_central(terrain, x, h)) for x in grid]
    flat_by_h.append(float(grid[int(np.argmin(values))]))
assert len(flat_by_h) == len(test_h)
print(list(zip(test_h, flat_by_h)))
""",
        ),
        (
            "## D. Вызов: несколько стационарных точек",
            """STATIONARY_NOTE = ""  # какие кандидаты минимумы/максимумы и как проверили знаком
READY = False
assert len(STATIONARY_NOTE) >= 220
assert READY is True
print(STATIONARY_NOTE)
""",
            """STATIONARY_NOTE = (
    "Сканирование дает группы соседних кандидатов, а не уникальные точные корни. Для каждого "
    "кластера я беру одну точку и сравниваю знак производной слева и справа. Переход «минус → плюс» "
    "означает локальный минимум, «плюс → минус» — локальный максимум. Такой тест различает тип "
    "стационарной точки, но его результат зависит от сетки, допуска и шага h."
)
READY = True
assert len(STATIONARY_NOTE) >= 220 and READY
print(STATIONARY_NOTE)
""",
        ),
    ]
    return add_bundle(
        "lessons/01_derivative_intuition",
        "Производная как скорость изменения",
        setup,
        sections,
        "ДЗ: производная как численный датчик",
        hw_setup,
        homework,
    )


def lesson02() -> dict[str, dict]:
    setup = """import numpy as np
import matplotlib.pyplot as plt

def loss(x):
    return (x - 2.5) ** 2 + 0.2

def derivative_central(fun, x, h=1e-4):
    return float((fun(x + h) - fun(x - h)) / (2 * h))
"""
    sections = [
        (
            "## 1. Проверка направления шага",
            """x0, eta = -1.0, 0.2
gradient0 = None
x1 = None
assert gradient0 is not None and x1 is not None
assert loss(x1) < loss(x0)
print(x0, gradient0, x1, loss(x1))
""",
            """x0, eta = -1.0, 0.2
gradient0 = derivative_central(loss, x0)
x1 = x0 - eta * gradient0
assert loss(x1) < loss(x0)
print(x0, gradient0, x1, loss(x1))
""",
        ),
        (
            "## 2. Один шаг как функция",
            """def gd_step(fun, x, eta):
    return None

left_step = gd_step(loss, -1.0, 0.1)
right_step = gd_step(loss, 4.0, 0.1)
assert left_step is not None and right_step is not None
assert left_step > -1.0 and right_step < 4.0
print(left_step, right_step)
""",
            """def gd_step(fun, x, eta):
    return float(x - eta * derivative_central(fun, x))

left_step = gd_step(loss, -1.0, 0.1)
right_step = gd_step(loss, 4.0, 0.1)
assert left_step > -1.0 and right_step < 4.0
print(left_step, right_step)
""",
        ),
        (
            "## 3. Полная траектория",
            """def gradient_descent_1d(fun, start, eta=0.1, steps=25):
    # Верните два списка, включая стартовую точку.
    return None, None

path_x, path_loss = gradient_descent_1d(loss, -1.0, eta=0.2, steps=20)
assert path_x is not None and path_loss is not None
assert len(path_x) == len(path_loss) == 21
assert path_loss[-1] < path_loss[0]
print(path_x[-1], path_loss[-1])
""",
            """def gradient_descent_1d(fun, start, eta=0.1, steps=25):
    x = float(start)
    path_x = [x]
    path_loss = [float(fun(x))]
    for _ in range(steps):
        x = gd_step(fun, x, eta)
        path_x.append(x)
        path_loss.append(float(fun(x)))
    return path_x, path_loss

path_x, path_loss = gradient_descent_1d(loss, -1.0, eta=0.2, steps=20)
assert len(path_x) == len(path_loss) == 21 and path_loss[-1] < path_loss[0]
print(path_x[-1], path_loss[-1])
""",
        ),
        (
            "## 4. Инварианты траектории",
            """is_finite = None
non_increasing = None
assert isinstance(is_finite, (bool, np.bool_))
assert isinstance(non_increasing, (bool, np.bool_))
assert is_finite and non_increasing
print(is_finite, non_increasing)
""",
            """is_finite = bool(np.all(np.isfinite(path_loss)))
non_increasing = bool(np.all(np.diff(path_loss) <= 1e-10))
assert is_finite and non_increasing
print(is_finite, non_increasing)
""",
        ),
        (
            "## 5. Сравнение трех шагов обучения",
            """eta_values = [0.03, 0.2, 0.9]
final_losses = []  # финальный loss после 25 шагов
assert len(final_losses) == len(eta_values)
assert all(np.isfinite(value) for value in final_losses)
print(list(zip(eta_values, final_losses)))
""",
            """eta_values = [0.03, 0.2, 0.9]
final_losses = [
    gradient_descent_1d(loss, -1.0, eta=value, steps=25)[1][-1]
    for value in eta_values
]
assert len(final_losses) == len(eta_values)
print(list(zip(eta_values, final_losses)))
""",
        ),
        (
            "## 6. График траекторий",
            """fig, ax = plt.subplots(figsize=(8, 4))
# Для каждого eta постройте loss по номеру шага.
assert len(ax.lines) == len(eta_values)
assert ax.get_xlabel() and ax.get_ylabel()
plt.show()
""",
            """fig, ax = plt.subplots(figsize=(8, 4))
for value in eta_values:
    _, losses = gradient_descent_1d(loss, -1.0, eta=value, steps=25)
    ax.plot(losses, marker=".", label=f"eta={value}")
ax.set(xlabel="step", ylabel="loss", title="Как eta меняет траекторию")
ax.legend()
assert len(ax.lines) == len(eta_values)
plt.show()
""",
        ),
        (
            "## 7. Критерий ранней остановки",
            """def gradient_descent_until(fun, start, eta=0.1, max_steps=100, tolerance=1e-5):
    # Остановитесь, когда |gradient| < tolerance.
    return None, None

short_x, short_loss = gradient_descent_until(loss, -1.0, eta=0.2)
assert short_x is not None and short_loss is not None
assert 2 <= len(short_x) <= 101
assert abs(derivative_central(loss, short_x[-1])) < 1e-5
print(len(short_x), short_x[-1], short_loss[-1])
""",
            """def gradient_descent_until(fun, start, eta=0.1, max_steps=100, tolerance=1e-5):
    x = float(start)
    path_x, path_loss = [x], [float(fun(x))]
    for _ in range(max_steps):
        gradient = derivative_central(fun, x)
        if abs(gradient) < tolerance:
            break
        x = float(x - eta * gradient)
        path_x.append(x)
        path_loss.append(float(fun(x)))
    return path_x, path_loss

short_x, short_loss = gradient_descent_until(loss, -1.0, eta=0.2)
assert abs(derivative_central(loss, short_x[-1])) < 1e-5
print(len(short_x), short_x[-1], short_loss[-1])
""",
        ),
        (
            "## 8. Самостоятельно: диагностический отчёт",
            """def diagnose_run(losses):
    # Верните 'converged', 'slow', 'unstable' или 'invalid'.
    return None

diagnoses = [diagnose_run(gradient_descent_1d(loss, -1, e, 25)[1]) for e in eta_values]
ETA_NOTE = ""
assert set(diagnoses) <= {"converged", "slow", "unstable", "invalid"}
assert len(diagnoses) == 3 and len(ETA_NOTE) >= 160
print(diagnoses)
print(ETA_NOTE)
""",
            """def diagnose_run(losses):
    values = np.asarray(losses, dtype=float)
    if not np.all(np.isfinite(values)):
        return "invalid"
    if np.any(np.diff(values) > 1e-9):
        return "unstable"
    if len(values) >= 2 and abs(values[-1] - values[-2]) < 1e-6:
        return "converged"
    return "slow"

diagnoses = [diagnose_run(gradient_descent_1d(loss, -1, e, 25)[1]) for e in eta_values]
ETA_NOTE = (
    "Шаг eta выбирают по траектории, а не по одному финальному числу. Малый шаг может быть "
    "стабильным, но медленным; слишком большой дает рост или колебания loss. Для этой квадратичной "
    "функции eta=0.2 быстро уменьшает loss без нарушения монотонности."
)
assert len(ETA_NOTE) >= 160
print(diagnoses)
print(ETA_NOTE)
""",
        ),
    ]
    hw_setup = setup + """
def rugged_loss(x):
    return 0.15 * (x - 4.0) ** 2 + 0.3 * np.sin(2.2 * x) + 1.0
"""
    homework = [
        (
            "## A. Закрепление: перенесите GD",
            """def gd(fun, start, eta=0.08, steps=40):
    return None, None

path_a, loss_a = gd(rugged_loss, -2.0)
assert path_a is not None and loss_a is not None
assert len(path_a) == len(loss_a) == 41
assert np.all(np.isfinite(loss_a))
print(path_a[-1], loss_a[-1])
""",
            """def gd(fun, start, eta=0.08, steps=40):
    x = float(start)
    path_x, losses = [x], [float(fun(x))]
    for _ in range(steps):
        x -= eta * derivative_central(fun, x)
        path_x.append(float(x))
        losses.append(float(fun(x)))
    return path_x, losses

path_a, loss_a = gd(rugged_loss, -2.0)
assert len(path_a) == len(loss_a) == 41
print(path_a[-1], loss_a[-1])
""",
        ),
        (
            "## B. База: разные старты",
            """starts = [-2.0, 1.0, 7.0]
end_x = []
end_loss = []
assert len(end_x) == len(end_loss) == len(starts)
assert all(np.isfinite(value) for value in end_loss)
print(list(zip(starts, end_x, end_loss)))
""",
            """starts = [-2.0, 1.0, 7.0]
runs = [gd(rugged_loss, start) for start in starts]
end_x = [path[-1] for path, _ in runs]
end_loss = [losses[-1] for _, losses in runs]
assert len(end_x) == len(starts)
print(list(zip(starts, end_x, end_loss)))
""",
        ),
        (
            "## C. Углубление: сетка eta",
            """eta_grid = [0.01, 0.03, 0.08, 0.15, 0.3]
eta_scores = []  # пары (eta, final_loss)
best_eta = None
assert len(eta_scores) == len(eta_grid)
assert best_eta in eta_grid
print(eta_scores, best_eta)
""",
            """eta_grid = [0.01, 0.03, 0.08, 0.15, 0.3]
eta_scores = [(eta, gd(rugged_loss, -2.0, eta=eta)[1][-1]) for eta in eta_grid]
best_eta = min(eta_scores, key=lambda item: item[1])[0]
assert best_eta in eta_grid
print(eta_scores, best_eta)
""",
        ),
        (
            "## D. Вызов: локальные минимумы",
            """LOCAL_NOTE = ""  # почему разные старты могут дать разные ответы
COUNTEREXAMPLE_READY = False
assert len(LOCAL_NOTE) >= 240
assert COUNTEREXAMPLE_READY is True
print(LOCAL_NOTE)
""",
            """LOCAL_NOTE = (
    "На неровной функции градиентный спуск использует только локальный наклон и не видит весь "
    "рельеф. Поэтому два старта могут попасть в разные впадины и закончить с разными loss. "
    "Меньший финальный loss среди нескольких запусков лучше в этом эксперименте, но перебор "
    "трех стартов не доказывает нахождение глобального минимума. Это ограничение метода, а не "
    "ошибка реализации."
)
COUNTEREXAMPLE_READY = True
assert len(LOCAL_NOTE) >= 240 and COUNTEREXAMPLE_READY
print(LOCAL_NOTE)
""",
        ),
    ]
    return add_bundle(
        "lessons/02_practice_gd_1d",
        "Практика численного градиентного спуска в 1D",
        setup,
        sections,
        "ДЗ: устойчивость градиентного спуска",
        hw_setup,
        homework,
    )


def lesson03() -> dict[str, dict]:
    setup = """import numpy as np
import matplotlib.pyplot as plt

def curve(x):
    return 1.2 + 0.4 * x + 0.2 * np.sin(1.3 * x)

left, right = 0.0, 6.0
"""
    sections = [
        (
            "## 1. Левые прямоугольники",
            """def left_rectangle_area(fun, left, right, parts):
    return None

area_10 = left_rectangle_area(curve, left, right, 10)
assert area_10 is not None and 0 < area_10 < 30
print(area_10)
""",
            """def left_rectangle_area(fun, left, right, parts):
    dx = (right - left) / parts
    points = left + np.arange(parts) * dx
    return float(np.sum(fun(points)) * dx)

area_10 = left_rectangle_area(curve, left, right, 10)
assert 0 < area_10 < 30
print(round(area_10, 4))
""",
        ),
        (
            "## 2. Трапеции без готовой функции",
            """def trapezoid_area(fun, left, right, parts):
    return None

trap_10 = trapezoid_area(curve, left, right, 10)
assert trap_10 is not None and 0 < trap_10 < 30
print(trap_10)
""",
            """def trapezoid_area(fun, left, right, parts):
    points = np.linspace(left, right, parts + 1)
    values = fun(points)
    dx = (right - left) / parts
    return float(dx * (0.5 * values[0] + np.sum(values[1:-1]) + 0.5 * values[-1]))

trap_10 = trapezoid_area(curve, left, right, 10)
assert 0 < trap_10 < 30
print(round(trap_10, 4))
""",
        ),
        (
            "## 3. Сходимость оценки площади",
            """parts_values = [5, 10, 20, 100]
left_estimates = []
trap_estimates = []
assert len(left_estimates) == len(trap_estimates) == len(parts_values)
assert all(np.isfinite(value) for value in left_estimates + trap_estimates)
print(left_estimates)
print(trap_estimates)
""",
            """parts_values = [5, 10, 20, 100]
left_estimates = [left_rectangle_area(curve, left, right, n) for n in parts_values]
trap_estimates = [trapezoid_area(curve, left, right, n) for n in parts_values]
assert len(left_estimates) == len(trap_estimates) == len(parts_values)
print([round(x, 5) for x in left_estimates])
print([round(x, 5) for x in trap_estimates])
""",
        ),
        (
            "## 4. Визуализация накопления",
            """grid = np.linspace(left, right, 101)
fig, ax = plt.subplots(figsize=(8, 4))
# Постройте curve(grid) и закрасьте площадь до оси x.
assert len(ax.lines) >= 1 and len(ax.collections) >= 1
assert ax.get_xlabel() and ax.get_ylabel()
plt.show()
""",
            """grid = np.linspace(left, right, 101)
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(grid, curve(grid), color="navy")
ax.fill_between(grid, 0, curve(grid), alpha=0.25)
ax.set(xlabel="x", ylabel="curve(x)", title="Площадь как накопленная величина")
assert len(ax.lines) >= 1 and len(ax.collections) >= 1
plt.show()
""",
        ),
        (
            "## 5. Площадь под историей loss",
            """epoch_loss = np.array([2.4, 2.1, 1.9, 1.7, 1.55, 1.45, 1.38, 1.34, 1.31, 1.29])
epochs = np.arange(len(epoch_loss), dtype=float)
accumulated_loss = None
assert accumulated_loss is not None and accumulated_loss > 0
print(accumulated_loss)
""",
            """epoch_loss = np.array([2.4, 2.1, 1.9, 1.7, 1.55, 1.45, 1.38, 1.34, 1.31, 1.29])
epochs = np.arange(len(epoch_loss), dtype=float)
accumulated_loss = float(np.trapezoid(epoch_loss, epochs))
assert accumulated_loss > 0
print(round(accumulated_loss, 4))
""",
        ),
        (
            "## 6. Финальный loss и весь путь — разные критерии",
            """loss_a = np.array([2.4, 2.1, 1.8, 1.55, 1.35, 1.2, 1.1, 1.04, 1.01, 1.0])
loss_b = np.array([2.4, 1.7, 1.3, 1.1, 1.02, 0.99, 0.98, 0.98, 0.99, 1.02])
final_winner = ""
area_winner = ""
assert final_winner in {"A", "B"} and area_winner in {"A", "B"}
assert final_winner != area_winner
print(final_winner, area_winner)
""",
            """loss_a = np.array([2.4, 2.1, 1.8, 1.55, 1.35, 1.2, 1.1, 1.04, 1.01, 1.0])
loss_b = np.array([2.4, 1.7, 1.3, 1.1, 1.02, 0.99, 0.98, 0.98, 0.99, 1.02])
final_winner = "A" if loss_a[-1] < loss_b[-1] else "B"
area_a = float(np.trapezoid(loss_a, epochs))
area_b = float(np.trapezoid(loss_b, epochs))
area_winner = "A" if area_a < area_b else "B"
assert final_winner != area_winner
print(final_winner, area_winner, round(area_a, 3), round(area_b, 3))
""",
        ),
        (
            "## 7. Нормировка по времени",
            """short_loss = loss_b[:5]
raw_short = None
mean_short = None
mean_full = None
assert raw_short is not None and mean_short is not None and mean_full is not None
assert raw_short > 0 and mean_short > 0 and mean_full > 0
print(raw_short, mean_short, mean_full)
""",
            """short_loss = loss_b[:5]
raw_short = float(np.trapezoid(short_loss))
mean_short = raw_short / (len(short_loss) - 1)
mean_full = float(np.trapezoid(loss_b)) / (len(loss_b) - 1)
assert raw_short > 0 and mean_short > 0 and mean_full > 0
print(round(raw_short, 4), round(mean_short, 4), round(mean_full, 4))
""",
        ),
        (
            "## 8. Самостоятельно: границы метрики",
            """INTEGRAL_NOTE = ""  # когда площадь полезна и почему это не стандартный training loss
assert len(INTEGRAL_NOTE) >= 260
assert "финаль" in INTEGRAL_NOTE.lower()
print(INTEGRAL_NOTE)
""",
            """INTEGRAL_NOTE = (
    "Площадь под кривой loss описывает весь путь обучения и полезна для сравнения скорости "
    "снижения ошибки при одинаковых эпохах и стоимости шага. Она не заменяет финальный loss: "
    "модель с меньшей площадью может закончить хуже, а длина запуска напрямую меняет сырую площадь. "
    "Поэтому сравнивать нужно одинаковые интервалы или нормированную площадь. Это диагностическая "
    "метрика эксперимента, а не функция потерь, которую модель обязательно минимизирует."
)
assert len(INTEGRAL_NOTE) >= 260
print(INTEGRAL_NOTE)
""",
        ),
    ]
    hw_setup = """import numpy as np

def trapezoid_from_values(values, step=1.0):
    values = np.asarray(values, dtype=float)
    return float(step * (0.5 * values[0] + np.sum(values[1:-1]) + 0.5 * values[-1]))
"""
    homework = [
        (
            "## A. Закрепление: площадь по таблице",
            """x = np.linspace(0.0, 5.0, 101)
y = 1.0 + 0.3 * x + 0.15 * np.cos(1.7 * x)
area = None
assert area is not None and 0 < area < 20
print(area)
""",
            """x = np.linspace(0.0, 5.0, 101)
y = 1.0 + 0.3 * x + 0.15 * np.cos(1.7 * x)
area = trapezoid_from_values(y, step=x[1] - x[0])
assert 0 < area < 20
print(round(area, 4))
""",
        ),
        (
            "## B. База: сравнение историй",
            """loss_c = np.array([3.0, 2.7, 2.5, 2.35, 2.2, 2.1, 2.0, 1.94, 1.9, 1.86])
loss_d = np.array([3.0, 2.6, 2.35, 2.2, 2.08, 1.98, 1.9, 1.83, 1.79, 1.76])
areas = []
winner = ""
assert len(areas) == 2 and winner in {"C", "D"}
print(areas, winner)
""",
            """loss_c = np.array([3.0, 2.7, 2.5, 2.35, 2.2, 2.1, 2.0, 1.94, 1.9, 1.86])
loss_d = np.array([3.0, 2.6, 2.35, 2.2, 2.08, 1.98, 1.9, 1.83, 1.79, 1.76])
areas = [trapezoid_from_values(loss_c), trapezoid_from_values(loss_d)]
winner = "C" if areas[0] < areas[1] else "D"
assert winner == "D"
print(areas, winner)
""",
        ),
        (
            "## C. Углубление: честное сравнение разной длины",
            """short_run = loss_d[:6]
long_run = loss_d
normalized = []  # средняя площадь на один интервал для двух запусков
assert len(normalized) == 2
assert all(value > 0 for value in normalized)
print(normalized)
""",
            """short_run = loss_d[:6]
long_run = loss_d
normalized = [
    trapezoid_from_values(short_run) / (len(short_run) - 1),
    trapezoid_from_values(long_run) / (len(long_run) - 1),
]
assert len(normalized) == 2
print(normalized)
""",
        ),
        (
            "## D. Вызов: контрпример для площади",
            """COUNTEREXAMPLE = ""  # две истории: меньшая площадь, но худший финальный loss
READY = False
assert len(COUNTEREXAMPLE) >= 260
assert READY is True
print(COUNTEREXAMPLE)
""",
            """COUNTEREXAMPLE = (
    "Например, история P = [5, 1, 1, 1] имеет площадь 5, а финальный loss 1. "
    "История Q = [2, 2, 2, 0.5] имеет площадь 5.25, но заканчивает с меньшим loss 0.5. "
    "По площади лучше P, по финальному качеству лучше Q. Контрпример показывает, что критерии "
    "отвечают на разные вопросы: площадь — о затратах ошибки на пути, финальное значение — "
    "о результате последнего шага. Выбор критерия должен следовать задаче."
)
READY = True
assert len(COUNTEREXAMPLE) >= 260 and READY
print(COUNTEREXAMPLE)
""",
        ),
    ]
    return add_bundle(
        "lessons/03_integral_loss_overview",
        "Интеграл как накопление: площадь под кривой loss",
        setup,
        sections,
        "ДЗ: площадь и история ошибки",
        hw_setup,
        homework,
    )


def lesson04() -> dict[str, dict]:
    setup = """import numpy as np
import matplotlib.pyplot as plt

x_data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
y_data = np.array([2.2, 3.9, 6.1, 8.0, 10.2])

def predict(w):
    return w * x_data

def mse_for_w(w):
    return float(np.mean((predict(w) - y_data) ** 2))

def derivative_central(fun, x, h=1e-4):
    return float((fun(x + h) - fun(x - h)) / (2 * h))
"""
    sections = [
        (
            "## 1. Рельеф MSE по параметру w",
            """w_grid = np.linspace(0.0, 4.0, 161)
loss_grid = []  # MSE для каждого w
grid_best_w = None
assert len(loss_grid) == len(w_grid)
assert grid_best_w is not None and 0 < grid_best_w < 4
print(grid_best_w, min(loss_grid))
""",
            """w_grid = np.linspace(0.0, 4.0, 161)
loss_grid = [mse_for_w(w) for w in w_grid]
grid_best_w = float(w_grid[int(np.argmin(loss_grid))])
assert 0 < grid_best_w < 4
print(grid_best_w, min(loss_grid))
""",
        ),
        (
            "## 2. Знак производной MSE",
            """probe_w = [0.5, 1.5, 2.5, 3.5]
gradients = []
assert len(gradients) == len(probe_w)
assert gradients[0] < 0 < gradients[-1]
print(list(zip(probe_w, gradients)))
""",
            """probe_w = [0.5, 1.5, 2.5, 3.5]
gradients = [derivative_central(mse_for_w, w) for w in probe_w]
assert gradients[0] < 0 < gradients[-1]
print(list(zip(probe_w, gradients)))
""",
        ),
        (
            "## 3. Спуск по параметру модели",
            """def fit_w(start_w, eta=0.05, steps=40):
    # Верните траектории w и MSE, включая старт.
    return None, None

w_path, loss_path = fit_w(0.2)
assert w_path is not None and loss_path is not None
assert len(w_path) == len(loss_path) == 41
assert loss_path[-1] < loss_path[0]
print(w_path[-1], loss_path[-1])
""",
            """def fit_w(start_w, eta=0.05, steps=40):
    w = float(start_w)
    w_path, losses = [w], [mse_for_w(w)]
    for _ in range(steps):
        w -= eta * derivative_central(mse_for_w, w)
        w_path.append(float(w))
        losses.append(mse_for_w(w))
    return w_path, losses

w_path, loss_path = fit_w(0.2)
assert len(w_path) == len(loss_path) == 41 and loss_path[-1] < loss_path[0]
print(w_path[-1], loss_path[-1])
""",
        ),
        (
            "## 4. Сравнение eta по траектории",
            """eta_values = [0.01, 0.05, 0.2]
eta_final_loss = []
eta_status = []  # 'stable' или 'unstable'
assert len(eta_final_loss) == len(eta_status) == len(eta_values)
assert set(eta_status) <= {"stable", "unstable"}
assert "unstable" in eta_status
print(list(zip(eta_values, eta_final_loss, eta_status)))
""",
            """eta_values = [0.01, 0.05, 0.2]
runs = [fit_w(0.2, eta=eta, steps=30) for eta in eta_values]
eta_final_loss = [losses[-1] for _, losses in runs]
eta_status = [
    "stable" if np.all(np.isfinite(losses)) and np.all(np.diff(losses) <= 1e-9) else "unstable"
    for _, losses in runs
]
assert "unstable" in eta_status
print(list(zip(eta_values, eta_final_loss, eta_status)))
""",
        ),
        (
            "## 5. Разные старты — один минимум",
            """starts = [0.2, 1.0, 3.0, 4.8]
end_w = []
end_loss = []
assert len(end_w) == len(end_loss) == len(starts)
assert max(end_w) - min(end_w) < 0.02
print(list(zip(starts, end_w, end_loss)))
""",
            """starts = [0.2, 1.0, 3.0, 4.8]
runs_by_start = [fit_w(start, eta=0.05, steps=40) for start in starts]
end_w = [path[-1] for path, _ in runs_by_start]
end_loss = [losses[-1] for _, losses in runs_by_start]
assert max(end_w) - min(end_w) < 0.02
print(list(zip(starts, end_w, end_loss)))
""",
        ),
        (
            "## 6. Визуальная проверка модели",
            """best_w = end_w[0]
fig, ax = plt.subplots(figsize=(7, 4))
# Точки данных и линия y = best_w * x.
assert len(ax.lines) >= 1 and len(ax.collections) >= 1
assert ax.get_xlabel() and ax.get_ylabel()
plt.show()
""",
            """best_w = end_w[0]
fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(x_data, y_data, label="data")
ax.plot(x_data, best_w * x_data, color="crimson", label=f"w={best_w:.3f}")
ax.set(xlabel="x", ylabel="y", title="Модель после минимизации MSE")
ax.legend()
assert len(ax.lines) >= 1 and len(ax.collections) >= 1
plt.show()
""",
        ),
        (
            "## 7. Сверка с точным минимумом",
            """exact_w = None  # для y=w*x: sum(x*y) / sum(x*x)
gap = None
assert exact_w is not None and gap is not None
assert abs(float(gap)) < 0.02
print(exact_w, best_w, gap)
""",
            """exact_w = float(np.sum(x_data * y_data) / np.sum(x_data ** 2))
gap = float(best_w - exact_w)
assert abs(gap) < 0.02
print(exact_w, best_w, gap)
""",
        ),
        (
            "## 8. Самостоятельно: паспорт запуска",
            """RUN_REPORT = ""  # данные, старт, eta, шаги, финальный w/MSE, проверка и ограничение
BRIDGE_NOTE = ""  # что переносится в 9 класс, без изучения многомерного градиента сейчас
READY = False
assert len(RUN_REPORT) >= 320
assert len(BRIDGE_NOTE) >= 180
assert READY is True
print(RUN_REPORT)
print(BRIDGE_NOTE)
""",
            """RUN_REPORT = (
    f"Модель y=w*x обучалась на пяти парах наблюдений. Из старта w=0.2 за 40 шагов при "
    f"eta=0.05 получено w={best_w:.4f} и MSE={mse_for_w(best_w):.4f}. Loss убывал на каждом "
    f"шаге; четыре разных старта пришли к значениям w с разбросом меньше 0.02. Точный минимум "
    f"для этой специальной модели равен {exact_w:.4f}, расхождение с численным ответом {gap:.4g}. "
    "Вывод относится к выпуклому 1D-рельефу; на неровной или многомерной функции одних этих "
    "проверок недостаточно."
)
BRIDGE_NOTE = (
    "В 9 классе параметров станет несколько, а направление будет задаваться набором частных "
    "производных. Из этого модуля переносится инженерный цикл: выбрать шаг, записать траекторию, "
    "проверить конечность и снижение loss, сравнить старты и явно назвать границы вывода."
)
READY = True
assert len(RUN_REPORT) >= 320 and len(BRIDGE_NOTE) >= 180 and READY
print(RUN_REPORT)
print(BRIDGE_NOTE)
""",
        ),
    ]
    hw_setup = setup + """
def fit_w(start_w, eta=0.05, steps=40):
    w = float(start_w)
    w_path, losses = [w], [mse_for_w(w)]
    for _ in range(steps):
        w -= eta * derivative_central(mse_for_w, w)
        w_path.append(float(w))
        losses.append(mse_for_w(w))
    return w_path, losses
"""
    homework = [
        (
            "## A. Закрепление: другой старт",
            """path, losses = fit_w(4.8, eta=0.05, steps=40)
final_w = None
final_loss = None
assert final_w is not None and final_loss is not None
assert len(path) == len(losses) == 41
assert final_loss < losses[0]
print(final_w, final_loss)
""",
            """path, losses = fit_w(4.8, eta=0.05, steps=40)
final_w = path[-1]
final_loss = losses[-1]
assert final_loss < losses[0]
print(final_w, final_loss)
""",
        ),
        (
            "## B. База: автоматическая проверка запуска",
            """def run_is_stable(losses):
    return None

stable = run_is_stable(losses)
_, bad_losses = fit_w(0.2, eta=0.2, steps=20)
bad_stable = run_is_stable(bad_losses)
assert stable is True and bad_stable is False
print(stable, bad_stable)
""",
            """def run_is_stable(losses):
    values = np.asarray(losses, dtype=float)
    return bool(np.all(np.isfinite(values)) and np.all(np.diff(values) <= 1e-9))

stable = run_is_stable(losses)
_, bad_losses = fit_w(0.2, eta=0.2, steps=20)
bad_stable = run_is_stable(bad_losses)
assert stable is True and bad_stable is False
print(stable, bad_stable)
""",
        ),
        (
            "## C. Углубление: модель со свободным членом",
            """def mse_for_b(b, fixed_w=2.0):
    return None

def fit_b(start_b, eta=0.05, steps=40):
    return None, None

b_path, b_losses = fit_b(-2.0)
assert b_path is not None and b_losses is not None
assert len(b_path) == len(b_losses) == 41
assert b_losses[-1] < b_losses[0]
print(b_path[-1], b_losses[-1])
""",
            """def mse_for_b(b, fixed_w=2.0):
    predictions = fixed_w * x_data + b
    return float(np.mean((predictions - y_data) ** 2))

def fit_b(start_b, eta=0.05, steps=40):
    b = float(start_b)
    path, losses = [b], [mse_for_b(b)]
    for _ in range(steps):
        b -= eta * derivative_central(mse_for_b, b)
        path.append(float(b))
        losses.append(mse_for_b(b))
    return path, losses

b_path, b_losses = fit_b(-2.0)
assert b_losses[-1] < b_losses[0]
print(b_path[-1], b_losses[-1])
""",
        ),
        (
            "## D. Вызов: итоговый отчёт полигона",
            """FINAL_REPORT = ""  # 5 абзацев: задача, метод, evidence, ограничение, следующий вопрос
PERSONAL_NOTE = ""  # конкретная способность за год и свидетельство
READY = False
assert len(FINAL_REPORT) >= 520
assert len(PERSONAL_NOTE) >= 180
assert READY is True
print(FINAL_REPORT)
print(PERSONAL_NOTE)
""",
            """FINAL_REPORT = (
    "Задача. Мы подбирали один параметр w модели y=w*x по минимуму MSE на пяти наблюдениях.\\n\\n"
    "Метод. Производную MSE оценивали центральной разностью и обновляли w правилом "
    "w = w - eta * gradient, сохраняя всю траекторию.\\n\\n"
    f"Свидетельства. При eta=0.05 и старте 4.8 финальный w={final_w:.4f}, "
    f"MSE={final_loss:.4f}; loss снижался монотонно. При eta=0.2 проверка пометила запуск "
    "нестабильным.\\n\\n"
    "Ограничение. Один параметр и выпуклый MSE-рельеф не показывают локальные минимумы и "
    "взаимодействие нескольких параметров. Совпадение разных стартов здесь ожидаемо и не "
    "является общей гарантией градиентного спуска.\\n\\n"
    "Следующий вопрос. Как хранить и обновлять направление, если у модели одновременно меняются "
    "w и свободный член b, и как выбирать шаги для параметров разного масштаба?"
)
PERSONAL_NOTE = (
    "За год я научился связывать код с проверяемым утверждением: задавать контракт assert, "
    "сохранять промежуточные результаты, сравнивать метрики и отделять наблюдение от гарантии. "
    "В этом модуле свидетельство — диагностическая функция, которая различает стабильную и "
    "расходящуюся траектории по самим значениям loss."
)
READY = True
assert len(FINAL_REPORT) >= 520 and len(PERSONAL_NOTE) >= 180 and READY
print(FINAL_REPORT)
print(PERSONAL_NOTE)
""",
        ),
    ]
    return add_bundle(
        "lessons/04_practice_min_loss_year_reflect",
        "Практика: минимум MSE и итог модуля",
        setup,
        sections,
        "ДЗ: итоговый отчёт виртуального полигона",
        hw_setup,
        homework,
    )


BUILDERS = [lesson01, lesson02, lesson03, lesson04]


def main() -> None:
    notebooks: dict[str, dict] = {}
    for builder in BUILDERS:
        notebooks.update(builder())
    for rel_path, notebook in notebooks.items():
        write(rel_path, notebook)
    print(f"done: {len(notebooks)} notebooks in {len(BUILDERS)} lessons")


if __name__ == "__main__":
    main()
