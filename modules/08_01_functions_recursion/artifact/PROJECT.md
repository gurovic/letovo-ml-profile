# Артефакт модуля: библиотека `text_stats`

**Тип:** Python-модуль + README учащегося  
**Срок:** 1–2 недели после урока 6 (до 8 ч по UNIT.md)  
**ML-смысл:** bag-of-words, naive classification, inference pipeline

Данные: `TEXTS_POSITIVE`, `TEXTS_NEGATIVE` в [data/module_datasets.py](../data/module_datasets.py).

---

## Задача

Собрать модуль анализа текста **без pandas/sklearn**:

1. preprocessing и частоты (bag-of-words);
2. сравнение двух классов коротких отзывов;
3. naive-классификатор по «маркерным» словам.

Итог — работающий `text_stats.py`, README и прохождение `manual_tests.py`.

---

## Обязательные функции

| Функция | Контракт | Data/ML |
|---|---|---|
| `tokenize(text)` | `str` → список слов в lower | preprocessing |
| `word_frequencies(tokens)` | список → `{слово: частота}` | bag-of-words |
| `filter_tokens(tokens, min_len=3)` | оставить токены длиной ≥ `min_len` | отбор признаков |
| `top_n(freq, n=5)` | top-n пар `(слово, count)` по убыванию частоты | топ признаков |
| `count_char_recursive(s, ch)` | рекурсивный подсчёт `ch` в `s` | рекурсия |
| `analyze_text(text)` | `{"word_count", "unique_words", "top3"}` | mini-EDA документа |
| `apply_pipeline(data, steps)` | последовательно применить функции из `steps` | pipeline |
| `aggregate_frequencies(texts)` | суммарные частоты по списку текстов класса | агрегат класса |
| `compare_class_frequencies(texts_a, texts_b, ratio=2.0)` | `{слово: "positive"\|"negative"}` при перевесе ≥ `ratio` | маркеры классов |
| `naive_classify(text, texts_a, texts_b)` | `"positive"` / `"negative"` / `"unknown"` | predict |

Вспомогательная `count_words(tokens)` — по желанию; в эталоне используется в `analyze_text`.

---

## Пример использования

```python
from text_stats import apply_pipeline, tokenize, filter_tokens, word_frequencies, naive_classify
from data.module_datasets import TEXTS_POSITIVE, TEXTS_NEGATIVE

pipeline = [tokenize, lambda t: filter_tokens(t, 3), word_frequencies]
freq_one = apply_pipeline("отличный фильм", pipeline)

naive_classify("отличный фильм рекомендую", TEXTS_POSITIVE, TEXTS_NEGATIVE)
# → "positive"
```

---

## Критерии приёмки

| # | Критерий |
|---|---|
| 1 | `manual_tests.py` в `starter/` — все 10 тестов без ошибок |
| 2 | `compare_class_frequencies` на demo-данных — ≥2 маркера (в т.ч. `отличный`, `скучный`) |
| 3 | `naive_classify` — ≥4/5 верных на **своих** тестовых фразах (перечислить в README) |
| 4 | `analyze_text("one two two")` → `word_count==3`, `unique_words==2`, `top3[0]==("two", 2)` |
| 5 | `count_char_recursive("banana", "a") == 3` |
| 6 | README: порядок pipeline, tie-break в `naive_classify`, 1 абзац про связь с будущим NLP |

---

## Решения учащегося (зафиксировать в README)

1. Агрегация частот по списку текстов (`aggregate_frequencies`).
2. Порог маркера (`ratio`, по умолчанию 2.0).
3. Tie-break при равных score в `naive_classify` (эталон: `"unknown"`).
4. Обработка пунктуации в `tokenize` (эталон: `\w+` после lower).

---

## Связь с уроками

| Урок | В артефакте |
|---|---|
| 1–2 | `def`, `return`, docstring |
| 3 | отладка `naive_classify` |
| 4 | `count_char_recursive` |
| 5 | `lambda` в pipeline |
| 6 | `apply_pipeline` |

---

## Файлы

| Путь | Назначение |
|---|---|
| [starter/](starter/) | заготовки + тесты для учащегося |
| [solution/](solution/) | эталон и ответы для учителя |

Эталон: `cd artifact/solution && python manual_tests.py` → 10 passed.
