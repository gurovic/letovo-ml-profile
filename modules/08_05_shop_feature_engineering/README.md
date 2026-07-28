# Интернет-магазин / маркетплейс: Feature Engineering и lambda

**Класс:** 8  
**КТП:** пары **30–35**  
**Статус:** материалы модуля (UNIT, LESSON, ноутбуки, артефакт)

Сюжет: CRM маркетплейса на данных Olist собирает RFM-признаки покупателей и воспроизводимый preprocessing.

## Данные

Slim-датасет: `orders_slim.csv`, `customers_slim.csv`, `payments_slim.csv` в `data/`.  
Правила источника и RFM: [data/README.md](data/README.md).

## Уроки

| Пара | Папка | Роль |
|---|---|---|
| 30 | [01_feature_types_apply](lessons/01_feature_types_apply/) | введение |
| 31 | [02_practice_apply_orders](lessons/02_practice_apply_orders/) | отработка |
| 32 | [03_rfm_groupby](lessons/03_rfm_groupby/) | введение |
| 33 | [04_practice_aggregates](lessons/04_practice_aggregates/) | отработка |
| 34 | [05_logging_raise](lessons/05_logging_raise/) | введение |
| 35 | [06_practice_pipeline](lessons/06_practice_pipeline/) | интеграция |

## Запуск

```bash
python modules/08_05_shop_feature_engineering/generate_notebooks.py
python scripts/run_solutions.py modules/08_05_shop_feature_engineering
```

Артефакт: [artifact/PROJECT.md](artifact/PROJECT.md).  
План модуля: [UNIT.md](UNIT.md).
