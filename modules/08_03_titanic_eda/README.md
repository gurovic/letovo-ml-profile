# Расследование на «Титанике»: EDA и статистика

**Класс:** 8  
**КТП:** пары **21–29**  
**Статус:** материалы модуля (UNIT, LESSON, ноутбуки, артефакт)

Сюжет: историческое общество поручило выяснить, кто выживал чаще, только анализом данных (**без** обучения модели).

## Данные

Стандартный Titanic: `data/titanic.csv` — экспорт `seaborn.load_dataset('titanic')` (891×15).  
Атрибуция и столбцы: [data/README.md](data/README.md). **Не** синтетический генератор.

## Уроки

| Пара | Папка | Роль |
|---|---|---|
| 21 | [01_load_inspect_paths](lessons/01_load_inspect_paths/) | введение |
| 22 | [02_practice_inspect](lessons/02_practice_inspect/) | отработка |
| 23 | [03_mean_median_std](lessons/03_mean_median_std/) | введение |
| 24 | [04_practice_boxplot](lessons/04_practice_boxplot/) | отработка |
| 25 | [05_sampling_bias](lessons/05_sampling_bias/) | введение |
| 26 | [06_normal_missing](lessons/06_normal_missing/) | введение |
| 27 | [07_practice_groups](lessons/07_practice_groups/) | отработка |
| 28 | [08_report_draft](lessons/08_report_draft/) | интеграция |
| 29 | [09_report_submit](lessons/09_report_submit/) | интеграция |

## Запуск

```bash
# пересборка ноутбуков (после правок generate_notebooks.py)
python modules/08_03_titanic_eda/generate_notebooks.py
```

Артефакт: [artifact/PROJECT.md](artifact/PROJECT.md).

План модуля: [UNIT.md](UNIT.md).

## Canvas

- Курс: **6465**
- Gist map: [canvas_gist_map.json](canvas_gist_map.json) (пары 21–29 → Colab)
- Publish: `python scripts/publish_canvas_m3.py --all`
- **Статус publish:** Canvas модуль **54690** (курс 6465), пары 21–29 опубликованы (`python scripts/publish_canvas_m3.py --all`)
