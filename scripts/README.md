# scripts/

Утилиты репозитория. Секреты — в `.env` (gitignore).

## canvas_api.py

Клиент Canvas LMS (`canvas.letovo.ru`). Skill: `.cursor/skills/canvas-lms/`.

```bash
python scripts/canvas_api.py courses --search "ML"
python scripts/canvas_api.py modules COURSE_ID
```

Требует `CANVAS_ACCESS_TOKEN` в `.env`.

## build_ktp_08.py

Генерация операционного КТП 8 класса → `docs/ktp/08.md`.

```bash
python scripts/build_ktp_08.py
```
