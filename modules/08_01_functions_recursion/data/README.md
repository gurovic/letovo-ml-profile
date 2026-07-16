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
| `APARTMENTS` | 2–3, 9 | площадь → цена; линейное предсказание |
| `EXAM_SCORES` | 4–5, 9 | описание баллов; порог «сдал»; фильтр аномалий |
| `PREDICTIONS` / `LABELS` | 6–7 | доля верных ответов; счётчики tp/fp/fn/tn |
| `NESTED_API_RESPONSE` | 8–9 | вложенный список/dict — рекурсия |
| `CATEGORY_TREE` | 8–9 | дерево категорий — обход с отступом |
| `FEATURE_ROWS` | 9 | словарь-признак; цепочка extract → scale → predict |
| `MODEL_RUNS` | 9 | сортировка моделей по метрике f1 |
| `FEATURE_POINTS` | 9 | точка с максимальной «дальностью» (задача на `key=`) |
| `TEXTS_POSITIVE` / `TEXTS_NEGATIVE` | 9–10 | итоговый артефакт `text_stats` |
