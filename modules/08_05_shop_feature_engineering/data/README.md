# Данные модуля 5 — slim заказов маркетплейса (схема Olist)

| Файл | Назначение |
|---|---|
| `orders_slim.csv` | Заказы: id, клиент, статус, даты |
| `customers_slim.csv` | Клиенты: id, unique_id, штат |
| `payments_slim.csv` | Оплаты: order_id, тип, сумма |
| `make_slim.py` | Сборка slim из Olist raw **или** classroom-синтетика |

## Источник

Канон сюжета — [Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
(`olist_orders_dataset`, `olist_customers_dataset`, `olist_order_payments_dataset`).

Чтобы ноутбуки работали **офлайн** без Kaggle, `make_slim.py` по умолчанию пишет
**classroom-slim** с теми же именами столбцов (seed=42). Если положить настоящие CSV
в `data/raw/`, скрипт соберёт slim из них.

```bash
python make_slim.py   # из каталога data/
```

Attribution: схема и сюжет — Olist / Kaggle; classroom-slim — учебная синтетика для профиля.

## RFM (зафиксировано)

| Признак | Правило |
|---|---|
| Recency | Дни от `max(order_purchase_timestamp)` клиента до опорной даты = max даты в таблице заказов |
| Frequency | Число заказов клиента в slim |
| Monetary | Сумма `payment_value` по заказам клиента |

Метку `churn` **не** вводим (модуль 10).

## Столбцы slim

**orders_slim:** `order_id`, `customer_id`, `order_status`, `order_purchase_timestamp`, `order_delivered_customer_date`  

**customers_slim:** `customer_id`, `customer_unique_id`, `customer_state`  

**payments_slim:** `order_id`, `payment_type`, `payment_value`

## Связь с модулем 8

Модуль 8 — тот же исходник Olist, другой вопрос (опоздания). Не смешивать один slim без пометки.
