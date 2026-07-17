# Titanic — сквозной датасет модуля

| Файл | Назначение |
|---|---|
| `titanic.csv` | Стандартная учебная таблица пассажиров Titanic |

## Источник

CSV экспортирован из **seaborn** `sns.load_dataset('titanic')` (891 строка × 15 столбцов).

Это канонический публичный Titanic passenger table в учебном виде seaborn (на базе исторических данных о пассажирах RMS Titanic). **Не** синтетическая генерация.

Пересборка (если нужно обновить файл из той же версии seaborn):

```bash
python -c "import seaborn as sns; sns.load_dataset('titanic').to_csv('titanic.csv', index=False)"
```

Из каталога `data/`.

## Столбцы (ключевые для модуля)

| Столбец | Смысл |
|---|---|
| `survived` | 0/1 — выжил ли |
| `pclass` | класс каюты 1–3 |
| `sex` | male / female |
| `age` | возраст (есть пропуски) |
| `sibsp`, `parch` | родственники на борту |
| `fare` | плата за проезд |
| `embarked` | порт посадки C/Q/S (есть пропуски) |
| `class`, `who`, `adult_male`, `deck`, `embark_town`, `alive`, `alone` | производные/удобные поля seaborn |

Учебные ноутбуки читают **этот** `titanic.csv` через `pd.read_csv`, не вызывают `sns.load_dataset` на уроке (чтобы Colab работал offline с файлом рядом).
