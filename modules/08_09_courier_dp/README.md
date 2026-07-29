# Динамическое программирование и игры

**Класс:** 8  
**КТП:** пары **55-59**  
**Статус:** материалы перепроектированы под планку M1; Canvas не опубликован

Сюжет модуля: курьерская служба «Мгновение» оптимизирует размен, стоимость маршрутов и игровые сценарии выбора хода.  
Логика движения по парам: memoization -> DP 1D -> DP 2D -> win/lose game -> когда DP действительно нужен.

## Данные

Микродатасеты: [data/README.md](data/README.md).

## Уроки

| Пара | Папка | Роль |
|---|---|---|
| 55 | [01_memo_dp1d](lessons/01_memo_dp1d/) | введение |
| 56 | [02_practice_dp1d](lessons/02_practice_dp1d/) | отработка |
| 57 | [03_dp2d](lessons/03_dp2d/) | введение |
| 58 | [04_practice_dp2d](lessons/04_practice_dp2d/) | отработка |
| 59 | [05_games_when_dp](lessons/05_games_when_dp/) | интеграция |

## Запуск

```bash
python modules/08_09_courier_dp/generate_notebooks.py
python scripts/run_solutions.py modules/08_09_courier_dp
```

Артефакт модуля: [artifact/PROJECT.md](artifact/PROJECT.md).  
Unit Planner: [UNIT.md](UNIT.md).
