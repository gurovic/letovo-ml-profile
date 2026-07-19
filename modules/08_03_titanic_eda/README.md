# Расследование на «Титанике»: EDA и статистика

**Класс:** 8  
**КТП:** пары **17–23**  
**Статус:** материалы модуля (UNIT, LESSON, ноутбуки, артефакт)

Сюжет: историческое общество поручило выяснить, кто выживал чаще, только анализом данных (**без** обучения модели).

## Данные

Стандартный Titanic: `data/titanic.csv` — экспорт `seaborn.load_dataset('titanic')` (891×15).  
Атрибуция и столбцы: [data/README.md](data/README.md). **Не** синтетический генератор.

## Уроки

| Пара | Папка | Роль |
|---|---|---|
| 17 | [01_load_inspect_paths](lessons/01_load_inspect_paths/) | введение |
| 18 | [02_practice_inspect](lessons/02_practice_inspect/) | отработка |
| 19 | [03_mean_median_std](lessons/03_mean_median_std/) | введение |
| 20 | [04_practice_boxplot](lessons/04_practice_boxplot/) | отработка |
| 21 | [05_bias_clt_missing](lessons/05_bias_clt_missing/) | введение |
| 22 | [06_practice_groups](lessons/06_practice_groups/) | отработка |
| 23 | [07_eda_report](lessons/07_eda_report/) | интеграция |

## Запуск

```bash
# пересборка ноутбуков (после правок generate_notebooks.py)
python modules/08_03_titanic_eda/generate_notebooks.py
```

Артефакт: [artifact/PROJECT.md](artifact/PROJECT.md).

План модуля: [UNIT.md](UNIT.md).

## Canvas

- Курс: **6465**
- Gist map: [canvas_gist_map.json](canvas_gist_map.json) (пары 17–23 → Colab)
- Publish: `python scripts/publish_canvas_m3.py --all`
- **Статус publish:** после сжатия 9→7 пар — переопубликовать модуль **54690** (курс 6465)
