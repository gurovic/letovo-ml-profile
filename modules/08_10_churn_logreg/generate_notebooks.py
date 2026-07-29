#!/usr/bin/env python3
"""Generate gold-standard notebooks for module 08_10.

The generator is the source of truth. Student notebooks contain stubs and
executable contracts; sectional teacher notebooks solve every lesson and
homework task. The post-call column ``duration`` is forbidden in every model.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_CSV = ROOT / "data" / "bank_marketing_slim.csv"
LESSON_DIRS = [
    "lessons/01_logreg_sigmoid_threshold",
    "lessons/02_practice_fit_threshold",
    "lessons/03_imbalance_metrics",
    "lessons/04_practice_metrics_cli",
    "lessons/05_venv_requirements_readme",
]

SOL_BANNER = (
    "**Для преподавателя.** Полный эталон к `lesson.ipynb` и "
    "`homework.ipynb`; ученикам до сдачи не показывать."
)

LOAD_DATA = """from pathlib import Path
import numpy as np
import pandas as pd


def find_bank_csv() -> Path:
    for path in (Path("bank_marketing_slim.csv"), Path("../../data/bank_marketing_slim.csv")):
        if path.exists():
            return path.resolve()
    raise FileNotFoundError("bank_marketing_slim.csv не найден рядом с ноутбуком или в ../../data/")


CSV_PATH = find_bank_csv()
df = pd.read_csv(CSV_PATH)
target = df["y"].eq("yes").astype(int)
assert len(df) > 0 and set(target.unique()) == {0, 1}
assert "duration" in df.columns  # колонка видна только для разбора утечки
print(f"Строк: {len(df)}; доля yes: {target.mean():.3f}")
"""

MODEL_IMPORTS = """
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
"""

SAFE_FEATURES = """FEATURE_COLUMNS = [column for column in df.columns if column not in {"y", "duration"}]
assert "duration" not in FEATURE_COLUMNS, "LEAKAGE: duration известна только после звонка"
assert "y" not in FEATURE_COLUMNS
"""


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


def student_notebook(title: str, setup: str, sections: list[tuple[str, str]]) -> dict:
    cells = [md(f"# {title}"), code(setup)]
    for text, source in sections:
        cells.extend((md(text), code(source)))
    return nb(cells)


def solution_notebook(title: str, setup: str, sections: list[tuple[str, str]]) -> dict:
    cells = [md(f"# Решения: {title}\n\n{SOL_BANNER}"), code(setup)]
    for heading, source in sections:
        cells.extend((md(heading), code(source)))
    return nb(cells)


def write(relative: str, notebook: dict) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {relative}: {len(notebook['cells'])} cells")


def add(base: str, lesson: dict, homework: dict, solutions: dict) -> None:
    write(f"{base}/lesson.ipynb", lesson)
    write(f"{base}/homework.ipynb", homework)
    write(f"{base}/solutions.ipynb", solutions)


def lesson01() -> None:
    base = LESSON_DIRS[0]
    lesson = student_notebook(
        "Логистическая регрессия: score, сигмоида и порог",
        LOAD_DATA,
        [
            (
                "## 1. Момент предсказания\n\n"
                "Разделите колонки на доступные до звонка и известные после него. "
                "`duration` должна оказаться только во второй группе.",
                """before_call = None  # TODO: все колонки, кроме y и duration
after_call = None   # TODO: список из duration
assert isinstance(before_call, list) and isinstance(after_call, list)
assert "duration" not in before_call
assert after_call == ["duration"]
assert set(before_call) | {"duration", "y"} == set(df.columns)
""",
            ),
            (
                "## 2. Почему `duration` — утечка\n\n"
                "Опишите, в какой момент значение становится известно и почему "
                "его нельзя получить для ещё не совершённого звонка.",
                """LEAKAGE_NOTE = ""  # TODO: не менее 180 символов
assert len(LEAKAGE_NOTE) >= 180
assert "duration" in LEAKAGE_NOTE.lower()
assert any(word in LEAKAGE_NOTE.lower() for word in ["после", "звон"])
""",
            ),
            (
                "## 3. Линейный score\n\n"
                "Реализуйте сумму `intercept + weight * value` для одного признака.",
                """def linear_score(value, weight, intercept):
    # TODO
    ...


assert abs(linear_score(2.0, 1.5, -1.0) - 2.0) < 1e-9
assert abs(linear_score(0.0, 7.0, -0.4) + 0.4) < 1e-9
""",
            ),
            (
                "## 4. Сигмоида\n\n"
                "Преобразуйте число или массив score в значения строго между 0 и 1.",
                """def sigmoid(z):
    # TODO: используйте np.asarray и np.exp
    ...


grid = np.array([-4.0, 0.0, 4.0])
probabilities = sigmoid(grid)
assert probabilities.shape == grid.shape
assert np.all((probabilities > 0) & (probabilities < 1))
assert abs(float(sigmoid(0.0)) - 0.5) < 1e-9
""",
            ),
            (
                "## 5. Монотонность вероятности\n\n"
                "Проверьте, как меняется вероятность на score от -6 до 6.",
                """score_grid = np.arange(-6.0, 7.0, 1.0)
probability_grid = None  # TODO
is_increasing = None     # TODO
assert len(probability_grid) == len(score_grid)
assert is_increasing is True
assert np.all(np.diff(probability_grid) > 0)
""",
            ),
            (
                "## 6. Функция порога\n\n"
                "Верните бинарные метки: 1, если вероятность не меньше порога.",
                """def apply_threshold(proba, threshold=0.5):
    # TODO
    ...


demo = np.array([0.10, 0.30, 0.49, 0.50, 0.82])
assert apply_threshold(demo, 0.5).tolist() == [0, 0, 0, 1, 1]
assert apply_threshold(demo, 0.3).tolist() == [0, 1, 1, 1, 1]
""",
            ),
            (
                "## 7. Сколько клиентов попадёт в обзвон\n\n"
                "Для пяти порогов посчитайте число положительных решений.",
                """demo_proba = np.array([0.06, 0.18, 0.24, 0.31, 0.47, 0.52, 0.68, 0.79, 0.91])
thresholds = [0.2, 0.35, 0.5, 0.65, 0.8]
selected_counts = None  # TODO: список чисел
assert len(selected_counts) == len(thresholds)
assert all(isinstance(value, (int, np.integer)) for value in selected_counts)
assert all(selected_counts[i] >= selected_counts[i + 1] for i in range(len(selected_counts) - 1))
""",
            ),
            (
                "## 8. Открытый эксперимент: порог под бюджет\n\n"
                "Бюджет позволяет выбрать не более трёх клиентов. Найдите "
                "наименьший порог из сетки 0.05…0.95, который соблюдает бюджет.",
                """budget = 3
threshold_grid = np.arange(0.05, 1.0, 0.05)
budget_threshold = None  # TODO
chosen = None            # TODO: индексы выбранных клиентов
assert budget_threshold is not None
assert 0.05 <= budget_threshold <= 0.95
assert isinstance(chosen, np.ndarray) and len(chosen) <= budget
""",
            ),
            (
                "## 9. Самостоятельно: контракт решения\n\n"
                "Напишите функцию, которая возвращает и метки, и число выбранных.",
                """def campaign_decision(proba, threshold):
    # TODO: return labels, selected_count
    ...


labels, count = campaign_decision(demo_proba, 0.5)
assert labels.shape == demo_proba.shape
assert set(np.unique(labels)) <= {0, 1}
assert count == int(labels.sum())
assert count == 4
""",
            ),
        ],
    )
    homework = student_notebook(
        "ДЗ: сигмоида, порог и защита от leakage",
        LOAD_DATA,
        [
            (
                "### Part A — обязательно\n\n## A1. Score для нескольких клиентов",
                """ages = np.array([22, 35, 47, 61], dtype=float)
scores = None  # TODO: -3 + 0.06 * age
assert isinstance(scores, np.ndarray) and scores.shape == ages.shape
assert np.isfinite(scores).all()
""",
            ),
            (
                "## A2. Вероятности и решения\n\n"
                "Используйте свои `sigmoid` и `apply_threshold`.",
                """def sigmoid(z):
    # TODO
    ...


def apply_threshold(proba, threshold):
    # TODO
    ...


age_proba = sigmoid(scores)
age_pred = apply_threshold(age_proba, 0.5)
assert age_proba.shape == ages.shape and age_pred.shape == ages.shape
assert np.all((age_proba > 0) & (age_proba < 1))
assert set(np.unique(age_pred)) <= {0, 1}
""",
            ),
            (
                "## A3. Проверка списка признаков",
                """FEATURE_COLUMNS = None  # TODO
assert isinstance(FEATURE_COLUMNS, list) and len(FEATURE_COLUMNS) >= 5
assert "duration" not in FEATURE_COLUMNS
assert "y" not in FEATURE_COLUMNS
assert set(FEATURE_COLUMNS) <= set(df.columns)
""",
            ),
            (
                "### Challenge\n\n## B1. Контрпример к «точнее значит лучше»\n\n"
                "Объясните, почему высокая test-метрика с `duration` не делает "
                "модель пригодной для выбора клиентов до звонка.",
                """COUNTEREXAMPLE = ""  # TODO: не менее 240 символов
assert len(COUNTEREXAMPLE) >= 240
assert "duration" in COUNTEREXAMPLE.lower()
assert any(word in COUNTEREXAMPLE.lower() for word in ["момент", "после", "до звон"])
""",
            ),
            (
                "## B2. Устойчивость бюджетного порога\n\n"
                "Сравните порог при бюджете 2, 3 и 4 клиента.",
                """budgets = [2, 3, 4]
budget_thresholds = []  # TODO
assert len(budget_thresholds) == len(budgets)
assert all(0.0 < value < 1.0 for value in budget_thresholds)
assert all(budget_thresholds[i] >= budget_thresholds[i + 1] for i in range(len(budgets) - 1))
""",
            ),
        ],
    )
    solutions = solution_notebook(
        "score, сигмоида и порог",
        LOAD_DATA,
        [
            ("## Урок. 1. Момент предсказания", 'before_call = [c for c in df.columns if c not in {"y", "duration"}]\nafter_call = ["duration"]\nassert "duration" not in before_call\n'),
            ("## Урок. 2. Объяснение leakage", 'LEAKAGE_NOTE = ("duration измеряет длительность уже состоявшегося звонка и становится известна только после контакта. "\n"В момент выбора клиента для будущего обзвона такого значения нет. Модель увидит связь с результатом, "\n"но этот сигнал нельзя воспроизвести в реальном процессе; test-оценка будет вводить в заблуждение.")\nassert len(LEAKAGE_NOTE) >= 180\n'),
            ("## Урок. 3. Линейный score", "def linear_score(value, weight, intercept):\n    return intercept + weight * value\n\nassert linear_score(2.0, 1.5, -1.0) == 2.0\n"),
            ("## Урок. 4–5. Сигмоида и монотонность", "def sigmoid(z):\n    arr = np.asarray(z, dtype=float)\n    return 1.0 / (1.0 + np.exp(-arr))\n\nscore_grid = np.arange(-6.0, 7.0, 1.0)\nprobability_grid = sigmoid(score_grid)\nis_increasing = bool(np.all(np.diff(probability_grid) > 0))\nassert is_increasing and abs(float(sigmoid(0.0)) - 0.5) < 1e-9\n"),
            ("## Урок. 6. Порог", "def apply_threshold(proba, threshold=0.5):\n    return (np.asarray(proba) >= threshold).astype(int)\n\ndemo = np.array([0.10, 0.30, 0.49, 0.50, 0.82])\nassert apply_threshold(demo, 0.5).tolist() == [0, 0, 0, 1, 1]\n"),
            ("## Урок. 7. Объём обзвона", "demo_proba = np.array([0.06, 0.18, 0.24, 0.31, 0.47, 0.52, 0.68, 0.79, 0.91])\nthresholds = [0.2, 0.35, 0.5, 0.65, 0.8]\nselected_counts = [int(apply_threshold(demo_proba, t).sum()) for t in thresholds]\nassert selected_counts == sorted(selected_counts, reverse=True)\n"),
            ("## Урок. 8. Порог под бюджет", "budget = 3\nthreshold_grid = np.arange(0.05, 1.0, 0.05)\nbudget_threshold = next(t for t in threshold_grid if apply_threshold(demo_proba, t).sum() <= budget)\nchosen = np.flatnonzero(apply_threshold(demo_proba, budget_threshold))\nassert len(chosen) <= budget\n"),
            ("## Урок. 9. Контракт решения", "def campaign_decision(proba, threshold):\n    labels = apply_threshold(proba, threshold)\n    return labels, int(labels.sum())\n\nlabels, count = campaign_decision(demo_proba, 0.5)\nassert count == 4\n"),
            ("## ДЗ. A1–A2. Score и решение", "ages = np.array([22, 35, 47, 61], dtype=float)\nscores = -3 + 0.06 * ages\nage_proba = sigmoid(scores)\nage_pred = apply_threshold(age_proba, 0.5)\nassert age_proba.shape == ages.shape\n"),
            ("## ДЗ. A3. Безопасные признаки", SAFE_FEATURES + 'assert "duration" not in FEATURE_COLUMNS\n'),
            ("## ДЗ. Challenge. Контрпример", 'COUNTEREXAMPLE = ("Даже если duration резко повышает test-метрику, результат непригоден для кампании: в момент решения, "\n"кому звонить, duration ещё не существует. Она появляется после звонка и частично отражает сам отклик. "\n"Следовательно, offline test проверяет задачу с недоступным сигналом, а не будущий процесс. Сравнивать модели нужно только на признаках, доступных до звонка.")\nassert len(COUNTEREXAMPLE) >= 240\n'),
            ("## ДЗ. Challenge. Устойчивость бюджета", "budgets = [2, 3, 4]\nbudget_thresholds = [next(t for t in threshold_grid if apply_threshold(demo_proba, t).sum() <= b) for b in budgets]\nassert budget_thresholds == sorted(budget_thresholds, reverse=True)\n"),
        ],
    )
    add(base, lesson, homework, solutions)


def lesson02() -> None:
    base = LESSON_DIRS[1]
    setup = LOAD_DATA + MODEL_IMPORTS
    lesson = student_notebook(
        "Практика: fit, predict_proba и выбор порога",
        setup,
        [
            ("## 1. Явный список безопасных признаков", """FEATURE_COLUMNS = None  # TODO
assert isinstance(FEATURE_COLUMNS, list) and len(FEATURE_COLUMNS) >= 5
assert "duration" not in FEATURE_COLUMNS and "y" not in FEATURE_COLUMNS
assert set(FEATURE_COLUMNS) <= set(df.columns)
"""),
            ("## 2. Кодирование категорий", """X = None  # TODO: pd.get_dummies(..., drop_first=True)
assert isinstance(X, pd.DataFrame) and len(X) == len(df)
assert "duration" not in X.columns
assert X.select_dtypes(exclude="number").shape[1] == 0
assert not X.isna().any().any()
"""),
            ("## 3. Стратифицированный train/test", """X_train, X_test, y_train, y_test = None, None, None, None  # TODO
assert X_train is not None and len(X_train) + len(X_test) == len(X)
assert set(X_train.index).isdisjoint(set(X_test.index))
assert abs(float(y_train.mean()) - float(y_test.mean())) < 0.05
"""),
            ("## 4. Обучение модели", """model = None  # TODO: LogisticRegression(max_iter=2000)
assert model is not None and hasattr(model, "coef_")
assert model.n_features_in_ == X_train.shape[1]
"""),
            ("## 5. Вероятность положительного класса", """proba_test = None  # TODO: второй столбец predict_proba
assert isinstance(proba_test, np.ndarray) and len(proba_test) == len(y_test)
assert np.all((0 <= proba_test) & (proba_test <= 1))
assert np.std(proba_test) > 0
"""),
            ("## 6. Функция метрик для порога", """def score_at_threshold(y_true, proba, threshold):
    # TODO: dict threshold, selected, precision, recall, f1
    ...


row_05 = score_at_threshold(y_test, proba_test, 0.5)
assert set(row_05) == {"threshold", "selected", "precision", "recall", "f1"}
assert 0 <= row_05["f1"] <= 1
"""),
            ("## 7. Таблица порогов", """thresholds = np.arange(0.10, 0.91, 0.05)
threshold_table = None  # TODO: DataFrame из score_at_threshold
assert isinstance(threshold_table, pd.DataFrame) and len(threshold_table) == len(thresholds)
assert threshold_table["selected"].is_monotonic_decreasing
assert threshold_table[["precision", "recall", "f1"]].apply(lambda s: s.between(0, 1).all()).all()
"""),
            ("## 8. Порог при ограничении recall\n\nВыберите среди строк с recall ≥ 0.70 строку с наибольшей precision.", """eligible = None  # TODO
chosen_row = None  # TODO: Series
assert isinstance(eligible, pd.DataFrame) and len(eligible) > 0
assert float(chosen_row["recall"]) >= 0.70
assert float(chosen_row["precision"]) == float(eligible["precision"].max())
"""),
            ("## 9. Самостоятельно: рекомендация кампании", """THRESHOLD_NOTE = ""  # TODO: числа chosen_row, компромисс и ограничение test
assert len(THRESHOLD_NOTE) >= 220
assert "recall" in THRESHOLD_NOTE.lower() and "precision" in THRESHOLD_NOTE.lower()
assert str(round(float(chosen_row["threshold"]), 2)) in THRESHOLD_NOTE
"""),
        ],
    )
    homework = student_notebook(
        "ДЗ: исследование порога классификации",
        setup,
        [
            ("### Part A — обязательно\n\n## A1. Воспроизвести безопасный pipeline", """FEATURE_COLUMNS = None  # TODO
X = None                # TODO
X_train, X_test, y_train, y_test = None, None, None, None  # TODO
model = None            # TODO
proba_test = None       # TODO
assert "duration" not in FEATURE_COLUMNS and "duration" not in X.columns
assert len(proba_test) == len(y_test)
"""),
            ("## A2. Более плотная сетка", """thresholds = np.arange(0.05, 0.96, 0.025)
rows = []  # TODO
table = pd.DataFrame(rows)
assert len(table) == len(thresholds)
assert {"threshold", "precision", "recall", "f1"} <= set(table.columns)
"""),
            ("## A3. Лучший F1", """best_f1_row = None  # TODO: Series
assert best_f1_row is not None
assert float(best_f1_row["f1"]) == float(table["f1"].max())
assert 0.05 <= float(best_f1_row["threshold"]) <= 0.95
"""),
            ("### Challenge\n\n## B1. Выбор при бюджете 15% test", """budget = max(1, int(np.ceil(0.15 * len(y_test))))
budget_rows = None  # TODO: selected <= budget
budget_choice = None  # TODO: максимум recall, затем precision
assert len(budget_rows) > 0
assert int(budget_choice["selected"]) <= budget
"""),
            ("## B2. Сравнение двух правил", """DECISION_NOTE = ""  # TODO: best F1 против budget choice, 260+ символов
assert len(DECISION_NOTE) >= 260
assert all(word in DECISION_NOTE.lower() for word in ["f1", "бюджет", "порог"])
"""),
        ],
    )
    prep = SAFE_FEATURES + """X = pd.get_dummies(df[FEATURE_COLUMNS], drop_first=True)
assert "duration" not in X.columns
X_train, X_test, y_train, y_test = train_test_split(
    X, target, test_size=0.25, random_state=61, stratify=target
)
model = LogisticRegression(max_iter=1000, solver="liblinear", class_weight="balanced")
model.fit(X_train, y_train)
proba_test = model.predict_proba(X_test)[:, 1]
"""
    metric_fn = """def score_at_threshold(y_true, proba, threshold):
    pred = (np.asarray(proba) >= threshold).astype(int)
    return {
        "threshold": float(threshold),
        "selected": int(pred.sum()),
        "precision": float(precision_score(y_true, pred, zero_division=0)),
        "recall": float(recall_score(y_true, pred, zero_division=0)),
        "f1": float(f1_score(y_true, pred, zero_division=0)),
    }
"""
    solutions = solution_notebook(
        "fit, predict_proba и порог",
        setup,
        [
            ("## Урок. 1–3. Признаки и split", prep + "assert abs(float(y_train.mean()) - float(y_test.mean())) < 0.05\n"),
            ("## Урок. 4–5. Fit и вероятности", "assert hasattr(model, 'coef_')\nassert len(proba_test) == len(y_test) and np.std(proba_test) > 0\n"),
            ("## Урок. 6. Контракт метрик", metric_fn + "row_05 = score_at_threshold(y_test, proba_test, 0.5)\nassert set(row_05) == {'threshold', 'selected', 'precision', 'recall', 'f1'}\n"),
            ("## Урок. 7. Сетка порогов", "thresholds = np.arange(0.10, 0.91, 0.05)\nthreshold_table = pd.DataFrame([score_at_threshold(y_test, proba_test, t) for t in thresholds])\nassert threshold_table['selected'].is_monotonic_decreasing\n"),
            ("## Урок. 8. Ограничение recall", "eligible = threshold_table[threshold_table['recall'].ge(0.70)]\nchosen_row = eligible.sort_values(['precision', 'threshold'], ascending=False).iloc[0]\nassert chosen_row['recall'] >= 0.70\n"),
            ("## Урок. 9. Рекомендация", 'THRESHOLD_NOTE = (f"Порог {chosen_row.threshold:.2f} сохраняет recall={chosen_row.recall:.3f} и среди допустимых строк даёт "\nf"precision={chosen_row.precision:.3f}. Это правило уменьшает пропуски отклика, но число звонков равно {int(chosen_row.selected)}. "\n"Вывод относится к одной test-выборке; перед кампанией порог нужно перепроверить на новом периоде и при реальном бюджете.")\nassert len(THRESHOLD_NOTE) >= 220\n'),
            ("## ДЗ. A1. Воспроизводимый pipeline", "assert 'duration' not in FEATURE_COLUMNS and 'duration' not in X.columns\nassert len(proba_test) == len(y_test)\n"),
            ("## ДЗ. A2. Плотная сетка", "thresholds = np.arange(0.05, 0.96, 0.025)\nrows = [score_at_threshold(y_test, proba_test, t) for t in thresholds]\ntable = pd.DataFrame(rows)\nassert len(table) == len(thresholds)\n"),
            ("## ДЗ. A3. Максимум F1", "best_f1_row = table.loc[table['f1'].idxmax()]\nassert best_f1_row['f1'] == table['f1'].max()\n"),
            ("## ДЗ. Challenge. Бюджет", "budget = max(1, int(np.ceil(0.15 * len(y_test))))\nbudget_rows = table[table['selected'].le(budget)]\nbudget_choice = budget_rows.sort_values(['recall', 'precision'], ascending=False).iloc[0]\nassert budget_choice['selected'] <= budget\n"),
            (
                "## ДЗ. Challenge. Два правила",
                """DECISION_NOTE = (
    f"Максимум F1 выбирает порог {best_f1_row.threshold:.3f} и балансирует precision и recall без явной цены звонка. "
    f"Бюджетное правило допускает не более {budget} клиентов и выбирает порог {budget_choice.threshold:.3f}; "
    "оно оптимизирует recall внутри ограничения. Если бюджет жёсткий, второе правило честнее бизнес-задаче. "
    "Если стоимость ошибок симметрична, F1 удобнее как сводный критерий. Оба порога оценены только на test."
)
assert len(DECISION_NOTE) >= 260
""",
            ),
        ],
    )
    add(base, lesson, homework, solutions)


def lesson03() -> None:
    base = LESSON_DIRS[2]
    setup = LOAD_DATA + MODEL_IMPORTS
    lesson = student_notebook(
        "Дисбаланс классов: матрица ошибок и метрики",
        setup,
        [
            ("## 1. Размер классов", """class_counts = None  # TODO: Series
positive_share = None  # TODO
assert int(class_counts.sum()) == len(df) and set(class_counts.index) == {0, 1}
assert 0 < positive_share < 0.5
"""),
            ("## 2. Baseline «всегда no»", """baseline_pred = None  # TODO
baseline_accuracy = None
baseline_recall = None
assert len(baseline_pred) == len(target)
assert baseline_accuracy > 0.5
assert baseline_recall == 0.0
"""),
            ("## 3. Безопасная модель", """FEATURE_COLUMNS = None  # TODO
X = None  # TODO
X_train, X_test, y_train, y_test = None, None, None, None  # TODO
model = None
proba = None
assert "duration" not in FEATURE_COLUMNS and "duration" not in X.columns
assert len(proba) == len(y_test)
"""),
            ("## 4. Матрица ошибок", """pred_05 = None  # TODO
tn, fp, fn, tp = None, None, None, None  # TODO
assert tn + fp + fn + tp == len(y_test)
assert all(value >= 0 for value in (tn, fp, fn, tp))
"""),
            ("## 5. Метрики вручную", """accuracy_manual = None
precision_manual = None
recall_manual = None
f1_manual = None
assert all(0 <= value <= 1 for value in (accuracy_manual, precision_manual, recall_manual, f1_manual))
"""),
            ("## 6. Сверка со sklearn", """sklearn_metrics = None  # TODO: dict
assert set(sklearn_metrics) == {"accuracy", "precision", "recall", "f1"}
assert abs(accuracy_manual - sklearn_metrics["accuracy"]) < 1e-12
assert abs(precision_manual - sklearn_metrics["precision"]) < 1e-12
assert abs(recall_manual - sklearn_metrics["recall"]) < 1e-12
assert abs(f1_manual - sklearn_metrics["f1"]) < 1e-12
"""),
            ("## 7. Цена ошибок", """ERROR_COSTS = {"fp": 1, "fn": 5}
cost_05 = None  # TODO
assert cost_05 == ERROR_COSTS["fp"] * fp + ERROR_COSTS["fn"] * fn
assert cost_05 >= 0
"""),
            ("## 8. Эксперимент с порогом", """cost_rows = []  # TODO: threshold, fp, fn, cost для 0.1..0.9
cost_table = pd.DataFrame(cost_rows)
assert len(cost_table) == 9
assert {"threshold", "fp", "fn", "cost"} <= set(cost_table.columns)
best_cost_row = cost_table.loc[cost_table["cost"].idxmin()]
assert best_cost_row["cost"] == cost_table["cost"].min()
"""),
            ("## 9. Самостоятельно: почему accuracy недостаточна", """METRIC_NOTE = ""  # TODO: baseline, FN и выбранный критерий; 240+ символов
assert len(METRIC_NOTE) >= 240
assert "accuracy" in METRIC_NOTE.lower()
assert any(word in METRIC_NOTE.lower() for word in ["recall", "fn", "пропуск"])
"""),
        ],
    )
    homework = student_notebook(
        "ДЗ: метрики под разные цены ошибок",
        setup,
        [
            ("### Part A — обязательно\n\n## A1. Подготовить модель без `duration`", """FEATURE_COLUMNS = None
X = None
X_train, X_test, y_train, y_test = None, None, None, None
model = None
proba = None
assert "duration" not in FEATURE_COLUMNS and "duration" not in X.columns
assert len(proba) == len(y_test)
"""),
            ("## A2. Универсальная строка метрик", """def metrics_row(y_true, proba, threshold):
    # TODO: threshold, tn, fp, fn, tp, accuracy, precision, recall, f1
    ...


row = metrics_row(y_test, proba, 0.5)
assert set(row) == {"threshold", "tn", "fp", "fn", "tp", "accuracy", "precision", "recall", "f1"}
assert row["tn"] + row["fp"] + row["fn"] + row["tp"] == len(y_test)
"""),
            ("## A3. Таблица 17 порогов", """thresholds = np.arange(0.10, 0.91, 0.05)
metric_table = None  # TODO
assert isinstance(metric_table, pd.DataFrame) and len(metric_table) == 17
assert metric_table["recall"].between(0, 1).all()
"""),
            ("### Challenge\n\n## B1. Три сценария стоимости", """cost_scenarios = {"balanced": (1, 1), "miss_expensive": (1, 6), "call_expensive": (5, 1)}
choices = []  # TODO: scenario, fp_cost, fn_cost, threshold, total_cost
choice_table = pd.DataFrame(choices)
assert len(choice_table) == 3
assert {"scenario", "threshold", "total_cost"} <= set(choice_table.columns)
"""),
            ("## B2. Рекомендация по сценариям", """COST_NOTE = ""  # TODO: сравнить три порога, 280+ символов
assert len(COST_NOTE) >= 280
assert all(name in COST_NOTE for name in cost_scenarios)
"""),
        ],
    )
    prep = SAFE_FEATURES + """X = pd.get_dummies(df[FEATURE_COLUMNS], drop_first=True)
assert "duration" not in X.columns
X_train, X_test, y_train, y_test = train_test_split(
    X, target, test_size=0.25, random_state=62, stratify=target
)
model = LogisticRegression(max_iter=1000, solver="liblinear", class_weight="balanced").fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]
"""
    metric_fn = """def metrics_row(y_true, proba_values, threshold):
    pred = (np.asarray(proba_values) >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, pred).ravel()
    return {
        "threshold": float(threshold), "tn": int(tn), "fp": int(fp),
        "fn": int(fn), "tp": int(tp),
        "accuracy": float(accuracy_score(y_true, pred)),
        "precision": float(precision_score(y_true, pred, zero_division=0)),
        "recall": float(recall_score(y_true, pred, zero_division=0)),
        "f1": float(f1_score(y_true, pred, zero_division=0)),
    }
"""
    solutions = solution_notebook(
        "дисбаланс и метрики",
        setup,
        [
            ("## Урок. 1. Размер классов", "class_counts = target.value_counts().sort_index()\npositive_share = float(target.mean())\nassert 0 < positive_share < 0.5\n"),
            ("## Урок. 2. Baseline", "baseline_pred = np.zeros(len(target), dtype=int)\nbaseline_accuracy = float(accuracy_score(target, baseline_pred))\nbaseline_recall = float(recall_score(target, baseline_pred, zero_division=0))\nassert baseline_recall == 0.0\n"),
            ("## Урок. 3. Модель без утечки", prep + "assert len(proba) == len(y_test)\n"),
            ("## Урок. 4. Матрица ошибок", "pred_05 = (proba >= 0.5).astype(int)\ntn, fp, fn, tp = (int(x) for x in confusion_matrix(y_test, pred_05).ravel())\nassert tn + fp + fn + tp == len(y_test)\n"),
            ("## Урок. 5. Метрики вручную", "accuracy_manual = (tn + tp) / (tn + fp + fn + tp)\nprecision_manual = tp / (tp + fp) if tp + fp else 0.0\nrecall_manual = tp / (tp + fn) if tp + fn else 0.0\nf1_manual = 2 * precision_manual * recall_manual / (precision_manual + recall_manual) if precision_manual + recall_manual else 0.0\nassert all(0 <= x <= 1 for x in (accuracy_manual, precision_manual, recall_manual, f1_manual))\n"),
            ("## Урок. 6. Сверка", "sklearn_metrics = {'accuracy': float(accuracy_score(y_test, pred_05)), 'precision': float(precision_score(y_test, pred_05, zero_division=0)), 'recall': float(recall_score(y_test, pred_05, zero_division=0)), 'f1': float(f1_score(y_test, pred_05, zero_division=0))}\nassert abs(f1_manual - sklearn_metrics['f1']) < 1e-12\n"),
            ("## Урок. 7–8. Цена ошибок", metric_fn + "\nERROR_COSTS = {'fp': 1, 'fn': 5}\ncost_05 = ERROR_COSTS['fp'] * fp + ERROR_COSTS['fn'] * fn\ncost_rows = []\nfor threshold in np.arange(0.1, 1.0, 0.1):\n    row = metrics_row(y_test, proba, threshold)\n    cost_rows.append({'threshold': threshold, 'fp': row['fp'], 'fn': row['fn'], 'cost': row['fp'] + 5 * row['fn']})\ncost_table = pd.DataFrame(cost_rows)\nbest_cost_row = cost_table.loc[cost_table['cost'].idxmin()]\nassert len(cost_table) == 9\n"),
            ("## Урок. 9. Выбор метрики", 'METRIC_NOTE = (f"Baseline получает accuracy={baseline_accuracy:.3f}, но recall=0: он не находит ни одного yes. "\n"Поэтому accuracy скрывает пропуски редкого класса. Для кампании смотрим confusion matrix, recall и FN; "\nf"при цене FN в пять раз выше FP минимальную стоимость дал порог {best_cost_row.threshold:.1f}. Этот выбор зависит от принятой цены ошибок, а не только от алгоритма.")\nassert len(METRIC_NOTE) >= 240\n'),
            ("## ДЗ. A1. Pipeline", "assert 'duration' not in FEATURE_COLUMNS and 'duration' not in X.columns\n"),
            ("## ДЗ. A2. Функция метрик", metric_fn + "row = metrics_row(y_test, proba, 0.5)\nassert row['tn'] + row['fp'] + row['fn'] + row['tp'] == len(y_test)\n"),
            ("## ДЗ. A3. Таблица", "thresholds = np.arange(0.10, 0.91, 0.05)\nmetric_table = pd.DataFrame([metrics_row(y_test, proba, t) for t in thresholds])\nassert len(metric_table) == 17\n"),
            ("## ДЗ. Challenge. Сценарии", "cost_scenarios = {'balanced': (1, 1), 'miss_expensive': (1, 6), 'call_expensive': (5, 1)}\nchoices = []\nfor name, (fp_cost, fn_cost) in cost_scenarios.items():\n    costs = metric_table['fp'] * fp_cost + metric_table['fn'] * fn_cost\n    best = metric_table.loc[costs.idxmin()]\n    choices.append({'scenario': name, 'fp_cost': fp_cost, 'fn_cost': fn_cost, 'threshold': float(best.threshold), 'total_cost': int(costs.min())})\nchoice_table = pd.DataFrame(choices)\nassert len(choice_table) == 3\n"),
            (
                "## ДЗ. Challenge. Рекомендация",
                """values = dict(zip(choice_table["scenario"], choice_table["threshold"]))
COST_NOTE = (
    f"balanced: порог {values['balanced']:.2f} при одинаковой цене FP и FN. "
    f"miss_expensive: порог {values['miss_expensive']:.2f}, потому что пропуск yes дороже и нужен больший recall. "
    f"call_expensive: порог {values['call_expensive']:.2f}, потому что лишний звонок дорог и важнее precision. "
    "Различие порогов показывает: оптимального порога вне операционного сценария нет; "
    "цены ошибок нужно согласовать до выбора модели."
)
assert len(COST_NOTE) >= 280
""",
            ),
        ],
    )
    add(base, lesson, homework, solutions)


def lesson04() -> None:
    base = LESSON_DIRS[3]
    setup = """import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("train_cli.py")
DATA_PATH = Path("bank_marketing_slim.csv")
assert SCRIPT.exists() and DATA_PATH.exists()
"""
    lesson = student_notebook(
        "Практика: воспроизводимый ML-запуск через CLI",
        setup,
        [
            ("## 1. Команда как список аргументов", """cmd = None  # TODO: sys.executable, script, --data, path, --threshold, 0.45
assert isinstance(cmd, list) and len(cmd) == 6
assert cmd[0] == sys.executable
assert "--data" in cmd and "--threshold" in cmd
"""),
            ("## 2. Запуск и диагностика", """proc = None  # TODO: subprocess.run(..., capture_output=True, text=True, check=False)
assert proc is not None and proc.returncode == 0, getattr(proc, "stderr", "")
assert proc.stdout.strip().startswith("{")
"""),
            ("## 3. JSON-контракт", """metrics = None  # TODO: json.loads
expected_keys = {"threshold", "duration_in_features", "accuracy", "precision", "recall", "f1"}
assert set(metrics) == expected_keys
assert metrics["duration_in_features"] is False
assert all(0 <= metrics[name] <= 1 for name in ("accuracy", "precision", "recall", "f1"))
"""),
            ("## 4. Функция запуска", """def run_experiment(threshold, seed=63):
    # TODO: вернуть parsed JSON; при ошибке поднять RuntimeError со stderr
    ...


trial = run_experiment(0.5)
assert trial["threshold"] == 0.5
assert trial["duration_in_features"] is False
"""),
            ("## 5. Серия порогов", """thresholds = [0.25, 0.35, 0.45, 0.55, 0.65]
runs = None  # TODO: список результатов
assert len(runs) == len(thresholds)
assert [row["threshold"] for row in runs] == thresholds
assert all(row["duration_in_features"] is False for row in runs)
"""),
            ("## 6. Таблица результатов", """import pandas as pd
run_table = None  # TODO
assert isinstance(run_table, pd.DataFrame) and len(run_table) == len(thresholds)
assert {"threshold", "precision", "recall", "f1"} <= set(run_table.columns)
assert run_table["recall"].is_monotonic_decreasing
"""),
            ("## 7. Acceptance gate", """checks = {
    "process_ok": None,
    "json_contract": None,
    "duration_forbidden": None,
    "metrics_in_range": None,
    "deterministic": None,
}  # TODO
assert set(checks.values()) == {True}
"""),
            ("## 8. Ошибочный запуск\n\nЗапустите CLI с несуществующим CSV и сохраните диагностическое сообщение.", """bad_cmd = [sys.executable, str(SCRIPT), "--data", "missing.csv", "--threshold", "0.5"]
bad_proc = None  # TODO
error_text = None  # TODO: stderr + stdout
assert bad_proc.returncode != 0
assert isinstance(error_text, str) and len(error_text) > 20
"""),
            (
                "## 9. Самостоятельно: отчёт запуска\n\n"
                "Подготовьте короткий отчёт для коллеги, который не видел ноутбук. "
                "Укажите точную роль параметра `threshold`, лучший F1 из выполненной "
                "серии, результат проверки `duration_in_features` и то, как система "
                "повела себя на намеренно неверном пути к данным. Отделите успешный "
                "результат модели от инженерного статуса процесса: корректные метрики "
                "не компенсируют ненулевой код завершения, а успешный процесс не "
                "компенсирует нарушение leakage-guard.",
                """CLI_REPORT = ""  # TODO: команда, лучший F1, leakage guard, ошибка; 240+ символов
assert len(CLI_REPORT) >= 240
assert "duration" in CLI_REPORT.lower()
assert "threshold" in CLI_REPORT.lower()
""",
            ),
        ],
    )
    homework = student_notebook(
        "ДЗ: CLI-эксперимент и проверка контракта",
        setup,
        [
            ("### Part A — обязательно\n\n## A1. Универсальный runner", """def run_experiment(threshold, seed):
    # TODO
    ...


result = run_experiment(0.4, 64)
assert result["threshold"] == 0.4 and result["duration_in_features"] is False
"""),
            ("## A2. Сетка threshold × seed", """import pandas as pd
rows = []  # TODO: 3 порога × 3 seed
grid = pd.DataFrame(rows)
assert len(grid) == 9
assert set(grid["threshold"]) == {0.3, 0.5, 0.7}
assert set(grid["seed"]) == {11, 22, 33}
assert not grid["duration_in_features"].any()
"""),
            ("## A3. Разброс F1", """stability = None  # TODO: groupby threshold, min/max/mean F1
assert isinstance(stability, pd.DataFrame) and len(stability) == 3
assert {"f1_min", "f1_max", "f1_mean"} <= set(stability.columns)
assert (stability["f1_max"] >= stability["f1_min"]).all()
"""),
            ("### Challenge\n\n## B1. Машиночитаемый gate", """def acceptance(result):
    # TODO: bool по ключам, диапазонам и duration
    ...


assert all(acceptance(row) for row in rows)
assert acceptance({"duration_in_features": True}) is False
"""),
            ("## B2. Инженерная записка", """ENGINEERING_NOTE = ""  # TODO: CLI, seed, contract, stderr; 280+ символов
assert len(ENGINEERING_NOTE) >= 280
assert all(word in ENGINEERING_NOTE.lower() for word in ["cli", "seed", "duration", "stderr"])
"""),
        ],
    )
    runner = """def run_experiment(threshold, seed=63):
    command = [
        sys.executable, str(SCRIPT), "--data", str(DATA_PATH),
        "--threshold", str(threshold), "--seed", str(seed),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr or completed.stdout)
    return json.loads(completed.stdout)
"""
    solutions = solution_notebook(
        "CLI и контракт эксперимента",
        setup,
        [
            ("## Урок. 1. Команда", "cmd = [sys.executable, str(SCRIPT), '--data', str(DATA_PATH), '--threshold', '0.45']\nassert len(cmd) == 6\n"),
            ("## Урок. 2–3. Процесс и JSON", "proc = subprocess.run(cmd, capture_output=True, text=True, check=False)\nassert proc.returncode == 0, proc.stderr\nmetrics = json.loads(proc.stdout)\nexpected_keys = {'threshold', 'duration_in_features', 'accuracy', 'precision', 'recall', 'f1'}\nassert set(metrics) == expected_keys and metrics['duration_in_features'] is False\n"),
            ("## Урок. 4. Runner", runner + "trial = run_experiment(0.5)\nassert trial['threshold'] == 0.5\n"),
            ("## Урок. 5–6. Серия запусков", "import pandas as pd\nthresholds = [0.25, 0.35, 0.45, 0.55, 0.65]\nruns = [run_experiment(t) for t in thresholds]\nrun_table = pd.DataFrame(runs)\nassert run_table['recall'].is_monotonic_decreasing\n"),
            ("## Урок. 7. Acceptance gate", "repeat = run_experiment(0.45)\nchecks = {'process_ok': proc.returncode == 0, 'json_contract': set(metrics) == expected_keys, 'duration_forbidden': metrics['duration_in_features'] is False, 'metrics_in_range': all(0 <= metrics[n] <= 1 for n in ('accuracy', 'precision', 'recall', 'f1')), 'deterministic': repeat == metrics}\nassert set(checks.values()) == {True}\n"),
            ("## Урок. 8. Диагностика ошибки", "bad_cmd = [sys.executable, str(SCRIPT), '--data', 'missing.csv', '--threshold', '0.5']\nbad_proc = subprocess.run(bad_cmd, capture_output=True, text=True, check=False)\nerror_text = bad_proc.stderr + bad_proc.stdout\nassert bad_proc.returncode != 0 and len(error_text) > 20\n"),
            ("## Урок. 9. Отчёт", 'best = run_table.loc[run_table["f1"].idxmax()]\nCLI_REPORT = (f"Команда CLI принимает --data, --threshold и --seed; все пять запусков вернули JSON. "\nf"Лучший F1={best.f1:.3f} при threshold={best.threshold:.2f}. Поле duration_in_features во всех результатах false, "\n"поэтому guard против duration сработал. Ошибочный путь завершился ненулевым кодом и дал stderr, пригодный для диагностики. Повтор с тем же seed детерминирован.")\nassert len(CLI_REPORT) >= 240\n'),
            ("## ДЗ. A1. Универсальный runner", "result = run_experiment(0.4, 64)\nassert result['threshold'] == 0.4\n"),
            ("## ДЗ. A2. Сетка запусков", "rows = []\nfor threshold in (0.3, 0.5, 0.7):\n    for seed in (11, 22, 33):\n        row = run_experiment(threshold, seed)\n        row['seed'] = seed\n        rows.append(row)\ngrid = pd.DataFrame(rows)\nassert len(grid) == 9 and not grid['duration_in_features'].any()\n"),
            ("## ДЗ. A3. Устойчивость", "stability = grid.groupby('threshold').agg(f1_min=('f1', 'min'), f1_max=('f1', 'max'), f1_mean=('f1', 'mean'))\nassert len(stability) == 3\n"),
            ("## ДЗ. Challenge. Gate", "def acceptance(result):\n    required = {'threshold', 'duration_in_features', 'accuracy', 'precision', 'recall', 'f1'}\n    return required <= set(result) and result['duration_in_features'] is False and all(0 <= result[n] <= 1 for n in ('accuracy', 'precision', 'recall', 'f1'))\n\nassert all(acceptance(row) for row in rows) and not acceptance({'duration_in_features': True})\n"),
            ("## ДЗ. Challenge. Инженерная записка", 'ENGINEERING_NOTE = ("CLI отделяет параметры запуска от кода и позволяет повторить эксперимент одной командой. seed фиксирует split, "\n"но сетка seed показывает устойчивость метрик. JSON-контракт проверяется автоматически; duration обязан оставаться false. "\n"Ненулевой return code нельзя игнорировать: stderr сохраняет причину ошибки пути или аргумента. Такой runner можно включить в следующий gate, не копируя notebook-состояние и не читая вывод вручную.")\nassert len(ENGINEERING_NOTE) >= 280\n'),
        ],
    )
    add(base, lesson, homework, solutions)


def lesson05() -> None:
    base = LESSON_DIRS[4]
    setup = """import json
import subprocess
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

DATA_PATH = Path("bank_marketing_slim.csv")
CLI_SCRIPT = Path("../04_practice_metrics_cli/train_cli.py")
assert DATA_PATH.exists() and CLI_SCRIPT.exists()
"""
    lesson = student_notebook(
        "venv, requirements и README воспроизводимого эксперимента",
        setup,
        [
            ("## 1. Команды создания среды", """venv_commands = None  # TODO: создание, активация Windows, обновление pip, install
assert isinstance(venv_commands, list) and len(venv_commands) >= 4
assert venv_commands[0] == "python -m venv .venv"
assert any(".venv\\\\Scripts\\\\activate" in command for command in venv_commands)
assert any("-r requirements.txt" in command for command in venv_commands)
"""),
            ("## 2. Минимальные зависимости", """required_packages = None  # TODO
assert required_packages == ["numpy", "pandas", "scikit-learn"]
assert len(required_packages) == len(set(required_packages))
"""),
            ("## 3. Версии среды", """def package_line(distribution_name):
    # TODO: name==installed version; понятная ошибка, если пакета нет
    ...


requirements_lines = None  # TODO
assert len(requirements_lines) == 3
assert all("==" in line for line in requirements_lines)
assert requirements_lines[2].startswith("scikit-learn==")
"""),
            ("## 4. Текст requirements.txt", """requirements_text = None  # TODO: строки + завершающий перевод строки
assert requirements_text.endswith("\\n")
assert requirements_text.count("\\n") == 3
assert all(name in requirements_text for name in required_packages)
"""),
            ("## 5. Фактический запуск CLI", """cmd = [sys.executable, str(CLI_SCRIPT), "--data", str(DATA_PATH), "--threshold", "0.45"]
proc = None  # TODO
metrics = None  # TODO
assert proc.returncode == 0, proc.stderr
assert metrics["duration_in_features"] is False
assert metrics["threshold"] == 0.45
"""),
            ("## 6. Структура README", """readme_sections = None  # TODO: Цель, Данные, Leakage, Установка, Запуск, Результаты, Ограничения
assert isinstance(readme_sections, list) and len(readme_sections) == 7
assert "Leakage" in readme_sections and "Ограничения" in readme_sections
"""),
            ("## 7. README эксперимента", """experiment_readme = ""  # TODO: markdown по разделам и фактическим metrics
assert len(experiment_readme) >= 700
assert "duration" in experiment_readme.lower()
assert "threshold" in experiment_readme.lower()
assert "python -m venv .venv" in experiment_readme
assert f"{metrics['f1']:.3f}" in experiment_readme
"""),
            ("## 8. Gate структуры сдачи", """submission_files = {"train_cli.py", "requirements.txt", "README.md", "metrics.json"}
required_files = None  # TODO: обязательные без metrics.json
missing = None         # TODO
assert required_files == {"train_cli.py", "requirements.txt", "README.md"}
assert missing == set()
"""),
            (
                "## 9. Самостоятельно: передача коллеге\n\n"
                "Напишите инструкцию для запуска на чистой машине: среда, зависимости, "
                "команда, проверка leakage и границы интерпретации slim-среза.",
                """HANDOFF_NOTE = ""  # TODO: 260+ символов, clean machine, команда, guard, ограничение
assert len(HANDOFF_NOTE) >= 260
assert all(word in HANDOFF_NOTE.lower() for word in ["venv", "requirements", "duration", "огранич"])
""",
            ),
        ],
    )
    homework = student_notebook(
        "ДЗ: финальная приёмка артефакта модуля",
        setup,
        [
            ("### Part A — обязательно\n\n## A1. Дерево сдачи", """tree_text = ""  # TODO
assert len(tree_text) >= 120
assert all(name in tree_text for name in ["train_cli.py", "requirements.txt", "README.md"])
"""),
            ("## A2. Чек-лист README", """readme_checks = {
    "goal": None, "data": None, "leakage": None, "install": None,
    "run": None, "metrics": None, "limitations": None,
}  # TODO
assert set(readme_checks.values()) == {True}
"""),
            ("## A3. Команда чистого воспроизведения", """reproduction_commands = None  # TODO
assert isinstance(reproduction_commands, list) and len(reproduction_commands) >= 5
assert reproduction_commands[0] == "python -m venv .venv"
assert any("train_cli.py" in command and "--threshold" in command for command in reproduction_commands)
"""),
            ("### Challenge\n\n## B1. Проверка README как контракта", """def audit_readme(text):
    # TODO: вернуть dict из 7 bool-проверок
    ...


audit = audit_readme(experiment_readme if "experiment_readme" in globals() else "")
assert set(audit) == {"goal", "data", "leakage", "install", "run", "metrics", "limitations"}
assert all(isinstance(value, bool) for value in audit.values())
"""),
            ("## B2. Postmortem воспроизводимости", """POSTMORTEM = ""  # TODO: 320+ символов, версии, seed, путь, leakage, slim
assert len(POSTMORTEM) >= 320
assert all(word in POSTMORTEM.lower() for word in ["верс", "seed", "duration", "slim"])
"""),
        ],
    )
    package_fn = """def package_line(distribution_name):
    try:
        return f"{distribution_name}=={version(distribution_name)}"
    except PackageNotFoundError as exc:
        raise RuntimeError(f"Пакет {distribution_name} не установлен") from exc
"""
    solutions = solution_notebook(
        "venv, requirements и README",
        setup,
        [
            ("## Урок. 1. Команды среды", "venv_commands = ['python -m venv .venv', '.venv\\\\Scripts\\\\activate', 'python -m pip install --upgrade pip', 'python -m pip install -r requirements.txt']\nassert len(venv_commands) == 4\n"),
            ("## Урок. 2–4. Зависимости", "required_packages = ['numpy', 'pandas', 'scikit-learn']\n" + package_fn + "\nrequirements_lines = [package_line(name) for name in required_packages]\nrequirements_text = '\\n'.join(requirements_lines) + '\\n'\nassert requirements_text.count('\\n') == 3\n"),
            ("## Урок. 5. Фактические метрики", "cmd = [sys.executable, str(CLI_SCRIPT), '--data', str(DATA_PATH), '--threshold', '0.45']\nproc = subprocess.run(cmd, capture_output=True, text=True, check=False)\nassert proc.returncode == 0, proc.stderr\nmetrics = json.loads(proc.stdout)\nassert metrics['duration_in_features'] is False\n"),
            ("## Урок. 6. Каркас README", "readme_sections = ['Цель', 'Данные', 'Leakage', 'Установка', 'Запуск', 'Результаты', 'Ограничения']\nassert len(readme_sections) == 7\n"),
            ("## Урок. 7. README", """experiment_readme = f'''# Эксперимент: отклик на депозит

## Цель
Ранжировать клиентов банковской кампании по вероятности отклика `y=yes` и применить порог решения.

## Данные
Использован учебный `bank_marketing_slim.csv`, подготовленный из UCI Bank Marketing.

## Leakage
`duration` известна только после звонка и запрещена как признак. Скрипт проверяет `assert "duration" not in FEATURE_COLUMNS`, а JSON возвращает `duration_in_features=false`.

## Установка
```text
python -m venv .venv
.venv\\\\Scripts\\\\activate
python -m pip install -r requirements.txt
```

## Запуск
```text
python train_cli.py --data bank_marketing_slim.csv --threshold 0.45 --seed 63
```

## Результаты
- threshold: {metrics["threshold"]:.2f}
- accuracy: {metrics["accuracy"]:.3f}
- precision: {metrics["precision"]:.3f}
- recall: {metrics["recall"]:.3f}
- f1: {metrics["f1"]:.3f}

## Ограничения
Это учебный slim-срез, а не свежая выборка банка. Метрики относятся к одному стратифицированному split. Порог нужно пересчитать под реальный бюджет, период данных и цену ошибок.
'''
assert len(experiment_readme) >= 700 and f"{metrics['f1']:.3f}" in experiment_readme
"""),
            ("## Урок. 8. Gate сдачи", "submission_files = {'train_cli.py', 'requirements.txt', 'README.md', 'metrics.json'}\nrequired_files = {'train_cli.py', 'requirements.txt', 'README.md'}\nmissing = required_files - submission_files\nassert missing == set()\n"),
            ("## Урок. 9. Передача", 'HANDOFF_NOTE = ("На чистой машине создать venv, активировать его и установить requirements.txt, затем запустить указанную CLI-команду. "\n"Сверить JSON-ключи и убедиться, что duration_in_features=false: duration недоступна до звонка. "\n"Полученные метрики должны совпасть при том же seed и версиях. Ограничение: slim-срез учебный, поэтому результат не является оценкой будущей банковской кампании.")\nassert len(HANDOFF_NOTE) >= 260\n'),
            ("## ДЗ. A1. Дерево", "tree_text = 'submission/\\n  train_cli.py  # CLI модели\\n  requirements.txt  # версии зависимостей\\n  README.md  # инструкция и результаты\\n  metrics.json  # сохранённый вывод, опционально\\n'\nassert len(tree_text) >= 120\n"),
            ("## ДЗ. A2. Чек-лист", "readme_checks = {'goal': '## Цель' in experiment_readme, 'data': '## Данные' in experiment_readme, 'leakage': 'duration' in experiment_readme, 'install': 'python -m venv .venv' in experiment_readme, 'run': 'train_cli.py' in experiment_readme, 'metrics': 'f1:' in experiment_readme, 'limitations': '## Ограничения' in experiment_readme}\nassert set(readme_checks.values()) == {True}\n"),
            ("## ДЗ. A3. Воспроизведение", "reproduction_commands = ['python -m venv .venv', '.venv\\\\Scripts\\\\activate', 'python -m pip install --upgrade pip', 'python -m pip install -r requirements.txt', 'python train_cli.py --data bank_marketing_slim.csv --threshold 0.45 --seed 63']\nassert len(reproduction_commands) == 5\n"),
            ("## ДЗ. Challenge. Аудит README", "def audit_readme(text):\n    return {'goal': '## Цель' in text, 'data': '## Данные' in text, 'leakage': 'duration' in text.lower(), 'install': 'python -m venv .venv' in text, 'run': 'train_cli.py' in text, 'metrics': all(name in text for name in ('precision', 'recall', 'f1')), 'limitations': '## Ограничения' in text}\n\naudit = audit_readme(experiment_readme)\nassert set(audit.values()) == {True}\n"),
            ("## ДЗ. Challenge. Postmortem", 'POSTMORTEM = ("Воспроизводимость ломается, если не зафиксированы версии библиотек: solver или кодировка могут измениться. "\n"Другой seed меняет train/test и метрики; неверный относительный путь мешает найти CSV. Самый опасный тихий сбой — добавить duration и получить завышенное качество с недоступным признаком. "\n"Даже при исправном запуске slim-срез не представляет будущую кампанию: нужны свежие данные, мониторинг доли yes и повторный выбор порога. Поэтому README фиксирует среду, команду, seed, leakage-guard и границы вывода.")\nassert len(POSTMORTEM) >= 320\n'),
        ],
    )
    add(base, lesson, homework, solutions)


def main() -> None:
    if not DATA_CSV.exists():
        raise SystemExit(f"Missing {DATA_CSV}")
    for lesson_dir in LESSON_DIRS:
        destination = ROOT / lesson_dir / DATA_CSV.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(DATA_CSV, destination)
        print(f"copied {DATA_CSV.name} -> {lesson_dir}")
    for builder in (lesson01, lesson02, lesson03, lesson04, lesson05):
        builder()
    print("done: 15 notebooks and 5 CSV copies")


if __name__ == "__main__":
    main()
