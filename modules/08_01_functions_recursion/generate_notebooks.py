#!/usr/bin/env python3
"""Generate lesson notebooks for module 08_01_functions_recursion (data/ML integrated)."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

DATA_IMPORT = (
    "import sys\n"
    "from pathlib import Path\n"
    "sys.path.insert(0, str(Path('../..').resolve()))\n"
    "from data.module_datasets import (\n"
    "    APARTMENTS, EXAM_SCORES, PREDICTIONS, LABELS,\n"
    "    NESTED_API_RESPONSE, CATEGORY_TREE, FEATURE_ROWS,\n"
    "    MODEL_RUNS, FEATURE_POINTS,\n"
    "    PRICE_INTERCEPT, PRICE_COEF_AREA,\n"
    ")\n"
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


def write(rel_path: str, notebook: dict):
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", path)


NOTEBOOKS = {
    "lessons/01_function_as_mapping/lesson.ipynb": nb(
        md("# Функция как отображение\n\n**Data/ML-контекст:** любая модель — функция `f(признаки) → предсказание`.\n\n**Цель:** понять `def` как именованное отображение вход → выход.\n\n**Сквозной датасет:** квартиры `APARTMENTS` (площадь → цена)."),
        md("## Результаты обучения\n\n1. Объяснить связь f(x), `def` и `model.predict`.\n2. Написать функцию-предсказатель с `return`.\n3. Применить функцию к нескольким объектам данных."),
        code(DATA_IMPORT),
        md("## 1. Проблема: дублирование предсказаний\n\nТри квартиры — один и тот же код прогноза цены."),
        code("def predict_price_v0(area_sqm):\n    return 1.5 + 0.09 * area_sqm\n\n\nfor apt in APARTMENTS:\n    p = 1.5 + 0.09 * apt['area_sqm']  # дублирование формулы\n    print(apt['area_sqm'], '→', p, 'млн')"),
        md("**Вопрос:** что общего у повторяющихся строк? Как назвать операцию «площадь → цена»?"),
        md("## 2. Модель как функция\n\nЛинейная модель (как в будущем sklearn, но **коэффициенты заданы**):\n\n`price = 1.5 + 0.09 × area`"),
        code("def predict_price(area_sqm):\n    \"\"\"Предсказать цену квартиры (млн руб.) по площади.\"\"\"\n    return PRICE_INTERCEPT + PRICE_COEF_AREA * area_sqm\n\n\nfor apt in APARTMENTS:\n    pred = predict_price(apt['area_sqm'])\n    print(f\"{apt['area_sqm']} м² → {pred:.2f} млн (факт: {apt['price_mln']})\")"),
        md("## 3. return vs print в ML-коде\n\n`return` — предсказание можно **использовать дальше** (метрика, pipeline).\n\n`print` — только вывод в консоль."),
        code("def predict_print(area):\n    print(PRICE_INTERCEPT + PRICE_COEF_AREA * area)\n\n\ndef predict_return(area):\n    return PRICE_INTERCEPT + PRICE_COEF_AREA * area\n\n\na = predict_print(45)\nprint('a =', a)  # None\n\nb = predict_return(45)\nprint('b =', b)  # число\n\nerrors = [abs(predict_return(x['area_sqm']) - x['price_mln']) for x in APARTMENTS]\nprint('MAE (упрощённо):', sum(errors) / len(errors))"),
        md("**Рефлексия:** зачем в ML-инференсе нужен именно `return`?"),
        md("## 4. Практика: функции для данных"),
        code("def predict_pass(score, threshold=60):\n    \"\"\"1 если сдал, 0 если нет — задел под классификацию.\"\"\"\n    pass\n\n\nassert predict_pass(72) == 1\nassert predict_pass(55) == 0\nprint('predict_pass OK')"),
        code("def batch_predict(areas, predict_fn):\n    \"\"\"Применить predict_fn к списку площадей.\"\"\"\n    pass\n\n\nareas = [a['area_sqm'] for a in APARTMENTS]\n# preds = batch_predict(areas, predict_price)\n# assert len(preds) == len(areas)\n"),
        md("## 5. Эксперимент\n\nИзмените `PRICE_COEF_AREA` на 0.12. Как меняется MAE по `APARTMENTS`? Какой коэффициент **интуитивно** ближе к фактам?"),
        code("# ваш эксперимент\n"),
        md("## 6. Самостоятельное задание\n\n`predict_room_price(area_sqm, rooms)` — добавьте надбавку `0.3` млн за каждую комнату сверх 1.\n\nПроверьте на 2–3 примерах."),
        code("# ваш код"),
        md("## Итог\n\n**Модель = функция.** sklearn позже даст `fit`, сейчас — ручное правило с `return`.\n\n**Дальше:** контракт функции, proto-EDA по спискам."),
    ),
    "lessons/02_parameters_and_return/lesson.ipynb": nb(
        md("# Параметры и return\n\n**Data/ML-контекст:** feature engineering и описательная статистика — набор функций с чётким контрактом.\n\n**Сквозной датасет:** `EXAM_SCORES`, `APARTMENTS`."),
        code(DATA_IMPORT),
        md("## 1. Proto-EDA: describe_numbers\n\nПеред pandas — функции над списком чисел."),
        code("def describe_numbers(values):\n    \"\"\"Вернуть (mean, min, max, count) — мини-описание выборки.\"\"\"\n    pass\n\n\nassert describe_numbers([10, 20, 30])[0] == 20\nprint('describe_numbers — допишите')"),
        md("## 2. Нормализация признака (задел под kNN)\n\nПриведение к [0, 1]: `(x - min) / (max - min)`."),
        code("def min_max_scale(values):\n    \"\"\"Min-max scaling списка чисел.\"\"\"\n    pass\n\n\nareas = [a['area_sqm'] for a in APARTMENTS]\n# scaled = min_max_scale(areas)\n# assert min(scaled) == 0 and max(scaled) == 1\n"),
        md("## 3. clip — ограничение выбросов"),
        code("def clip_outlier(x, low, high):\n    \"\"\"Ограничить значение (как winsorize на простом уровне).\"\"\"\n    return max(low, min(high, x))\n\n\nprint(clip_outlier(150, 0, 100))\nprint(clip_outlier(EXAM_SCORES[0], 0, 100))"),
        md("## 4. Mutable default — баг в сборе выбросов"),
        code("def collect_outliers_bad(x, bucket=[]):\n    if x > 100:\n        bucket.append(x)\n    return bucket\n\n\nprint(collect_outliers_bad(105))\nprint(collect_outliers_bad(110))  # ?"),
        code("def collect_outliers_ok(x, bucket=None):\n    if bucket is None:\n        bucket = []\n    if x > 100:\n        bucket.append(x)\n    return bucket\n"),
        md("## 5. grade_stats — порог класса «сдал»"),
        code("def grade_stats(scores, pass_threshold=60):\n    \"\"\"(mean, passed, failed).\"\"\"\n    pass\n\n\n# assert grade_stats(EXAM_SCORES)[1] + grade_stats(EXAM_SCORES)[2] == len(EXAM_SCORES)\n"),
        md("## 6. Эксперимент\n\nПри каком `pass_threshold` доля сдавших по `EXAM_SCORES` равна 50%?"),
        code("# эксперимент"),
        md("## 7. Самостоятельное задание\n\n`feature_row_stats(row)` для словаря `{'area_sqm': ..., 'rooms': ..., 'floor': ...}` → кортеж (mean, max) по **числовым** значениям.\n\nПроверьте на `FEATURE_ROWS[0]`.\n\n**Canvas (адаптация):** sort списка моделей по убыванию `(m1+m2+m3)/3` через `key=lambda`."),
        code("# ваш код\n\nmodels_3m = [\n    {'name': 'knn', 'm1': 0.8, 'm2': 0.75, 'm3': 0.82},\n    {'name': 'logreg', 'm1': 0.77, 'm2': 0.79, 'm3': 0.76},\n]\n# ranked = sorted(models_3m, key=lambda m: ..., reverse=True)\n"),
        md("## Итог\n\nEDA = функции с понятным входом/выходом. В pandas будет `.describe()`, логика та же."),
    ),
    "lessons/03_scope_and_debugging/lesson.ipynb": nb(
        md("# Область видимости и отладка\n\n**Data/ML-контекст:** отладка метрик и предсказаний — типичная инженерная задача.\n\n**Данные:** `PREDICTIONS`, `LABELS`."),
        code(DATA_IMPORT),
        md("## 1. accuracy — этalon\n\nAccuracy = доля верных предсказаний."),
        code("def accuracy(preds, labels):\n    \"\"\"Доля совпадений preds[i] == labels[i].\"\"\"\n    if len(preds) != len(labels):\n        return None\n    correct = sum(p == y for p, y in zip(preds, labels))\n    return correct / len(labels)\n\n\nprint('accuracy =', accuracy(PREDICTIONS, LABELS))"),
        md("## 2. Сломанная accuracy\n\nИсправьте и запишите в журнал отладки."),
        code("def accuracy_buggy(preds, labels):\n    correct = 0\n    for i in range(len(preds)):\n        if preds[i] == labels[i]:\n            correct += 1\n    # баг: нет return — что вернёт функция?\n\n\nprint(accuracy_buggy(PREDICTIONS, LABELS))"),
        code("def accuracy_fixed(preds, labels):\n    # ваша исправленная версия\n    pass\n\n\nassert abs(accuracy_fixed(PREDICTIONS, LABELS) - accuracy(PREDICTIONS, LABELS)) < 1e-9\n"),
        md("## 3. Global-метрика в цикле\n\nТипичный баг при подсчёте метрик по батчам."),
        code("total_correct = 0\n\n\ndef update_metrics(pred, label):\n    total_correct = total_correct + (pred == label)  # баг scope\n    return total_correct\n\n\n# исправьте: не используйте global без необходимости\n"),
        md("## 4. Забытый return в predict"),
        code("def predict_pass_buggy(score, threshold=60):\n    if score >= threshold:\n        1\n    else:\n        0\n\n\n# result = predict_pass_buggy(72)\n# print(result)  # None — почему?\n"),
        md("## 5. Журнал отладки\n\n| Функция | Симптом | Причина | Fix |\n|---|---|---|---|\n| | | | |"),
        md("## 6. Самостоятельное задание\n\n`confusion_counts(preds, labels)` → `(tp, fp, fn, tn)` для бинарных 0/1.\n\nПроверьте на `PREDICTIONS`, `LABELS`."),
        code("def confusion_counts(preds, labels):\n    pass\n"),
        md("## Итог\n\nМетрика — функция. Баг в метрике = неверные выводы об модели."),
    ),
    "lessons/04_recursion/lesson.ipynb": nb(
        md("# Рекурсия\n\n**Data/ML-контекст:** вложенные данные (API, JSON), деревья категорий, divide-and-conquer.\n\n**Данные:** `NESTED_API_RESPONSE`, `CATEGORY_TREE`."),
        code(DATA_IMPORT),
        md("## 1. flatten — развернуть вложенный ответ API"),
        code("def flatten(nested):\n    \"\"\"Список любой вложенности → плоский список.\"\"\"\n    pass\n\n\nassert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]\n"),
        md("## 2. extract_ids — только id из вложенных dict"),
        code("def extract_ids(nested):\n    \"\"\"Собрать все значения ключа 'id' рекурсивно.\"\"\"\n    pass\n\n\n# ids = extract_ids(NESTED_API_RESPONSE)\n# print(ids)\n"),
        md("## 3. walk_categories — обход дерева"),
        code("def walk_categories(node, depth=0):\n    \"\"\"Печать категорий с отступом (как decision tree).\"\"\"\n    pass\n\n\n# walk_categories(CATEGORY_TREE)\n"),
        md("## 4. count_char — базовая рекурсия на строке"),
        code("def count_char(s, ch):\n    pass\n\n\nassert count_char('banana', 'a') == 3\n"),
        md("## 5. Fibonacci — антипример\n\nНаивная рекурсия vs итерация для n=25. Вывод: pipeline — итерация; рекурсия — для **структур данных**."),
        code("def fib_recursive(n):\n    if n <= 1:\n        return n\n    return fib_recursive(n - 1) + fib_recursive(n - 2)\n\n\ndef fib_iterative(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n\n\n# import time\n# сравните время для n=25\n"),
        md("## 6. Эксперимент\n\nСравните глубину рекурсии для `flatten(NESTED_API_RESPONSE)` и для `[[[[1]]]]`."),
        code("# наблюдения"),
        md("## 7. Самостоятельное задание\n\n`count_leaves(node)` — число «листьев» в дереве категорий.\n\nЗадачи Canvas (binary_search, max_digit) — [canvas_practice.md](canvas_practice.md); в КТП 8 класса — модуль 7, вне scope этого урока."),
        code("def count_leaves(node):\n    pass\n"),
        md("## Итог\n\nРекурсия — естественный инструмент для **вложенных данных** и **деревьев**."),
    ),
    "lessons/05_lambda/lesson.ipynb": nb(
        md("# Лямбда-функции\n\n**Data/ML-контекст:** `.apply(lambda ...)`, масштабирование, фильтр аномалий, ранжирование моделей.\n\n**Данные:** `EXAM_SCORES`, `FEATURE_ROWS`, `MODEL_RUNS`, `FEATURE_POINTS`.\n\n**Практика Canvas:** [canvas_practice.md](canvas_practice.md)."),
        code(DATA_IMPORT),
        md("## 1. map — нормализация списка оценок"),
        code("raw = EXAM_SCORES\nmx = max(raw)\nscaled = list(map(lambda x: x / mx, raw))\nprint(scaled)"),
        md("## 2. filter — отбор «аномалий» (score < 50 или > 90)"),
        code("anomalies = list(filter(lambda s: s < 50 or s > 90, EXAM_SCORES))\nprint(anomalies)"),
        md("## 3. sorted — ранжирование моделей по метрике"),
        code("models = [\n    {'name': 'knn', 'f1': 0.81},\n    {'name': 'logreg', 'f1': 0.77},\n    {'name': 'baseline', 'f1': 0.65},\n]\n\nranked = sorted(models, key=lambda m: m['f1'], reverse=True)\nprint([m['name'] for m in ranked])"),
        md("## 4. Практика: min_max_scale через map"),
        code("def min_max_scale_list(values):\n    lo, hi = min(values), max(values)\n    return list(map(lambda x: (x - lo) / (hi - lo), values))\n\n\nprint(min_max_scale_list([r['area_sqm'] for r in FEATURE_ROWS]))"),
        md("## 5. Canvas: farthest point\n\n`FEATURE_POINTS` — пары `[area_sqm, floor]`. Точка с **максимальной** суммой квадратов координат."),
        code("# farthest = max(FEATURE_POINTS, key=lambda p: ...)\n# print(farthest)\n"),
        md("## 6. Canvas: leaderboard MODEL_RUNS\n\nSort по **убыванию f1**; при равенстве — по **возрастанию id**."),
        code("leaderboard = sorted(MODEL_RUNS, key=lambda r: (-r['f1'], r['id']))\nprint([r['id'] for r in leaderboard])\n# ожидаемый порядок id: 25, 30, 305, 101, 200\n"),
        md("## 7. Эксперимент\n\nПорог аномалии: как меняется список при `> 85` vs `> 90`?"),
        code("# эксперимент"),
        md("## 8. Самостоятельное задание\n\n1. Отсортировать `FEATURE_ROWS` по `area_sqm`, затем по `floor`.\n2. Sort id прогонов по **последней цифре** `int(f1*100)` (stable sort).\n\nСм. [canvas_practice.md](canvas_practice.md)."),
        code("# ваш код"),
        md("## Итог\n\nВ pandas: `df['col'].apply(lambda x: ...)`. Здесь — те же идеи на списках."),
    ),
    "lessons/06_higher_order/lesson.ipynb": nb(
        md("# Функции высшего порядка\n\n**Data/ML-контекст:** inference pipeline = цепочка transform → predict.\n\n**Аналог sklearn:** `Pipeline(steps=[('scale', ...), ('model', ...)])`."),
        code(DATA_IMPORT),
        md("## 1. apply_pipeline"),
        code("def apply_pipeline(data, steps):\n    result = data\n    for step in steps:\n        result = step(result)\n    return result\n"),
        md("## 2. ML-пipeline для одной квартиры\n\n`raw dict → извлечь area → scale → predict`"),
        code("def extract_area(row):\n    return row['area_sqm']\n\n\ndef scale_area(area, max_area=60):\n    return area / max_area\n\n\ndef predict_from_scaled(scaled_area):\n    return PRICE_INTERCEPT + PRICE_COEF_AREA * (scaled_area * 60)\n\n\napt_pipeline = [extract_area, scale_area, predict_from_scaled]\n\npred = apply_pipeline(FEATURE_ROWS[0], apt_pipeline)\nprint('predicted mln:', pred)"),
        md("## 3. Текстовый pipeline (задел под NLP)"),
        code("text_pipeline = [\n    lambda s: s.strip().lower(),\n    lambda s: s.split(),\n    lambda tokens: [t for t in tokens if len(t) >= 4],\n]\n\nprint(apply_pipeline('  Data science ML course  ', text_pipeline))"),
        md("## 4. Сравнение со sklearn (концепт)\n\n```python\n# Будущий модуль:\n# from sklearn.pipeline import Pipeline\n# pipe = Pipeline([('scale', StandardScaler()), ('model', LinearRegression())])\n# pipe.fit(X_train, y_train)\n# pipe.predict(X_test)\n```\n\nСейчас `steps` — список **функций**, позже — объекты с `.fit`/`.predict`."),
        md("## 5. Эксперимент\n\nПоменяйте порядок: `scale_area` до/после `extract_area`. Что ломается?"),
        code("# эксперимент"),
        md("## 6. compose"),
        code("def compose(f, g):\n    \"\"\"Вернуть lambda x: f(g(x)).\"\"\"\n    pass\n\n\nh = compose(lambda x: x + 1, lambda x: x * 2)\nassert h(3) == 7\n"),
        md("## 7. Подготовка к артефакту\n\nСпроектируйте pipeline: tokenize → filter → word_frequencies → compare_classes.\n\nСм. [artifact/PROJECT.md](../../artifact/PROJECT.md)."),
        code("# черновик pipeline для text_stats"),
        md("## Итог\n\n**Pipeline = композиция функций.** Следующий модуль — pandas + sklearn с тем же смыслом."),
    ),
}


if __name__ == "__main__":
    for rel, notebook in NOTEBOOKS.items():
        write(rel, notebook)
