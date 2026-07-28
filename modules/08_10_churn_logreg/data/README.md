# Данные модуля 10: UCI Bank Marketing (пары 60-64)

## Файл модуля

| Файл | Назначение |
|---|---|
| `bank_marketing_slim.csv` | Учебный срез для уроков 60-64 |
| `make_bank_marketing_slim.py` | Сборка slim: сначала UCI, при недоступности сети — синтетический fallback с теми же типами столбцов |

## Источник

| Поле | Значение |
|---|---|
| Базовый источник | [UCI Bank Marketing](https://archive.ics.uci.edu/dataset/222/bank+marketing) |
| Цель | `y` в `{yes, no}` — отклик на депозит |
| Почему выбран | Реальный кейс банковской кампании + естественный дисбаланс классов |
| Fallback | Синтетика в стиле UCI (те же смысловые столбцы), только если UCI недоступен |

## Leakage rule (обязательно)

`duration` присутствует в slim только для демонстрации leakage.  
Во всех уроках, CLI и артефакте: `duration` запрещен в признаках модели.

Минимальная проверка:

```python
assert "duration" not in feature_columns
```

## Состав `bank_marketing_slim.csv`

`age`, `job`, `marital`, `education`, `contact`, `month`, `campaign`, `pdays`, `previous`, `poutcome`, `emp.var.rate`, `cons.price.idx`, `cons.conf.idx`, `euribor3m`, `nr.employed`, `duration`, `y`.

## Как пересобрать

Из корня репозитория:

```bash
python modules/08_10_churn_logreg/data/make_bank_marketing_slim.py
```

Скрипт печатает `source=...`:
- `source=uci_bank_marketing` — взят реальный UCI;
- `source=synthetic_fallback` — сеть/источник недоступны, использован classroom fallback.
