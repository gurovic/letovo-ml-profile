# Сквозные данные модуля

Один набор примеров на **все пары** модуля — без pandas, только списки и словари.

Импорт в ноутбуке (из папки урока):

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path('../..').resolve()))  # корень modules/08_01_functions_recursion
from data.module_datasets import APARTMENTS, EXAM_SCORES
```

Файл с данными: [module_datasets.py](module_datasets.py)

| Датасет | Пары | Зачем на уроке |
|---|---|---|
| `APARTMENTS` | 2–3 | площадь → цена; линейное предсказание |
| `EXAM_SCORES` | 3–4, 7 | описание баллов; порог «сдал»; фильтр аномалий |
| `PREDICTIONS` / `LABELS` | 5–6 | доля верных ответов; счётчики tp/fp/fn/tn |
| `NESTED_API_RESPONSE` | 7 | вложенный список/dict — рекурсия |
| `CATEGORY_TREE` | 7 | дерево категорий — обход с отступом |
| `FEATURE_ROWS` | 7 | словарь-признак; цепочка extract → scale → predict |
| `MODEL_RUNS` | 7 | сортировка моделей по метрике f1 |
| `FEATURE_POINTS` | 7 | точка с максимальной «дальностью» (задача на `key=`) |
| `TEXTS_POSITIVE` / `TEXTS_NEGATIVE` | 8 | итоговый артефакт `text_stats` |
