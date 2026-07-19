# Данные модуля 8 (план)

**Статус:** исходник выбран; slim CSV ещё не собран. Собирать на этапе `design-lesson`.

## Источник

| Поле | Значение |
|---|---|
| Набор | [Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) |
| Файлы исходника | `olist_orders_dataset.csv`, `olist_order_items_dataset.csv`, `olist_sellers_dataset.csv`, `olist_customers_dataset.csv` (гео штатов) |
| Почему здесь | Реальные сроки доставки и freight; метка опоздания без синтетики |

## Целевой артефакт данных модуля

| Файл (ожидаемый) | Содержание |
|---|---|
| `orders_slim.csv` | Одна строка ≈ заказ (или item): id, даты purchase / estimated / delivered, `freight_value`, гео-прокси (штат seller/customer), опц. `seller_id` |
| `is_late` | Бинарный столбец по правилу ниже |

## Правило метки (черновик — зафиксировать при сборке)

```
is_late = 1, если order_delivered_customer_date > order_estimated_delivery_date
         (и обе даты непустые); иначе 0 или NaN → отфильтровать
```

Дополнительно полезны: `delivery_days`, `estimated_days`, `freight_value`.

## Ограничения среза

- Ученик на паре 49 **не** собирает полный join с Kaggle с нуля — только работает со slim.
- Объём: ориентир 5–20k строк после фильтра доставленных заказов.
- Не тащить сюда RFM-таблицу модуля 5 как основной объект (можно упомянуть связь маркеплейса устно).
- Attribution: Olist / Kaggle.

## Связь с модулем 5

Тот же исходник Olist, **другой slim и другой вопрос** (опоздание vs RFM).
