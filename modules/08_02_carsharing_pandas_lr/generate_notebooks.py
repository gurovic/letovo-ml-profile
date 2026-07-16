#!/usr/bin/env python3
"""Generate lesson notebooks for module 08_02 (KTP pairs 11–20).

Source of truth for .ipynb: edit this file, then run it.
Pattern (как в модуле 1): stubs + asserts в lesson/homework; полный solutions.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent

LOAD_DATA = (
    "from pathlib import Path\n"
    "import pandas as pd\n\n\n"
    "def find_trips_csv() -> Path:\n"
    "    for p in (Path('trips.csv'), Path('../../data/trips.csv'), Path('../data/trips.csv')):\n"
    "        if p.exists():\n"
    "            return p.resolve()\n"
    "    raise FileNotFoundError('trips.csv не найден')\n\n\n"
    "TRIPS_PATH = find_trips_csv()\n"
    "df = pd.read_csv(TRIPS_PATH)\n"
)

IMPORTS_MPL = "import matplotlib.pyplot as plt\n"
IMPORTS_SKLEARN = (
    "from sklearn.model_selection import train_test_split\n"
    "from sklearn.linear_model import LinearRegression\n"
    "from sklearn.metrics import mean_squared_error, r2_score\n"
)

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
    base = "lessons/01_pandas_dataframe"
    lesson = nb(
        md("# pandas: таблица поездок каршеринга"),
        code(LOAD_DATA),
        md(
            "## 1. Первая таблица\n\n"
            "Выведите число строк и столбцов, первые 5 строк и список имён столбцов."
        ),
        code(
            "# ваш код: shape, head, columns\n"
            "n_rows, n_cols = None, None  # замените\n"
            "assert n_rows == len(df)\n"
            "assert n_cols == df.shape[1]"
        ),
        md(
            "## 2. Признак, цель, служебный столбец\n\n"
            "Заполните переменные. Цель — длительность поездки; id — не признак для модели."
        ),
        code(
            "TARGET = ''  # имя столбца-цели\n"
            "FEATURES = []  # список имён признаков\n"
            "ID_COL = ''  # служебный столбец\n\n"
            "assert TARGET in df.columns\n"
            "assert TARGET not in FEATURES\n"
            "assert ID_COL in df.columns\n"
            "assert ID_COL not in FEATURES\n"
            "assert 'distance_km' in FEATURES\n"
            "assert set(FEATURES).issubset(df.columns)\n"
            "assert df[TARGET].dtype.kind in 'iuf'"
        ),
        md(
            "## 3. Тип object\n\n"
            "Соберите список столбцов с `dtype == object`. "
            "Почему `distance_km` не входит в этот список?"
        ),
        code(
            "object_cols = []  # заполните\n"
            "print('object:', object_cols)\n"
            "print('distance_km dtype:', df['distance_km'].dtype)\n"
            "assert 'trip_id' in object_cols\n"
            "assert 'zone' in object_cols\n"
            "assert 'distance_km' not in object_cols"
        ),
        md(
            "## 4. Расширение\n\n"
            "Сколько уникальных значений в `zone`? Запишите ответ числом."
        ),
        code(
            "n_zones = None  # ваш код\n"
            "assert n_zones == df['zone'].nunique()\n"
            "print(n_zones)"
        ),
    )
    hw = nb(
        md("# ДЗ: осмотр таблицы"),
        code(LOAD_DATA),
        md("### A. Закрепление"),
        md("## 1. Срез столбцов\n\nПервые 10 строк только `distance_km`, `duration_min`, `hour`."),
        code(
            "subset = None  # DataFrame 10×3\n"
            "assert subset is not None\n"
            "assert list(subset.columns) == ['distance_km', 'duration_min', 'hour']\n"
            "assert len(subset) == 10\n"
            "print(subset)"
        ),
        md("## 2. Одна поездка\n\nДлительность поездки с `trip_id == 'T0001'`."),
        code(
            "duration_t0001 = None  # число\n"
            "assert duration_t0001 == df.loc[df['trip_id'] == 'T0001', 'duration_min'].iloc[0]\n"
            "print(duration_t0001)"
        ),
        md("## 3. Два способа длины\n\nПроверьте, что `len(df)` и `df.shape[0]` совпадают."),
        code(
            "a = len(df)\n"
            "b = df.shape[0]\n"
            "assert a == b\n"
            "print(a)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 4. Средняя comfort\n\n"
            "Средняя `duration_min` только для `vehicle_type == 'comfort'` "
            "(округлите до 1 знака). Сравните со средним по всей таблице — одной фразой."
        ),
        code(
            "mean_comfort = None  # float\n"
            "mean_all = round(df['duration_min'].mean(), 1)\n"
            "COMPARE_NOTE = ''  # одна фраза\n"
            "assert mean_comfort is not None\n"
            "assert abs(mean_comfort - round(df.loc[df['vehicle_type'] == 'comfort', 'duration_min'].mean(), 1)) < 1e-9\n"
            "assert len(COMPARE_NOTE) > 10\n"
            "print(mean_comfort, mean_all, COMPARE_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: pandas DataFrame\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        md("## Урок. 1. Первая таблица"),
        code(
            "n_rows, n_cols = df.shape\n"
            "print(n_rows, n_cols)\n"
            "print(df.head())\n"
            "print(list(df.columns))\n"
            "assert n_rows == len(df)\n"
            "assert n_cols == df.shape[1]"
        ),
        md("## Урок. 2. Признак / цель / id"),
        code(
            "TARGET = 'duration_min'\n"
            "FEATURES = ['distance_km', 'hour', 'zone', 'vehicle_type']\n"
            "ID_COL = 'trip_id'\n"
            "assert TARGET in df.columns\n"
            "assert TARGET not in FEATURES\n"
            "assert ID_COL not in FEATURES"
        ),
        md("## Урок. 3. object"),
        code(
            "object_cols = df.select_dtypes(include='object').columns.tolist()\n"
            "print('object:', object_cols)\n"
            "assert 'trip_id' in object_cols\n"
            "assert 'zone' in object_cols\n"
            "assert 'distance_km' not in object_cols"
        ),
        md("## Урок. 4. Зоны"),
        code(
            "n_zones = df['zone'].nunique()\n"
            "assert n_zones == df['zone'].nunique()\n"
            "print(n_zones)"
        ),
        md("## ДЗ. 1. Срез столбцов"),
        code(
            "subset = df[['distance_km', 'duration_min', 'hour']].head(10)\n"
            "assert list(subset.columns) == ['distance_km', 'duration_min', 'hour']\n"
            "assert len(subset) == 10\n"
            "print(subset)"
        ),
        md("## ДЗ. 2. Одна поездка"),
        code(
            "duration_t0001 = df.loc[df['trip_id'] == 'T0001', 'duration_min'].iloc[0]\n"
            "print(duration_t0001)"
        ),
        md("## ДЗ. 3. Два способа длины"),
        code(
            "a = len(df)\n"
            "b = df.shape[0]\n"
            "assert a == b\n"
            "print(a)"
        ),
        md("## ДЗ. 4. Средняя comfort"),
        code(
            "mean_comfort = round(df.loc[df['vehicle_type'] == 'comfort', 'duration_min'].mean(), 1)\n"
            "mean_all = round(df['duration_min'].mean(), 1)\n"
            "COMPARE_NOTE = f'comfort: {mean_comfort}, все: {mean_all} — сравните порядок величин'\n"
            "print(mean_comfort, mean_all, COMPARE_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson02() -> None:
    base = "lessons/02_practice_filters"
    lesson = nb(
        md("# Практика: фильтры и типы"),
        code(LOAD_DATA),
        md("## 1. Фильтр по зоне\n\nТолько `zone == 'center'`. Сколько таких строк?"),
        code(
            "center = None  # DataFrame\n"
            "assert center is not None\n"
            "assert (center['zone'] == 'center').all()\n"
            "assert len(center) > 0\n"
            "print(len(center))"
        ),
        md("## 2. Длинные поездки\n\n`distance_km >= 15`. Выведите `trip_id`, расстояние, длительность (head)."),
        code(
            "long_trips = None\n"
            "assert long_trips is not None\n"
            "assert (long_trips['distance_km'] >= 15).all()\n"
            "print(long_trips[['trip_id', 'distance_km', 'duration_min']].head())"
        ),
        md(
            "## 3. loc vs iloc\n\n"
            "Первые 3 строки столбцов `distance_km` и `duration_min` "
            "через `.loc` и через `.iloc`. Значения должны совпасть."
        ),
        code(
            "by_name = None  # .loc\n"
            "by_pos = None  # .iloc\n"
            "assert by_name is not None and by_pos is not None\n"
            "assert by_name.shape == (3, 2)\n"
            "assert by_pos.shape == (3, 2)\n"
            "assert (by_name.values == by_pos.values).all()\n"
            "print(by_name)\nprint(by_pos)"
        ),
        md("## 4. Тип hour\n\nПриведите `hour` к `int`, проверьте диапазон 0–23."),
        code(
            "hours = None  # Series int\n"
            "assert hours is not None\n"
            "assert hours.dtype.kind in 'iu'\n"
            "assert hours.min() >= 0 and hours.max() <= 23\n"
            "print(int(hours.min()), int(hours.max()))"
        ),
    )
    hw = nb(
        md("# ДЗ: фильтры"),
        code(LOAD_DATA),
        md("### A. Закрепление"),
        md("## 1. Комфорт\n\nТолько `vehicle_type == 'comfort'` — число строк."),
        code(
            "n_comfort = None\n"
            "assert n_comfort == (df['vehicle_type'] == 'comfort').sum()\n"
            "print(n_comfort)"
        ),
        md("## 2. Утро\n\n`hour` от 7 до 9 включительно — число строк."),
        code(
            "n_morning = None\n"
            "assert n_morning == ((df['hour'] >= 7) & (df['hour'] <= 9)).sum()\n"
            "print(n_morning)"
        ),
        md("## 3. Топ-5\n\n5 самых длинных по `duration_min` (`trip_id`, `duration_min`)."),
        code(
            "top5 = None\n"
            "assert top5 is not None\n"
            "assert len(top5) == 5\n"
            "assert top5['duration_min'].is_monotonic_decreasing\n"
            "print(top5[['trip_id', 'duration_min']])"
        ),
        md(
            "### B. Вызов\n\n"
            "## 4. Доля center\n\n"
            "Доля поездок `zone == 'center'` среди всех (0–1, округлить до 3 знаков). "
            "Одной фразой: это много или мало для аналитика?"
        ),
        code(
            "share_center = None\n"
            "SHARE_NOTE = ''\n"
            "assert share_center == round((df['zone'] == 'center').mean(), 3)\n"
            "assert len(SHARE_NOTE) > 8\n"
            "print(share_center, SHARE_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: фильтры\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        md("## Урок. 1. Фильтр center"),
        code(
            "center = df[df['zone'] == 'center']\n"
            "assert (center['zone'] == 'center').all()\n"
            "print(len(center))"
        ),
        md("## Урок. 2. Длинные поездки"),
        code(
            "long_trips = df[df['distance_km'] >= 15]\n"
            "assert (long_trips['distance_km'] >= 15).all()\n"
            "print(long_trips[['trip_id', 'distance_km', 'duration_min']].head())"
        ),
        md("## Урок. 3. loc vs iloc"),
        code(
            "by_name = df.loc[:2, ['distance_km', 'duration_min']]\n"
            "by_pos = df.iloc[:3][['distance_km', 'duration_min']]\n"
            "assert (by_name.values == by_pos.values).all()\n"
            "print(by_name)\nprint(by_pos)"
        ),
        md("## Урок. 4. Тип hour"),
        code(
            "hours = df['hour'].astype(int)\n"
            "assert hours.min() >= 0 and hours.max() <= 23\n"
            "print(int(hours.min()), int(hours.max()))"
        ),
        md("## ДЗ. 1. Комфорт"),
        code(
            "n_comfort = int((df['vehicle_type'] == 'comfort').sum())\n"
            "print(n_comfort)"
        ),
        md("## ДЗ. 2. Утро"),
        code(
            "n_morning = int(((df['hour'] >= 7) & (df['hour'] <= 9)).sum())\n"
            "print(n_morning)"
        ),
        md("## ДЗ. 3. Топ-5"),
        code(
            "top5 = df.sort_values('duration_min', ascending=False).head(5)\n"
            "print(top5[['trip_id', 'duration_min']])"
        ),
        md("## ДЗ. 4. Доля center"),
        code(
            "share_center = round((df['zone'] == 'center').mean(), 3)\n"
            "SHARE_NOTE = f'center ≈ {share_center:.0%} поездок — ориентир доли центра'\n"
            "print(share_center, SHARE_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson03() -> None:
    base = "lessons/03_eda_scatter"
    lesson = nb(
        md("# EDA: describe и scatter"),
        code(LOAD_DATA + IMPORTS_MPL),
        md(
            "## 1. describe\n\n"
            "Описательная статистика для `distance_km` и `duration_min`. "
            "Запишите mean длительности в `mean_duration`."
        ),
        code(
            "# вызовите describe и заполните\n"
            "mean_duration = None\n"
            "assert mean_duration is not None\n"
            "assert abs(mean_duration - df['duration_min'].mean()) < 1e-9\n"
            "print(mean_duration)"
        ),
        md("## 2. info\n\nВызовите `df.info()`. Сколько ненулевых значений в `duration_min`?"),
        code(
            "# df.info()\n"
            "n_non_null_duration = None\n"
            "assert n_non_null_duration == df['duration_min'].notna().sum()\n"
            "print(n_non_null_duration)"
        ),
        md(
            "## 3. Scatter\n\n"
            "Scatter: X = `distance_km`, Y = `duration_min`. Подписи осей и заголовок обязательны."
        ),
        code(
            "# постройте график\n"
            "plt.figure(figsize=(6, 4))\n"
            "# ...\n"
            "plt.show()\n"
            "SCATTER_DONE = False  # True после построения\n"
            "assert SCATTER_DONE"
        ),
        md(
            "## 4. Вывод\n\n"
            "Одно предложение: есть ли положительная связь расстояние → длительность? "
            "Есть ли разброс?"
        ),
        code(
            "EDA_CONCLUSION = ''\n"
            "assert len(EDA_CONCLUSION) > 20\n"
            "print(EDA_CONCLUSION)"
        ),
    )
    hw = nb(
        md("# ДЗ: EDA"),
        code(LOAD_DATA + IMPORTS_MPL),
        md("### A. Закрепление"),
        md("## 1. hour\n\n`describe()` для `hour`. Запишите медиану в `median_hour`."),
        code(
            "median_hour = None\n"
            "assert median_hour == df['hour'].median()\n"
            "print(median_hour)"
        ),
        md("## 2. Scatter hour\n\nScatter `hour` → `duration_min` с подписями."),
        code(
            "plt.figure(figsize=(6, 4))\n"
            "# ваш scatter\n"
            "plt.show()\n"
            "HOUR_SCATTER_DONE = False\n"
            "assert HOUR_SCATTER_DONE"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. Сравнение scatter\n\n"
            "Сравните визуально distance→duration и hour→duration. "
            "Какой признак выглядит перспективнее для линейной модели? Почему (2 предложения)?"
        ),
        code(
            "BETTER_FOR_LINEAR = ''  # 'distance_km' или 'hour'\n"
            "WHY_VISUAL = ''\n"
            "assert BETTER_FOR_LINEAR in ('distance_km', 'hour')\n"
            "assert len(WHY_VISUAL) > 30\n"
            "print(BETTER_FOR_LINEAR, WHY_VISUAL)"
        ),
    )
    sol = nb(
        md("# Решения: EDA\n\n" + SOL_BANNER),
        code(LOAD_DATA + IMPORTS_MPL),
        md("## Урок. 1. describe"),
        code(
            "print(df[['distance_km', 'duration_min']].describe())\n"
            "mean_duration = df['duration_min'].mean()\n"
            "assert abs(mean_duration - df['duration_min'].mean()) < 1e-9\n"
            "print(mean_duration)"
        ),
        md("## Урок. 2. info"),
        code(
            "n_non_null_duration = int(df['duration_min'].notna().sum())\n"
            "print(n_non_null_duration)"
        ),
        md("## Урок. 3. Scatter distance"),
        code(
            "plt.figure(figsize=(6, 4))\n"
            "plt.scatter(df['distance_km'], df['duration_min'], alpha=0.5)\n"
            "plt.xlabel('distance_km')\n"
            "plt.ylabel('duration_min')\n"
            "plt.title('Длительность vs расстояние')\n"
            "plt.show()"
        ),
        md("## Урок. 4. Вывод EDA"),
        code(
            "EDA_CONCLUSION = (\n"
            "    'С ростом distance_km длительность в среднем растёт, но разброс заметный.'\n"
            ")\n"
            "print(EDA_CONCLUSION)"
        ),
        md("## ДЗ. 1. hour describe"),
        code(
            "median_hour = df['hour'].median()\n"
            "print(median_hour)"
        ),
        md("## ДЗ. 2. Scatter hour"),
        code(
            "plt.figure(figsize=(6, 4))\n"
            "plt.scatter(df['hour'], df['duration_min'], alpha=0.4)\n"
            "plt.xlabel('hour')\n"
            "plt.ylabel('duration_min')\n"
            "plt.title('Длительность vs час')\n"
            "plt.show()"
        ),
        md("## ДЗ. 3. Сравнение признаков"),
        code(
            "BETTER_FOR_LINEAR = 'distance_km'\n"
            "WHY_VISUAL = (\n"
            "    'На scatter с distance видна наклонная полоса; у hour облако более размытое. '\n"
            "    'Линейная модель на distance выглядит уместнее как первый кандидат.'\n"
            ")\n"
            "print(BETTER_FOR_LINEAR, WHY_VISUAL)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson04() -> None:
    base = "lessons/04_train_test_lr"
    lesson = nb(
        md("# train/test и LinearRegression"),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md(
            "## 1. Признак и цель\n\n"
            "Соберите `X` как DataFrame из одного столбца `distance_km` и `y` — Series `duration_min`. "
            "Важно: двойные скобки у X."
        ),
        code(
            "X = None\n"
            "y = None\n"
            "assert X is not None and y is not None\n"
            "assert list(X.columns) == ['distance_km']\n"
            "assert X.shape[1] == 1\n"
            "assert len(y) == len(X)\n"
            "print(X.shape, y.shape)"
        ),
        md("## 2. train/test split\n\n20% в test, `random_state=42`."),
        code(
            "X_train = X_test = y_train = y_test = None\n"
            "# train_test_split(...)\n"
            "assert X_test is not None\n"
            "assert len(X_test) == int(0.2 * len(df))\n"
            "assert len(X_train) + len(X_test) == len(df)\n"
            "print(len(X_train), len(X_test))"
        ),
        md(
            "## 3. fit / predict\n\n"
            "Обучите `LinearRegression` на train, предскажите test. "
            "Выведите `coef_` и `intercept_`."
        ),
        code(
            "model = None\n"
            "y_pred = None\n"
            "assert model is not None and y_pred is not None\n"
            "assert len(y_pred) == len(y_test)\n"
            "print('coef', model.coef_, 'intercept', model.intercept_)\n"
            "print('первые 3 pred:', y_pred[:3])"
        ),
        md(
            "## 4. Расширение\n\n"
            "Повторите split с тем же `test_size` и `random_state=0`. "
            "Совпадают ли первые 3 индекса `y_test` с предыдущим split? Запишите ответ bool."
        ),
        code(
            "same_first_indices = None  # True/False после эксперимента\n"
            "assert same_first_indices is False\n"
            "print(same_first_indices)"
        ),
    )
    hw = nb(
        md("# ДЗ: split и воспроизводимость"),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("### A. Закрепление"),
        md("## 1. Другой test_size\n\n`test_size=0.3`, `random_state=42`. Сколько строк в test?"),
        code(
            "X = df[['distance_km']]\n"
            "y = df['duration_min']\n"
            "n_test_03 = None\n"
            "assert n_test_03 == int(0.3 * len(df))\n"
            "print(n_test_03)"
        ),
        md(
            "## 2. Воспроизводимость\n\n"
            "Дважды сделайте split 0.2 / seed 42. Совпадают ли `y_test.values` целиком?"
        ),
        code(
            "reproducible = None  # True/False\n"
            "assert reproducible is True\n"
            "print(reproducible)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. Модель на hour\n\n"
            "Обучите модель на `hour` (тот же split 0.2 / 42). "
            "Выведите `coef_`. Одной фразой: знак коэффициента ожидаем?"
        ),
        code(
            "coef_hour = None  # число или массив coef_\n"
            "COEF_NOTE = ''\n"
            "assert coef_hour is not None\n"
            "assert len(COEF_NOTE) > 10\n"
            "print(coef_hour, COEF_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: train/test и LR\n\n" + SOL_BANNER),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("## Урок. 1. X и y"),
        code(
            "X = df[['distance_km']]\n"
            "y = df['duration_min']\n"
            "assert list(X.columns) == ['distance_km']\n"
            "print(X.shape, y.shape)"
        ),
        md("## Урок. 2. train/test split"),
        code(
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X, y, test_size=0.2, random_state=42\n"
            ")\n"
            "assert len(X_test) == int(0.2 * len(df))\n"
            "print(len(X_train), len(X_test))"
        ),
        md("## Урок. 3. fit / predict"),
        code(
            "model = LinearRegression().fit(X_train, y_train)\n"
            "y_pred = model.predict(X_test)\n"
            "print('coef', model.coef_, 'intercept', model.intercept_)\n"
            "print('первые 3 pred:', y_pred[:3])"
        ),
        md("## Урок. 4. Другой seed"),
        code(
            "_, _, _, y_test_other = train_test_split(X, y, test_size=0.2, random_state=0)\n"
            "same_first_indices = bool((y_test.index[:3] == y_test_other.index[:3]).all())\n"
            "assert same_first_indices is False\n"
            "print(same_first_indices)"
        ),
        md("## ДЗ. 1. test_size=0.3"),
        code(
            "X = df[['distance_km']]\n"
            "y = df['duration_min']\n"
            "_, X_te, _, y_te = train_test_split(X, y, test_size=0.3, random_state=42)\n"
            "n_test_03 = len(X_te)\n"
            "print(n_test_03)"
        ),
        md("## ДЗ. 2. Воспроизводимость"),
        code(
            "a = train_test_split(X, y, test_size=0.2, random_state=42)[3].values\n"
            "b = train_test_split(X, y, test_size=0.2, random_state=42)[3].values\n"
            "reproducible = bool((a == b).all())\n"
            "print(reproducible)"
        ),
        md("## ДЗ. 3. coef hour"),
        code(
            "Xh = df[['hour']]\n"
            "Xtr, Xte, ytr, yte = train_test_split(Xh, y, test_size=0.2, random_state=42)\n"
            "coef_hour = LinearRegression().fit(Xtr, ytr).coef_\n"
            "COEF_NOTE = 'Знак coef зависит от данных; на паре важнее зафиксировать seed и размер test'\n"
            "print(coef_hour, COEF_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson05() -> None:
    base = "lessons/05_practice_metrics"
    starter = LOAD_DATA + IMPORTS_SKLEARN
    lesson = nb(
        md("# Практика: MSE и R²"),
        code(starter),
        md(
            "## 1. Split и модель\n\n"
            "X = `distance_km`, y = `duration_min`. Split 0.2 / seed 42, "
            "обучите `LinearRegression`, получите `y_pred` на test."
        ),
        code(
            "X = None\n"
            "y = None\n"
            "X_train = X_test = y_train = y_test = None\n"
            "model = None\n"
            "y_pred = None\n"
            "assert X is not None and y is not None\n"
            "assert list(X.columns) == ['distance_km']\n"
            "assert X_test is not None\n"
            "assert len(X_test) == int(0.2 * len(df))\n"
            "assert model is not None and y_pred is not None\n"
            "assert len(y_pred) == len(y_test)\n"
            "print(len(X_train), len(X_test))"
        ),
        md(
            "## 2. MSE\n\n"
            "Посчитайте среднеквадратичную ошибку на **test** "
            "(`mean_squared_error` или вручную)."
        ),
        code(
            "mse = None\n"
            "assert mse is not None\n"
            "assert abs(mse - mean_squared_error(y_test, y_pred)) < 1e-9\n"
            "assert mse >= 0\n"
            "print('MSE', round(mse, 2))"
        ),
        md("## 3. R²\n\nКоэффициент детерминации на test."),
        code(
            "r2 = None\n"
            "assert r2 is not None\n"
            "assert abs(r2 - r2_score(y_test, y_pred)) < 1e-9\n"
            "print('R2', round(r2, 3))"
        ),
        md(
            "## 4. Таблица сравнения\n\n"
            "DataFrame: столбцы `fact`, `pred`, `error` (= fact − pred). Покажите `head()`."
        ),
        code(
            "compare = None\n"
            "assert compare is not None\n"
            "assert list(compare.columns) == ['fact', 'pred', 'error']\n"
            "assert abs(compare['error'].iloc[0] - (compare['fact'].iloc[0] - compare['pred'].iloc[0])) < 1e-9\n"
            "print(compare.head())"
        ),
        md(
            "## 5. Интерпретация\n\n"
            "Одна фраза про R²: какую долю разброса длительности модель объясняет на test?"
        ),
        code(
            "METRIC_NOTE = ''\n"
            "assert len(METRIC_NOTE) > 15\n"
            "print(METRIC_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: метрики"),
        code(starter),
        md("### A. Закрепление"),
        md(
            "## 1. MAE\n\n"
            "Повторите split/fit (0.2 / 42) на `distance_km`. "
            "Средняя абсолютная ошибка на test (как MAE из модуля 1)."
        ),
        code(
            "X = df[['distance_km']]\n"
            "y = df['duration_min']\n"
            "X_train, X_test, y_train, y_test = None, None, None, None\n"
            "model = None\n"
            "y_pred = None\n"
            "mae = None\n"
            "assert X_train is not None and model is not None and y_pred is not None\n"
            "assert mae is not None\n"
            "assert abs(mae - abs(y_test - y_pred).mean()) < 1e-9\n"
            "print(round(mae, 2))"
        ),
        md(
            "## 2. Метрики на train\n\n"
            "Посчитайте MSE на **train** и на **test**. "
            "Больше или меньше на train? Одной фразой — почему смотрим на test."
        ),
        code(
            "mse_train = None\n"
            "mse_test = None\n"
            "TRAIN_VS_TEST = ''\n"
            "assert mse_train is not None and mse_test is not None\n"
            "assert abs(mse_train - mean_squared_error(y_train, model.predict(X_train))) < 1e-9\n"
            "assert abs(mse_test - mean_squared_error(y_test, y_pred)) < 1e-9\n"
            "assert len(TRAIN_VS_TEST) > 20\n"
            "print(mse_train, mse_test, TRAIN_VS_TEST)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. Baseline R²\n\n"
            "Если предсказывать везде среднее `y_train`, какой будет R² на test? "
            "(ожидание: около 0). Проверьте численно."
        ),
        code(
            "import numpy as np\n"
            "baseline_pred = np.full_like(y_test, y_train.mean(), dtype=float)\n"
            "r2_baseline = None\n"
            "assert r2_baseline is not None\n"
            "assert abs(r2_baseline - r2_score(y_test, baseline_pred)) < 1e-9\n"
            "assert abs(r2_baseline) < 0.05\n"
            "print(round(r2_baseline, 4))"
        ),
    )
    sol = nb(
        md("# Решения: метрики\n\n" + SOL_BANNER),
        code(starter),
        md("## Урок. 1. Split и модель"),
        code(
            "X = df[['distance_km']]\n"
            "y = df['duration_min']\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X, y, test_size=0.2, random_state=42\n"
            ")\n"
            "model = LinearRegression().fit(X_train, y_train)\n"
            "y_pred = model.predict(X_test)\n"
            "print(len(X_train), len(X_test))"
        ),
        md("## Урок. 2. MSE"),
        code(
            "mse = mean_squared_error(y_test, y_pred)\n"
            "print('MSE', round(mse, 2))"
        ),
        md("## Урок. 3. R²"),
        code(
            "r2 = r2_score(y_test, y_pred)\n"
            "print('R2', round(r2, 3))"
        ),
        md("## Урок. 4. Таблица"),
        code(
            "compare = pd.DataFrame({'fact': y_test.values, 'pred': y_pred})\n"
            "compare['error'] = compare['fact'] - compare['pred']\n"
            "print(compare.head())"
        ),
        md("## Урок. 5. Интерпретация"),
        code(
            "METRIC_NOTE = f'R²≈{r2:.2f}: модель объясняет часть разброса длительности на test'\n"
            "print(METRIC_NOTE)"
        ),
        md("## ДЗ. 1. MAE"),
        code(
            "X = df[['distance_km']]\n"
            "y = df['duration_min']\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X, y, test_size=0.2, random_state=42\n"
            ")\n"
            "model = LinearRegression().fit(X_train, y_train)\n"
            "y_pred = model.predict(X_test)\n"
            "mae = float(abs(y_test - y_pred).mean())\n"
            "print(round(mae, 2))"
        ),
        md("## ДЗ. 2. train vs test"),
        code(
            "mse_train = mean_squared_error(y_train, model.predict(X_train))\n"
            "mse_test = mean_squared_error(y_test, y_pred)\n"
            "TRAIN_VS_TEST = (\n"
            "    'На test ошибка важнее: так мы оцениваем обобщение на новые поездки, не заучивание train'\n"
            ")\n"
            "print(mse_train, mse_test, TRAIN_VS_TEST)"
        ),
        md("## ДЗ. 3. Baseline R²"),
        code(
            "import numpy as np\n"
            "baseline_pred = np.full_like(y_test, float(y_train.mean()), dtype=float)\n"
            "r2_baseline = r2_score(y_test, baseline_pred)\n"
            "print(round(r2_baseline, 4))"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson06() -> None:
    base = "lessons/06_try_except_csv"
    stubs = (
        "from pathlib import Path\n"
        "import pandas as pd\n\n\n"
        "def load_trips(path: Path) -> pd.DataFrame:\n"
        "    \"\"\"Загрузить CSV; при отсутствии файла — FileNotFoundError с понятным текстом.\"\"\"\n"
        "    pass\n\n\n"
        "def clean_trips(raw: pd.DataFrame) -> pd.DataFrame:\n"
        "    \"\"\"Удалить строки без distance_km или duration_min.\"\"\"\n"
        "    pass\n"
    )
    lesson = nb(
        md("# try/except при загрузке CSV"),
        code(stubs),
        md("## 1. Успешная загрузка\n\nРеализуйте `load_trips` и загрузите существующий `trips.csv`."),
        code(
            "TRIPS_PATH = None\n"
            "for p in (Path('trips.csv'), Path('../../data/trips.csv'), Path('../data/trips.csv')):\n"
            "    if p.exists():\n"
            "        TRIPS_PATH = p.resolve()\n"
            "        break\n"
            "assert TRIPS_PATH is not None\n"
            "df = load_trips(TRIPS_PATH)\n"
            "assert isinstance(df, pd.DataFrame)\n"
            "assert len(df) > 0\n"
            "print(df.shape)"
        ),
        md("## 2. Ошибка пути\n\nВызовите `load_trips` на несуществующем пути и поймайте `FileNotFoundError`."),
        code(
            "caught = False\n"
            "try:\n"
            "    load_trips(Path('no_such_file.csv'))\n"
            "except FileNotFoundError as e:\n"
            "    caught = True\n"
            "    print('Поймали:', e)\n"
            "assert caught"
        ),
        md(
            "## 3. Очистка\n\n"
            "В копии таблицы обнулите `duration_min` в первой строке (`None`). "
            "`clean_trips` должен убрать ровно одну строку."
        ),
        code(
            "raw = df.copy()\n"
            "raw.loc[raw.index[0], 'duration_min'] = None\n"
            "cleaned = clean_trips(raw)\n"
            "assert len(cleaned) == len(raw) - 1\n"
            "print(len(raw), len(cleaned))"
        ),
    )
    hw = nb(
        md("# ДЗ: устойчивая загрузка"),
        code("from pathlib import Path\nimport pandas as pd\n"),
        md("### A. Закрепление"),
        md(
            "## 1. safe_load\n\n"
            "`safe_load(path)` возвращает DataFrame или `None` при `FileNotFoundError` "
            "(не пробрасывает исключение)."
        ),
        code(
            "def safe_load(path):\n"
            "    pass\n\n\n"
            "assert safe_load(Path('no_such_file.csv')) is None\n"
        ),
        md("## 2. Успешный путь\n\n`safe_load` на реальном `trips.csv` возвращает непустой DataFrame."),
        code(
            "path = None\n"
            "for p in (Path('trips.csv'), Path('../../data/trips.csv'), Path('../data/trips.csv')):\n"
            "    if p.exists():\n"
            "        path = p\n"
            "        break\n"
            "ok = safe_load(path)\n"
            "assert ok is not None and len(ok) > 0\n"
            "print(ok.shape)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. clean_trips и zone\n\n"
            "`clean_trips` не должен трогать строки, где NaN только в `zone` "
            "(ключевые — distance и duration)."
        ),
        code(
            "from copy import deepcopy\n"
            "# переиспользуйте clean_trips из урока или скопируйте реализацию сюда\n"
            "def clean_trips(raw: pd.DataFrame) -> pd.DataFrame:\n"
            "    pass\n\n\n"
            "sample = pd.DataFrame({\n"
            "    'distance_km': [1.0, 2.0],\n"
            "    'duration_min': [10.0, 20.0],\n"
            "    'zone': [None, 'center'],\n"
            "})\n"
            "out = clean_trips(sample)\n"
            "assert len(out) == 2\n"
            "print(out)"
        ),
    )
    sol = nb(
        md("# Решения: try/except\n\n" + SOL_BANNER),
        md("## Урок. 1. load_trips"),
        code(
            "from pathlib import Path\n"
            "import pandas as pd\n\n\n"
            "def load_trips(path: Path) -> pd.DataFrame:\n"
            "    try:\n"
            "        return pd.read_csv(path)\n"
            "    except FileNotFoundError:\n"
            "        raise FileNotFoundError(f'Файл не найден: {path}') from None\n\n\n"
            "TRIPS_PATH = next(\n"
            "    p.resolve()\n"
            "    for p in (Path('trips.csv'), Path('../../data/trips.csv'), Path('../data/trips.csv'))\n"
            "    if p.exists()\n"
            ")\n"
            "df = load_trips(TRIPS_PATH)\n"
            "print(df.shape)"
        ),
        md("## Урок. 2. FileNotFoundError"),
        code(
            "caught = False\n"
            "try:\n"
            "    load_trips(Path('no_such_file.csv'))\n"
            "except FileNotFoundError as e:\n"
            "    caught = True\n"
            "    print('Поймали:', e)\n"
            "assert caught"
        ),
        md("## Урок. 3. clean_trips"),
        code(
            "def clean_trips(raw: pd.DataFrame) -> pd.DataFrame:\n"
            "    return raw.dropna(subset=['distance_km', 'duration_min'])\n\n\n"
            "raw = df.copy()\n"
            "raw.loc[raw.index[0], 'duration_min'] = None\n"
            "assert len(clean_trips(raw)) == len(raw) - 1\n"
            "print(len(raw), len(clean_trips(raw)))"
        ),
        md("## ДЗ. 1. safe_load"),
        code(
            "def safe_load(path):\n"
            "    try:\n"
            "        return pd.read_csv(path)\n"
            "    except FileNotFoundError:\n"
            "        return None\n\n\n"
            "assert safe_load(Path('no_such_file.csv')) is None\n"
            "print('ok')"
        ),
        md("## ДЗ. 2. Успешный путь"),
        code(
            "ok = safe_load(TRIPS_PATH)\n"
            "assert ok is not None and len(ok) > 0\n"
            "print(ok.shape)"
        ),
        md("## ДЗ. 3. zone NaN"),
        code(
            "sample = pd.DataFrame({\n"
            "    'distance_km': [1.0, 2.0],\n"
            "    'duration_min': [10.0, 20.0],\n"
            "    'zone': [None, 'center'],\n"
            "})\n"
            "assert len(clean_trips(sample)) == 2\n"
            "print(clean_trips(sample))"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson07() -> None:
    base = "lessons/07_practice_features"
    fit_stub = (
        "def eval_feature(feature_name: str, random_state: int = 42):\n"
        "    \"\"\"Вернуть (mse, r2) LinearRegression на одном признаке, test 20%, seed.\"\"\"\n"
        "    pass\n"
    )
    lesson = nb(
        md("# Практика: сравнение признаков"),
        code(LOAD_DATA + IMPORTS_SKLEARN + fit_stub),
        md("## 1. Реализуйте `eval_feature`\n\nПроверка на `distance_km`: оба числа конечные, MSE ≥ 0."),
        code(
            "mse_d, r2_d = eval_feature('distance_km')\n"
            "assert mse_d >= 0\n"
            "assert r2_d == r2_d  # not NaN\n"
            "print('distance', round(mse_d, 2), round(r2_d, 3))"
        ),
        md("## 2. hour\n\nТе же метрики для `hour` (тот же seed внутри функции)."),
        code(
            "mse_h, r2_h = eval_feature('hour')\n"
            "print('hour', round(mse_h, 2), round(r2_h, 3))"
        ),
        md("## 3. Сравнение\n\nЛучший признак по R² на test → `BETTER_FEATURE`."),
        code(
            "BETTER_FEATURE = ''\n"
            "assert BETTER_FEATURE in ('distance_km', 'hour')\n"
            "assert BETTER_FEATURE == ('distance_km' if r2_d >= r2_h else 'hour')"
        ),
        md("## 4. Обоснование\n\n2 предложения для отдела аналитики (без слова «магия»)."),
        code(
            "WHY = ''\n"
            "assert len(WHY) > 40\n"
            "print(BETTER_FEATURE, WHY)"
        ),
    )
    hw = nb(
        md("# ДЗ: таблица сравнения"),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("### A. Закрепление"),
        md(
            "## 1. Таблица\n\n"
            "DataFrame со столбцами `feature`, `mse`, `r2` для `distance_km` и `hour`."
        ),
        code(
            "def eval_feature(feature_name: str, random_state: int = 42):\n"
            "    pass\n\n\n"
            "table = None  # DataFrame\n"
            "assert table is not None\n"
            "assert list(table.columns) == ['feature', 'mse', 'r2']\n"
            "assert set(table['feature']) == {'distance_km', 'hour'}\n"
            "print(table)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 2. is_comfort\n\n"
            "Добавьте третий признак `vehicle_type`: сначала закодируйте "
            "`comfort→1`, иначе `0` в новый столбец `is_comfort`, затем `eval_feature('is_comfort')`. "
            "Лучше ли он distance по R²?"
        ),
        code(
            "df = df.copy()\n"
            "df['is_comfort'] = (df['vehicle_type'] == 'comfort').astype(int)\n"
            "mse_c, r2_c = eval_feature('is_comfort')\n"
            "beats_distance = None  # True/False\n"
            "assert beats_distance is False or beats_distance is True\n"
            "print(r2_c, beats_distance)"
        ),
    )
    sol = nb(
        md("# Решения: сравнение признаков\n\n" + SOL_BANNER),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("## Урок. 1. eval_feature на distance"),
        code(
            "def eval_feature(feature_name: str, random_state: int = 42):\n"
            "    X = df[[feature_name]]\n"
            "    y = df['duration_min']\n"
            "    X_tr, X_te, y_tr, y_te = train_test_split(\n"
            "        X, y, test_size=0.2, random_state=random_state\n"
            "    )\n"
            "    pred = LinearRegression().fit(X_tr, y_tr).predict(X_te)\n"
            "    return mean_squared_error(y_te, pred), r2_score(y_te, pred)\n\n\n"
            "mse_d, r2_d = eval_feature('distance_km')\n"
            "print('distance', round(mse_d, 2), round(r2_d, 3))"
        ),
        md("## Урок. 2. hour"),
        code(
            "mse_h, r2_h = eval_feature('hour')\n"
            "print('hour', round(mse_h, 2), round(r2_h, 3))"
        ),
        md("## Урок. 3. BETTER_FEATURE"),
        code(
            "BETTER_FEATURE = 'distance_km' if r2_d >= r2_h else 'hour'\n"
            "print(BETTER_FEATURE)"
        ),
        md("## Урок. 4. WHY"),
        code(
            "WHY = (\n"
            "    f'По R² на test лучше {BETTER_FEATURE} '\n"
            "    f'(distance R²={r2_d:.3f}, hour R²={r2_h:.3f}). '\n"
            "    'Для отчёта фиксируем один признак и те же seed/test_size.'\n"
            ")\n"
            "print(WHY)"
        ),
        md("## ДЗ. 1. Таблица"),
        code(
            "rows = []\n"
            "for f in ('distance_km', 'hour'):\n"
            "    m, r = eval_feature(f)\n"
            "    rows.append({'feature': f, 'mse': m, 'r2': r})\n"
            "table = pd.DataFrame(rows)\n"
            "print(table)"
        ),
        md("## ДЗ. 2. is_comfort"),
        code(
            "df2 = df.copy()\n"
            "df2['is_comfort'] = (df2['vehicle_type'] == 'comfort').astype(int)\n"
            "\n"
            "def eval_feature_df(frame, feature_name: str, random_state: int = 42):\n"
            "    X = frame[[feature_name]]\n"
            "    y = frame['duration_min']\n"
            "    X_tr, X_te, y_tr, y_te = train_test_split(\n"
            "        X, y, test_size=0.2, random_state=random_state\n"
            "    )\n"
            "    pred = LinearRegression().fit(X_tr, y_tr).predict(X_te)\n"
            "    return mean_squared_error(y_te, pred), r2_score(y_te, pred)\n\n\n"
            "mse_c, r2_c = eval_feature_df(df2, 'is_comfort')\n"
            "beats_distance = r2_c > r2_d\n"
            "print(r2_c, beats_distance)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson08() -> None:
    base = "lessons/08_multifeature_overview"
    lesson = nb(
        md("# Несколько признаков (обзор)"),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md(
            "## 1. Два признака\n\n"
            "X = `distance_km` и `hour`. Split 0.2 / seed 42. "
            "Обучите модель; сохраните `r2_two`."
        ),
        code(
            "model = None\n"
            "r2_two = None\n"
            "assert model is not None and r2_two is not None\n"
            "assert len(model.coef_) == 2\n"
            "print('coef', model.coef_, 'R2', round(r2_two, 3))"
        ),
        md(
            "## 2. Сравнение с одним признаком\n\n"
            "Тот же seed: R² только на `distance_km` → `r2_one`. "
            "Запишите в `two_better`, улучшил ли второй признак R² на test "
            "(на этих данных ответ может быть **False** — это нормально для обзора)."
        ),
        code(
            "r2_one = None\n"
            "two_better = None  # True/False: r2_two > r2_one\n"
            "assert r2_one is not None\n"
            "assert two_better == (r2_two > r2_one)\n"
            "print('one', round(r2_one, 3), 'two', round(r2_two, 3), 'two_better', two_better)"
        ),
        md(
            "## 3. Когда добавлять второй столбец\n\n"
            "Кратко: зачем пробовать второй признак и почему «больше столбцов» "
            "не гарантирует лучший R² на test?"
        ),
        code(
            "MULTI_NOTE = ''\n"
            "assert len(MULTI_NOTE) > 30\n"
            "print(MULTI_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: обзор нескольких признаков"),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("### A. Закрепление"),
        md("## 1. MSE двух признаков\n\nMSE на test для distance+hour (seed 42, test 0.2)."),
        code(
            "mse_two = None\n"
            "assert mse_two is not None and mse_two >= 0\n"
            "print(round(mse_two, 2))"
        ),
        md(
            "### B. Вызов\n\n"
            "## 2. Третий признак\n\n"
            "Добавьте `is_comfort` (0/1) к distance+hour. Вырос ли R² относительно двух признаков? "
            "Ответ bool + одна фраза ограничения обзора."
        ),
        code(
            "improved = None\n"
            "LIMIT_NOTE = ''\n"
            "assert improved in (True, False)\n"
            "assert len(LIMIT_NOTE) > 15\n"
            "print(improved, LIMIT_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: несколько признаков\n\n" + SOL_BANNER),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("## Урок. 1. Два признака"),
        code(
            "y = df['duration_min']\n"
            "X2 = df[['distance_km', 'hour']]\n"
            "X2_tr, X2_te, y_tr, y_te = train_test_split(X2, y, test_size=0.2, random_state=42)\n"
            "model = LinearRegression().fit(X2_tr, y_tr)\n"
            "pred2 = model.predict(X2_te)\n"
            "r2_two = r2_score(y_te, pred2)\n"
            "print('coef', model.coef_, 'R2', round(r2_two, 3))"
        ),
        md("## Урок. 2. Сравнение с одним"),
        code(
            "X1 = df[['distance_km']]\n"
            "X1_tr, X1_te, y1_tr, y1_te = train_test_split(X1, y, test_size=0.2, random_state=42)\n"
            "r2_one = r2_score(y1_te, LinearRegression().fit(X1_tr, y1_tr).predict(X1_te))\n"
            "two_better = r2_two > r2_one\n"
            "print('one', round(r2_one, 3), 'two', round(r2_two, 3), 'two_better', two_better)"
        ),
        md("## Урок. 3. MULTI_NOTE"),
        code(
            "MULTI_NOTE = (\n"
            "    'Второй признак стоит пробовать, но решение — по метрике на test: '\n"
            "    'лишний столбец может не помочь или чуть ухудшить R².'\n"
            ")\n"
            "print(MULTI_NOTE)"
        ),
        md("## ДЗ. 1. MSE двух признаков"),
        code(
            "mse_two = mean_squared_error(y_te, pred2)\n"
            "print(round(mse_two, 2))"
        ),
        md("## ДЗ. 2. is_comfort"),
        code(
            "df3 = df.copy()\n"
            "df3['is_comfort'] = (df3['vehicle_type'] == 'comfort').astype(int)\n"
            "X3 = df3[['distance_km', 'hour', 'is_comfort']]\n"
            "X3_tr, X3_te, y3_tr, y3_te = train_test_split(X3, y, test_size=0.2, random_state=42)\n"
            "r2_three = r2_score(y3_te, LinearRegression().fit(X3_tr, y3_tr).predict(X3_te))\n"
            "improved = r2_three > r2_two\n"
            "LIMIT_NOTE = 'Обзорно: рост R² не заменяет проверку на test и осмысленность признаков'\n"
            "print(improved, LIMIT_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson09() -> None:
    base = "lessons/09_report_draft"
    lesson = nb(
        md("# Мини-отчёт: черновик"),
        code(LOAD_DATA + IMPORTS_SKLEARN + IMPORTS_MPL),
        md(
            "## 1. Данные\n\n"
            "2–3 предложения: источник файла, число строк, цель предсказания. "
            "Строка в `REPORT_DATA`."
        ),
        code(
            "REPORT_DATA = ''\n"
            "assert str(len(df)) in REPORT_DATA\n"
            "assert 'duration' in REPORT_DATA.lower() or 'длитель' in REPORT_DATA.lower()\n"
            "print(REPORT_DATA)"
        ),
        md("## 2. EDA\n\n`describe` по distance/duration + краткий вывод в `REPORT_EDA`."),
        code(
            "# describe на экране\n"
            "REPORT_EDA = ''\n"
            "assert len(REPORT_EDA) > 20\n"
            "print(REPORT_EDA)"
        ),
        md(
            "## 3. Модель\n\n"
            "Train/test 0.2 / 42, LR на `distance_km`, метрики test в `report_mse` и `report_r2`."
        ),
        code(
            "report_mse = None\n"
            "report_r2 = None\n"
            "assert report_mse is not None and report_r2 is not None\n"
            "assert report_mse >= 0\n"
            "print('MSE', report_mse, 'R2', report_r2)"
        ),
        md(
            "## 4. Рекомендация\n\n"
            "Черновик абзаца для отдела аналитики (признак, качество, ограничение). "
            "Добить на паре 20."
        ),
        code(
            "REPORT_RECOMMENDATION = ''  # заполните к паре 20\n"
            "assert len(REPORT_RECOMMENDATION) >= 0  # на паре 19 достаточно черновика\n"
            "print(REPORT_RECOMMENDATION or '(черновик пуст — доделать дома / на паре 20)')"
        ),
    )
    hw = nb(
        md("# ДЗ: доработать черновик"),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("### A. Закрепление"),
        md(
            "## 1. Сравнение признаков в тексте\n\n"
            "Добавьте в черновик 2 предложения: R² для distance и hour (seed 42)."
        ),
        code(
            "COMPARE_DRAFT = ''\n"
            "assert 'distance' in COMPARE_DRAFT.lower() or 'distance_km' in COMPARE_DRAFT\n"
            "assert 'hour' in COMPARE_DRAFT.lower()\n"
            "print(COMPARE_DRAFT)"
        ),
        md("### B. Вызов"),
        md("## 2. Рекомендация ≥ 2 предложений\n\nЗаполните `REPORT_RECOMMENDATION`."),
        code(
            "REPORT_RECOMMENDATION = ''\n"
            "assert len(REPORT_RECOMMENDATION) > 40\n"
            "print(REPORT_RECOMMENDATION)"
        ),
    )
    sol = nb(
        md("# Решения: черновик отчёта\n\n" + SOL_BANNER),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("## Урок. 1. Данные"),
        code(
            "REPORT_DATA = (\n"
            "    f'Источник: {TRIPS_PATH.name}, строк: {len(df)}. '\n"
            "    'Цель: предсказать duration_min по признакам поездки.'\n"
            ")\n"
            "print(REPORT_DATA)"
        ),
        md("## Урок. 2. EDA"),
        code(
            "REPORT_EDA = (\n"
            "    'describe показывает разброс distance и duration; '\n"
            "    'на scatter distance→duration видна положительная связь.'\n"
            ")\n"
            "print(REPORT_EDA)"
        ),
        md("## Урок. 3. Модель"),
        code(
            "X = df[['distance_km']]\n"
            "y = df['duration_min']\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            "pred = LinearRegression().fit(X_tr, y_tr).predict(X_te)\n"
            "report_mse = mean_squared_error(y_te, pred)\n"
            "report_r2 = r2_score(y_te, pred)\n"
            "print('MSE', report_mse, 'R2', report_r2)"
        ),
        md("## Урок. 4. Черновик рекомендации"),
        code(
            "REPORT_RECOMMENDATION = ''\n"
            "print(REPORT_RECOMMENDATION or '(черновик пуст — доделать дома / на паре 20)')"
        ),
        md("## ДЗ. 1. Сравнение признаков"),
        code(
            "def r2_of(col):\n"
            "    Xc = df[[col]]\n"
            "    tr, te, ytr, yte = train_test_split(Xc, y, test_size=0.2, random_state=42)\n"
            "    return r2_score(yte, LinearRegression().fit(tr, ytr).predict(te))\n\n\n"
            "COMPARE_DRAFT = (\n"
            "    f'distance_km R²≈{r2_of(\"distance_km\"):.3f}; '\n"
            "    f'hour R²≈{r2_of(\"hour\"):.3f} на том же test.'\n"
            ")\n"
            "print(COMPARE_DRAFT)"
        ),
        md("## ДЗ. 2. Рекомендация"),
        code(
            "REPORT_RECOMMENDATION = (\n"
            "    'Рекомендуем distance_km как основной признак: выше R² на test. '\n"
            "    'Ограничение: один признак и линейная модель; hour можно добавить обзорно.'\n"
            ")\n"
            "print(REPORT_RECOMMENDATION)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson10() -> None:
    base = "lessons/10_report_submit"
    lesson = nb(
        md("# Сдача мини-отчёта"),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md(
            "## 1. Чек-лист\n\n"
            "Пройдите пункты (данные, EDA, train/test+LR, MSE/R² на test, "
            "сравнение ≥2 признаков, рекомендация). Поставьте `CHECKLIST_OK = True`."
        ),
        code(
            "CHECKLIST_OK = False\n"
            "assert CHECKLIST_OK is True"
        ),
        md(
            "## 2. Финальные метрики\n\n"
            "Пересчитайте MSE/R² для выбранной модели на test (зафиксируйте числа сдачи)."
        ),
        code(
            "FINAL_MSE = None\n"
            "FINAL_R2 = None\n"
            "assert FINAL_MSE is not None and FINAL_R2 is not None\n"
            "assert FINAL_MSE >= 0\n"
            "print(FINAL_MSE, FINAL_R2)"
        ),
        md(
            "## 3. Сравнение признаков в сдаче\n\n"
            "Кратко: какой признак лучше и на сколько по R² (два числа)."
        ),
        code(
            "FEATURE_COMPARE_NOTE = ''\n"
            "assert 'distance' in FEATURE_COMPARE_NOTE.lower() or 'hour' in FEATURE_COMPARE_NOTE.lower()\n"
            "assert len(FEATURE_COMPARE_NOTE) > 20\n"
            "print(FEATURE_COMPARE_NOTE)"
        ),
        md(
            "## 4. Рефлексия модуля\n\n"
            "3 предложения: что изменилось после модуля 1 (списки → таблица → sklearn)?"
        ),
        code(
            "REFLECTION = ''\n"
            "assert REFLECTION.count('.') >= 2 or REFLECTION.count('!') + REFLECTION.count('?') >= 2\n"
            "assert len(REFLECTION) > 60\n"
            "print(REFLECTION)"
        ),
    )
    sol = nb(
        md("# Решения: сдача отчёта\n\n" + SOL_BANNER),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("## Урок. 1. Чек-лист"),
        code(
            "CHECKLIST_OK = True\n"
            "print(CHECKLIST_OK)"
        ),
        md("## Урок. 2. Финальные метрики"),
        code(
            "y = df['duration_min']\n"
            "\n"
            "def metrics(cols):\n"
            "    X = df[cols]\n"
            "    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            "    pred = LinearRegression().fit(X_tr, y_tr).predict(X_te)\n"
            "    return mean_squared_error(y_te, pred), r2_score(y_te, pred)\n\n\n"
            "FINAL_MSE, FINAL_R2 = metrics(['distance_km'])\n"
            "print(FINAL_MSE, FINAL_R2)"
        ),
        md("## Урок. 3. Сравнение признаков"),
        code(
            "_, r2_h = metrics(['hour'])\n"
            "FEATURE_COMPARE_NOTE = (\n"
            "    f'distance_km R²={FINAL_R2:.3f}, hour R²={r2_h:.3f} — выбираем distance_km'\n"
            ")\n"
            "print(FEATURE_COMPARE_NOTE)"
        ),
        md("## Урок. 4. Рефлексия"),
        code(
            "REFLECTION = (\n"
            "    'В модуле 1 predict был функцией на списках. '\n"
            "    'Здесь данные — таблица CSV и DataFrame. '\n"
            "    'sklearn даёт fit/predict и метрики на test вместо ручного коэффициента.'\n"
            ")\n"
            "print(REFLECTION)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_report_starter() -> None:
    starter = nb(
        md("# Мини-отчёт: каршеринг «Дорога»"),
        code(LOAD_DATA + IMPORTS_SKLEARN + IMPORTS_MPL),
        md(
            "## 1. Данные\n\n"
            "2–3 предложения: источник файла, число строк, цель предсказания."
        ),
        code(
            "REPORT_DATA = ''  # заполните\n"
            "assert len(REPORT_DATA) > 20\n"
            "assert str(len(df)) in REPORT_DATA\n"
            "print(REPORT_DATA)"
        ),
        md("## 2. EDA\n\n`describe` и/или scatter для связи признака с `duration_min`."),
        code(
            "# ваш код EDA\n"
            "REPORT_EDA = ''\n"
            "assert len(REPORT_EDA) > 20\n"
            "print(REPORT_EDA)"
        ),
        md(
            "## 3. Модель\n\n"
            "Train/test 0.2 / seed 42, `LinearRegression`, MSE и R² **на test**."
        ),
        code(
            "report_mse = None\n"
            "report_r2 = None\n"
            "assert report_mse is not None and report_r2 is not None\n"
            "assert report_mse >= 0\n"
            "print('MSE', report_mse, 'R2', report_r2)"
        ),
        md(
            "## 4. Сравнение признаков\n\n"
            "Таблица или два блока: минимум `distance_km` и `hour`."
        ),
        code(
            "FEATURE_COMPARE = None  # DataFrame или текст\n"
            "assert FEATURE_COMPARE is not None\n"
            "print(FEATURE_COMPARE)"
        ),
        md("## 5. Рекомендация\n\n1 абзац с числами и ограничениями модели."),
        code(
            "REPORT_RECOMMENDATION = ''\n"
            "assert len(REPORT_RECOMMENDATION) > 40\n"
            "print(REPORT_RECOMMENDATION)"
        ),
        md(
            "## 6. Рефлексия\n\n"
            "3 предложения: что изменилось после модуля 1 (списки → таблица → sklearn)?"
        ),
        code(
            "REFLECTION = ''\n"
            "assert len(REFLECTION) > 60\n"
            "print(REFLECTION)"
        ),
    )
    NOTEBOOKS["artifact/starter/report_starter.ipynb"] = starter


def main() -> None:
    add_lesson01()
    add_lesson02()
    add_lesson03()
    add_lesson04()
    add_lesson05()
    add_lesson06()
    add_lesson07()
    add_lesson08()
    add_lesson09()
    add_lesson10()
    add_report_starter()
    for rel, notebook in NOTEBOOKS.items():
        write(rel, notebook)
    src_csv = ROOT / "data" / "trips.csv"
    dst_csv = ROOT / "artifact" / "starter" / "trips.csv"
    if src_csv.exists():
        shutil.copy(src_csv, dst_csv)
        print("copied", dst_csv)
    print(f"total notebooks: {len(NOTEBOOKS)}")


if __name__ == "__main__":
    main()
