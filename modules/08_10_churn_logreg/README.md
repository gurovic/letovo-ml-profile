# Отклик на кампанию: логистическая регрессия и venv

**Класс:** 8  
**КТП:** пары **60-64**  
**Статус:** перепроектирован под планку модуля 1; Canvas не опубликован

Сюжет модуля: аналитик банковской кампании прогнозирует отклик на депозит (`y`) и выбирает рабочий порог классификации.  
Критическое правило модуля: `duration` не используется в признаках модели (leakage). Запрет проверяется assert в ноутбуках, teacher solutions и CLI.

## Данные

`bank_marketing_slim.csv` и генератор: [data/README.md](data/README.md).

## Уроки

| Пара | Папка | Роль |
|---|---|---|
| 60 | [01_logreg_sigmoid_threshold](lessons/01_logreg_sigmoid_threshold/) | введение |
| 61 | [02_practice_fit_threshold](lessons/02_practice_fit_threshold/) | отработка |
| 62 | [03_imbalance_metrics](lessons/03_imbalance_metrics/) | введение |
| 63 | [04_practice_metrics_cli](lessons/04_practice_metrics_cli/) | отработка |
| 64 | [05_venv_requirements_readme](lessons/05_venv_requirements_readme/) | интеграция |

## Запуск

```bash
python modules/08_10_churn_logreg/data/make_bank_marketing_slim.py
python modules/08_10_churn_logreg/generate_notebooks.py
python scripts/run_solutions.py modules/08_10_churn_logreg
```

Генератор — источник истины для 15 ноутбуков. В каждой паре: `lesson.ipynb` со stubs и assert, отдельное ДЗ Part A + Challenge и секционный `solutions.ipynb`.

CLI для пары 63:

```bash
python modules/08_10_churn_logreg/lessons/04_practice_metrics_cli/train_cli.py --data modules/08_10_churn_logreg/data/bank_marketing_slim.csv --threshold 0.45
```

Артефакт модуля: [artifact/PROJECT.md](artifact/PROJECT.md).  
Unit Planner: [UNIT.md](UNIT.md).
