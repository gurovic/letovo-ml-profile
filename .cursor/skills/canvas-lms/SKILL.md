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
- Шаблон переменных: `.env.example`. Канон выпуска токена: [docs/08_CANVAS.md](../../docs/08_CANVAS.md) §2.

| Переменная | Назначение |
|---|---|
| `CANVAS_BASE_URL` | https://canvas.letovo.ru |
| `CANVAS_API_URL` | https://canvas.letovo.ru/api/v1 |
| `CANVAS_ACCESS_TOKEN` | Bearer token (Personal Access Token) |

Канон курса 8 класса и публикации пар: [docs/08_CANVAS.md](../../docs/08_CANVAS.md) (`course_id` **6465**; §11 — push → gist → Colab в Canvas). Полный цикл: [Lesson Design](../../docs/04_LESSON_DESIGN.md#полный-цикл-от-слота-ктп-до-canvas).

## Обязательный preflight (не пропускать)

Перед **любой** записью в Canvas (publish, put item, wiki, assignment) и перед длинной сессией чтения:

```bash
python scripts/canvas_api.py self
```

| Результат | Действие агента |
|---|---|
| JSON с `id`, `name` | Продолжать |
| `401` / `AUTH_401_HINT` | **Остановиться.** Не публиковать «частично». Сообщить пользователю: обновить токен в Canvas **без короткого expires** → вставить в `.env` → снова `self`. Не угадывать токен и не просить прислать его в чат. |

`publish_canvas_lesson.py` / `publish_canvas_m2.py` сами вызывают `require_canvas_auth()`; если preflight упал — сначала починить `.env`, потом повторить команду.

### Почему бывает 401 «уже обновляли токен»

1. У токена истёк `expires_at` (короткий срок при создании).
2. В UI нажали **Regenerate** / создали новый — старое значение в `.env` сразу мёртво.
3. Команда агента в **sandbox** не читает gitignored `.env` и берёт устаревший `CANVAS_ACCESS_TOKEN` из окружения.

### Запуск агентом

- Рабочая директория — **корень репозитория**.
- Для Canvas API / publish: `required_permissions: ["all"]` (доступ к `.env` + сеть). Не полагаться на sandbox-default для gitignored secrets.
- В логе (`CANVAS_API_DEBUG=1`) смотреть `CANVAS auth source=file:.env` vs `env:CANVAS_ACCESS_TOKEN` — без печати самого токена.

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
- [ ] 2. python scripts/canvas_api.py self   # preflight
- [ ] 3. python scripts/canvas_api.py courses [--search "..."]
- [ ] 4. Зафиксировать course_id
- [ ] 5. Вызвать нужную подкоманду (modules / pages / syllabus / …)
- [ ] 6. Для HTML страниц — page --body-only; интерпретировать для задачи
- [ ] 7. Сохранить вывод в reference/ только если пользователь просит; не дублировать секреты
```

## Типовые задачи в этом репозитории

| Запрос пользователя | Действие |
|---|---|
| Формат модуля / стандарт школы в Canvas | `self` → `modules` + `module-items`; wiki `pages` |
| Программа курса ML | `courses --search`, затем `syllabus` или `pages` |
| Сверить demo-модуль с Canvas | выгрузить структуру модулей, сравнить с UNIT.md |
| Опубликовать пару в модуле | `self` → [08_CANVAS §11](../../docs/08_CANVAS.md): урок — ExternalUrl; ДЗ — Assignment; план и решения скрыты |
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
| 401 Unauthorized | Остановиться; чек-лист §2 в `08_CANVAS.md` / `AUTH_401_HINT`; не публиковать дальше |
| 404 | неверный course_id или slug страницы |
| Пустой courses | расширить search или проверить доступ token |
| `CANVAS_ACCESS_TOKEN not found` + намёк на sandbox | перезапуск с `permissions: all` из корня репо |

## Связь с другими skills

- Контент для модуля → `design-module`, `design-lesson`
- Сверка качества → `review-edu-material`
- Шаблон Unit Planner «стандарт школы» → выгрузка из Canvas + правка UNIT.md

## После получения данных

Кратко: course_id, что выгрузили, как используете в задаче. Не вставлять длинный HTML в чат — только релевантные фрагменты.
