# Сквозные данные модуля

Один набор сюжетов на все 6 уроков — без pandas, только списки и словари.

| Датасет | Уроки | ML/data-смысл |
|---|---|---|
| `APARTMENTS` | 1, 2, 6 | один признак → регрессия, `predict_price` |
| `EXAM_SCORES` | 2, 5 | описательная статистика, порог класса |
| `PREDICTIONS` / `LABELS` | 3 | accuracy, отладка метрики |
| `NESTED_API_RESPONSE` | 4 | flatten вложенных данных |
| `CATEGORY_TREE` | 4 | рекурсивное дерево категорий |
| `FEATURE_ROWS` | 5, 6 | масштабирование признаков перед kNN |
| `MODEL_RUNS` | 5 | leaderboard моделей (Canvas lambda) |
| `FEATURE_POINTS` | 5 | farthest point, key= (Canvas lambda) |
| `TEXTS_POSITIVE` / `TEXTS_NEGATIVE` | артефакт | bag-of-words, сравнение классов |

Импорт в ноутбуке (из корня модуля):

```python
import sys
sys.path.insert(0, "../..")  # или путь к modules/08_functions_recursion
from data.module_datasets import APARTMENTS, EXAM_SCORES
```

Файл: [module_datasets.py](module_datasets.py)
