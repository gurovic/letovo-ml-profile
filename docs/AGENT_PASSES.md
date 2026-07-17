# Agent passes (журнал проходов)

Операционный журнал: **когда** skill/агент последний раз успешно закончил работу над модулем. Не педагогический стандарт.

Каждый skill после успешного прохода по модулю обновляет свою ячейку в таблице: дата-время ISO с оффсетом `+07:00` (`YYYY-MM-DDTHH:MM:SS+07:00`). Если прохода не было — `—`.

| Модуль | design-module | design-lesson | test-teacher | review-edu-material | expert-edu-editor | integrate-ml-context | canvas-lms |
|---|---|---|---|---|---|---|---|
| `08_01_functions_recursion` | — | 2026-07-18T00:55:00+07:00 | — | — | — | — | 2026-07-18T00:55:00+07:00 |
| `08_02_carsharing_pandas_lr` | — | 2026-07-18T00:55:00+07:00 | 2026-07-17T01:43:52+07:00 | — | 2026-07-17T17:06:03+07:00 | — | 2026-07-18T00:55:00+07:00 |
| `08_03_titanic_eda` | 2026-07-17T18:29:04+07:00 | 2026-07-18T01:08:30+07:00 | 2026-07-17T18:29:04+07:00 | — | 2026-07-17T18:29:04+07:00 | — | 2026-07-18T01:08:30+07:00 |
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
| `design-lesson` | 2026-07-18T00:55:00+07:00 | правка «A. Чего хотим от пары» пар 1–10; канон в Lesson Design |
| `canvas-lms` | 2026-07-18T00:55:00+07:00 | wiki планов пар 1–10 `--update-page-only` |

### Примечание по `08_02_carsharing_pandas_lr`

| Skill | Время | Основание |
|---|---|---|
| `design-lesson` | 2026-07-18T00:55:00+07:00 | добавлены блоки A (1–2 абзаца) во все 10 LESSON.md |
| `test-teacher` | 2026-07-17T01:43:52+07:00 | commit `e2a8b0b` — правки пути учителя после test-teacher |
| `expert-edu-editor` | 2026-07-17T17:06:03+07:00 | commit `a6b12a3` — deepen notebooks |
| `canvas-lms` | 2026-07-18T00:55:00+07:00 | `publish_canvas_m2.py --all --update-page-only` (пары 11–20) |

### Примечание по `08_03_titanic_eda`

| Skill | Время | Основание |
|---|---|---|
| `design-module` | 2026-07-17T18:29:04+07:00 | UNIT + 9 LESSON A–E; стандартный seaborn Titanic; generate_notebooks |
| `design-lesson` | 2026-07-18T01:08:30+07:00 | добавлены блоки «A. Чего хотим от пары» (1–2 абзаца) во все 9 LESSON.md, пары 21–29 |
| `test-teacher` / `expert-edu-editor` | 2026-07-17T18:29:04+07:00 | расшифровки ЦПТ/bias; ход B; артефакт-ссылки |
| `canvas-lms` | 2026-07-18T01:08:30+07:00 | `publish_canvas_m3.py --all --update-page-only --module-id 54690` (wiki планов 21–29) |
