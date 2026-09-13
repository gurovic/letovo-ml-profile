# Решения для учителя: `text_stats`

**Скрыто от учеников.** Эталон кода и ответы для проверки сдачи.

Скачайте архив с эталоном и данными: [text_stats_teacher_solutions.zip](canvas:artifact-teacher-code).

В архиве:

```text
text_stats_teacher/
  text_stats.py       ← эталон
  manual_tests.py     ← те же 10 тестов
  README.md           ← ответы и маркеры
  ASSIGNMENT.md       ← ученическое задание (для сверки)
  data/
    __init__.py
    module_datasets.py ← TEXTS_POSITIVE / TEXTS_NEGATIVE и остальные датасеты модуля
```

Запуск проверки:

```bash
cd text_stats_teacher
python manual_tests.py
```

Ожидается: `All 10 manual tests passed.`

Ученическое задание (для сверки формулировок): [Задание: text_stats](canvas:artifact-project).

---

## Маркерные слова (`compare_class_frequencies`, ratio=2)

| Слово | Класс |
|---|---|
| отличный | positive |
| понравилось | positive |
| лучший | positive |
| скучный | negative |
| слабый | negative |
| зря | negative |

Слова в обоих классах (`фильм`, `рекомендую`, `очень`) при `ratio=2` **не** становятся маркерами.

---

## Эталонные фразы для `naive_classify`

| Фраза | Ответ |
|---|---|
| отличный фильм рекомендую | positive |
| очень понравилось смотреть | positive |
| лучший фильм года | positive |
| скучный фильм не рекомендую | negative |
| потерял время зря | negative |

В README ученика — **свои** 5 фраз; критерий ≥4/5 верных.

---

## Прочие эталоны

| Вызов | Ответ |
|---|---|
| `count_char_recursive("banana", "a")` | 3 |
| `analyze_text("one two two three")` | `word_count=4`, `unique_words=3`, `top3[0]=("two", 2)` |
| `tokenize("Hello World")` | `["hello", "world"]` |

---

## Зачёт

1. `manual_tests.py` — 10/10.
2. README: pipeline, ratio, tie-break (`"unknown"`), 5 фраз (≥4 верных), абзац про NLP.
3. Код похож на эталон по контрактам, не обязательно совпадает построчно.
