# Каршеринг: pandas и линейная регрессия

**Класс:** 8  
**КТП:** пары 11–20  
**Статус:** материалы (уроки, ноутбуки, артефакт)

Сюжет: аналитический отдел каршеринга «Дорога» прогнозирует длительность поездок по таблице поездок.

| Документ | Назначение |
|---|---|
| [UNIT.md](UNIT.md) | Unit Planner |
| [data/trips.csv](data/trips.csv) | Сквозной датасет |
| [artifact/PROJECT.md](artifact/PROJECT.md) | Критерии мини-отчёта |
| [artifact/starter/](artifact/starter/) | Шаблон отчёта для ученика |
| [generate_notebooks.py](generate_notebooks.py) | Пересборка `.ipynb` |
| [canvas_gist_map.json](canvas_gist_map.json) | Gist ID → Colab (пары 11–20) |

## Пары

| Пара | Папка | Роль |
|---|---|---|
| 11 | [01_pandas_dataframe](lessons/01_pandas_dataframe/) | введение |
| 12 | [02_practice_filters](lessons/02_practice_filters/) | отработка |
| 13 | [03_eda_scatter](lessons/03_eda_scatter/) | введение |
| 14 | [04_train_test_lr](lessons/04_train_test_lr/) | введение |
| 15 | [05_practice_metrics](lessons/05_practice_metrics/) | отработка |
| 16 | [06_try_except_csv](lessons/06_try_except_csv/) | введение |
| 17 | [07_practice_features](lessons/07_practice_features/) | отработка |
| 18 | [08_multifeature_overview](lessons/08_multifeature_overview/) | введение (обзор) |
| 19 | [09_report_draft](lessons/09_report_draft/) | интеграция |
| 20 | [10_report_submit](lessons/10_report_submit/) | интеграция |

## Пересборка ноутбуков

```bash
python modules/08_02_carsharing_pandas_lr/generate_notebooks.py
python modules/08_02_carsharing_pandas_lr/data/generate_trips.py
```

Для Colab: в папке урока лежит копия `trips.csv` (рядом с ноутбуком).
