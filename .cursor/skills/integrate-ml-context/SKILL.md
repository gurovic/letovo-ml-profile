---
name: integrate-ml-context
description: >-
  Усиливает data/ML-контекст в существующем модуле: сквозной датасет,
  describe/transform/predict, артефакт, ноутбуки. Use when integrating ML
  context, data examples, EDA preview, sklearn bridge, «притянуть ML»,
  «data/ML в модуль», or refactoring demo module content.
---

# Интеграция data/ML в модуль

## Роль

Не добавлять ML «для галочки». Каждая data-активность закрывает **конкретную** способность из UNIT.md или готовит к модулю 8 класса (pandas/sklearn).

## Когда применять

- модуль уже есть (UNIT + уроки), но контекст абстрактный;
- программный модуль в профиле ML без связи с данными;
- демо-модуль нужно усилить перед ревью.

**Не применять:** если модуль вне профиля или Foundation §7 не предполагает data/ML на этом этапе.

## Обязательные документы

| Документ | Зачем |
|---|---|
| `docs/00_FOUNDATION.md` §7 | что уместно в классе |
| `reference/COURSE_PROGRAM_DRAFT.md` | черновик тем класса (reference only) |
| `modules/.../UNIT.md` | цель, scope, результаты |
| skill `design-module` | структура папок |

Эталон агрессивной интеграции: `modules/08_functions_recursion/`.

## Три сквозные линии

В каждом модуле проверить покрытие:

| Линия | Смысл | Примеры функций/активностей |
|---|---|---|
| **describe** | proto-EDA | `describe_numbers`, `grade_stats`, частоты |
| **transform** | preprocessing | `min_max_scale`, `filter`, pipeline-шаги |
| **predict** | модель как функция | `predict_*`, `accuracy`, `naive_classify` |

Минимум **одна активность на линию** по модулю (урок или артефакт).

## Workflow

```
- [ ] 1. Прочитать UNIT.md: цель, вне scope, класс
- [ ] 2. Выбрать 1 сквозной микро-датасет (см. ниже)
- [ ] 3. Создать/обновить data/module_datasets.py + data/README.md
- [ ] 4. Пройти уроки: где заменить абстрактные x,y на данные
- [ ] 5. Добавить ML-мотивацию в LESSON.md §5 (конкретно, 1–2 предложения)
- [ ] 6. Обновить ноутбуки (generate_notebooks.py → пересборка)
- [ ] 7. Усилить артефакт модуля data/ML-смыслом
- [ ] 8. Обновить UNIT.md §3, §5, §9 — без дублирования MDS
- [ ] 9. Ревью: skill review-edu-material
```

## Выбор сквозного датасета

Один сюжет на весь модуль. Подобрать по теме:

| Тема модуля | Датасет | ML-мост |
|---|---|---|
| Функции, Python | квартиры area→price | регрессия, MAE |
| Функции | exam scores | порог класса, метрики |
| Структуры данных | вложенный API / JSON | flatten, extract |
| Текст, строки | positive/negative отзывы | bag-of-words |
| Алгоритмы | отсортированные признаки | binary search |

Данные: **списки и словари**, без pandas/csv в этом skill (следующий модуль).

## Уровни интеграции

| Уровень | Что делаем |
|---|---|
| **Лёгкий** | §5 профконтекст + 1 пример на реальных числах |
| **Средний** | сквозной датасет + describe/transform в 2 уроках |
| **Агрессивный** | 3 линии + pipeline + артефакт с classify/метрикой |

Пользователь просит «агрессивно» → средний + predict/pipeline + артефакт.

## Что можно / нельзя тянуть

| Можно | Нельзя (вне scope модуля) |
|---|---|
| f(x), predict вручную | sklearn `fit` |
| MAE, accuracy, confusion | train/test split |
| min-max scale, filter | pandas, CSV |
| Pipeline из функций | TF-IDF, embeddings |
| «Позже будет sklearn Pipeline» — 1 абзац | полноценный EDA-модуль |

## Изменения по файлам

| Файл | Действие |
|---|---|
| `data/module_datasets.py` | константы датасетов |
| `data/README.md` | таблица: датасет → урок → ML-смысл |
| `UNIT.md` | §3 мотивация, §5 результаты, §9 уроки |
| `lessons/*/LESSON.md` | §5, §8, data в активностях |
| `lessons/*/slides.md` | data-контекст на слайде 1 |
| `generate_notebooks.py` | импорт data, ML-примеры |
| `artifact/PROJECT.md` | ML-смысл артефакта |

## Правила

- Не ломать «одна центральная идея урока» ради ML.
- Не дублировать содержание будущих модулей pandas/sklearn.
- Терминология: `.cursor/rules/02_Терминология.mdc`.
- Сообщить пользователю, если интеграция требует изменения Foundation/Pedagogy.

## После завершения

Краткий отчёт:

1. какой датасет и почему;
2. какие уроки затронуты;
3. покрытие describe / transform / predict;
4. что осталось вне scope.
