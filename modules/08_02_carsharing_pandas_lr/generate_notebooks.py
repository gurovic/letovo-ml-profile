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
        md(
            "# pandas: таблица поездок каршеринга\n\n"
            "Отдел аналитики «Дорога» хранит поездки в CSV. В модуле 1 `predict` работал на "
            "парах чисел; здесь **сотни строк** и **несколько полей** на поездку — нужен `DataFrame`."
        ),
        code(LOAD_DATA),
        md(
            "## 1. Зачем таблица\n\n"
            "Одна **строка** = одна поездка; один **столбец** = одно поле (расстояние, час, зона…). "
            "Выведите число строк и столбцов, первые 5 строк и список имён столбцов.\n\n"
            "**Вопрос:** сколько поездок в файле и сколько полей у каждой?\n\n"
            "**Pitfall:** `print(df)` на больших данных заливает экран — для осмотра хватает "
            "`shape`, `head`, `columns`."
        ),
        code(
            "n_rows, n_cols = None, None  # df.shape\n"
            "# print(df.head())\n"
            "# print(list(df.columns))\n"
            "assert n_rows is not None and n_cols is not None\n"
            "assert isinstance(n_rows, (int, float)) and n_rows > 50\n"
            "assert n_cols >= 5\n"
            "print(n_rows, n_cols)"
        ),
        md(
            "## 2. dtypes: число vs текст\n\n"
            "Вызовите `df.dtypes` (или `df.info()`). Числовые столбцы нужны для `fit`; "
            "`object` — строки/категории, их нельзя сразу подать в `LinearRegression`.\n\n"
            "**How:** `df['distance_km'].dtype` vs `df['zone'].dtype`.\n\n"
            "**Checkpoint:** почему `distance_km` не `object`?"
        ),
        code(
            "# print(df.dtypes)\n"
            "distance_dtype = None  # str(df['distance_km'].dtype)\n"
            "zone_dtype = None  # str(df['zone'].dtype)\n"
            "assert distance_dtype is not None and zone_dtype is not None\n"
            "assert 'object' not in str(distance_dtype).lower() or 'float' in str(distance_dtype).lower() or 'int' in str(distance_dtype).lower()\n"
            "assert 'object' in str(zone_dtype).lower() or str(zone_dtype) == 'object'\n"
            "print('distance:', distance_dtype, '| zone:', zone_dtype)"
        ),
        md(
            "## 3. Одна ячейка через iloc\n\n"
            "Расстояние первой поездки: `df.iloc[0]['distance_km']` (или `df.iloc[0, …]`). "
            "Запишите в `first_distance`.\n\n"
            "**Зачем:** модель потом читает признаки **построчно**.\n\n"
            "**Pitfall:** `iloc` — по **позиции** (0, 1, 2…), не по `trip_id`."
        ),
        code(
            "first_distance = None\n"
            "assert first_distance is not None\n"
            "assert isinstance(first_distance, (int, float)) and first_distance > 0\n"
            "print('первая поездка, км:', first_distance)"
        ),
        md(
            "## 4. loc vs iloc — нюанс\n\n"
            "Возьмите первые 3 строки столбцов `distance_km` и `duration_min` "
            "двумя способами: `.loc` (имена) и `.iloc` (позиции). Значения должны совпасть.\n\n"
            "**Why:** после фильтра индекс строк может быть не 0…n; "
            "`iloc[0]` — «первая видимая», `loc[0]` — «строка с меткой 0» (может отсутствовать)."
        ),
        code(
            "by_name = None  # .loc\n"
            "by_pos = None  # .iloc\n"
            "assert by_name is not None and by_pos is not None\n"
            "assert by_name.shape == (3, 2) and by_pos.shape == (3, 2)\n"
            "assert list(by_name.columns) == ['distance_km', 'duration_min']\n"
            "assert (by_name.values == by_pos.values).all()\n"
            "print(by_name)\n"
            "print(by_pos)"
        ),
        md(
            "## 5. Признак, цель, служебный столбец\n\n"
            "Для ML явно назовите роли:\n"
            "- **цель** — что предсказываем (`duration_min`);\n"
            "- **признаки** — числа/категории для модели;\n"
            "- **id** — служебный ключ, **не** признак.\n\n"
            "Заполните переменные ниже."
        ),
        code(
            "TARGET = ''\n"
            "FEATURES = []\n"
            "ID_COL = ''\n\n"
            "assert TARGET in df.columns\n"
            "assert TARGET not in FEATURES\n"
            "assert ID_COL in df.columns\n"
            "assert ID_COL not in FEATURES\n"
            "assert 'distance_km' in FEATURES\n"
            "assert set(FEATURES).issubset(df.columns)\n"
            "assert df[TARGET].dtype.kind in 'iuf'"
        ),
        md(
            "## 6. value_counts: зоны\n\n"
            "Сколько поездок в каждой `zone`? Используйте `value_counts()` "
            "(частоты категорий — база для EDA и фильтров).\n\n"
            "Запишите число **уникальных** зон в `n_zones`."
        ),
        code(
            "zone_counts = None  # df['zone'].value_counts()\n"
            "# print(zone_counts)\n"
            "n_zones = None\n"
            "assert zone_counts is not None\n"
            "assert n_zones is not None\n"
            "assert isinstance(n_zones, (int, float)) and 2 <= n_zones <= 20\n"
            "print('уникальных zone:', n_zones)\n"
            "print(zone_counts)"
        ),
        md(
            "## 7. Checkpoint: почему не list of dicts\n\n"
            "В модуле 1 данные жили в списках. Здесь — таблица.\n\n"
            "Напишите 2–3 предложения в `WHY_DATAFRAME`: зачем `DataFrame` вместо "
            "`list[dict]` для сотен поездок (фильтр, столбец целиком, dtypes, "
            "готовность к `sklearn`).\n\n"
            "**How:** подумайте про `df['distance_km']` vs цикл по словарям."
        ),
        code(
            "WHY_DATAFRAME = ''\n"
            "assert len(WHY_DATAFRAME) > 40\n"
            "assert 'list' in WHY_DATAFRAME.lower() or 'слов' in WHY_DATAFRAME.lower() or 'dataframe' in WHY_DATAFRAME.lower() or 'таблиц' in WHY_DATAFRAME.lower()\n"
            "print(WHY_DATAFRAME)"
        ),
        md(
            "## 8. Расширение: поездка по id\n\n"
            "Найдите длительность поездки `T0001` через `.loc` и маску по `trip_id`.\n\n"
            "**Зачем:** id нужен для поиска строки, но в `X` для `fit` его не кладут."
        ),
        code(
            "duration_t0001 = None\n"
            "assert duration_t0001 is not None\n"
            "assert isinstance(duration_t0001, (int, float)) and duration_t0001 > 0\n"
            "print('T0001 duration:', duration_t0001)"
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
            "assert duration_t0001 is not None\n"
            "assert isinstance(duration_t0001, (int, float)) and duration_t0001 > 0\n"
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
            "mean_all = None  # float, округлить до 1 знака\n"
            "COMPARE_NOTE = ''  # одна фраза\n"
            "assert mean_comfort is not None and mean_all is not None\n"
            "assert isinstance(mean_comfort, (int, float)) and mean_comfort > 0\n"
            "assert isinstance(mean_all, (int, float)) and mean_all > 0\n"
            "assert len(COMPARE_NOTE) > 10\n"
            "print(mean_comfort, mean_all, COMPARE_NOTE)"
        ),
        md(
            "## 5. value_counts в ДЗ\n\n"
            "Топ-частота `vehicle_type` (какое значение встречается чаще всего). "
            "Запишите имя в `top_vehicle`."
        ),
        code(
            "top_vehicle = None  # str\n"
            "assert top_vehicle is not None\n"
            "assert isinstance(top_vehicle, str) and len(top_vehicle) > 0\n"
            "assert top_vehicle in set(df['vehicle_type'])\n"
            "print(top_vehicle)"
        ),
    )
    sol = nb(
        md("# Решения: pandas DataFrame\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        md("## Урок. 1. Зачем таблица"),
        code(
            "n_rows, n_cols = df.shape\n"
            "print(n_rows, n_cols)\n"
            "print(df.head())\n"
            "print(list(df.columns))"
        ),
        md("## Урок. 2. dtypes"),
        code(
            "distance_dtype = str(df['distance_km'].dtype)\n"
            "zone_dtype = str(df['zone'].dtype)\n"
            "print('distance:', distance_dtype, '| zone:', zone_dtype)"
        ),
        md("## Урок. 3. Одна ячейка"),
        code(
            "first_distance = float(df.iloc[0]['distance_km'])\n"
            "print('первая поездка, км:', first_distance)"
        ),
        md("## Урок. 4. loc vs iloc"),
        code(
            "by_name = df.loc[:2, ['distance_km', 'duration_min']]\n"
            "by_pos = df.iloc[:3][['distance_km', 'duration_min']]\n"
            "assert (by_name.values == by_pos.values).all()\n"
            "print(by_name)\n"
            "print(by_pos)"
        ),
        md("## Урок. 5. Признак / цель / id"),
        code(
            "TARGET = 'duration_min'\n"
            "FEATURES = ['distance_km', 'hour', 'zone', 'vehicle_type']\n"
            "ID_COL = 'trip_id'\n"
            "assert TARGET not in FEATURES and ID_COL not in FEATURES"
        ),
        md("## Урок. 6. value_counts"),
        code(
            "zone_counts = df['zone'].value_counts()\n"
            "n_zones = int(df['zone'].nunique())\n"
            "print('уникальных zone:', n_zones)\n"
            "print(zone_counts)"
        ),
        md("## Урок. 7. WHY_DATAFRAME"),
        code(
            "WHY_DATAFRAME = (\n"
            "    'DataFrame даёт столбцы целиком, фильтры и dtypes без цикла по list[dict]. '\n"
            "    'Сотни поездок удобнее резать маской; sklearn ждёт таблицу признаков X.'\n"
            ")\n"
            "print(WHY_DATAFRAME)"
        ),
        md("## Урок. 8. Поездка по id"),
        code(
            "duration_t0001 = float(df.loc[df['trip_id'] == 'T0001', 'duration_min'].iloc[0])\n"
            "print('T0001 duration:', duration_t0001)"
        ),
        md("## ДЗ. 1. Срез столбцов"),
        code(
            "subset = df[['distance_km', 'duration_min', 'hour']].head(10)\n"
            "print(subset)"
        ),
        md("## ДЗ. 2. Одна поездка"),
        code(
            "duration_t0001 = float(df.loc[df['trip_id'] == 'T0001', 'duration_min'].iloc[0])\n"
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
        md("## ДЗ. 5. top vehicle"),
        code(
            "top_vehicle = str(df['vehicle_type'].value_counts().index[0])\n"
            "print(top_vehicle)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson02() -> None:
    base = "lessons/02_practice_filters"
    lesson = nb(
        md(
            "# Практика: фильтры и типы\n\n"
            "Тот же `trips.csv`. Фильтры — первый инструмент аналитика: "
            "«покажи только центр», «только длинные поездки»."
        ),
        code(LOAD_DATA),
        md(
            "## 1. Фильтр по зоне\n\n"
            "Оставьте строки с `zone == 'center'`. Сколько таких поездок?\n\n"
            "**Why:** маска — Series из True/False той же длины, что `df`.\n\n"
            "**Вопрос:** строка в `center` — подмножество таблицы или новый файл?"
        ),
        code(
            "center = None  # df[маска]\n"
            "assert center is not None\n"
            "assert (center['zone'] == 'center').all()\n"
            "assert len(center) > 0\n"
            "print('center:', len(center), 'из', len(df))"
        ),
        md(
            "## 2. Длинные поездки\n\n"
            "`distance_km >= 15`. Выведите `trip_id`, расстояние, длительность (`head`).\n\n"
            "**Pitfall:** сравнивайте с числом (`15`), не со строкой `'15'`."
        ),
        code(
            "long_trips = None\n"
            "assert long_trips is not None\n"
            "assert (long_trips['distance_km'] >= 15).all()\n"
            "print(long_trips[['trip_id', 'distance_km', 'duration_min']].head())"
        ),
        md(
            "## 3. Составная маска (&)\n\n"
            "Нужны поездки **и** в center, **и** с `distance_km >= 10`. "
            "Так **не работает**: `df['zone'] == 'center' and df['distance_km'] >= 10` — "
            "Python сравнивает два Series через `and` и падает.\n\n"
            "**How:** `&` и скобки вокруг каждого условия: `df[(...) & (...)]`."
        ),
        code(
            "center_long = None  # df[(...) & (...)]\n"
            "assert center_long is not None\n"
            "assert (center_long['zone'] == 'center').all()\n"
            "assert (center_long['distance_km'] >= 10).all()\n"
            "print(len(center_long))"
        ),
        md(
            "## 4. Отрицание ~\n\n"
            "Оставьте поездки **не** из `center` (`zone != 'center'` или `~ (df['zone'] == 'center')`).\n\n"
            "**Checkpoint:** `len(not_center) + len(center)` должно равняться `len(df)` "
            "(если нет NaN в zone)."
        ),
        code(
            "not_center = None\n"
            "assert not_center is not None\n"
            "assert (not_center['zone'] != 'center').all()\n"
            "assert len(not_center) + len(center) == len(df)\n"
            "print('not center:', len(not_center))"
        ),
        md(
            "## 5. Сортировка и топ-N\n\n"
            "Три самые длинные поездки по `duration_min` — только `trip_id` и `duration_min`.\n\n"
            "**How:** `sort_values(..., ascending=False).head(3)`."
        ),
        code(
            "top3 = None\n"
            "assert top3 is not None\n"
            "assert len(top3) == 3\n"
            "assert top3['duration_min'].is_monotonic_decreasing\n"
            "print(top3[['trip_id', 'duration_min']])"
        ),
        md(
            "## 6. Доля фильтра\n\n"
            "Доля поездок `zone == 'center'` среди всех (0–1, округлить до 3 знаков).\n\n"
            "**Why:** абсолютное число строк без доли плохо сравнивать между выборками разного размера."
        ),
        code(
            "share_center = None\n"
            "assert share_center is not None\n"
            "assert 0 < float(share_center) < 1\n"
            "print('доля center:', share_center)"
        ),
        md(
            "## 7. loc vs iloc после фильтра\n\n"
            "После фильтра `center` индекс может быть «дырявым». "
            "Возьмите **первую строку** `center` через `.iloc[0]` и запишите её `trip_id`.\n\n"
            "**Pitfall:** `center.loc[0]` часто падает — метки 0 может не быть."
        ),
        code(
            "first_center_id = None  # str trip_id\n"
            "assert first_center_id is not None\n"
            "assert isinstance(first_center_id, str) and first_center_id.startswith('T')\n"
            "print(first_center_id)"
        ),
        md(
            "## 8. Тип hour\n\n"
            "Приведите `hour` к `int`, проверьте диапазон 0–23. "
            "Час — **категория времени суток**, не дробное число для «средней температуры»."
        ),
        code(
            "hours = None  # df['hour'].astype(int)\n"
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
            "assert n_comfort is not None\n"
            "assert isinstance(n_comfort, (int, float))\n"
            "assert 0 < n_comfort < len(df)\n"
            "print(n_comfort)"
        ),
        md("## 2. Утро\n\n`hour` от 7 до 9 включительно — число строк."),
        code(
            "n_morning = None\n"
            "assert n_morning is not None\n"
            "assert isinstance(n_morning, (int, float))\n"
            "assert 0 < n_morning < len(df)\n"
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
            "assert share_center is not None\n"
            "assert 0 < float(share_center) < 1\n"
            "assert len(SHARE_NOTE) > 8\n"
            "print(share_center, SHARE_NOTE)"
        ),
        md(
            "## 5. Не comfort\n\n"
            "Число строк, где `vehicle_type` **не** `'comfort'` (через `~` или `!=`). "
            "Проверьте: сумма с `n_comfort` равна `len(df)`."
        ),
        code(
            "n_not_comfort = None\n"
            "assert n_not_comfort is not None\n"
            "assert isinstance(n_not_comfort, (int, float))\n"
            "assert 0 < n_not_comfort < len(df)\n"
            "print(n_not_comfort)"
        ),
    )
    sol = nb(
        md("# Решения: фильтры\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        md("## Урок. 1. Фильтр center"),
        code(
            "center = df[df['zone'] == 'center']\n"
            "print('center:', len(center), 'из', len(df))"
        ),
        md("## Урок. 2. Длинные поездки"),
        code(
            "long_trips = df[df['distance_km'] >= 15]\n"
            "print(long_trips[['trip_id', 'distance_km', 'duration_min']].head())"
        ),
        md("## Урок. 3. Составная маска"),
        code(
            "center_long = df[(df['zone'] == 'center') & (df['distance_km'] >= 10)]\n"
            "print(len(center_long))"
        ),
        md("## Урок. 4. Отрицание ~"),
        code(
            "not_center = df[~(df['zone'] == 'center')]\n"
            "assert len(not_center) + len(center) == len(df)\n"
            "print('not center:', len(not_center))"
        ),
        md("## Урок. 5. Топ-3"),
        code(
            "top3 = df.sort_values('duration_min', ascending=False).head(3)\n"
            "print(top3[['trip_id', 'duration_min']])"
        ),
        md("## Урок. 6. Доля center"),
        code(
            "share_center = round(len(center) / len(df), 3)\n"
            "print('доля center:', share_center)"
        ),
        md("## Урок. 7. loc vs iloc после фильтра"),
        code(
            "first_center_id = str(center.iloc[0]['trip_id'])\n"
            "print(first_center_id)"
        ),
        md("## Урок. 8. Тип hour"),
        code(
            "hours = df['hour'].astype(int)\n"
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
        md("## ДЗ. 5. Не comfort"),
        code(
            "n_not_comfort = int((df['vehicle_type'] != 'comfort').sum())\n"
            "print(n_not_comfort)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson03() -> None:
    base = "lessons/03_eda_scatter"
    lesson = nb(
        md(
            "# EDA: describe и scatter\n\n"
            "Перед `fit` аналитик **смотрит** данные: типичные значения, пропуски, "
            "есть ли связь признака с целью. Это EDA — exploratory data analysis."
        ),
        code(LOAD_DATA + IMPORTS_MPL),
        md(
            "## 1. describe: читать таблицу\n\n"
            "Описательная статистика для `distance_km` и `duration_min`.\n\n"
            "**How читать:** `mean` — среднее; `50%` — медиана; `min`/`max` — хвосты; "
            "`std` — разброс.\n\n"
            "Запишите mean длительности в `mean_duration` (без подсказки формулы в assert)."
        ),
        code(
            "stats = None  # df[['distance_km', 'duration_min']].describe()\n"
            "# print(stats)\n"
            "mean_duration = None\n"
            "assert stats is not None\n"
            "assert mean_duration is not None\n"
            "assert isinstance(mean_duration, (int, float)) and mean_duration > 0\n"
            "print('mean duration:', mean_duration)"
        ),
        md(
            "## 2. mean vs median\n\n"
            "Сравните mean и median для `duration_min`. "
            "Если mean заметно больше median — правый хвост (длинные поездки тянут среднее).\n\n"
            "Запишите обе величины и короткий вывод в `MEAN_MEDIAN_NOTE`."
        ),
        code(
            "median_duration = None\n"
            "MEAN_MEDIAN_NOTE = ''\n"
            "assert median_duration is not None\n"
            "assert isinstance(median_duration, (int, float)) and median_duration > 0\n"
            "assert len(MEAN_MEDIAN_NOTE) > 15\n"
            "print(mean_duration, median_duration, MEAN_MEDIAN_NOTE)"
        ),
        md(
            "## 3. info и пропуски\n\n"
            "Вызовите `df.info()`. Сколько **ненулевых** значений в `duration_min`? "
            "Если меньше числа строк — есть пропуски."
        ),
        code(
            "# df.info()\n"
            "n_non_null_duration = None\n"
            "assert n_non_null_duration is not None\n"
            "assert isinstance(n_non_null_duration, (int, float))\n"
            "assert n_non_null_duration == len(df) or n_non_null_duration < len(df)\n"
            "print('non-null duration:', n_non_null_duration, '/', len(df))"
        ),
        md(
            "## 4. Scatter: подписи и ловушки\n\n"
            "Scatter `distance_km` → `duration_min`.\n\n"
            "**Pitfalls:**\n"
            "- без `xlabel`/`ylabel`/`title` график «немой»;\n"
            "- при тысячах точек облако заливает — `alpha=0.4…0.6`;\n"
            "- оси перепутаны → ложный вывод о связи.\n\n"
            "Допишите подписи, затем `SCATTER_DONE = True`."
        ),
        code(
            "plt.figure(figsize=(6, 4))\n"
            "plt.scatter(df['distance_km'], df['duration_min'], alpha=0.5)\n"
            "# plt.xlabel(...); plt.ylabel(...); plt.title(...)\n"
            "plt.show()\n"
            "SCATTER_DONE = False\n"
            "assert SCATTER_DONE"
        ),
        md(
            "## 5. Что видно на графике\n\n"
            "Одно–два предложения: есть ли **положительная** связь расстояние → длительность? "
            "Есть ли **разброс** (точки далеко от воображаемой линии)?"
        ),
        code(
            "EDA_CONCLUSION = ''\n"
            "assert len(EDA_CONCLUSION) > 20\n"
            "print(EDA_CONCLUSION)"
        ),
        md(
            "## 6. hour — другой признак\n\n"
            "Медиана `hour` и scatter `hour` → `duration_min` (с подписями). "
            "Сравните с distance: облако плотнее или размытее?"
        ),
        code(
            "median_hour = None\n"
            "assert median_hour is not None\n"
            "assert 0 <= float(median_hour) <= 23\n"
            "plt.figure(figsize=(6, 4))\n"
            "plt.scatter(df['hour'], df['duration_min'], alpha=0.4)\n"
            "plt.xlabel('hour')\n"
            "plt.ylabel('duration_min')\n"
            "plt.title('Длительность vs час')\n"
            "plt.show()\n"
            "print('median hour:', median_hour)"
        ),
        md(
            "## 7. Корреляция — число, не доказательство\n\n"
            "`corr_dist` — корреляция Пирсона между `distance_km` и `duration_min`.\n\n"
            "**Важно:** corr близко к 1 говорит о **линейной** согласованности на этих данных, "
            "но **не доказывает** причинность («далеко → долго из‑за X»). "
            "Запишите число и фразу-ограничение в `CORR_NOTE`."
        ),
        code(
            "corr_dist = None\n"
            "CORR_NOTE = ''\n"
            "assert corr_dist is not None\n"
            "assert -1 <= float(corr_dist) <= 1\n"
            "assert len(CORR_NOTE) > 20\n"
            "print('corr(distance, duration):', round(float(corr_dist), 3))\n"
            "print(CORR_NOTE)"
        ),
        md(
            "## 8. Checkpoint: какой признак в модель\n\n"
            "По describe + scatter: какой признак перспективнее для **линейной** модели "
            "как первый кандидат — `distance_km` или `hour`? Почему (2 предложения)?"
        ),
        code(
            "BETTER_FOR_LINEAR = ''  # 'distance_km' или 'hour'\n"
            "WHY_EDA = ''\n"
            "assert BETTER_FOR_LINEAR in ('distance_km', 'hour')\n"
            "assert len(WHY_EDA) > 30\n"
            "print(BETTER_FOR_LINEAR, WHY_EDA)"
        ),
    )
    hw = nb(
        md("# ДЗ: EDA"),
        code(LOAD_DATA + IMPORTS_MPL),
        md("### A. Закрепление"),
        md("## 1. describe hour\n\n`describe()` для `hour`. Запишите медиану в `median_hour`."),
        code(
            "median_hour = None\n"
            "assert median_hour is not None\n"
            "assert 0 <= float(median_hour) <= 23\n"
            "print(median_hour)"
        ),
        md("## 2. Scatter hour\n\nScatter `hour` → `duration_min` с подписями осей и заголовком."),
        code(
            "plt.figure(figsize=(6, 4))\n"
            "# ваш scatter + подписи\n"
            "plt.show()\n"
            "HOUR_SCATTER_DONE = False\n"
            "assert HOUR_SCATTER_DONE"
        ),
        md("## 3. max distance\n\n`trip_id` поездки с максимальным `distance_km`."),
        code(
            "max_dist_id = None\n"
            "assert max_dist_id is not None\n"
            "assert isinstance(max_dist_id, str) and str(max_dist_id).startswith('T')\n"
            "print(max_dist_id)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 4. Сравнение scatter\n\n"
            "Сравните визуально distance→duration и hour→duration. "
            "Какой признак перспективнее для **линейной** модели? Почему (2 предложения)?"
        ),
        code(
            "BETTER_FOR_LINEAR = ''  # 'distance_km' или 'hour'\n"
            "WHY_VISUAL = ''\n"
            "assert BETTER_FOR_LINEAR in ('distance_km', 'hour')\n"
            "assert len(WHY_VISUAL) > 30\n"
            "print(BETTER_FOR_LINEAR, WHY_VISUAL)"
        ),
        md(
            "## 5. corr hour\n\n"
            "Корреляция `hour` и `duration_min` (число от −1 до 1) + одна фраза: "
            "меньше по модулю, чем у distance — что это значит для линейной модели?"
        ),
        code(
            "corr_hour = None\n"
            "CORR_HOUR_NOTE = ''\n"
            "assert corr_hour is not None\n"
            "assert -1 <= float(corr_hour) <= 1\n"
            "assert len(CORR_HOUR_NOTE) > 15\n"
            "print(round(float(corr_hour), 3), CORR_HOUR_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: EDA\n\n" + SOL_BANNER),
        code(LOAD_DATA + IMPORTS_MPL),
        md("## Урок. 1. describe"),
        code(
            "stats = df[['distance_km', 'duration_min']].describe()\n"
            "print(stats)\n"
            "mean_duration = float(df['duration_min'].mean())\n"
            "print('mean duration:', mean_duration)"
        ),
        md("## Урок. 2. mean vs median"),
        code(
            "median_duration = float(df['duration_min'].median())\n"
            "MEAN_MEDIAN_NOTE = (\n"
            "    'Сравните mean и median: если mean выше — длинный хвост поездок тянет среднее.'\n"
            ")\n"
            "print(mean_duration, median_duration, MEAN_MEDIAN_NOTE)"
        ),
        md("## Урок. 3. info"),
        code(
            "n_non_null_duration = int(df['duration_min'].notna().sum())\n"
            "print('non-null duration:', n_non_null_duration, '/', len(df))"
        ),
        md("## Урок. 4. Scatter distance"),
        code(
            "plt.figure(figsize=(6, 4))\n"
            "plt.scatter(df['distance_km'], df['duration_min'], alpha=0.5)\n"
            "plt.xlabel('distance_km')\n"
            "plt.ylabel('duration_min')\n"
            "plt.title('Длительность vs расстояние')\n"
            "plt.show()\n"
            "SCATTER_DONE = True"
        ),
        md("## Урок. 5. Вывод EDA"),
        code(
            "EDA_CONCLUSION = (\n"
            "    'С ростом distance_km длительность в среднем растёт, но разброс заметный.'\n"
            ")\n"
            "print(EDA_CONCLUSION)"
        ),
        md("## Урок. 6. hour scatter"),
        code(
            "median_hour = float(df['hour'].median())\n"
            "plt.figure(figsize=(6, 4))\n"
            "plt.scatter(df['hour'], df['duration_min'], alpha=0.4)\n"
            "plt.xlabel('hour')\n"
            "plt.ylabel('duration_min')\n"
            "plt.title('Длительность vs час')\n"
            "plt.show()\n"
            "print('median hour:', median_hour)"
        ),
        md("## Урок. 7. Корреляция"),
        code(
            "corr_dist = float(df['distance_km'].corr(df['duration_min']))\n"
            "CORR_NOTE = (\n"
            "    'corr — мера линейной согласованности на этих данных, не доказательство причины.'\n"
            ")\n"
            "print('corr(distance, duration):', round(corr_dist, 3))\n"
            "print(CORR_NOTE)"
        ),
        md("## Урок. 8. Checkpoint признак"),
        code(
            "BETTER_FOR_LINEAR = 'distance_km'\n"
            "WHY_EDA = (\n"
            "    'На scatter с distance видна наклонная полоса; у hour облако более размытое. '\n"
            "    'Линейная модель на distance — первый кандидат.'\n"
            ")\n"
            "print(BETTER_FOR_LINEAR, WHY_EDA)"
        ),
        md("## ДЗ. 1. hour describe"),
        code(
            "median_hour = float(df['hour'].median())\n"
            "print(median_hour)"
        ),
        md("## ДЗ. 2. Scatter hour"),
        code(
            "plt.figure(figsize=(6, 4))\n"
            "plt.scatter(df['hour'], df['duration_min'], alpha=0.4)\n"
            "plt.xlabel('hour')\n"
            "plt.ylabel('duration_min')\n"
            "plt.title('Длительность vs час')\n"
            "plt.show()\n"
            "HOUR_SCATTER_DONE = True"
        ),
        md("## ДЗ. 3. max distance"),
        code(
            "max_dist_id = str(df.loc[df['distance_km'].idxmax(), 'trip_id'])\n"
            "print(max_dist_id)"
        ),
        md("## ДЗ. 4. Сравнение признаков"),
        code(
            "BETTER_FOR_LINEAR = 'distance_km'\n"
            "WHY_VISUAL = (\n"
            "    'На scatter с distance видна наклонная полоса; у hour облако более размытое. '\n"
            "    'Линейная модель на distance выглядит уместнее как первый кандидат.'\n"
            ")\n"
            "print(BETTER_FOR_LINEAR, WHY_VISUAL)"
        ),
        md("## ДЗ. 5. corr hour"),
        code(
            "corr_hour = float(df['hour'].corr(df['duration_min']))\n"
            "CORR_HOUR_NOTE = 'Слабее линейная связь с duration — hour хуже как единственный признак'\n"
            "print(round(corr_hour, 3), CORR_HOUR_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson04() -> None:
    base = "lessons/04_train_test_lr"
    lesson = nb(
        md(
            "# train/test и LinearRegression\n\n"
            "Переход от осмотра таблицы к первой модели sklearn: признак → split → fit → predict."
        ),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md(
            "## 1. Утечка смыслами (leakage)\n\n"
            "Если учить и проверять модель на **одних и тех же** строках, метрика будет "
            "завышенной: модель «видела» ответы.\n\n"
            "**How в словах:** test — поездки, которых не было в `fit`. "
            "Не подглядывать в test при выборе признаков «до конца модуля» — "
            "пока достаточно: всегда считать качество на отложенных строках.\n\n"
            "Запишите 1–2 предложения в `LEAKAGE_NOTE`."
        ),
        code(
            "LEAKAGE_NOTE = ''\n"
            "assert len(LEAKAGE_NOTE) > 30\n"
            "print(LEAKAGE_NOTE)"
        ),
        md(
            "## 2. Признак и цель\n\n"
            "Соберите `X` как DataFrame из одного столбца `distance_km` и `y` — Series `duration_min`. "
            "Важно: двойные скобки у X (`df[['distance_km']]`)."
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
        md(
            "## 3. train/test split и random_state\n\n"
            "Разделите: 20% в test, `random_state=42`.\n\n"
            "**Why seed:** без него сосед получит другой состав test и другие метрики. "
            "Seed фиксирует перемешивание — воспроизводимость отчёта."
        ),
        code(
            "X_train = X_test = y_train = y_test = None\n"
            "# train_test_split(X, y, test_size=0.2, random_state=42)\n"
            "assert X_test is not None\n"
            "assert len(X_test) == int(0.2 * len(df))\n"
            "assert len(X_train) + len(X_test) == len(df)\n"
            "print(len(X_train), len(X_test))"
        ),
        md(
            "## 4. fit / predict\n\n"
            "Обучите `LinearRegression` **только на train**, предскажите **test**. "
            "Выведите `coef_` и `intercept_`.\n\n"
            "**Связь с модулем 1:** `coef_` — тот же смысл, что коэффициент `k` в ручном `predict`."
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
            "## 5. Другой seed\n\n"
            "Повторите split с тем же `test_size` и `random_state=0`. "
            "Совпадают ли первые 3 индекса `y_test` с предыдущим split? Запишите bool."
        ),
        code(
            "same_first_indices = None  # True/False после эксперимента\n"
            "assert same_first_indices is False\n"
            "print(same_first_indices)"
        ),
        md(
            "## 6. Сборка конвейера целиком\n\n"
            "В одной ячейке заново: `X`/`y` → split 0.2/42 → fit → `y_pred`. "
            "Это шаблон, который повторится на парах метрик и сравнения признаков.\n\n"
            "Проверка: длины и наличие `coef_`."
        ),
        code(
            "# пересоберите pipeline с нуля в переменных ниже\n"
            "X2 = None\n"
            "y2 = None\n"
            "Xtr = Xte = ytr = yte = None\n"
            "model2 = None\n"
            "pred2 = None\n"
            "assert X2 is not None and list(X2.columns) == ['distance_km']\n"
            "assert Xte is not None and len(Xte) == int(0.2 * len(df))\n"
            "assert model2 is not None and hasattr(model2, 'coef_')\n"
            "assert pred2 is not None and len(pred2) == len(yte)\n"
            "print('pipeline ok', len(Xtr), len(Xte), model2.coef_)"
        ),
        md(
            "## 7. Checkpoint: что нельзя делать\n\n"
            "Одна фраза: почему нельзя вызывать `fit` на всём `df`, а потом считать ошибку "
            "на тех же строках и радоваться маленькой ошибке?"
        ),
        code(
            "NO_FIT_ALL_NOTE = ''\n"
            "assert len(NO_FIT_ALL_NOTE) > 25\n"
            "print(NO_FIT_ALL_NOTE)"
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
            "assert n_test_03 is not None\n"
            "assert isinstance(n_test_03, (int, float))\n"
            "assert 40 <= n_test_03 <= 80\n"
            "print(n_test_03)"
        ),
        md(
            "## 2. Воспроизводимость\n\n"
            "Дважды сделайте split 0.2 / seed 42. Совпадают ли `y_test.values` целиком? "
            "Запишите True/False в `reproducible`."
        ),
        code(
            "reproducible = None  # True/False\n"
            "assert reproducible in (True, False)\n"
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
        md(
            "## 4. Leakage своими словами\n\n"
            "2 предложения: чем плох отчёт, где MSE посчитан на train после `fit` на тех же строках."
        ),
        code(
            "HW_LEAKAGE = ''\n"
            "assert len(HW_LEAKAGE) > 40\n"
            "print(HW_LEAKAGE)"
        ),
    )
    sol = nb(
        md("# Решения: train/test и LR\n\n" + SOL_BANNER),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("## Урок. 1. Leakage"),
        code(
            "LEAKAGE_NOTE = (\n"
            "    'Если учить и проверять на одних строках, ошибка занижена: модель видела ответы. '\n"
            "    'Test — отложенные поездки, которых не было в fit.'\n"
            ")\n"
            "print(LEAKAGE_NOTE)"
        ),
        md("## Урок. 2. X и y"),
        code(
            "X = df[['distance_km']]\n"
            "y = df['duration_min']\n"
            "print(X.shape, y.shape)"
        ),
        md("## Урок. 3. train/test split"),
        code(
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X, y, test_size=0.2, random_state=42\n"
            ")\n"
            "print(len(X_train), len(X_test))"
        ),
        md("## Урок. 4. fit / predict"),
        code(
            "model = LinearRegression().fit(X_train, y_train)\n"
            "y_pred = model.predict(X_test)\n"
            "print('coef', model.coef_, 'intercept', model.intercept_)\n"
            "print('первые 3 pred:', y_pred[:3])"
        ),
        md("## Урок. 5. Другой seed"),
        code(
            "_, _, _, y_test_other = train_test_split(X, y, test_size=0.2, random_state=0)\n"
            "same_first_indices = bool((y_test.index[:3] == y_test_other.index[:3]).all())\n"
            "assert same_first_indices is False\n"
            "print(same_first_indices)"
        ),
        md("## Урок. 6. Pipeline целиком"),
        code(
            "X2 = df[['distance_km']]\n"
            "y2 = df['duration_min']\n"
            "Xtr, Xte, ytr, yte = train_test_split(X2, y2, test_size=0.2, random_state=42)\n"
            "model2 = LinearRegression().fit(Xtr, ytr)\n"
            "pred2 = model2.predict(Xte)\n"
            "print('pipeline ok', len(Xtr), len(Xte), model2.coef_)"
        ),
        md("## Урок. 7. Checkpoint"),
        code(
            "NO_FIT_ALL_NOTE = (\n"
            "    'Ошибка на тех же строках, где был fit, не показывает обобщение на новые поездки.'\n"
            ")\n"
            "print(NO_FIT_ALL_NOTE)"
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
        md("## ДЗ. 4. Leakage"),
        code(
            "HW_LEAKAGE = (\n"
            "    'MSE на train после fit на тех же строках занижает ошибку. '\n"
            "    'В отчёте нужны метрики на отложенном test.'\n"
            ")\n"
            "print(HW_LEAKAGE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson05() -> None:
    base = "lessons/05_practice_metrics"
    starter = LOAD_DATA + IMPORTS_SKLEARN
    lesson = nb(
        md(
            "# Практика: MSE и R²\n\n"
            "Модель уже умеет `predict`. Сегодня — **как измерить** качество на test "
            "и сравнить с наивным baseline."
        ),
        code(starter),
        md(
            "## 1. Split и модель\n\n"
            "X = `distance_km`, y = `duration_min`. Split 0.2 / seed 42, "
            "обучите `LinearRegression`, получите `y_pred` на test.\n\n"
            "**How:** тот же конвейер, что на паре 14."
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
            "## 2. MSE — интуиция\n\n"
            "Среднеквадратичная ошибка на **test**: штрафует крупные промахи сильнее "
            "(квадрат разности). Единицы — «минуты²», не минуты.\n\n"
            "Посчитайте `mse` (`mean_squared_error` или вручную)."
        ),
        code(
            "mse = None\n"
            "assert mse is not None\n"
            "assert isinstance(mse, (int, float)) and mse >= 0\n"
            "print('MSE', round(float(mse), 2))"
        ),
        md(
            "## 3. R² — интуиция\n\n"
            "R² на test: какую долю разброса `y` объясняет модель "
            "относительно наивного «всегда среднее». "
            "1 — идеально; 0 — как константа-среднее; отрицательное — хуже константы.\n\n"
            "Запишите `r2`."
        ),
        code(
            "r2 = None\n"
            "assert r2 is not None\n"
            "assert isinstance(r2, (int, float))\n"
            "assert -1 < float(r2) <= 1\n"
            "print('R2', round(float(r2), 3))"
        ),
        md(
            "## 4. Baseline: предсказатель-среднее\n\n"
            "Если предсказывать везде среднее `y_train`, какой будет R² на test? "
            "(ожидание: около 0). Это **нижняя планка**: модель должна бить baseline.\n\n"
            "Запишите `r2_baseline`."
        ),
        code(
            "import numpy as np\n"
            "baseline_pred = None  # вектор длины len(y_test)\n"
            "r2_baseline = None\n"
            "assert baseline_pred is not None and r2_baseline is not None\n"
            "assert -0.25 < float(r2_baseline) < 0.25\n"
            "print('R2 baseline', round(float(r2_baseline), 4))"
        ),
        md(
            "## 5. Train vs test\n\n"
            "Посчитайте MSE на **train** и на **test**. "
            "Одной фразой в `TRAIN_VS_TEST`: почему в отчёт смотрим на test."
        ),
        code(
            "mse_train = None\n"
            "mse_test = None\n"
            "TRAIN_VS_TEST = ''\n"
            "assert mse_train is not None and mse_test is not None\n"
            "assert mse_train >= 0 and mse_test >= 0\n"
            "assert len(TRAIN_VS_TEST) > 20\n"
            "print(round(float(mse_train), 2), round(float(mse_test), 2), TRAIN_VS_TEST)"
        ),
        md(
            "## 6. Таблица сравнения\n\n"
            "DataFrame: столбцы `fact`, `pred`, `error` (= fact − pred). Покажите `head()`."
        ),
        code(
            "compare = None\n"
            "assert compare is not None\n"
            "assert list(compare.columns) == ['fact', 'pred', 'error']\n"
            "assert abs(float(compare['error'].iloc[0]) - (float(compare['fact'].iloc[0]) - float(compare['pred'].iloc[0]))) < 1e-6\n"
            "print(compare.head())"
        ),
        md(
            "## 7. Интерпретация для отчёта\n\n"
            "2 предложения: MSE vs R² — когда смотреть на каждое; "
            "и обогнала ли ваша модель baseline по R²."
        ),
        code(
            "METRIC_NOTE = ''\n"
            "assert len(METRIC_NOTE) > 30\n"
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
            "assert mae is not None and mae >= 0\n"
            "print(round(float(mae), 2))"
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
            "assert mse_train >= 0 and mse_test >= 0\n"
            "assert len(TRAIN_VS_TEST) > 20\n"
            "print(mse_train, mse_test, TRAIN_VS_TEST)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. Baseline R²\n\n"
            "Если предсказывать везде среднее `y_train`, какой будет R² на test? "
            "(ожидание: около 0). Проверьте численно — **не копируйте формулу в assert**."
        ),
        code(
            "import numpy as np\n"
            "baseline_pred = None\n"
            "r2_baseline = None\n"
            "assert baseline_pred is not None and r2_baseline is not None\n"
            "assert -0.2 < float(r2_baseline) < 0.2\n"
            "print(round(float(r2_baseline), 4))"
        ),
        md(
            "## 4. MSE vs R² своими словами\n\n"
            "Когда полезнее MSE, когда R²? 2 предложения без формул в assert."
        ),
        code(
            "MSE_VS_R2 = ''\n"
            "assert len(MSE_VS_R2) > 40\n"
            "print(MSE_VS_R2)"
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
        md("## Урок. 4. Baseline"),
        code(
            "import numpy as np\n"
            "baseline_pred = np.full_like(y_test, float(y_train.mean()), dtype=float)\n"
            "r2_baseline = r2_score(y_test, baseline_pred)\n"
            "print('R2 baseline', round(r2_baseline, 4))"
        ),
        md("## Урок. 5. Train vs test"),
        code(
            "mse_train = mean_squared_error(y_train, model.predict(X_train))\n"
            "mse_test = mean_squared_error(y_test, y_pred)\n"
            "TRAIN_VS_TEST = (\n"
            "    'На test ошибка важнее: так мы оцениваем обобщение на новые поездки'\n"
            ")\n"
            "print(round(mse_train, 2), round(mse_test, 2), TRAIN_VS_TEST)"
        ),
        md("## Урок. 6. Таблица"),
        code(
            "compare = pd.DataFrame({'fact': y_test.values, 'pred': y_pred})\n"
            "compare['error'] = compare['fact'] - compare['pred']\n"
            "print(compare.head())"
        ),
        md("## Урок. 7. Интерпретация"),
        code(
            "METRIC_NOTE = (\n"
            "    f'MSE={mse:.1f} — масштаб ошибки в мин²; R²≈{r2:.2f} — доля объяснённого разброса. '\n"
            "    f'Модель бьёт baseline (R² baseline≈{r2_baseline:.2f}).'\n"
            ")\n"
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
        md("## ДЗ. 4. MSE vs R²"),
        code(
            "MSE_VS_R2 = (\n"
            "    'MSE удобен, когда важен абсолютный масштаб ошибки. '\n"
            "    'R² удобен, чтобы сравнить модель с константой-средним и между признаками.'\n"
            ")\n"
            "print(MSE_VS_R2)"
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
        "    pass\n\n\n"
        "def assert_usable(frame: pd.DataFrame) -> None:\n"
        "    \"\"\"Проверить: непустой df и есть столбцы distance_km, duration_min.\"\"\"\n"
        "    pass\n"
    )
    impl = (
        "def load_trips(path: Path) -> pd.DataFrame:\n"
        "    try:\n"
        "        return pd.read_csv(path)\n"
        "    except FileNotFoundError as e:\n"
        "        raise FileNotFoundError(\n"
        "            f'Файл не найден: {path}. Положите trips.csv рядом с ноутбуком.'\n"
        "        ) from e\n\n\n"
        "def clean_trips(raw: pd.DataFrame) -> pd.DataFrame:\n"
        "    return raw.dropna(subset=['distance_km', 'duration_min']).copy()\n\n\n"
        "def assert_usable(frame: pd.DataFrame) -> None:\n"
        "    if len(frame) == 0:\n"
        "        raise ValueError('пустой DataFrame после очистки')\n"
        "    for col in ('distance_km', 'duration_min'):\n"
        "        if col not in frame.columns:\n"
        "            raise ValueError(f'нет столбца {col}')\n"
    )
    path_finder = (
        "TRIPS_PATH = None\n"
        "for p in (Path('trips.csv'), Path('../../data/trips.csv'), Path('../data/trips.csv')):\n"
        "    if p.exists():\n"
        "        TRIPS_PATH = p.resolve()\n"
        "        break\n"
        "assert TRIPS_PATH is not None\n"
    )
    lesson = nb(
        md(
            "# try/except при загрузке CSV\n\n"
            "В отчёте пайплайн ломается не на `fit`, а на «файл не там» / пустая таблица / нет столбца. "
            "Сегодня — устойчивая загрузка."
        ),
        code(stubs),
        md(
            "## 1. Успешная загрузка\n\n"
            "Реализуйте `load_trips` и загрузите существующий `trips.csv`.\n\n"
            "**How:** `try` вокруг `pd.read_csv`; при успехе вернуть DataFrame."
        ),
        code(
            path_finder
            + "df = load_trips(TRIPS_PATH)\n"
            "assert isinstance(df, pd.DataFrame)\n"
            "assert len(df) > 0\n"
            "print(df.shape)"
        ),
        md(
            "## 2. Ошибка пути\n\n"
            "Вызовите `load_trips` на несуществующем пути и поймайте `FileNotFoundError`.\n\n"
            "**Pitfall:** голое `except:` глотает SyntaxError — ловите конкретный тип. "
            "В сообщении должны быть путь и подсказка."
        ),
        code(
            "caught = False\n"
            "try:\n"
            "    load_trips(Path('no_such_file.csv'))\n"
            "except FileNotFoundError as e:\n"
            "    caught = True\n"
            "    print('Поймали:', e)\n"
            "assert caught\n"
            "ERROR_MSG_NOTE = ''\n"
            "assert len(ERROR_MSG_NOTE) > 20\n"
            "print(ERROR_MSG_NOTE)"
        ),
        md(
            "## 3. Очистка\n\n"
            "`clean_trips`: удалить строки без `distance_km` или `duration_min` "
            "(`dropna(subset=...)`). Проверка: одна NaN в duration → на одну строку меньше."
        ),
        code(
            "raw = df.copy()\n"
            "raw.loc[raw.index[0], 'duration_min'] = None\n"
            "cleaned = clean_trips(raw)\n"
            "assert len(cleaned) == len(raw) - 1\n"
            "print(len(raw), len(cleaned))"
        ),
        md(
            "## 4. assert_usable\n\n"
            "Пустой df и df без `duration_min` должны давать `ValueError`. "
            "Поймайте оба случая и напечатайте сообщение."
        ),
        code(
            "empty = pd.DataFrame(columns=['distance_km', 'duration_min'])\n"
            "try:\n"
            "    assert_usable(empty)\n"
            "    empty_ok = False\n"
            "except ValueError as e:\n"
            "    empty_ok = True\n"
            "    print('empty:', e)\n"
            "bad = pd.DataFrame({'distance_km': [1.0, 2.0], 'hour': [8, 9]})\n"
            "try:\n"
            "    assert_usable(bad)\n"
            "    bad_ok = False\n"
            "except ValueError as e:\n"
            "    bad_ok = True\n"
            "    print('bad cols:', e)\n"
            "assert empty_ok and bad_ok"
        ),
        md(
            "## 5. Pipeline до модели\n\n"
            "`load_trips` → `clean_trips` → `assert_usable`. Выведите shape итога."
        ),
        code(
            "pipeline_df = clean_trips(load_trips(TRIPS_PATH))\n"
            "assert_usable(pipeline_df)\n"
            "assert len(pipeline_df) > 0\n"
            "print('pipeline', pipeline_df.shape)"
        ),
        md(
            "## 6. Checkpoint: зачем try до fit\n\n"
            "Одна фраза: почему ловить отсутствие файла **до** обучения модели, "
            "а не надеяться на ошибку внутри sklearn?"
        ),
        code(
            "WHY_TRY_FIRST = ''\n"
            "assert len(WHY_TRY_FIRST) > 25\n"
            "print(WHY_TRY_FIRST)"
        ),
    )
    hw = nb(
        md("# ДЗ: контракт ошибки"),
        code(stubs + "\n" + path_finder),
        md("### A. Закрепление"),
        md(
            "## 1. safe_load\n\n"
            "Функция `safe_load(path)`: при отсутствии файла вернуть `None`, "
            "иначе DataFrame. Другой контракт, чем `raise`."
        ),
        code(
            "def safe_load(path):\n"
            "    pass\n\n\n"
            "assert safe_load(Path('no_such_file.csv')) is None\n"
            "print('ok')"
        ),
        md("## 2. Успешный путь\n\n`safe_load(TRIPS_PATH)` — непустой DataFrame."),
        code(
            "ok = safe_load(TRIPS_PATH)\n"
            "assert ok is not None and len(ok) > 0\n"
            "print(ok.shape)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. zone NaN\n\n"
            "`clean_trips` не должен удалять строку только из‑за NaN в `zone`, "
            "если distance и duration заполнены."
        ),
        code(
            "# допишите clean_trips выше\n"
            "sample = pd.DataFrame({\n"
            "    'distance_km': [1.0, 2.0],\n"
            "    'duration_min': [10.0, 20.0],\n"
            "    'zone': [None, 'center'],\n"
            "})\n"
            "out = clean_trips(sample)\n"
            "assert len(out) == 2\n"
            "print(out)"
        ),
        md(
            "## 4. Пустой после clean\n\n"
            "Одна строка с NaN в duration → после clean длина 0. "
            "Запишите статус `'empty after clean'` или `'ok'`."
        ),
        code(
            "tiny = pd.DataFrame({'distance_km': [1.0], 'duration_min': [None]})\n"
            "cleaned = clean_trips(tiny)\n"
            "status = None  # 'empty after clean' или 'ok'\n"
            "assert status in ('empty after clean', 'ok')\n"
            "print(status)"
        ),
    )
    sol = nb(
        md("# Решения: try/except CSV\n\n" + SOL_BANNER),
        code("from pathlib import Path\nimport pandas as pd\n\n" + impl),
        md("## Урок. 1. Успешная загрузка"),
        code(
            path_finder
            + "df = load_trips(TRIPS_PATH)\n"
            "print(df.shape)"
        ),
        md("## Урок. 2. Ошибка пути"),
        code(
            "caught = False\n"
            "try:\n"
            "    load_trips(Path('no_such_file.csv'))\n"
            "except FileNotFoundError as e:\n"
            "    caught = True\n"
            "    print('Поймали:', e)\n"
            "assert caught\n"
            "ERROR_MSG_NOTE = (\n"
            "    'Сообщение должно содержать путь и подсказку: '\n"
            "    'положите trips.csv рядом с ноутбуком'\n"
            ")\n"
            "print(ERROR_MSG_NOTE)"
        ),
        md("## Урок. 3. Очистка"),
        code(
            "raw = df.copy()\n"
            "raw.loc[raw.index[0], 'duration_min'] = None\n"
            "cleaned = clean_trips(raw)\n"
            "assert len(cleaned) == len(raw) - 1\n"
            "print(len(raw), len(cleaned))"
        ),
        md("## Урок. 4. assert_usable"),
        code(
            "empty = pd.DataFrame(columns=['distance_km', 'duration_min'])\n"
            "try:\n"
            "    assert_usable(empty)\n"
            "except ValueError as e:\n"
            "    print('empty:', e)\n"
            "bad = pd.DataFrame({'distance_km': [1.0, 2.0], 'hour': [8, 9]})\n"
            "try:\n"
            "    assert_usable(bad)\n"
            "except ValueError as e:\n"
            "    print('bad cols:', e)"
        ),
        md("## Урок. 5. Pipeline"),
        code(
            "pipeline_df = clean_trips(load_trips(TRIPS_PATH))\n"
            "assert_usable(pipeline_df)\n"
            "print('pipeline', pipeline_df.shape)"
        ),
        md("## Урок. 6. Checkpoint"),
        code(
            "WHY_TRY_FIRST = (\n"
            "    'Ошибка файла должна быть понятной до fit: иначе traceback sklearn '\n"
            "    'маскирует проблему данных.'\n"
            ")\n"
            "print(WHY_TRY_FIRST)"
        ),
        md("## ДЗ. 1–2. safe_load"),
        code(
            "def safe_load(path):\n"
            "    try:\n"
            "        return pd.read_csv(path)\n"
            "    except FileNotFoundError:\n"
            "        return None\n\n\n"
            "assert safe_load(Path('no_such_file.csv')) is None\n"
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
            "print(clean_trips(sample))"
        ),
        md("## ДЗ. 4. Пустой после clean"),
        code(
            "tiny = pd.DataFrame({'distance_km': [1.0], 'duration_min': [None]})\n"
            "cleaned = clean_trips(tiny)\n"
            "status = 'empty after clean' if len(cleaned) == 0 else 'ok'\n"
            "print(status)"
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
        md(
            "# Практика: сравнение признаков\n\n"
            "Один и тот же pipeline, два кандидата: `distance_km` и `hour`. "
            "Решение для отчёта — по R² на test при фиксированном seed."
        ),
        code(LOAD_DATA + IMPORTS_SKLEARN + fit_stub),
        md(
            "## 1. Контракт `eval_feature`\n\n"
            "Внутри функции: `X = df[[feature_name]]`, `y = duration_min`, "
            "`train_test_split(..., test_size=0.2, random_state=...)`, "
            "`LinearRegression().fit`, вернуть `(mse, r2)` на test.\n\n"
            "**Why функция:** иначе легко «случайно» сменить seed между признаками."
        ),
        code(
            "# допишите тело eval_feature выше, затем проверьте сигнатуру\n"
            "assert callable(eval_feature)\n"
            "print('eval_feature готов к проверке')"
        ),
        md(
            "## 2. Метрики distance_km\n\n"
            "Проверка на `distance_km`: оба числа конечные, MSE ≥ 0."
        ),
        code(
            "mse_d, r2_d = eval_feature('distance_km')\n"
            "assert mse_d >= 0\n"
            "assert r2_d == r2_d  # not NaN\n"
            "print('distance', round(mse_d, 2), round(r2_d, 3))"
        ),
        md(
            "## 3. Метрики hour\n\n"
            "Те же метрики для `hour` (тот же seed внутри функции)."
        ),
        code(
            "mse_h, r2_h = eval_feature('hour')\n"
            "assert mse_h >= 0\n"
            "print('hour', round(mse_h, 2), round(r2_h, 3))"
        ),
        md(
            "## 4. Таблица сравнения\n\n"
            "Соберите DataFrame со столбцами `feature`, `mse`, `r2` для обоих признаков. "
            "Это заготовка § «сравнение» мини-отчёта."
        ),
        code(
            "compare_table = None  # DataFrame\n"
            "assert compare_table is not None\n"
            "assert list(compare_table.columns) == ['feature', 'mse', 'r2']\n"
            "assert set(compare_table['feature']) == {'distance_km', 'hour'}\n"
            "print(compare_table)"
        ),
        md(
            "## 5. Выбор для отчёта\n\n"
            "Лучший признак по R² на test → `BETTER_FEATURE`."
        ),
        code(
            "BETTER_FEATURE = ''\n"
            "assert BETTER_FEATURE in ('distance_km', 'hour')\n"
            "assert BETTER_FEATURE == ('distance_km' if r2_d >= r2_h else 'hour')\n"
            "print(BETTER_FEATURE)"
        ),
        md(
            "## 6. Обоснование для аналитиков\n\n"
            "2 предложения в `WHY`: числа R² + почему этот признак в отчёт "
            "(без слова «магия»)."
        ),
        code(
            "WHY = ''\n"
            "assert len(WHY) > 40\n"
            "print(BETTER_FEATURE, WHY)"
        ),
        md(
            "## 7. Checkpoint: одинаковый протокол\n\n"
            "Одна фраза: почему нельзя сравнить distance при seed=42 и hour при seed=7?"
        ),
        code(
            "PROTOCOL_NOTE = ''\n"
            "assert len(PROTOCOL_NOTE) > 25\n"
            "print(PROTOCOL_NOTE)"
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
            "assert beats_distance in (True, False)\n"
            "print(r2_c, beats_distance)"
        ),
        md(
            "## 3. Фраза для отчёта\n\n"
            "1–2 предложения: какой признак берёте в сдачу и с какими MSE/R² "
            "(числа из вашей таблицы)."
        ),
        code(
            "REPORT_CHOICE = ''\n"
            "assert len(REPORT_CHOICE) > 30\n"
            "print(REPORT_CHOICE)"
        ),
    )
    sol = nb(
        md("# Решения: сравнение признаков\n\n" + SOL_BANNER),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("## Урок. 1–3. eval_feature"),
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
            "mse_h, r2_h = eval_feature('hour')\n"
            "print('distance', round(mse_d, 2), round(r2_d, 3))\n"
            "print('hour', round(mse_h, 2), round(r2_h, 3))"
        ),
        md("## Урок. 4. Таблица"),
        code(
            "compare_table = pd.DataFrame([\n"
            "    {'feature': 'distance_km', 'mse': mse_d, 'r2': r2_d},\n"
            "    {'feature': 'hour', 'mse': mse_h, 'r2': r2_h},\n"
            "])\n"
            "print(compare_table)"
        ),
        md("## Урок. 5. BETTER_FEATURE"),
        code(
            "BETTER_FEATURE = 'distance_km' if r2_d >= r2_h else 'hour'\n"
            "print(BETTER_FEATURE)"
        ),
        md("## Урок. 6. WHY"),
        code(
            "WHY = (\n"
            "    f'По R² на test лучше {BETTER_FEATURE} '\n"
            "    f'(distance R²={r2_d:.3f}, hour R²={r2_h:.3f}). '\n"
            "    'Для отчёта фиксируем один признак и те же seed/test_size.'\n"
            ")\n"
            "print(WHY)"
        ),
        md("## Урок. 7. PROTOCOL"),
        code(
            "PROTOCOL_NOTE = (\n"
            "    'Разный seed меняет состав test — сравнение R² становится некорректным.'\n"
            ")\n"
            "print(PROTOCOL_NOTE)"
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
        md("## ДЗ. 3. REPORT_CHOICE"),
        code(
            "REPORT_CHOICE = (\n"
            "    f'В сдачу берём {BETTER_FEATURE}: '\n"
            "    f'R² distance={r2_d:.3f}, R² hour={r2_h:.3f} на test (seed 42).'\n"
            ")\n"
            "print(REPORT_CHOICE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson08() -> None:
    base = "lessons/08_multifeature_overview"
    lesson = nb(
        md(
            "# Несколько признаков (обзор)\n\n"
            "Можно ли улучшить R², добавив `hour` к `distance_km`? "
            "Обзорно: два столбца в `X`, тот же seed, сравнение с одним признаком."
        ),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md(
            "## 1. X из двух столбцов\n\n"
            "Соберите `X = df[['distance_km', 'hour']]`, `y = duration_min`. "
            "Проверьте `X.shape[1] == 2`."
        ),
        code(
            "X = None\n"
            "y = None\n"
            "assert X is not None and y is not None\n"
            "assert list(X.columns) == ['distance_km', 'hour']\n"
            "assert X.shape[1] == 2\n"
            "print(X.shape)"
        ),
        md(
            "## 2. Модель на двух признаках\n\n"
            "Split 0.2 / seed 42. Обучите модель; сохраните `r2_two` и посмотрите `coef_` "
            "(два числа — по одному на признак)."
        ),
        code(
            "model = None\n"
            "r2_two = None\n"
            "assert model is not None and r2_two is not None\n"
            "assert len(model.coef_) == 2\n"
            "assert isinstance(r2_two, (int, float))\n"
            "print('coef', model.coef_, 'R2', round(float(r2_two), 3))"
        ),
        md(
            "## 3. Сравнение с одним признаком\n\n"
            "Тот же seed: R² только на `distance_km` → `r2_one`. "
            "Запишите в `two_better`, улучшил ли второй признак R² на test "
            "(на этих данных ответ может быть **False** — это нормально для обзора)."
        ),
        code(
            "r2_one = None\n"
            "two_better = None  # True/False: r2_two > r2_one\n"
            "assert r2_one is not None\n"
            "assert two_better == (r2_two > r2_one)\n"
            "print('one', round(float(r2_one), 3), 'two', round(float(r2_two), 3), 'two_better', two_better)"
        ),
        md(
            "## 4. Когда второй признак мешает\n\n"
            "**Why может упасть R² на test:** шум, корреляция признаков, мало данных, "
            "линейная модель не ловит взаимодействие.\n\n"
            "1–2 предложения в `WHEN_HURTS` — без «магии»."
        ),
        code(
            "WHEN_HURTS = ''\n"
            "assert len(WHEN_HURTS) > 30\n"
            "print(WHEN_HURTS)"
        ),
        md(
            "## 5. Правило для отчёта\n\n"
            "Кратко в `MULTI_NOTE`: зачем пробовать второй признак и почему "
            "«больше столбцов» не гарантирует лучший R² на test?"
        ),
        code(
            "MULTI_NOTE = ''\n"
            "assert len(MULTI_NOTE) > 30\n"
            "print(MULTI_NOTE)"
        ),
        md(
            "## 6. Практика: MSE двух признаков\n\n"
            "Запишите MSE на test для модели distance+hour (тот же split)."
        ),
        code(
            "mse_two = None\n"
            "assert mse_two is not None and mse_two >= 0\n"
            "print('MSE two', round(float(mse_two), 2))"
        ),
        md(
            "## 7. Checkpoint: интерпретация coef_\n\n"
            "Одна фраза: можно ли читать `coef_[1]` (hour) как «минуты на час суток» "
            "без оговорок, если в модели уже есть distance?"
        ),
        code(
            "COEF_READ_NOTE = ''\n"
            "assert len(COEF_READ_NOTE) > 25\n"
            "print(COEF_READ_NOTE)"
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
            "print(round(float(mse_two), 2))"
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
        md(
            "## 3. Когда не добавлять\n\n"
            "2 предложения: в каких условиях вы оставите один признак в сдаче, "
            "даже если «можно» добавить второй."
        ),
        code(
            "KEEP_ONE_NOTE = ''\n"
            "assert len(KEEP_ONE_NOTE) > 30\n"
            "print(KEEP_ONE_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: несколько признаков\n\n" + SOL_BANNER),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("## Урок. 1–2. Два признака"),
        code(
            "y = df['duration_min']\n"
            "X = df[['distance_km', 'hour']]\n"
            "X2_tr, X2_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            "model = LinearRegression().fit(X2_tr, y_tr)\n"
            "pred2 = model.predict(X2_te)\n"
            "r2_two = r2_score(y_te, pred2)\n"
            "print('coef', model.coef_, 'R2', round(r2_two, 3))"
        ),
        md("## Урок. 3. Сравнение с одним"),
        code(
            "X1 = df[['distance_km']]\n"
            "X1_tr, X1_te, y1_tr, y1_te = train_test_split(X1, y, test_size=0.2, random_state=42)\n"
            "r2_one = r2_score(y1_te, LinearRegression().fit(X1_tr, y1_tr).predict(X1_te))\n"
            "two_better = r2_two > r2_one\n"
            "print('one', round(r2_one, 3), 'two', round(r2_two, 3), 'two_better', two_better)"
        ),
        md("## Урок. 4–5. WHEN_HURTS / MULTI_NOTE"),
        code(
            "WHEN_HURTS = (\n"
            "    'Второй признак может добавить шум: R² на test падает, хотя на train всё «красиво».'\n"
            ")\n"
            "MULTI_NOTE = (\n"
            "    'Второй признак стоит пробовать, но решение — по метрике на test: '\n"
            "    'лишний столбец может не помочь или чуть ухудшить R².'\n"
            ")\n"
            "print(WHEN_HURTS)\n"
            "print(MULTI_NOTE)"
        ),
        md("## Урок. 6. MSE"),
        code(
            "mse_two = mean_squared_error(y_te, pred2)\n"
            "print('MSE two', round(mse_two, 2))"
        ),
        md("## Урок. 7. coef_"),
        code(
            "COEF_READ_NOTE = (\n"
            "    'coef hour — при фиксированном distance; это не «минуты на час» без оговорок.'\n"
            ")\n"
            "print(COEF_READ_NOTE)"
        ),
        md("## ДЗ. 1. MSE двух признаков"),
        code(
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
        md("## ДЗ. 3. KEEP_ONE"),
        code(
            "KEEP_ONE_NOTE = (\n"
            "    'Если второй признак не улучшает R² на test или усложняет интерпретацию — '\n"
            "    'в сдачу оставляем один столбец.'\n"
            ")\n"
            "print(KEEP_ONE_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson09() -> None:
    base = "lessons/09_report_draft"
    lesson = nb(
        md(
            "# Мини-отчёт: черновик\n\n"
            "Соберите каркас отчёта для отдела аналитики. "
            "Каждая секция — готовый абзац или числа для `report_starter`."
        ),
        code(LOAD_DATA + IMPORTS_SKLEARN + IMPORTS_MPL),
        md(
            "## 1. Структура отчёта\n\n"
            "Каркас: 1) данные → 2) EDA → 3) модель и метрики на test → "
            "4) сравнение признаков → 5) рекомендация + ограничения.\n\n"
            "Поставьте `STRUCTURE_OK = True`, когда порядок ясен."
        ),
        code(
            "STRUCTURE_OK = False\n"
            "assert STRUCTURE_OK is True"
        ),
        md(
            "## 2. Данные\n\n"
            "2–3 предложения в `REPORT_DATA`: источник файла, число строк, цель предсказания. "
            "В тексте должно быть число строк (`len(df)`)."
        ),
        code(
            "REPORT_DATA = ''\n"
            "assert str(len(df)) in REPORT_DATA\n"
            "assert 'duration' in REPORT_DATA.lower() or 'длитель' in REPORT_DATA.lower()\n"
            "print(REPORT_DATA)"
        ),
        md(
            "## 3. EDA\n\n"
            "`describe` по distance/duration на экране + краткий вывод в `REPORT_EDA`."
        ),
        code(
            "# print(df[['distance_km', 'duration_min']].describe())\n"
            "REPORT_EDA = ''\n"
            "assert len(REPORT_EDA) > 20\n"
            "print(REPORT_EDA)"
        ),
        md(
            "## 4. Модель\n\n"
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
            "## 5. Сравнение признаков (черновик)\n\n"
            "2 предложения: R² для distance и hour при том же протоколе (seed 42)."
        ),
        code(
            "COMPARE_DRAFT = ''\n"
            "assert 'distance' in COMPARE_DRAFT.lower() or 'distance_km' in COMPARE_DRAFT\n"
            "assert 'hour' in COMPARE_DRAFT.lower()\n"
            "print(COMPARE_DRAFT)"
        ),
        md(
            "## 6. Рекомендация (черновик)\n\n"
            "Абзац: признак, качество, ограничение. Добить на паре 20, если не успеете."
        ),
        code(
            "REPORT_RECOMMENDATION = ''\n"
            "assert len(REPORT_RECOMMENDATION) >= 0\n"
            "print(REPORT_RECOMMENDATION or '(черновик пуст — доделать дома / на паре 20)')"
        ),
        md(
            "## 7. Ограничения модели\n\n"
            "1–2 предложения в `LIMITATIONS`: линейность, число признаков, данные одной компании."
        ),
        code(
            "LIMITATIONS = ''\n"
            "assert len(LIMITATIONS) > 25\n"
            "print(LIMITATIONS)"
        ),
    )
    hw = nb(
        md("# ДЗ: доработать черновик"),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("### A. Закрепление"),
        md(
            "## 1. Сравнение признаков в тексте\n\n"
            "2 предложения: R² для distance и hour (seed 42)."
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
        md(
            "## 3. Полный каркас\n\n"
            "Склейте `FULL_DRAFT`: данные + EDA + рекомендация (минимум 80 символов)."
        ),
        code(
            "FULL_DRAFT = ''\n"
            "assert len(FULL_DRAFT) > 80\n"
            "print(FULL_DRAFT)"
        ),
    )
    sol = nb(
        md("# Решения: черновик отчёта\n\n" + SOL_BANNER),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("## Урок. 1. Структура"),
        code(
            "STRUCTURE_OK = True\n"
            "print(STRUCTURE_OK)"
        ),
        md("## Урок. 2. Данные"),
        code(
            "REPORT_DATA = (\n"
            "    f'Источник: {TRIPS_PATH.name}, строк: {len(df)}. '\n"
            "    'Цель: предсказать duration_min по признакам поездки.'\n"
            ")\n"
            "print(REPORT_DATA)"
        ),
        md("## Урок. 3. EDA"),
        code(
            "print(df[['distance_km', 'duration_min']].describe())\n"
            "REPORT_EDA = (\n"
            "    'describe показывает разброс distance и duration; '\n"
            "    'на scatter distance→duration видна положительная связь.'\n"
            ")\n"
            "print(REPORT_EDA)"
        ),
        md("## Урок. 4. Модель"),
        code(
            "X = df[['distance_km']]\n"
            "y = df['duration_min']\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            "pred = LinearRegression().fit(X_tr, y_tr).predict(X_te)\n"
            "report_mse = mean_squared_error(y_te, pred)\n"
            "report_r2 = r2_score(y_te, pred)\n"
            "print('MSE', report_mse, 'R2', report_r2)"
        ),
        md("## Урок. 5. Сравнение"),
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
        md("## Урок. 6–7. Рекомендация и ограничения"),
        code(
            "REPORT_RECOMMENDATION = (\n"
            "    'Рекомендуем distance_km как основной признак: выше R² на test. '\n"
            "    'Ограничение: один признак и линейная модель.'\n"
            ")\n"
            "LIMITATIONS = (\n"
            "    'Линейная модель и данные одной компании не обещают точность на других городах.'\n"
            ")\n"
            "print(REPORT_RECOMMENDATION)\n"
            "print(LIMITATIONS)"
        ),
        md("## ДЗ. 1–3"),
        code(
            "FULL_DRAFT = REPORT_DATA + ' ' + REPORT_EDA + ' ' + REPORT_RECOMMENDATION\n"
            "print(FULL_DRAFT)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson10() -> None:
    base = "lessons/10_report_submit"
    lesson = nb(
        md(
            "# Сдача мини-отчёта\n\n"
            "Финиш модуля 2: чек-лист PROJECT, финальные числа, мост к модулю 1, сдача starter."
        ),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md(
            "## 1. Чек-лист сдачи\n\n"
            "Пройдите пункты (данные, EDA, train/test+LR, MSE/R² на test, "
            "сравнение ≥2 признаков, рекомендация, ограничения). "
            "Сверьте с PROJECT.md. Поставьте `CHECKLIST_OK = True`."
        ),
        code(
            "CHECKLIST_OK = False\n"
            "assert CHECKLIST_OK is True"
        ),
        md(
            "## 2. Мост к модулю 1\n\n"
            "3 коротких пункта в `BRIDGE_M1`: `predict` на списках → DataFrame + "
            "`fit`/`predict` sklearn; связь `k` и `coef_`."
        ),
        code(
            "BRIDGE_M1 = ''\n"
            "assert len(BRIDGE_M1) > 50\n"
            "assert 'coef' in BRIDGE_M1.lower() or 'predict' in BRIDGE_M1.lower() or 'спис' in BRIDGE_M1.lower()\n"
            "print(BRIDGE_M1)"
        ),
        md(
            "## 3. Финальные метрики\n\n"
            "Пересчитайте MSE/R² для выбранной модели на test. Seed 42, test 0.2."
        ),
        code(
            "FINAL_MSE = None\n"
            "FINAL_R2 = None\n"
            "assert FINAL_MSE is not None and FINAL_R2 is not None\n"
            "assert FINAL_MSE >= 0\n"
            "print(FINAL_MSE, FINAL_R2)"
        ),
        md(
            "## 4. Сравнение признаков в сдаче\n\n"
            "Кратко: какой признак лучше и на сколько по R² (два числа)."
        ),
        code(
            "FEATURE_COMPARE_NOTE = ''\n"
            "assert 'distance' in FEATURE_COMPARE_NOTE.lower() or 'hour' in FEATURE_COMPARE_NOTE.lower()\n"
            "assert len(FEATURE_COMPARE_NOTE) > 20\n"
            "print(FEATURE_COMPARE_NOTE)"
        ),
        md(
            "## 5. Рефлексия модуля\n\n"
            "3 предложения: что изменилось после модуля 1 (списки → таблица → sklearn)?"
        ),
        code(
            "REFLECTION = ''\n"
            "assert REFLECTION.count('.') >= 2 or REFLECTION.count('!') + REFLECTION.count('?') >= 2\n"
            "assert len(REFLECTION) > 60\n"
            "print(REFLECTION)"
        ),
        md(
            "## 6. Файл сдачи\n\n"
            "Сдаём заполненный `artifact/starter/report_starter.ipynb` (не только этот lesson). "
            "Поставьте `STARTER_READY = True`, когда starter заполнен."
        ),
        code(
            "STARTER_READY = False\n"
            "assert STARTER_READY is True\n"
            "print('starter ready')"
        ),
        md(
            "## 7. Финальный gate\n\n"
            "Все флаги True и числа на месте? `SUBMIT_NOTE` — одна фраза, что отправляете в Canvas."
        ),
        code(
            "SUBMIT_NOTE = ''\n"
            "assert CHECKLIST_OK and STARTER_READY\n"
            "assert FINAL_MSE is not None and FINAL_R2 is not None\n"
            "assert len(SUBMIT_NOTE) > 15\n"
            "print(SUBMIT_NOTE)"
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
        md("## Урок. 2. Мост к модулю 1"),
        code(
            "BRIDGE_M1 = (\n"
            "    'В модуле 1 predict был функцией на списках с ручным k. '\n"
            "    'Здесь данные — DataFrame из CSV; sklearn даёт fit/predict. '\n"
            "    'coef_ — тот же смысл, что k, но подобран по train.'\n"
            ")\n"
            "print(BRIDGE_M1)"
        ),
        md("## Урок. 3. Финальные метрики"),
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
        md("## Урок. 4. Сравнение признаков"),
        code(
            "_, r2_h = metrics(['hour'])\n"
            "FEATURE_COMPARE_NOTE = (\n"
            "    f'distance_km R²={FINAL_R2:.3f}, hour R²={r2_h:.3f} — выбираем distance_km'\n"
            ")\n"
            "print(FEATURE_COMPARE_NOTE)"
        ),
        md("## Урок. 5. Рефлексия"),
        code(
            "REFLECTION = (\n"
            "    'В модуле 1 predict был функцией на списках. '\n"
            "    'Здесь данные — таблица CSV и DataFrame. '\n"
            "    'sklearn даёт fit/predict и метрики на test вместо ручного коэффициента.'\n"
            ")\n"
            "print(REFLECTION)"
        ),
        md("## Урок. 6–7. Сдача"),
        code(
            "STARTER_READY = True\n"
            "SUBMIT_NOTE = 'Отправляю заполненный report_starter.ipynb с метриками на test и сравнением признаков'\n"
            "print(STARTER_READY, SUBMIT_NOTE)"
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
