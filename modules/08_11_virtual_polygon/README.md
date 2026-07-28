# Виртуальный полигон: производная и градиентный спуск

**Класс:** 8  
**КТП:** пары **65–68**  
**Статус:** материалы модуля (UNIT, LESSON, ноутбуки, артефакт)

Сюжет: испытатели на полигоне изучают рельеф функции и шаг за шагом идут к минимуму loss.

## Данные

Отдельный CSV не обязателен: в модуле используются инлайн-функции и небольшие массивы для численных экспериментов.

## Уроки

| Пара | Папка | Роль |
|---|---|---|
| 65 | [01_derivative_intuition](lessons/01_derivative_intuition/) | введение |
| 66 | [02_practice_gd_1d](lessons/02_practice_gd_1d/) | отработка |
| 67 | [03_integral_loss_overview](lessons/03_integral_loss_overview/) | введение |
| 68 | [04_practice_min_loss_year_reflect](lessons/04_practice_min_loss_year_reflect/) | интеграция |

## Запуск

```bash
# пересборка ноутбуков
python modules/08_11_virtual_polygon/generate_notebooks.py

# ворота качества: только teacher solutions
python scripts/run_solutions.py modules/08_11_virtual_polygon
```

Артефакт: [artifact/PROJECT.md](artifact/PROJECT.md).  
План модуля: [UNIT.md](UNIT.md).
