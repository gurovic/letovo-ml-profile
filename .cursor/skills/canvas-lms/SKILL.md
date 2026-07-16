---
name: canvas-lms
description: >-
  Fetches data from school Canvas LMS (canvas.letovo.ru) via API: courses,
  modules, pages, assignments, syllabus, files. Use when user mentions Canvas,
  LMS, курс в канвасе, модули Canvas, syllabus, задания, страницы курса,
  стандарт школы, or needs content from canvas.letovo.ru.
---

# Canvas LMS (Letovo)

## Секреты

- Токен и URL — **только** в `.env` (не в git).
- **Никогда** не выводить токен, не коммитить, не вставлять в skill/rules/docs.
- Шаблон переменных: `.env.example`.

| Переменная | Назначение |
|---|---|
| `CANVAS_BASE_URL` | https://canvas.letovo.ru |
| `CANVAS_API_URL` | https://canvas.letovo.ru/api/v1 |
| `CANVAS_ACCESS_TOKEN` | Bearer token |

Канон курса 8 класса и публикации пар: [docs/08_CANVAS.md](../../docs/08_CANVAS.md) (`course_id` **6465**; §11 — push → gist → Colab в Canvas). Полный цикл: [Lesson Design](../../docs/04_LESSON_DESIGN.md#полный-цикл-от-слота-ктп-до-canvas).

## Инструмент

Скрипт **`scripts/canvas_api.py`** (stdlib, без pip).

Запуск из **корня репозитория**:

```bash
python scripts/canvas_api.py self
python scripts/canvas_api.py courses
python scripts/canvas_api.py courses --search "машинное"
python scripts/canvas_api.py course COURSE_ID
python scripts/canvas_api.py modules COURSE_ID
python scripts/canvas_api.py module-items COURSE_ID MODULE_ID
python scripts/canvas_api.py pages COURSE_ID
python scripts/canvas_api.py page COURSE_ID page-url-slug --body-only
python scripts/canvas_api.py syllabus COURSE_ID --body-only
python scripts/canvas_api.py assignments COURSE_ID
python scripts/canvas_api.py files COURSE_ID
python scripts/canvas_api.py raw "courses/COURSE_ID/..." --paginate
```

Создание (по явной просьбе пользователя):

```bash
python scripts/canvas_api.py init-8ml
python scripts/canvas_api.py create-course --name "8ML" --code "8ML" --enroll-me
python scripts/canvas_api.py create-module COURSE_ID --name "Модуль 1. ..."
```

`init-8ml` идемпотентен: не дублирует курс и модуль с тем же названием.

Добавляй `--json` для полного ответа.

## Workflow: получить информацию

```
- [ ] 1. Уточнить, что нужно (курс, модуль, страница, формат школы, syllabus)
- [ ] 2. python scripts/canvas_api.py courses [--search "..."]
- [ ] 3. Зафиксировать course_id
- [ ] 4. Вызвать нужную подкоманду (modules / pages / syllabus / …)
- [ ] 5. Для HTML страниц — page --body-only; интерпретировать для задачи
- [ ] 6. Сохранить вывод в reference/ только если пользователь просит; не дублировать секреты
```

## Типовые задачи в этом репозитории

| Запрос пользователя | Действие |
|---|---|
| Формат модуля / стандарт школы в Canvas | `modules` + `module-items`; wiki `pages` |
| Программа курса ML | `courses --search`, затем `syllabus` или `pages` |
| Сверить demo-модуль с Canvas | выгрузить структуру модулей, сравнить с UNIT.md |
| Опубликовать пару в модуле | [08_CANVAS §11.3.1–11.3.2](../../docs/08_CANVAS.md): урок — ExternalUrl; ДЗ — Assignment «Домашнее задание»; план и решения скрыты |
| Unit Planner TODO «стандарт школы» | найти страницу-шаблон в Canvas, процитировать структуру |

## Canvas API (справка)

- Auth: `Authorization: Bearer <token>`
- Docs: https://canvas.instructure.com/doc/api/
- Пагинация: скрипт следует `Link: rel="next"` при `--paginate` / list-командах
- Права: token видит только доступные пользователю курсы

## Ограничения

- Создание/изменение курсов — только по явной просьбе; команды `create-course`, `create-module`, `init-8ml`.
- Не скачивать бинарные файлы без запроса (список — `files`).
- HTML из pages — сырой; для решений опираться на смысл, не копировать разметку слепо.

## Ошибки

| Симптом | Действие |
|---|---|
| 401 Unauthorized | токен в `.env`; перевыпустить в Canvas |
| 404 | неверный course_id или slug страницы |
| Пустой courses | расширить search или проверить доступ token |

## Связь с другими skills

- Контент для модуля → `design-module`, `design-lesson`
- Сверка качества → `review-edu-material`
- Шаблон Unit Planner «стандарт школы» → выгрузка из Canvas + правка UNIT.md

## После получения данных

Кратко: course_id, что выгрузили, как используете в задаче. Не вставлять длинный HTML в чат — только релевантные фрагменты.
