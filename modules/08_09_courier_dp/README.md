# Динамическое программирование и игры

**Класс:** 8  
**КТП:** пары **59–63** (модуль **11, дополнительный**)  
**Статус:** материалы есть; Canvas не опубликован

## Сюжет

**Курьерская служба «Мгновение»** — размен, маршруты, игровые ходы; наивный перебор заменяем **DP**. Подробнее — [UNIT.md §1](UNIT.md#1-идентификация).

Логика движения по парам: memoization → DP 1D → DP 2D → win/lose game → когда DP действительно нужен.

**Обязательность:** не входит в обязательную программу-источник (`ai-school-program`); у нас стоит **после** полигона (M10) и закрывает часть календарного резерва. Проводить по готовности группы / как олимпиадное углубление.

## Данные

Микродатасеты: [data/README.md](data/README.md).

## Уроки

| Пара | Папка | Роль |
|---|---|---|
| 59 | [01_memo_dp1d](lessons/01_memo_dp1d/) | введение |
| 60 | [02_practice_dp1d](lessons/02_practice_dp1d/) | отработка |
| 61 | [03_dp2d](lessons/03_dp2d/) | введение |
| 62 | [04_practice_dp2d](lessons/04_practice_dp2d/) | отработка |
| 63 | [05_games_when_dp](lessons/05_games_when_dp/) | интеграция |

## Запуск

```bash
python modules/08_09_courier_dp/generate_notebooks.py
python scripts/run_solutions.py modules/08_09_courier_dp
```

Артефакт модуля: [artifact/PROJECT.md](artifact/PROJECT.md).  
Unit Planner: [UNIT.md](UNIT.md).
