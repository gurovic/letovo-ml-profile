# Сопоставление с Canvas IT-8

**Источник:** курс [IT: Профиль 8](https://canvas.letovo.ru/courses/5782), модуль «Модуль ФУНКЦИИ и РЕКУРСИИ» (module_id `47970`).

**Наш модуль:** `modules/08_functions_recursion/` — профиль ML, не общий IT.

---

## Структура Canvas (10+ занятий)

| Canvas | Содержание | Наш модуль |
|---|---|---|
| З1 | Функции, pre-assessment | Урок 1 + 2 (контракт, *args) |
| З2 | Lambda, контест, quiz | Урок 5 + `canvas_practice.md` |
| З3 | Рекурсия, контест | Урок 4 |
| З4 | Рекурсивные сортировки, mergesort | **Вне scope** (алгоритмы IT) |
| З5 | Комбинаторный перебор | **Вне scope** |
| З6 | itertools | **Вне scope** |
| З7 | Декораторы | **Вне scope** (9 класс) |
| З8 | Решение задач, quiz | Частично: отладка (урок 3) |
| З9 | Фракталы, DRAWZERO | **Вне scope** |
| З10 | Итоговая, критерии A/B | Артефакт `text_stats` |

---

## Что перенесено (ML-адаптация)

| Canvas | Адаптация | Где |
|---|---|---|
| Функции: return, *args | batch_predict, mean_any | урок 1–2 |
| Lambda: sorted(key=), min(key=) | leaderboard, farthest point | урок 5 |
| Lambda: олимпиада по баллам | sort MODEL_RUNS по f1 | урок 5 |
| Lambda: средний балл | sort по mean метрик | урок 2 ДЗ |
| Рекурсия: max digit | max_digit_recursive | урок 4 |
| Рекурсия: Fibonacci | антипример сложности | урок 4 |
| map/filter | нормализация, аномалии | урок 5 |

---

## Не переносим

Hanoi, reverse без списка, скобки, mergesort, itertools, декораторы, фракталы, ejudge как обязательная сдача.

---

## Обновлено

2026-07 — обогащение demo-модуля по Canvas IT-8.
