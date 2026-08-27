# letovo-ml-profile

Инженерная документация для проектирования профиля «Машинное обучение» (8–11 класс, школа Летово).

Операционный мануал профиля и материалы курса (модули в `modules/`).

## Документы

| Документ | Вопрос |
|---|---|
| [Foundation](docs/00_FOUNDATION.md) | Зачем существует профиль |
| [Pedagogy](docs/01_PEDAGOGY.md) | Как принимаются педагогические решения |
| [Material Design Standard](docs/02_MATERIAL_DESIGN_STANDARD.md) | Как проектируются материалы |
| [Unit Planner](docs/03_UNIT_PLANNER.md) | Как проектируется модуль |
| [Lesson Design](docs/04_LESSON_DESIGN.md) | Как проектируется урок; [полный цикл до Canvas](docs/04_LESSON_DESIGN.md#полный-цикл-от-слота-ктп-до-canvas) |
| [Notebook Standard](docs/05_NOTEBOOK_STANDARD.md) | Как проектируется ноутбук |
| [Presentation Standard](docs/06_PRESENTATION_STANDARD.md) | Как проектируется презентация |
| [KTP](docs/07_KTP.md) | Календарно-тематическое планирование года (`docs/ktp/`) |
| [Canvas LMS](docs/08_CANVAS.md) | Техническая работа с курсом в Canvas (API, права; курс 8 класса — **6465**) |

Приоритет: Foundation → Pedagogy → Material Design Standard → Unit Planner → Lesson Design → форматные стандарты.

## Справочные материалы

Папка [reference/](reference/) — внешний черновик программы и скрипт извлечения. Не является частью операционного мануала.

## Модули 8 класса

КТП: [docs/ktp/08.md](docs/ktp/08.md). Вводная пара входит в модуль 1. Статусы: **материалы** (уроки + ноутбуки + артефакт) / **план** (`UNIT.md`).

| # | Модуль | Пары КТП | Статус |
|---|---|---|---|
| 1 | [08_01_functions_recursion](modules/08_01_functions_recursion/) | 1–8 | материалы |
| 2 | [08_02_carsharing_pandas_lr](modules/08_02_carsharing_pandas_lr/) | 9–16 | материалы |
| 3 | [08_03_titanic_eda](modules/08_03_titanic_eda/) | 17–24 | материалы |
| 4 | [08_04_mnist_knn](modules/08_04_mnist_knn/) | 25–30 | материалы |
| 5 | [08_05_shop_feature_engineering](modules/08_05_shop_feature_engineering/) | 31–37 | материалы |
| 6 | [08_06_ab_startup](modules/08_06_ab_startup/) | 38–43 | материалы |
| 7 | [08_07_bank_arrays_search](modules/08_07_bank_arrays_search/) | 44–47 | материалы |
| 8 | [08_08_logistics_clustering](modules/08_08_logistics_clustering/) | 48–50 | материалы |
| 9 | [08_10_churn_logreg](modules/08_10_churn_logreg/) | 51–54 | материалы |
| 10 | [08_11_virtual_polygon](modules/08_11_virtual_polygon/) | 55–58 | материалы |
| 11 (доп.) | [08_09_courier_dp](modules/08_09_courier_dp/) | 59–63 | материалы |

## Работа с ИИ

Контекст для ИИ — [AI_CONTEXT.md](AI_CONTEXT.md). Правила — `.cursor/rules/`. Skills — [.cursor/skills/](.cursor/skills/) (модуль, урок, ML-интеграция, ревью).
