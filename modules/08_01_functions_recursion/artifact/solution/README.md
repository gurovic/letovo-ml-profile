# Эталонное решение `text_stats`

Для учителя и проверки критериев [PROJECT.md](../PROJECT.md). Учащиеся работают в [starter/](../starter/).

## Запуск тестов

```bash
cd modules/08_01_functions_recursion/artifact/solution
python manual_tests.py
```

Ожидается: `All 10 manual tests passed.`

## Ответы на демо-данных

Данные: `TEXTS_POSITIVE`, `TEXTS_NEGATIVE` в [data/module_datasets.py](../../data/module_datasets.py).

### Маркерные слова (`compare_class_frequencies`, ratio=2)

| Слово | Класс |
|---|---|
| отличный | positive |
| понравилось | positive |
| лучший | positive |
| скучный | negative |
| слабый | negative |
| зря | negative |

Слова в обоих классах (фильм, рекомендую, очень) при ratio=2 **не** становятся маркерами.

### `naive_classify` — эталонные фразы

| Фраза | Ответ |
|---|---|
| отличный фильм рекомендую | positive |
| очень понравилось смотреть | positive |
| лучший фильм года | positive |
| скучный фильм не рекомендую | negative |
| потерял время зря | negative |

Учащийся в своём README фиксирует **свои** 5 тестовых фраз; критерий — 4/5 верных на выбранном наборе.

### Прочие эталоны

| Вызов | Ответ |
|---|---|
| `count_char_recursive('banana', 'a')` | 3 |
| `analyze_text('one two two')['word_count']` | 3 |
| `tokenize('Hello World')` | `['hello', 'world']` |
