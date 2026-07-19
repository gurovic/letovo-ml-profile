# Стартовый код `text_stats`

Работать **в этой папке** (`artifact/starter/`). Не копировать файлы из `solution/` — это эталон только для учителя.

Полное задание: [PROJECT.md](../PROJECT.md). Кратко для учителя — ниже.

---

## Учителю: порядок на паре 8

| Шаг | Функции в `text_stats.py` | После шага запустить |
|---|---|---|
| 1 | `tokenize` | `python manual_tests.py` → OK: `test_tokenize` |
| 2 | `count_char_recursive` | → OK: `test_count_char_recursive` |
| 3 | `word_frequencies`, `filter_tokens`, `top_n` | → OK: `test_word_frequencies`, `test_filter_tokens`, `test_top_n` |
| 4 | `apply_pipeline` | → OK: `test_apply_pipeline` |
| 5 | `analyze_text` (можно через `count_words`) | → OK: `test_analyze_text` |
| 6 | `aggregate_frequencies`, `compare_class_frequencies` | → OK: `test_compare_class_frequencies` |
| 7 | `naive_classify` | → OK: оба `test_naive_classify_*` |
| 8 | README ученика (шаблон ниже) | сдача |

**Пара 8:** шаги 1–8 на одной паре (ориентир к середине: ≥6/10 тестов).

Подсказка по `tokenize`: в начале файла `import re`; слова — `re.findall(r"\w+", text.lower(), flags=re.UNICODE)` (кириллица тоже слово). Пунктуация отбрасывается.

Если тест упал — см. таблицу в [PROJECT.md § Если тест упал](../PROJECT.md#если-тест-упал).

---

## Запуск тестов

```bash
cd modules/08_01_functions_recursion/artifact/starter
python manual_tests.py
```

Пока функция не реализована — `NotImplementedError` на соответствующем тесте; это нормально в начале.

Успех: строка `All 10 manual tests passed.`

---

## Что сдаёт ученик

1. `text_stats.py` — все функции из [PROJECT.md](../PROJECT.md).
2. `README.md` (создать в этой папке) — по шаблону ниже.
3. Прохождение `manual_tests.py`.

---

## Шаблон README ученика

Скопировать в `README.md` и заполнить:

```markdown
# text_stats — [ФИО]

## Цепочка шагов (pipeline)

1. tokenize → …
2. …

## Решения

- Порог маркера (ratio): …
- При равном счёте маркеров в naive_classify: …

## 5 моих фраз для naive_classify

| Фраза | Ожидаю | Получилось |
|---|---|---|
| … | positive/negative | … |
(всего 5 строк; нужно ≥4 верных)

## Связь с курсом (1 абзац)

Как частоты слов связаны с будущим NLP / анализом текстов.
```

---

## Эталон для учителя

[solution/](../solution/) — готовый код и [solution/README.md](../solution/README.md) с маркерами (`отличный`, `скучный` и др.).
