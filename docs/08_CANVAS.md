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
| `publish_canvas_lesson.py` | Пара в модуль: `--pair N`, wiki (MD→HTML) + элементы; `--update-page-only` — только wiki |
| `upload_lesson_gist.py` | Gist из `lesson.ipynb` / `homework.ipynb` / `solutions.ipynb` → JSON с Colab URL |
| `lesson_md_html.py` | MD → HTML для Canvas wiki |

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

Канон размещения материалов одной пары КТП в модуле курса. Предшествующие фазы проектирования — [Lesson Design: полный цикл](04_LESSON_DESIGN.md#полный-цикл-от-слота-ктп-до-canvas).

Репозиторий — **источник правды**; Canvas — витрина для класса. Порядок: commit → для **ноутбуков** gist/Colab → для **документов** (`.md` и стартовый код) — wiki-страницы курса (MD→HTML). **Не** ссылаться на `github.com/.../letovo-ml-profile` в материалах для учеников; gist — только для `.ipynb`.

### 11.1. Иерархия

```
Курс (6465, ML: 8)
└── Модуль N  (напр. 54688 — «Модуль 1. …»)
    └── Подмодуль «Пара K»  (номер и краткое имя из LESSON.md / КТП)
        ├── LESSON.md          — только учитель
        ├── solutions.ipynb    — только учитель
        ├── lesson.ipynb       — ученики (ExternalUrl → Colab)
        └── homework.ipynb     — ученики (Assignment «Домашнее задание»: ссылка на Colab + сдача .ipynb)
```

**Подмодуль** в Canvas = вложенный module item типа `SubHeader` + дочерние элементы **или** отдельный дочерний модуль (оба варианта допустимы; в Letovo чаще плоский список с префиксом «Пара K» в названии элементов).

Имя подмодуля / блока: **`Пара K. <краткое название>`** — как в зоне A `LESSON.md` (поле «Название урока»).

**Названия элементов — человеческие, не имена файлов.** Ученик и учитель видят русские названия, а не `lesson.ipynb` / `LESSON.md`.

| Элемент | Название в Canvas |
|---|---|
| План пары (элемент модуля) | **`План урока (для преподавателя)`** — без «Пара K» в названии; номер пары уже в SubHeader |
| Решения | **`Решения (для преподавателя)`** |
| Ноутбук урока | `Ноутбук урока` |
| Домашнее задание | **`Домашнее задание`** (Assignment; не отдельный ExternalUrl) |
| Материалы артефакта | **`Материалы артефакта`** (Page-хаб; пары 9–10) |
| Задание / шаги / код | **`Задание: text_stats`**, **`Как делать (шаги)`** (wiki); **`Стартовый код (zip)`** — File `text_stats_starter.zip` |
| Сдача артефакта | **`Сдача артефакта text_stats`** (Assignment; только пара 10) |

Номер пары — только в SubHeader (`Пара K. …`). У остальных элементов списка **не** дублировать «Пара K».

**Нет Assignment «Домашнее задание»** у пар **1** (ориентация) и **9–10** (артефакт). После элемента сдачи артефакта (конец модуля) **не** ставить ДЗ — сдача на паре 10, дальше домашнего задания модуля нет.

Для Page-элемента: `module_item[title]` задавать явно (`План урока (для преподавателя)`). Заголовок wiki (`wiki_page[title]`) можно оставить длиннее; **не** переименовывать wiki после публикации без необходимости — slug привязан к названию страницы.

### 11.2. Видимость материалов

| Файл репозитория | Кто видит | В Canvas |
|---|---|---|
| `LESSON.md` | **Только учитель** | Wiki-страница или файл курса; элемент модуля **не опубликован** («скрыт от студентов») |
| `lesson.ipynb` | **Ученики** | ExternalUrl → Colab; элемент **опубликован** |
| `homework.ipynb` | **Ученики** | **Assignment** «Домашнее задание»: ссылка на Colab в описании + загрузка `.ipynb`; **без** отдельного ExternalUrl в модуле |
| `solutions.ipynb` | **Только учитель** | ExternalUrl → Colab; элемент **не опубликован** |

**Не опубликован** в Canvas: учитель видит элемент (серый, перечёркнутый глаз); ученики — нет. Это и есть «скрытый LESSON.md».

Ноутбуки **не** загружать файлом в Canvas на этом этапе — только ссылка на gist (см. §11.3).

### 11.3. Пайплайн ноутбуков: push → gist → Canvas

Обязательная последовательность:

| Шаг | Действие |
|---|---|
| 1 | Материалы готовы в `modules/…/lessons/<NN>_*/` |
| 2 | **Commit + `git push`** в `origin` ([github.com/gurovic/letovo-ml-profile](https://github.com/gurovic/letovo-ml-profile)) |
| 3 | Для каждого `.ipynb` — **GitHub Gist** с содержимым из запушенной версии |
| 4 | В Canvas — `lesson.ipynb` как **ExternalUrl** → Colab; `homework.ipynb` — **Assignment** (§11.3.2) |

**Почему push перед gist:** gist должен соответствовать зафиксированной в git версии; при правках — новый push, обновить gist (новый revision или новый gist), обновить ссылку в Canvas.

**Форматы ссылок (примеры):**

| Назначение | URL |
|---|---|
| Gist (исходник) | `https://gist.github.com/{user}/{gist_id}` |
| **Google Colab** (для Canvas) | `https://colab.research.google.com/gist/{user}/{gist_id}/{filename}.ipynb` |

**Не использовать** nbviewer — ученик работает в Colab, не в просмотрщике.

Название элемента урока — `Ноутбук урока` (§11.1). ДЗ — только Assignment `Домашнее задание`.

**Инструменты gist (на выбор):** веб-интерфейс gist.github.com; `gh gist create file.ipynb --public`. Токены gist — в `.env`, не в docs.

### 11.3.1. Ноутбук урока: External URL + Colab

**Только `lesson.ipynb`.** `homework.ipynb` в модуле **не** выкладывать отдельным ExternalUrl — см. §11.3.2.

| Параметр | Значение |
|---|---|
| Тип элемента модуля | `ExternalUrl` |
| URL | `https://colab.research.google.com/gist/{user}/{gist_id}/lesson.ipynb` |
| Название | `Ноутбук урока` |
| Опубликован | **да** |
| `new_tab` | **да** |

**Поведение для ученика**

1. Клик по элементу в модуле → **промежуточная страница Canvas** («откройте в новом окне» / ссылка на Colab).
2. Colab открывается в **новой вкладке** (при `new_tab=true`).

Промежуточную страницу **не считать ошибкой**: у External URL в Canvas нет режима «сразу уйти на внешний сайт без промежуточного экрана». Instructure оставляет её для навигации «предыдущий / следующий» по модулю.

**API (при публикации через скрипт):**

```python
{
    "module_item[type]": "ExternalUrl",
    "module_item[external_url]": "https://colab.research.google.com/gist/.../lesson.ipynb",
    "module_item[new_tab]": "true",
    "module_item[published]": "true",
}
```

**Не использовать:** nbviewer; имена файлов в заголовках элементов (`lesson.ipynb`).

**Альтернатива (не принята):** wiki-страница со ссылкой `<a target="_blank">` — Colab без промежуточного экрана, но теряется prev/next в модуле и единообразие структуры пары.

### 11.3.2. Домашнее задание: Assignment

**Канон:** сразу после «Ноутбук урока» — один элемент **`Домашнее задание`** типа **Assignment**. Отдельного ExternalUrl на `homework.ipynb` в модуле **нет**.

**Исключения (ДЗ не создавать):** пара **1** (ориентация); пары **9–10** (артефакт). После «Сдача артефакта…» в модуле больше ничего не добавлять.

| Параметр | Значение |
|---|---|
| Тип элемента модуля | `Assignment` |
| Название задания и элемента | **`Домашнее задание`** |
| Опубликован | **да** |
| Описание | Ссылка на Colab с `homework.ipynb` + инструкция сдать `.ipynb` |
| Тип сдачи | `online_upload` |
| Формат файла | `.ipynb` |
| Баллы | `1` (формирующее; при необходимости меняет учитель) |

**Порядок для ученика:** (1) ноутбук урока → (2) домашнее задание (открыть Colab из описания → сдать файл).

**API:**

```python
canvas_post(f"courses/{course_id}/assignments", {
    "assignment[name]": "Домашнее задание",
    "assignment[description]": "<a href=...>Открыть ноутбук с заданием в Colab</a>...",
    "assignment[submission_types][]": "online_upload",
    "assignment[allowed_extensions][]": "ipynb",
    "assignment[published]": "true",
    "assignment[points_possible]": "1",
})

canvas_post(f"courses/{course_id}/modules/{module_id}/items", {
    "module_item[title]": "Домашнее задание",
    "module_item[type]": "Assignment",
    "module_item[content_id]": str(assignment_id),
    "module_item[published]": "true",
})
```

Добавить к уже опубликованной паре:

```bash
python scripts/publish_canvas_lesson.py --add-homework-assignment
```

Миграция со старой схемы (ExternalUrl + «Сдача домашнего задания») — пара 2:

```bash
python scripts/publish_canvas_lesson.py --migrate-homework-layout
```

Источник — `LESSON.md` из репозитория. В Canvas wiki **не** вставлять сырой текст в `<pre>`: страница показывает **отрендеренный Markdown** (заголовки, таблицы, списки).

**Для учителя на уроке (не весь файл):** при публикации плана скрипт оставляет зоны **A–C** (сценарий, ход, если сбились) и убирает **D** (проектирование) и **E** (§13, школьный экспорт). Поле «Canvas» с ID/gist заменяется короткой строкой «В модуле». Полный `LESSON.md` остаётся в репозитории.

| Способ | Когда |
|---|---|
| Wiki-страница + элемент модуля (не опубликован) | **Предпочтительно:** MD → HTML при публикации |
| Файл `.md` в Files + элемент модуля (не опубликован) | Только если нужен скачиваемый файл (Canvas **не** рендерит MD из Files) |

**Рендер MD → HTML**

1. Установить зависимость (один раз): `pip install -r scripts/requirements.txt`
2. Конвертация: `scripts/lesson_md_html.py` (библиотека `markdown`, расширения `tables`, `fenced_code`)
3. Таблицы — с **видимой разлиновкой**: бордюры задаются **инлайн** на `<table>/<th>/<td>` (Canvas вырезает `<style>`), заголовок с фоном
4. Относительные ссылки `[…](lesson.ipynb)` / `[…](homework.ipynb)` в `LESSON.md` при публикации **переписываются** на Colab-URL (в репозитории оставлять относительные — для работы в git)
5. Тело wiki — HTML в обёртке `<div class="user_content lesson-md-content">…</div>`

**Slug и название страницы**

- Название wiki — человеческое: `Пара K — план урока (для преподавателя)`.
- Canvas формирует slug из названия; при **переименовании** slug меняется и ломает привязку Page-элемента.
- Правило: не менять название после публикации; если поменяли — обновить `module_item[page_url]` (или пересоздать Page-элемент).

**Обновить страницу пары 2** (без дублирования элементов модуля):

```bash
python scripts/publish_canvas_lesson.py --update-page-only
# или явно:
python scripts/publish_canvas_lesson.py --update-page-only --page-url para-2-plan-uroka-dlia-priepodavatielia
```

При смене gist передавать `--lesson-nb-url` / `--homework-nb-url` — они же подставляются в тело wiki вместо относительных `.ipynb`.

Полная публикация новой пары:

```bash
python scripts/upload_lesson_gist.py modules/08_01_functions_recursion/lessons/03_parameters_and_return
python scripts/publish_canvas_lesson.py --pair 3
```

Пресеты пар 1–10 — в `PAIR_PRESETS`. Пара **8** — последнее ДЗ модуля (A3/B3/C2); Assignment сразу после «Ноутбук урока» пары 8. Пары **9–10** — `artifact=True`: скрытый план + wiki-хаб «Материалы артефакта» со ссылками на **wiki курса** (`artifact-project`, `artifact-starter-readme`, `artifact-starter-code` — MD→HTML, без GitHub). **Без** Assignment «Домашнее задание». На паре 10 — Assignment сдачи (описание ссылается на wiki задания); это **последний** элемент модуля.

**Slug wiki:** Canvas строит `page.url` из `wiki_page[title]` (транслит); русский заголовок ломает slug. Канон: `wiki_page[title] = <slug>`; человеческое имя — только в `module_item[title]`.

**Документы для учеников (не ноутбуки):** генерируются скриптом (ученический текст), не копируются «как есть» из `artifact/PROJECT.md`. Стартовый код — **один zip** (`text_stats_starter.zip`) в Files курса + краткая wiki со ссылкой на скачивание. Исходник учителя — в репо и в скрытом плане пары. Gist/Colab — **только** для `.ipynb`.

Отладка API: `scripts/canvas_api.py` пишет каждый запрос в stdout и в `.canvas_api.log` (в git не коммитить). Выключить: `CANVAS_API_DEBUG=0`. Агент после вызовов Canvas вставляет фрагмент лога в чат.

После правок в git — перезапустить `--update-page-only` с тем же `--page-url`.

### 11.5. Эталон: пара 1 (ориентация)

| Поле | Значение |
|---|---|
| Курс | `6465` (`ML: 8`) |
| Модуль Canvas | `54688` |
| Пара КТП | **1** |
| Путь в репо | `modules/08_01_functions_recursion/lessons/01_intro_profile/` |
| Файлы | только `LESSON.md` (без ноутбуков) |
| Название в Canvas | `Пара 1. ИИ, ML и профиль: ориентация` |

**Структура в модуле 54688** (позиции 1–2; пары с ноутбуками сдвигаются ниже):

| # | Элемент Canvas | Тип | Опубликован |
|---|---|---|---|
| 1 | Пара 1. ИИ, ML и профиль… | SubHeader | — |
| 2 | План урока (для преподавателя) | Page (wiki, MD→HTML) | **Нет** |

Canvas ID / slug (2026-07-16):

| Сущность | ID / slug |
|---|---|
| Wiki (тело плана) | page_id **312668**, slug `para-1-plan-uroka-dlia-priepodavatielia` |
| SubHeader «Пара 1…» | **486026** |
| План урока (для преподавателя) | **486027** (не опубликован) |

Публикация: `python scripts/publish_canvas_lesson.py --pair 1`. Домашнее задание **не** создаётся (ориентация).

### 11.6. Эталон: пара 2, модуль 1

| Поле | Значение |
|---|---|
| Курс | `6465` (`ML: 8`) |
| Модуль Canvas | `54688` |
| Пара КТП | **2** |
| Путь в репо | `modules/08_01_functions_recursion/lessons/02_function_as_mapping/` |
| Файлы | `LESSON.md`, `lesson.ipynb`, `homework.ipynb`, `solutions.ipynb` |
| Название в Canvas | `Пара 2. Функция-предсказатель: от правила к выбору модели` |

**Целевая структура в модуле 54688** (позиции 4–8 после пары 1):

| # | Элемент Canvas | Тип | Опубликован |
|---|---|---|---|
| 4 | Пара 2. Функция-предсказатель… | SubHeader | — |
| 5 | План урока (для преподавателя) | Page (wiki, MD→HTML) | **Нет** |
| 6 | Решения (для преподавателя) | ExternalUrl → Colab, `new_tab` | **Нет** |
| 7 | Ноутбук урока | ExternalUrl → Colab, `new_tab` | **Да** |
| 8 | Домашнее задание | Assignment (Colab в описании + upload `.ipynb`) | **Да** |

Canvas ID / slug — зафиксировано (2026-07-15):

| Сущность | ID / slug |
|---|---|
| Wiki (тело плана) | page_id **312663**, slug `para-2-plan-uroka-dlia-priepodavatielia` |
| SubHeader «Пара 2…» | **485999** |
| План урока (для преподавателя) | **486003** (не опубликован; title в модуле без «Пара 2») |
| Решения (для преподавателя) | **486004** (не опубликован; `new_tab=true`) |
| Ноутбук урока | **486001**, `new_tab=true` |
| Домашнее задание | **486005** (Assignment **198690**, upload `.ipynb`; Colab в описании) |
| Gist урока | [gist](https://gist.github.com/gurovic/cfc377717ba193c512a9e88593405ab8) → [Colab](https://colab.research.google.com/gist/gurovic/cfc377717ba193c512a9e88593405ab8/lesson.ipynb) |
| Gist ДЗ | [gist](https://gist.github.com/gurovic/15255de29367ddc86fb8d141f63b5cfd) → [Colab](https://colab.research.google.com/gist/gurovic/15255de29367ddc86fb8d141f63b5cfd/homework.ipynb) |
| Gist решений | [gist](https://gist.github.com/gurovic/d6626c4ad9ebc6f8c1366f31d4ab39a1) → [Colab](https://colab.research.google.com/gist/gurovic/d6626c4ad9ebc6f8c1366f31d4ab39a1/solutions.ipynb) |

Скрипты: `publish_canvas_lesson.py` (wiki + элементы), `lesson_md_html.py` (MD→HTML с разлиновкой таблиц). Обновление только wiki:

```bash
python scripts/publish_canvas_lesson.py --update-page-only --page-url para-2-plan-uroka-dlia-priepodavatielia
```

### 11.7. Чек-лист публикации одной пары

- [ ] `LESSON.md`, `lesson.ipynb`, `homework.ipynb`, `solutions.ipynb` согласованы с [Lesson Design](04_LESSON_DESIGN.md)
- [ ] `git push origin main` (или рабочая ветка, влитая в main)
- [ ] Gist для `lesson.ipynb`, `homework.ipynb`, `solutions.ipynb`; урок — ExternalUrl; ДЗ — Assignment (§11.3.2)
- [ ] Wiki плана пары — отрендеренный MD (таблицы с разлиновкой)
- [ ] В модуле — человеческие названия (§11.1); план и решения скрыты; **нет** ExternalUrl на `homework.ipynb`
- [ ] Assignment «Домашнее задание» опубликован; Colab-ссылка в описании — **кроме** пар 1 и 9–10
- [ ] Пары 9–10: нет ДЗ в модуле; после «Сдача артефакта…» нет лишних Assignment
- [ ] ID и gist-URL записаны в §11.5 (или в `LESSON.md` / `UNIT.md` при необходимости)
- [ ] Поле **Canvas** в зоне A `LESSON.md` обновлено (что выложено, не `—`)
