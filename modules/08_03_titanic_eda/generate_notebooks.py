#!/usr/bin/env python3
"""Generate lesson notebooks for module 08_03 (KTP pairs 17–23).

Source of truth for .ipynb: edit this file, then run it.
Data: checked-in standard Titanic CSV (seaborn.load_dataset('titanic') export).
Pattern: stubs + asserts in lesson/homework; full solutions.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_CSV = ROOT / "data" / "titanic.csv"

LOAD_DATA = (
    "from pathlib import Path\n"
    "import pandas as pd\n\n\n"
    "def find_titanic_csv() -> Path:\n"
    "    for p in (Path('titanic.csv'), Path('../../data/titanic.csv'), Path('../data/titanic.csv')):\n"
    "        if p.exists():\n"
    "            return p.resolve()\n"
    "    raise FileNotFoundError('titanic.csv не найден — положите файл рядом с ноутбуком')\n\n\n"
    "TITANIC_PATH = find_titanic_csv()\n"
    "df = pd.read_csv(TITANIC_PATH)\n"
)

IMPORTS_MPL = "import matplotlib.pyplot as plt\n"

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


def copy_csv(lesson_dir: str) -> None:
    dest = ROOT / lesson_dir / "titanic.csv"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DATA_CSV, dest)
    print("copied csv ->", dest)


NOTEBOOKS: dict[str, dict] = {}


def add_lesson01() -> None:
    base = "lessons/01_load_inspect_paths"
    lesson = nb(
        md(
            "# Titanic: загрузка, осмотр, пути и графики\n\n"
            "Историческое общество прислало таблицу пассажиров RMS Titanic. "
            "Модель строить **запрещено** — сначала понять, что в данных."
        ),
        code(LOAD_DATA),
        md(
            "## 1. Первичный осмотр\n\n"
            "Выведите `shape`, `head(5)` и список столбцов.\n\n"
            "**Вопрос:** сколько пассажиров и сколько полей?\n\n"
            "**Pitfall:** `print(df)` на 891 строке заливает экран."
        ),
        code(
            "n_rows, n_cols = None, None  # df.shape\n"
            "# print(df.head())\n"
            "# print(list(df.columns))\n"
            "assert n_rows is not None and n_cols is not None\n"
            "assert isinstance(n_rows, (int, float)) and n_rows == 891\n"
            "assert n_cols >= 10\n"
            "print(n_rows, n_cols)"
        ),
        md(
            "## 2. Цель анализа vs столбец survived\n\n"
            "Столбец `survived` (0/1) — **факт** из истории, не предсказание модели.\n\n"
            "Запишите долю выживших: `df['survived'].mean()` -> `survival_rate`.\n\n"
            "**Checkpoint:** почему `mean()` по 0/1 даёт долю?"
        ),
        code(
            "survival_rate = None  # float\n"
            "assert survival_rate is not None\n"
            "assert isinstance(survival_rate, float)\n"
            "assert 0.2 < survival_rate < 0.6\n"
            "print('доля выживших:', round(survival_rate, 3))"
        ),
        md(
            "## 3. dtypes и пропуски на уровне осмотра\n\n"
            "Вызовите `df.info()` или `df.isna().sum()`.\n\n"
            "Запишите число пропусков в `age` и в `embarked`.\n\n"
            "**How:** `df['age'].isna().sum()`."
        ),
        code(
            "age_na = None\n"
            "embarked_na = None\n"
            "assert age_na is not None and embarked_na is not None\n"
            "assert isinstance(age_na, (int, float)) and age_na > 100\n"
            "assert isinstance(embarked_na, (int, float)) and 0 <= embarked_na <= 5\n"
            "print('age NA:', age_na, '| embarked NA:', embarked_na)"
        ),
        md(
            "## 4. Роли столбцов для EDA\n\n"
            "Для отчёта обществу зафиксируйте:\n"
            "- **факт выживания** — `survived`;\n"
            "- **группы сравнения** — например `sex`, `pclass`, `embarked`;\n"
            "- **числовые описания** — `age`, `fare`.\n\n"
            "Заполните списки ниже (имена столбцов из `df.columns`)."
        ),
        code(
            "OUTCOME = ''\n"
            "GROUP_COLS = []\n"
            "NUMERIC_COLS = []\n\n"
            "assert OUTCOME in df.columns\n"
            "assert OUTCOME == 'survived'\n"
            "assert 'sex' in GROUP_COLS and 'pclass' in GROUP_COLS\n"
            "assert 'age' in NUMERIC_COLS and 'fare' in NUMERIC_COLS\n"
            "assert set(GROUP_COLS + NUMERIC_COLS + [OUTCOME]).issubset(df.columns)"
        ),
        md(
            "## 5. Путь к файлу\n\n"
            "Напечатайте `TITANIC_PATH` и проверьте, что файл существует.\n\n"
            "**Зачем:** в Colab CSV должен лежать **рядом** с ноутбуком или путь документирован."
        ),
        code(
            "path_ok = TITANIC_PATH.exists()\n"
            "assert path_ok is True\n"
            "print(TITANIC_PATH)"
        ),
        md(
            "## 6. Папка figures и первый график\n\n"
            "Создайте каталог `figures` (если нет). Постройте простой bar: "
            "число пассажиров по `pclass`. Сохраните в `figures/pclass_counts.png`.\n\n"
            "**How:** `Path('figures').mkdir(exist_ok=True)`; "
            "`df['pclass'].value_counts().sort_index().plot(kind='bar')`; `plt.savefig(...)`."
        ),
        code(
            IMPORTS_MPL
            + "from pathlib import Path as _P\n\n"
            "figures_dir = _P('figures')\n"
            "# figures_dir.mkdir(exist_ok=True)\n"
            "# ... plot ...\n"
            "saved_path = None  # Path к png\n"
            "assert saved_path is not None\n"
            "assert _P(saved_path).exists()\n"
            "print('saved:', saved_path)"
        ),
        md(
            "## 7. Checkpoint: без модели\n\n"
            "Напишите 2–3 предложения в `NO_MODEL_YET`: почему общество просит "
            "**сначала EDA**, а не `fit` классификатора (пропуски, группы, bias)."
        ),
        code(
            "NO_MODEL_YET = ''\n"
            "assert len(NO_MODEL_YET) > 40\n"
            "assert any(w in NO_MODEL_YET.lower() for w in ('eda', 'данн', 'пропуск', 'групп', 'bias', 'выбор'))\n"
            "print(NO_MODEL_YET)"
        ),
        md(
            "## 8. Расширение: deck\n\n"
            "Столбец `deck` почти пустой. Посчитайте долю пропусков в `deck` "
            "(число NA / число строк). Запишите в `deck_na_share`."
        ),
        code(
            "deck_na_share = None  # float 0..1\n"
            "assert deck_na_share is not None\n"
            "assert isinstance(deck_na_share, float)\n"
            "assert 0.5 < deck_na_share < 1.0\n"
            "print('доля NA в deck:', round(deck_na_share, 3))"
        ),
    )
    hw = nb(
        md("# ДЗ: загрузка и осмотр Titanic"),
        code(LOAD_DATA),
        md("### A. Закрепление"),
        md("## 1. Срез столбцов\n\nПервые 8 строк только `survived`, `pclass`, `sex`, `age`, `fare`."),
        code(
            "subset = None\n"
            "assert subset is not None\n"
            "assert list(subset.columns) == ['survived', 'pclass', 'sex', 'age', 'fare']\n"
            "assert len(subset) == 8\n"
            "print(subset)"
        ),
        md("## 2. value_counts по sex\n\nЧисло мужчин и женщин; запишите число уникальных значений `sex` в `n_sex`."),
        code(
            "sex_counts = None\n"
            "n_sex = None\n"
            "assert sex_counts is not None and n_sex is not None\n"
            "assert isinstance(n_sex, (int, float)) and n_sex == 2\n"
            "print(sex_counts)"
        ),
        md("## 3. Путь\n\nИмя файла из `TITANIC_PATH.name` должно быть `titanic.csv`."),
        code(
            "fname = TITANIC_PATH.name\n"
            "assert fname == 'titanic.csv'\n"
            "print(fname)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 4. Доля выживших в 3 классе\n\n"
            "Отфильтруйте `pclass == 3`, посчитайте `survived.mean()`. "
            "Сравните с общей долей — одной фразой."
        ),
        code(
            "rate_p3 = None\n"
            "rate_all = None\n"
            "COMPARE = ''\n"
            "assert rate_p3 is not None and rate_all is not None\n"
            "assert isinstance(rate_p3, float) and isinstance(rate_all, float)\n"
            "assert 0 < rate_p3 < 1 and 0 < rate_all < 1\n"
            "assert len(COMPARE) > 10\n"
            "print(round(rate_p3, 3), round(rate_all, 3), COMPARE)"
        ),
        md(
            "## 5. Сохранить график\n\n"
            "Bar по `embarked` (без NA) -> `figures/embarked_counts.png`."
        ),
        code(
            IMPORTS_MPL
            + "from pathlib import Path as _P\n"
            "_P('figures').mkdir(exist_ok=True)\n"
            "hw_fig = None  # Path\n"
            "assert hw_fig is not None and _P(hw_fig).exists()\n"
            "print(hw_fig)"
        ),
    )
    sol = nb(
        md("# Решения: загрузка Titanic\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        md("## Урок. 1. Осмотр"),
        code(
            "n_rows, n_cols = df.shape\n"
            "print(n_rows, n_cols)\n"
            "print(df.head())\n"
            "print(list(df.columns))"
        ),
        md("## Урок. 2. survival_rate"),
        code(
            "survival_rate = float(df['survived'].mean())\n"
            "print('доля выживших:', round(survival_rate, 3))"
        ),
        md("## Урок. 3. Пропуски"),
        code(
            "age_na = int(df['age'].isna().sum())\n"
            "embarked_na = int(df['embarked'].isna().sum())\n"
            "print('age NA:', age_na, '| embarked NA:', embarked_na)"
        ),
        md("## Урок. 4. Роли"),
        code(
            "OUTCOME = 'survived'\n"
            "GROUP_COLS = ['sex', 'pclass', 'embarked']\n"
            "NUMERIC_COLS = ['age', 'fare']"
        ),
        md("## Урок. 5. Путь"),
        code("print(TITANIC_PATH)\nassert TITANIC_PATH.exists()"),
        md("## Урок. 6. График"),
        code(
            IMPORTS_MPL
            + "from pathlib import Path as _P\n"
            "figures_dir = _P('figures')\n"
            "figures_dir.mkdir(exist_ok=True)\n"
            "ax = df['pclass'].value_counts().sort_index().plot(kind='bar')\n"
            "plt.xlabel('pclass'); plt.ylabel('count'); plt.tight_layout()\n"
            "saved_path = figures_dir / 'pclass_counts.png'\n"
            "plt.savefig(saved_path); plt.close()\n"
            "print('saved:', saved_path)"
        ),
        md("## Урок. 7. NO_MODEL_YET"),
        code(
            "NO_MODEL_YET = (\n"
            "    'Сначала EDA: пропуски в age/deck, различие групп sex/pclass, '\n"
            "    'риск смещения выборки. Без этого fit даст уверенный, но слепой ответ.'\n"
            ")\n"
            "print(NO_MODEL_YET)"
        ),
        md("## Урок. 8. deck"),
        code(
            "deck_na_share = float(df['deck'].isna().mean())\n"
            "print('доля NA в deck:', round(deck_na_share, 3))"
        ),
        md("## ДЗ. 1–5"),
        code(
            "subset = df[['survived', 'pclass', 'sex', 'age', 'fare']].head(8)\n"
            "sex_counts = df['sex'].value_counts()\n"
            "n_sex = int(df['sex'].nunique())\n"
            "print(subset); print(sex_counts)\n"
            "rate_p3 = float(df.loc[df['pclass'] == 3, 'survived'].mean())\n"
            "rate_all = float(df['survived'].mean())\n"
            "COMPARE = f'3 класс: {rate_p3:.3f}, все: {rate_all:.3f} — в 3 классе ниже'\n"
            "print(COMPARE)\n"
            + IMPORTS_MPL
            + "from pathlib import Path as _P\n"
            "_P('figures').mkdir(exist_ok=True)\n"
            "df['embarked'].dropna().value_counts().plot(kind='bar')\n"
            "hw_fig = _P('figures/embarked_counts.png')\n"
            "plt.tight_layout(); plt.savefig(hw_fig); plt.close()\n"
            "print(hw_fig)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson02() -> None:
    base = "lessons/02_practice_inspect"
    lesson = nb(
        md(
            "# Практика: осмотр таблицы Titanic\n\n"
            "Закрепляем срезы, фильтры и частоты — без статистики mean/median (это пара 19)."
        ),
        code(LOAD_DATA),
        md(
            "## 1. Фильтр: женщины 1 класса\n\n"
            "Сколько строк с `sex == 'female'` и `pclass == 1`? Запишите в `n_f1`."
        ),
        code(
            "n_f1 = None\n"
            "assert n_f1 is not None\n"
            "assert isinstance(n_f1, (int, float)) and 50 < n_f1 < 120\n"
            "print(n_f1)"
        ),
        md(
            "## 2. Доля выживших в этой группе\n\n"
            "`survived.mean()` только для женщин 1 класса -> `rate_f1`."
        ),
        code(
            "rate_f1 = None\n"
            "assert rate_f1 is not None and isinstance(rate_f1, float)\n"
            "assert 0.8 < rate_f1 <= 1.0\n"
            "print(round(rate_f1, 3))"
        ),
        md(
            "## 3. Ложный вывод — опровергнуть\n\n"
            "Утверждение: «почти все на Титанике выжили».\n\n"
            "Посчитайте общую долю и запишите опровержение в `REBUTTAL` (с числом)."
        ),
        code(
            "overall = float(df['survived'].mean())\n"
            "REBUTTAL = ''\n"
            "assert len(REBUTTAL) > 20\n"
            "assert '0.' in REBUTTAL or '%' in REBUTTAL or str(round(overall, 2))[:3] in REBUTTAL\n"
            "print(overall, REBUTTAL)"
        ),
        md(
            "## 4. who vs sex\n\n"
            "Столбец `who` (man/woman/child). Сравните `value_counts` для `who` и `sex`.\n\n"
            "Запишите число детей (`who == 'child'`) в `n_child`."
        ),
        code(
            "n_child = None\n"
            "assert n_child is not None\n"
            "assert isinstance(n_child, (int, float)) and 20 < n_child < 120\n"
            "print(n_child)"
        ),
        md(
            "## 5. alone и выживаемость\n\n"
            "Доля выживших среди `alone == True` и среди `alone == False`.\n\n"
            "**Вопрос учителю классу:** совпадает ли «один на борту» с низкой выживаемостью?"
        ),
        code(
            "rate_alone = None\n"
            "rate_not_alone = None\n"
            "assert rate_alone is not None and rate_not_alone is not None\n"
            "assert isinstance(rate_alone, float) and isinstance(rate_not_alone, float)\n"
            "print(round(rate_alone, 3), round(rate_not_alone, 3))"
        ),
        md(
            "## 6. Срез по порту\n\n"
            "Таблица: для каждого `embarked` (без NA) — число пассажиров и доля выживших.\n\n"
            "**How:** `groupby('embarked')['survived'].agg(['count', 'mean'])`."
        ),
        code(
            "by_port = None  # DataFrame\n"
            "assert by_port is not None\n"
            "assert 'count' in by_port.columns or by_port.shape[1] >= 2\n"
            "print(by_port)"
        ),
        md(
            "## 7. Checkpoint: корреляция ≠ причинность\n\n"
            "Разница долей по портам **не** доказывает, что порт «спасает». "
            "Напишите в `CAUSALITY_NOTE`, какой скрытый фактор может объяснять разницу "
            "(подсказка: связь порта и `pclass`)."
        ),
        code(
            "CAUSALITY_NOTE = ''\n"
            "assert len(CAUSALITY_NOTE) > 30\n"
            "assert any(w in CAUSALITY_NOTE.lower() for w in ('класс', 'pclass', 'богат', 'палуб', 'билет'))\n"
            "print(CAUSALITY_NOTE)"
        ),
        md(
            "## 8. Расширение: adult_male\n\n"
            "Доля выживших среди `adult_male == True` — обычно самая низкая группа. "
            "Запишите в `rate_adult_male`."
        ),
        code(
            "rate_adult_male = None\n"
            "assert rate_adult_male is not None and isinstance(rate_adult_male, float)\n"
            "assert 0.05 < rate_adult_male < 0.35\n"
            "print(round(rate_adult_male, 3))"
        ),
    )
    hw = nb(
        md("# ДЗ: практика осмотра"),
        code(LOAD_DATA),
        md("### A. Закрепление"),
        md("## 1. Мужчины 3 класса: число и доля выживших"),
        code(
            "n_m3 = None\n"
            "rate_m3 = None\n"
            "assert n_m3 is not None and rate_m3 is not None\n"
            "assert isinstance(n_m3, (int, float)) and n_m3 > 200\n"
            "assert isinstance(rate_m3, float) and 0 < rate_m3 < 0.4\n"
            "print(n_m3, round(rate_m3, 3))"
        ),
        md("## 2. Топ embark_town по числу пассажиров"),
        code(
            "top_town = None  # str\n"
            "assert top_town is not None and isinstance(top_town, str) and len(top_town) > 2\n"
            "print(top_town)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. Опровержение\n\n"
            "Утверждение: «дети выживали реже взрослых мужчин». "
            "Сравните `who=='child'` и `adult_male==True`; напишите `VERDICT` с двумя числами."
        ),
        code(
            "rate_child = None\n"
            "rate_am = None\n"
            "VERDICT = ''\n"
            "assert rate_child is not None and rate_am is not None\n"
            "assert isinstance(rate_child, float) and isinstance(rate_am, float)\n"
            "assert len(VERDICT) > 20\n"
            "print(round(rate_child, 3), round(rate_am, 3), VERDICT)"
        ),
        md(
            "## 4. Crosstab sex × pclass\n\n"
            "Постройте `pd.crosstab(df['sex'], df['pclass'])` — числа пассажиров. "
            "Запишите число женщин во 2 классе в `n_f2`."
        ),
        code(
            "ct = None\n"
            "n_f2 = None\n"
            "assert ct is not None and n_f2 is not None\n"
            "assert isinstance(n_f2, (int, float)) and 50 < n_f2 < 100\n"
            "print(ct); print(n_f2)"
        ),
    )
    sol = nb(
        md("# Решения: практика осмотра\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        md("## Урок"),
        code(
            "n_f1 = int(((df['sex'] == 'female') & (df['pclass'] == 1)).sum())\n"
            "rate_f1 = float(df.loc[(df['sex'] == 'female') & (df['pclass'] == 1), 'survived'].mean())\n"
            "overall = float(df['survived'].mean())\n"
            "REBUTTAL = f'Выжили лишь ~{overall:.1%}, не почти все'\n"
            "n_child = int((df['who'] == 'child').sum())\n"
            "rate_alone = float(df.loc[df['alone'] == True, 'survived'].mean())\n"
            "rate_not_alone = float(df.loc[df['alone'] == False, 'survived'].mean())\n"
            "by_port = df.dropna(subset=['embarked']).groupby('embarked')['survived'].agg(['count', 'mean'])\n"
            "CAUSALITY_NOTE = 'Порт связан с pclass/тарифом: Cherbourg чаще 1 класс — не «магия порта».'\n"
            "rate_adult_male = float(df.loc[df['adult_male'] == True, 'survived'].mean())\n"
            "print(n_f1, rate_f1, REBUTTAL, n_child, by_port, rate_adult_male)"
        ),
        md("## ДЗ"),
        code(
            "n_m3 = int(((df['sex'] == 'male') & (df['pclass'] == 3)).sum())\n"
            "rate_m3 = float(df.loc[(df['sex'] == 'male') & (df['pclass'] == 3), 'survived'].mean())\n"
            "top_town = str(df['embark_town'].value_counts().index[0])\n"
            "rate_child = float(df.loc[df['who'] == 'child', 'survived'].mean())\n"
            "rate_am = float(df.loc[df['adult_male'] == True, 'survived'].mean())\n"
            "VERDICT = f'дети {rate_child:.3f} vs adult_male {rate_am:.3f} — утверждение ложно'\n"
            "ct = pd.crosstab(df['sex'], df['pclass'])\n"
            "n_f2 = int(ct.loc['female', 2])\n"
            "print(n_m3, rate_m3, top_town, VERDICT, n_f2)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson03() -> None:
    base = "lessons/03_mean_median_std"
    lesson = nb(
        md(
            "# Среднее, медиана, std — вручную и в pandas\n\n"
            "Описываем `age` и `fare`: центр и разброс. Модель не нужна."
        ),
        code(LOAD_DATA + "\nages = df['age'].dropna()\nfares = df['fare']\n"),
        md(
            "## 1. Среднее age вручную\n\n"
            "`sum(ages) / len(ages)` -> `mean_age_manual`. Сверьте с `ages.mean()`."
        ),
        code(
            "mean_age_manual = None\n"
            "mean_age_pd = float(ages.mean())\n"
            "assert mean_age_manual is not None\n"
            "assert abs(float(mean_age_manual) - mean_age_pd) < 1e-9\n"
            "print(mean_age_manual, mean_age_pd)"
        ),
        md(
            "## 2. Медиана age\n\n"
            "Упорядочите значения и возьмите середину (при чётном n — среднее двух центральных). "
            "Или `ages.median()`. -> `median_age`.\n\n"
            "**Why:** медиана устойчивее к выбросам, чем mean."
        ),
        code(
            "median_age = None\n"
            "assert median_age is not None\n"
            "assert abs(float(median_age) - float(ages.median())) < 1e-9\n"
            "print(median_age)"
        ),
        md(
            "## 3. Std age\n\n"
            "`ages.std()` (выборочное, ddof=1 в pandas по умолчанию). -> `std_age`.\n\n"
            "**Интуиция:** типичный разброс вокруг среднего в тех же единицах (годы)."
        ),
        code(
            "std_age = None\n"
            "assert std_age is not None and isinstance(float(std_age), float)\n"
            "assert 10 < float(std_age) < 20\n"
            "print(round(float(std_age), 2))"
        ),
        md(
            "## 4. mean vs median для fare\n\n"
            "Сравните `fares.mean()` и `fares.median()`. "
            "Почему mean больше? Запишите в `FARE_NOTE`."
        ),
        code(
            "fare_mean = None\n"
            "fare_median = None\n"
            "FARE_NOTE = ''\n"
            "assert fare_mean is not None and fare_median is not None\n"
            "assert float(fare_mean) > float(fare_median)\n"
            "assert len(FARE_NOTE) > 20\n"
            "print(round(float(fare_mean), 2), round(float(fare_median), 2), FARE_NOTE)"
        ),
        md(
            "## 5. describe\n\n"
            "Выведите `df[['age', 'fare']].describe()` и найдите 75% квартиль fare -> `fare_q3`."
        ),
        code(
            "# print(df[['age', 'fare']].describe())\n"
            "fare_q3 = None\n"
            "assert fare_q3 is not None\n"
            "assert 20 < float(fare_q3) < 50\n"
            "print(fare_q3)"
        ),
        md(
            "## 6. Эксперимент: выброс\n\n"
            "Скопируйте `fares` в список/Series, добавьте искусственный билет 5000, "
            "пересчитайте mean и median. Что сдвинулось сильнее? -> `OUTLIER_EFFECT`."
        ),
        code(
            "mean_with_outlier = None\n"
            "median_with_outlier = None\n"
            "OUTLIER_EFFECT = ''\n"
            "assert mean_with_outlier is not None and median_with_outlier is not None\n"
            "assert float(mean_with_outlier) > float(fares.mean())\n"
            "assert abs(float(median_with_outlier) - float(fares.median())) < 1.0\n"
            "assert len(OUTLIER_EFFECT) > 15\n"
            "print(mean_with_outlier, median_with_outlier, OUTLIER_EFFECT)"
        ),
        md(
            "## 7. Группы: средний age по pclass\n\n"
            "`groupby('pclass')['age'].mean()` -> `age_by_class`."
        ),
        code(
            "age_by_class = None\n"
            "assert age_by_class is not None\n"
            "assert len(age_by_class) == 3\n"
            "print(age_by_class)"
        ),
        md(
            "## 8. Checkpoint\n\n"
            "Когда для отчёта обществу лучше указать **медиану** fare, а не mean? -> `WHEN_MEDIAN`."
        ),
        code(
            "WHEN_MEDIAN = ''\n"
            "assert len(WHEN_MEDIAN) > 25\n"
            "assert any(w in WHEN_MEDIAN.lower() for w in ('выброс', 'дорог', 'смещ', 'устой', 'типич'))\n"
            "print(WHEN_MEDIAN)"
        ),
    )
    hw = nb(
        md("# ДЗ: mean / median / std"),
        code(LOAD_DATA + "\nages = df['age'].dropna()\n"),
        md("### A. Закрепление"),
        md("## 1. mean, median, std для age — через pandas"),
        code(
            "a_mean = None\n"
            "a_med = None\n"
            "a_std = None\n"
            "assert a_mean is not None and a_med is not None and a_std is not None\n"
            "assert 25 < float(a_mean) < 35\n"
            "assert 20 < float(a_med) < 35\n"
            "assert 10 < float(a_std) < 20\n"
            "print(a_mean, a_med, a_std)"
        ),
        md("## 2. Средний fare по sex"),
        code(
            "fare_by_sex = None\n"
            "assert fare_by_sex is not None\n"
            "assert set(fare_by_sex.index) >= {'male', 'female'}\n"
            "print(fare_by_sex)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. Устойчивость\n\n"
            "Удалите 1% самых больших fare (`quantile(0.99)`), сравните mean до/после. "
            "`MEAN_DROP_NOTE` — на сколько примерно упало mean."
        ),
        code(
            "mean_before = float(df['fare'].mean())\n"
            "mean_after = None\n"
            "MEAN_DROP_NOTE = ''\n"
            "assert mean_after is not None\n"
            "assert float(mean_after) < mean_before\n"
            "assert len(MEAN_DROP_NOTE) > 10\n"
            "print(mean_before, mean_after, MEAN_DROP_NOTE)"
        ),
        md(
            "## 4. Ручная медиана на маленьком списке\n\n"
            "Для `[1, 3, 100]` посчитайте median вручную -> `toy_median` (должно быть 3)."
        ),
        code(
            "toy_median = None\n"
            "assert toy_median is not None and float(toy_median) == 3\n"
            "print(toy_median)"
        ),
    )
    sol = nb(
        md("# Решения: mean median std\n\n" + SOL_BANNER),
        code(LOAD_DATA + "\nages = df['age'].dropna()\nfares = df['fare']\n"),
        md("## Урок"),
        code(
            "mean_age_manual = float(sum(ages) / len(ages))\n"
            "median_age = float(ages.median())\n"
            "std_age = float(ages.std())\n"
            "fare_mean = float(fares.mean())\n"
            "fare_median = float(fares.median())\n"
            "FARE_NOTE = 'mean тянут редкие очень дорогие билеты; медиана ближе к типичному'\n"
            "fare_q3 = float(fares.quantile(0.75))\n"
            "fares2 = pd.concat([fares, pd.Series([5000.0])])\n"
            "mean_with_outlier = float(fares2.mean())\n"
            "median_with_outlier = float(fares2.median())\n"
            "OUTLIER_EFFECT = 'mean вырос сильно, median почти нет'\n"
            "age_by_class = df.groupby('pclass')['age'].mean()\n"
            "WHEN_MEDIAN = 'Когда есть дорогие выбросы и нужен типичный билет, а не среднее арифметическое'\n"
            "print(mean_age_manual, median_age, std_age, fare_q3, age_by_class)"
        ),
        md("## ДЗ"),
        code(
            "a_mean, a_med, a_std = float(ages.mean()), float(ages.median()), float(ages.std())\n"
            "fare_by_sex = df.groupby('sex')['fare'].mean()\n"
            "thr = df['fare'].quantile(0.99)\n"
            "mean_after = float(df.loc[df['fare'] <= thr, 'fare'].mean())\n"
            "MEAN_DROP_NOTE = f'mean {df[\"fare\"].mean():.1f} -> {mean_after:.1f} после отсечения top 1%'\n"
            "toy_median = 3\n"
            "print(a_mean, fare_by_sex, MEAN_DROP_NOTE, toy_median)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson04() -> None:
    base = "lessons/04_practice_boxplot"
    lesson = nb(
        md(
            "# Квартили, boxplot, группы\n\n"
            "Визуализируем разброс `age`/`fare` и сравниваем классы каюты."
        ),
        code(LOAD_DATA + "\n" + IMPORTS_MPL),
        md(
            "## 1. Квартили age\n\n"
            "Q1, Q2 (медиана), Q3 через `quantile(0.25/0.5/0.75)` на `age` без NA."
        ),
        code(
            "ages = df['age'].dropna()\n"
            "q1 = q2 = q3 = None\n"
            "assert q1 is not None and q2 is not None and q3 is not None\n"
            "assert float(q1) < float(q2) < float(q3)\n"
            "print(q1, q2, q3)"
        ),
        md(
            "## 2. IQR и «усы»\n\n"
            "IQR = Q3 − Q1. Запишите `iqr_age`. "
            "Граница выброса часто Q3 + 1.5·IQR — посчитайте `upper_fence`."
        ),
        code(
            "iqr_age = None\n"
            "upper_fence = None\n"
            "assert iqr_age is not None and upper_fence is not None\n"
            "assert float(iqr_age) > 0\n"
            "print(iqr_age, upper_fence)"
        ),
        md(
            "## 3. Boxplot age\n\n"
            "`df.boxplot(column='age')` или `plt.boxplot(...)`. "
            "Сохраните `figures/age_box.png`."
        ),
        code(
            "from pathlib import Path as _P\n"
            "_P('figures').mkdir(exist_ok=True)\n"
            "age_box_path = None\n"
            "assert age_box_path is not None and _P(age_box_path).exists()\n"
            "print(age_box_path)"
        ),
        md(
            "## 4. Boxplot fare по pclass\n\n"
            "`df.boxplot(column='fare', by='pclass')`. Сохраните `figures/fare_by_pclass.png`.\n\n"
            "**Наблюдение:** в 1 классе медиана и усы выше."
        ),
        code(
            "fare_box_path = None\n"
            "assert fare_box_path is not None\n"
            "from pathlib import Path as _P\n"
            "assert _P(fare_box_path).exists()\n"
            "print(fare_box_path)"
        ),
        md(
            "## 5. Сколько выбросов fare\n\n"
            "Число пассажиров с `fare > Q3 + 1.5*IQR` (IQR по всей выборке fare) -> `n_fare_outliers`."
        ),
        code(
            "n_fare_outliers = None\n"
            "assert n_fare_outliers is not None\n"
            "assert isinstance(n_fare_outliers, (int, float)) and n_fare_outliers > 10\n"
            "print(n_fare_outliers)"
        ),
        md(
            "## 6. Группы: age по who\n\n"
            "Медиана age для man / woman / child. -> `age_med_by_who`."
        ),
        code(
            "age_med_by_who = None\n"
            "assert age_med_by_who is not None\n"
            "print(age_med_by_who)"
        ),
        md(
            "## 7. Критика графика\n\n"
            "Утверждение: «boxplot fare доказывает, что 3 класс не выживал». "
            "Почему это **неверный** вывод из одного boxplot fare? -> `WRONG_CLAIM`."
        ),
        code(
            "WRONG_CLAIM = ''\n"
            "assert len(WRONG_CLAIM) > 40\n"
            "assert any(w in WRONG_CLAIM.lower() for w in ('survived', 'выж', 'не показ', 'другой', 'связ'))\n"
            "print(WRONG_CLAIM)"
        ),
        md(
            "## 8. Расширение: boxplot age по survived\n\n"
            "Сравните возраст выживших и нет. Сохраните `figures/age_by_survived.png` "
            "и одной фразой `AGE_SURV_NOTE`."
        ),
        code(
            "age_surv_path = None\n"
            "AGE_SURV_NOTE = ''\n"
            "assert age_surv_path is not None\n"
            "assert len(AGE_SURV_NOTE) > 15\n"
            "print(age_surv_path, AGE_SURV_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: квартили и boxplot"),
        code(LOAD_DATA + "\n" + IMPORTS_MPL),
        md("### A. Закрепление"),
        md("## 1. Q1/Q2/Q3 для fare"),
        code(
            "fq1 = fq2 = fq3 = None\n"
            "assert fq1 is not None and float(fq1) < float(fq2) < float(fq3)\n"
            "print(fq1, fq2, fq3)"
        ),
        md("## 2. Boxplot fare — сохранить figures/fare_box_hw.png"),
        code(
            "from pathlib import Path as _P\n"
            "_P('figures').mkdir(exist_ok=True)\n"
            "p = None\n"
            "assert p is not None and _P(p).exists()\n"
            "print(p)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. Медиана fare: female vs male\n\n"
            "Кто платил больше по медиане? `COMPARE_FARE` с двумя числами."
        ),
        code(
            "med_f = None\n"
            "med_m = None\n"
            "COMPARE_FARE = ''\n"
            "assert med_f is not None and med_m is not None\n"
            "assert len(COMPARE_FARE) > 15\n"
            "print(med_f, med_m, COMPARE_FARE)"
        ),
        md(
            "## 4. Опровержение\n\n"
            "«Все выбросы fare — ошибки данных». Почему это сомнительно на Titanic? -> `OUTLIER_NOTE`."
        ),
        code(
            "OUTLIER_NOTE = ''\n"
            "assert len(OUTLIER_NOTE) > 30\n"
            "print(OUTLIER_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: boxplot\n\n" + SOL_BANNER),
        code(LOAD_DATA + "\n" + IMPORTS_MPL + "from pathlib import Path as _P\n_P('figures').mkdir(exist_ok=True)\n"),
        md("## Урок"),
        code(
            "ages = df['age'].dropna()\n"
            "q1, q2, q3 = float(ages.quantile(0.25)), float(ages.quantile(0.5)), float(ages.quantile(0.75))\n"
            "iqr_age = q3 - q1\n"
            "upper_fence = q3 + 1.5 * iqr_age\n"
            "plt.figure(); df.boxplot(column='age'); plt.tight_layout()\n"
            "age_box_path = _P('figures/age_box.png'); plt.savefig(age_box_path); plt.close()\n"
            "plt.figure(); df.boxplot(column='fare', by='pclass'); plt.suptitle(''); plt.tight_layout()\n"
            "fare_box_path = _P('figures/fare_by_pclass.png'); plt.savefig(fare_box_path); plt.close()\n"
            "fq1, fq3 = float(df['fare'].quantile(0.25)), float(df['fare'].quantile(0.75))\n"
            "n_fare_outliers = int((df['fare'] > fq3 + 1.5 * (fq3 - fq1)).sum())\n"
            "age_med_by_who = df.groupby('who')['age'].median()\n"
            "WRONG_CLAIM = 'Boxplot fare не содержит survived — нельзя вывести выживаемость из одного разброса цены'\n"
            "plt.figure(); df.boxplot(column='age', by='survived'); plt.suptitle(''); plt.tight_layout()\n"
            "age_surv_path = _P('figures/age_by_survived.png'); plt.savefig(age_surv_path); plt.close()\n"
            "AGE_SURV_NOTE = 'медианы близки; возраст сам по себе слабый разделитель'\n"
            "print(q1, q2, q3, n_fare_outliers, age_med_by_who)"
        ),
        md("## ДЗ"),
        code(
            "fq1, fq2, fq3 = [float(df['fare'].quantile(q)) for q in (0.25, 0.5, 0.75)]\n"
            "plt.figure(); df.boxplot(column='fare'); plt.tight_layout()\n"
            "p = _P('figures/fare_box_hw.png'); plt.savefig(p); plt.close()\n"
            "med_f = float(df.loc[df['sex'] == 'female', 'fare'].median())\n"
            "med_m = float(df.loc[df['sex'] == 'male', 'fare'].median())\n"
            "COMPARE_FARE = f'female {med_f:.1f} vs male {med_m:.1f}'\n"
            "OUTLIER_NOTE = 'Дорогие билеты 1 класса — реальные suite/luxury, не обязательно ошибка ввода'\n"
            "print(fq1, fq2, fq3, COMPARE_FARE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol

def add_lesson05() -> None:
    """Pair 21: sampling bias + CLT + missing (old 25+26)."""
    base = "lessons/05_bias_clt_missing"
    lesson = nb(
        md(
            "# Sampling bias; ЦПТ; пропуски\n\n"
            "Три темы одной пары: смещённая подвыборка, колокол средних, стратегия чистки."
        ),
        code(LOAD_DATA + "\n" + IMPORTS_MPL + "import numpy as np\n"),
        md(
            "## 1. Истинная доля выживших\n\n"
            "`true_rate = df['survived'].mean()` — эталон «полной» таблицы урока."
        ),
        code(
            "true_rate = float(df['survived'].mean())\n"
            "assert 0.3 < true_rate < 0.5\n"
            "print(round(true_rate, 3))"
        ),
        md(
            "## 2. Смещённые подвыборки\n\n"
            "`rate_first` (pclass==1) и `rate_male`. Запишите `BIAS_MALE` — почему опрос только мужчин врёт."
        ),
        code(
            "rate_first = None\n"
            "rate_male = None\n"
            "BIAS_MALE = ''\n"
            "assert rate_first is not None and float(rate_first) > true_rate\n"
            "assert rate_male is not None and float(rate_male) < true_rate\n"
            "assert len(BIAS_MALE) > 30\n"
            "print(round(float(rate_first), 3), round(float(rate_male), 3), BIAS_MALE)"
        ),
        md(
            "## 3. Случайная выборка n=50\n\n"
            "Два `sample(50)` с `random_state` 0 и 1 → `rate_s50`, `rate_s50_b`."
        ),
        code(
            "rate_s50 = None\n"
            "rate_s50_b = None\n"
            "assert rate_s50 is not None and rate_s50_b is not None\n"
            "print(rate_s50, rate_s50_b, abs(float(rate_s50) - float(rate_s50_b)))"
        ),
        md(
            "## 4. Known deck + LIMITATIONS\n\n"
            "`rate_known_deck` на строках с известным deck; абзац `LIMITATIONS` (≥120 символов) "
            "для отчёта обществу."
        ),
        code(
            "rate_known_deck = None\n"
            "LIMITATIONS = ''\n"
            "assert rate_known_deck is not None\n"
            "assert len(LIMITATIONS) > 120\n"
            "print(round(float(rate_known_deck), 3), LIMITATIONS[:80], '...')"
        ),
        md(
            "## 5. Гистограмма age и ЦПТ на средних fare\n\n"
            "1) hist age → `figures/age_hist.png`, комментарий `AGE_SHAPE`.\n"
            "2) 200 выборок размера 40 из `fare`, mean каждой → hist → `figures/clt_fare_means.png`.\n\n"
            "**Идея:** колокол — у *средних*, не обязательно у сырого fare. `CLT_LIMIT`."
        ),
        code(
            "from pathlib import Path as _P\n"
            "_P('figures').mkdir(exist_ok=True)\n"
            "AGE_SHAPE = ''\n"
            "means = None  # list длины 200\n"
            "clt_path = None\n"
            "CLT_LIMIT = ''\n"
            "assert len(AGE_SHAPE) > 15\n"
            "assert means is not None and len(means) == 200\n"
            "assert clt_path is not None and _P(clt_path).exists()\n"
            "assert len(CLT_LIMIT) > 30\n"
            "print(AGE_SHAPE, round(float(np.mean(means)), 2), CLT_LIMIT)"
        ),
        md(
            "## 6. Пропуски и стратегии\n\n"
            "`TOP_NA` (топ-3); `n_drop` строк с известным age (=714); "
            "`age_filled_median`; почему ноль плох — `ZERO_BAD`."
        ),
        code(
            "TOP_NA = []\n"
            "n_drop = None\n"
            "age_filled_median = None\n"
            "ZERO_BAD = ''\n"
            "assert len(TOP_NA) == 3 and 'deck' in TOP_NA and 'age' in TOP_NA\n"
            "assert n_drop is not None and int(n_drop) == 714\n"
            "assert age_filled_median is not None and int(pd.Series(age_filled_median).isna().sum()) == 0\n"
            "assert len(ZERO_BAD) > 25\n"
            "print(TOP_NA, n_drop, ZERO_BAD)"
        ),
        md(
            "## 7. dropna по всей таблице + журнал\n\n"
            "`n_all_drop` после `df.dropna()`; `DROP_ALL_RISK`; `CLEAN_LOG` (deck/age/duplicates)."
        ),
        code(
            "n_all_drop = None\n"
            "DROP_ALL_RISK = ''\n"
            "CLEAN_LOG = ''\n"
            "assert n_all_drop is not None and int(n_all_drop) < 300\n"
            "assert len(DROP_ALL_RISK) > 30\n"
            "assert len(CLEAN_LOG) > 80\n"
            "print(n_all_drop, DROP_ALL_RISK, CLEAN_LOG[:80], '...')"
        ),
        md(
            "## 8. Расширение: стратификация\n\n"
            "`STRATA_IDEA` — зачем выборка с той же долей pclass лучше sample из одного класса."
        ),
        code(
            "STRATA_IDEA = ''\n"
            "assert len(STRATA_IDEA) > 25\n"
            "print(STRATA_IDEA)"
        ),
    )
    hw = nb(
        md("# ДЗ: bias, ЦПТ, пропуски"),
        code(LOAD_DATA + "\nimport numpy as np\n"),
        md("### A. Закрепление"),
        md("## 1. rate только female и только pclass==3"),
        code(
            "rate_f = None\n"
            "rate_p3 = None\n"
            "true_rate = float(df['survived'].mean())\n"
            "assert rate_f is not None and rate_p3 is not None\n"
            "assert float(rate_f) > true_rate and float(rate_p3) < true_rate\n"
            "print(rate_f, rate_p3, true_rate)"
        ),
        md("## 2. 100 средних age (sample n=25) — std этих средних"),
        code(
            "std_of_means = None\n"
            "assert std_of_means is not None and float(std_of_means) > 0\n"
            "print(std_of_means)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. rate_all vs rate_age_known + `AGE_NA_BIAS`\n\n"
            "## 4. «Большая выборка всегда репрезентативна» → `BIG_N_MYTH`"
        ),
        code(
            "rate_all = float(df['survived'].mean())\n"
            "rate_age_known = None\n"
            "AGE_NA_BIAS = ''\n"
            "BIG_N_MYTH = ''\n"
            "assert rate_age_known is not None\n"
            "assert len(AGE_NA_BIAS) > 30 and len(BIG_N_MYTH) > 40\n"
            "print(rate_all, rate_age_known, AGE_NA_BIAS, BIG_N_MYTH)"
        ),
    )
    sol = nb(
        md("# Решения: bias + CLT + missing\n\n" + SOL_BANNER),
        code(LOAD_DATA + "\n" + IMPORTS_MPL + "import numpy as np\nfrom pathlib import Path as _P\n_P('figures').mkdir(exist_ok=True)\n"),
        md("## Урок"),
        code(
            "true_rate = float(df['survived'].mean())\n"
            "rate_first = float(df.loc[df['pclass'] == 1, 'survived'].mean())\n"
            "rate_male = float(df.loc[df['sex'] == 'male', 'survived'].mean())\n"
            "BIAS_MALE = 'Мужчины выживали реже; опрос только мужчин занизит долю выживших'\n"
            "rate_s50 = float(df.sample(50, random_state=0)['survived'].mean())\n"
            "rate_s50_b = float(df.sample(50, random_state=1)['survived'].mean())\n"
            "rate_known_deck = float(df.dropna(subset=['deck'])['survived'].mean())\n"
            "LIMITATIONS = (\n"
            "    'Таблица — пассажиры из учебного набора, не полный список всех на борту. '\n"
            "    'Команда и часть документов отсутствуют. Срезы по deck/1 классу перепредставляют состоятельных. '\n"
            "    'Нельзя переносить доли на всё население 1912 года. Вывод — об этой таблице и её ограничениях.'\n"
            ")\n"
            "plt.figure(); df['age'].dropna().hist(bins=20); plt.tight_layout()\n"
            "plt.savefig('figures/age_hist.png'); plt.close()\n"
            "AGE_SHAPE = 'возраст скошен, не идеальный колокол'\n"
            "rng = np.random.default_rng(0)\n"
            "fare = df['fare'].to_numpy()\n"
            "means = [float(rng.choice(fare, size=40, replace=True).mean()) for _ in range(200)]\n"
            "plt.figure(); plt.hist(means, bins=20); plt.tight_layout()\n"
            "clt_path = _P('figures/clt_fare_means.png'); plt.savefig(clt_path); plt.close()\n"
            "CLT_LIMIT = 'ЦПТ про распределение средних при больших n, не про форму сырого fare'\n"
            "TOP_NA = list(df.isna().sum().sort_values(ascending=False).head(3).index)\n"
            "n_drop = int(df['age'].notna().sum())\n"
            "age_filled_median = df['age'].fillna(df['age'].median())\n"
            "ZERO_BAD = 'Возраст 0 путается с младенцами и ломает mean/модель'\n"
            "n_all_drop = int(len(df.dropna()))\n"
            "DROP_ALL_RISK = 'Остаются в основном строки с известным deck — смещение к 1 классу'\n"
            "CLEAN_LOG = (\n"
            "    'deck: не импутируем (слишком много NA). age: для описательных таблиц — median fill или анализ с NA отдельно. '\n"
            "    'duplicates: drop_duplicates перед агрегатами. embarked: 2 NA — можно dropna точечно.'\n"
            ")\n"
            "STRATA_IDEA = 'Страты по pclass сохраняют структуру классов и меньше тянут bias'\n"
            "print(true_rate, TOP_NA, n_all_drop)"
        ),
        md("## ДЗ"),
        code(
            "rate_f = float(df.loc[df['sex'] == 'female', 'survived'].mean())\n"
            "rate_p3 = float(df.loc[df['pclass'] == 3, 'survived'].mean())\n"
            "ages = df['age'].dropna().to_numpy()\n"
            "rng = np.random.default_rng(1)\n"
            "std_of_means = float(np.std([rng.choice(ages, 25, replace=True).mean() for _ in range(100)]))\n"
            "rate_age_known = float(df.dropna(subset=['age'])['survived'].mean())\n"
            "AGE_NA_BIAS = 'Пропуски age не случайны по классу/кто — доля survived может сдвинуться'\n"
            "BIG_N_MYTH = 'Можно взять много мужчин 3 класса — n большое, но структура всё ещё смещена'\n"
            "print(rate_f, rate_p3, std_of_means, rate_age_known)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson06() -> None:
    """Pair 22: practice groups (old 27)."""
    base = "lessons/06_practice_groups"
    lesson = nb(
        md(
            "# Практика: гистограммы, группы, стратегии пропусков\n\n"
            "Сводим визуальное сравнение выживаемости и осознанный выбор чистки."
        ),
        code(LOAD_DATA + "\n" + IMPORTS_MPL),
        md(
            "## 1. Гистограмма fare по survived\n\n"
            "Две гистограммы (или одна с alpha): fare для survived==0 и ==1. "
            "Сохраните `figures/fare_by_survived_hist.png`. Краткий вывод `FARE_HIST_NOTE`."
        ),
        code(
            "from pathlib import Path as _P\n"
            "_P('figures').mkdir(exist_ok=True)\n"
            "fare_hist_path = None\n"
            "FARE_HIST_NOTE = ''\n"
            "assert fare_hist_path is not None and _P(fare_hist_path).exists()\n"
            "assert len(FARE_HIST_NOTE) > 15\n"
            "print(FARE_HIST_NOTE)"
        ),
        md(
            "## 2. Доли survived: sex × pclass\n\n"
            "`groupby(['sex','pclass'])['survived'].mean().unstack()` -> `rates`.\n\n"
            "**Наблюдение:** женщины 1–2 класса vs мужчины 3."
        ),
        code(
            "rates = None\n"
            "assert rates is not None\n"
            "print(rates)"
        ),
        md(
            "## 3. Bar: доля выживших по who\n\n"
            "Сохраните `figures/survived_by_who.png`."
        ),
        code(
            "who_bar_path = None\n"
            "from pathlib import Path as _P\n"
            "assert who_bar_path is not None and _P(who_bar_path).exists()\n"
            "print(who_bar_path)"
        ),
        md(
            "## 4. Стратегия A vs B для age\n\n"
            "A: анализ только с известным age — `rate_A`.\n"
            "B: заполнить медианой age, затем средний age выживших vs нет — "
            "`mean_age_surv_B`, `mean_age_dead_B`.\n\n"
            "Когда A честнее для доли survived? -> `WHEN_A`."
        ),
        code(
            "rate_A = None\n"
            "mean_age_surv_B = None\n"
            "mean_age_dead_B = None\n"
            "WHEN_A = ''\n"
            "assert rate_A is not None and mean_age_surv_B is not None\n"
            "assert len(WHEN_A) > 25\n"
            "print(rate_A, mean_age_surv_B, mean_age_dead_B, WHEN_A)"
        ),
        md(
            "## 5. Не удалять deck-строки слепо\n\n"
            "Сравните долю 1 класса во всём df и среди строк с известным deck. "
            "`share_p1_all` vs `share_p1_deck`."
        ),
        code(
            "share_p1_all = None\n"
            "share_p1_deck = None\n"
            "assert share_p1_all is not None and share_p1_deck is not None\n"
            "assert float(share_p1_deck) > float(share_p1_all)\n"
            "print(round(float(share_p1_all), 3), round(float(share_p1_deck), 3))"
        ),
        md(
            "## 6. Опровержение\n\n"
            "«Разница долей sex доказывает, что пол *причинно* спасает». "
            "Сформулируйте корректную формулировку для общества -> `CAREFUL_CLAIM`."
        ),
        code(
            "CAREFUL_CLAIM = ''\n"
            "assert len(CAREFUL_CLAIM) > 40\n"
            "assert any(w in CAREFUL_CLAIM.lower() for w in ('связ', 'ассоц', 'наблюд', 'не доказ', 'корреля'))\n"
            "print(CAREFUL_CLAIM)"
        ),
        md(
            "## 7. Сводная таблица для отчёта\n\n"
            "Соберите DataFrame `summary` с колонками group, n, survival_rate "
            "хотя бы для sex=female/male и pclass=1/2/3 (можно concat)."
        ),
        code(
            "summary = None\n"
            "assert summary is not None\n"
            "assert len(summary) >= 5\n"
            "print(summary)"
        ),
        md(
            "## 8. Расширение: embark_town\n\n"
            "Доли survived по `embark_town` (dropna). Есть ли город с аномально высокой долей? "
            "`TOWN_NOTE`."
        ),
        code(
            "by_town = None\n"
            "TOWN_NOTE = ''\n"
            "assert by_town is not None and len(TOWN_NOTE) > 15\n"
            "print(by_town, TOWN_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: группы и пропуски"),
        code(LOAD_DATA + "\n" + IMPORTS_MPL),
        md("### A. Закрепление"),
        md("## 1. Bar survived rate by pclass -> figures/surv_by_pclass_hw.png"),
        code(
            "from pathlib import Path as _P\n"
            "_P('figures').mkdir(exist_ok=True)\n"
            "p = None\n"
            "assert p is not None and _P(p).exists()\n"
            "print(p)"
        ),
        md("## 2. rates sex×pclass — женщина 3 класса vs мужчина 1"),
        code(
            "rate_f3 = None\n"
            "rate_m1 = None\n"
            "assert rate_f3 is not None and rate_m1 is not None\n"
            "assert 0 < float(rate_f3) < 1 and 0 < float(rate_m1) < 1\n"
            "print(rate_f3, rate_m1)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. Политика пропусков\n\n"
            "Выберите для финального отчёта политику по age (drop / median / separately) "
            "и обоснуйте `POLICY` (≥3 предложения)."
        ),
        code(
            "POLICY = ''\n"
            "assert len(POLICY) > 80\n"
            "print(POLICY)"
        ),
        md(
            "## 4. После drop_duplicates: изменилась ли доля survived?\n\n"
            "`rate_before`, `rate_after`, `CHANGED` (bool)."
        ),
        code(
            "rate_before = float(df['survived'].mean())\n"
            "rate_after = None\n"
            "CHANGED = None\n"
            "assert rate_after is not None and CHANGED is not None\n"
            "print(rate_before, rate_after, CHANGED)"
        ),
    )
    sol = nb(
        md("# Решения: группы\n\n" + SOL_BANNER),
        code(LOAD_DATA + "\n" + IMPORTS_MPL + "from pathlib import Path as _P\n_P('figures').mkdir(exist_ok=True)\n"),
        md("## Урок"),
        code(
            "plt.figure()\n"
            "df.loc[df['survived']==0, 'fare'].hist(bins=30, alpha=0.5, label='0')\n"
            "df.loc[df['survived']==1, 'fare'].hist(bins=30, alpha=0.5, label='1')\n"
            "plt.legend(); plt.tight_layout()\n"
            "fare_hist_path = _P('figures/fare_by_survived_hist.png'); plt.savefig(fare_hist_path); plt.close()\n"
            "FARE_HIST_NOTE = 'у выживших чаще более высокий fare, но распределения перекрываются'\n"
            "rates = df.groupby(['sex', 'pclass'])['survived'].mean().unstack()\n"
            "plt.figure(); df.groupby('who')['survived'].mean().plot(kind='bar'); plt.tight_layout()\n"
            "who_bar_path = _P('figures/survived_by_who.png'); plt.savefig(who_bar_path); plt.close()\n"
            "rate_A = float(df.dropna(subset=['age'])['survived'].mean())\n"
            "d2 = df.copy(); d2['age'] = d2['age'].fillna(d2['age'].median())\n"
            "mean_age_surv_B = float(d2.loc[d2['survived']==1, 'age'].mean())\n"
            "mean_age_dead_B = float(d2.loc[d2['survived']==0, 'age'].mean())\n"
            "WHEN_A = 'Когда вопрос именно о доле survived без искажения импутацией возраста'\n"
            "share_p1_all = float((df['pclass']==1).mean())\n"
            "share_p1_deck = float((df.dropna(subset=['deck'])['pclass']==1).mean())\n"
            "CAREFUL_CLAIM = 'Наблюдается ассоциация пола с выживаемостью; причинность из EDA не следует'\n"
            "rows = []\n"
            "for s in ('female', 'male'):\n"
            "    g = df[df['sex']==s]\n"
            "    rows.append({'group': f'sex={s}', 'n': len(g), 'survival_rate': g['survived'].mean()})\n"
            "for c in (1, 2, 3):\n"
            "    g = df[df['pclass']==c]\n"
            "    rows.append({'group': f'pclass={c}', 'n': len(g), 'survival_rate': g['survived'].mean()})\n"
            "summary = pd.DataFrame(rows)\n"
            "by_town = df.dropna(subset=['embark_town']).groupby('embark_town')['survived'].mean()\n"
            "TOWN_NOTE = 'Cherbourg выше — связать с долей 1 класса, не с магией города'\n"
            "print(rates, summary)"
        ),
        md("## ДЗ"),
        code(
            "plt.figure(); df.groupby('pclass')['survived'].mean().plot(kind='bar'); plt.tight_layout()\n"
            "p = _P('figures/surv_by_pclass_hw.png'); plt.savefig(p); plt.close()\n"
            "rate_f3 = float(df.loc[(df['sex']=='female')&(df['pclass']==3), 'survived'].mean())\n"
            "rate_m1 = float(df.loc[(df['sex']=='male')&(df['pclass']==1), 'survived'].mean())\n"
            "POLICY = (\n"
            "    'В отчёте: доли survived — на полной таблице без импутации age. '\n"
            "    'Описания возраста — отдельно на non-NA или с пометкой median fill. '\n"
            "    'deck не используем как группу из-за огромной доли NA.'\n"
            ")\n"
            "rate_after = float(df.drop_duplicates()['survived'].mean())\n"
            "CHANGED = abs(rate_after - df['survived'].mean()) > 1e-12\n"
            "print(rate_f3, rate_m1, CHANGED)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson07() -> None:
    """Pair 23: EDA report draft + submit (old 28+29)."""
    base = "lessons/07_eda_report"
    lesson = nb(
        md(
            "# EDA-отчёт: сборка и сдача (без модели)\n\n"
            "Одна пара: каркас ответа обществу + чек-лист PROJECT + рефлексия. **Без** sklearn / fit."
        ),
        code(LOAD_DATA + "\n" + IMPORTS_MPL + "from pathlib import Path as _P\n_P('figures').mkdir(exist_ok=True)\n"),
        md(
            "## 1. Паспорт данных\n\n"
            "Заполните: `n_rows`, `n_cols`, `source_note` (seaborn Titanic CSV), `outcome_col`."
        ),
        code(
            "n_rows = n_cols = None\n"
            "source_note = ''\n"
            "outcome_col = ''\n"
            "assert n_rows == 891 and n_cols == 15\n"
            "assert 'seaborn' in source_note.lower() or 'titanic' in source_note.lower()\n"
            "assert outcome_col == 'survived'\n"
            "print(n_rows, n_cols, source_note)"
        ),
        md(
            "## 2. Ключевые доли\n\n"
            "Таблица/словарь `headline_rates`: overall, female, male, pclass1, pclass3."
        ),
        code(
            "headline_rates = {}\n"
            "assert set(headline_rates) >= {'overall', 'female', 'male', 'pclass1', 'pclass3'}\n"
            "assert all(isinstance(float(v), float) for v in headline_rates.values())\n"
            "print(headline_rates)"
        ),
        md(
            "## 3. Описательная статистика age/fare\n\n"
            "`desc = df[['age','fare']].describe()` — сохранить в переменную и показать."
        ),
        code(
            "desc = None\n"
            "assert desc is not None\n"
            "print(desc)"
        ),
        md(
            "## 4. Два обязательных графика\n\n"
            "1) bar survival by sex -> `figures/report_surv_sex.png`\n"
            "2) boxplot age by pclass -> `figures/report_age_pclass.png`"
        ),
        code(
            "fig1 = fig2 = None\n"
            "assert fig1 is not None and fig2 is not None\n"
            "assert _P(fig1).exists() and _P(fig2).exists()\n"
            "print(fig1, fig2)"
        ),
        md(
            "## 5. Пропуски, bias, черновик вывода\n\n"
            "`MISSING_SECTION`, `BIAS_SECTION`, `DRAFT_CONCLUSION` (без fit/sklearn)."
        ),
        code(
            "MISSING_SECTION = ''\n"
            "BIAS_SECTION = ''\n"
            "DRAFT_CONCLUSION = ''\n"
            "assert len(MISSING_SECTION) > 60 and len(BIAS_SECTION) > 60\n"
            "assert len(DRAFT_CONCLUSION) > 100\n"
            "assert 'fit' not in DRAFT_CONCLUSION.lower() and 'sklearn' not in DRAFT_CONCLUSION.lower()\n"
            "print(DRAFT_CONCLUSION)"
        ),
        md(
            "## 6. Запрет модели и чек-лист артефакта\n\n"
            "`USED_MODEL = False`. Флаги `artifact_ok` из PROJECT.md: "
            "numbers, figures, missing, bias, conclusion, no_causality_overclaim."
        ),
        code(
            "USED_MODEL = True  # поставьте False\n"
            "artifact_ok = {\n"
            "    'numbers': False,\n"
            "    'figures': False,\n"
            "    'missing': False,\n"
            "    'bias': False,\n"
            "    'conclusion': False,\n"
            "    'no_causality_overclaim': False,\n"
            "}\n"
            "assert USED_MODEL is False\n"
            "assert all(artifact_ok.values())\n"
            "print(artifact_ok)"
        ),
        md(
            "## 7. Финальные числа и список figures\n\n"
            "`final_rates` (≥5 ключей); `figure_files` — ≥2 имени `.png`."
        ),
        code(
            "final_rates = {}\n"
            "figure_files = []\n"
            "assert len(final_rates) >= 5\n"
            "assert len(figure_files) >= 2\n"
            "assert all(isinstance(x, str) and x.endswith('.png') for x in figure_files)\n"
            "print({k: round(float(v), 3) for k, v in final_rates.items()}, figure_files)"
        ),
        md(
            "## 8. Рефлексия, мост к M4, READY\n\n"
            "`REFLECTION` (≥100 символов); `NEXT_MODULE` — риск kNN без EDA; "
            "`READY = True` только если отчёт + figures готовы к сдаче."
        ),
        code(
            "REFLECTION = ''\n"
            "NEXT_MODULE = ''\n"
            "READY = False\n"
            "assert len(REFLECTION) > 100 and len(NEXT_MODULE) > 30\n"
            "assert READY is True\n"
            "print(REFLECTION, NEXT_MODULE)"
        ),
    )
    hw = nb(
        md("# ДЗ: полировка EDA-отчёта"),
        code(LOAD_DATA),
        md("### A. Закрепление"),
        md("## 1. Markdown-черновик `report_md` с ## Данные / ## Находки / ## Ограничения / ## Вывод"),
        code(
            "report_md = ''\n"
            "assert '## Данные' in report_md and '## Вывод' in report_md\n"
            "assert '## Ограничения' in report_md\n"
            "assert len(report_md) > 300\n"
            "print(report_md[:500])"
        ),
        md("## 2. Точные overall и female rates (3 знака)"),
        code(
            "overall = None\n"
            "female = None\n"
            "assert overall is not None and female is not None\n"
            "assert 0.3 < float(overall) < 0.5\n"
            "assert float(female) > float(overall)\n"
            "print(round(float(overall), 3), round(float(female), 3))"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. Перепишите одно место с риском причинности → `FIXED_SENTENCE`.\n\n"
            "`NO_MODEL_CONFIRM = True` только если текст чист от намёков на обучение классификатора."
        ),
        code(
            "FIXED_SENTENCE = ''\n"
            "NO_MODEL_CONFIRM = False\n"
            "assert len(FIXED_SENTENCE) > 40\n"
            "assert NO_MODEL_CONFIRM is True\n"
            "print(FIXED_SENTENCE)"
        ),
    )
    sol = nb(
        md("# Решения: EDA report\n\n" + SOL_BANNER),
        code(LOAD_DATA + "\n" + IMPORTS_MPL + "from pathlib import Path as _P\n_P('figures').mkdir(exist_ok=True)\n"),
        md("## Урок"),
        code(
            "n_rows, n_cols = df.shape\n"
            "source_note = 'seaborn load_dataset(titanic) -> data/titanic.csv'\n"
            "outcome_col = 'survived'\n"
            "headline_rates = {\n"
            "    'overall': float(df['survived'].mean()),\n"
            "    'female': float(df.loc[df['sex']=='female','survived'].mean()),\n"
            "    'male': float(df.loc[df['sex']=='male','survived'].mean()),\n"
            "    'pclass1': float(df.loc[df['pclass']==1,'survived'].mean()),\n"
            "    'pclass3': float(df.loc[df['pclass']==3,'survived'].mean()),\n"
            "}\n"
            "desc = df[['age','fare']].describe()\n"
            "plt.figure(); df.groupby('sex')['survived'].mean().plot(kind='bar'); plt.tight_layout()\n"
            "fig1 = _P('figures/report_surv_sex.png'); plt.savefig(fig1); plt.close()\n"
            "plt.figure(); df.boxplot(column='age', by='pclass'); plt.suptitle(''); plt.tight_layout()\n"
            "fig2 = _P('figures/report_age_pclass.png'); plt.savefig(fig2); plt.close()\n"
            "MISSING_SECTION = 'age ~177 NA, deck большинство NA, embarked 2; deck не группируем; age описываем отдельно'\n"
            "BIAS_SECTION = 'Подвыборки по deck/классу смещают доли; разница групп — ассоциация, не доказанная причина'\n"
            "DRAFT_CONCLUSION = (\n"
            "    f\"Женщины выживали чаще мужчин ({headline_rates['female']:.0%} vs {headline_rates['male']:.0%}); \"\n"
            "    f\"1 класс выше 3 ({headline_rates['pclass1']:.0%} vs {headline_rates['pclass3']:.0%}). \"\n"
            "    'Вывод описательный по данной таблице; модель не строилась; есть пропуски и риск bias.'\n"
            ")\n"
            "USED_MODEL = False\n"
            "artifact_ok = {k: True for k in ('numbers','figures','missing','bias','conclusion','no_causality_overclaim')}\n"
            "final_rates = dict(headline_rates)\n"
            "figure_files = ['report_surv_sex.png', 'report_age_pclass.png']\n"
            "REFLECTION = (\n"
            "    'До модуля таблица казалась готовой к fit. Теперь сначала доли, пропуски, bias и формулировки без причинности. '\n"
            "    'Выбросы fare и пустой deck показывают, что «удобный срез» врёт. '\n"
            "    'Отчёт обществу — про ограничения так же, как про находки.'\n"
            ")\n"
            "NEXT_MODULE = 'Без EDA kNN получит мусорные признаки и смещённую оценку качества'\n"
            "READY = True\n"
            "print(final_rates, READY)"
        ),
        md("## ДЗ"),
        code(
            "report_md = (\n"
            "    '## Данные\\nИсточник: seaborn Titanic, 891x15. Цель описания: survived.\\n\\n'\n"
            "    '## Находки\\nЖенщины и 1 класс — выше доля survived. См. figures/report_surv_sex.png.\\n\\n'\n"
            "    '## Ограничения\\nПропуски age/deck; sampling bias на срезах; нет причинности.\\n\\n'\n"
            "    '## Вывод\\nОтвет обществу — описательный, без обученной модели.'\n"
            ")\n"
            "overall = float(df['survived'].mean())\n"
            "female = float(df.loc[df['sex']=='female','survived'].mean())\n"
            "FIXED_SENTENCE = 'Наблюдается более высокая доля выживших среди женщин в этой таблице; причина из EDA не установлена'\n"
            "NO_MODEL_CONFIRM = True\n"
            "print(len(report_md), overall, female)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def main() -> None:
    if not DATA_CSV.exists():
        raise SystemExit(f"Missing {DATA_CSV}. See data/README.md for Titanic CSV export.")
    add_lesson01()
    add_lesson02()
    add_lesson03()
    add_lesson04()
    add_lesson05()
    add_lesson06()
    add_lesson07()
    lesson_dirs = [
        "lessons/01_load_inspect_paths",
        "lessons/02_practice_inspect",
        "lessons/03_mean_median_std",
        "lessons/04_practice_boxplot",
        "lessons/05_bias_clt_missing",
        "lessons/06_practice_groups",
        "lessons/07_eda_report",
    ]
    for rel, notebook in NOTEBOOKS.items():
        write(rel, notebook)
    for d in lesson_dirs:
        copy_csv(d)
    print(f"done: {len(NOTEBOOKS)} notebooks in {len(lesson_dirs)} lessons")


if __name__ == "__main__":
    main()
