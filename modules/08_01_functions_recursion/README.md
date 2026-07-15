# Демо-модуль: Функции и рекурсия в Python

**Класс:** 8 | **Статус:** демоверсия с data/ML-контекстом  
**Объём:** 11 пар КТП (22 ч): вводная + введение/отработка + рекурсия + практика + артефакт

## Для преподавателя (с чего начать)

1. **План модуля:** [UNIT.md](UNIT.md) — цель, глоссарий (§18), таблица пар (§11).
2. **План каждой пары:** `lessons/<NN>_*/LESSON.md` — зоны **A–C** (сценарий / ход / если сбились). Один файл = одна пара (2 ч). Эталон формата: [пара 2 — введение](lessons/02_function_as_mapping/LESSON.md), [пара 3 — отработка](lessons/03_practice_predict/LESSON.md).
3. **Код на уроке:** `lessons/<NN>_*/lesson.ipynb` (Jupyter); пары 1, 10–11 — без ноутбука урока.
4. **Итоговая работа:** пары 10–11 — [artifact/PROJECT.md](artifact/PROJECT.md), стартовый код в [artifact/starter/](artifact/starter/).

| Пара КТП | Что вести | План урока | Ноутбук / материал |
|---|---|---|---|
| 1 | Вводная: профиль, правила | [01](lessons/01_intro_profile/LESSON.md) | — |
| 2 | Функция как отображение | [02](lessons/02_function_as_mapping/LESSON.md) | [lesson.ipynb](lessons/02_function_as_mapping/lesson.ipynb) |
| 3 | Практика: predict | [03](lessons/03_practice_predict/LESSON.md) | [lesson.ipynb](lessons/03_practice_predict/lesson.ipynb) |
| 4 | Параметры и return | [04](lessons/04_parameters_and_return/LESSON.md) | [lesson.ipynb](lessons/04_parameters_and_return/lesson.ipynb) |
| 5 | Практика: transform | [05](lessons/05_practice_transform/LESSON.md) | [lesson.ipynb](lessons/05_practice_transform/lesson.ipynb) |
| 6 | Scope и отладка | [06](lessons/06_scope_and_debugging/LESSON.md) | [lesson.ipynb](lessons/06_scope_and_debugging/lesson.ipynb) |
| 7 | Практика: метрики | [07](lessons/07_practice_metrics/LESSON.md) | [lesson.ipynb](lessons/07_practice_metrics/lesson.ipynb); [homework_counter.py](lessons/07_practice_metrics/homework_counter.py) |
| 8 | Рекурсия | [08](lessons/08_recursion/LESSON.md) | [lesson.ipynb](lessons/08_recursion/lesson.ipynb) |
| 9 | Практика: рекурсия, lambda, pipeline | [09](lessons/09_practice_pipeline/LESSON.md) | [lesson.ipynb](lessons/09_practice_pipeline/lesson.ipynb) |
| 10 | Артефакт: реализация | [10](lessons/10_artifact_build/LESSON.md) | [artifact/starter/](artifact/starter/) |
| 11 | Артефакт: сдача | [11](lessons/11_artifact_submit/LESSON.md) | [artifact/starter/](artifact/starter/) |

**Сленг модуля** (proto-EDA, pipeline, HOF и т.д.) — расшифровки в [UNIT.md §18](UNIT.md#18-глоссарий-модуля).

## Сквозная линия (для класса)

Три шага работы с данными на каждом уроке:

1. **Описать** числа в списке (среднее, min, max).
2. **Преобразовать** (масштаб, обрезка выброса).
3. **Предсказать** (цена, класс «сдал/не сдал»).

Один набор примеров: [data/module_datasets.py](data/module_datasets.py).

## Документы

- [UNIT.md](UNIT.md) — план модуля
- [lessons/](lessons/) — планы пар (LESSON.md), по одному на пару КТП
- [artifact/PROJECT.md](artifact/PROJECT.md) — итоговая работа

## Запуск (техническое)

```bash
cd modules/08_01_functions_recursion
python generate_notebooks.py   # пересобрать lesson.ipynb пар 2–9
jupyter notebook
```

**Вне scope модуля:** pandas, sklearn `fit`, train/test split.
