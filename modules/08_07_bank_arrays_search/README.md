# Массивы: поиск и сортировка

**Класс:** 8  
**КТП:** пары 42–48  

**Статус:** материалы модуля (UNIT, LESSON, ноутбуки, артефакт)

Сюжет: банк «Надёжный» ищет транзакции в отсортированных логах.

## Данные

Файлы модуля:

- `data/bank_transactions_unsorted.csv`
- `data/bank_transactions_sorted_by_txn_id.csv`
- `data/bank_transactions_sorted_by_amount.csv`
- `data/bank_transactions_tiny.csv`

Сборка (фиксированный seed):  
`python modules/08_07_bank_arrays_search/data/make_bank_transactions_csv.py`

Описание полей: [data/README.md](data/README.md)

## Уроки

| Пара | Папка | Роль |
|---|---|---|
| 42 | [01_linear_binary_search](lessons/01_linear_binary_search/) | введение |
| 43 | [02_practice_search_logs](lessons/02_practice_search_logs/) | отработка |
| 44 | [03_selection_merge_quick](lessons/03_selection_merge_quick/) | введение |
| 45 | [04_practice_sorts](lessons/04_practice_sorts/) | отработка |
| 46 | [05_sorted_key_two_pointers](lessons/05_sorted_key_two_pointers/) | введение |
| 47 | [06_practice_keys_pointers](lessons/06_practice_keys_pointers/) | отработка |
| 48 | [07_complexity_integration](lessons/07_complexity_integration/) | интеграция |

## Генерация и проверка

```bash
python modules/08_07_bank_arrays_search/data/make_bank_transactions_csv.py
python modules/08_07_bank_arrays_search/generate_notebooks.py
python scripts/run_solutions.py modules/08_07_bank_arrays_search
```

Артефакт: [artifact/PROJECT.md](artifact/PROJECT.md)  
План модуля: [UNIT.md](UNIT.md)
