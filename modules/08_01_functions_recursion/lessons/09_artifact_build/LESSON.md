# Lesson Design: Артефакт text_stats — проектирование и реализация

## A. Сценарий пары

| Поле | Значение |
|---|---|
| Модуль | Функции и рекурсия в Python (`08_01`) |
| Название урока | Итоговая работа text_stats — проектирование, реализация, manual_tests |
| Пара КТП | **9** |
| Длительность | 2 академических часа (**80 минут**) |
| Роль | интеграция (артефакт модуля) |
| Пререквизиты | Пары 2–8: функции, transform, метрики, рекурсия, pipeline |
| **Открыть** | [PROJECT.md](../../artifact/PROJECT.md); выдать [starter/](../../artifact/starter/) |
| **Первая фраза** | «Вы собираете библиотеку из функций, которые мы тренировали 8 пар — тесты скажут, что готово» |
| **Минимум сдачи** | ≥6 из 10 тестов `manual_tests.py` к концу пары (шаги 1–5) |
| **Домашнее задание** | по необходимости — добить шаги 1–5 к паре 10 |
| **Дальше** | сдача — [пара 10](../10_artifact_submit/LESSON.md) |
| **Canvas** | Модуль 54688: план (скрыт); ученикам: [материалы](https://canvas.letovo.ru/courses/6465/pages/para-9-artifact-materialy), [задание](https://canvas.letovo.ru/courses/6465/pages/artifact-project), [шаги](https://canvas.letovo.ru/courses/6465/pages/artifact-starter-readme), [zip](https://canvas.letovo.ru/courses/6465/files/2913388/download?download_frd=1) |

### A. Чего хотим от пары

Интеграция модуля: навыки tokenize, частоты, pipeline, рекурсия — в один сдаваемый `text_stats.py` с автотестами. На паре разобрать PROJECT + starter, реализовать шаги 1–5; compare/classify и README — на паре 10.

Успех пары: к концу ≥6 из 10 тестов `manual_tests.py` зелёные (шаги 1–5). Эталон solution ученикам не раздавать.

---

## B. Ход пары

| # | Этап | ~мин | Ученик | Учитель | Материал | Критерий |
|---|---|---|---|---|---|---|
| 1 | Разбор | 15 | Читает PROJECT, starter/README | Критерии приёмки | [PROJECT.md](../../artifact/PROJECT.md) | называет 2–3 обязательные функции |
| 2 | Шаги 1–3 | 25 | `tokenize`, `count_char_recursive`, частоты | Таблица «если тест упал» | `text_stats.py` | OK: test_tokenize … test_top_n |
| 3 | Шаги 4–5 | 30 | `apply_pipeline`, `analyze_text` | Ход по ряду | шаги 4–5 README | OK: test_apply_pipeline, test_analyze_text |
| 4 | Тесты | 10 | `python manual_tests.py` | Типовые падения | terminal | ≥6/10 зелёных |

Работа **в папке** `artifact/starter/`. Отдельного `lesson.ipynb` нет.

---

## C. Если сбились

| Симптом | Что сказать |
|---|---|
| `ModuleNotFoundError: data` | Запускать из `artifact/starter/` |
| `NotImplementedError` | Нормально в начале — идти по шагам README |
| Путает порядок tokenize → filter → frequencies | Напомнить цепочку пары 8 |

| | |
|---|---|
| Слабее | Только шаги 1–4; `analyze_text` с подсказкой |
| Сильнее | Полные шаги 1–5 + начать шаг 6 дома |

---

## D. Проектирование

### Зачем урок

Интеграция модуля: навыки tokenize, частоты, pipeline, рекурсия — в один сдаваемый `text_stats.py` с автотестами.

### Центральная идея

| Поле | Значение |
|---|---|
| Центральная идея | Артефакт = функции с контрактами + `manual_tests.py` |
| Данные | `TEXTS_POSITIVE`, `TEXTS_NEGATIVE` — [data/module_datasets.py](../../data/module_datasets.py) |

### Результаты обучения

1. Реализовать шаги 1–5 из [starter/README.md](../../artifact/starter/README.md).
2. Прогонять `manual_tests.py` после каждой группы функций.
3. Объяснить, зачем `tokenize` перед частотами.

### Материалы

- [x] [artifact/PROJECT.md](../../artifact/PROJECT.md)
- [x] [artifact/starter/](../../artifact/starter/) — `text_stats.py`, `manual_tests.py`, README
- [ ] ноутбук урока — не нужен

### Домашнее задание

| Поле | Значение |
|---|---|
| Назначается | **по необходимости** |
| Содержание | Добить шаги 1–5 / незакрытые тесты к паре 10 |

---

## E. Карточка урока (§13)

| Поле | Значение |
|---|---|
| Часы | 2 |
| Стратегии обучения / виды деятельности | Разбор PROJECT; реализация text_stats (шаги 1–5); прогон manual_tests |
| Формирующее оценивание | Устно: зачем tokenize перед частотами; зелёные OK: test_* |
| Дифференциация | База — шаги 1–4; углубление — analyze_text + шаг 6 дома |
| По продукту | ≥6/10 тестов; рабочие tokenize … analyze_text |
| Canvas | Модуль 54688: план скрыт; материалы + задание + шаги + стартовый код (wiki курса) |
