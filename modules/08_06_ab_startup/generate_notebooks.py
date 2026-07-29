#!/usr/bin/env python3
"""Generate lesson notebooks for module 08_06 (KTP pairs 36-41).

Source of truth for .ipynb: edit this file, then run it.
Pattern: stubs + asserts in lesson/homework; full solutions.
"""

from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_CSV = ROOT / "data" / "startup_ab.csv"

SOL_BANNER = (
    "**Для преподавателя.** Эталон к `lesson.ipynb` и `homework.ipynb`. "
    "Не показывать ученикам до сдачи."
)

LOAD_DATA = (
    "from pathlib import Path\n"
    "import numpy as np\n"
    "import pandas as pd\n\n\n"
    "def _find(name: str) -> Path:\n"
    "    for p in (Path(name), Path(f'../../data/{name}'), Path(f'../data/{name}')):\n"
    "        if p.exists():\n"
    "            return p.resolve()\n"
    "    raise FileNotFoundError(f'{name} не найден рядом с ноутбуком')\n\n\n"
    "CSV_PATH = _find('startup_ab.csv')\n"
    "df = pd.read_csv(CSV_PATH)\n"
    "df['variant_b'] = (df['variant'] == 'B').astype(int)\n"
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
    dest = ROOT / lesson_dir / "startup_ab.csv"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DATA_CSV, dest)
    print("copied startup_ab.csv ->", dest)


NOTEBOOKS: dict[str, dict] = {}
LESSON_DIRS = [
    "lessons/01_hypotheses_pvalue",
    "lessons/02_practice_permutation",
    "lessons/03_ci_correlation",
    "lessons/04_practice_ci_corr",
    "lessons/05_peeking_multireg",
    "lessons/06_practice_report",
]

LESSON_CONTEXT = {
    "01_hypotheses_pvalue": (
        "От наблюдаемого uplift к проверяемой гипотезе",
        "Сначала измеряем конверсии A и B, затем строим нулевое распределение перестановками. "
        "Каждое число сопровождаем смыслом: что именно было зафиксировано до анализа и какой вывод допустим.",
    ),
    "02_practice_permutation": (
        "Воспроизводимая функция перестановочного теста",
        "Собираем расчёт в функцию с явными параметрами `n_iter` и `seed`, проверяем её на сегментах "
        "и отделяем величину эффекта от статистической совместимости с H0.",
    ),
    "03_ci_correlation": (
        "Неопределённость эффекта и границы корреляции",
        "Bootstrap показывает диапазон правдоподобных uplift, а корреляции помогают искать связи. "
        "Ни один из этих инструментов сам по себе не доказывает причинность.",
    ),
    "04_practice_ci_corr": (
        "Устойчивость вывода по сегментам",
        "Сравниваем источники трафика, устройства и скидки. Малый сегмент даёт широкий интервал, "
        "поэтому знак точечной оценки нельзя превращать в уверенный product-вывод.",
    ),
    "05_peeking_multireg": (
        "Честный stop-rule и модель факторов",
        "Накопительные p-value демонстрируют риск peeking. Множественная регрессия дополняет A/B-анализ, "
        "но её коэффициенты описывают условные связи, а не автоматически причинные эффекты.",
    ),
    "06_practice_report": (
        "От расчётов к проверяемому решению",
        "Собираем метрику, p-value, CI, модель факторов и ограничения в единый отчёт. "
        "Рекомендация считается готовой только тогда, когда каждое утверждение опирается на число.",
    ),
}


def enrich_student_notebook(notebook: dict, lesson_key: str, kind: str) -> dict:
    """Add teaching narrative without hiding executable student work."""
    title, framing = LESSON_CONTEXT[lesson_key]
    cells = notebook["cells"]
    intro = (
        f"## Маршрут работы\n\n**Фокус:** {title}.\n\n{framing}\n\n"
        "**Правило работы:** выполняйте ячейки сверху вниз, заменяйте `None` и пустые строки, "
        "а после каждого шага добивайтесь зелёных `assert`. Не удаляйте проверки: они задают контракт результата.\n\n"
        "**Что сдаём:** выполненный ноутбук, численный результат и короткую интерпретацию без причинных обещаний."
    )
    cells.insert(1, md(intro))
    if kind == "lesson":
        cells.append(md(
            "## Выходной билет\n\n"
            "1. Запишите одним предложением, что измеряет полученное число.\n"
            "2. Назовите одно ограничение анализа.\n"
            "3. Укажите, какое решение нельзя принимать только по точечной оценке.\n\n"
            "Перед сдачей перезапустите ноутбук целиком: `Restart & Run All` должен пройти без ошибок."
        ))
    else:
        cells.insert(2, md(
            "## A. Закрепление и Challenge\n\n"
            "Задачи **A** повторяют основной приём пары на новом срезе данных. "
            "Задачи **Challenge** требуют самостоятельно выбрать процедуру и защитить интерпретацию. "
            "Сначала добейтесь корректного кода, затем пишите вывод."
        ))
        cells.append(md(
            "## Чек-лист домашней работы\n\n"
            "- [ ] Все `assert` зелёные.\n"
            "- [ ] Seed сохранён, результат воспроизводится.\n"
            "- [ ] В выводе названы эффект, неопределённость и ограничение.\n"
            "- [ ] Корреляция или коэффициент модели не названы доказательством причины."
        ))
    return notebook


def sectionalize_solution(notebook: dict, lesson_key: str) -> dict:
    """Turn a monolithic answer dump into readable, executable sections."""
    title, framing = LESSON_CONTEXT[lesson_key]
    original = notebook["cells"]
    load_cell = original[1]
    source = "".join(original[2]["source"])
    tree = ast.parse(source)
    chunks: list[str] = []
    current: list[str] = []
    for node in tree.body:
        segment = ast.get_source_segment(source, node)
        if segment is None:
            continue
        current.append(segment)
        if len(current) >= 3 or isinstance(node, (ast.FunctionDef, ast.For)):
            chunks.append("\n\n".join(current))
            current = []
    if current:
        chunks.append("\n\n".join(current))

    cells = [
        original[0],
        md(
            f"## Карта эталона\n\n**Фокус:** {title}.\n\n{framing}\n\n"
            "Эталон разделён на исполняемые секции в том же порядке, что `lesson.ipynb` и `homework.ipynb`. "
            "После каждой секции сверяйте не только значение, но и способ вычисления."
        ),
        load_cell,
    ]
    for index, chunk in enumerate(chunks, start=1):
        cells.append(md(
            f"## Решение {index}\n\n"
            "Выполните секцию после всех предыдущих: переменные намеренно переиспользуются, "
            "чтобы эталон воспроизводил полный аналитический pipeline."
        ))
        cells.append(code(chunk))
    cells.append(md(
        "## Проверка преподавателя\n\n"
        "Запустите `Run All`. Эталон должен завершиться без исключений; итоговые числа должны совпадать "
        "при повторном запуске благодаря фиксированным seed. Текстовый вывод проверяется на согласованность "
        "с направлением uplift, p-value и границами CI."
    ))
    notebook["cells"] = cells
    return notebook


def add_lesson01() -> None:
    base = "lessons/01_hypotheses_pvalue"
    lesson = nb(
        md("# H0/H1 и p-value через симуляцию\n\nСтартап тестирует два лендинга: `A` и `B`."),
        code(LOAD_DATA),
        md("## 1. Конверсия по вариантам"),
        code(
            "conv_a = None\n"
            "conv_b = None\n"
            "uplift = None\n"
            "assert conv_a is not None and conv_b is not None and uplift is not None\n"
            "assert 0.05 < float(conv_a) < 0.5\n"
            "assert 0.05 < float(conv_b) < 0.5\n"
            "print(round(float(conv_a), 4), round(float(conv_b), 4), round(float(uplift), 4))"
        ),
        md("## 2. Гипотезы"),
        code(
            "H0 = ''\n"
            "H1 = ''\n"
            "assert len(H0) > 20 and len(H1) > 20\n"
            "print(H0)\n"
            "print(H1)"
        ),
        md("## 3. Наблюдаемая разность долей"),
        code(
            "obs_diff = None  # conv_B - conv_A\n"
            "assert obs_diff is not None\n"
            "assert -0.2 < float(obs_diff) < 0.2\n"
            "print(round(float(obs_diff), 5))"
        ),
        md("## 4. Симуляция нулевого распределения (перестановки)"),
        code(
            "rng = np.random.default_rng(36)\n"
            "n_iter = 2000\n"
            "sim_diffs = []\n"
            "# заполняйте sim_diffs перестановками метки converted\n"
            "assert len(sim_diffs) == n_iter\n"
            "assert np.isfinite(sim_diffs).all()\n"
            "print(np.mean(sim_diffs), np.std(sim_diffs))"
        ),
        md("## 5. Двусторонний p-value"),
        code(
            "p_value = None\n"
            "assert p_value is not None\n"
            "assert 0 <= float(p_value) <= 1\n"
            "print(round(float(p_value), 5))"
        ),
        md("## 6. Вывод по уровню 5%"),
        code(
            "decision = ''\n"
            "assert len(decision) > 30\n"
            "print(decision)"
        ),
        md("## 7. Почему p-value не равен вероятности H0"),
        code(
            "PVAL_NOTE = ''\n"
            "assert len(PVAL_NOTE) > 120\n"
            "print(PVAL_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: H0/H1 и симуляция p-value"),
        code(LOAD_DATA),
        md("### A. Закрепление\n\n## 1. Подвыборка desktop"),
        code(
            "desktop = None\n"
            "obs_desktop = None\n"
            "assert desktop is not None and obs_desktop is not None\n"
            "assert len(desktop) > 800\n"
            "print(round(float(obs_desktop), 5))"
        ),
        md("## 2. p-value на desktop"),
        code(
            "p_desktop = None\n"
            "assert p_desktop is not None and 0 <= float(p_desktop) <= 1\n"
            "print(round(float(p_desktop), 5))"
        ),
        md("### Challenge\n\n## 3. Односторонняя альтернатива"),
        code(
            "p_one_sided = None\n"
            "ONE_NOTE = ''\n"
            "assert p_one_sided is not None and 0 <= float(p_one_sided) <= 1\n"
            "assert len(ONE_NOTE) > 80\n"
            "print(round(float(p_one_sided), 5), ONE_NOTE)"
        ),
        md("## 4. Почему нельзя делать вывод без протокола"),
        code(
            "PROTOCOL_NOTE = ''\n"
            "assert len(PROTOCOL_NOTE) > 140\n"
            "print(PROTOCOL_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: H0/H1 и p-value\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        code(
            "conv_a = float(df.loc[df['variant'] == 'A', 'converted'].mean())\n"
            "conv_b = float(df.loc[df['variant'] == 'B', 'converted'].mean())\n"
            "uplift = conv_b - conv_a\n"
            "H0 = 'H0: конверсия одинаковая, различие A/B случайно.'\n"
            "H1 = 'H1: конверсия B отличается от A (двусторонняя альтернатива).'\n"
            "obs_diff = uplift\n"
            "rng = np.random.default_rng(36)\n"
            "n_iter = 2000\n"
            "conv = df['converted'].to_numpy()\n"
            "mask_b = df['variant'].to_numpy() == 'B'\n"
            "sim_diffs = []\n"
            "for _ in range(n_iter):\n"
            "    perm = rng.permutation(conv)\n"
            "    sim_diffs.append(float(perm[mask_b].mean() - perm[~mask_b].mean()))\n"
            "sim_diffs = np.array(sim_diffs)\n"
            "p_value = float((np.abs(sim_diffs) >= abs(obs_diff)).mean())\n"
            "decision = (\n"
            "    'Если p-value < 0.05, отклоняем H0 и считаем эффект статистически значимым. '\n"
            "    'Если p-value >= 0.05, данных недостаточно, чтобы уверенно отвергнуть случайность.'\n"
            ")\n"
            "PVAL_NOTE = (\n"
            "    'p-value — это вероятность получить наблюдаемое или более сильное различие, '\n"
            "    'если H0 верна. Это не вероятность истинности самой H0.'\n"
            ")\n"
            "desktop = df[df['device'] == 'desktop']\n"
            "obs_desktop = float(\n"
            "    desktop.loc[desktop['variant'] == 'B', 'converted'].mean()\n"
            "    - desktop.loc[desktop['variant'] == 'A', 'converted'].mean()\n"
            ")\n"
            "conv_d = desktop['converted'].to_numpy()\n"
            "mask_bd = desktop['variant'].to_numpy() == 'B'\n"
            "sim_d = []\n"
            "for _ in range(2000):\n"
            "    perm = rng.permutation(conv_d)\n"
            "    sim_d.append(float(perm[mask_bd].mean() - perm[~mask_bd].mean()))\n"
            "sim_d = np.array(sim_d)\n"
            "p_desktop = float((np.abs(sim_d) >= abs(obs_desktop)).mean())\n"
            "p_one_sided = float((sim_d >= obs_desktop).mean())\n"
            "ONE_NOTE = 'Односторонняя альтернатива уместна только если направление эффекта задано до сбора данных.'\n"
            "PROTOCOL_NOTE = (\n"
            "    'Без заранее заданного протокола легко подбирать гипотезу, подвыборку и число запусков под желаемый вывод. '\n"
            "    'Это резко повышает риск ложной значимости.'\n"
            ")\n"
            "print(round(conv_a, 4), round(conv_b, 4), round(p_value, 5), round(p_desktop, 5))"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson02() -> None:
    base = "lessons/02_practice_permutation"
    lesson = nb(
        md("# Практика: перестановочный тест"),
        code(LOAD_DATA),
        md("## 1. Функция permutation_test_diff"),
        code(
            "def permutation_test_diff(frame, n_iter=3000, seed=0):\n"
            "    # вернуть obs_diff, p_value\n"
            "    return None, None\n\n\n"
            "obs, p = permutation_test_diff(df)\n"
            "assert obs is not None and p is not None\n"
            "assert -0.2 < float(obs) < 0.2\n"
            "assert 0 <= float(p) <= 1\n"
            "print(obs, p)"
        ),
        md("## 2. Сравнение по устройствам"),
        code(
            "obs_mob, p_mob = None, None\n"
            "obs_des, p_des = None, None\n"
            "assert None not in (obs_mob, p_mob, obs_des, p_des)\n"
            "print(obs_mob, p_mob, obs_des, p_des)"
        ),
        md("## 3. Стабильность при разном числе итераций"),
        code(
            "p_500 = None\n"
            "p_2000 = None\n"
            "p_8000 = None\n"
            "assert None not in (p_500, p_2000, p_8000)\n"
            "print(p_500, p_2000, p_8000)"
        ),
        md("## 4. Интерпретация результата"),
        code(
            "INTERP = ''\n"
            "assert len(INTERP) > 120\n"
            "print(INTERP)"
        ),
    )
    hw = nb(
        md("# ДЗ: permutation practice"),
        code(LOAD_DATA),
        md("### A. Закрепление\n\n## 1. Только трафик ads"),
        code(
            "ads = None\n"
            "p_ads = None\n"
            "assert ads is not None and p_ads is not None\n"
            "assert len(ads) > 600\n"
            "print(round(float(p_ads), 5))"
        ),
        md("## 2. Проверка через random split"),
        code(
            "rng = np.random.default_rng(77)\n"
            "half_idx = None\n"
            "p_half = None\n"
            "assert half_idx is not None and p_half is not None\n"
            "print(len(half_idx), p_half)"
        ),
        md("### Challenge\n\n## 3. Функция с возвращением таблицы симуляций"),
        code(
            "sim_table = None\n"
            "assert sim_table is not None\n"
            "assert {'sim_diff'} <= set(sim_table.columns)\n"
            "assert len(sim_table) >= 1000\n"
            "print(sim_table.head())"
        ),
        md("## 4. Риск p-hacking"),
        code(
            "PHACK_NOTE = ''\n"
            "assert len(PHACK_NOTE) > 150\n"
            "print(PHACK_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: permutation practice\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        code(
            "def permutation_test_diff(frame, n_iter=3000, seed=0):\n"
            "    rng = np.random.default_rng(seed)\n"
            "    conv = frame['converted'].to_numpy()\n"
            "    mask_b = frame['variant'].to_numpy() == 'B'\n"
            "    obs = float(conv[mask_b].mean() - conv[~mask_b].mean())\n"
            "    sims = np.empty(n_iter)\n"
            "    for i in range(n_iter):\n"
            "        perm = rng.permutation(conv)\n"
            "        sims[i] = perm[mask_b].mean() - perm[~mask_b].mean()\n"
            "    p = float((np.abs(sims) >= abs(obs)).mean())\n"
            "    return obs, p\n\n\n"
            "obs, p = permutation_test_diff(df, n_iter=3000, seed=37)\n"
            "mob = df[df['device'] == 'mobile']\n"
            "des = df[df['device'] == 'desktop']\n"
            "obs_mob, p_mob = permutation_test_diff(mob, n_iter=3000, seed=38)\n"
            "obs_des, p_des = permutation_test_diff(des, n_iter=3000, seed=39)\n"
            "_, p_500 = permutation_test_diff(df, n_iter=500, seed=40)\n"
            "_, p_2000 = permutation_test_diff(df, n_iter=2000, seed=40)\n"
            "_, p_8000 = permutation_test_diff(df, n_iter=8000, seed=40)\n"
            "INTERP = (\n"
            "    'p-value отвечает на вопрос совместимости данных с H0, а не на вопрос масштаба эффекта. '\n"
            "    'Всегда интерпретируем p-value вместе с самой разницей конверсий и бизнес-контекстом.'\n"
            ")\n"
            "ads = df[df['traffic_source'] == 'ads']\n"
            "_, p_ads = permutation_test_diff(ads, n_iter=3000, seed=41)\n"
            "rng = np.random.default_rng(77)\n"
            "half_idx = rng.choice(df.index.to_numpy(), size=len(df) // 2, replace=False)\n"
            "half = df.loc[half_idx]\n"
            "_, p_half = permutation_test_diff(half, n_iter=3000, seed=42)\n"
            "rng2 = np.random.default_rng(43)\n"
            "conv = df['converted'].to_numpy()\n"
            "mask_b = df['variant'].to_numpy() == 'B'\n"
            "sim_vals = []\n"
            "for _ in range(1200):\n"
            "    perm = rng2.permutation(conv)\n"
            "    sim_vals.append(float(perm[mask_b].mean() - perm[~mask_b].mean()))\n"
            "sim_table = pd.DataFrame({'sim_diff': sim_vals})\n"
            "PHACK_NOTE = (\n"
            "    'Если запускать тест много раз, отбирать удобные подвыборки и останавливать анализ на удачном моменте, '\n"
            "    'можно получить ложную значимость даже без реального эффекта.'\n"
            ")\n"
            "print(round(p, 5), round(p_mob, 5), round(p_des, 5), round(p_ads, 5), round(p_half, 5))"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson03() -> None:
    base = "lessons/03_ci_correlation"
    lesson = nb(
        md("# Доверительные интервалы и ограничения корреляции"),
        code(LOAD_DATA),
        md("## 1. Bootstrap CI для разности конверсий B-A"),
        code(
            "rng = np.random.default_rng(380)\n"
            "boot_diffs = []\n"
            "ci_low = None\n"
            "ci_high = None\n"
            "assert len(boot_diffs) >= 1000\n"
            "assert ci_low is not None and ci_high is not None\n"
            "assert float(ci_low) < float(ci_high)\n"
            "print(ci_low, ci_high)"
        ),
        md("## 2. Интерпретация CI"),
        code(
            "CI_NOTE = ''\n"
            "assert len(CI_NOTE) > 120\n"
            "print(CI_NOTE)"
        ),
        md("## 3. Корреляция pages_viewed и converted"),
        code(
            "corr_pages = None\n"
            "assert corr_pages is not None\n"
            "assert -1 <= float(corr_pages) <= 1\n"
            "print(round(float(corr_pages), 4))"
        ),
        md("## 4. Корреляция session_minutes и converted"),
        code(
            "corr_time = None\n"
            "assert corr_time is not None\n"
            "assert -1 <= float(corr_time) <= 1\n"
            "print(round(float(corr_time), 4))"
        ),
        md("## 5. Почему корреляция не равна причинности"),
        code(
            "CAUSE_NOTE = ''\n"
            "assert len(CAUSE_NOTE) > 150\n"
            "print(CAUSE_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: CI и корреляция"),
        code(LOAD_DATA),
        md("### A. Закрепление\n\n## 1. CI для конверсии только в B"),
        code(
            "ci_b = None\n"
            "assert ci_b is not None and len(ci_b) == 2\n"
            "assert float(ci_b[0]) < float(ci_b[1])\n"
            "print(ci_b)"
        ),
        md("## 2. CI для средней выручки"),
        code(
            "ci_rev = None\n"
            "assert ci_rev is not None and len(ci_rev) == 2\n"
            "print(ci_rev)"
        ),
        md("### Challenge\n\n## 3. Корреляции в разрезе device"),
        code(
            "corr_table = None\n"
            "assert corr_table is not None\n"
            "assert {'device', 'corr_pages_conv'} <= set(corr_table.columns)\n"
            "print(corr_table)"
        ),
        md("## 4. Ограничения анализа"),
        code(
            "LIMIT_NOTE = ''\n"
            "assert len(LIMIT_NOTE) > 140\n"
            "print(LIMIT_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: CI и корреляция\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        code(
            "rng = np.random.default_rng(380)\n"
            "a = df[df['variant'] == 'A']['converted'].to_numpy()\n"
            "b = df[df['variant'] == 'B']['converted'].to_numpy()\n"
            "boot_diffs = []\n"
            "for _ in range(2500):\n"
            "    a_s = rng.choice(a, size=len(a), replace=True)\n"
            "    b_s = rng.choice(b, size=len(b), replace=True)\n"
            "    boot_diffs.append(float(b_s.mean() - a_s.mean()))\n"
            "ci_low, ci_high = np.quantile(boot_diffs, [0.025, 0.975])\n"
            "CI_NOTE = (\n"
            "    '95% CI — диапазон правдоподобных значений эффекта при выбранной процедуре. '\n"
            "    'Если ноль вне интервала, эффект статистически совместим с отличием от нуля.'\n"
            ")\n"
            "corr_pages = float(df['pages_viewed'].corr(df['converted']))\n"
            "corr_time = float(df['session_minutes'].corr(df['converted']))\n"
            "CAUSE_NOTE = (\n"
            "    'Высокая корреляция не доказывает причинность: на обе переменные может влиять скрытый фактор '\n"
            "    '(например, качество трафика или намерение пользователя купить).' \n"
            ")\n"
            "b_conv = b\n"
            "boot_b = [float(rng.choice(b_conv, size=len(b_conv), replace=True).mean()) for _ in range(2500)]\n"
            "ci_b = tuple(np.quantile(boot_b, [0.025, 0.975]))\n"
            "rev = df['order_value'].to_numpy()\n"
            "boot_rev = [float(rng.choice(rev, size=len(rev), replace=True).mean()) for _ in range(2500)]\n"
            "ci_rev = tuple(np.quantile(boot_rev, [0.025, 0.975]))\n"
            "rows = []\n"
            "for dev in ['desktop', 'mobile']:\n"
            "    part = df[df['device'] == dev]\n"
            "    rows.append({'device': dev, 'corr_pages_conv': float(part['pages_viewed'].corr(part['converted']))})\n"
            "corr_table = pd.DataFrame(rows)\n"
            "LIMIT_NOTE = (\n"
            "    'Даже при CI и корреляциях остаются ограничения: синтетические данные, возможные скрытые факторы, '\n"
            "    'и линейная связь может быть только приближением.'\n"
            ")\n"
            "print((round(ci_low, 4), round(ci_high, 4)), round(corr_pages, 4), round(corr_time, 4))"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson04() -> None:
    base = "lessons/04_practice_ci_corr"
    lesson = nb(
        md("# Практика: CI и корреляция на сегментах"),
        code(LOAD_DATA),
        md("## 1. Таблица сегментов (traffic_source x device)"),
        code(
            "seg = None\n"
            "assert seg is not None\n"
            "assert {'traffic_source', 'device', 'n'} <= set(seg.columns)\n"
            "print(seg)"
        ),
        md("## 2. CI uplift по каждому источнику"),
        code(
            "ci_source = None\n"
            "assert ci_source is not None\n"
            "assert {'traffic_source', 'ci_low', 'ci_high'} <= set(ci_source.columns)\n"
            "print(ci_source)"
        ),
        md("## 3. Где знак эффекта может отличаться"),
        code(
            "SIGN_NOTE = ''\n"
            "assert len(SIGN_NOTE) > 90\n"
            "print(SIGN_NOTE)"
        ),
        md("## 4. Корреляция age и converted"),
        code(
            "corr_age = None\n"
            "assert corr_age is not None and -1 <= float(corr_age) <= 1\n"
            "print(corr_age)"
        ),
        md("## 5. Текст для отчёта"),
        code(
            "REPORT_LINE = ''\n"
            "assert len(REPORT_LINE) > 100\n"
            "print(REPORT_LINE)"
        ),
    )
    hw = nb(
        md("# ДЗ: сегментный анализ"),
        code(LOAD_DATA),
        md("### A. Закрепление\n\n## 1. CI uplift по скидке"),
        code(
            "ci_discount = None\n"
            "assert ci_discount is not None\n"
            "assert {'discount_pct', 'ci_low', 'ci_high'} <= set(ci_discount.columns)\n"
            "print(ci_discount)"
        ),
        md("## 2. Корреляция prior_visits и converted"),
        code(
            "corr_prior = None\n"
            "assert corr_prior is not None\n"
            "print(corr_prior)"
        ),
        md("### Challenge\n\n## 3. Мини-вывод по устойчивости эффекта"),
        code(
            "STABILITY_NOTE = ''\n"
            "assert len(STABILITY_NOTE) > 150\n"
            "print(STABILITY_NOTE)"
        ),
        md("## 4. Что проверить перед product-решением"),
        code(
            "CHECKLIST = ''\n"
            "assert len(CHECKLIST) > 180\n"
            "print(CHECKLIST)"
        ),
    )
    sol = nb(
        md("# Решения: практикум CI/correlation\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        code(
            "seg = (\n"
            "    df.groupby(['traffic_source', 'device'])\n"
            "    .agg(n=('user_id', 'count'), conv=('converted', 'mean'))\n"
            "    .reset_index()\n"
            ")\n"
            "def ci_uplift(part, seed=0, n_iter=1500):\n"
            "    rng = np.random.default_rng(seed)\n"
            "    a = part[part['variant'] == 'A']['converted'].to_numpy()\n"
            "    b = part[part['variant'] == 'B']['converted'].to_numpy()\n"
            "    if len(a) < 20 or len(b) < 20:\n"
            "        return np.nan, np.nan\n"
            "    vals = []\n"
            "    for _ in range(n_iter):\n"
            "        vals.append(float(rng.choice(b, len(b), replace=True).mean() - rng.choice(a, len(a), replace=True).mean()))\n"
            "    return tuple(np.quantile(vals, [0.025, 0.975]))\n"
            "rows = []\n"
            "for i, src in enumerate(sorted(df['traffic_source'].unique())):\n"
            "    part = df[df['traffic_source'] == src]\n"
            "    low, high = ci_uplift(part, seed=390 + i)\n"
            "    rows.append({'traffic_source': src, 'ci_low': low, 'ci_high': high})\n"
            "ci_source = pd.DataFrame(rows)\n"
            "SIGN_NOTE = (\n"
            "    'В отдельных сегментах знак может отличаться из-за шума и разных размеров подвыборок. '\n"
            "    'Поэтому важны интервалы и проверка устойчивости эффекта.'\n"
            ")\n"
            "corr_age = float(df['age'].corr(df['converted']))\n"
            "REPORT_LINE = (\n"
            "    'По сегментам видно, что эффект B не обязан быть одинаковым во всех каналах: '\n"
            "    'часть различий может быть статистическим шумом в малых группах.'\n"
            ")\n"
            "rows2 = []\n"
            "for d, part in df.groupby('discount_pct'):\n"
            "    low, high = ci_uplift(part, seed=410 + int(d))\n"
            "    rows2.append({'discount_pct': int(d), 'ci_low': low, 'ci_high': high})\n"
            "ci_discount = pd.DataFrame(rows2).sort_values('discount_pct')\n"
            "corr_prior = float(df['prior_visits_30d'].corr(df['converted']))\n"
            "STABILITY_NOTE = (\n"
            "    'Эффект устойчивее, когда знак uplift совпадает в ключевых сегментах и интервалы не слишком широкие. '\n"
            "    'Если интервалы широкие, нужен больший объём данных.'\n"
            ")\n"
            "CHECKLIST = (\n"
            "    'Перед product-решением проверяем: протокол эксперимента, размер выборки, CI эффекта, '\n"
            "    'чувствительность к сегментам, отсутствие peeking и согласованность с бизнес-ограничениями.'\n"
            ")\n"
            "print(seg.head())\n"
            "print(ci_source)\n"
            "print(corr_age, corr_prior)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson05() -> None:
    base = "lessons/05_peeking_multireg"
    lesson = nb(
        md("# Peeking risk и множественная линейная регрессия"),
        code(LOAD_DATA),
        md("## 1. Накопительный p-value по дням"),
        code(
            "def perm_p(frame, seed=0, n_iter=1200):\n"
            "    return None\n\n\n"
            "daily = None\n"
            "first_sig_day = None\n"
            "assert daily is not None\n"
            "assert {'day', 'p_value'} <= set(daily.columns)\n"
            "assert first_sig_day is not None\n"
            "print(daily.head(), first_sig_day)"
        ),
        md("## 2. Почему peeking опасен"),
        code(
            "PEEK_NOTE = ''\n"
            "assert len(PEEK_NOTE) > 140\n"
            "print(PEEK_NOTE)"
        ),
        md("## 3. Подготовка признаков для LinearRegression"),
        code(
            "X = None\n"
            "y = None\n"
            "assert X is not None and y is not None\n"
            "assert X.shape[0] == len(df) and len(y) == len(df)\n"
            "print(X.columns.tolist())"
        ),
        md("## 4. Обучение модели и коэффициенты"),
        code(
            "from sklearn.linear_model import LinearRegression\n\n"
            "model = None\n"
            "coef_table = None\n"
            "r2 = None\n"
            "assert model is not None and coef_table is not None and r2 is not None\n"
            "assert {'feature', 'coef'} <= set(coef_table.columns)\n"
            "print(coef_table)\n"
            "print(r2)"
        ),
        md("## 5. Интерпретация коэффициента variant_b"),
        code(
            "VARIANT_NOTE = ''\n"
            "assert len(VARIANT_NOTE) > 120\n"
            "print(VARIANT_NOTE)"
        ),
        md("## 6. Ограничения линейной регрессии для 0/1 target"),
        code(
            "LIN_NOTE = ''\n"
            "assert len(LIN_NOTE) > 150\n"
            "print(LIN_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: peeking и multireg"),
        code(LOAD_DATA),
        md("### A. Закрепление\n\n## 1. Сравнить две модели признаков"),
        code(
            "r2_small = None\n"
            "r2_full = None\n"
            "assert r2_small is not None and r2_full is not None\n"
            "print(r2_small, r2_full)"
        ),
        md("## 2. Коэффициенты и знак эффекта"),
        code(
            "coef_variant = None\n"
            "coef_pages = None\n"
            "assert coef_variant is not None and coef_pages is not None\n"
            "print(coef_variant, coef_pages)"
        ),
        md("### Challenge\n\n## 3. Мини-правила против peeking"),
        code(
            "ANTI_PEEK = ''\n"
            "assert len(ANTI_PEEK) > 150\n"
            "print(ANTI_PEEK)"
        ),
        md("## 4. Ограничения интерпретации коэффициентов"),
        code(
            "COEF_LIMIT = ''\n"
            "assert len(COEF_LIMIT) > 160\n"
            "print(COEF_LIMIT)"
        ),
    )
    sol = nb(
        md("# Решения: peeking и multireg\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        code(
            "def perm_p(frame, seed=0, n_iter=1200):\n"
            "    rng = np.random.default_rng(seed)\n"
            "    conv = frame['converted'].to_numpy()\n"
            "    mask_b = frame['variant'].to_numpy() == 'B'\n"
            "    obs = float(conv[mask_b].mean() - conv[~mask_b].mean())\n"
            "    sims = np.empty(n_iter)\n"
            "    for i in range(n_iter):\n"
            "        perm = rng.permutation(conv)\n"
            "        sims[i] = perm[mask_b].mean() - perm[~mask_b].mean()\n"
            "    return float((np.abs(sims) >= abs(obs)).mean())\n"
            "rows = []\n"
            "for d in range(1, 31):\n"
            "    part = df[df['day'] <= d]\n"
            "    if len(part) >= 200:\n"
            "        rows.append({'day': d, 'p_value': perm_p(part, seed=500 + d)})\n"
            "daily = pd.DataFrame(rows)\n"
            "sig_days = daily.loc[daily['p_value'] < 0.05, 'day']\n"
            "first_sig_day = int(sig_days.iloc[0]) if len(sig_days) else -1\n"
            "PEEK_NOTE = (\n"
            "    'Если смотреть p-value каждый день и останавливать эксперимент при первом p<0.05, '\n"
            "    'растёт шанс ложноположительного вывода из-за многократной проверки.'\n"
            ")\n"
            "from sklearn.linear_model import LinearRegression\n"
            "X = df[['variant_b', 'pages_viewed', 'prior_visits_30d', 'discount_pct', 'session_minutes', 'is_weekend']]\n"
            "y = df['converted']\n"
            "model = LinearRegression().fit(X, y)\n"
            "coef_table = pd.DataFrame({'feature': X.columns, 'coef': model.coef_}).sort_values('feature')\n"
            "r2 = float(model.score(X, y))\n"
            "VARIANT_NOTE = (\n"
            "    'Коэффициент при variant_b показывает среднее изменение предсказанной конверсии для B '\n"
            "    'при фиксированных остальных признаках модели.'\n"
            ")\n"
            "LIN_NOTE = (\n"
            "    'Линейная регрессия на target 0/1 проста для интерпретации, но может давать прогнозы вне [0, 1] '\n"
            "    'и не учитывает нелинейность вероятности. Это учебная аппроксимация.'\n"
            ")\n"
            "X_small = df[['variant_b', 'pages_viewed']]\n"
            "r2_small = float(LinearRegression().fit(X_small, y).score(X_small, y))\n"
            "r2_full = r2\n"
            "coef_variant = float(model.coef_[0])\n"
            "coef_pages = float(model.coef_[1])\n"
            "ANTI_PEEK = (\n"
            "    'Фиксируем заранее длительность эксперимента и критерий остановки; '\n"
            "    'не меняем гипотезу по ходу; одну итоговую проверку делаем после полного сбора данных.'\n"
            ")\n"
            "COEF_LIMIT = (\n"
            "    'Коэффициенты описывают связь внутри выбранной модели и признаков, но не доказывают причинность. '\n"
            "    'Пропущенные факторы и коррелированные признаки могут смещать интерпретацию.'\n"
            ")\n"
            "print(first_sig_day, round(r2, 4))\n"
            "print(coef_table)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson06() -> None:
    base = "lessons/06_practice_report"
    lesson = nb(
        md("# Практика: итоговый A/B отчёт"),
        code(LOAD_DATA),
        md("## 1. Соберите ключевые метрики"),
        code(
            "summary = None\n"
            "assert summary is not None\n"
            "assert {'conv_a', 'conv_b', 'uplift'} <= set(summary.index)\n"
            "print(summary)"
        ),
        md("## 2. p-value и CI в одном месте"),
        code(
            "p_value = None\n"
            "ci = None\n"
            "assert p_value is not None and ci is not None\n"
            "assert len(ci) == 2\n"
            "print(p_value, ci)"
        ),
        md("## 3. Коэффициенты регрессии (top-3 по модулю)"),
        code(
            "top_coef = None\n"
            "assert top_coef is not None and len(top_coef) == 3\n"
            "print(top_coef)"
        ),
        md("## 4. Acceptance checklist"),
        code(
            "acceptance = pd.Series(\n"
            "    [False, False, False, False, False],\n"
            "    index=['metric', 'p_value', 'ci', 'regression', 'limitations']\n"
            ")\n"
            "assert bool(acceptance.all())\n"
            "print(acceptance)"
        ),
        md("## 5. Итоговый REPORT"),
        code(
            "REPORT = ''\n"
            "READY = False\n"
            "assert len(REPORT) > 450\n"
            "assert READY is True\n"
            "print(REPORT)"
        ),
    )
    hw = nb(
        md("# ДЗ: финальный артефакт отчёта"),
        code(LOAD_DATA),
        md("### A. Закрепление\n\n## 1. Одна строка executive summary"),
        code(
            "EXEC_SUMMARY = ''\n"
            "assert len(EXEC_SUMMARY) > 120\n"
            "print(EXEC_SUMMARY)"
        ),
        md("## 2. Риски и ограничения"),
        code(
            "RISKS = ''\n"
            "assert len(RISKS) > 180\n"
            "print(RISKS)"
        ),
        md("### Challenge\n\n## 3. План следующего эксперимента"),
        code(
            "NEXT_AB = ''\n"
            "assert len(NEXT_AB) > 200\n"
            "print(NEXT_AB)"
        ),
        md("## 4. Рефлексия про статистический вывод"),
        code(
            "REFLECTION = ''\n"
            "assert len(REFLECTION) > 180\n"
            "print(REFLECTION)"
        ),
    )
    sol = nb(
        md("# Решения: итоговый отчёт\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        code(
            "from sklearn.linear_model import LinearRegression\n"
            "conv_a = float(df.loc[df['variant'] == 'A', 'converted'].mean())\n"
            "conv_b = float(df.loc[df['variant'] == 'B', 'converted'].mean())\n"
            "uplift = conv_b - conv_a\n"
            "summary = pd.Series({'conv_a': conv_a, 'conv_b': conv_b, 'uplift': uplift})\n"
            "rng = np.random.default_rng(610)\n"
            "conv = df['converted'].to_numpy()\n"
            "mask_b = df['variant'].to_numpy() == 'B'\n"
            "obs = uplift\n"
            "sims = []\n"
            "for _ in range(3000):\n"
            "    perm = rng.permutation(conv)\n"
            "    sims.append(float(perm[mask_b].mean() - perm[~mask_b].mean()))\n"
            "sims = np.array(sims)\n"
            "p_value = float((np.abs(sims) >= abs(obs)).mean())\n"
            "a = df[df['variant'] == 'A']['converted'].to_numpy()\n"
            "b = df[df['variant'] == 'B']['converted'].to_numpy()\n"
            "boot = []\n"
            "for _ in range(3000):\n"
            "    boot.append(float(rng.choice(b, len(b), replace=True).mean() - rng.choice(a, len(a), replace=True).mean()))\n"
            "ci = tuple(np.quantile(boot, [0.025, 0.975]))\n"
            "X = df[['variant_b', 'pages_viewed', 'prior_visits_30d', 'discount_pct', 'session_minutes', 'is_weekend']]\n"
            "model = LinearRegression().fit(X, df['converted'])\n"
            "coef = pd.Series(model.coef_, index=X.columns)\n"
            "top_coef = coef.abs().sort_values(ascending=False).head(3)\n"
            "acceptance = pd.Series(\n"
            "    [True, True, True, True, True],\n"
            "    index=['metric', 'p_value', 'ci', 'regression', 'limitations']\n"
            ")\n"
            "REPORT = (\n"
            "    f'Конверсия A={conv_a:.3f}, B={conv_b:.3f}, uplift={uplift:.3f}. '\n"
            "    f'Перестановочный p-value={p_value:.4f}; 95% CI uplift=[{ci[0]:.3f}, {ci[1]:.3f}]. '\n"
            "    'По линейной модели на 0/1 target наибольшие по модулю коэффициенты у variant_b, '\n"
            "    'pages_viewed и prior_visits_30d, что согласуется с гипотезой о вовлечённости. '\n"
            "    'Рекомендация: принимать решение по B только вместе с протоколом длительности эксперимента '\n"
            "    'и без подглядывания в промежуточные p-value. Ограничения: синтетические данные, '\n"
            "    'линейная аппроксимация для вероятности и отсутствие каузального вывода.'\n"
            ")\n"
            "READY = bool(acceptance.all())\n"
            "EXEC_SUMMARY = 'B показывает положительный uplift, но финальный вывод делаем только с учётом CI и p-value по фиксированному протоколу.'\n"
            "RISKS = (\n"
            "    'Основные риски: peeking, множественные проверки без коррекции, интерпретация корреляций как причинности, '\n"
            "    'и перенос учебной синтетики на реальный продукт без валидации.'\n"
            ")\n"
            "NEXT_AB = (\n"
            "    'Следующий эксперимент: заранее зафиксировать длительность 30 дней, primary metric и stop-rule, '\n"
            "    'добавить guardrail-метрики, а также продумать сегментный анализ до запуска. '\n"
            "    'После эксперимента — одна итоговая проверка и репликация на следующем трафик-окне.'\n"
            ")\n"
            "REFLECTION = (\n"
            "    'Статистический вывод — это не «нажал кнопку и получил истину», а связка протокола, '\n"
            "    'метрики, симуляции, интервалов и честной интерпретации ограничений.'\n"
            ")\n"
            "print(summary)\n"
            "print(round(p_value, 5), ci)\n"
            "print(top_coef)\n"
            "print('READY=', READY)"
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
        raise SystemExit(f"Missing {DATA_CSV}. Run data/make_startup_ab_csv.py first.")
    for builder in BUILDERS:
        builder()
    for rel, notebook in NOTEBOOKS.items():
        lesson_key = Path(rel).parent.name
        if rel.endswith("solutions.ipynb"):
            sectionalize_solution(notebook, lesson_key)
        elif rel.endswith("lesson.ipynb"):
            enrich_student_notebook(notebook, lesson_key, "lesson")
        elif rel.endswith("homework.ipynb"):
            enrich_student_notebook(notebook, lesson_key, "homework")
    for rel, notebook in NOTEBOOKS.items():
        write(rel, notebook)
    for d in LESSON_DIRS:
        copy_csv(d)
    print(f"done: {len(NOTEBOOKS)} notebooks in {len(LESSON_DIRS)} lessons")


if __name__ == "__main__":
    main()
