# Lesson Design: Лямбда-функции

## Data/ML-фокус

map/filter/sorted на данных: нормализация, аномалии, ранжирование моделей по F1.

**Данные:** `EXAM_SCORES`, `FEATURE_ROWS`

---

## 4. Результаты обучения

1. **Нормализовать** scores через map+lambda.
2. **Отфильтровать** аномалии (порог).
3. **Отсортировать** модели и `FEATURE_ROWS` по key.
4. **Leaderboard** `MODEL_RUNS` по f1 ↓, id ↑ (Canvas-адаптация).
5. **Найти** farthest point в `FEATURE_POINTS` через `max(..., key=)`.

**Данные:** `EXAM_SCORES`, `FEATURE_ROWS`, `MODEL_RUNS`, `FEATURE_POINTS`

**Практика Canvas:** [canvas_practice.md](canvas_practice.md)

---

## 5. Профессиональный контекст

pandas: `.apply(lambda row: ...)`. Здесь — на списках.

---

## 11. Домашнее задание

Два `sorted` для `FEATURE_ROWS`: по area, по floor.

---

## 12. Чек-лист

- [x] выполнено
