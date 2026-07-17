# Agent passes (журнал проходов)

Операционный журнал: **когда** skill/агент последний раз успешно закончил работу над модулем. Не педагогический стандарт.

Каждый skill после успешного прохода по модулю обновляет свою ячейку в таблице: дата-время ISO с оффсетом `+07:00` (`YYYY-MM-DDTHH:MM:SS+07:00`). Если прохода не было — `—`.

| Модуль | design-module | design-lesson | test-teacher | review-edu-material | expert-edu-editor | integrate-ml-context | canvas-lms |
|---|---|---|---|---|---|---|---|
| `08_01_functions_recursion` | — | 2026-07-17T23:34:55+07:00 | — | — | 2026-07-17T23:34:55+07:00 | — | 2026-07-17T23:34:55+07:00 |
| `08_02_carsharing_pandas_lr` | — | — | 2026-07-17T01:43:52+07:00 | — | 2026-07-17T17:06:03+07:00 | — | 2026-07-17T17:06:07+07:00 |
| `08_03_titanic_eda` | 2026-07-17T18:29:04+07:00 | 2026-07-17T18:29:04+07:00 | 2026-07-17T18:29:04+07:00 | — | 2026-07-17T18:29:04+07:00 | — | 2026-07-17T18:37:01+07:00 |
| `08_04_mnist_knn` | — | — | — | — | — | — | — |
| `08_05_shop_feature_engineering` | — | — | — | — | — | — | — |
| `08_06_ab_startup` | — | — | — | — | — | — | — |
| `08_07_bank_arrays_search` | — | — | — | — | — | — | — |
| `08_08_logistics_clustering` | — | — | — | — | — | — | — |
| `08_09_courier_dp` | — | — | — | — | — | — | — |
| `08_10_churn_logreg` | — | — | — | — | — | — | — |
| `08_11_virtual_polygon` | — | — | — | — | — | — | — |


### Примечание по `08_01_functions_recursion`

| Skill | Время | Основание |
|---|---|---|
| `design-lesson` / `expert-edu-editor` | 2026-07-17T23:34:55+07:00 | «A. Чего хотим от пары» в LESSON.md; без «Ориентир времени» |
| `canvas-lms` | 2026-07-17T23:34:55+07:00 | wiki планов пар 1–10 updated+published (`--update-page-only`) |

### Примечание по `08_02_carsharing_pandas_lr`

По git log (best-effort при заведении журнала):

| Skill | Время | Основание |
|---|---|---|
| `test-teacher` | 2026-07-17T01:43:52+07:00 | commit `e2a8b0b` — правки пути учителя после test-teacher |
| `expert-edu-editor` | 2026-07-17T17:06:03+07:00 | commit `a6b12a3` — deepen notebooks (тот же день, что и publish) |
| `canvas-lms` | 2026-07-17T17:06:07+07:00 | commit `a6b12a3` — Canvas publish lesson items |

### Примечание по `08_03_titanic_eda`

| Skill | Время | Основание |
|---|---|---|
| `design-module` / `design-lesson` | 2026-07-17T18:29:04+07:00 | UNIT + 9 LESSON A–E; стандартный seaborn Titanic; generate_notebooks |
| `test-teacher` / `expert-edu-editor` | 2026-07-17T18:29:04+07:00 | расшифровки ЦПТ/bias; ход B; артефакт-ссылки |
| `canvas-lms` | 2026-07-17T18:37:01+07:00 | модуль Canvas **54690**, пары 21–29 published (`publish_canvas_m3.py --all`) |
