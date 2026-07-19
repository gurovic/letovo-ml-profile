# Lesson Design: Рекурсия, lambda, pipeline

## A. Сценарий пары

| Поле | Значение |
|---|---|
| Модуль | Функции и рекурсия в Python (`08_01`) |
| Название урока | Рекурсия на данных; lambda / HOF / apply_pipeline |
| Пара КТП | **7** |
| Длительность | 2 академических часа (**80 минут**) |
| Роль | введение + отработка (рекурсия; серия lambda/pipeline) |
| Пререквизиты | Пары 2–6: функции, `return`, отладка, метрики |
| **Открыть** | [lesson.ipynb](lesson.ipynb) — сначала `NESTED_LIST` / `CATEGORY_TREE`, затем блоки A→B→C |
| **Первая фраза** | «Сначала разворачиваем вложенные данные рекурсией; потом — короткие функции и цепочка шагов» |
| **Минимум сдачи** | (1) `flatten` + assert; (2) `walk_categories` с отступом; (3) A1 `extract_ids`; (4) B1–B2 lambda; (5) C1 `apply_pipeline` на `FEATURE_ROWS[0]` |
| **Домашнее задание** | [homework.ipynb](homework.ipynb) — A3, B3, C2 + Fibonacci-рефлексия (~1 ч) |
| **Дальше** | артефакт — [пара 8](../08_artifact/LESSON.md) |
| **Canvas** | Модуль 54688: планы старых пар 7–8 (gist recursion / pipeline); ДЗ Assignment **198700** (последнее ДЗ модуля; пара 8 без ДЗ). **Canvas republish:** объединить страницы para-7 и para-8 под пару КТП 7 |

### A. Чего хотим от пары

Главное — рекурсия с базовым случаем на вложенном списке и дереве категорий, затем на той же паре закрепить `lambda` в `filter`/`sorted` и сборку шагов в `apply_pipeline`. Новых больших тем сверх этого не открываем. HOF = «функция высшего порядка» — [UNIT §18](../../UNIT.md#18-глоссарий-модуля).

Побочно мост к артефакту `text_stats`: те же приёмы соберутся в один модуль на паре 8.

---
### Калибровка (одарённое ядро)

| Блок | Заложено | Сильное ядро |
|---|---|---|
| Trace + flatten + walk | 30 | 18–20 |
| Рекурсия A1 | 10 | 5–7 |
| Lambda B1–B2 | 15 | 8–10 |
| Pipeline C1 | 20 | 12–15 |
| Мост | 5 | 3 |
| **Итого** | **80** | **~45–55** |

Fibonacci — антипример в ДЗ (markdown), не на паре. Углубление A3/B3/C2 — дома.

---

## B. Ход пары

| # | Этап | ~мин | Ученик | Учитель | Материал | Критерий |
|---|---|---|---|---|---|---|
| 1 | Trace + flatten | 20 | Пишет `flatten`, assert | Стек вызовов на доске | `## 1. flatten` | `[1,2,3,4,5]` |
| 2 | Дерево | 10 | `walk_categories` с отступом | Желаемый вывод | `## 2. walk_categories` | печать с глубиной |
| 3 | A1 extract_ids | 10 | Рекурсия по API-ответу | Базовый случай dict/list | A1 | `[1,2,3]` |
| 4 | Lambda | 15 | filter аномалий; leaderboard | `key=` в sorted | B1–B2 | id: 25, 30, 305, 101, 200 |
| 5 | Pipeline | 20 | `apply_pipeline` на `FEATURE_ROWS[0]` | «scale до или после extract?» | C1 | число на выходе |
| 6 | Мост + ДЗ | 5 | Открывает PROJECT / `homework.ipynb` | [PROJECT.md](../../artifact/PROJECT.md) | знает старт пары 8 |

Обязательный минимум: **flatten, walk, A1, B1–B2, C1**. A3, B3, C2 — углубление (ДЗ).

---

## C. Если сбились

| Симптом | Что сказать |
|---|---|
| `RecursionError` | «Где базовый случай? Что если элемент не список?» |
| Пишет цикл без вызова себя | «Где функция вызывает саму себя?» |
| `sorted(models)` без `key=` | «По какому полю? Нужен `key=lambda r: …`» |
| Scale до extract | Сначала `extract_area(row)` → число, потом scale |
| «Разве dict не вне scope?» | Доступ `row['area_sqm']` — пререквизит (UNIT §4); теорию hash map не открываем |
| binary_search из Canvas | «Это модуль 7 КТП, не эта пара» — [canvas_practice_recursion.md](canvas_practice_recursion.md) |

| | |
|---|---|
| Слабее | flatten по шагам; B2 — разобрать готовый `key=`; C1 — шаги по одному |
| Сильнее | A3 `count_leaves`; B3 farthest; C2 текстовый pipeline |

---

## D. Проектирование

### Зачем урок

Вложенные структуры требуют рекурсии; сразу после введения нужна серия на `lambda` и `apply_pipeline` — мост к артефакту. Сжатие двух бывших пар (7+8) в одну: guided coding + минимум серии на той же паре.

### Центральная идея

| Поле | Значение |
|---|---|
| Центральная идея | Рекурсия с базовым случаем + lambda/pipeline как композиция функций над данными |
| Данные | `NESTED_LIST`, `CATEGORY_TREE`, `NESTED_API_RESPONSE`, `MODEL_RUNS`, `FEATURE_ROWS` — [data/module_datasets.py](../../data/module_datasets.py) |

### Результаты обучения

1. Назвать базовый случай и шаг рекурсии для `flatten`.
2. Реализовать `flatten` и `walk_categories`.
3. Применить `filter` / `sorted(..., key=)` с lambda; собрать leaderboard.
4. Прогнать `FEATURE_ROWS[0]` через extract → scale → predict.

### Материалы

- [x] [lesson.ipynb](lesson.ipynb)
- [x] [homework.ipynb](homework.ipynb)
- [x] [solutions.ipynb](solutions.ipynb) — только преподаватель
- [ ] [canvas_practice_recursion.md](canvas_practice_recursion.md) / [canvas_practice_pipeline.md](canvas_practice_pipeline.md) — по остатку времени

### Домашнее задание

| Поле | Значение |
|---|---|
| Назначается | **да** |
| Файл | [homework.ipynb](homework.ipynb) |
| Содержание | A3 `count_leaves`; B3 farthest; C2 текстовый pipeline; markdown — рекурсия vs цикл (Fibonacci) |
| Время | ~1 ч |
| Почему не на паре | Минимум серии — на паре; углубление и антипример Fibonacci — дома |

---

## E. Карточка урока (§13)

| Поле | Значение |
|---|---|
| Часы | 2 |
| Стратегии обучения / виды деятельности | Trace + guided coding flatten/walk; extract_ids; filter/sorted с lambda; apply_pipeline; мост к text_stats |
| Формирующее оценивание | Устно: базовый случай flatten; assert A1, B1–B2, C1 |
| Дифференциация | База — flatten, walk, A1, B1–B2, C1; сильные — A3, B3, C2 |
| По содержанию | Только минимум vs углубление A3/B3/C2 |
| По процессу | Общий trace; затем индивидуальная серия A→B→C |
| По продукту | Рабочий минимум на паре; сдача `homework.ipynb` |
| Canvas | Модуль 54688: gist recursion + pipeline; ДЗ Assignment **198700**; нужна republish под пару 7 |
