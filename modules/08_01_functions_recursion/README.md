# Демо-модуль: Функции и рекурсия в Python

**Класс:** 8 | **Статус:** демоверсия с **агрессивной data/ML-интеграцией**

## Сквозная линия

```
describe (EDA)  →  transform (scale, filter)  →  predict (regression, classify)
```

Один набор данных на все уроки: [data/module_datasets.py](data/module_datasets.py)

| Датасет | ML-смысл |
|---|---|
| APARTMENTS | регрессия, predict_price |
| EXAM_SCORES | порог класса, аномалии |
| PREDICTIONS / LABELS | accuracy, confusion |
| NESTED_API_RESPONSE | flatten nested data |
| TEXTS_POSITIVE / NEGATIVE | bag-of-words, naive classify |
| MODEL_RUNS / FEATURE_POINTS | Canvas lambda-контест (leaderboard, farthest point) |

## Согласование с Canvas IT-8

Модуль Canvas «ФУНКЦИИ и РЕКУРСИИ» (47970) — источник задач, адаптированных под ML. Таблица: [reference/CANVAS_MAPPING.md](reference/CANVAS_MAPPING.md).

## Документы

- [UNIT.md](UNIT.md) — план модуля
- [lessons/](lessons/) — 6 уроков
- [artifact/PROJECT.md](artifact/PROJECT.md) — итоговый артефакт

## Уроки

| # | Тема | Data/ML |
|---|---|---|
| 1 | Функция как отображение | predict_price, MAE |
| 2 | Параметры и return | describe, min_max_scale |
| 3 | Scope и отладка | accuracy, confusion |
| 4 | Рекурсия | flatten API, дерево |
| 5 | Lambda | map/filter на данных |
| 6 | HOF | inference pipeline ≈ sklearn |

## Запуск

```bash
cd modules/08_01_functions_recursion
python generate_notebooks.py   # пересобрать .ipynb
jupyter notebook
```

**Вне scope:** pandas, sklearn fit, train/test.
