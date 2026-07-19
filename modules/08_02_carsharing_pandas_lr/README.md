# Краткосрочная аренда: pandas и линейная регрессия

**Класс:** 8  
**КТП:** пары 9–16  
**Статус:** материалы (уроки, ноутбуки, артефакт)

Сюжет: аналитический отдел краткосрочной аренды «StayLocal» прогнозирует ночную цену по таблице объявлений.

| Документ | Назначение |
|---|---|
| [UNIT.md](UNIT.md) | Unit Planner |
| [data/listings.csv](data/listings.csv) | Сквозной датасет |
| [artifact/PROJECT.md](artifact/PROJECT.md) | Критерии мини-отчёта |
| [artifact/starter/](artifact/starter/) | Шаблон отчёта для ученика |
| [generate_notebooks.py](generate_notebooks.py) | Пересборка `.ipynb` |
| [canvas_gist_map.json](canvas_gist_map.json) | Gist ID → Colab (пары 9–16) |
| [media/intro_analyst_video.md](media/intro_analyst_video.md) | Сценарий видео 90–110 с (вступление пары 9) |

## Пары

| Пара | Папка | Роль |
|---|---|---|
| 9 | [01_pandas_dataframe](lessons/01_pandas_dataframe/) | введение |
| 10 | [02_practice_filters](lessons/02_practice_filters/) | отработка |
| 11 | [03_eda_scatter](lessons/03_eda_scatter/) | введение |
| 12 | [04_train_test_lr](lessons/04_train_test_lr/) | введение |
| 13 | [05_practice_metrics](lessons/05_practice_metrics/) | отработка |
| 14 | [06_try_except_csv](lessons/06_try_except_csv/) | введение |
| 15 | [07_practice_features](lessons/07_practice_features/) | отработка (+ обзор multi) |
| 16 | [08_report](lessons/08_report/) | интеграция (сборка + сдача) |

## Пересборка ноутбуков

```bash
python modules/08_02_carsharing_pandas_lr/generate_notebooks.py
python modules/08_02_carsharing_pandas_lr/data/generate_listings.py
```

Для Colab: в папке урока лежит копия `listings.csv` (рядом с ноутбуком).
