# Каршеринг: pandas и линейная регрессия

**Класс:** 8  
**КТП:** пары 12–21  
**Статус:** материалы модуля (уроки, ноутбуки, артефакт)

Сюжет: аналитический отдел каршеринга «Дорога» прогнозирует длительность поездок по таблице поездок.

| Документ | Назначение |
|---|---|
| [UNIT.md](UNIT.md) | Unit Planner |
| [data/trips.csv](data/trips.csv) | Сквозной датасет |
| [artifact/PROJECT.md](artifact/PROJECT.md) | Критерии мини-отчёта |
| [generate_notebooks.py](generate_notebooks.py) | Пересборка `.ipynb` |

## Пары

| Пара | Папка | Роль |
|---|---|---|
| 12 | [01_pandas_dataframe](lessons/01_pandas_dataframe/) | введение |
| 13 | [02_practice_filters](lessons/02_practice_filters/) | отработка |
| 14 | [03_eda_scatter](lessons/03_eda_scatter/) | введение |
| 15 | [04_train_test_lr](lessons/04_train_test_lr/) | введение |
| 16 | [05_practice_metrics](lessons/05_practice_metrics/) | отработка |
| 17 | [06_try_except_csv](lessons/06_try_except_csv/) | введение |
| 18 | [07_practice_features](lessons/07_practice_features/) | отработка |
| 19 | [08_multifeature_overview](lessons/08_multifeature_overview/) | введение (обзор) |
| 20 | [09_report_draft](lessons/09_report_draft/) | интеграция |
| 21 | [10_report_submit](lessons/10_report_submit/) | интеграция |

## Пересборка ноутбуков

```bash
python modules/08_02_carsharing_pandas_lr/generate_notebooks.py
python modules/08_02_carsharing_pandas_lr/data/generate_trips.py
```

Для Colab: в папке урока лежит копия `trips.csv` (рядом с ноутбуком).
