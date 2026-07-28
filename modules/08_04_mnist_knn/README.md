# Распознавание цифр: вероятность и kNN

**Класс:** 8  
**КТП:** пары **24–29**  
**Статус:** материалы модуля (UNIT, LESSON, ноутбуки, артефакт)

Сюжет: почтовый сервис автоматизирует чтение индексов на конвертах.

## Данные

Рукописные цифры 8×8: `data/digits.csv` — экспорт `sklearn.datasets.load_digits` (UCI, 1797×64).  
Атрибуция и почему не полный MNIST: [data/README.md](data/README.md).

Имя папки `mnist_knn` — историческое; в материалах — «цифры 8×8».

## Уроки

| Пара | Папка | Роль |
|---|---|---|
| 24 | [01_probability_frequency](lessons/01_probability_frequency/) | введение |
| 25 | [02_practice_split](lessons/02_practice_split/) | отработка |
| 26 | [03_knn_scaling](lessons/03_knn_scaling/) | введение |
| 27 | [04_practice_knn_baseline](lessons/04_practice_knn_baseline/) | отработка |
| 28 | [05_accuracy_f1_val](lessons/05_accuracy_f1_val/) | введение |
| 29 | [06_practice_search_metrics](lessons/06_practice_search_metrics/) | интеграция |

## Запуск

```bash
# пересборка CSV (если нужно)
python modules/08_04_mnist_knn/data/make_digits_csv.py

# пересборка ноутбуков
python modules/08_04_mnist_knn/generate_notebooks.py

# ворота: эталоны преподавателя
python scripts/run_solutions.py modules/08_04_mnist_knn
```

Артефакт: [artifact/PROJECT.md](artifact/PROJECT.md).  
План модуля: [UNIT.md](UNIT.md).
