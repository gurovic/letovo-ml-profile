# Артефакт модуля: библиотека `text_stats`

**Тип:** Python-модуль + README учащегося  
**Срок:** пара КТП **8** (**2** академических часа + доработка дома при необходимости)  
**Для учителя:** это **итоговая сдача** модуля; минимум — `manual_tests.py` без ошибок (10 проверок)

**Смысл для класса:** частоты слов в текстах двух классов отзывов; простой классификатор «позитив / негатив» без pandas и sklearn.

Данные: `TEXTS_POSITIVE`, `TEXTS_NEGATIVE` в [data/module_datasets.py](../data/module_datasets.py).

---

## Задача

Собрать модуль анализа текста **без pandas/sklearn**:

1. разбить текст на слова и посчитать частоты;
2. сравнить два класса коротких отзывов (позитивные / негативные);
3. по «маркерным» словам угадать класс нового текста.

Итог — работающий `text_stats.py`, README ученика и прохождение `manual_tests.py`.

---

## Обязательные функции

Справочник контрактов. **Порядок кода на парах** — в [starter/README.md](starter/README.md) (шаги 1–8); не обязан совпадать с порядком строк ниже.

| Функция | Контракт | Зачем |
|---|---|---|
| `tokenize(text)` | `str` → список слов в lower | разбить текст на слова |
| `word_frequencies(tokens)` | список → `{слово: частота}` | частоты слов |
| `filter_tokens(tokens, min_len=3)` | оставить токены длиной ≥ `min_len` | убрать короткие слова |
| `top_n(freq, n=5)` | top-n пар `(слово, count)` по убыванию частоты | самые частые слова |
| `count_char_recursive(s, ch)` | рекурсивный подсчёт `ch` в `s` | рекурсия (пара 7) |
| `analyze_text(text)` | `{"word_count", "unique_words", "top3"}` | краткое описание одного текста |
| `apply_pipeline(data, steps)` | последовательно применить функции из `steps` | цепочка шагов (пара 7) |
| `aggregate_frequencies(texts)` | суммарные частоты по списку текстов класса | нужна для сравнения классов; **отдельного теста нет** — проверяется через `compare_class_frequencies` |
| `compare_class_frequencies(texts_a, texts_b, ratio=2.0)` | `{слово: "positive"\|"negative"}` при перевесе ≥ `ratio` | маркерные слова класса |
| `naive_classify(text, texts_a, texts_b)` | `"positive"` / `"negative"` / `"unknown"` | предсказание класса текста |

Вспомогательная `count_words(tokens)` — по желанию; в эталоне используется в `analyze_text`.

---

## Пример использования

Запускать из папки `artifact/starter/` (как `manual_tests.py` — он сам добавляет путь к `data/`):

```python
from text_stats import apply_pipeline, tokenize, filter_tokens, word_frequencies, naive_classify
from data.module_datasets import TEXTS_POSITIVE, TEXTS_NEGATIVE

pipeline = [tokenize, lambda t: filter_tokens(t, 3), word_frequencies]
freq_one = apply_pipeline("отличный фильм", pipeline)

naive_classify("отличный фильм рекомендую", TEXTS_POSITIVE, TEXTS_NEGATIVE)
# ожидается: "positive"
```

Демо-тексты отзывов — в [data/module_datasets.py](../data/module_datasets.py) (`TEXTS_POSITIVE`, `TEXTS_NEGATIVE`).

---

## Критерии приёмки

| # | Критерий |
|---|---|
| 1 | `manual_tests.py` в `starter/` — все 10 тестов без ошибок |
| 2 | `compare_class_frequencies` на примерах из задания — ≥2 маркера (в т.ч. `отличный`, `скучный`) |
| 3 | `naive_classify` — ≥4/5 верных на **своих** тестовых фразах (перечислить в README) |
| 4 | `analyze_text("one two two three")` → `word_count==4`, `unique_words==3`, `top3[0]==("two", 2)` (как в `manual_tests.py`) |
| 5 | `count_char_recursive("banana", "a") == 3` |
| 6 | README: порядок pipeline, tie-break в `naive_classify`, 1 абзац про связь с будущим NLP |

---

## Решения учащегося (зафиксировать в README)

1. Агрегация частот по списку текстов (`aggregate_frequencies`).
2. Порог маркера (`ratio`, по умолчанию 2.0).
3. Tie-break при равных score в `naive_classify` (эталон: `"unknown"`).
4. Обработка пунктуации в `tokenize`: регулярное выражение `\w+` с флагом Unicode (кириллица — отдельные токены; запятые и кавычки отбрасываются).

Шаблон README для ученика — [starter/README.md](starter/README.md#шаблон-readme-ученика).

---

## Связь с парами модуля

| Пары | В артефакте |
|---|---|
| 2–3 | `def`, `return`, docstring |
| 5–6 | отладка метрик / журнал — тот же навык при отладке `naive_classify` |
| 7 | `count_char_recursive`; `lambda` в pipeline, `apply_pipeline` |
| 8 | сборка `text_stats` + сдача |

---

## Файлы

| Путь | Назначение |
|---|---|
| [starter/](starter/) | заготовки + тесты для учащегося |
| [solution/](solution/) | эталон и ответы для учителя |

Эталон: `cd artifact/solution && python manual_tests.py` → 10 passed.

---

## Для учителя (пара 8)

План пары и карточка §13: [08_artifact/LESSON.md](../lessons/08_artifact/LESSON.md).

| | |
|---|---|
| **Выдать** | папку [starter/](starter/) целиком; ученики **не** трогают `solution/` |
| **Инструкция ученику** | [starter/README.md](starter/README.md) — порядок функций и шаблон README |
| **Пара 8** | разбор PROJECT; шаги 1–8; сдача `text_stats.py` + README + 10 тестов |
| **Проверка** | из `artifact/starter/`: `python manual_tests.py` → `All 10 manual tests passed.` |
| **Зачёт** | 10 тестов + README ученика (5 своих фраз для `naive_classify`, из них ≥4 верных) |
| **Эталон (не раздавать)** | [solution/](solution/) — ответы и разбор маркеров |
| **Первая фраза** | «Собираете библиотеку из функций модуля — тесты и README решают, готово ли к сдаче» |

### Если тест упал

| Симптом | Что проверить |
|---|---|
| `ModuleNotFoundError: data` | запускать из `artifact/starter/`, не из корня репозитория |
| `NotImplementedError` | функция ещё не реализована — нормально в начале |
| `compare_class_frequencies` | нужны рабочие `tokenize`, `word_frequencies`, `aggregate_frequencies` |
| `naive_classify` → всегда `unknown` | сначала проверить `compare_class_frequencies`; при равном счёте маркеров — `"unknown"` |
| тест `analyze_text` не сходится | вход `"one two two three"` — 4 слова, 3 уникальных, `two` встречается 2 раза |

---

## Карточка урока (§13)

В LESSON пары 8 (одна пара = один LESSON.md):

- [§13 пара 8](../lessons/08_artifact/LESSON.md#e-карточка-урока-13)
