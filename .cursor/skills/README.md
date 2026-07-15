# Skills проекта

Процедурные playbook'и для агента. **Правила** — в `.cursor/rules/`; **предметная правда** — в `docs/`.

| Skill | Когда использовать |
|---|---|
| [design-module](design-module/SKILL.md) | новый или переработка модуля → `UNIT.md` |
| [design-lesson](design-lesson/SKILL.md) | урок → `LESSON.md` + ноутбук/слайды |
| [integrate-ml-context](integrate-ml-context/SKILL.md) | усилить data/ML в существующем модуле |
| [canvas-lms](canvas-lms/SKILL.md) | данные из Canvas LMS (canvas.letovo.ru) |
| [review-edu-material](review-edu-material/SKILL.md) | ревью перед публикацией или после демо |
| [refine-md-fragment](refine-md-fragment/SKILL.md) | доработка выделенного фрагмента `.md` |
| [expert-edu-editor](expert-edu-editor/SKILL.md) | итеративная доводка материалов до качества (редактор-эксперт) |
| [test-teacher](test-teacher/SKILL.md) | прогон глазами преподавателя: вопросы → сразу правки в материалах |

В чате: «используй skill design-module» или опишите задачу — агент подберёт по description.

## Доработка фрагмента в preview

1. Выделить текст в preview **в Agent-окне** (или в исходнике `.md` в обычном окне).
2. **Ctrl+L** → добавить в чат.
3. **`/refine-md`** → агент пояснит и поправит исходный файл.

Подробнее: `.cursor/rules/06_Доработка_md.mdc`, команда `.cursor/commands/refine-md.md`.

## Редактор-эксперт (полная доводка)

`/polish-material` или skill **expert-edu-editor** — правки в цикле до ворот: педагогика, наука, инженерия, ясность для учителя, без воды, без забегания вперёд, уровень одарённых; халтура → перепроектировать.

Эталон: `modules/08_01_functions_recursion/`.

## Прогон тестового учителя

`/test-teacher` или skill **test-teacher** — преподаватель **без инсайдерского сленга** читает `UNIT` / `LESSON` / ноутбуки, задаёт вопросы «что делать на паре»; агент **сразу** отвечает правками. Затем при необходимости — `expert-edu-editor` (канон и качество).
