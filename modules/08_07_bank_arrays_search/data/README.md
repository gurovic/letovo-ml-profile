# Данные модуля: логи банковских транзакций

Датасет создан для модуля `08_07_bank_arrays_search` (пары 42–48): линейный/бинарный поиск, сортировки, `sorted(key=...)`, два указателя.

## Файлы

| Файл | Размер | Назначение |
|---|---:|---|
| `bank_transactions_unsorted_sample.csv` | 24 строки | Inline-friendly несортированный пример |
| `bank_transactions_sorted_by_txn_id_sample.csv` | 24 строки | Inline-friendly пример для бинарного поиска |
| `bank_transactions_sorted_by_amount_sample.csv` | 24 строки | Inline-friendly пример для задач по сумме |
| `bank_transactions_unsorted.csv` | 960 строк | Линейный поиск и задачи до сортировки |
| `bank_transactions_sorted_by_txn_id.csv` | 960 строк | Бинарный поиск по `txn_id` |
| `bank_transactions_sorted_by_amount.csv` | 960 строк | Сортировки по ключу, два указателя по `amount` |
| `bank_transactions_tiny.csv` | 80 строк | Inline-friendly сэмпл для быстрых примеров |

## Схема столбцов

| Столбец | Тип | Смысл |
|---|---|---|
| `txn_id` | int | Идентификатор транзакции |
| `account_id` | int | Идентификатор счёта |
| `day` | int | День месяца (1–30) |
| `amount` | int | Сумма транзакции |
| `tx_type` | str | Тип операции (`debit`, `credit`, `transfer`, `cash_out`) |
| `merchant_category` | str | Категория операции |
| `city` | str | Город |
| `risk_score` | int | Учебный риск-скор |

## Генерация

```bash
python modules/08_07_bank_arrays_search/data/make_bank_transactions_csv.py
```

- Используется фиксированный seed: `80742`.
- Объём данных classroom-friendly: сотни/низкие тысячи строк.
- Файлы `*_sample.csv` лежат в репозитории как быстрые примеры для чтения без генерации.
- В модуле нет теории hash map; задачи строятся на списках, кортежах и индексах.
