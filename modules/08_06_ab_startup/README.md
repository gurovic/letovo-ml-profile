# A/B-тест стартапа и статистический вывод

**Класс:** 8  
**КТП:** пары **36–41**  
**Статус:** полностью переписан; 6/6 пар имеют LESSON A–E, student stubs/asserts, ДЗ A+Challenge и секционные решения

Сюжет: стартап тестирует два дизайна лендинга, оценивает статистическую значимость uplift и формирует отчёт для product-решения.

## Данные

Файл модуля: `data/startup_ab.csv`  
Сборка (фиксированный seed): `python modules/08_06_ab_startup/data/make_startup_ab_csv.py`

Описание полей и ограничений: [data/README.md](data/README.md)

## Уроки

| Пара | Папка | Роль |
|---|---|---|
| 36 | [01_hypotheses_pvalue](lessons/01_hypotheses_pvalue/) | введение |
| 37 | [02_practice_permutation](lessons/02_practice_permutation/) | отработка |
| 38 | [03_ci_correlation](lessons/03_ci_correlation/) | введение |
| 39 | [04_practice_ci_corr](lessons/04_practice_ci_corr/) | отработка |
| 40 | [05_peeking_multireg](lessons/05_peeking_multireg/) | введение |
| 41 | [06_practice_report](lessons/06_practice_report/) | интеграция |

## Генерация и проверка

```bash
python modules/08_06_ab_startup/data/make_startup_ab_csv.py
python modules/08_06_ab_startup/generate_notebooks.py
python scripts/run_solutions.py modules/08_06_ab_startup
```

Последняя локальная проверка при переписывании: **PASS 6/6**. `generate_notebooks.py` — единственный источник истины для 18 ноутбуков; при генерации один и тот же `startup_ab.csv` копируется во все шесть папок уроков. Размеры пар: lesson **12–18** ячеек, homework **13**, solutions **18–28**; каждый `LESSON.md` содержит полные разделы A–E.

Артефакт: [artifact/PROJECT.md](artifact/PROJECT.md)  
План модуля: [UNIT.md](UNIT.md)
