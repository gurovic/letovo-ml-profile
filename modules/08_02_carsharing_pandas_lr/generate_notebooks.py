#!/usr/bin/env python3
"""Generate lesson notebooks for module 08_02 (pairs 12-21)."""

from __future__ import annotations

import json
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
        md("## 1. Первая таблица\n\nЗагрузите CSV и выведите `shape`, первые 5 строк и список столбцов."),
        code("print('строк, столбцов:', df.shape)\nprint(df.head())\nprint(list(df.columns))"),
        md(
            "## 2. Признак, цель, служебный столбец\n\n"
            "Разделите столбцы на три группы: **цель**, **признаки**, **id**. "
            "Запишите в переменные `TARGET`, `FEATURES`, `ID_COL`."
        ),
        code(
            "TARGET = 'duration_min'\n"
            "FEATURES = ['distance_km', 'hour', 'zone', 'vehicle_type']\n"
            "ID_COL = 'trip_id'\n\n"
            "assert TARGET in df.columns\n"
            "assert ID_COL in df.columns\n"
            "assert set(FEATURES).issubset(df.columns)"
        ),
        md("## 3. Тип object\n\nНайдите столбцы с типом `object`. Почему `distance_km` — не object?"),
        code(
            "object_cols = df.select_dtypes(include='object').columns.tolist()\n"
            "print('object:', object_cols)\n"
            "print(df['distance_km'].dtype)\n"
            "assert 'trip_id' in object_cols"
        ),
    )
    hw = nb(
        md("# ДЗ: осмотр таблицы"),
        code(LOAD_DATA),
        md("## 1. Срез столбцов\n\nВыведите только `distance_km`, `duration_min`, `hour` — первые 10 строк."),
        code("subset = df[['distance_km', 'duration_min', 'hour']]\nprint(subset.head(10))"),
        md("## 2. Одна поездка\n\nНайдите строку с `trip_id == 'T0001'` и выведите длительность."),
        code("row = df[df['trip_id'] == 'T0001']\nassert len(row) == 1\nprint(row['duration_min'].iloc[0])"),
        md("## 3. Сколько поездок\n\nПосчитайте число строк таблицы двумя способами: `len(df)` и `df.shape[0]`."),
        code("assert len(df) == df.shape[0]\nprint(len(df))"),
    )
    sol = nb(
        md("# Решения: pandas DataFrame"),
        code(LOAD_DATA),
        code(
            "TARGET = 'duration_min'\n"
            "FEATURES = ['distance_km', 'hour', 'zone', 'vehicle_type']\n"
            "ID_COL = 'trip_id'\n"
            "object_cols = df.select_dtypes(include='object').columns.tolist()\n"
            "print(df.shape, object_cols)"
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
        md("## 1. Фильтр по зоне\n\nОставьте только поездки с `zone == 'center'`."),
        code("center = df[df['zone'] == 'center']\nassert len(center) > 0\nprint(len(center))"),
        md("## 2. Длинные поездки\n\nСтроки, где `distance_km >= 15`."),
        code("long_trips = df[df['distance_km'] >= 15]\nprint(long_trips[['trip_id', 'distance_km', 'duration_min']].head())"),
        md("## 3. loc vs iloc\n\nПервые 3 строки столбцов `distance_km` и `duration_min` через `.loc` и через `.iloc`."),
        code(
            "by_name = df.loc[:2, ['distance_km', 'duration_min']]\n"
            "by_pos = df.iloc[:3, [1, 2]]\n"
            "print(by_name)\nprint(by_pos)"
        ),
        md("## 4. Тип hour\n\nПриведите `hour` к целому (`astype(int)`) и проверьте min/max."),
        code(
            "hours = df['hour'].astype(int)\n"
            "assert hours.min() >= 0 and hours.max() <= 23\n"
            "print(hours.min(), hours.max())"
        ),
    )
    hw = nb(
        md("# ДЗ: фильтры"),
        code(LOAD_DATA),
        md("## 1. Комфорт\n\nТолько `vehicle_type == 'comfort'`."),
        code("comfort = df[df['vehicle_type'] == 'comfort']\nprint(len(comfort))"),
        md("## 2. Утро\n\nПоездки с `hour` от 7 до 9 включительно."),
        code("morning = df[(df['hour'] >= 7) & (df['hour'] <= 9)]\nprint(len(morning))"),
        md("## 3. Сортировка\n\n5 самых длинных по `duration_min`."),
        code("top5 = df.sort_values('duration_min', ascending=False).head(5)\nprint(top5[['trip_id', 'duration_min']])"),
    )
    sol = nb(md("# Решения: фильтры"), code(LOAD_DATA + "\ncenter = df[df['zone'] == 'center']\nprint(len(center))"))
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson03() -> None:
    base = "lessons/03_eda_scatter"
    lesson = nb(
        md("# EDA: describe и scatter"),
        code(LOAD_DATA + IMPORTS_MPL),
        md("## 1. describe\n\nОписательная статистика для `distance_km` и `duration_min`."),
        code("print(df[['distance_km', 'duration_min']].describe())"),
        md("## 2. info\n\n`df.info()` — сколько пропусков?"),
        code("df.info()"),
        md(
            "## 3. Scatter\n\n"
            "Постройте scatter: ось X — `distance_km`, ось Y — `duration_min`. "
            "Подпишите оси и заголовок."
        ),
        code(
            "plt.figure(figsize=(6, 4))\n"
            "plt.scatter(df['distance_km'], df['duration_min'], alpha=0.5)\n"
            "plt.xlabel('distance_km')\n"
            "plt.ylabel('duration_min')\n"
            "plt.title('Длительность vs расстояние')\n"
            "plt.show()"
        ),
        md("## 4. Вывод\n\nОдно предложение: что видно на графике? (положительная связь / разброс)"),
        code("# Ваш вывод:\nEDA_CONCLUSION = ''  # заполните строкой\n"),
    )
    hw = nb(
        md("# ДЗ: EDA"),
        code(LOAD_DATA + IMPORTS_MPL),
        md("## 1. hour\n\n`describe()` для столбца `hour`."),
        code("print(df['hour'].describe())"),
        md("## 2. Scatter hour\n\nScatter `hour` → `duration_min`."),
        code(
            "plt.scatter(df['hour'], df['duration_min'], alpha=0.4)\n"
            "plt.xlabel('hour')\nplt.ylabel('duration_min')\nplt.show()"
        ),
    )
    sol = nb(md("# Решения: EDA"), code(LOAD_DATA + "\nprint(df[['distance_km', 'duration_min']].describe())"))
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson04() -> None:
    base = "lessons/04_train_test_lr"
    Xy = (
        "FEATURE = 'distance_km'\n"
        "TARGET = 'duration_min'\n"
        "X = df[[FEATURE]]\n"
        "y = df[TARGET]\n"
    )
    split = (
        "X_train, X_test, y_train, y_test = train_test_split(\n"
        "    X, y, test_size=0.2, random_state=42\n"
        ")\n"
        "print(len(X_train), len(X_test))\n"
    )
    lesson = nb(
        md("# train/test и LinearRegression"),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("## 1. Признак и цель\n\nВыделите X (один столбец) и y."),
        code(Xy + "print(X.head(), y.head())"),
        md("## 2. train/test split\n\n20% в test, `random_state=42`."),
        code(split + "assert len(X_test) == int(0.2 * len(df))"),
        md("## 3. fit / predict\n\nОбучите `LinearRegression` на train, предскажите test."),
        code(
            "model = LinearRegression()\n"
            "model.fit(X_train, y_train)\n"
            "y_pred = model.predict(X_test)\n"
            "print('coef', model.coef_, 'intercept', model.intercept_)\n"
            "print('первые 3 предсказания:', y_pred[:3])"
        ),
    )
    hw = nb(
        md("# ДЗ: split"),
        code(LOAD_DATA + IMPORTS_SKLEARN + Xy),
        md("## 1. Другой test_size\n\nПовторите split с `test_size=0.3`, тот же seed. Сколько строк в test?"),
        code(
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)\n"
            "print(len(X_te))"
        ),
    )
    sol = nb(
        md("# Решения: LR"),
        code(LOAD_DATA + IMPORTS_SKLEARN + Xy + split + "model = LinearRegression()\nmodel.fit(X_train, y_train)\nprint(model.predict(X_test)[:3])"),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson05() -> None:
    base = "lessons/05_practice_metrics"
    pipeline = (
        LOAD_DATA + IMPORTS_SKLEARN +
        "X = df[['distance_km']]\ny = df['duration_min']\n"
        "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n"
        "model = LinearRegression().fit(X_train, y_train)\n"
        "y_pred = model.predict(X_test)\n"
    )
    lesson = nb(
        md("# Практика: MSE и R²"),
        code(pipeline),
        md("## 1. MSE\n\nСреднеквадратичная ошибка на **test**."),
        code(
            "mse = mean_squared_error(y_test, y_pred)\n"
            "print('MSE', round(mse, 2))\n"
            "assert mse >= 0"
        ),
        md("## 2. R²\n\nКоэффициент детерминации на test."),
        code(
            "r2 = r2_score(y_test, y_pred)\n"
            "print('R2', round(r2, 3))\n"
            "assert -1 <= r2 <= 1"
        ),
        md("## 3. Таблица сравнения\n\nDataFrame из 5 строк: `y_test`, `y_pred`, `error`."),
        code(
            "compare = pd.DataFrame({'fact': y_test.values, 'pred': y_pred})\n"
            "compare['error'] = compare['fact'] - compare['pred']\n"
            "print(compare.head())"
        ),
        md("## 4. Интерпретация\n\nОдна фраза: модель объясняет долю разброса? (смотрите R²)"),
        code("METRIC_NOTE = ''  # заполните"),
    )
    hw = nb(
        md("# ДЗ: метрики"),
        code(pipeline),
        md("## 1. MAE\n\nСредняя абсолютная ошибка на test (вручную или `mean(abs(...))`)."),
        code("mae = (abs(y_test - y_pred)).mean()\nprint(round(mae, 2))"),
    )
    sol = nb(md("# Решения: метрики"), code(pipeline + "print(mean_squared_error(y_test, y_pred), r2_score(y_test, y_pred))"))
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson06() -> None:
    base = "lessons/06_try_except_csv"
    lesson = nb(
        md("# try/except при загрузке CSV"),
        code(
            "from pathlib import Path\n"
            "import pandas as pd\n\n\n"
            "def load_trips(path: Path) -> pd.DataFrame:\n"
            "    \"\"\"Загрузить CSV; при ошибке вернуть понятное сообщение.\"\"\"\n"
            "    try:\n"
            "        return pd.read_csv(path)\n"
            "    except FileNotFoundError:\n"
            "        raise FileNotFoundError(f'Файл не найден: {path}')\n\n\n"
            "def clean_trips(raw: pd.DataFrame) -> pd.DataFrame:\n"
            "    \"\"\"Удалить строки без distance или duration.\"\"\"\n"
            "    cleaned = raw.dropna(subset=['distance_km', 'duration_min'])\n"
            "    return cleaned\n"
        ),
        md("## 1. Успешная загрузка\n\nВызовите `load_trips` для существующего файла."),
        code(
            LOAD_DATA.split("df = pd.read_csv(TRIPS_PATH)")[0] +
            "df = load_trips(TRIPS_PATH)\nprint(df.shape)"
        ),
        md("## 2. Ошибка пути\n\nПопробуйте несуществующий путь в try/except и выведите сообщение."),
        code(
            "bad = Path('no_such_file.csv')\n"
            "try:\n"
            "    load_trips(bad)\n"
            "except FileNotFoundError as e:\n"
            "    print('Поймали:', e)"
        ),
        md("## 3. Очистка\n\nПримените `clean_trips`; сравните число строк до/после."),
        code(
            "raw = df.copy()\n"
            "raw.loc[0, 'duration_min'] = None\n"
            "cleaned = clean_trips(raw)\n"
            "print(len(raw), len(cleaned))\n"
            "assert len(cleaned) == len(raw) - 1"
        ),
    )
    hw = nb(
        md("# ДЗ: устойчивая загрузка"),
        code("from pathlib import Path\nimport pandas as pd\n"),
        md("## 1. Обёртка\n\nФункция `safe_load(path)` возвращает DataFrame или `None` при FileNotFoundError."),
        code(
            "def safe_load(path):\n"
            "    try:\n"
            "        return pd.read_csv(path)\n"
            "    except FileNotFoundError:\n"
            "        return None\n"
        ),
    )
    sol = nb(md("# Решения: try/except"), code("print('see lesson')"))
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson07() -> None:
    base = "lessons/07_practice_features"
    fit_fn = (
        "def eval_feature(feature_name: str, random_state: int = 42):\n"
        "    X = df[[feature_name]]\n"
        "    y = df['duration_min']\n"
        "    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=random_state)\n"
        "    m = LinearRegression().fit(X_tr, y_tr)\n"
        "    pred = m.predict(X_te)\n"
        "    return mean_squared_error(y_te, pred), r2_score(y_te, pred)\n"
    )
    lesson = nb(
        md("# Практика: сравнение признаков"),
        code(LOAD_DATA + IMPORTS_SKLEARN + fit_fn),
        md("## 1. distance_km\n\nMSE и R² для признака `distance_km`."),
        code("mse_d, r2_d = eval_feature('distance_km')\nprint('distance', mse_d, r2_d)"),
        md("## 2. hour\n\nТе же метрики для `hour`."),
        code("mse_h, r2_h = eval_feature('hour')\nprint('hour', mse_h, r2_h)"),
        md("## 3. Сравнение\n\nКакой признак лучше по R² на test? Запишите имя в `BETTER_FEATURE`."),
        code(
            "BETTER_FEATURE = 'distance_km'  # замените если hour лучше\n"
            "assert BETTER_FEATURE in ('distance_km', 'hour')"
        ),
        md("## 4. Обоснование\n\n2 предложения для «отдела аналитики»."),
        code("WHY = ''  # заполните"),
    )
    hw = nb(
        md("# ДЗ: эксперимент"),
        code(LOAD_DATA + IMPORTS_SKLEARN + fit_fn),
        md("## 1. Таблица\n\nDataFrame с колонками feature, mse, r2 для distance и hour."),
        code(
            "rows = []\n"
            "for f in ('distance_km', 'hour'):\n"
            "    m, r = eval_feature(f)\n"
            "    rows.append({'feature': f, 'mse': m, 'r2': r})\n"
            "print(pd.DataFrame(rows))"
        ),
    )
    sol = nb(md("# Решения: признаки"), code(LOAD_DATA + IMPORTS_SKLEARN + fit_fn + "print(eval_feature('distance_km'))"))
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
            "X = `distance_km` и `hour`. Обучите модель; выведите коэффициенты."
        ),
        code(
            "X = df[['distance_km', 'hour']]\n"
            "y = df['duration_min']\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            "model = LinearRegression().fit(X_tr, y_tr)\n"
            "pred = model.predict(X_te)\n"
            "print('coef', model.coef_, 'intercept', model.intercept_)\n"
            "print('R2', round(r2_score(y_te, pred), 3))"
        ),
        md("## 2. Сравнение с одним признаком\n\nR² двух признаков выше, чем у одного `distance_km`?"),
        code(
            "X1 = df[['distance_km']]\n"
            "X1_tr, X1_te, y1_tr, y1_te = train_test_split(X1, y, test_size=0.2, random_state=42)\n"
            "r2_one = r2_score(y1_te, LinearRegression().fit(X1_tr, y1_tr).predict(X1_te))\n"
            "r2_two = r2_score(y_te, pred)\n"
            "print('one', r2_one, 'two', r2_two)\n"
            "assert r2_two >= r2_one"
        ),
        md("## 3. Когда одного столбца мало\n\nКратко: зачем добавлять второй признак?"),
        code("MULTI_NOTE = ''  # заполните"),
    )
    hw = nb(
        md("# ДЗ: обзор"),
        code(LOAD_DATA + IMPORTS_SKLEARN),
        md("## 1. MSE двух признаков\n\nПосчитайте MSE на test для модели с distance+hour."),
        code("# используйте model и pred с урока или пересчитайте"),
    )
    sol = nb(md("# Решения: multifeature"), code(LOAD_DATA + IMPORTS_SKLEARN))
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
            "2–3 предложения: источник, число строк, цель предсказания."
        ),
        code("REPORT_DATA = f'Таблица {TRIPS_PATH.name}, строк: {len(df)}. Цель: duration_min.'\nprint(REPORT_DATA)"),
        md("## 2. EDA\n\n`describe` + вывод по scatter distance."),
        code("print(df[['distance_km', 'duration_min']].describe())"),
        md("## 3. Модель\n\nTrain/test, LR на лучшем одном признаке (distance_km), метрики test."),
        code(
            "X = df[['distance_km']]\ny = df['duration_min']\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            "model = LinearRegression().fit(X_tr, y_tr)\n"
            "pred = model.predict(X_te)\n"
            "report_mse = mean_squared_error(y_te, pred)\n"
            "report_r2 = r2_score(y_te, pred)\n"
            "print('MSE', report_mse, 'R2', report_r2)"
        ),
        md("## 4. Рекомендация\n\n1 абзац для отдела аналитики: какой признак, качество, ограничения."),
        code("REPORT_RECOMMENDATION = ''  # заполните к паре 20"),
    )
    hw = nb(
        md("# ДЗ: доработать черновик"),
        code(LOAD_DATA),
        md("Добейте разделы 2–4 в ноутбуке или отдельном `report.md`."),
        code("# черновик"),
    )
    sol = nb(md("# Решения: отчёт"), code(LOAD_DATA))
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
            "- [ ] данные описаны\n"
            "- [ ] scatter или describe\n"
            "- [ ] train/test + LR\n"
            "- [ ] MSE и R² на test\n"
            "- [ ] сравнение ≥2 признаков\n"
            "- [ ] рекомендация для аналитиков"
        ),
        code("CHECKLIST_OK = False  # поставьте True когда готово"),
        md("## 2. Финальные метрики\n\nПересчитайте и зафиксируйте MSE/R² для сдачи."),
        code(
            "X = df[['distance_km']]\ny = df['duration_min']\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            "pred = LinearRegression().fit(X_tr, y_tr).predict(X_te)\n"
            "FINAL_MSE = mean_squared_error(y_te, pred)\n"
            "FINAL_R2 = r2_score(y_te, pred)\n"
            "print(FINAL_MSE, FINAL_R2)"
        ),
        md("## 3. Рефлексия модуля\n\n3 предложения: что изменилось после модуля 1 (списки → таблица → sklearn)?"),
        code("REFLECTION = ''  # заполните"),
    )
    sol = nb(md("# Решения: сдача"), code(LOAD_DATA))
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


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
    for rel, notebook in NOTEBOOKS.items():
        write(rel, notebook)
    print(f"total notebooks: {len(NOTEBOOKS)}")


if __name__ == "__main__":
    main()
