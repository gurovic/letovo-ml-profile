# Данные модуля 8: логистика и кластеризация

## Источник и режим сборки

| Поле | Значение |
|---|---|
| Базовый источник | [Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) |
| Raw-файлы (если доступны) | `olist_orders_dataset.csv`, `olist_order_items_dataset.csv`, `olist_customers_dataset.csv`, `olist_sellers_dataset.csv` в `data/raw/` |
| Fallback | classroom synthetic (~2000 строк) с Olist-подобными колонками |
| Скрипт сборки | `make_slim.py` |

## Файл модуля

| Файл | Назначение |
|---|---|
| `orders_slim.csv` | Единый срез для всех 6 уроков: структуры данных, частоты, k-means, DBSCAN, аномалии |

## Схема `orders_slim.csv`

- `order_id`, `seller_id`
- `seller_state`, `customer_state`
- `order_purchase_timestamp`
- `order_estimated_delivery_date`
- `order_delivered_customer_date`
- `freight_value`, `price`
- `delivery_days`, `estimated_days`, `delay_days`
- `is_late`

## Правило метки `is_late`

```text
is_late = 1, если order_delivered_customer_date > order_estimated_delivery_date
is_late = 0, иначе
```

Для уроков кластера используются признаки `delivery_days`, `freight_value`, `delay_days`.

## Как собрать данные

```bash
python modules/08_08_logistics_clustering/data/make_slim.py
```

## Ограничения

- В уроках 49-52 используем только готовый slim, без полного join на паре.
- Метка `is_late` нужна для describe и интерпретации кластеров, а не для supervised-предсказания.
- RFM-контекст модуля 5 сюда не переносится.
