# Краткосрочная аренда: pandas и линейная регрессия

**Класс:** 8  
**КТП:** пары 9–16 (Draft 4)  
**Статус:** материалы; сетка выровнена под Draft 4 (перенос/сдвиг, без переписывания тем)

## Сюжет

**StayLocal** (Porto): помочь владельцам объявлений выбрать ночную цену — отчёт с рекомендацией, а не «цифра из головы». Подробнее — [UNIT.md §1](UNIT.md#1-идентификация).

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
| 9 | [01_pandas_dataframe](lessons/01_pandas_dataframe/) (+ [filters/](lessons/01_pandas_dataframe/filters/)) | введение + фильтры |
| 10 | [02_eda_scatter](lessons/02_eda_scatter/) | введение |
| 11 | [03_train_test_lr](lessons/03_train_test_lr/) | введение |
| 12 | [04_practice_metrics](lessons/04_practice_metrics/) | отработка |
| 13 | [05_try_except_csv](lessons/05_try_except_csv/) | введение |
| 14 | [06_practice_features](lessons/06_practice_features/) | отработка (+ обзор multi) |
| 15 | [07_report_build](lessons/07_report_build/) | интеграция (сборка) |
| 16 | [08_report_submit](lessons/08_report_submit/) | интеграция (сдача) |

Перенос Draft 3→4: фильтры **переехали** в подпапку пары 9 (тема не переписывалась); отчёт разнесён на две пары с теми же ноутбуками.

## Пересборка ноутбуков

```bash
python modules/08_02_carsharing_pandas_lr/generate_notebooks.py
python modules/08_02_carsharing_pandas_lr/data/generate_listings.py
```

Для Colab: в папке урока лежит копия `listings.csv` (рядом с ноутбуком).
