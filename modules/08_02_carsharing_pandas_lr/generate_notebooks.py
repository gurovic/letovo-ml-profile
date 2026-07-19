#!/usr/bin/env python3
"""Generate lesson notebooks for module 08_02 (KTP pairs 9–16).

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
    "def find_listings_csv() -> Path:\n"
    "    for p in (Path('listings.csv'), Path('../../data/listings.csv'), Path('../data/listings.csv')):\n"
    "        if p.exists():\n"
    "            return p.resolve()\n"
    "    raise FileNotFoundError('listings.csv не найден')\n\n\n"
    "LISTINGS_PATH = find_listings_csv()\n"
    "df = pd.read_csv(LISTINGS_PATH)\n"
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
            "# pandas: таблица объявлений краткосрочной аренды\n\n"
            "Отдел аналитики «StayLocal» хранит объявления в CSV. В модуле 1 `predict` работал на "
            "парах чисел; здесь **сотни строк** и **несколько полей** на объявление — нужен `DataFrame`."
        ),
        code(LOAD_DATA),
        md(
            "## 1. Зачем таблица\n\n"
            "Одна **строка** = одно объявление; один **столбец** = одно поле (вместимость, отзывы, район…). "
            "Выведите число строк и столбцов, первые 5 строк и список имён столбцов.\n\n"
            "**Вопрос:** сколько объявлений в файле и сколько полей у каждой?\n\n"
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
            "**How:** `df['accommodates'].dtype` vs `df['neighbourhood'].dtype`.\n\n"
            "**Checkpoint:** почему `accommodates` не `object`?"
        ),
        code(
            "# print(df.dtypes)\n"
            "accommodates_dtype = None  # str(df['accommodates'].dtype)\n"
            "neighbourhood_dtype = None  # str(df['neighbourhood'].dtype)\n"
            "assert accommodates_dtype is not None and neighbourhood_dtype is not None\n"
            "assert 'object' not in str(accommodates_dtype).lower() or 'float' in str(accommodates_dtype).lower() or 'int' in str(accommodates_dtype).lower()\n"
            "assert 'object' in str(neighbourhood_dtype).lower() or str(neighbourhood_dtype) == 'object'\n"
            "print('accommodates:', accommodates_dtype, '| neighbourhood:', neighbourhood_dtype)"
        ),
        md(
            "## 3. Одна ячейка через iloc\n\n"
            "Вместимость первого объявления: `df.iloc[0]['accommodates']` (или `df.iloc[0, …]`). "
            "Запишите в `first_accommodates`.\n\n"
            "**Зачем:** модель потом читает признаки **построчно**.\n\n"
            "**Pitfall:** `iloc` — по **позиции** (0, 1, 2…), не по `listing_id`."
        ),
        code(
            "first_accommodates = None\n"
            "assert first_accommodates is not None\n"
            "assert isinstance(first_accommodates, (int, float)) and first_accommodates > 0\n"
            "print('первый listing, accommodates:', first_accommodates)"
        ),
        md(
            "## 4. loc vs iloc — нюанс\n\n"
            "Возьмите первые 3 строки столбцов `accommodates` и `price` "
            "двумя способами: `.loc` (имена) и `.iloc` (позиции). Значения должны совпасть.\n\n"
            "**Why:** после фильтра индекс строк может быть не 0…n; "
            "`iloc[0]` — «первая видимая», `loc[0]` — «строка с меткой 0» (может отсутствовать)."
        ),
        code(
            "by_name = None  # .loc\n"
            "by_pos = None  # .iloc\n"
            "assert by_name is not None and by_pos is not None\n"
            "assert by_name.shape == (3, 2) and by_pos.shape == (3, 2)\n"
            "assert list(by_name.columns) == ['accommodates', 'price']\n"
            "assert (by_name.values == by_pos.values).all()\n"
            "print(by_name)\n"
            "print(by_pos)"
        ),
        md(
            "## 5. Признак, цель, служебный столбец\n\n"
            "Для ML явно назовите роли:\n"
            "- **цель** — что предсказываем (`price`);\n"
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
            "assert 'accommodates' in FEATURES\n"
            "assert set(FEATURES).issubset(df.columns)\n"
            "assert df[TARGET].dtype.kind in 'iuf'"
        ),
        md(
            "## 6. value_counts: районы\n\n"
            "Сколько объявлений в каждом `neighbourhood`? Используйте `value_counts()` "
            "(частоты категорий — база для EDA и фильтров).\n\n"
            "Запишите число **уникальных** зон в `n_neighbourhoods`."
        ),
        code(
            "neighbourhood_counts = None  # df['neighbourhood'].value_counts()\n"
            "# print(neighbourhood_counts)\n"
            "n_neighbourhoods = None\n"
            "assert neighbourhood_counts is not None\n"
            "assert n_neighbourhoods is not None\n"
            "assert isinstance(n_neighbourhoods, (int, float)) and 2 <= n_neighbourhoods <= 20\n"
            "print('уникальных neighbourhood:', n_neighbourhoods)\n"
            "print(neighbourhood_counts)"
        ),
        md(
            "## 7. Checkpoint: почему не list of dicts\n\n"
            "В модуле 1 данные жили в списках. Здесь — таблица.\n\n"
            "Напишите 2–3 предложения в `WHY_DATAFRAME`: зачем `DataFrame` вместо "
            "`list[dict]` для сотен объявлений (фильтр, столбец целиком, dtypes, "
            "готовность к `sklearn`).\n\n"
            "**How:** подумайте про `df['accommodates']` vs цикл по словарям."
        ),
        code(
            "WHY_DATAFRAME = ''\n"
            "assert len(WHY_DATAFRAME) > 40\n"
            "assert 'list' in WHY_DATAFRAME.lower() or 'слов' in WHY_DATAFRAME.lower() or 'dataframe' in WHY_DATAFRAME.lower() or 'таблиц' in WHY_DATAFRAME.lower()\n"
            "print(WHY_DATAFRAME)"
        ),
        md(
            "## 8. Расширение: объявление по id\n\n"
            "Найдите цену объявления `L0001` через `.loc` и маску по `listing_id`.\n\n"
            "**Зачем:** id нужен для поиска строки, но в `X` для `fit` его не кладут."
        ),
        code(
            "price_l0001 = None\n"
            "assert price_l0001 is not None\n"
            "assert isinstance(price_l0001, (int, float)) and price_l0001 > 0\n"
            "print('L0001 price:', price_l0001)"
        ),
    )
    hw = nb(
        md("# ДЗ: осмотр таблицы"),
        code(LOAD_DATA),
        md("### A. Закрепление"),
        md("## 1. Срез столбцов\n\nПервые 10 строк только `accommodates`, `price`, `number_of_reviews`."),
        code(
            "subset = None  # DataFrame 10×3\n"
            "assert subset is not None\n"
            "assert list(subset.columns) == ['accommodates', 'price', 'number_of_reviews']\n"
            "assert len(subset) == 10\n"
            "print(subset)"
        ),
        md("## 2. Одно объявление\n\nЦена объявления с `listing_id == 'L0001'`."),
        code(
            "price_l0001 = None  # число\n"
            "assert price_l0001 is not None\n"
            "assert isinstance(price_l0001, (int, float)) and price_l0001 > 0\n"
            "print(price_l0001)"
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
            "## 4. Средняя entire\n\n"
            "Средняя `price` только для `room_type == 'entire'` "
            "(округлите до 1 знака). Сравните со средним по всей таблице — одной фразой."
        ),
        code(
            "mean_entire = None  # float\n"
            "mean_all = None  # float, округлить до 1 знака\n"
            "COMPARE_NOTE = ''  # одна фраза\n"
            "assert mean_entire is not None and mean_all is not None\n"
            "assert isinstance(mean_entire, (int, float)) and mean_entire > 0\n"
            "assert isinstance(mean_all, (int, float)) and mean_all > 0\n"
            "assert len(COMPARE_NOTE) > 10\n"
            "print(mean_entire, mean_all, COMPARE_NOTE)"
        ),
        md(
            "## 5. value_counts в ДЗ\n\n"
            "Топ-частота `room_type` (какое значение встречается чаще всего). "
            "Запишите имя в `top_room_type`."
        ),
        code(
            "top_room_type = None  # str\n"
            "assert top_room_type is not None\n"
            "assert isinstance(top_room_type, str) and len(top_room_type) > 0\n"
            "assert top_room_type in set(df['room_type'])\n"
            "print(top_room_type)"
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
            "accommodates_dtype = str(df['accommodates'].dtype)\n"
            "neighbourhood_dtype = str(df['neighbourhood'].dtype)\n"
            "print('accommodates:', accommodates_dtype, '| neighbourhood:', neighbourhood_dtype)"
        ),
        md("## Урок. 3. Одна ячейка"),
        code(
            "first_accommodates = float(df.iloc[0]['accommodates'])\n"
            "print('первый listing, accommodates:', first_accommodates)"
        ),
        md("## Урок. 4. loc vs iloc"),
        code(
            "by_name = df.loc[:2, ['accommodates', 'price']]\n"
            "by_pos = df.iloc[:3][['accommodates', 'price']]\n"
            "assert (by_name.values == by_pos.values).all()\n"
            "print(by_name)\n"
            "print(by_pos)"
        ),
        md("## Урок. 5. Признак / цель / id"),
        code(
            "TARGET = 'price'\n"
            "FEATURES = ['accommodates', 'number_of_reviews', 'neighbourhood', 'room_type']\n"
            "ID_COL = 'listing_id'\n"
            "assert TARGET not in FEATURES and ID_COL not in FEATURES"
        ),
        md("## Урок. 6. value_counts"),
        code(
            "neighbourhood_counts = df['neighbourhood'].value_counts()\n"
            "n_neighbourhoods = int(df['neighbourhood'].nunique())\n"
            "print('уникальных neighbourhood:', n_neighbourhoods)\n"
            "print(neighbourhood_counts)"
        ),
        md("## Урок. 7. WHY_DATAFRAME"),
        code(
            "WHY_DATAFRAME = (\n"
            "    'DataFrame даёт столбцы целиком, фильтры и dtypes без цикла по list[dict]. '\n"
            "    'Сотни объявлений удобнее резать маской; sklearn ждёт таблицу признаков X.'\n"
            ")\n"
            "print(WHY_DATAFRAME)"
        ),
        md("## Урок. 8. Объявление по id"),
        code(
            "price_l0001 = float(df.loc[df['listing_id'] == 'L0001', 'price'].iloc[0])\n"
            "print('L0001 price:', price_l0001)"
        ),
        md("## ДЗ. 1. Срез столбцов"),
        code(
            "subset = df[['accommodates', 'price', 'number_of_reviews']].head(10)\n"
            "print(subset)"
        ),
        md("## ДЗ. 2. Одно объявление"),
        code(
            "price_l0001 = float(df.loc[df['listing_id'] == 'L0001', 'price'].iloc[0])\n"
            "print(price_l0001)"
        ),
        md("## ДЗ. 3. Два способа длины"),
        code(
            "a = len(df)\n"
            "b = df.shape[0]\n"
            "assert a == b\n"
            "print(a)"
        ),
        md("## ДЗ. 4. Средняя entire"),
        code(
            "mean_entire = round(df.loc[df['room_type'] == 'entire', 'price'].mean(), 1)\n"
            "mean_all = round(df['price'].mean(), 1)\n"
            "COMPARE_NOTE = f'entire: {mean_entire}, все: {mean_all} — сравните порядок величин'\n"
            "print(mean_entire, mean_all, COMPARE_NOTE)"
        ),
        md("## ДЗ. 5. top room_type"),
        code(
            "top_room_type = str(df['room_type'].value_counts().index[0])\n"
            "print(top_room_type)"
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
            "Тот же `listings.csv`. Фильтры — первый инструмент аналитика: "
            "«покажи только центр», «только вместительные объявления»."
        ),
        code(LOAD_DATA),
        md(
            "## 1. Фильтр по району\n\n"
            "Оставьте строки с `neighbourhood == 'center'`. Сколько таких объявлений?\n\n"
            "**Why:** маска — Series из True/False той же длины, что `df`.\n\n"
            "**Вопрос:** строка в `center` — подмножество таблицы или новый файл?"
        ),
        code(
            "center = None  # df[маска]\n"
            "assert center is not None\n"
            "assert (center['neighbourhood'] == 'center').all()\n"
            "assert len(center) > 0\n"
            "print('center:', len(center), 'из', len(df))"
        ),
        md(
            "## 2. Вместительные объявления\n\n"
            "`accommodates >= 6`. Выведите `listing_id`, вместимость, цена (`head`).\n\n"
            "**Pitfall:** сравнивайте с числом (`6`), не со строкой `'6'`."
        ),
        code(
            "large_listings = None\n"
            "assert large_listings is not None\n"
            "assert (large_listings['accommodates'] >= 6).all()\n"
            "print(large_listings[['listing_id', 'accommodates', 'price']].head())"
        ),
        md(
            "## 3. Составная маска (&)\n\n"
            "Нужны объявления **и** в center, **и** с `accommodates >= 4`. "
            "Так **не работает**: `df['neighbourhood'] == 'center' and df['accommodates'] >= 4` — "
            "Python сравнивает два Series через `and` и падает.\n\n"
            "**How:** `&` и скобки вокруг каждого условия: `df[(...) & (...)]`."
        ),
        code(
            "center_long = None  # df[(...) & (...)]\n"
            "assert center_long is not None\n"
            "assert (center_long['neighbourhood'] == 'center').all()\n"
            "assert (center_long['accommodates'] >= 4).all()\n"
            "print(len(center_long))"
        ),
        md(
            "## 4. Отрицание ~\n\n"
            "Оставьте объявления **не** из `center` (`neighbourhood != 'center'` или `~ (df['neighbourhood'] == 'center')`).\n\n"
            "**Checkpoint:** `len(not_center) + len(center)` должно равняться `len(df)` "
            "(если нет NaN в neighbourhood)."
        ),
        code(
            "not_center = None\n"
            "assert not_center is not None\n"
            "assert (not_center['neighbourhood'] != 'center').all()\n"
            "assert len(not_center) + len(center) == len(df)\n"
            "print('not center:', len(not_center))"
        ),
        md(
            "## 5. Сортировка и топ-N\n\n"
            "Три самые дорогие объявления по `price` — только `listing_id` и `price`.\n\n"
            "**How:** `sort_values(..., ascending=False).head(3)`."
        ),
        code(
            "top3 = None\n"
            "assert top3 is not None\n"
            "assert len(top3) == 3\n"
            "assert top3['price'].is_monotonic_decreasing\n"
            "print(top3[['listing_id', 'price']])"
        ),
        md(
            "## 6. Доля фильтра\n\n"
            "Доля объявлений `neighbourhood == 'center'` среди всех (0–1, округлить до 3 знаков).\n\n"
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
            "Возьмите **первую строку** `center` через `.iloc[0]` и запишите её `listing_id`.\n\n"
            "**Pitfall:** `center.loc[0]` часто падает — метки 0 может не быть."
        ),
        code(
            "first_center_id = None  # str listing_id\n"
            "assert first_center_id is not None\n"
            "assert isinstance(first_center_id, str) and first_center_id.startswith('L')\n"
            "print(first_center_id)"
        ),
        md(
            "## 8. Тип number_of_reviews\n\n"
            "Приведите `number_of_reviews` к `int`, проверьте, что значения ≥ 0. "
            "Число отзывов — **счётчик**, не доля и не цена."
        ),
        code(
            "reviews = None  # df['number_of_reviews'].astype(int)\n"
            "assert reviews is not None\n"
            "assert reviews.dtype.kind in 'iu'\n"
            "assert reviews.min() >= 0\n"
            "print(int(reviews.min()), int(reviews.max()))"
        ),
    )
    hw = nb(
        md("# ДЗ: фильтры"),
        code(LOAD_DATA),
        md("### A. Закрепление"),
        md("## 1. Entire\n\nТолько `room_type == 'entire'` — число строк."),
        code(
            "n_entire = None\n"
            "assert n_entire is not None\n"
            "assert isinstance(n_entire, (int, float))\n"
            "assert 0 < n_entire < len(df)\n"
            "print(n_entire)"
        ),
        md("## 2. Отзывы 10–50\n\n`number_of_reviews` от 10 до 50 включительно — число строк."),
        code(
            "n_mid_reviews = None\n"
            "assert n_mid_reviews is not None\n"
            "assert isinstance(n_mid_reviews, (int, float))\n"
            "assert 0 < n_mid_reviews < len(df)\n"
            "print(n_mid_reviews)"
        ),
        md("## 3. Топ-5\n\n5 самых дорогих по `price` (`listing_id`, `price`)."),
        code(
            "top5 = None\n"
            "assert top5 is not None\n"
            "assert len(top5) == 5\n"
            "assert top5['price'].is_monotonic_decreasing\n"
            "print(top5[['listing_id', 'price']])"
        ),
        md(
            "### B. Вызов\n\n"
            "## 4. Доля center\n\n"
            "Доля объявлений `neighbourhood == 'center'` среди всех (0–1, округлить до 3 знаков). "
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
            "## 5. Не entire\n\n"
            "Число строк, где `room_type` **не** `'entire'` (через `~` или `!=`). "
            "Проверьте: сумма с `n_entire` равна `len(df)`."
        ),
        code(
            "n_not_entire = None\n"
            "assert n_not_entire is not None\n"
            "assert isinstance(n_not_entire, (int, float))\n"
            "assert 0 < n_not_entire < len(df)\n"
            "print(n_not_entire)"
        ),
    )
    sol = nb(
        md("# Решения: фильтры\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        md("## Урок. 1. Фильтр center"),
        code(
            "center = df[df['neighbourhood'] == 'center']\n"
            "print('center:', len(center), 'из', len(df))"
        ),
        md("## Урок. 2. Вместительные объявления"),
        code(
            "large_listings = df[df['accommodates'] >= 6]\n"
            "print(large_listings[['listing_id', 'accommodates', 'price']].head())"
        ),
        md("## Урок. 3. Составная маска"),
        code(
            "center_long = df[(df['neighbourhood'] == 'center') & (df['accommodates'] >= 4)]\n"
            "print(len(center_long))"
        ),
        md("## Урок. 4. Отрицание ~"),
        code(
            "not_center = df[~(df['neighbourhood'] == 'center')]\n"
            "assert len(not_center) + len(center) == len(df)\n"
            "print('not center:', len(not_center))"
        ),
        md("## Урок. 5. Топ-3"),
        code(
            "top3 = df.sort_values('price', ascending=False).head(3)\n"
            "print(top3[['listing_id', 'price']])"
        ),
        md("## Урок. 6. Доля center"),
        code(
            "share_center = round(len(center) / len(df), 3)\n"
            "print('доля center:', share_center)"
        ),
        md("## Урок. 7. loc vs iloc после фильтра"),
        code(
            "first_center_id = str(center.iloc[0]['listing_id'])\n"
            "print(first_center_id)"
        ),
        md("## Урок. 8. Тип number_of_reviews"),
        code(
            "reviews = df['number_of_reviews'].astype(int)\n"
            "print(int(reviews.min()), int(reviews.max()))"
        ),
        md("## ДЗ. 1. Entire"),
        code(
            "n_entire = int((df['room_type'] == 'entire').sum())\n"
            "print(n_entire)"
        ),
        md("## ДЗ. 2. Отзывы 10–50"),
        code(
            "n_mid_reviews = int(((df['number_of_reviews'] >= 7) & (df['number_of_reviews'] <= 9)).sum())\n"
            "print(n_mid_reviews)"
        ),
        md("## ДЗ. 3. Топ-5"),
        code(
            "top5 = df.sort_values('price', ascending=False).head(5)\n"
            "print(top5[['listing_id', 'price']])"
        ),
        md("## ДЗ. 4. Доля center"),
        code(
            "share_center = round((df['neighbourhood'] == 'center').mean(), 3)\n"
            "SHARE_NOTE = f'center ≈ {share_center:.0%} объявлений — ориентир доли центра'\n"
            "print(share_center, SHARE_NOTE)"
        ),
        md("## ДЗ. 5. Не entire"),
        code(
            "n_not_entire = int((df['room_type'] != 'entire').sum())\n"
            "print(n_not_entire)"
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
            "Описательная статистика для `accommodates` и `price`.\n\n"
            "**How читать:** `mean` — среднее; `50%` — медиана; `min`/`max` — хвосты; "
            "`std` — разброс.\n\n"
            "Запишите mean цены в `mean_price` (без подсказки формулы в assert)."
        ),
        code(
            "stats = None  # df[['accommodates', 'price']].describe()\n"
            "# print(stats)\n"
            "mean_price = None\n"
            "assert stats is not None\n"
            "assert mean_price is not None\n"
            "assert isinstance(mean_price, (int, float)) and mean_price > 0\n"
            "print('mean price:', mean_price)"
        ),
        md(
            "## 2. mean vs median\n\n"
            "Сравните mean и median для `price`. "
            "Если mean заметно больше median — правый хвост (вместительные объявления тянут среднее).\n\n"
            "Запишите обе величины и короткий вывод в `MEAN_MEDIAN_NOTE`."
        ),
        code(
            "median_price = None\n"
            "MEAN_MEDIAN_NOTE = ''\n"
            "assert median_price is not None\n"
            "assert isinstance(median_price, (int, float)) and median_price > 0\n"
            "assert len(MEAN_MEDIAN_NOTE) > 15\n"
            "print(mean_price, median_price, MEAN_MEDIAN_NOTE)"
        ),
        md(
            "## 3. info и пропуски\n\n"
            "Вызовите `df.info()`. Сколько **ненулевых** значений в `price`? "
            "Если меньше числа строк — есть пропуски."
        ),
        code(
            "# df.info()\n"
            "n_non_null_price = None\n"
            "assert n_non_null_price is not None\n"
            "assert isinstance(n_non_null_price, (int, float))\n"
            "assert n_non_null_price == len(df) or n_non_null_price < len(df)\n"
            "print('non-null price:', n_non_null_price, '/', len(df))"
        ),
        md(
            "## 4. Scatter: подписи и ловушки\n\n"
            "Scatter `accommodates` → `price`.\n\n"
            "**Pitfalls:**\n"
            "- без `xlabel`/`ylabel`/`title` график «немой»;\n"
            "- при тысячах точек облако заливает — `alpha=0.4…0.6`;\n"
            "- оси перепутаны → ложный вывод о связи.\n\n"
            "Допишите подписи, затем `SCATTER_DONE = True`."
        ),
        code(
            "plt.figure(figsize=(6, 4))\n"
            "plt.scatter(df['accommodates'], df['price'], alpha=0.5)\n"
            "# plt.xlabel(...); plt.ylabel(...); plt.title(...)\n"
            "plt.show()\n"
            "SCATTER_DONE = False\n"
            "assert SCATTER_DONE"
        ),
        md(
            "## 5. Что видно на графике\n\n"
            "Одно–два предложения: есть ли **положительная** связь вместимость → цена? "
            "Есть ли **разброс** (точки далеко от воображаемой линии)?"
        ),
        code(
            "EDA_CONCLUSION = ''\n"
            "assert len(EDA_CONCLUSION) > 20\n"
            "print(EDA_CONCLUSION)"
        ),
        md(
            "## 6. number_of_reviews — другой признак\n\n"
            "Медиана `number_of_reviews` и scatter `number_of_reviews` → `price` (с подписями). "
            "Сравните с accommodates: облако плотнее или размытее?"
        ),
        code(
            "median_reviews = None\n"
            "assert median_reviews is not None\n"
            "assert 0 <= float(median_reviews) <= 23\n"
            "plt.figure(figsize=(6, 4))\n"
            "plt.scatter(df['number_of_reviews'], df['price'], alpha=0.4)\n"
            "plt.xlabel('number_of_reviews')\n"
            "plt.ylabel('price')\n"
            "plt.title('Цена vs отзывы')\n"
            "plt.show()\n"
            "print('median reviews:', median_reviews)"
        ),
        md(
            "## 7. Корреляция — число, не доказательство\n\n"
            "`corr_acc` — корреляция Пирсона между `accommodates` и `price`.\n\n"
            "**Важно:** corr близко к 1 говорит о **линейной** согласованности на этих данных, "
            "но **не доказывает** причинность («далеко → долго из‑за X»). "
            "Запишите число и фразу-ограничение в `CORR_NOTE`."
        ),
        code(
            "corr_acc = None\n"
            "CORR_NOTE = ''\n"
            "assert corr_acc is not None\n"
            "assert -1 <= float(corr_acc) <= 1\n"
            "assert len(CORR_NOTE) > 20\n"
            "print('corr(accommodates, price):', round(float(corr_acc), 3))\n"
            "print(CORR_NOTE)"
        ),
        md(
            "## 8. Checkpoint: какой признак в модель\n\n"
            "По describe + scatter: какой признак перспективнее для **линейной** модели "
            "как первый кандидат — `accommodates` или `number_of_reviews`? Почему (2 предложения)?"
        ),
        code(
            "BETTER_FOR_LINEAR = ''  # 'accommodates' или 'number_of_reviews'\n"
            "WHY_EDA = ''\n"
            "assert BETTER_FOR_LINEAR in ('accommodates', 'number_of_reviews')\n"
            "assert len(WHY_EDA) > 30\n"
            "print(BETTER_FOR_LINEAR, WHY_EDA)"
        ),
    )
    hw = nb(
        md("# ДЗ: EDA"),
        code(LOAD_DATA + IMPORTS_MPL),
        md("### A. Закрепление"),
        md("## 1. describe number_of_reviews\n\n`describe()` для `number_of_reviews`. Запишите медиану в `median_reviews`."),
        code(
            "median_reviews = None\n"
            "assert median_reviews is not None\n"
            "assert 0 <= float(median_reviews) <= 23\n"
            "print(median_reviews)"
        ),
        md("## 2. Scatter number_of_reviews\n\nScatter `number_of_reviews` → `price` с подписями осей и заголовком."),
        code(
            "plt.figure(figsize=(6, 4))\n"
            "# ваш scatter + подписи\n"
            "plt.show()\n"
            "REVIEWS_SCATTER_DONE = False\n"
            "assert REVIEWS_SCATTER_DONE"
        ),
        md("## 3. max accommodates\n\n`listing_id` объявления с максимальным `accommodates`."),
        code(
            "max_acc_id = None\n"
            "assert max_acc_id is not None\n"
            "assert isinstance(max_acc_id, str) and str(max_acc_id).startswith('L')\n"
            "print(max_acc_id)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 4. Сравнение scatter\n\n"
            "Сравните визуально accommodates→price и number_of_reviews→price. "
            "Какой признак перспективнее для **линейной** модели? Почему (2 предложения)?"
        ),
        code(
            "BETTER_FOR_LINEAR = ''  # 'accommodates' или 'number_of_reviews'\n"
            "WHY_VISUAL = ''\n"
            "assert BETTER_FOR_LINEAR in ('accommodates', 'number_of_reviews')\n"
            "assert len(WHY_VISUAL) > 30\n"
            "print(BETTER_FOR_LINEAR, WHY_VISUAL)"
        ),
        md(
            "## 5. corr number_of_reviews\n\n"
            "Корреляция `number_of_reviews` и `price` (число от −1 до 1) + одна фраза: "
            "меньше по модулю, чем у accommodates — что это значит для линейной модели?"
        ),
        code(
            "corr_reviews = None\n"
            "CORR_HOUR_NOTE = ''\n"
            "assert corr_reviews is not None\n"
            "assert -1 <= float(corr_reviews) <= 1\n"
            "assert len(CORR_HOUR_NOTE) > 15\n"
            "print(round(float(corr_reviews), 3), CORR_HOUR_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: EDA\n\n" + SOL_BANNER),
        code(LOAD_DATA + IMPORTS_MPL),
        md("## Урок. 1. describe"),
        code(
            "stats = df[['accommodates', 'price']].describe()\n"
            "print(stats)\n"
            "mean_price = float(df['price'].mean())\n"
            "print('mean price:', mean_price)"
        ),
        md("## Урок. 2. mean vs median"),
        code(
            "median_price = float(df['price'].median())\n"
            "MEAN_MEDIAN_NOTE = (\n"
            "    'Сравните mean и median: если mean выше — длинный хвост цен тянет среднее.'\n"
            ")\n"
            "print(mean_price, median_price, MEAN_MEDIAN_NOTE)"
        ),
        md("## Урок. 3. info"),
        code(
            "n_non_null_price = int(df['price'].notna().sum())\n"
            "print('non-null price:', n_non_null_price, '/', len(df))"
        ),
        md("## Урок. 4. Scatter accommodates"),
        code(
            "plt.figure(figsize=(6, 4))\n"
            "plt.scatter(df['accommodates'], df['price'], alpha=0.5)\n"
            "plt.xlabel('accommodates')\n"
            "plt.ylabel('price')\n"
            "plt.title('Цена vs вместимость')\n"
            "plt.show()\n"
            "SCATTER_DONE = True"
        ),
        md("## Урок. 5. Вывод EDA"),
        code(
            "EDA_CONCLUSION = (\n"
            "    'С ростом accommodates цена в среднем растёт, но разброс заметный.'\n"
            ")\n"
            "print(EDA_CONCLUSION)"
        ),
        md("## Урок. 6. number_of_reviews scatter"),
        code(
            "median_reviews = float(df['number_of_reviews'].median())\n"
            "plt.figure(figsize=(6, 4))\n"
            "plt.scatter(df['number_of_reviews'], df['price'], alpha=0.4)\n"
            "plt.xlabel('number_of_reviews')\n"
            "plt.ylabel('price')\n"
            "plt.title('Цена vs отзывы')\n"
            "plt.show()\n"
            "print('median reviews:', median_reviews)"
        ),
        md("## Урок. 7. Корреляция"),
        code(
            "corr_acc = float(df['accommodates'].corr(df['price']))\n"
            "CORR_NOTE = (\n"
            "    'corr — мера линейной согласованности на этих данных, не доказательство причины.'\n"
            ")\n"
            "print('corr(accommodates, price):', round(corr_acc, 3))\n"
            "print(CORR_NOTE)"
        ),
        md("## Урок. 8. Checkpoint признак"),
        code(
            "BETTER_FOR_LINEAR = 'accommodates'\n"
            "WHY_EDA = (\n"
            "    'На scatter с accommodates видна наклонная полоса; у number_of_reviews облако более размытое. '\n"
            "    'Линейная модель на accommodates — первый кандидат.'\n"
            ")\n"
            "print(BETTER_FOR_LINEAR, WHY_EDA)"
        ),
        md("## ДЗ. 1. number_of_reviews describe"),
        code(
            "median_reviews = float(df['number_of_reviews'].median())\n"
            "print(median_reviews)"
        ),
        md("## ДЗ. 2. Scatter number_of_reviews"),
        code(
            "plt.figure(figsize=(6, 4))\n"
            "plt.scatter(df['number_of_reviews'], df['price'], alpha=0.4)\n"
            "plt.xlabel('number_of_reviews')\n"
            "plt.ylabel('price')\n"
            "plt.title('Цена vs отзывы')\n"
            "plt.show()\n"
            "REVIEWS_SCATTER_DONE = True"
        ),
        md("## ДЗ. 3. max accommodates"),
        code(
            "max_acc_id = str(df.loc[df['accommodates'].idxmax(), 'listing_id'])\n"
            "print(max_acc_id)"
        ),
        md("## ДЗ. 4. Сравнение признаков"),
        code(
            "BETTER_FOR_LINEAR = 'accommodates'\n"
            "WHY_VISUAL = (\n"
            "    'На scatter с accommodates видна наклонная полоса; у number_of_reviews облако более размытое. '\n"
            "    'Линейная модель на accommodates выглядит уместнее как первый кандидат.'\n"
            ")\n"
            "print(BETTER_FOR_LINEAR, WHY_VISUAL)"
        ),
        md("## ДЗ. 5. corr number_of_reviews"),
        code(
            "corr_reviews = float(df['number_of_reviews'].corr(df['price']))\n"
            "CORR_HOUR_NOTE = 'Слабее линейная связь с price — number_of_reviews хуже как единственный признак'\n"
            "print(round(corr_reviews, 3), CORR_HOUR_NOTE)"
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
            "**How в словах:** test — объявления, которых не было в `fit`. "
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
            "Соберите `X` как DataFrame из одного столбца `accommodates` и `y` — Series `price`. "
            "Важно: двойные скобки у X (`df[['accommodates']]`)."
        ),
        code(
            "X = None\n"
            "y = None\n"
            "assert X is not None and y is not None\n"
            "assert list(X.columns) == ['accommodates']\n"
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
            "assert X2 is not None and list(X2.columns) == ['accommodates']\n"
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
            "X = df[['accommodates']]\n"
            "y = df['price']\n"
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
            "## 3. Модель на number_of_reviews\n\n"
            "Обучите модель на `number_of_reviews` (тот же split 0.2 / 42). "
            "Выведите `coef_`. Одной фразой: знак коэффициента ожидаем?"
        ),
        code(
            "coef_reviews = None  # число или массив coef_\n"
            "COEF_NOTE = ''\n"
            "assert coef_reviews is not None\n"
            "assert len(COEF_NOTE) > 10\n"
            "print(coef_reviews, COEF_NOTE)"
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
            "    'Test — отложенные объявления, которых не было в fit.'\n"
            ")\n"
            "print(LEAKAGE_NOTE)"
        ),
        md("## Урок. 2. X и y"),
        code(
            "X = df[['accommodates']]\n"
            "y = df['price']\n"
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
            "X2 = df[['accommodates']]\n"
            "y2 = df['price']\n"
            "Xtr, Xte, ytr, yte = train_test_split(X2, y2, test_size=0.2, random_state=42)\n"
            "model2 = LinearRegression().fit(Xtr, ytr)\n"
            "pred2 = model2.predict(Xte)\n"
            "print('pipeline ok', len(Xtr), len(Xte), model2.coef_)"
        ),
        md("## Урок. 7. Checkpoint"),
        code(
            "NO_FIT_ALL_NOTE = (\n"
            "    'Ошибка на тех же строках, где был fit, не показывает обобщение на новые объявления.'\n"
            ")\n"
            "print(NO_FIT_ALL_NOTE)"
        ),
        md("## ДЗ. 1. test_size=0.3"),
        code(
            "X = df[['accommodates']]\n"
            "y = df['price']\n"
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
        md("## ДЗ. 3. coef number_of_reviews"),
        code(
            "Xh = df[['number_of_reviews']]\n"
            "Xtr, Xte, ytr, yte = train_test_split(Xh, y, test_size=0.2, random_state=42)\n"
            "coef_reviews = LinearRegression().fit(Xtr, ytr).coef_\n"
            "COEF_NOTE = 'Знак coef зависит от данных; на паре важнее зафиксировать seed и размер test'\n"
            "print(coef_reviews, COEF_NOTE)"
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
            "X = `accommodates`, y = `price`. Split 0.2 / seed 42, "
            "обучите `LinearRegression`, получите `y_pred` на test.\n\n"
            "**How:** тот же конвейер, что на паре 12."
        ),
        code(
            "X = None\n"
            "y = None\n"
            "X_train = X_test = y_train = y_test = None\n"
            "model = None\n"
            "y_pred = None\n"
            "assert X is not None and y is not None\n"
            "assert list(X.columns) == ['accommodates']\n"
            "assert X_test is not None\n"
            "assert len(X_test) == int(0.2 * len(df))\n"
            "assert model is not None and y_pred is not None\n"
            "assert len(y_pred) == len(y_test)\n"
            "print(len(X_train), len(X_test))"
        ),
        md(
            "## 2. MSE — интуиция\n\n"
            "Среднеквадратичная ошибка на **test**: штрафует крупные промахи сильнее "
            "(квадрат разности). Единицы — «квадрат цены», не цена за ночь.\n\n"
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
            "Повторите split/fit (0.2 / 42) на `accommodates`. "
            "Средняя абсолютная ошибка на test (как MAE из модуля 1)."
        ),
        code(
            "X = df[['accommodates']]\n"
            "y = df['price']\n"
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
            "X = df[['accommodates']]\n"
            "y = df['price']\n"
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
            "    'На test ошибка важнее: так мы оцениваем обобщение на новые объявления'\n"
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
            "    f'MSE={mse:.1f} — масштаб ошибки в (цена)²; R²≈{r2:.2f} — доля объяснённого разброса. '\n"
            "    f'Модель бьёт baseline (R² baseline≈{r2_baseline:.2f}).'\n"
            ")\n"
            "print(METRIC_NOTE)"
        ),
        md("## ДЗ. 1. MAE"),
        code(
            "X = df[['accommodates']]\n"
            "y = df['price']\n"
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
            "    'На test ошибка важнее: так мы оцениваем обобщение на новые объявления, не заучивание train'\n"
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
        "def load_listings(path: Path) -> pd.DataFrame:\n"
        "    \"\"\"Загрузить CSV; при отсутствии файла — FileNotFoundError с понятным текстом.\"\"\"\n"
        "    pass\n\n\n"
        "def clean_listings(raw: pd.DataFrame) -> pd.DataFrame:\n"
        "    \"\"\"Удалить строки без accommodates или price.\"\"\"\n"
        "    pass\n\n\n"
        "def assert_usable(frame: pd.DataFrame) -> None:\n"
        "    \"\"\"Проверить: непустой df и есть столбцы accommodates, price.\"\"\"\n"
        "    pass\n"
    )
    impl = (
        "def load_listings(path: Path) -> pd.DataFrame:\n"
        "    try:\n"
        "        return pd.read_csv(path)\n"
        "    except FileNotFoundError as e:\n"
        "        raise FileNotFoundError(\n"
        "            f'Файл не найден: {path}. Положите listings.csv рядом с ноутбуком.'\n"
        "        ) from e\n\n\n"
        "def clean_listings(raw: pd.DataFrame) -> pd.DataFrame:\n"
        "    return raw.dropna(subset=['accommodates', 'price']).copy()\n\n\n"
        "def assert_usable(frame: pd.DataFrame) -> None:\n"
        "    if len(frame) == 0:\n"
        "        raise ValueError('пустой DataFrame после очистки')\n"
        "    for col in ('accommodates', 'price'):\n"
        "        if col not in frame.columns:\n"
        "            raise ValueError(f'нет столбца {col}')\n"
    )
    path_finder = (
        "LISTINGS_PATH = None\n"
        "for p in (Path('listings.csv'), Path('../../data/listings.csv'), Path('../data/listings.csv')):\n"
        "    if p.exists():\n"
        "        LISTINGS_PATH = p.resolve()\n"
        "        break\n"
        "assert LISTINGS_PATH is not None\n"
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
            "Реализуйте `load_listings` и загрузите существующий `listings.csv`.\n\n"
            "**How:** `try` вокруг `pd.read_csv`; при успехе вернуть DataFrame."
        ),
        code(
            path_finder
            + "df = load_listings(LISTINGS_PATH)\n"
            "assert isinstance(df, pd.DataFrame)\n"
            "assert len(df) > 0\n"
            "print(df.shape)"
        ),
        md(
            "## 2. Ошибка пути\n\n"
            "Вызовите `load_listings` на несуществующем пути и поймайте `FileNotFoundError`.\n\n"
            "**Pitfall:** голое `except:` глотает SyntaxError — ловите конкретный тип. "
            "В сообщении должны быть путь и подсказка."
        ),
        code(
            "caught = False\n"
            "try:\n"
            "    load_listings(Path('no_such_file.csv'))\n"
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
            "`clean_listings`: удалить строки без `accommodates` или `price` "
            "(`dropna(subset=...)`). Проверка: одна NaN в price → на одну строку меньше."
        ),
        code(
            "raw = df.copy()\n"
            "raw.loc[raw.index[0], 'price'] = None\n"
            "cleaned = clean_listings(raw)\n"
            "assert len(cleaned) == len(raw) - 1\n"
            "print(len(raw), len(cleaned))"
        ),
        md(
            "## 4. assert_usable\n\n"
            "Пустой df и df без `price` должны давать `ValueError`. "
            "Поймайте оба случая и напечатайте сообщение."
        ),
        code(
            "empty = pd.DataFrame(columns=['accommodates', 'price'])\n"
            "try:\n"
            "    assert_usable(empty)\n"
            "    empty_ok = False\n"
            "except ValueError as e:\n"
            "    empty_ok = True\n"
            "    print('empty:', e)\n"
            "bad = pd.DataFrame({'accommodates': [1.0, 2.0], 'number_of_reviews': [8, 9]})\n"
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
            "`load_listings` → `clean_listings` → `assert_usable`. Выведите shape итога."
        ),
        code(
            "pipeline_df = clean_listings(load_listings(LISTINGS_PATH))\n"
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
        md("## 2. Успешный путь\n\n`safe_load(LISTINGS_PATH)` — непустой DataFrame."),
        code(
            "ok = safe_load(LISTINGS_PATH)\n"
            "assert ok is not None and len(ok) > 0\n"
            "print(ok.shape)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. neighbourhood NaN\n\n"
            "`clean_listings` не должен удалять строку только из‑за NaN в `neighbourhood`, "
            "если accommodates и price заполнены."
        ),
        code(
            "# допишите clean_listings выше\n"
            "sample = pd.DataFrame({\n"
            "    'accommodates': [1.0, 2.0],\n"
            "    'price': [10.0, 20.0],\n"
            "    'neighbourhood': [None, 'center'],\n"
            "})\n"
            "out = clean_listings(sample)\n"
            "assert len(out) == 2\n"
            "print(out)"
        ),
        md(
            "## 4. Пустой после clean\n\n"
            "Одна строка с NaN в price → после clean длина 0. "
            "Запишите статус `'empty after clean'` или `'ok'`."
        ),
        code(
            "tiny = pd.DataFrame({'accommodates': [1.0], 'price': [None]})\n"
            "cleaned = clean_listings(tiny)\n"
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
            + "df = load_listings(LISTINGS_PATH)\n"
            "print(df.shape)"
        ),
        md("## Урок. 2. Ошибка пути"),
        code(
            "caught = False\n"
            "try:\n"
            "    load_listings(Path('no_such_file.csv'))\n"
            "except FileNotFoundError as e:\n"
            "    caught = True\n"
            "    print('Поймали:', e)\n"
            "assert caught\n"
            "ERROR_MSG_NOTE = (\n"
            "    'Сообщение должно содержать путь и подсказку: '\n"
            "    'положите listings.csv рядом с ноутбуком'\n"
            ")\n"
            "print(ERROR_MSG_NOTE)"
        ),
        md("## Урок. 3. Очистка"),
        code(
            "raw = df.copy()\n"
            "raw.loc[raw.index[0], 'price'] = None\n"
            "cleaned = clean_listings(raw)\n"
            "assert len(cleaned) == len(raw) - 1\n"
            "print(len(raw), len(cleaned))"
        ),
        md("## Урок. 4. assert_usable"),
        code(
            "empty = pd.DataFrame(columns=['accommodates', 'price'])\n"
            "try:\n"
            "    assert_usable(empty)\n"
            "except ValueError as e:\n"
            "    print('empty:', e)\n"
            "bad = pd.DataFrame({'accommodates': [1.0, 2.0], 'number_of_reviews': [8, 9]})\n"
            "try:\n"
            "    assert_usable(bad)\n"
            "except ValueError as e:\n"
            "    print('bad cols:', e)"
        ),
        md("## Урок. 5. Pipeline"),
        code(
            "pipeline_df = clean_listings(load_listings(LISTINGS_PATH))\n"
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
            "ok = safe_load(LISTINGS_PATH)\n"
            "assert ok is not None and len(ok) > 0\n"
            "print(ok.shape)"
        ),
        md("## ДЗ. 3. neighbourhood NaN"),
        code(
            "sample = pd.DataFrame({\n"
            "    'accommodates': [1.0, 2.0],\n"
            "    'price': [10.0, 20.0],\n"
            "    'neighbourhood': [None, 'center'],\n"
            "})\n"
            "print(clean_listings(sample))"
        ),
        md("## ДЗ. 4. Пустой после clean"),
        code(
            "tiny = pd.DataFrame({'accommodates': [1.0], 'price': [None]})\n"
            "cleaned = clean_listings(tiny)\n"
            "status = 'empty after clean' if len(cleaned) == 0 else 'ok'\n"
            "print(status)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson07() -> None:
    """Pair 15: compare features + brief multi-feature overview."""
    base = "lessons/07_practice_features"
    fit_stub = (
        "def eval_feature(feature_name: str, random_state: int = 42):\n"
        "    \"\"\"Вернуть (mse, r2) LinearRegression на одном признаке, test 20%, seed.\"\"\"\n"
        "    pass\n"
    )
    lesson = nb(
        md(
            "# Практика: сравнение признаков (+ обзор multi)\n\n"
            "Один pipeline — два кандидата (`accommodates`, `number_of_reviews`). "
            "В конце пары — короткий обзор: два столбца в одной модели."
        ),
        code(LOAD_DATA + IMPORTS_SKLEARN + fit_stub),
        md(
            "## 1. Контракт `eval_feature`\n\n"
            "Внутри: `X = df[[feature_name]]`, `y = price`, "
            "`train_test_split(..., test_size=0.2, random_state=...)`, "
            "`LinearRegression().fit`, вернуть `(mse, r2)` на test.\n\n"
            "**Why функция:** иначе легко сменить seed между признаками."
        ),
        code(
            "# допишите тело eval_feature выше\n"
            "assert callable(eval_feature)\n"
            "print('eval_feature готов к проверке')"
        ),
        md("## 2. Метрики accommodates\n\nПроверка: оба числа конечные, MSE ≥ 0."),
        code(
            "mse_d, r2_d = eval_feature('accommodates')\n"
            "assert mse_d >= 0\n"
            "assert r2_d == r2_d  # not NaN\n"
            "print('accommodates', round(mse_d, 2), round(r2_d, 3))"
        ),
        md(
            "## 3. Метрики number_of_reviews\n\n"
            "Те же метрики для `number_of_reviews` (тот же seed внутри функции)."
        ),
        code(
            "mse_r, r2_r = eval_feature('number_of_reviews')\n"
            "assert mse_r >= 0\n"
            "print('number_of_reviews', round(mse_r, 2), round(r2_r, 3))"
        ),
        md(
            "## 4. Таблица сравнения\n\n"
            "DataFrame со столбцами `feature`, `mse`, `r2` для обоих признаков."
        ),
        code(
            "compare_table = None  # DataFrame\n"
            "assert compare_table is not None\n"
            "assert list(compare_table.columns) == ['feature', 'mse', 'r2']\n"
            "assert set(compare_table['feature']) == {'accommodates', 'number_of_reviews'}\n"
            "print(compare_table)"
        ),
        md("## 5. Выбор для отчёта\n\nЛучший признак по R² на test → `BETTER_FEATURE`."),
        code(
            "BETTER_FEATURE = ''\n"
            "assert BETTER_FEATURE in ('accommodates', 'number_of_reviews')\n"
            "assert BETTER_FEATURE == ('accommodates' if r2_d >= r2_r else 'number_of_reviews')\n"
            "print(BETTER_FEATURE)"
        ),
        md(
            "## 6. Обоснование\n\n"
            "2 предложения в `WHY`: числа R² + почему этот признак в отчёт."
        ),
        code(
            "WHY = ''\n"
            "assert len(WHY) > 40\n"
            "print(BETTER_FEATURE, WHY)"
        ),
        md(
            "## 7. Обзор: два признака сразу\n\n"
            "`X = df[['accommodates', 'number_of_reviews']]`, тот же seed 42 / test 0.2. "
            "Сохраните `r2_two` и `two_better` (`r2_two > r2_one`, где `r2_one` — только accommodates). "
            "На этих данных `two_better` может быть **False** — это нормально."
        ),
        code(
            "r2_one = None\n"
            "r2_two = None\n"
            "two_better = None  # True/False\n"
            "assert r2_one is not None and r2_two is not None\n"
            "assert two_better == (r2_two > r2_one)\n"
            "print('one', round(float(r2_one), 3), 'two', round(float(r2_two), 3), 'two_better', two_better)"
        ),
        md(
            "## 8. Checkpoint: больше столбцов ≠ лучше\n\n"
            "`MULTI_NOTE`: зачем пробовать второй признак и почему это не гарантия роста R² на test?"
        ),
        code(
            "MULTI_NOTE = ''\n"
            "assert len(MULTI_NOTE) > 30\n"
            "print(MULTI_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: таблица сравнения + multi"),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("### A. Закрепление"),
        md(
            "## 1. Таблица\n\n"
            "DataFrame `feature` / `mse` / `r2` для `accommodates` и `number_of_reviews`."
        ),
        code(
            "def eval_feature(feature_name: str, random_state: int = 42):\n"
            "    pass\n\n\n"
            "table = None  # DataFrame\n"
            "assert table is not None\n"
            "assert list(table.columns) == ['feature', 'mse', 'r2']\n"
            "assert set(table['feature']) == {'accommodates', 'number_of_reviews'}\n"
            "print(table)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 2. is_entire\n\n"
            "Код `entire→1`, иначе `0` → столбец `is_entire`; `eval_feature('is_entire')`. "
            "Лучше ли accommodates по R²?"
        ),
        code(
            "df = df.copy()\n"
            "df['is_entire'] = (df['room_type'] == 'entire').astype(int)\n"
            "mse_c, r2_c = eval_feature('is_entire')\n"
            "beats_accommodates = None  # True/False\n"
            "assert beats_accommodates in (True, False)\n"
            "print(r2_c, beats_accommodates)"
        ),
        md(
            "## 3. MSE двух признаков\n\n"
            "MSE на test для модели accommodates+number_of_reviews (seed 42, test 0.2) + "
            "одна фраза: когда оставить один признак в сдаче."
        ),
        code(
            "mse_two = None\n"
            "KEEP_ONE_NOTE = ''\n"
            "assert mse_two is not None and mse_two >= 0\n"
            "assert len(KEEP_ONE_NOTE) > 25\n"
            "print(round(float(mse_two), 2), KEEP_ONE_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: сравнение признаков\n\n" + SOL_BANNER),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("## Урок. 1–3. eval_feature"),
        code(
            "def eval_feature(feature_name: str, random_state: int = 42):\n"
            "    X = df[[feature_name]]\n"
            "    y = df['price']\n"
            "    X_tr, X_te, y_tr, y_te = train_test_split(\n"
            "        X, y, test_size=0.2, random_state=random_state\n"
            "    )\n"
            "    pred = LinearRegression().fit(X_tr, y_tr).predict(X_te)\n"
            "    return mean_squared_error(y_te, pred), r2_score(y_te, pred)\n\n\n"
            "mse_d, r2_d = eval_feature('accommodates')\n"
            "mse_r, r2_r = eval_feature('number_of_reviews')\n"
            "print('accommodates', round(mse_d, 2), round(r2_d, 3))\n"
            "print('number_of_reviews', round(mse_r, 2), round(r2_r, 3))"
        ),
        md("## Урок. 4. Таблица"),
        code(
            "compare_table = pd.DataFrame([\n"
            "    {'feature': 'accommodates', 'mse': mse_d, 'r2': r2_d},\n"
            "    {'feature': 'number_of_reviews', 'mse': mse_r, 'r2': r2_r},\n"
            "])\n"
            "print(compare_table)"
        ),
        md("## Урок. 5–6. BETTER_FEATURE / WHY"),
        code(
            "BETTER_FEATURE = 'accommodates' if r2_d >= r2_r else 'number_of_reviews'\n"
            "WHY = (\n"
            "    f'По R² на test лучше {BETTER_FEATURE} '\n"
            "    f'(accommodates R²={r2_d:.3f}, number_of_reviews R²={r2_r:.3f}). '\n"
            "    'Для отчёта фиксируем один признак и те же seed/test_size.'\n"
            ")\n"
            "print(BETTER_FEATURE)\n"
            "print(WHY)"
        ),
        md("## Урок. 7–8. Multi-feature обзор"),
        code(
            "y = df['price']\n"
            "X1 = df[['accommodates']]\n"
            "X2 = df[['accommodates', 'number_of_reviews']]\n"
            "X1_tr, X1_te, y1_tr, y1_te = train_test_split(X1, y, test_size=0.2, random_state=42)\n"
            "X2_tr, X2_te, y2_tr, y2_te = train_test_split(X2, y, test_size=0.2, random_state=42)\n"
            "r2_one = r2_score(y1_te, LinearRegression().fit(X1_tr, y1_tr).predict(X1_te))\n"
            "pred2 = LinearRegression().fit(X2_tr, y2_tr).predict(X2_te)\n"
            "r2_two = r2_score(y2_te, pred2)\n"
            "two_better = r2_two > r2_one\n"
            "MULTI_NOTE = (\n"
            "    'Второй признак стоит пробовать, но решение — по метрике на test: '\n"
            "    'лишний столбец может не помочь или чуть ухудшить R².'\n"
            ")\n"
            "print('one', round(r2_one, 3), 'two', round(r2_two, 3), 'two_better', two_better)\n"
            "print(MULTI_NOTE)"
        ),
        md("## ДЗ. 1. Таблица"),
        code(
            "rows = []\n"
            "for f in ('accommodates', 'number_of_reviews'):\n"
            "    m, r = eval_feature(f)\n"
            "    rows.append({'feature': f, 'mse': m, 'r2': r})\n"
            "table = pd.DataFrame(rows)\n"
            "print(table)"
        ),
        md("## ДЗ. 2. is_entire"),
        code(
            "df2 = df.copy()\n"
            "df2['is_entire'] = (df2['room_type'] == 'entire').astype(int)\n"
            "\n"
            "def eval_feature_df(frame, feature_name: str, random_state: int = 42):\n"
            "    X = frame[[feature_name]]\n"
            "    y = frame['price']\n"
            "    X_tr, X_te, y_tr, y_te = train_test_split(\n"
            "        X, y, test_size=0.2, random_state=random_state\n"
            "    )\n"
            "    pred = LinearRegression().fit(X_tr, y_tr).predict(X_te)\n"
            "    return mean_squared_error(y_te, pred), r2_score(y_te, pred)\n\n\n"
            "mse_c, r2_c = eval_feature_df(df2, 'is_entire')\n"
            "beats_accommodates = r2_c > r2_d\n"
            "print(r2_c, beats_accommodates)"
        ),
        md("## ДЗ. 3. MSE two + KEEP_ONE"),
        code(
            "mse_two = mean_squared_error(y2_te, pred2)\n"
            "KEEP_ONE_NOTE = (\n"
            "    'Если второй признак не улучшает R² на test или усложняет интерпретацию — '\n"
            "    'в сдачу оставляем один столбец.'\n"
            ")\n"
            "print(round(mse_two, 2), KEEP_ONE_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson08() -> None:
    """Pair 16: report draft + submit in one pair."""
    base = "lessons/08_report"
    lesson = nb(
        md(
            "# Мини-отчёт: сборка и сдача\n\n"
            "Одна пара: каркас по PROJECT → числа на test → сравнение признаков → "
            "рекомендация → сдача `report_starter.ipynb`."
        ),
        code(LOAD_DATA + IMPORTS_SKLEARN + IMPORTS_MPL),
        md(
            "## 1. Структура и чек-лист\n\n"
            "Каркас: данные → EDA → модель/метрики на test → сравнение ≥2 признаков → "
            "рекомендация + ограничения → рефлексия.\n\n"
            "Сверьте с PROJECT.md. `STRUCTURE_OK = True`, `CHECKLIST_OK = True`."
        ),
        code(
            "STRUCTURE_OK = False\n"
            "CHECKLIST_OK = False\n"
            "assert STRUCTURE_OK is True and CHECKLIST_OK is True"
        ),
        md(
            "## 2. Данные\n\n"
            "2–3 предложения в `REPORT_DATA`: источник, число строк (`len(df)`), цель `price`."
        ),
        code(
            "REPORT_DATA = ''\n"
            "assert str(len(df)) in REPORT_DATA\n"
            "assert 'price' in REPORT_DATA.lower() or 'цен' in REPORT_DATA.lower()\n"
            "print(REPORT_DATA)"
        ),
        md(
            "## 3. EDA\n\n"
            "`describe` по accommodates/price + краткий вывод в `REPORT_EDA`."
        ),
        code(
            "# print(df[['accommodates', 'price']].describe())\n"
            "REPORT_EDA = ''\n"
            "assert len(REPORT_EDA) > 20\n"
            "print(REPORT_EDA)"
        ),
        md(
            "## 4. Модель и финальные метрики\n\n"
            "Train/test 0.2 / seed 42, LR на `accommodates` → `FINAL_MSE`, `FINAL_R2` на test."
        ),
        code(
            "FINAL_MSE = None\n"
            "FINAL_R2 = None\n"
            "assert FINAL_MSE is not None and FINAL_R2 is not None\n"
            "assert FINAL_MSE >= 0\n"
            "print('MSE', FINAL_MSE, 'R2', FINAL_R2)"
        ),
        md(
            "## 5. Сравнение признаков\n\n"
            "Текст: R² для accommodates и number_of_reviews при том же протоколе (seed 42)."
        ),
        code(
            "FEATURE_COMPARE_NOTE = ''\n"
            "assert 'accommodates' in FEATURE_COMPARE_NOTE.lower()\n"
            "assert 'number_of_reviews' in FEATURE_COMPARE_NOTE.lower() or 'review' in FEATURE_COMPARE_NOTE.lower()\n"
            "assert len(FEATURE_COMPARE_NOTE) > 20\n"
            "print(FEATURE_COMPARE_NOTE)"
        ),
        md(
            "## 6. Рекомендация и ограничения\n\n"
            "`REPORT_RECOMMENDATION` (≥2 предложения с числами) + `LIMITATIONS`."
        ),
        code(
            "REPORT_RECOMMENDATION = ''\n"
            "LIMITATIONS = ''\n"
            "assert len(REPORT_RECOMMENDATION) > 40\n"
            "assert len(LIMITATIONS) > 25\n"
            "print(REPORT_RECOMMENDATION)\n"
            "print(LIMITATIONS)"
        ),
        md(
            "## 7. Рефлексия модуля\n\n"
            "3 предложения: списки модуля 1 → DataFrame → sklearn fit/predict."
        ),
        code(
            "REFLECTION = ''\n"
            "assert len(REFLECTION) > 60\n"
            "print(REFLECTION)"
        ),
        md(
            "## 8. Сдача starter\n\n"
            "Файл сдачи — заполненный `artifact/starter/report_starter.ipynb` "
            "(можно перенести блоки из этого lesson).\n\n"
            "`STARTER_READY = True`; `SUBMIT_NOTE` — что отправляете в Canvas."
        ),
        code(
            "STARTER_READY = False\n"
            "SUBMIT_NOTE = ''\n"
            "assert STARTER_READY is True\n"
            "assert CHECKLIST_OK and FINAL_MSE is not None and FINAL_R2 is not None\n"
            "assert len(SUBMIT_NOTE) > 15\n"
            "print(SUBMIT_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: добить starter к сдаче (если не успели на паре)"),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("### A. Закрепление"),
        md(
            "## 1. Сравнение в тексте\n\n"
            "2 предложения: R² accommodates vs number_of_reviews (seed 42)."
        ),
        code(
            "FEATURE_COMPARE_NOTE = ''\n"
            "assert 'accommodates' in FEATURE_COMPARE_NOTE.lower()\n"
            "assert 'number_of_reviews' in FEATURE_COMPARE_NOTE.lower() or 'review' in FEATURE_COMPARE_NOTE.lower()\n"
            "print(FEATURE_COMPARE_NOTE)"
        ),
        md("### B. Вызов"),
        md(
            "## 2. Рекомендация ≥ 2 предложений\n\n"
            "Заполните `REPORT_RECOMMENDATION` с числами и ограничением."
        ),
        code(
            "REPORT_RECOMMENDATION = ''\n"
            "assert len(REPORT_RECOMMENDATION) > 40\n"
            "print(REPORT_RECOMMENDATION)"
        ),
        md(
            "## 3. Перенос в starter\n\n"
            "`STARTER_READY = True`, когда блоки §1–6 в `report_starter.ipynb` заполнены."
        ),
        code(
            "STARTER_READY = False\n"
            "assert STARTER_READY is True\n"
            "print('starter ready')"
        ),
    )
    sol = nb(
        md("# Решения: мини-отчёт\n\n" + SOL_BANNER),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("## Урок. 1. Структура"),
        code(
            "STRUCTURE_OK = True\n"
            "CHECKLIST_OK = True\n"
            "print(STRUCTURE_OK, CHECKLIST_OK)"
        ),
        md("## Урок. 2–3. Данные и EDA"),
        code(
            "REPORT_DATA = (\n"
            "    f'Источник: {LISTINGS_PATH.name}, строк: {len(df)}. '\n"
            "    'Цель: предсказать price по признакам объявления.'\n"
            ")\n"
            "print(df[['accommodates', 'price']].describe())\n"
            "REPORT_EDA = (\n"
            "    'describe показывает разброс accommodates и price; '\n"
            "    'на scatter accommodates→price видна положительная связь.'\n"
            ")\n"
            "print(REPORT_DATA)\n"
            "print(REPORT_EDA)"
        ),
        md("## Урок. 4–5. Метрики и сравнение"),
        code(
            "y = df['price']\n"
            "\n"
            "def metrics(cols):\n"
            "    X = df[cols]\n"
            "    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            "    pred = LinearRegression().fit(X_tr, y_tr).predict(X_te)\n"
            "    return mean_squared_error(y_te, pred), r2_score(y_te, pred)\n\n\n"
            "FINAL_MSE, FINAL_R2 = metrics(['accommodates'])\n"
            "_, r2_r = metrics(['number_of_reviews'])\n"
            "FEATURE_COMPARE_NOTE = (\n"
            "    f'accommodates R²={FINAL_R2:.3f}, number_of_reviews R²={r2_r:.3f} — выбираем accommodates'\n"
            ")\n"
            "print(FINAL_MSE, FINAL_R2)\n"
            "print(FEATURE_COMPARE_NOTE)"
        ),
        md("## Урок. 6–8. Рекомендация, рефлексия, сдача"),
        code(
            "REPORT_RECOMMENDATION = (\n"
            "    'Рекомендуем accommodates как основной признак: выше R² на test. '\n"
            "    'Ограничение: один признак и линейная модель.'\n"
            ")\n"
            "LIMITATIONS = (\n"
            "    'Линейная модель и сэмпл Porto (Inside Airbnb) не обещают точность на других городах.'\n"
            ")\n"
            "REFLECTION = (\n"
            "    'В модуле 1 predict был функцией на списках. '\n"
            "    'Здесь данные — таблица CSV и DataFrame. '\n"
            "    'sklearn даёт fit/predict и метрики на test вместо ручного коэффициента.'\n"
            ")\n"
            "STARTER_READY = True\n"
            "SUBMIT_NOTE = 'Отправляю заполненный report_starter.ipynb с метриками на test и сравнением признаков'\n"
            "print(REPORT_RECOMMENDATION)\n"
            "print(LIMITATIONS)\n"
            "print(REFLECTION)\n"
            "print(STARTER_READY, SUBMIT_NOTE)"
        ),
        md("## ДЗ. 1–3"),
        code(
            "print(FEATURE_COMPARE_NOTE)\n"
            "print(REPORT_RECOMMENDATION)\n"
            "print(STARTER_READY)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_report_starter() -> None:
    starter = nb(
        md("# Мини-отчёт: краткосрочная аренда «StayLocal»"),
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
        md("## 2. EDA\n\n`describe` и/или scatter для связи признака с `price`."),
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
            "Таблица или два блока: минимум `accommodates` и `number_of_reviews`."
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
    add_report_starter()
    for rel, notebook in NOTEBOOKS.items():
        write(rel, notebook)
    src_csv = ROOT / "data" / "listings.csv"
    if src_csv.exists():
        targets = [ROOT / "artifact" / "starter" / "listings.csv"]
        for lesson_dir in (ROOT / "lessons").iterdir():
            if lesson_dir.is_dir() and not lesson_dir.name.startswith("_"):
                targets.append(lesson_dir / "listings.csv")
        for dst in targets:
            shutil.copy(src_csv, dst)
            print("copied", dst)
    print(f"total notebooks: {len(NOTEBOOKS)}")


if __name__ == "__main__":
    main()
