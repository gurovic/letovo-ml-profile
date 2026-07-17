# Lesson Design: Практика — рекурсия, lambda, pipeline

## A. Сценарий пары

| Поле | Значение |
|---|---|
| Модуль | Функции и рекурсия в Python (`08_01`) |
| Название урока | Практика: рекурсия; lambda / HOF / apply_pipeline |
| Пара КТП | **8** |
| Длительность | 2 академических часа (**80 минут**) |
| Роль | отработка (серия задач; мост к артефакту) |
| Пререквизиты | [Пара 7](../07_recursion/LESSON.md): `flatten`, `walk_categories`; пары 2–6: функции, метрики |
| **Открыть** | [lesson.ipynb](lesson.ipynb) — блоки A → B → C |
| **Первая фраза** | «Сегодня только практика: дорешиваем рекурсию, короткие функции в `filter`/`sorted`, собираем цепочку шагов» |
| **Минимум сдачи** | A1–A2, B1–B2, C1 (см. §B) |
| **Домашнее задание** | [homework.ipynb](homework.ipynb) — A3, B3, C2 (~1 ч) |
| **Дальше** | артефакт — [пара 9](../09_artifact_build/LESSON.md) |
| **Canvas** | Модуль 54688: [план](https://canvas.letovo.ru/courses/6465/pages/para-8-plan-uroka-dlia-priepodavatielia) (скрыт); [урок Colab](https://colab.research.google.com/gist/gurovic/83ac6b1d22b4385e6ee4a424a243f7dd/lesson.ipynb); ДЗ Assignment **198700** (последнее ДЗ модуля; пары 9–10 без ДЗ) |

### A. Чего хотим от пары

**Основная тема:** серия на уже известных приёмах — рекурсия, короткий `lambda` в `filter`/`sorted`, вызов функций по порядку (`pipeline`). Новой теории нет.

**Побочно:** подготовка к сборке `text_stats` (отдельные шаги ещё не склеиваем в один файл).

---
### Калибровка (одарённое ядро)

| Блок | Заложено | Сильное ядро |
|---|---|---|
| Рекурсия A1–A2 | 25 | 12–15 |
| Lambda B1–B2 | 20 | 10–12 |
| Pipeline C1 | 25 | 15–18 |
| **Итого** | **80** | **~40–45** |

Новую тему не вводим: lambda — 5 мин синтаксис + задачи; `apply_pipeline` — уже есть заготовка в ноутбуке.

---

## B. Ход пары

| # | Этап | ~мин | Ученик | Учитель | Материал | Критерий |
|---|---|---|---|---|---|---|
| 1 | Рекурсия | 25 | `extract_ids`, `walk_categories` | Базовый случай | A1–A2 | id / печать дерева |
| 2 | Lambda | 20 | filter аномалий; leaderboard | `key=` в sorted | B1–B2 | порядок id: 25, 30, 305, 101, 200 |
| 3 | Pipeline | 25 | `apply_pipeline` на `FEATURE_ROWS[0]` | «scale до или после extract?» | C1 | число на выходе |
| 4 | Мост | 10 | Читает постановку `text_stats` | [PROJECT.md](../../artifact/PROJECT.md) | понятен старт пары 9 |

Обязательный минимум: **A1–A2, B1–B2, C1**. A3, B3, C2 — углубление.

---

## C. Если сбились

| Симптом | Что сказать |
|---|---|
| `sorted(models)` без `key=` | «По чему сортируется dict по умолчанию?» |
| Scale до extract из dict | Прогнать тип после каждого шага |
| Шаг без `return` | Печать типа после шага |
| binary_search из Canvas | «Это модуль 7, не эта пара» — [canvas_practice.md](canvas_practice.md) |

| | |
|---|---|
| Слабее | A1 с подсказкой «если dict — id»; B2 — готовый `key=` разобрать; C1 — шаги по одному |
| Сильнее | A3 `count_leaves`; B3 farthest point; C2 текстовый pipeline |

---

## D. Проектирование

### Зачем урок

После введения рекурсии нужна серия задач. Закрепляются `lambda` в `filter`/`sorted` и сборка шагов в `apply_pipeline` — мост к артефакту `text_stats`.

### Центральная идея

| Поле | Значение |
|---|---|
| Центральная идея | Серия известных приёмов; lambda — короткая функция в одну строку; pipeline — вызов функций по порядку |
| Данные | `NESTED_API_RESPONSE`, `CATEGORY_TREE`, `EXAM_SCORES`, `MODEL_RUNS`, `FEATURE_ROWS` — [data/module_datasets.py](../../data/module_datasets.py) |

### Результаты обучения

1. Дорешать рекурсию: `extract_ids`, `walk_categories`.
2. Применить `filter` / `sorted(..., key=)` с lambda.
3. Собрать leaderboard `MODEL_RUNS` (f1 ↓, id ↑).
4. Прогнать `FEATURE_ROWS[0]` через extract → scale → predict.

### Профессиональный контекст

`sorted(..., key=)` и pandas `.apply(lambda …)` — один приём. `Pipeline(steps=[...])` в sklearn — тот же смысл, что список функций.

### Материалы

- [x] [lesson.ipynb](lesson.ipynb) — блоки A/B/C
- [x] [solutions.ipynb](solutions.ipynb) — только преподаватель
- [x] [artifact/PROJECT.md](../../artifact/PROJECT.md)
- [ ] [canvas_practice.md](canvas_practice.md) — по остатку времени

### Домашнее задание

| Поле | Значение |
|---|---|
| Назначается | **да** |
| Файл | [homework.ipynb](homework.ipynb) |
| Содержание | A3 `count_leaves`, B3 farthest point, C2 текстовый pipeline |
| Время | ~1 ч |
| Почему не на паре | Минимум серии — на паре; углубление — дома |

---

## E. Карточка урока (§13)

| Поле | Значение |
|---|---|
| Часы | 2 |
| Стратегии обучения / виды деятельности | Серия рекурсии; filter/sorted с lambda; apply_pipeline; мост к text_stats |
| Формирующее оценивание | Вывод A1–A2, B2; прогон FEATURE_ROWS через pipeline |
| Дифференциация | Минимум A1–A2, B1–B2, C1; сильные — A3, B3, C2 |
| По продукту | Решённый минимум серии на паре |
| Canvas | Модуль 54688: план скрыт; урок Colab; ДЗ Assignment **198700** |
