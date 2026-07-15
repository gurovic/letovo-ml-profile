# Canvas LMS — техническая работа с курсом

**Вопрос документа:** как подключиться к школьному Canvas, какие команды и ограничения API действуют для профиля ML.

Педагогика размещения материалов в Canvas — в [Lesson Design](04_LESSON_DESIGN.md) (поле Canvas в зоне A и §13). Школьный unit planner — маппинг в [Unit Planner §20](03_UNIT_PLANNER.md). Здесь только инфраструктура и API.

---

## 1. Инстанс

| Параметр | Значение |
|---|---|
| Веб | https://canvas.letovo.ru |
| API | https://canvas.letovo.ru/api/v1 |
| Документация API | https://canvas.instructure.com/doc/api/ |
| Авторизация | `Authorization: Bearer <token>` |

---

## 2. Секреты и конфигурация

Файл **`.env`** в корне репозитория (в `.gitignore`, не коммитить). Шаблон — `.env.example`.

| Переменная | Назначение |
|---|---|
| `CANVAS_BASE_URL` | https://canvas.letovo.ru |
| `CANVAS_API_URL` | https://canvas.letovo.ru/api/v1 |
| `CANVAS_ACCESS_TOKEN` | Personal access token пользователя Canvas |
| `CANVAS_ACCOUNT_ID` | ID подаккаунта для `create-course` (см. §4) |
| `CANVAS_COURSE_ID_08` | ID курса 8 класса в Canvas (**6465**) — опционально для скриптов |

**Проверка токена (чтение):**

```bash
python scripts/canvas_api.py self
```

Успех — JSON с `id`, `name`. Ошибка `401 Invalid access token` — перевыпустить токен в Canvas: **Настройки → Утверждённые интеграции → New Access Token**.

**Безопасность:** не вставлять токен в чат, skills, rules, docs, git. После утечки — перевыпуск.

---

## 3. Инструмент: `scripts/canvas_api.py`

Stdlib, без pip. Запуск из **корня репозитория**.

### 3.1. Чтение

| Команда | Назначение |
|---|---|
| `self` | Текущий пользователь API |
| `courses [--search TERM] [--json]` | Список курсов с активной записью |
| `course COURSE_ID` | Детали курса |
| `modules COURSE_ID` | Модули курса |
| `module-items COURSE_ID MODULE_ID` | Элементы модуля |
| `pages COURSE_ID` | Wiki-страницы |
| `page COURSE_ID slug [--body-only]` | Одна страница |
| `syllabus COURSE_ID [--body-only]` | Syllabus |
| `assignments COURSE_ID` | Задания |
| `files COURSE_ID` | Файлы курса |
| `folders COURSE_ID` | Папки |
| `accounts` | Подаккаунты для создания курсов |
| `raw PATH [--param k=v] [--paginate]` | Произвольный GET под `/api/v1/` |

Флаг `--json` — полный ответ API.

### 3.2. Создание (только по явной задаче)

| Команда | Назначение |
|---|---|
| `create-course --name N --code C [--account-id ID] [--enroll-me]` | Новый курс в подаккаунте |
| `create-module COURSE_ID --name N [--position P]` | Пустой модуль |
| `init-8ml [--account-id ID] [--module-name N]` | Курс `8ML` + модуль 1 (идемпотентно) |

Скрипт поддерживает GET и POST. PUT/DELETE — через `raw` или доработку скрипта при необходимости.

### 3.3. Пагинация

Списочные команды и `raw --paginate` следуют заголовку `Link: rel="next"`.

---

## 4. Права и подаккаунты (обнаружено на Letovo)

### 4.1. Токен преподавателя

| Эндпоинт / действие | Результат |
|---|---|
| `GET users/self` | Работает |
| `GET courses` (свои курсы) | Работает |
| `GET accounts` | **Пустой массив `[]`** — список подаккаунтов недоступен |
| `GET accounts/6/courses` | **403** |
| `POST accounts/6/courses` | **Работает** при указании `CANVAS_ACCOUNT_ID=6` |
| `course[enroll_me]=true` при создании | Курс создаётся, но **запись преподавателем не гарантирована** |
| `GET/POST courses/:id/...` без записи | **403** unauthorized |
| `POST courses/:id/enrollments` (самозапись) | **403** |

**Вывод:** создание курса через API возможно, но без роли учителя в курсе дальнейшие операции (модули, страницы) недоступны. Нужна ручная запись через Canvas UI или админ.

### 4.2. Подаккаунт IT

Курсы преподавателя IT в выборке имеют `account_id: 6`, `root_account_id: 1`.

Для `create-course` задать в `.env`:

```
CANVAS_ACCOUNT_ID=6
```

Если `accounts` пуст и `CANVAS_ACCOUNT_ID` не задан — скрипт завершится с ошибкой `no Canvas accounts available`.

### 4.3. Учебные периоды

Новый курс через API может получить `enrollment_term_id: 1` (не текущий год). Курсы 2025/26 в выборке — `enrollment_term_id: 15`. При проблемах с видимостью — сверить период в настройках курса в UI.

---

## 5. Курс 8 класса (профиль ML)

**Канонический `course_id`:** **6465** — рабочий курс для публикации материалов 8 класса.

| Поле | Значение |
|---|---|
| `course_id` | **6465** |
| `name` | `ML: 8` |
| `course_code` | `ML: 8` |
| `account_id` | 3 |
| `workflow_state` | `unpublished` |
| Запись API-пользователя | Учитель (TeacherEnrollment) |
| URL | https://canvas.letovo.ru/courses/6465 |

Модули на момент фиксации: модуль 1 создан (`module_id` **54688**), элементов нет.

**Модуль 1 (плановое имя):** `Модуль 1. Оценка недвижимости: функции и inference pipeline` — из [КТП 8 класса](ktp/08.md).

### 5.1. Создать модуль 1

```bash
python scripts/canvas_api.py create-module 6465 --name "Модуль 1. Оценка недвижимости: функции и inference pipeline"
```

Проверка:

```bash
python scripts/canvas_api.py modules 6465
```

### 5.2. Фиксация ID в репозитории

| Сущность | Canvas ID |
|---|---|
| Курс 8 класса (`ML: 8`) | **6465** |
| Модуль 1 | **54688** |

Опционально в `.env` (для скриптов):

```
CANVAS_COURSE_ID_08=6465
```

### 5.3. Черновик `8ML` (6464) — не использовать

При первой настройке API был создан курс `8ML` (`course_id` **6464**, `account_id` 6) без автоматической записи преподавателя. Доступ к нему через API — **403**. Канонический курс — **6465**; дубликат 6464 можно удалить или оставить неиспользуемым через админку Canvas.

Команда `init-8ml` в скрипте ориентирована на код `8ML` и **не** соответствует текущему курсу `ML: 8`. Для 6465 использовать `create-module` напрямую (см. §5.1).

---

## 6. Смежные курсы IT (справочно)

Полезны для сверки формата модулей и страниц школы. ID из API (запись преподавателя).

| course_id | course_code | Назначение |
|---|---|---|
| 5782 | IT-8-0 | IT: профиль 8 |
| 6081 | IT-ML | IT: ML (текущий год) |
| 5600 | IT: 11. ML | IT: 11, блок ML |

Поиск:

```bash
python scripts/canvas_api.py courses --search "ML"
```

---

## 7. Типовые сценарии

### 7.1. Сверить структуру с `UNIT.md`

```bash
python scripts/canvas_api.py modules COURSE_ID
python scripts/canvas_api.py module-items COURSE_ID MODULE_ID
```

Сравнить названия модулей и типы элементов с §11 `UNIT.md` и последовательностью пар КТП.

### 7.2. Шаблон оформления модуля в школе

```bash
python scripts/canvas_api.py pages COURSE_ID
python scripts/canvas_api.py page COURSE_ID page-slug --body-only
```

HTML — сырой; для решений извлекать структуру, не копировать разметку слепо.

### 7.3. Непубликованные курсы в списке

```bash
python scripts/canvas_api.py raw courses --param enrollment_type=teacher --param "state[]=unpublished" --param "state[]=available"
```

### 7.4. Опубликовать пару в модуле

См. **§11** — канон структуры урока, видимости и пайплайна ноутбуков (push → gist).

---

## 8. Ошибки

| Код | Смысл | Действие |
|---|---|---|
| 401 | Неверный или просроченный токен | Перевыпустить, обновить `.env` |
| 403 | Нет прав на объект | Проверить запись в курс; не полагаться на `enroll_me` |
| 404 | Неверный `course_id` или slug страницы | `courses --search` |
| Пустой `courses` | Нет записи или другой search | Расширить поиск; проверить `enrollment_state` |
| `no Canvas accounts available` | Пустой `accounts` и нет `CANVAS_ACCOUNT_ID` | Задать `CANVAS_ACCOUNT_ID=6` |

---

## 9. Связь с остальной системой

| Документ / артефакт | Связь |
|---|---|
| [Lesson Design §13](04_LESSON_DESIGN.md) | Поле Canvas в карточке урока (экспорт) |
| [Unit Planner §20](03_UNIT_PLANNER.md) | Опционально Canvas ID модуля/урока |
| [reference/SCHOOL_UNIT_PLANNER.md](../reference/SCHOOL_UNIT_PLANNER.md) | Школьная форма (только чтение) |
| `.cursor/skills/canvas-lms/SKILL.md` | Skill для ИИ: когда вызывать API |
| `.env.example` | Шаблон переменных |

**Правило:** в `reference/` не писать. Канон по Canvas для репозитория — этот файл + `scripts/canvas_api.py`.

---

## 10. Чек-лист перед публикацией модуля

- [ ] `python scripts/canvas_api.py self` — токен валиден
- [ ] Известен `course_id` курса 8 класса (**6465**, `ML: 8`)
- [ ] Есть роль учителя в курсе (модули открываются без 403)
- [ ] Модуль Canvas создан; имя согласовано с КТП / `UNIT.md`
- [ ] `course_id` / `module_id` зафиксированы при необходимости автоматизации
- [ ] Пары внутри модуля — по **§11** (push → gist → Canvas)
- [ ] Токен не светился в git и публичных каналах

---

## 11. Пара (урок) внутри модуля Canvas

Канон размещения материалов одной пары КТП в модуле курса.

Репозиторий — **источник правды**; Canvas — витрина для класса. Порядок действий фиксирован: сначала коммит и **push**, затем gist для ноутбуков, затем элементы в Canvas.

### 11.1. Иерархия

```
Курс (6465, ML: 8)
└── Модуль N  (напр. 54688 — «Модуль 1. …»)
    └── Подмодуль «Пара K»  (номер и краткое имя из LESSON.md / КТП)
        ├── LESSON.md          — только учитель
        ├── lesson.ipynb       — ученики (внешняя ссылка)
        └── homework.ipynb     — ученики (внешняя ссылка), если есть
```

**Подмодуль** в Canvas = вложенный module item типа `SubHeader` + дочерние элементы **или** отдельный дочерний модуль (оба варианта допустимы; в Letovo чаще плоский список с префиксом «Пара K» в названии элементов).

Имя подмодуля / блока: **`Пара K. <краткое название>`** — как в зоне A `LESSON.md` (поле «Название урока»).

### 11.2. Видимость материалов

| Файл репозитория | Кто видит | В Canvas |
|---|---|---|
| `LESSON.md` | **Только учитель** | Wiki-страница или файл курса; элемент модуля **не опубликован** («скрыт от студентов») |
| `lesson.ipynb` | **Ученики** | Внешняя ссылка (External URL); элемент **опубликован** |
| `homework.ipynb` | **Ученики** | Внешняя ссылка (External URL); элемент **опубликован** |

**Не опубликован** в Canvas: учитель видит элемент (серый, перечёркнутый глаз); ученики — нет. Это и есть «скрытый LESSON.md».

Ноутбуки **не** загружать файлом в Canvas на этом этапе — только ссылка на gist (см. §11.3).

### 11.3. Пайплайн ноутбуков: push → gist → Canvas

Обязательная последовательность:

| Шаг | Действие |
|---|---|
| 1 | Материалы готовы в `modules/…/lessons/<NN>_*/` |
| 2 | **Commit + `git push`** в `origin` ([github.com/gurovic/letovo-ml-profile](https://github.com/gurovic/letovo-ml-profile)) |
| 3 | Для каждого `.ipynb` — **GitHub Gist** с содержимым из запушенной версии |
| 4 | В Canvas — элемент **Внешний URL** на gist; для просмотра в браузере предпочтительно **nbviewer** |

**Почему push перед gist:** gist должен соответствовать зафиксированной в git версии; при правках — новый push, обновить gist (новый revision или новый gist), обновить ссылку в Canvas.

**Форматы ссылок (примеры):**

| Назначение | URL |
|---|---|
| Gist (raw) | `https://gist.githubusercontent.com/{user}/{gist_id}/raw/{revision}/lesson.ipynb` |
| Nbviewer | `https://nbviewer.org/gist/{user}/{gist_id}` |

Имя элемента в Canvas: `lesson.ipynb` / `homework.ipynb` или с пояснением (`Ноутбук урока`, `Домашнее задание`).

**Инструменты gist (на выбор):** веб-интерфейс gist.github.com; `gh gist create file.ipynb --public`. Токены gist — в `.env`, не в docs.

### 11.4. LESSON.md в Canvas

| Способ | Когда |
|---|---|
| Wiki-страница курса + элемент модуля (не опубликован) | Предпочтительно: содержимое `LESSON.md` в теле страницы, slug вида `m1-p2-lesson` |
| Файл `.md` в Files + элемент модуля (не опубликован) | Если нужен скачиваемый файл |

Источник текста — всегда `LESSON.md` из репозитория. После правок в git — обновить страницу в Canvas вручную или через API (пока не автоматизировано).

### 11.5. Эталон: пара 2, модуль 1

| Поле | Значение |
|---|---|
| Курс | `6465` (`ML: 8`) |
| Модуль Canvas | `54688` |
| Пара КТП | **2** |
| Путь в репо | `modules/08_01_functions_recursion/lessons/02_function_as_mapping/` |
| Файлы | `LESSON.md`, `lesson.ipynb`, `homework.ipynb` |
| Название в Canvas | `Пара 2. Функция-предсказатель: от правила к выбору модели` |

**Целевая структура в модуле 54688:**

| # | Элемент Canvas | Тип | Опубликован |
|---|---|---|---|
| 1 | `Пара 2. Функция-предсказатель…` | SubHeader или Text Header | — |
| 2 | `LESSON.md` (план пары) | Page / File | **Нет** |
| 3 | `lesson.ipynb` | External URL → gist / nbviewer | **Да** |
| 4 | `homework.ipynb` | External URL → gist / nbviewer | **Да** |

Canvas ID подмодуля / элементов — фиксировать здесь после создания:

| Сущность | Canvas ID |
|---|---|
| Пара 2 (подмодуль / блок) | *(заполнить)* |
| LESSON.md (элемент) | *(заполнить)* |
| lesson.ipynb (элемент) | *(заполнить)* |
| homework.ipynb (элемент) | *(заполнить)* |
| Gist `lesson.ipynb` | *(заполнить после push)* |
| Gist `homework.ipynb` | *(заполнить после push)* |

### 11.6. Чек-лист публикации одной пары

- [ ] `LESSON.md`, `lesson.ipynb`, `homework.ipynb` согласованы с [Lesson Design](04_LESSON_DESIGN.md)
- [ ] `git push origin main` (или рабочая ветка, влитая в main)
- [ ] Gist создан для каждого ноутбука; ссылки проверены в nbviewer
- [ ] В модуле Canvas — блок «Пара K»; `LESSON.md` скрыт от учеников
- [ ] Ноутбуки — опубликованные внешние ссылки
- [ ] ID и gist-URL записаны в §11.5 (или в `LESSON.md` / `UNIT.md` при необходимости)
- [ ] Поле **Canvas** в зоне A `LESSON.md` обновлено (что выложено, не `—`)
