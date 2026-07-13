# Unit Planner: Функции и рекурсия в Python

**Класс:** 8  
**Статус:** демоверсия (data/ML-интеграция)  
**Длительность:** 6 уроков × 2 академических часа ≈ 2,5 недели при 5 ч/нед (план расширения: до 10 уроков)

**Сквозная линия модуля:** описание данных → преобразование → предсказание (на списках, без pandas/sklearn).

---

## 1. Идентификация

| Поле | Значение |
|---|---|
| Название | Функции и рекурсия в Python |
| Класс | 8 |
| Длительность (оценка) | 12 академических часов |
| Место в траектории 8–11 | Первый модуль программирования 8 класса; **мост к EDA и табличному ML** через абстракцию «функция = transform / predict» |

---

## 2. Зачем существует модуль

**Проблема:** учащийся видит `model.fit()` и `.predict()` как магию. Без функций нет связи f(x) → код → pipeline.

**Если убрать модуль:** pandas/sklearn становятся копированием рецептов; метрики и preprocessing не отлаживаются.

---

## 3. Профессиональная мотивация

| Контекст | Где встречается в модуле |
|---|---|
| Регрессия | `predict_price(area)` — линейная модель вручную |
| Классификация | `predict_pass`, `accuracy`, confusion counts |
| EDA | `describe_numbers`, `grade_stats`, частоты слов |
| Preprocessing | `min_max_scale`, `clip`, pipeline шагов |
| NLP (задел) | `text_stats`, bag-of-words, сравнение классов |
| Структуры данных | `flatten`, дерево категорий, binary search |

---

## 4. Пререквизиты

| Тип | Что требуется |
|---|---|
| Математика | f(x), таблица значений; интуиция линейной зависимости |
| Программирование | Python 7 класса: циклы, списки, словари |
| Data/ML | Идея «модель как f(x)» из 7 класса (reference) |
| Предыдущие модули | Основы Python (7 класс) |

---

## 5. Результаты обучения

После модуля учащийся может:

1. **Объяснить** модель ML как функцию «признаки → предсказание» и реализовать простой `predict_*` с `return`.
2. **Вычислить** proto-EDA: mean, min, max, долю класса по порогу.
3. **Масштабировать** список признаков min-max (задел под kNN).
4. **Отладить** функцию метрики (`accuracy`) и предсказания.
5. **Реализовать** рекурсию на вложенных данных и дереве категорий.
6. **Применить** `map`/`filter`/`sorted(key=)` к данным и метрикам моделей.
7. **Собрать** inference pipeline из функций (аналог sklearn Pipeline).
8. **Создать** модуль `text_stats` со сравнением частот двух классов текстов.

---

## 6. Ключевые идеи

| # | Идея | Data/ML |
|---|---|---|
| 1 | Функция = отображение | predict, transform |
| 2 | Контракт (params, return) | сигнатура preprocessing |
| 3 | Scope | баги в метриках |
| 4 | Рекурсия | nested JSON, деревья |
| 5 | HOF + pipeline | sklearn Pipeline |

---

## 7. Инженерные практики

- [x] отладка (метрики, predict)
- [x] документирование
- [x] экспериментирование (коэффициент модели, порог)
- [x] воспроизводимость (общий `data/module_datasets.py`)
- [x] декомпозиция: EDA / transform / predict

---

## 8. Математические идеи

| Идея | В модуле |
|---|---|
| f(x) = kx + b | `predict_price` |
| Доля верных | accuracy |
| Min-max scaling | нормализация признаков |
| Композиция | pipeline |

---

## 9. Последовательность уроков

| # | Урок | Data/ML-фокус | Артефакт |
|---|---|---|---|
| 1 | Функция как отображение | `predict_price`, MAE, batch predict | функции-предикторы |
| 2 | Параметры и return | describe, min_max_scale, grade_stats | proto-EDA |
| 3 | Scope и отладка | accuracy, confusion, баги метрик | журнал отладки |
| 4 | Рекурсия | flatten API, дерево категорий, binary search | рекурсия на данных |
| 5 | Lambda | map/filter, аномалии, ранжирование моделей | lambda на данных |
| 6 | HOF | ML inference pipeline, sklearn-аналог | pipeline |
| — | Артефакт | naive text classification по частотам | `text_stats` |

---

## 10. Итоговый артефакт

| Поле | Значение |
|---|---|
| Тип | Python-модуль + README |
| Описание | `text_stats`: частоты, pipeline, **compare_class_frequencies** для positive/negative текстов |
| ML-смысл | bag-of-words, задел под NLP |

[artifact/PROJECT.md](artifact/PROJECT.md)

---

## 11. Типовые трудности

| Тип | Трудность | Адресация |
|---|---|---|
| ML | «fit и predict — не функции» | урок 1: predict вручную |
| ML | Путают metric и predict | урок 3: accuracy отдельной функцией |
| Data | Scaling до/после extract | урок 6: порядок в pipeline |

---

## 12. Вне scope

- pandas, CSV, matplotlib (следующие модули)
- sklearn fit (только концепт Pipeline)
- train/test split, cross-validation
- TF-IDF, embeddings

---

## 13. Чек-лист модуля

- [x] сквозной data-контекст
- [x] три линии: describe / transform / predict
- [x] артефакт с классификацией текстов

Общие данные: [data/module_datasets.py](data/module_datasets.py)

---

## 14. Согласование с Canvas IT-8

Модуль Canvas «ФУНКЦИИ и РЕКУРСИИ» (47970) — 10+ занятий общего IT. Наш модуль — **6 уроков с ML-фокусом**.

| Canvas | Наш модуль |
|---|---|
| Функции, pre-assessment | Уроки 1–2 |
| Lambda-контест | Урок 5 + `lessons/05_lambda/canvas_practice.md` |
| Рекурсия-контест | Урок 4 + `lessons/04_recursion/canvas_practice.md` |
| mergesort, itertools, декораторы, фракталы | Вне scope |

Подробная таблица: [reference/CANVAS_MAPPING.md](reference/CANVAS_MAPPING.md)

Годовой КТП (модуль 1 = пары 1–14): [docs/ktp/08.md](../../docs/ktp/08.md)
