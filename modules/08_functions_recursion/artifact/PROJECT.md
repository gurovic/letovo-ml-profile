# Артефакт модуля: библиотека `text_stats`

**Тип:** Python-модуль + README  
**ML-смысл:** bag-of-words, naive classification по частотам, inference pipeline  
**Срок:** 1–2 недели после урока 6

---

## Задача

Модуль для анализа текста **без pandas/sklearn**. Итог — **сравнение двух классов** коротких отзывов (positive / negative) по частотам слов — задел под NLP-классификацию.

Данные для проверки: `TEXTS_POSITIVE`, `TEXTS_NEGATIVE` в [data/module_datasets.py](../data/module_datasets.py).

---

## Обязательные функции

| Функция | Data/ML |
|---|---|
| `tokenize(text)` | preprocessing |
| `word_frequencies(tokens)` | bag-of-words |
| `filter_tokens(tokens, min_len=3)` | feature selection |
| `top_n(freq, n=5)` | top features |
| `count_char_recursive(s, ch)` | рекурсия |
| `analyze_text(text)` | mini-EDA одного документа |
| `apply_pipeline(data, steps)` | pipeline |
| **`compare_class_frequencies(texts_a, texts_b)`** | **сравнить частоты двух классов; вернуть слова, где freq_a / freq_b > 2 или наоборот** |
| **`naive_classify(text, ref_a, ref_b)`** | **по сумме частот «характерных» слов решить, ближе к классу A или B** |

---

## Пример

```python
from text_stats import apply_pipeline, tokenize, filter_tokens, word_frequencies
from data.module_datasets import TEXTS_POSITIVE, TEXTS_NEGATIVE

pipeline = [tokenize, lambda t: filter_tokens(t, 3), word_frequencies]

# частоты по классам
# compare_class_frequencies(...) → {"отличный": "positive", ...}

# naive_classify("отличный фильм", TEXTS_POSITIVE, TEXTS_NEGATIVE) → "positive"
```

---

## Критерии приёмки

- [ ] `compare_class_frequencies` находит ≥2 «маркерных» слова на demo-данных
- [ ] `naive_classify` верно классифицирует 4/5 тестовых фраз (задать самому в README)
- [ ] `analyze_text` → `word_count`, `unique_words`, `top3`
- [ ] `count_char_recursive('banana', 'a') == 3`
- [ ] README: связь с будущим NLP-модулем (1 абзац)
- [ ] `manual_tests.py` — 7+ assert

---

## Решения учащегося

1. Как агрегировать частоты по **списку** текстов класса.
2. Порог «маркерного» слова (2×, 3×).
3. Tie-break при равных score в `naive_classify`.
4. Пунктуация в tokenize.

---

## Связь с модулем

| Урок | В артефакте |
|---|---|
| 1–2 | def, return, docstring |
| 3 | отладка classify |
| 4 | count_char_recursive |
| 5 | lambda в pipeline |
| 6 | apply_pipeline |

---

## Стартовые файлы

[starter/](starter/) — заготовки + тесты.
