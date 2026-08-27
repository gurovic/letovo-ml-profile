# Сквозные данные модуля

Один набор примеров на **все пары** модуля — без pandas, только списки и словари.

Файл с данными: [module_datasets.py](module_datasets.py).  
Загрузка с fallback для Colab: [load_module_datasets.py](load_module_datasets.py).

## Импорт в ноутбуке

Локально (VS Code / Jupyter в репо) — из папки урока. В **Colab** (gist) локального `data/` нет: ячейка скачивает `module_datasets.py` с raw GitHub.

```python
import importlib.util
import sys
import urllib.request
from pathlib import Path

_RAW = (
    "https://raw.githubusercontent.com/gurovic/letovo-ml-profile/main/"
    "modules/08_01_functions_recursion/data/module_datasets.py"
)

def _import_module_datasets():
    for root in (Path("../..").resolve(), Path(".").resolve()):
        path = root / "data" / "module_datasets.py"
        if path.is_file():
            root_s = str(root)
            if root_s not in sys.path:
                sys.path.insert(0, root_s)
            import data.module_datasets as md
            return md
    dest = Path("module_datasets.py")
    urllib.request.urlretrieve(_RAW, dest)
    spec = importlib.util.spec_from_file_location("module_datasets", dest)
    md = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(md)
    return md

_md = _import_module_datasets()
APARTMENTS = _md.APARTMENTS
EXAM_SCORES = _md.EXAM_SCORES
# … остальные имена по необходимости урока
```

Тот же порядок «диск → URL», что для CSV в модуле 2. В материалах для учеников — только **raw**-ссылка на файл данных, не обзор репозитория.

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
