# Интернет-магазин: Feature Engineering и lambda

**Класс:** 8 · **КТП:** пары 30–35 · **Объём:** 12 академических часов  
**Статус:** полный комплект: UNIT, 6 LESSON, 18 ноутбуков, данные и итоговый артефакт  
**Canvas:** не опубликовано

## Сквозной результат

Команда CRM получает три slim-таблицы в схеме Olist и строит функцию
`preprocess_customers(orders_df, customers_df, payments_df)`. На выходе — одна
строка на клиента с `Recency`, `Frequency`, `Monetary`, долей оплат картой,
средним сроком доставки и штатом; рядом — ordered log выполненных шагов.

Модуль посвящён **transform**, а не predict: метки `churn` нет, модель не
обучается. Ученик отвечает за четыре инженерные гарантии:

1. единица наблюдения и ключ зафиксированы до `join` / `groupby`;
2. вход проверяется через `raise` до вычисления признаков;
3. число заказов и общая сумма оплат сходятся с источником;
4. повторный запуск даёт тот же результат и не меняет входные DataFrame.

## Маршрут по парам

| Пара | Урок | Решение ученика | Вклад в артефакт |
|---|---|---|---|
| 30 | [Типы и apply](lessons/01_feature_types_apply/LESSON.md) | тип, правило, границы, apply vs vectorized | карточка признака |
| 31 | [Признаки заказа](lessons/02_practice_apply_orders/LESSON.md) | календарь, срок доставки, p99, leakage | проверяемые order-level transforms |
| 32 | [RFM через groupby](lessons/03_rfm_groupby/LESSON.md) | общая ref date и три агрегата | таблица клиент×RFM |
| 33 | [RFM+](lessons/04_practice_aggregates/LESSON.md) | share_card, средний срок, score | расширенная таблица признаков |
| 34 | [Logging и raise](lessons/05_logging_raise/LESSON.md) | schema/key/value contract и negative tests | fail-fast валидатор и audit |
| 35 | [Итоговый pipeline](lessons/06_practice_pipeline/LESSON.md) | чистая функция, инварианты, preview | сдаваемый preprocessing |

Каждая папка содержит:

- `lesson.ipynb` — 8 последовательных разделов, stubs и assert;
- `homework.ipynb` — Part A и Challenge;
- `solutions.ipynb` — секционные решения урока и ДЗ для преподавателя;
- три локальные копии CSV для автономного запуска;
- `LESSON.md` A–E с поминутным ходом, репликами и критериями закрытия.

## Данные и правила

Канон, attribution, схема и точные определения RFM находятся в
[data/README.md](data/README.md). В комплект входят:

- `orders_slim.csv` — заказ, клиент, статус и даты;
- `customers_slim.csv` — клиент и штат;
- `payments_slim.csv` — тип и сумма оплаты.

`Recency` считается от последней покупки клиента до общей максимальной даты
таблицы; `Frequency` — число уникальных заказов; `Monetary` — сумма оплат.

## Ворота качества

Из корня репозитория:

```powershell
python modules/08_05_shop_feature_engineering/generate_notebooks.py
python scripts/run_solutions.py modules/08_05_shop_feature_engineering
```

Ожидается: 18 сгенерированных ноутбуков, 18 копий CSV, 6 полных LESSON и
`6 passed, 0 failed`. Генератор — источник истины для ноутбуков и LESSON:
ручные изменения сгенерированных файлов будут перезаписаны.

## Навигация

- [UNIT.md](UNIT.md) — цели, последовательность, оценивание и границы scope;
- [artifact/PROJECT.md](artifact/PROJECT.md) — бриф итоговой сдачи;
- [generate_notebooks.py](generate_notebooks.py) — воспроизводимая сборка.
