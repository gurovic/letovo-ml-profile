# Reference: внешний справочник

**Только для чтения.** В эту папку **не пишем** — это материалы из внешнего репозитория для сравнения при проектировании.

Канон профиля: `docs/` и `modules/`. КТП: `docs/ktp/`.

## Файлы

| Файл | Описание |
|---|---|
| `COURSE_PROGRAM_DRAFT.md` | Программа 7–11 (экспорт, может устаревать) |
| `SCHOOL_UNIT_PLANNER.md` | Поля школьного unit planner (MYP); маппинг на наш UP |
| `school_unit_planner_schema.json` | JSON-схема для автозаполнения школьной формы |
| `program_data.json` | Структурированные данные из HTML |
| `program.html` | Исходник ([aguschin/ai-school-program](https://github.com/aguschin/ai-school-program)) |
| `extract_program.py` | HTML → JSON + Markdown (обновление **внешнего** снимка) |

## Обновление внешнего снимка

```bash
# заменить program.html из источника, затем:
python reference/extract_program.py
```

Это не обновляет операционный КТП. КТП 8 класса: `python scripts/build_ktp_08.py` → `docs/ktp/08.md`.

## Использование

- сравнение идей с черновиком программы;
- **не** источник обязательных решений;
- при противоречии — `docs/` (Foundation).
