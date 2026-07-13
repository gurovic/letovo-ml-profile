# Слайды: Область видимости и отладка

---

## Слайд 1 — ML-контекст

Модель обучили. Как понять, хороша ли она?

**accuracy** = доля верных предсказаний.

---

## Слайд 2 — Данные

`PREDICTIONS` vs `LABELS` — 10 объектов, бинарная классификация.

---

## Слайд 3 — accuracy как функция

```python
def accuracy(preds, labels):
    correct = sum(p == y for p, y in zip(preds, labels))
    return correct / len(labels)
```

---

## Слайд 4 — Типовые баги

| Симптом | Причина |
|---|---|
| None | нет return |
| Завышенная accuracy | global counter |
| UnboundLocalError | scope |

---

## Слайд 5 — Алгоритм отладки

Воспроизвести → traceback → fix → граничный случай (пустой список labels)

---

## Слайд 6 — Переход

Исправить сломанные функции + `confusion_counts`.

---

## Слайд 7 — Итог

Не доверяй метрике, которую не можешь отладить.
