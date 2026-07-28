# Логистика маркетплейса: структуры данных и кластеризация

**Класс:** 8  
**КТП:** пары **49-54**  
**Статус:** полный комплект материалов (UNIT, LESSON, ноутбуки, артефакт)

Сюжет модуля: операционный хаб маркетплейса анализирует опоздания доставки на slim-срезе Olist.  
Логика движения по парам: `stack/queue/deque` -> `set/dict` -> `KMeans/DBSCAN` -> аномалии.

## Данные

`orders_slim.csv` и сборка `make_slim.py`: [data/README.md](data/README.md).

## Уроки

| Пара | Папка | Роль |
|---|---|---|
| 49 | [01_stack_queue_deque](lessons/01_stack_queue_deque/) | введение |
| 50 | [02_practice_buffers](lessons/02_practice_buffers/) | отработка |
| 51 | [03_set_dict_freq](lessons/03_set_dict_freq/) | введение |
| 52 | [04_practice_membership_counts](lessons/04_practice_membership_counts/) | отработка |
| 53 | [05_kmeans_dbscan](lessons/05_kmeans_dbscan/) | введение |
| 54 | [06_practice_clusters_anomalies](lessons/06_practice_clusters_anomalies/) | интеграция |

## Запуск

```bash
python modules/08_08_logistics_clustering/data/make_slim.py
python modules/08_08_logistics_clustering/generate_notebooks.py
python scripts/run_solutions.py modules/08_08_logistics_clustering
```

Артефакт модуля: [artifact/PROJECT.md](artifact/PROJECT.md).  
Unit Planner: [UNIT.md](UNIT.md).
