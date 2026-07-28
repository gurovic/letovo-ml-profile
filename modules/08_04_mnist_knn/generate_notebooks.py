#!/usr/bin/env python3
"""Generate lesson notebooks for module 08_04 (KTP pairs 24-29).

Source of truth for .ipynb: edit this file, then run it.
Data: data/digits.csv (sklearn load_digits export, 1797 x 8x8, see data/README.md).
Pattern: stubs + asserts in lesson/homework; full solutions.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_CSV = ROOT / "data" / "digits.csv"

LOAD_DATA = (
    "from pathlib import Path\n"
    "import pandas as pd\n\n\n"
    "def find_digits_csv() -> Path:\n"
    "    for p in (Path('digits.csv'), Path('../../data/digits.csv'), Path('../data/digits.csv')):\n"
    "        if p.exists():\n"
    "            return p.resolve()\n"
    "    raise FileNotFoundError('digits.csv не найден — положите файл рядом с ноутбуком')\n\n\n"
    "DIGITS_PATH = find_digits_csv()\n"
    "df = pd.read_csv(DIGITS_PATH)\n"
    "PIXELS = [c for c in df.columns if c.startswith('p')]\n"
)

SHOW_DIGIT = (
    "import matplotlib.pyplot as plt\n\n\n"
    "def show_digit(row, title=''):\n"
    "    \"\"\"Одна строка таблицы -> картинка 8x8.\"\"\"\n"
    "    values = [int(v) for v in row[PIXELS]]\n"
    "    grid = [values[i * 8:(i + 1) * 8] for i in range(8)]\n"
    "    plt.imshow(grid, cmap='gray_r')\n"
    "    plt.title(title)\n"
    "    plt.axis('off')\n"
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


def copy_csv(lesson_dir: str) -> None:
    dest = ROOT / lesson_dir / "digits.csv"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DATA_CSV, dest)
    print("copied csv ->", dest)


NOTEBOOKS: dict[str, dict] = {}

LESSON_DIRS = [
    "lessons/01_probability_frequency",
    "lessons/02_practice_split",
    "lessons/03_knn_scaling",
    "lessons/04_practice_knn_baseline",
    "lessons/05_accuracy_f1_val",
    "lessons/06_practice_search_metrics",
]


def add_lesson01() -> None:
    """Pair 24: частота класса, baseline, перебор вариантов."""
    base = "lessons/01_probability_frequency"
    lesson = nb(
        md(
            "# Частота цифры и перебор вариантов\n\n"
            "Почтовый сервис сканирует индексы: каждая картинка 8×8 — одна цифра. "
            "Прежде чем распознавать, надо знать, что вообще приходит на вход."
        ),
        code(LOAD_DATA + "\n" + SHOW_DIGIT),
        md(
            "## 1. Размер таблицы\n\n"
            "Сколько картинок, сколько пикселей в одной картинке, сколько разных цифр.\n\n"
            "**How:** `df.shape`, `len(PIXELS)`, `df['label'].nunique()`."
        ),
        code(
            "n_images = None\n"
            "n_pixels = None\n"
            "n_classes = None\n"
            "assert n_images is not None and n_pixels is not None and n_classes is not None\n"
            "assert n_images == 1797\n"
            "assert n_pixels == 64 and n_classes == 10\n"
            "print(n_images, n_pixels, n_classes)"
        ),
        md(
            "## 2. Одна картинка — это 64 числа\n\n"
            "Нарисуйте строку 17: `show_digit(df.loc[17])`. Посчитайте, сколько пикселей "
            "в этой строке равны 0 (белый фон) -> `n_zero_17`.\n\n"
            "**Вопрос:** почему пустых пикселей так много?"
        ),
        code(
            "# show_digit(df.loc[17], title='строка 17')\n"
            "n_zero_17 = None\n"
            "assert n_zero_17 is not None\n"
            "assert 0 < int(n_zero_17) < 64\n"
            "print('нулевых пикселей:', n_zero_17)"
        ),
        md(
            "## 3. Частота цифры = её вероятность в потоке\n\n"
            "`class_counts` — сколько картинок каждой цифры; `class_share` — доля каждой цифры "
            "(частота, делённая на общее число).\n\n"
            "**How:** `value_counts()` и `value_counts(normalize=True)`.\n\n"
            "**Checkpoint:** почему сумма долей равна 1?"
        ),
        code(
            "class_counts = None\n"
            "class_share = None\n"
            "assert class_counts is not None and class_share is not None\n"
            "assert len(class_share) == 10\n"
            "assert abs(float(class_share.sum()) - 1.0) < 1e-9\n"
            "print(class_share.sort_index().round(3))"
        ),
        md(
            "## 4. Baseline: всегда отвечать самой частой цифрой\n\n"
            "Самая частая цифра -> `top_digit`; её доля -> `baseline_accuracy` "
            "(так часто угадает распознаватель, который всегда отвечает одно и то же).\n\n"
            "**Зачем:** любую модель сравниваем с этим числом, иначе «90% точности» ни о чём не говорит."
        ),
        code(
            "top_digit = None\n"
            "baseline_accuracy = None\n"
            "assert top_digit is not None and baseline_accuracy is not None\n"
            "assert int(top_digit) in range(10)\n"
            "assert 0.09 < float(baseline_accuracy) < 0.12\n"
            "print(top_digit, round(float(baseline_accuracy), 3))"
        ),
        md(
            "## 5. Вероятность события «1 или 7»\n\n"
            "Индексы часто путают 1 и 7. Какова доля картинок, где цифра — 1 **или** 7? "
            "-> `p_1_or_7`.\n\n"
            "**How:** сложить две доли или посчитать долю строк по условию `isin([1, 7])`."
        ),
        code(
            "p_1_or_7 = None\n"
            "assert p_1_or_7 is not None\n"
            "assert 0.15 < float(p_1_or_7) < 0.25\n"
            "print(round(float(p_1_or_7), 3))"
        ),
        md(
            "## 6. Сколько пар пикселей можно сравнить\n\n"
            "Сколько существует **пар разных** пикселей из 64 (порядок не важен)? "
            "Посчитайте **перебором** двумя вложенными циклами -> `n_pairs`.\n\n"
            "Сверьте с формулой n·(n−1)/2 -> `n_pairs_formula`.\n\n"
            "**Связь:** так же перебираются варианты настроек распознавателя."
        ),
        code(
            "n_pairs = 0\n"
            "# for i in range(len(PIXELS)):\n"
            "#     for j in range(...):\n"
            "#         n_pairs += 1\n"
            "n_pairs_formula = None\n"
            "assert n_pairs == 2016\n"
            "assert n_pairs_formula is not None and int(n_pairs_formula) == n_pairs\n"
            "print(n_pairs)"
        ),
        md(
            "## 7. Сколько настроек надо проверить (правило произведения)\n\n"
            "Соберите список `configs` из всех сочетаний: число соседей из `K_VALUES` "
            "и набор признаков из `FEATURE_SETS` (перебор двумя циклами, каждый элемент — кортеж).\n\n"
            "**Правило произведения:** вариантов столько, сколько произведение длин."
        ),
        code(
            "K_VALUES = [1, 3, 5, 7, 9]\n"
            "FEATURE_SETS = ['все 64 пикселя', 'верхняя половина', 'сумма яркости']\n"
            "configs = []\n"
            "# соберите кортежи (k, набор)\n"
            "assert len(configs) == len(K_VALUES) * len(FEATURE_SETS)\n"
            "assert all(isinstance(c, tuple) and len(c) == 2 for c in configs)\n"
            "print(len(configs), configs[:3])"
        ),
        md(
            "## 8. Эксперимент: поток изменился\n\n"
            "Представьте участок, где почти все индексы начинаются с 0 и 1. Возьмите только строки "
            "с цифрами 0 и 1 -> `stream`; посчитайте новый `baseline_stream` (доля самой частой цифры там).\n\n"
            "Ответьте в `BIAS_NOTE`: почему распознаватель, оценённый на всей таблице, "
            "может вести себя иначе на таком участке. **Готового ответа нет.**"
        ),
        code(
            "stream = None\n"
            "baseline_stream = None\n"
            "BIAS_NOTE = ''\n"
            "assert stream is not None and baseline_stream is not None\n"
            "assert float(baseline_stream) > 0.4\n"
            "assert len(BIAS_NOTE) > 40\n"
            "print(len(stream), round(float(baseline_stream), 3), BIAS_NOTE)"
        ),
        md(
            "## 9. Расширение: две картинки подряд\n\n"
            "Если две картинки берут независимо, вероятность, что они **одной** цифры, — "
            "сумма квадратов долей. Посчитайте `p_same` и сравните с 1/10.\n\n"
            "**Вопрос:** почему это не то же самое, что «вероятность угадать»?"
        ),
        code(
            "p_same = None\n"
            "assert p_same is not None\n"
            "assert 0.09 < float(p_same) < 0.12\n"
            "print(round(float(p_same), 4))"
        ),
    )
    hw = nb(
        md("# ДЗ: частоты и перебор"),
        code(LOAD_DATA),
        md("### A. Закрепление"),
        md(
            "## 1. Частоты в первых 500 строках\n\n"
            "Доли цифр в `df.head(500)` -> `share_500`; самая частая цифра -> `top_500`."
        ),
        code(
            "share_500 = None\n"
            "top_500 = None\n"
            "assert share_500 is not None and top_500 is not None\n"
            "assert len(share_500) == 10\n"
            "assert abs(float(share_500.sum()) - 1.0) < 1e-9\n"
            "assert int(top_500) in range(10)\n"
            "print(top_500)"
        ),
        md(
            "## 2. Baseline на подвыборке\n\n"
            "Доля самой частой цифры в этих 500 строках -> `baseline_500`. "
            "Сравните с baseline на всей таблице -> `COMPARE_500` (одна фраза с двумя числами)."
        ),
        code(
            "baseline_500 = None\n"
            "COMPARE_500 = ''\n"
            "assert baseline_500 is not None and 0 < float(baseline_500) < 0.3\n"
            "assert len(COMPARE_500) > 15\n"
            "print(round(float(baseline_500), 3), COMPARE_500)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. Сколько индексов из трёх разных цифр\n\n"
            "Почтовый индекс из **трёх разных** цифр 0–9. Посчитайте перебором (три вложенных цикла) "
            "число таких индексов -> `n_codes`. Проверьте, что перебор совпал с 10·9·8."
        ),
        code(
            "n_codes = 0\n"
            "# три вложенных цикла по range(10) с условием «все разные»\n"
            "assert n_codes == 720\n"
            "print(n_codes)"
        ),
        md(
            "## 4. Зачем baseline\n\n"
            "Напишите в `WHY_BASELINE` (≥120 символов), почему точность распознавателя "
            "бессмысленно обсуждать без baseline. Придумайте пример потока, "
            "где 90% точности — плохой результат."
        ),
        code(
            "WHY_BASELINE = ''\n"
            "assert len(WHY_BASELINE) > 120\n"
            "print(WHY_BASELINE)"
        ),
    )
    sol = nb(
        md("# Решения: частота и перебор\n\n" + SOL_BANNER),
        code(LOAD_DATA + "\n" + SHOW_DIGIT),
        md("## Урок. 1–2. Размер и картинка"),
        code(
            "n_images, n_cols = df.shape\n"
            "n_pixels = len(PIXELS)\n"
            "n_classes = int(df['label'].nunique())\n"
            "print(n_images, n_pixels, n_classes)\n"
            "show_digit(df.loc[17], title=f\"строка 17: цифра {df.loc[17, 'label']}\")\n"
            "n_zero_17 = int((df.loc[17, PIXELS] == 0).sum())\n"
            "print('нулевых пикселей:', n_zero_17)"
        ),
        md("## Урок. 3–5. Частоты, baseline, событие «1 или 7»"),
        code(
            "class_counts = df['label'].value_counts()\n"
            "class_share = df['label'].value_counts(normalize=True)\n"
            "top_digit = int(class_share.idxmax())\n"
            "baseline_accuracy = float(class_share.max())\n"
            "p_1_or_7 = float(df['label'].isin([1, 7]).mean())\n"
            "print(class_share.sort_index().round(3))\n"
            "print(top_digit, round(baseline_accuracy, 3), round(p_1_or_7, 3))"
        ),
        md("## Урок. 6–7. Перебор пар и настроек"),
        code(
            "n_pairs = 0\n"
            "for i in range(len(PIXELS)):\n"
            "    for j in range(i + 1, len(PIXELS)):\n"
            "        n_pairs += 1\n"
            "n_pairs_formula = len(PIXELS) * (len(PIXELS) - 1) // 2\n"
            "K_VALUES = [1, 3, 5, 7, 9]\n"
            "FEATURE_SETS = ['все 64 пикселя', 'верхняя половина', 'сумма яркости']\n"
            "configs = []\n"
            "for k in K_VALUES:\n"
            "    for fs in FEATURE_SETS:\n"
            "        configs.append((k, fs))\n"
            "print(n_pairs, n_pairs_formula, len(configs))"
        ),
        md("## Урок. 8–9. Смещённый поток и две картинки"),
        code(
            "stream = df[df['label'].isin([0, 1])]\n"
            "baseline_stream = float(stream['label'].value_counts(normalize=True).max())\n"
            "BIAS_NOTE = (\n"
            "    'На таком участке почти нет других цифр: глупый ответ «0» уже даёт ~50%. '\n"
            "    'Точность, измеренная на равномерной таблице, не переносится на смещённый поток.'\n"
            ")\n"
            "p_same = float((df['label'].value_counts(normalize=True) ** 2).sum())\n"
            "print(len(stream), round(baseline_stream, 3), round(p_same, 4))"
        ),
        md("## ДЗ. 1–4"),
        code(
            "head = df.head(500)\n"
            "share_500 = head['label'].value_counts(normalize=True)\n"
            "top_500 = int(share_500.idxmax())\n"
            "baseline_500 = float(share_500.max())\n"
            "COMPARE_500 = (\n"
            "    f'на 500 строках baseline {baseline_500:.3f}, '\n"
            "    f\"на всей таблице {df['label'].value_counts(normalize=True).max():.3f}\"\n"
            ")\n"
            "n_codes = 0\n"
            "for a in range(10):\n"
            "    for b in range(10):\n"
            "        for c in range(10):\n"
            "            if a != b and b != c and a != c:\n"
            "                n_codes += 1\n"
            "WHY_BASELINE = (\n"
            "    'Точность без опоры ни о чём не говорит: если 90% потока — цифра 1, '\n"
            "    'распознаватель, который всегда отвечает 1, даёт 90% и не умеет ничего. '\n"
            "    'Сравнение с baseline показывает, что модель добавила к простому правилу.'\n"
            ")\n"
            "print(top_500, round(baseline_500, 3), n_codes, len(WHY_BASELINE))"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson02() -> None:
    """Pair 25: практика — вероятность, разбиение выборки."""
    base = "lessons/02_practice_split"
    lesson = nb(
        md(
            "# Практика: доли цифр и разбиение выборки\n\n"
            "Делим таблицу на **обучающую** и **проверочную** части и следим, "
            "чтобы доли цифр не разъехались."
        ),
        code(LOAD_DATA),
        md(
            "## 1. Разбиение руками\n\n"
            "Перемешайте строки: `order = df.sample(frac=1, random_state=0).index`. "
            "Первые 75% номеров -> `train_idx`, остальные -> `test_idx`.\n\n"
            "**Зачем seed:** без `random_state` каждый запуск даёт другое разбиение и другие числа в отчёте."
        ),
        code(
            "order = None\n"
            "train_idx = None\n"
            "test_idx = None\n"
            "assert order is not None and train_idx is not None and test_idx is not None\n"
            "assert len(train_idx) == 1347 and len(test_idx) == 450\n"
            "print(len(train_idx), len(test_idx))"
        ),
        md(
            "## 2. Части не пересекаются\n\n"
            "Проверьте, что ни один номер не попал в обе части: `n_overlap` — сколько номеров "
            "из `train_idx` встречается в `test_idx`.\n\n"
            "**How:** `train_idx.isin(test_idx).sum()`."
        ),
        code(
            "n_overlap = None\n"
            "n_total = None\n"
            "assert n_overlap is not None and int(n_overlap) == 0\n"
            "assert n_total is not None and int(n_total) == len(df)\n"
            "print(n_overlap, n_total)"
        ),
        md(
            "## 3. Доли цифр в двух частях\n\n"
            "`train_df` и `test_df` — строки по этим номерам (`df.loc[...]`). "
            "Посчитайте доли цифр в каждой части и максимальное расхождение по цифрам -> `max_gap`.\n\n"
            "**How:** две `value_counts(normalize=True).sort_index()`, затем `(a - b).abs().max()`."
        ),
        code(
            "train_df = None\n"
            "test_df = None\n"
            "max_gap = None\n"
            "assert train_df is not None and test_df is not None\n"
            "assert len(train_df) + len(test_df) == len(df)\n"
            "assert max_gap is not None and 0 < float(max_gap) < 0.1\n"
            "print(round(float(max_gap), 4))"
        ),
        md(
            "## 4. То же самое библиотекой\n\n"
            "`train_test_split` из модуля 2: `test_size=0.25`, `random_state=0`. "
            "Запишите размеры -> `n_tr_lib`, `n_te_lib` и убедитесь, что они совпали с ручным разбиением."
        ),
        code(
            "from sklearn.model_selection import train_test_split\n\n"
            "n_tr_lib = None\n"
            "n_te_lib = None\n"
            "assert n_tr_lib == len(train_idx) and n_te_lib == len(test_idx)\n"
            "print(n_tr_lib, n_te_lib)"
        ),
        md(
            "## 5. Разбиение с сохранением долей\n\n"
            "Тот же вызов с `stratify=df['label']`. Посчитайте расхождение долей -> `max_gap_strat` "
            "и сравните с `max_gap` из блока 3.\n\n"
            "**Вопрос:** зачем сохранять доли, если разбиение и так случайное?"
        ),
        code(
            "max_gap_strat = None\n"
            "assert max_gap_strat is not None\n"
            "assert float(max_gap_strat) < float(max_gap)\n"
            "print(round(float(max_gap_strat), 4), round(float(max_gap), 4))"
        ),
        md(
            "## 6. Доля цифры при условии\n\n"
            "`n_dark` — сколько пикселей картинки ярче 8 (сколько «чернил»). Разделите таблицу "
            "на картинки с `n_dark` выше медианы и остальные.\n\n"
            "Посчитайте долю цифры 8 в каждой части -> `p_eight_dark`, `p_eight_light`.\n\n"
            "В `COND_NOTE` объясните результат: чем восьмёрка отличается от других цифр по чернилам "
            "и как это использует поиск ближайших соседей."
        ),
        code(
            "n_dark = (df[PIXELS] > 8).sum(axis=1)\n"
            "p_eight_dark = None\n"
            "p_eight_light = None\n"
            "COND_NOTE = ''\n"
            "assert p_eight_dark is not None and p_eight_light is not None\n"
            "assert float(p_eight_dark) > 1.5 * float(p_eight_light)\n"
            "assert len(COND_NOTE) > 40\n"
            "print(round(float(p_eight_dark), 3), round(float(p_eight_light), 3), COND_NOTE)"
        ),
        md(
            "## 7. Проверочная часть — не для подглядывания\n\n"
            "Возьмите крошечную проверочную часть: `tiny = df.sample(20, random_state=11)`. "
            "Доля цифры 3 в ней -> `p_three_tiny`; доля в полной таблице -> `p_three_all`.\n\n"
            "Запишите в `TINY_NOTE`, почему по 20 картинкам нельзя судить о качестве распознавателя."
        ),
        code(
            "tiny = None\n"
            "p_three_tiny = None\n"
            "p_three_all = None\n"
            "TINY_NOTE = ''\n"
            "assert tiny is not None and len(tiny) == 20\n"
            "assert p_three_tiny is not None and p_three_all is not None\n"
            "assert len(TINY_NOTE) > 50\n"
            "print(round(float(p_three_tiny), 3), round(float(p_three_all), 3))"
        ),
        md(
            "## 8. Эксперимент: пять разных разбиений\n\n"
            "Для `random_state` 0…4 посчитайте долю цифры 3 в проверочной части (25%) -> список `spreads` "
            "(5 чисел). Найдите разницу между максимумом и минимумом -> `spread_range`.\n\n"
            "Вывод в `SEED_NOTE`: что это значит для сравнения двух распознавателей. **Готового ответа нет.**"
        ),
        code(
            "spreads = []\n"
            "spread_range = None\n"
            "SEED_NOTE = ''\n"
            "assert len(spreads) == 5\n"
            "assert spread_range is not None and float(spread_range) > 0\n"
            "assert len(SEED_NOTE) > 50\n"
            "print([round(float(s), 3) for s in spreads], round(float(spread_range), 3))"
        ),
        md(
            "## 9. Расширение: две проверочные части\n\n"
            "Разбейте таблицу на **три** части: 60% / 20% / 20% (обучение, проверка, финал). "
            "Запишите размеры -> `sizes_three` (список из трёх чисел, сумма = 1797).\n\n"
            "На паре 28 эта третья часть понадобится, чтобы честно выбрать число соседей."
        ),
        code(
            "sizes_three = []\n"
            "assert len(sizes_three) == 3\n"
            "assert sum(int(s) for s in sizes_three) == len(df)\n"
            "assert min(int(s) for s in sizes_three) > 300\n"
            "print(sizes_three)"
        ),
    )
    hw = nb(
        md("# ДЗ: разбиение и доли"),
        code(LOAD_DATA),
        md("### A. Закрепление"),
        md(
            "## 1. Пополам\n\n"
            "Разбейте таблицу руками на две равные части (`random_state=1`): "
            "`half_a_idx`, `half_b_idx`. Проверьте, что пересечения нет -> `n_overlap`."
        ),
        code(
            "half_a_idx = None\n"
            "half_b_idx = None\n"
            "n_overlap = None\n"
            "assert half_a_idx is not None and half_b_idx is not None\n"
            "assert abs(len(half_a_idx) - len(half_b_idx)) <= 1\n"
            "assert n_overlap is not None and int(n_overlap) == 0\n"
            "print(len(half_a_idx), len(half_b_idx))"
        ),
        md(
            "## 2. Доля цифры 9 в двух частях\n\n"
            "`p_nine_a`, `p_nine_b` и их разница -> `gap_nine`."
        ),
        code(
            "p_nine_a = None\n"
            "p_nine_b = None\n"
            "gap_nine = None\n"
            "assert p_nine_a is not None and p_nine_b is not None and gap_nine is not None\n"
            "assert 0 < float(p_nine_a) < 0.2 and 0 < float(p_nine_b) < 0.2\n"
            "assert float(gap_nine) >= 0\n"
            "print(round(float(p_nine_a), 3), round(float(p_nine_b), 3), round(float(gap_nine), 3))"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. Сохранение долей\n\n"
            "Сделайте два разбиения `train_test_split` (обычное и со `stratify`) для `random_state=2`. "
            "Посчитайте максимальное расхождение долей в каждом -> `gap_plain`, `gap_strat`, "
            "и объясните в `STRAT_NOTE`, когда разница важна."
        ),
        code(
            "gap_plain = None\n"
            "gap_strat = None\n"
            "STRAT_NOTE = ''\n"
            "assert gap_plain is not None and gap_strat is not None\n"
            "assert len(STRAT_NOTE) > 60\n"
            "print(round(float(gap_plain), 4), round(float(gap_strat), 4), STRAT_NOTE)"
        ),
        md(
            "## 4. Почему нельзя настраивать по проверочной части\n\n"
            "Напишите в `WHY_NOT_TEST` (≥150 символов) на примере почтового сервиса: "
            "что произойдёт, если каждый раз подкручивать распознаватель, пока не понравится "
            "результат на проверочных картинках."
        ),
        code(
            "WHY_NOT_TEST = ''\n"
            "assert len(WHY_NOT_TEST) > 150\n"
            "print(WHY_NOT_TEST)"
        ),
    )
    sol = nb(
        md("# Решения: разбиение выборки\n\n" + SOL_BANNER),
        code(LOAD_DATA + "\nfrom sklearn.model_selection import train_test_split\n"),
        md("## Урок. 1–3. Ручное разбиение"),
        code(
            "order = df.sample(frac=1, random_state=0).index\n"
            "n_train = int(len(df) * 0.75)\n"
            "train_idx, test_idx = order[:n_train], order[n_train:]\n"
            "n_overlap = int(train_idx.isin(test_idx).sum())\n"
            "n_total = len(train_idx) + len(test_idx)\n"
            "train_df, test_df = df.loc[train_idx], df.loc[test_idx]\n"
            "share_tr = train_df['label'].value_counts(normalize=True).sort_index()\n"
            "share_te = test_df['label'].value_counts(normalize=True).sort_index()\n"
            "max_gap = float((share_tr - share_te).abs().max())\n"
            "print(len(train_idx), len(test_idx), n_overlap, round(max_gap, 4))"
        ),
        md("## Урок. 4–5. Библиотека и stratify"),
        code(
            "tr, te = train_test_split(df, test_size=0.25, random_state=0)\n"
            "n_tr_lib, n_te_lib = len(tr), len(te)\n"
            "tr_s, te_s = train_test_split(df, test_size=0.25, random_state=0, stratify=df['label'])\n"
            "gap_s = (tr_s['label'].value_counts(normalize=True).sort_index()\n"
            "         - te_s['label'].value_counts(normalize=True).sort_index()).abs().max()\n"
            "max_gap_strat = float(gap_s)\n"
            "print(n_tr_lib, n_te_lib, round(max_gap_strat, 4), round(max_gap, 4))"
        ),
        md("## Урок. 6–7. Условная доля и крошечная проверка"),
        code(
            "n_dark = (df[PIXELS] > 8).sum(axis=1)\n"
            "dark = df[n_dark > n_dark.median()]\n"
            "light = df[n_dark <= n_dark.median()]\n"
            "p_eight_dark = float((dark['label'] == 8).mean())\n"
            "p_eight_light = float((light['label'] == 8).mean())\n"
            "COND_NOTE = (\n"
            "    'Восьмёрка состоит из двух замкнутых петель, чернил на неё уходит больше: '\n"
            "    'среди «жирных» картинок её доля примерно втрое выше. Знание признака меняет '\n"
            "    'вероятность цифры — на этом и работает поиск похожих картинок.'\n"
            ")\n"
            "tiny = df.sample(20, random_state=11)\n"
            "p_three_tiny = float((tiny['label'] == 3).mean())\n"
            "p_three_all = float((df['label'] == 3).mean())\n"
            "TINY_NOTE = (\n"
            "    'На 20 картинках одна ошибка сдвигает долю на 5 процентных пунктов: '\n"
            "    'разница двух распознавателей утонет в случайности выборки.'\n"
            ")\n"
            "print(round(p_eight_dark, 3), round(p_eight_light, 3),\n"
            "      round(p_three_tiny, 3), round(p_three_all, 3))"
        ),
        md("## Урок. 8–9. Пять разбиений и три части"),
        code(
            "spreads = []\n"
            "for seed in range(5):\n"
            "    _, te_i = train_test_split(df, test_size=0.25, random_state=seed)\n"
            "    spreads.append(float((te_i['label'] == 3).mean()))\n"
            "spread_range = max(spreads) - min(spreads)\n"
            "SEED_NOTE = (\n"
            "    'Доля одной цифры в проверочной части гуляет от разбиения к разбиению. '\n"
            "    'Значит и точность гуляет: сравнивать модели надо на одном фиксированном разбиении.'\n"
            ")\n"
            "rest, final = train_test_split(df, test_size=0.2, random_state=0, stratify=df['label'])\n"
            "fit_part, check_part = train_test_split(rest, test_size=0.25, random_state=0,\n"
            "                                        stratify=rest['label'])\n"
            "sizes_three = [len(fit_part), len(check_part), len(final)]\n"
            "print([round(s, 3) for s in spreads], round(spread_range, 3), sizes_three)"
        ),
        md("## ДЗ. 1–4"),
        code(
            "order1 = df.sample(frac=1, random_state=1).index\n"
            "mid = len(df) // 2\n"
            "half_a_idx, half_b_idx = order1[:mid], order1[mid:]\n"
            "n_overlap = int(half_a_idx.isin(half_b_idx).sum())\n"
            "p_nine_a = float((df.loc[half_a_idx, 'label'] == 9).mean())\n"
            "p_nine_b = float((df.loc[half_b_idx, 'label'] == 9).mean())\n"
            "gap_nine = abs(p_nine_a - p_nine_b)\n"
            "tr_p, te_p = train_test_split(df, test_size=0.25, random_state=2)\n"
            "gap_plain = float((tr_p['label'].value_counts(normalize=True).sort_index()\n"
            "                   - te_p['label'].value_counts(normalize=True).sort_index()).abs().max())\n"
            "tr_s, te_s = train_test_split(df, test_size=0.25, random_state=2, stratify=df['label'])\n"
            "gap_strat = float((tr_s['label'].value_counts(normalize=True).sort_index()\n"
            "                   - te_s['label'].value_counts(normalize=True).sort_index()).abs().max())\n"
            "STRAT_NOTE = (\n"
            "    'Когда классов много или какой-то класс редкий, случайное разбиение может '\n"
            "    'дать в проверочной части почти нет этого класса — оценка станет случайной.'\n"
            ")\n"
            "WHY_NOT_TEST = (\n"
            "    'Проверочные картинки играют роль будущей почты. Если подкручивать распознаватель, '\n"
            "    'пока не понравится результат именно на них, то мы выбираем настройку под эти 450 конвертов. '\n"
            "    'На настоящем потоке качество окажется ниже обещанного, а сервис уже подписал договор.'\n"
            ")\n"
            "print(n_overlap, round(gap_nine, 3), round(gap_plain, 4), round(gap_strat, 4))"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson03() -> None:
    """Pair 26: kNN и min-max scaling."""
    base = "lessons/03_knn_scaling"
    lesson = nb(
        md(
            "# Ближайшие соседи и масштаб признаков\n\n"
            "Распознаём цифру так: ищем в обучающей части самые похожие картинки "
            "и берём их ответ."
        ),
        code(
            LOAD_DATA
            + "\ntrain_part = df.iloc[:1200].reset_index(drop=True)\n"
            "test_part = df.iloc[1200:].reset_index(drop=True)\n"
            "train_pixels = train_part[PIXELS].to_numpy().tolist()\n"
            "train_labels = train_part['label'].tolist()\n"
        ),
        md(
            "## 1. Насколько похожи две картинки\n\n"
            "Реализуйте `distance(a, b)`: корень из суммы квадратов разностей по всем 64 числам.\n\n"
            "**How:** `zip(a, b)` и `sum(...) ** 0.5`.\n\n"
            "**Проверка:** для `[0, 0]` и `[3, 4]` расстояние равно 5."
        ),
        code(
            "def distance(a, b):\n"
            "    return None  # ваш код\n\n\n"
            "assert distance([1, 2, 3], [1, 2, 3]) == 0\n"
            "assert abs(distance([0, 0], [3, 4]) - 5) < 1e-9\n"
            "print(round(distance(train_pixels[0], train_pixels[1]), 2))"
        ),
        md(
            "## 2. Один ближайший сосед\n\n"
            "Возьмите картинку `probe = test_part.loc[0, PIXELS].tolist()`. "
            "Пройдите циклом по `train_pixels`, найдите номер ближайшей -> `nn_index`, "
            "её ответ -> `nn_label`, расстояние -> `nn_dist`.\n\n"
            "**Вопрос:** совпал ли `nn_label` с настоящей цифрой `test_part.loc[0, 'label']`?"
        ),
        code(
            "probe = test_part.loc[0, PIXELS].tolist()\n"
            "nn_index = None\n"
            "nn_label = None\n"
            "nn_dist = None\n"
            "assert nn_index is not None and nn_label is not None and nn_dist is not None\n"
            "assert 0 <= int(nn_index) < len(train_pixels)\n"
            "assert int(nn_label) in range(10)\n"
            "assert float(nn_dist) >= 0\n"
            "print(nn_index, nn_label, round(float(nn_dist), 2), test_part.loc[0, 'label'])"
        ),
        md(
            "## 3. Голосование трёх соседей\n\n"
            "Отсортируйте номера обучающих картинок по расстоянию до `probe` (`sorted(key=...)`), "
            "возьмите первые 3 ответа -> `three_labels`, самый частый среди них -> `vote_label`.\n\n"
            "**How:** частый элемент списка — `pd.Series(three_labels).value_counts().idxmax()`.\n\n"
            "**Checkpoint:** что делать при ничьей 1–1–1?"
        ),
        code(
            "three_labels = []\n"
            "vote_label = None\n"
            "assert len(three_labels) == 3\n"
            "assert vote_label is not None and int(vote_label) in range(10)\n"
            "print(three_labels, vote_label)"
        ),
        md(
            "## 4. Один признак может съесть все остальные\n\n"
            "Добавьте к таблице столбец `ink_thousands` — суммарную яркость, умноженную на 1000. "
            "Посчитайте для двух картинок (строки 0 и 1) вклад этого столбца в квадрат расстояния "
            "-> `share_from_ink`.\n\n"
            "**Идея:** расстояние измеряется в тех единицах, в которых записаны числа."
        ),
        code(
            "row_a = df.loc[0, PIXELS].tolist()\n"
            "row_b = df.loc[1, PIXELS].tolist()\n"
            "ink_a = sum(row_a) * 1000\n"
            "ink_b = sum(row_b) * 1000\n"
            "share_from_ink = None  # (ink_a - ink_b)^2 / (полный квадрат расстояния)\n"
            "assert share_from_ink is not None\n"
            "assert float(share_from_ink) > 0.9\n"
            "print(round(float(share_from_ink), 4))"
        ),
        md(
            "## 5. min-max: привести все столбцы к [0, 1]\n\n"
            "Реализуйте `scale_min_max(frame)`: из каждого столбца вычесть его минимум "
            "и поделить на размах (максимум − минимум).\n\n"
            "**Ловушка:** у трёх пикселей значение всегда одно и то же — размах 0, "
            "деление даёт `NaN`. Замените нулевой размах на 1.\n\n"
            "**How:** `rng = frame.max() - frame.min()`, затем `rng.replace(0, 1)`."
        ),
        code(
            "def scale_min_max(frame):\n"
            "    return None  # ваш код\n\n\n"
            "scaled_pixels = scale_min_max(df[PIXELS])\n"
            "assert scaled_pixels is not None\n"
            "assert int(scaled_pixels.isna().sum().sum()) == 0\n"
            "assert float(scaled_pixels.min().min()) >= 0 and float(scaled_pixels.max().max()) <= 1\n"
            "print(scaled_pixels.iloc[:2, :6].round(2))"
        ),
        md(
            "## 6. Тот же алгоритм библиотекой\n\n"
            "Разбейте таблицу (`test_size=0.25`, `random_state=0`, `stratify=df['label']`), "
            "обучите `KNeighborsClassifier(n_neighbors=3)` на пикселях и посчитайте долю верных "
            "ответов на проверочной части -> `acc_knn`.\n\n"
            "Сравните с baseline из пары 24 (~0.10)."
        ),
        code(
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.neighbors import KNeighborsClassifier\n"
            "from sklearn.metrics import accuracy_score\n\n"
            "acc_knn = None\n"
            "assert acc_knn is not None\n"
            "assert float(acc_knn) > 0.9\n"
            "print(round(float(acc_knn), 4))"
        ),
        md(
            "## 7. Эксперимент: сколько соседей спрашивать\n\n"
            "На том же разбиении посчитайте точность при `n_neighbors=1` и `n_neighbors=25` "
            "-> `acc_1`, `acc_25`.\n\n"
            "Запишите в `K_NOTE`, что происходит с ответом, когда соседей слишком много. "
            "**Готового ответа нет.**"
        ),
        code(
            "acc_1 = None\n"
            "acc_25 = None\n"
            "K_NOTE = ''\n"
            "assert acc_1 is not None and acc_25 is not None\n"
            "assert float(acc_1) > float(acc_25)\n"
            "assert len(K_NOTE) > 50\n"
            "print(round(float(acc_1), 4), round(float(acc_25), 4), K_NOTE)"
        ),
        md(
            "## 8. Расширение: свой поиск против библиотеки\n\n"
            "Для первых 50 картинок `test_part` предскажите ответ своим кодом (1 сосед) "
            "-> `my_preds`, затем то же — `KNeighborsClassifier(n_neighbors=1)` на `train_part`.\n\n"
            "Доля совпадений -> `agree_share`."
        ),
        code(
            "my_preds = []\n"
            "agree_share = None\n"
            "assert len(my_preds) == 50\n"
            "assert agree_share is not None and float(agree_share) > 0.95\n"
            "print(round(float(agree_share), 3))"
        ),
    )
    hw = nb(
        md("# ДЗ: соседи и масштаб"),
        code(LOAD_DATA),
        md("### A. Закрепление"),
        md(
            "## 1. Расстояние между двумя картинками\n\n"
            "Своей функцией `distance` посчитайте расстояние между строками 0 и 1 -> `d01`."
        ),
        code(
            "def distance(a, b):\n"
            "    return None  # ваш код\n\n\n"
            "d01 = None\n"
            "assert d01 is not None and 30 < float(d01) < 90\n"
            "print(round(float(d01), 2))"
        ),
        md(
            "## 2. kNN с пятью соседями\n\n"
            "Разбиение `random_state=1`, `stratify`; `n_neighbors=5`; точность -> `acc_5`.\n\n"
            "Импорты `train_test_split`, `KNeighborsClassifier`, `accuracy_score` — как на уроке."
        ),
        code(
            "acc_5 = None\n"
            "assert acc_5 is not None and float(acc_5) > 0.9\n"
            "print(round(float(acc_5), 4))"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. Сломать и починить масштаб\n\n"
            "Добавьте столбец `ink_thousands` (сумма яркости × 1000) к пикселям. "
            "Посчитайте точность kNN (k=5) на такой таблице -> `acc_broken`, "
            "затем на той же таблице после min-max -> `acc_fixed`.\n\n"
            "Функцию `scale_min_max` перенесите из урока (не забудьте про нулевой размах)."
        ),
        code(
            "acc_broken = None\n"
            "acc_fixed = None\n"
            "assert acc_broken is not None and acc_fixed is not None\n"
            "assert float(acc_fixed) > float(acc_broken) + 0.2\n"
            "print(round(float(acc_broken), 4), round(float(acc_fixed), 4))"
        ),
        md(
            "## 4. Почему масштабируем до расстояния\n\n"
            "Напишите в `WHY_SCALE` (≥120 символов): что именно измеряет расстояние "
            "в таблице со столбцами разного масштаба и почему это ломает распознавание."
        ),
        code(
            "WHY_SCALE = ''\n"
            "assert len(WHY_SCALE) > 120\n"
            "print(WHY_SCALE)"
        ),
    )
    sol = nb(
        md("# Решения: kNN и масштаб\n\n" + SOL_BANNER),
        code(
            LOAD_DATA
            + "\nfrom sklearn.model_selection import train_test_split\n"
            "from sklearn.neighbors import KNeighborsClassifier\n"
            "from sklearn.metrics import accuracy_score\n\n"
            "train_part = df.iloc[:1200].reset_index(drop=True)\n"
            "test_part = df.iloc[1200:].reset_index(drop=True)\n"
            "train_pixels = train_part[PIXELS].to_numpy().tolist()\n"
            "train_labels = train_part['label'].tolist()\n"
        ),
        md("## Урок. 1–3. Расстояние, сосед, голосование"),
        code(
            "def distance(a, b):\n"
            "    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5\n\n\n"
            "probe = test_part.loc[0, PIXELS].tolist()\n"
            "dists = [distance(probe, row) for row in train_pixels]\n"
            "nn_index = min(range(len(dists)), key=lambda j: dists[j])\n"
            "nn_label = train_labels[nn_index]\n"
            "nn_dist = dists[nn_index]\n"
            "order = sorted(range(len(dists)), key=lambda j: dists[j])[:3]\n"
            "three_labels = [train_labels[j] for j in order]\n"
            "vote_label = int(pd.Series(three_labels).value_counts().idxmax())\n"
            "print(nn_index, nn_label, round(nn_dist, 2), three_labels, vote_label,\n"
            "      test_part.loc[0, 'label'])"
        ),
        md("## Урок. 4–5. Масштаб и min-max"),
        code(
            "row_a = df.loc[0, PIXELS].tolist()\n"
            "row_b = df.loc[1, PIXELS].tolist()\n"
            "ink_a, ink_b = sum(row_a) * 1000, sum(row_b) * 1000\n"
            "pix_part = sum((x - y) ** 2 for x, y in zip(row_a, row_b))\n"
            "ink_part = (ink_a - ink_b) ** 2\n"
            "share_from_ink = ink_part / (pix_part + ink_part)\n\n\n"
            "def scale_min_max(frame):\n"
            "    rng = (frame.max() - frame.min()).replace(0, 1)\n"
            "    return (frame - frame.min()) / rng\n\n\n"
            "scaled_pixels = scale_min_max(df[PIXELS])\n"
            "print(round(share_from_ink, 4), int(scaled_pixels.isna().sum().sum()))"
        ),
        md("## Урок. 6–8. sklearn kNN, выбор k, сверка"),
        code(
            "X_tr, X_te, y_tr, y_te = train_test_split(df[PIXELS], df['label'], test_size=0.25,\n"
            "                                          random_state=0, stratify=df['label'])\n"
            "model = KNeighborsClassifier(n_neighbors=3).fit(X_tr, y_tr)\n"
            "acc_knn = float(accuracy_score(y_te, model.predict(X_te)))\n"
            "acc_1 = float(accuracy_score(y_te, KNeighborsClassifier(1).fit(X_tr, y_tr).predict(X_te)))\n"
            "acc_25 = float(accuracy_score(y_te, KNeighborsClassifier(25).fit(X_tr, y_tr).predict(X_te)))\n"
            "K_NOTE = (\n"
            "    'При k=25 в голосование попадают далёкие картинки других цифр, '\n"
            "    'ответ усредняется и редкие начертания теряются.'\n"
            ")\n"
            "my_preds = []\n"
            "for i in range(50):\n"
            "    p = test_part.loc[i, PIXELS].tolist()\n"
            "    d = [distance(p, row) for row in train_pixels]\n"
            "    my_preds.append(train_labels[min(range(len(d)), key=lambda j: d[j])])\n"
            "lib_preds = KNeighborsClassifier(1).fit(train_part[PIXELS], train_part['label'])\\\n"
            "    .predict(test_part[PIXELS].head(50)).tolist()\n"
            "agree_share = sum(1 for a, b in zip(my_preds, lib_preds) if a == b) / 50\n"
            "print(round(acc_knn, 4), round(acc_1, 4), round(acc_25, 4), agree_share)"
        ),
        md("## ДЗ. 1–4"),
        code(
            "d01 = distance(df.loc[0, PIXELS].tolist(), df.loc[1, PIXELS].tolist())\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(df[PIXELS], df['label'], test_size=0.25,\n"
            "                                          random_state=1, stratify=df['label'])\n"
            "acc_5 = float(accuracy_score(y_te, KNeighborsClassifier(5).fit(X_tr, y_tr).predict(X_te)))\n"
            "broken = df[PIXELS].copy()\n"
            "broken['ink_thousands'] = df[PIXELS].sum(axis=1) * 1000\n"
            "Xb_tr, Xb_te, yb_tr, yb_te = train_test_split(broken, df['label'], test_size=0.25,\n"
            "                                              random_state=0, stratify=df['label'])\n"
            "acc_broken = float(accuracy_score(yb_te, KNeighborsClassifier(5).fit(Xb_tr, yb_tr).predict(Xb_te)))\n"
            "fixed = scale_min_max(broken)\n"
            "Xf_tr, Xf_te, yf_tr, yf_te = train_test_split(fixed, df['label'], test_size=0.25,\n"
            "                                              random_state=0, stratify=df['label'])\n"
            "acc_fixed = float(accuracy_score(yf_te, KNeighborsClassifier(5).fit(Xf_tr, yf_tr).predict(Xf_te)))\n"
            "WHY_SCALE = (\n"
            "    'Расстояние складывает квадраты разностей по всем столбцам. Столбец с числами в тысячах '\n"
            "    'даёт вклад в миллионы, а пиксели 0..16 — единицы: сосед выбирается только по этому столбцу. '\n"
            "    'После min-max все столбцы лежат в [0, 1] и участвуют в сравнении сопоставимо.'\n"
            ")\n"
            "print(round(d01, 2), round(acc_5, 4), round(acc_broken, 4), round(acc_fixed, 4))"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson04() -> None:
    """Pair 27: практика — baseline kNN на подвыборке."""
    base = "lessons/04_practice_knn_baseline"
    lesson = nb(
        md(
            "# Практика: первый распознаватель и его честная оценка\n\n"
            "Сервис просит прототип к пятнице: маленькая подвыборка, baseline, kNN, таблица опытов."
        ),
        code(
            LOAD_DATA
            + "\nfrom sklearn.model_selection import train_test_split\n"
            "from sklearn.neighbors import KNeighborsClassifier\n"
            "from sklearn.metrics import accuracy_score\n"
            + SHOW_DIGIT
        ),
        md(
            "## 1. Подвыборка 400 картинок\n\n"
            "`sub = df.sample(400, random_state=0)`; разбейте на 300 обучающих и 100 проверочных "
            "(`test_size=100`, `random_state=0`, `stratify=sub['label']`) -> `X_tr`, `X_te`, `y_tr`, `y_te`.\n\n"
            "**Зачем подвыборка:** на паре важно успеть прогнать десяток опытов, а не один."
        ),
        code(
            "sub = None\n"
            "X_tr = X_te = y_tr = y_te = None\n"
            "assert sub is not None and len(sub) == 400\n"
            "assert X_tr is not None and len(X_tr) == 300 and len(X_te) == 100\n"
            "assert list(X_tr.columns) == PIXELS\n"
            "print(len(X_tr), len(X_te))"
        ),
        md(
            "## 2. Baseline на этой подвыборке\n\n"
            "Самая частая цифра в обучающей части -> `top_train`. Если всегда отвечать ею, "
            "доля верных ответов на проверочной части -> `baseline_acc`.\n\n"
            "**Это то число, которое обязан побить kNN.**"
        ),
        code(
            "top_train = None\n"
            "baseline_acc = None\n"
            "assert top_train is not None and int(top_train) in range(10)\n"
            "assert baseline_acc is not None and 0.02 < float(baseline_acc) < 0.3\n"
            "print(top_train, round(float(baseline_acc), 3))"
        ),
        md(
            "## 3. Масштаб считаем только по обучающей части\n\n"
            "Возьмите `mins = X_tr.min()`, `rng = (X_tr.max() - X_tr.min()).replace(0, 1)` "
            "и примените их к **обоим** наборам -> `tr_scaled`, `te_scaled`.\n\n"
            "Максимум в `te_scaled` -> `te_max`. Он может оказаться больше 1 — это нормально.\n\n"
            "В `LEAK_NOTE` ответьте: почему нельзя считать min/max по всей таблице сразу."
        ),
        code(
            "tr_scaled = None\n"
            "te_scaled = None\n"
            "te_max = None\n"
            "LEAK_NOTE = ''\n"
            "assert tr_scaled is not None and te_scaled is not None\n"
            "assert float(tr_scaled.max().max()) <= 1.0 + 1e-9\n"
            "assert te_max is not None and len(LEAK_NOTE) > 60\n"
            "print(round(float(te_max), 3), LEAK_NOTE)"
        ),
        md(
            "## 4. Таблица опытов по числу соседей\n\n"
            "Для `k` из 1, 3, 5, 7, 9 обучите kNN на `X_tr` и посчитайте точность на `X_te`. "
            "Соберите `results` — DataFrame со столбцами `k` и `accuracy` (постройте из списка списков).\n\n"
            "Лучшая точность -> `best_acc`, соответствующее k -> `best_k`."
        ),
        code(
            "results = None\n"
            "best_acc = None\n"
            "best_k = None\n"
            "assert results is not None and len(results) == 5\n"
            "assert list(results.columns) == ['k', 'accuracy']\n"
            "assert best_acc is not None and float(best_acc) > float(baseline_acc) + 0.5\n"
            "assert int(best_k) in (1, 3, 5, 7, 9)\n"
            "print(results)"
        ),
        md(
            "## 5. Сколько стоит один ответ\n\n"
            "kNN сравнивает картинку со **всеми** обучающими. Замерьте `time.perf_counter()` "
            "вокруг `predict` для обучения на 300 картинках -> `t_small` и на 1200 -> `t_big` "
            "(вторую модель обучите на `df.iloc[:1200]`, проверяйте те же 100 картинок).\n\n"
            "**Вопрос:** во сколько раз выросло время и почему."
        ),
        code(
            "import time\n\n"
            "t_small = None\n"
            "t_big = None\n"
            "assert t_small is not None and t_big is not None\n"
            "assert float(t_small) > 0 and float(t_big) > 0\n"
            "print(round(float(t_small), 4), round(float(t_big), 4))"
        ),
        md(
            "## 6. На чём распознаватель ошибается\n\n"
            "Обучите kNN с `best_k`, найдите номера проверочных картинок с неверным ответом "
            "-> `wrong_positions` (список позиций 0…99). Нарисуйте до трёх таких картинок "
            "и сохраните `figures/errors.png`.\n\n"
            "В `ERROR_NOTE` — что общего у ошибок."
        ),
        code(
            "from pathlib import Path as _P\n"
            "_P('figures').mkdir(exist_ok=True)\n"
            "wrong_positions = None\n"
            "errors_png = None\n"
            "ERROR_NOTE = ''\n"
            "assert wrong_positions is not None and len(wrong_positions) >= 1\n"
            "assert errors_png is not None and _P(errors_png).exists()\n"
            "assert len(ERROR_NOTE) > 40\n"
            "print(wrong_positions, ERROR_NOTE)"
        ),
        md(
            "## 7. Эксперимент: пиксели, которые всегда пустые\n\n"
            "Найдите пиксели, у которых во всей таблице одно и то же значение -> `const_pixels`. "
            "Обучите kNN (`best_k`) без них -> `acc_no_const`.\n\n"
            "В `CONST_NOTE` объясните результат. **Готового ответа нет.**"
        ),
        code(
            "const_pixels = None\n"
            "acc_no_const = None\n"
            "CONST_NOTE = ''\n"
            "assert const_pixels is not None and len(const_pixels) >= 1\n"
            "assert acc_no_const is not None and float(acc_no_const) > 0.8\n"
            "assert len(CONST_NOTE) > 40\n"
            "print(const_pixels, round(float(acc_no_const), 4), CONST_NOTE)"
        ),
        md(
            "## 8. Расширение: два признака вместо 64\n\n"
            "Постройте два признака: `ink` (сумма яркости) и `n_dark` (сколько пикселей ярче 8). "
            "Обучите kNN (`best_k`) только на них -> `acc_two`.\n\n"
            "В `FEATURES_NOTE` — почему потеря такая большая."
        ),
        code(
            "acc_two = None\n"
            "FEATURES_NOTE = ''\n"
            "assert acc_two is not None\n"
            "assert float(acc_two) < float(best_acc) - 0.3\n"
            "assert len(FEATURES_NOTE) > 40\n"
            "print(round(float(acc_two), 4), FEATURES_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: прототип распознавателя"),
        code(
            LOAD_DATA
            + "\nfrom sklearn.model_selection import train_test_split\n"
            "from sklearn.neighbors import KNeighborsClassifier\n"
            "from sklearn.metrics import accuracy_score\n"
        ),
        md("### A. Закрепление"),
        md(
            "## 1. Другая подвыборка\n\n"
            "`sub7 = df.sample(400, random_state=7)`, 300/100 со `stratify`; kNN k=3 -> `acc_hw`. "
            "Сравните с baseline этой подвыборки -> `baseline_hw`."
        ),
        code(
            "acc_hw = None\n"
            "baseline_hw = None\n"
            "assert acc_hw is not None and baseline_hw is not None\n"
            "assert float(acc_hw) > 0.8 and 0 < float(baseline_hw) < 0.3\n"
            "print(round(float(acc_hw), 4), round(float(baseline_hw), 3))"
        ),
        md(
            "## 2. Чётное число соседей\n\n"
            "На той же подвыборке посчитайте точность при k=2 и k=3 -> `acc_2`, `acc_3`. "
            "Объясните в `TIE_NOTE`, чем неудобно чётное число соседей."
        ),
        code(
            "acc_2 = None\n"
            "acc_3 = None\n"
            "TIE_NOTE = ''\n"
            "assert acc_2 is not None and acc_3 is not None\n"
            "assert len(TIE_NOTE) > 40\n"
            "print(round(float(acc_2), 4), round(float(acc_3), 4), TIE_NOTE)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. Сколько нужно обучающих картинок\n\n"
            "Обучите kNN (k=3) на 50, 100, 200, 300 картинках из `sub7` и проверяйте на тех же 100. "
            "Соберите `size_table` (столбцы `n_train`, `accuracy`) и опишите зависимость в `SIZE_NOTE`."
        ),
        code(
            "size_table = None\n"
            "SIZE_NOTE = ''\n"
            "assert size_table is not None and len(size_table) == 4\n"
            "assert list(size_table.columns) == ['n_train', 'accuracy']\n"
            "assert len(SIZE_NOTE) > 60\n"
            "print(size_table)"
        ),
        md(
            "## 4. Сохранить таблицу опытов\n\n"
            "Запишите `size_table` в файл `experiments_hw.csv` -> `csv_path` "
            "(эта таблица войдёт в артефакт модуля)."
        ),
        code(
            "from pathlib import Path as _P\n\n"
            "csv_path = None\n"
            "assert csv_path is not None and _P(csv_path).exists()\n"
            "print(_P(csv_path).read_text(encoding='utf-8')[:120])"
        ),
    )
    sol = nb(
        md("# Решения: прототип kNN\n\n" + SOL_BANNER),
        code(
            LOAD_DATA
            + "\nfrom sklearn.model_selection import train_test_split\n"
            "from sklearn.neighbors import KNeighborsClassifier\n"
            "from sklearn.metrics import accuracy_score\n"
            "from pathlib import Path as _P\n"
            "_P('figures').mkdir(exist_ok=True)\n"
            + SHOW_DIGIT
        ),
        md("## Урок. 1–3. Подвыборка, baseline, масштаб по train"),
        code(
            "sub = df.sample(400, random_state=0)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(sub[PIXELS], sub['label'], test_size=100,\n"
            "                                          random_state=0, stratify=sub['label'])\n"
            "top_train = int(y_tr.value_counts().idxmax())\n"
            "baseline_acc = float((y_te == top_train).mean())\n"
            "mins = X_tr.min()\n"
            "rng = (X_tr.max() - X_tr.min()).replace(0, 1)\n"
            "tr_scaled = (X_tr - mins) / rng\n"
            "te_scaled = (X_te - mins) / rng\n"
            "te_max = float(te_scaled.max().max())\n"
            "LEAK_NOTE = (\n"
            "    'min/max по всей таблице подсматривают проверочные картинки: настройка препроцессинга '\n"
            "    'уже зависит от данных, на которых мы обещали честную оценку.'\n"
            ")\n"
            "print(top_train, round(baseline_acc, 3), round(te_max, 3))"
        ),
        md("## Урок. 4–5. Таблица k и время"),
        code(
            "rows = []\n"
            "for k in (1, 3, 5, 7, 9):\n"
            "    m = KNeighborsClassifier(n_neighbors=k).fit(X_tr, y_tr)\n"
            "    rows.append([k, float(accuracy_score(y_te, m.predict(X_te)))])\n"
            "results = pd.DataFrame(rows, columns=['k', 'accuracy'])\n"
            "best_row = results.sort_values('accuracy', ascending=False).iloc[0]\n"
            "best_acc, best_k = float(best_row['accuracy']), int(best_row['k'])\n"
            "import time\n"
            "small = KNeighborsClassifier(n_neighbors=best_k).fit(X_tr, y_tr)\n"
            "t0 = time.perf_counter(); small.predict(X_te); t_small = time.perf_counter() - t0\n"
            "big = KNeighborsClassifier(n_neighbors=best_k).fit(df[PIXELS].iloc[:1200], df['label'].iloc[:1200])\n"
            "t0 = time.perf_counter(); big.predict(X_te); t_big = time.perf_counter() - t0\n"
            "print(results, best_k, round(t_small, 4), round(t_big, 4))"
        ),
        md("## Урок. 6–8. Ошибки, константные пиксели, два признака"),
        code(
            "model = KNeighborsClassifier(n_neighbors=best_k).fit(X_tr, y_tr)\n"
            "pred = model.predict(X_te)\n"
            "wrong_positions = [i for i in range(len(y_te)) if pred[i] != y_te.iloc[i]]\n"
            "plt.figure(figsize=(6, 2))\n"
            "for j, pos in enumerate(wrong_positions[:3]):\n"
            "    plt.subplot(1, 3, j + 1)\n"
            "    show_digit(X_te.iloc[pos], title=f'{y_te.iloc[pos]} -> {pred[pos]}')\n"
            "plt.tight_layout()\n"
            "errors_png = _P('figures/errors.png'); plt.savefig(errors_png); plt.close()\n"
            "ERROR_NOTE = 'Ошибки — на смазанных и наклонных начертаниях, где 8/9 и 1/7 похожи по пикселям'\n"
            "const_pixels = [c for c in PIXELS if df[c].nunique() == 1]\n"
            "keep = [c for c in PIXELS if c not in const_pixels]\n"
            "m_nc = KNeighborsClassifier(n_neighbors=best_k).fit(X_tr[keep], y_tr)\n"
            "acc_no_const = float(accuracy_score(y_te, m_nc.predict(X_te[keep])))\n"
            "CONST_NOTE = 'Пиксель с одним значением даёт нулевую разность всем: качество не изменилось'\n"
            "two_tr = pd.DataFrame({'ink': X_tr.sum(axis=1), 'n_dark': (X_tr > 8).sum(axis=1)})\n"
            "two_te = pd.DataFrame({'ink': X_te.sum(axis=1), 'n_dark': (X_te > 8).sum(axis=1)})\n"
            "m_two = KNeighborsClassifier(n_neighbors=best_k).fit(two_tr, y_tr)\n"
            "acc_two = float(accuracy_score(y_te, m_two.predict(two_te)))\n"
            "FEATURES_NOTE = 'Разные цифры имеют похожую суммарную яркость: два числа не различают форму'\n"
            "print(len(wrong_positions), round(acc_no_const, 4), round(acc_two, 4))"
        ),
        md("## ДЗ. 1–4"),
        code(
            "sub7 = df.sample(400, random_state=7)\n"
            "A_tr, A_te, b_tr, b_te = train_test_split(sub7[PIXELS], sub7['label'], test_size=100,\n"
            "                                          random_state=0, stratify=sub7['label'])\n"
            "acc_hw = float(accuracy_score(b_te, KNeighborsClassifier(3).fit(A_tr, b_tr).predict(A_te)))\n"
            "baseline_hw = float((b_te == b_tr.value_counts().idxmax()).mean())\n"
            "acc_2 = float(accuracy_score(b_te, KNeighborsClassifier(2).fit(A_tr, b_tr).predict(A_te)))\n"
            "acc_3 = acc_hw\n"
            "TIE_NOTE = 'При k=2 голоса могут разделиться 1:1, и ответ решает порядок соседей, а не большинство'\n"
            "rows = []\n"
            "for n in (50, 100, 200, 300):\n"
            "    m = KNeighborsClassifier(3).fit(A_tr.iloc[:n], b_tr.iloc[:n])\n"
            "    rows.append([n, float(accuracy_score(b_te, m.predict(A_te)))])\n"
            "size_table = pd.DataFrame(rows, columns=['n_train', 'accuracy'])\n"
            "SIZE_NOTE = ('Точность быстро растёт на первых сотнях примеров и затем почти выходит на плато: '\n"
            "             'ещё сто картинок дают меньше, чем первые сто.')\n"
            "csv_path = _P('experiments_hw.csv')\n"
            "size_table.to_csv(csv_path, index=False)\n"
            "print(round(acc_hw, 4), round(baseline_hw, 3), round(acc_2, 4), size_table)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson05() -> None:
    """Pair 28: accuracy, F1, выбор k по проверочной части."""
    base = "lessons/05_accuracy_f1_val"
    lesson = nb(
        md(
            "# Точность врёт: precision, recall, F1 и честный выбор k\n\n"
            "Сервис отдельно платит за поиск восьмёрок в индексах. Здесь доля восьмёрок мала — "
            "и обычная точность перестаёт работать."
        ),
        code(
            LOAD_DATA
            + "\nfrom sklearn.model_selection import train_test_split\n"
            "from sklearn.neighbors import KNeighborsClassifier\n"
            "from sklearn.metrics import accuracy_score, f1_score\n"
        ),
        md(
            "## 1. Задача с двумя ответами\n\n"
            "Постройте столбец `is_eight` (1, если цифра 8, иначе 0) и его долю -> `share_8`."
        ),
        code(
            "is_eight = None\n"
            "share_8 = None\n"
            "assert is_eight is not None and share_8 is not None\n"
            "assert set(pd.unique(is_eight)) == {0, 1}\n"
            "assert 0.05 < float(share_8) < 0.15\n"
            "print(round(float(share_8), 4))"
        ),
        md(
            "## 2. Ленивый ответ «это не восьмёрка»\n\n"
            "Какова точность правила, которое **всегда** отвечает 0? -> `acc_dumb`.\n\n"
            "В `WHY_ACC_LIES` объясните, почему сервис не примет такой распознаватель, "
            "хотя точность высокая."
        ),
        code(
            "acc_dumb = None\n"
            "WHY_ACC_LIES = ''\n"
            "assert acc_dumb is not None and float(acc_dumb) > 0.85\n"
            "assert len(WHY_ACC_LIES) > 60\n"
            "print(round(float(acc_dumb), 4), WHY_ACC_LIES)"
        ),
        md(
            "## 3. Четыре числа вместо одного\n\n"
            "Разбейте данные (`test_size=0.25`, `random_state=0`, `stratify=is_eight`), обучите kNN k=3 "
            "и посчитайте **вручную**:\n\n"
            "- `tp` — предсказали 8 и это 8;\n"
            "- `fp` — предсказали 8, а это не 8;\n"
            "- `fn` — пропустили настоящую 8;\n"
            "- `tn` — верно сказали «не 8».\n\n"
            "**How:** сравнение массивов предсказаний и ответов, как `confusion_counts` в модуле 1."
        ),
        code(
            "tp = fp = fn = tn = None\n"
            "assert None not in (tp, fp, fn, tn)\n"
            "assert tp + fp + fn + tn == 450\n"
            "assert int(tp) > 0\n"
            "print(tp, fp, fn, tn)"
        ),
        md(
            "## 4. precision, recall, F1 руками\n\n"
            "- `precision` = tp / (tp + fp) — какая доля наших «восьмёрок» настоящие;\n"
            "- `recall` = tp / (tp + fn) — какую долю настоящих восьмёрок мы нашли;\n"
            "- `f1_manual` = 2·precision·recall / (precision + recall).\n\n"
            "Сверьте с `f1_score(y_te, pred)` -> `f1_lib`.\n\n"
            "**Вопрос:** какая из двух ошибок дороже для почтового сервиса?"
        ),
        code(
            "precision = recall = f1_manual = None\n"
            "f1_lib = None\n"
            "assert None not in (precision, recall, f1_manual, f1_lib)\n"
            "assert abs(float(f1_manual) - float(f1_lib)) < 1e-9\n"
            "print(round(float(precision), 4), round(float(recall), 4), round(float(f1_manual), 4))"
        ),
        md(
            "## 5. Третья часть данных: где выбирать k\n\n"
            "Вернёмся к задаче «какая это цифра». Разбейте таблицу на три части: "
            "**обучающую** 60%, **проверочную** 20%, **финальную** 20% (`stratify` на каждом шаге).\n\n"
            "Для k из 1, 3, 5, 7, 9, 15 посчитайте точность на **проверочной** части -> `val_table` "
            "(столбцы `k`, `accuracy`), лучшее k -> `best_k`.\n\n"
            "**Правило:** финальную часть на этом шаге не трогаем."
        ),
        code(
            "X_fit = X_val = X_final = None\n"
            "y_fit = y_val = y_final = None\n"
            "val_table = None\n"
            "best_k = None\n"
            "assert X_fit is not None and len(X_fit) > 1000\n"
            "assert len(X_val) == len(X_final) == 360\n"
            "assert val_table is not None and len(val_table) == 6\n"
            "assert list(val_table.columns) == ['k', 'accuracy']\n"
            "assert int(best_k) in (1, 3, 5, 7, 9, 15)\n"
            "print(val_table, best_k)"
        ),
        md(
            "## 6. Один выстрел по финальной части\n\n"
            "Обучите kNN с `best_k` и посчитайте точность на финальной части -> `acc_final`.\n\n"
            "В `WHY_ONE_SHOT` объясните, почему это число можно получить только один раз "
            "и почему оно обычно чуть ниже проверочного."
        ),
        code(
            "acc_final = None\n"
            "WHY_ONE_SHOT = ''\n"
            "assert acc_final is not None and float(acc_final) > 0.9\n"
            "assert len(WHY_ONE_SHOT) > 80\n"
            "print(round(float(acc_final), 4), WHY_ONE_SHOT)"
        ),
        md(
            "## 7. Опровержение: «F1 всегда лучше accuracy»\n\n"
            "Посчитайте `f1_micro = f1_score(y_final, pred_final, average='micro')` и сравните "
            "с `acc_final`.\n\n"
            "В `F1_LIMIT` объясните, что показал этот опыт и когда F1 действительно нужен."
        ),
        code(
            "f1_micro = None\n"
            "F1_LIMIT = ''\n"
            "assert f1_micro is not None\n"
            "assert abs(float(f1_micro) - float(acc_final)) < 1e-9\n"
            "assert len(F1_LIMIT) > 60\n"
            "print(round(float(f1_micro), 4), F1_LIMIT)"
        ),
        md(
            "## 8. Расширение: F1 по каждой цифре\n\n"
            "`f1_macro` = `f1_score(..., average='macro')` — среднее F1 по десяти цифрам. "
            "Сравните с `f1_micro`.\n\n"
            "В `MACRO_NOTE` — в какой ситуации macro будет заметно ниже micro. **Готового ответа нет.**"
        ),
        code(
            "f1_macro = None\n"
            "MACRO_NOTE = ''\n"
            "assert f1_macro is not None and 0.5 < float(f1_macro) <= 1.0\n"
            "assert len(MACRO_NOTE) > 50\n"
            "print(round(float(f1_macro), 4), MACRO_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: метрики и протокол оценки"),
        code(
            LOAD_DATA
            + "\nfrom sklearn.model_selection import train_test_split\n"
            "from sklearn.neighbors import KNeighborsClassifier\n"
            "from sklearn.metrics import accuracy_score, f1_score, confusion_matrix\n"
        ),
        md("### A. Закрепление"),
        md(
            "## 1. «Это тройка»\n\n"
            "Задача с двумя ответами для цифры 3 (`test_size=0.25`, `random_state=0`, `stratify`), kNN k=3. "
            "Посчитайте `precision_3`, `recall_3`, `f1_3` (можно через sklearn)."
        ),
        code(
            "precision_3 = recall_3 = f1_3 = None\n"
            "assert None not in (precision_3, recall_3, f1_3)\n"
            "assert 0 < float(f1_3) <= 1\n"
            "print(round(float(precision_3), 4), round(float(recall_3), 4), round(float(f1_3), 4))"
        ),
        md(
            "## 2. Кто с кем путается\n\n"
            "Для задачи «какая цифра» постройте `confusion_matrix` (k=3, то же разбиение) -> `cm`. "
            "Найдите цифру с наибольшим числом ошибок -> `worst_digit`."
        ),
        code(
            "cm = None\n"
            "worst_digit = None\n"
            "assert cm is not None and cm.shape == (10, 10)\n"
            "assert worst_digit is not None and int(worst_digit) in range(10)\n"
            "print(worst_digit)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. Выбор k по проверочной части для задачи «это 8»\n\n"
            "Три части 60/20/20 (`stratify=is_eight`). Выберите k по F1 на проверочной части "
            "-> `best_k_bin`, затем один раз посчитайте F1 на финальной -> `f1_final`."
        ),
        code(
            "best_k_bin = None\n"
            "f1_final = None\n"
            "assert best_k_bin is not None and f1_final is not None\n"
            "assert 0 < float(f1_final) <= 1\n"
            "print(best_k_bin, round(float(f1_final), 4))"
        ),
        md(
            "## 4. Протокол оценки\n\n"
            "Опишите в `PROTOCOL` (≥200 символов) порядок работы, который вы будете применять "
            "в артефакте модуля: какие части данных, что настраиваем, где считаем итог, "
            "сколько раз смотрим финальную часть."
        ),
        code(
            "PROTOCOL = ''\n"
            "assert len(PROTOCOL) > 200\n"
            "print(PROTOCOL)"
        ),
    )
    sol = nb(
        md("# Решения: метрики и валидация\n\n" + SOL_BANNER),
        code(
            LOAD_DATA
            + "\nfrom sklearn.model_selection import train_test_split\n"
            "from sklearn.neighbors import KNeighborsClassifier\n"
            "from sklearn.metrics import accuracy_score, f1_score, confusion_matrix\n"
        ),
        md("## Урок. 1–4. Бинарная задача и четыре числа"),
        code(
            "is_eight = (df['label'] == 8).astype(int)\n"
            "share_8 = float(is_eight.mean())\n"
            "acc_dumb = float((is_eight == 0).mean())\n"
            "WHY_ACC_LIES = (\n"
            "    'Правило «никогда не 8» имеет точность 90% и не находит ни одной восьмёрки: '\n"
            "    'метрика измеряет частоту класса, а не полезность распознавателя.'\n"
            ")\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(df[PIXELS], is_eight, test_size=0.25,\n"
            "                                          random_state=0, stratify=is_eight)\n"
            "pred = KNeighborsClassifier(3).fit(X_tr, y_tr).predict(X_te)\n"
            "tp = int(((pred == 1) & (y_te == 1)).sum())\n"
            "fp = int(((pred == 1) & (y_te == 0)).sum())\n"
            "fn = int(((pred == 0) & (y_te == 1)).sum())\n"
            "tn = int(((pred == 0) & (y_te == 0)).sum())\n"
            "precision = tp / (tp + fp)\n"
            "recall = tp / (tp + fn)\n"
            "f1_manual = 2 * precision * recall / (precision + recall)\n"
            "f1_lib = float(f1_score(y_te, pred))\n"
            "print(round(share_8, 4), round(acc_dumb, 4), tp, fp, fn, tn,\n"
            "      round(precision, 4), round(recall, 4), round(f1_manual, 4), round(f1_lib, 4))"
        ),
        md("## Урок. 5–8. Три части, выбор k, F1 macro/micro"),
        code(
            "X_rest, X_final, y_rest, y_final = train_test_split(df[PIXELS], df['label'], test_size=0.2,\n"
            "                                                    random_state=0, stratify=df['label'])\n"
            "X_fit, X_val, y_fit, y_val = train_test_split(X_rest, y_rest, test_size=0.25,\n"
            "                                              random_state=0, stratify=y_rest)\n"
            "rows = []\n"
            "for k in (1, 3, 5, 7, 9, 15):\n"
            "    m = KNeighborsClassifier(k).fit(X_fit, y_fit)\n"
            "    rows.append([k, float(accuracy_score(y_val, m.predict(X_val)))])\n"
            "val_table = pd.DataFrame(rows, columns=['k', 'accuracy'])\n"
            "best_k = int(val_table.sort_values('accuracy', ascending=False).iloc[0]['k'])\n"
            "final_model = KNeighborsClassifier(best_k).fit(X_fit, y_fit)\n"
            "pred_final = final_model.predict(X_final)\n"
            "acc_final = float(accuracy_score(y_final, pred_final))\n"
            "WHY_ONE_SHOT = (\n"
            "    'Финальная часть заменяет будущую почту. Каждый повторный взгляд превращает её в ещё одну '\n"
            "    'проверочную: мы начинаем подбирать настройку под неё, и оценка становится завышенной.'\n"
            ")\n"
            "f1_micro = float(f1_score(y_final, pred_final, average='micro'))\n"
            "F1_LIMIT = (\n"
            "    'В сбалансированной задаче про десять цифр micro-F1 совпал с точностью: '\n"
            "    'F1 нужен там, где один класс редкий и цена пропуска высока.'\n"
            ")\n"
            "f1_macro = float(f1_score(y_final, pred_final, average='macro'))\n"
            "MACRO_NOTE = (\n"
            "    'Macro усредняет по цифрам без учёта их частоты: если одна редкая цифра распознаётся плохо, '\n"
            "    'macro просядет, а micro почти не заметит.'\n"
            ")\n"
            "print(val_table, best_k, round(acc_final, 4), round(f1_micro, 4), round(f1_macro, 4))"
        ),
        md("## ДЗ. 1–4"),
        code(
            "is_three = (df['label'] == 3).astype(int)\n"
            "A_tr, A_te, b_tr, b_te = train_test_split(df[PIXELS], is_three, test_size=0.25,\n"
            "                                          random_state=0, stratify=is_three)\n"
            "p3 = KNeighborsClassifier(3).fit(A_tr, b_tr).predict(A_te)\n"
            "tp3 = int(((p3 == 1) & (b_te == 1)).sum()); fp3 = int(((p3 == 1) & (b_te == 0)).sum())\n"
            "fn3 = int(((p3 == 0) & (b_te == 1)).sum())\n"
            "precision_3 = tp3 / (tp3 + fp3)\n"
            "recall_3 = tp3 / (tp3 + fn3)\n"
            "f1_3 = float(f1_score(b_te, p3))\n"
            "C_tr, C_te, d_tr, d_te = train_test_split(df[PIXELS], df['label'], test_size=0.25,\n"
            "                                          random_state=0, stratify=df['label'])\n"
            "pm = KNeighborsClassifier(3).fit(C_tr, d_tr).predict(C_te)\n"
            "cm = confusion_matrix(d_te, pm)\n"
            "errors_per_digit = cm.sum(axis=1) - cm.diagonal()\n"
            "worst_digit = int(errors_per_digit.argmax())\n"
            "is8 = (df['label'] == 8).astype(int)\n"
            "E_rest, E_final, f_rest, f_final = train_test_split(df[PIXELS], is8, test_size=0.2,\n"
            "                                                    random_state=0, stratify=is8)\n"
            "E_fit, E_val, f_fit, f_val = train_test_split(E_rest, f_rest, test_size=0.25,\n"
            "                                              random_state=0, stratify=f_rest)\n"
            "scores = []\n"
            "for k in (1, 3, 5, 7, 9):\n"
            "    m = KNeighborsClassifier(k).fit(E_fit, f_fit)\n"
            "    scores.append([k, float(f1_score(f_val, m.predict(E_val)))])\n"
            "best_k_bin = int(pd.DataFrame(scores, columns=['k', 'f1'])\n"
            "                 .sort_values('f1', ascending=False).iloc[0]['k'])\n"
            "f1_final = float(f1_score(f_final, KNeighborsClassifier(best_k_bin)\n"
            "                          .fit(E_fit, f_fit).predict(E_final)))\n"
            "PROTOCOL = (\n"
            "    'Делю таблицу на три части со stratify: 60% обучение, 20% проверка, 20% финал. '\n"
            "    'Все настройки — число соседей, масштабирование, набор признаков — выбираю по проверочной части. '\n"
            "    'Масштаб считаю только по обучающей. Финальную часть смотрю один раз в конце и записываю '\n"
            "    'полученное число в отчёт вместе с baseline самой частой цифры.'\n"
            ")\n"
            "print(round(f1_3, 4), worst_digit, best_k_bin, round(f1_final, 4))"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson06() -> None:
    """Pair 29: практика — систематический перебор, сборка артефакта."""
    base = "lessons/06_practice_search_metrics"
    lesson = nb(
        md(
            "# Практика: перебор настроек и сдача эксперимента\n\n"
            "Собираем итог модуля: таблица опытов, честная финальная оценка, отчёт сервису."
        ),
        code(
            LOAD_DATA
            + "\nimport itertools\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.neighbors import KNeighborsClassifier\n"
            "from sklearn.metrics import accuracy_score\n\n"
            "X_rest, X_final, y_rest, y_final = train_test_split(\n"
            "    df[PIXELS], df['label'], test_size=0.2, random_state=0, stratify=df['label'])\n"
            "X_fit, X_val, y_fit, y_val = train_test_split(\n"
            "    X_rest, y_rest, test_size=0.25, random_state=0, stratify=y_rest)\n"
        ),
        md(
            "## 1. Все пары настроек сразу\n\n"
            "`itertools.product` даёт декартово произведение — то самое, что вы считали "
            "двойным циклом на паре 24.\n\n"
            "Соберите `grid = list(itertools.product(K_VALUES, SCALING))` для "
            "`K_VALUES = [1, 3, 5, 7, 9]` и `SCALING = [False, True]`."
        ),
        code(
            "K_VALUES = [1, 3, 5, 7, 9]\n"
            "SCALING = [False, True]\n"
            "grid = None\n"
            "assert grid is not None and len(grid) == 10\n"
            "assert all(len(c) == 2 for c in grid)\n"
            "print(grid[:4])"
        ),
        md(
            "## 2. Прогон по сетке\n\n"
            "Для каждой пары `(k, scaled)` обучите kNN на обучающей части и посчитайте точность "
            "на **проверочной**. При `scaled=True` считайте min/max по обучающей части.\n\n"
            "Соберите `exp_table` со столбцами `k`, `scaled`, `accuracy`.\n\n"
            "**Наблюдение:** здесь все пиксели уже в одной шкале 0…16 — посмотрите, "
            "меняет ли масштабирование результат."
        ),
        code(
            "exp_table = None\n"
            "assert exp_table is not None and len(exp_table) == 10\n"
            "assert list(exp_table.columns) == ['k', 'scaled', 'accuracy']\n"
            "assert float(exp_table['accuracy'].max()) > 0.9\n"
            "print(exp_table)"
        ),
        md(
            "## 3. Подмножества признаков\n\n"
            "Постройте четыре признака: `ink`, `n_dark`, `top_ink` (сумма первых 32 пикселей), "
            "`bottom_ink` (сумма последних 32).\n\n"
            "`itertools.combinations(FEATURES, 2)` — все пары признаков. Для каждой пары обучите kNN "
            "(k=5) и соберите `combo_table` со столбцами `features`, `accuracy`."
        ),
        code(
            "FEATURES = ['ink', 'n_dark', 'top_ink', 'bottom_ink']\n"
            "combo_table = None\n"
            "assert combo_table is not None and len(combo_table) == 6\n"
            "assert list(combo_table.columns) == ['features', 'accuracy']\n"
            "assert float(combo_table['accuracy'].max()) < 0.9\n"
            "print(combo_table)"
        ),
        md(
            "## 4. Выбор конфигурации и один выстрел\n\n"
            "Возьмите лучшую строку `exp_table` по проверочной точности -> `best_k`, `best_scaled`. "
            "Обучите модель с этой настройкой и посчитайте точность на **финальной** части -> `acc_final`.\n\n"
            "Baseline самой частой цифры на финальной части -> `baseline_final`."
        ),
        code(
            "best_k = None\n"
            "best_scaled = None\n"
            "acc_final = None\n"
            "baseline_final = None\n"
            "assert best_k is not None and best_scaled is not None\n"
            "assert acc_final is not None and float(acc_final) > 0.9\n"
            "assert baseline_final is not None and float(baseline_final) < 0.2\n"
            "print(best_k, best_scaled, round(float(acc_final), 4), round(float(baseline_final), 4))"
        ),
        md(
            "## 5. Что было бы, если выбирать по финальной части\n\n"
            "Посчитайте точность **всех** настроек сетки на финальной части и возьмите максимум "
            "-> `acc_peek`. Разница `optimism = acc_peek - acc_final`.\n\n"
            "В `OPTIMISM_NOTE` объясните, почему выбор по финальной части — это подгонка, "
            "даже если разница маленькая."
        ),
        code(
            "acc_peek = None\n"
            "optimism = None\n"
            "OPTIMISM_NOTE = ''\n"
            "assert acc_peek is not None and optimism is not None\n"
            "assert float(optimism) >= 0\n"
            "assert len(OPTIMISM_NOTE) > 80\n"
            "print(round(float(acc_peek), 4), round(float(optimism), 4))"
        ),
        md(
            "## 6. Таблица и график для отчёта\n\n"
            "Сохраните `exp_table` в `experiments.csv` -> `csv_path`. "
            "Постройте график: точность на проверочной части по `k` (две линии — с масштабированием и без) "
            "и сохраните `figures/config_accuracy.png` -> `plot_path`."
        ),
        code(
            "from pathlib import Path as _P\n"
            "import matplotlib.pyplot as plt\n\n"
            "_P('figures').mkdir(exist_ok=True)\n"
            "csv_path = None\n"
            "plot_path = None\n"
            "assert csv_path is not None and _P(csv_path).exists()\n"
            "assert plot_path is not None and _P(plot_path).exists()\n"
            "print(csv_path, plot_path)"
        ),
        md(
            "## 7. Чек-лист сдачи\n\n"
            "Отметьте `True` только то, что действительно сделано (см. "
            "[artifact/PROJECT.md](../../artifact/PROJECT.md)). Число взглядов на финальную часть "
            "-> `n_final_looks`."
        ),
        code(
            "acceptance = pd.Series(\n"
            "    [False, False, False, False, False, False],\n"
            "    index=['baseline', 'protocol', 'experiments_csv', 'figure', 'final_score', 'limitations'],\n"
            ")\n"
            "n_final_looks = None\n"
            "assert bool(acceptance.all())\n"
            "assert n_final_looks is not None and int(n_final_looks) == 1\n"
            "print(acceptance)"
        ),
        md(
            "## 8. Отчёт сервису\n\n"
            "`REPORT` (≥250 символов): что за данные, какой протокол, какая настройка выбрана, "
            "какая точность против baseline, какие ограничения (8×8, подвыборка, скорость kNN).\n\n"
            "`READY = True` — только если чек-лист заполнен и файлы сохранены."
        ),
        code(
            "REPORT = ''\n"
            "READY = False\n"
            "assert len(REPORT) > 250\n"
            "assert 'baseline' in REPORT.lower()\n"
            "assert READY is True\n"
            "print(REPORT)"
        ),
        md(
            "## 9. Расширение: где kNN станет неудобен\n\n"
            "В `NEXT_MODULE` (≥80 символов) объясните, что произойдёт со временем ответа, "
            "если картинок станет миллион, и почему следующий модуль занимается **признаками**, "
            "а не новыми моделями."
        ),
        code(
            "NEXT_MODULE = ''\n"
            "assert len(NEXT_MODULE) > 80\n"
            "print(NEXT_MODULE)"
        ),
    )
    hw = nb(
        md("# ДЗ: перебор и отчёт эксперимента"),
        code(
            LOAD_DATA
            + "\nimport itertools\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.neighbors import KNeighborsClassifier\n"
            "from sklearn.metrics import accuracy_score\n"
        ),
        md("### A. Закрепление"),
        md(
            "## 1. Перебор по двум осям\n\n"
            "`itertools.product` для k из 1, 3, 5, 7, 9 и способа измерять расстояние "
            "`'euclidean'` / `'manhattan'` (параметр `metric` у `KNeighborsClassifier`).\n\n"
            "Разбиение: 60/20/20, точность считайте на проверочной части. "
            "Соберите `metric_table` со столбцами `k`, `metric`, `accuracy`."
        ),
        code(
            "metric_table = None\n"
            "assert metric_table is not None and len(metric_table) == 10\n"
            "assert list(metric_table.columns) == ['k', 'metric', 'accuracy']\n"
            "assert float(metric_table['accuracy'].max()) > 0.9\n"
            "print(metric_table)"
        ),
        md(
            "## 2. Лучшая строка и файл\n\n"
            "Лучшая настройка -> `best_row` (строка таблицы). Сохраните таблицу в "
            "`metric_experiments.csv` -> `csv_path`."
        ),
        code(
            "from pathlib import Path as _P\n\n"
            "best_row = None\n"
            "csv_path = None\n"
            "assert best_row is not None and csv_path is not None\n"
            "assert _P(csv_path).exists()\n"
            "print(best_row)"
        ),
        md(
            "### B. Вызов\n\n"
            "## 3. Отчёт эксперимента\n\n"
            "Соберите `report_md` с разделами `## Данные`, `## Протокол`, `## Опыты`, "
            "`## Итог`, `## Ограничения` (≥500 символов). Числа — из ваших таблиц, не «на глаз»."
        ),
        code(
            "report_md = ''\n"
            "assert '## Данные' in report_md and '## Протокол' in report_md\n"
            "assert '## Опыты' in report_md and '## Итог' in report_md\n"
            "assert '## Ограничения' in report_md\n"
            "assert len(report_md) > 500\n"
            "print(report_md[:400])"
        ),
        md(
            "## 4. Рефлексия модуля\n\n"
            "`REFLECTION` (≥200 символов): что изменилось в вашем понимании «точности модели» "
            "за модуль; `HONEST_LOOKS` — сколько раз вы смотрели на финальную часть данных."
        ),
        code(
            "REFLECTION = ''\n"
            "HONEST_LOOKS = None\n"
            "assert len(REFLECTION) > 200\n"
            "assert HONEST_LOOKS is not None and int(HONEST_LOOKS) >= 1\n"
            "print(REFLECTION)"
        ),
    )
    sol = nb(
        md("# Решения: перебор и сдача\n\n" + SOL_BANNER),
        code(
            LOAD_DATA
            + "\nimport itertools\n"
            "import matplotlib.pyplot as plt\n"
            "from pathlib import Path as _P\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.neighbors import KNeighborsClassifier\n"
            "from sklearn.metrics import accuracy_score\n\n"
            "_P('figures').mkdir(exist_ok=True)\n"
            "X_rest, X_final, y_rest, y_final = train_test_split(\n"
            "    df[PIXELS], df['label'], test_size=0.2, random_state=0, stratify=df['label'])\n"
            "X_fit, X_val, y_fit, y_val = train_test_split(\n"
            "    X_rest, y_rest, test_size=0.25, random_state=0, stratify=y_rest)\n"
        ),
        md("## Урок. 1–3. Сетка настроек и подмножества признаков"),
        code(
            "K_VALUES = [1, 3, 5, 7, 9]\n"
            "SCALING = [False, True]\n"
            "grid = list(itertools.product(K_VALUES, SCALING))\n\n\n"
            "def scale_by_train(fit_frame, other_frame):\n"
            "    mins = fit_frame.min()\n"
            "    rng = (fit_frame.max() - fit_frame.min()).replace(0, 1)\n"
            "    return (fit_frame - mins) / rng, (other_frame - mins) / rng\n\n\n"
            "rows = []\n"
            "for k, scaled in grid:\n"
            "    a, b = scale_by_train(X_fit, X_val) if scaled else (X_fit, X_val)\n"
            "    m = KNeighborsClassifier(n_neighbors=k).fit(a, y_fit)\n"
            "    rows.append([k, scaled, float(accuracy_score(y_val, m.predict(b)))])\n"
            "exp_table = pd.DataFrame(rows, columns=['k', 'scaled', 'accuracy'])\n\n\n"
            "def make_features(frame):\n"
            "    out = pd.DataFrame(index=frame.index)\n"
            "    out['ink'] = frame.sum(axis=1)\n"
            "    out['n_dark'] = (frame > 8).sum(axis=1)\n"
            "    out['top_ink'] = frame[PIXELS[:32]].sum(axis=1)\n"
            "    out['bottom_ink'] = frame[PIXELS[32:]].sum(axis=1)\n"
            "    return out\n\n\n"
            "FEATURES = ['ink', 'n_dark', 'top_ink', 'bottom_ink']\n"
            "feat_fit, feat_val = make_features(X_fit), make_features(X_val)\n"
            "combo_rows = []\n"
            "for pair in itertools.combinations(FEATURES, 2):\n"
            "    m = KNeighborsClassifier(5).fit(feat_fit[list(pair)], y_fit)\n"
            "    combo_rows.append(['+'.join(pair), float(accuracy_score(y_val, m.predict(feat_val[list(pair)])))])\n"
            "combo_table = pd.DataFrame(combo_rows, columns=['features', 'accuracy'])\n"
            "print(exp_table)\n"
            "print(combo_table)"
        ),
        md("## Урок. 4–6. Выбор, честная оценка, файлы"),
        code(
            "best = exp_table.sort_values('accuracy', ascending=False).iloc[0]\n"
            "best_k, best_scaled = int(best['k']), bool(best['scaled'])\n"
            "a, b = scale_by_train(X_fit, X_final) if best_scaled else (X_fit, X_final)\n"
            "final_model = KNeighborsClassifier(n_neighbors=best_k).fit(a, y_fit)\n"
            "acc_final = float(accuracy_score(y_final, final_model.predict(b)))\n"
            "baseline_final = float((y_final == y_fit.value_counts().idxmax()).mean())\n"
            "peek = []\n"
            "for k, scaled in grid:\n"
            "    aa, bb = scale_by_train(X_fit, X_final) if scaled else (X_fit, X_final)\n"
            "    m = KNeighborsClassifier(n_neighbors=k).fit(aa, y_fit)\n"
            "    peek.append(float(accuracy_score(y_final, m.predict(bb))))\n"
            "acc_peek = max(peek)\n"
            "optimism = acc_peek - acc_final\n"
            "OPTIMISM_NOTE = (\n"
            "    'Максимум по десяти настройкам на финальной части — уже результат подбора: '\n"
            "    'мы выбрали то, что случайно лучше подошло к этим 360 картинкам. '\n"
            "    'Отчётное число должно приходить от настройки, выбранной без них.'\n"
            ")\n"
            "csv_path = _P('experiments.csv')\n"
            "exp_table.to_csv(csv_path, index=False)\n"
            "plt.figure()\n"
            "for scaled in (False, True):\n"
            "    part = exp_table[exp_table['scaled'] == scaled]\n"
            "    plt.plot(part['k'], part['accuracy'], marker='o', label=f'scaled={scaled}')\n"
            "plt.xlabel('k (число соседей)'); plt.ylabel('точность на проверочной части')\n"
            "plt.legend(); plt.tight_layout()\n"
            "plot_path = _P('figures/config_accuracy.png'); plt.savefig(plot_path); plt.close()\n"
            "print(best_k, best_scaled, round(acc_final, 4), round(baseline_final, 4),\n"
            "      round(acc_peek, 4), round(optimism, 4))"
        ),
        md("## Урок. 7–9. Чек-лист, отчёт, мост к модулю 5"),
        code(
            "acceptance = pd.Series(\n"
            "    [True, True, True, True, True, True],\n"
            "    index=['baseline', 'protocol', 'experiments_csv', 'figure', 'final_score', 'limitations'],\n"
            ")\n"
            "n_final_looks = 1\n"
            "REPORT = (\n"
            "    f'Данные: 1797 картинок цифр 8x8, значения пикселя 0..16. Протокол: 60/20/20 со stratify, '\n"
            "    f'настройки выбирались по проверочной части, финальная часть использована один раз. '\n"
            "    f'Выбрано k={best_k}, масштабирование={best_scaled}. Точность на финальной части '\n"
            "    f'{acc_final:.3f} против baseline самой частой цифры {baseline_final:.3f}. '\n"
            "    f'Ограничения: картинки 8x8 вместо полного разрешения, kNN хранит всю обучающую часть '\n"
            "    f'и отвечает тем дольше, чем больше данных; поток реальной почты может быть смещён.'\n"
            ")\n"
            "READY = True\n"
            "NEXT_MODULE = (\n"
            "    'kNN не обучается заранее: на каждый конверт он сравнивает картинку со всей обучающей частью, '\n"
            "    'поэтому миллион примеров означает миллион сравнений на один ответ. '\n"
            "    'Дальше учимся строить признаки — они дают больше, чем замена модели.'\n"
            ")\n"
            "print(acceptance.all(), len(REPORT), READY)"
        ),
        md("## ДЗ. 1–4"),
        code(
            "rows = []\n"
            "for k, metric in itertools.product([1, 3, 5, 7, 9], ['euclidean', 'manhattan']):\n"
            "    m = KNeighborsClassifier(n_neighbors=k, metric=metric).fit(X_fit, y_fit)\n"
            "    rows.append([k, metric, float(accuracy_score(y_val, m.predict(X_val)))])\n"
            "metric_table = pd.DataFrame(rows, columns=['k', 'metric', 'accuracy'])\n"
            "best_row = metric_table.sort_values('accuracy', ascending=False).iloc[0]\n"
            "csv_path = _P('metric_experiments.csv')\n"
            "metric_table.to_csv(csv_path, index=False)\n"
            "report_md = (\n"
            "    '## Данные\\n1797 картинок 8x8, десять цифр, доли классов почти равные.\\n\\n'\n"
            "    '## Протокол\\n60/20/20 со stratify; настройки выбираются по проверочной части; '\n"
            "    'финальная часть — один раз.\\n\\n'\n"
            "    f'## Опыты\\nПеребрано {len(metric_table)} настроек (k x способ измерять расстояние). '\n"
            "    f\"Лучшая: k={int(best_row['k'])}, {best_row['metric']}, \"\n"
            "    f\"точность на проверочной {best_row['accuracy']:.3f}.\\n\\n\"\n"
            "    '## Итог\\nРаспознаватель уверенно бьёт baseline самой частой цифры (~0.10).\\n\\n'\n"
            "    '## Ограничения\\nМелкие картинки 8x8; kNN медленный на больших данных; '\n"
            "    'реальный поток индексов может быть смещён по цифрам.'\n"
            ")\n"
            "REFLECTION = (\n"
            "    'В начале модуля точность казалась одним числом про модель. Теперь видно, что число зависит '\n"
            "    'от разбиения, от baseline, от масштаба признаков и от того, сколько раз мы подглядывали '\n"
            "    'в проверочные данные. Честный результат — это протокол, а не удачный запуск.'\n"
            ")\n"
            "HONEST_LOOKS = 1\n"
            "print(metric_table)\n"
            "print(best_row)"
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
    add_lesson06,
]


def main() -> None:
    if not DATA_CSV.exists():
        raise SystemExit(f"Missing {DATA_CSV}. Run data/make_digits_csv.py first.")
    for builder in BUILDERS:
        builder()
    for rel, notebook in NOTEBOOKS.items():
        write(rel, notebook)
    for d in LESSON_DIRS:
        copy_csv(d)
    print(f"done: {len(NOTEBOOKS)} notebooks in {len(LESSON_DIRS)} lessons")


if __name__ == "__main__":
    main()
