#!/usr/bin/env python3
"""Generate lesson notebooks for module 08_08 (KTP pairs 49-54).

Source of truth for .ipynb: edit this file, then run it.
Pattern: stubs + asserts in lesson/homework; full solutions.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_CSV = ROOT / "data" / "orders_slim.csv"

SOL_BANNER = (
    "**Для преподавателя.** Эталон к `lesson.ipynb` и `homework.ipynb`. "
    "Не показывать ученикам до сдачи."
)

LOAD_DATA = (
    "from pathlib import Path\n"
    "import numpy as np\n"
    "import pandas as pd\n\n\n"
    "def _find(name: str) -> Path:\n"
    "    for p in (Path(name), Path(f'../../data/{name}'), Path(f'../data/{name}')):\n"
    "        if p.exists():\n"
    "            return p.resolve()\n"
    "    raise FileNotFoundError(f'{name} не найден рядом с ноутбуком')\n\n\n"
    "CSV_PATH = _find('orders_slim.csv')\n"
    "df = pd.read_csv(\n"
    "    CSV_PATH,\n"
    "    parse_dates=['order_purchase_timestamp', 'order_estimated_delivery_date', 'order_delivered_customer_date'],\n"
    ")\n"
)


def md(source: str):
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source: str):
    return {
        "cell_type": "code",
        "metadata": {},
        "source": source.splitlines(keepends=True),
        "outputs": [],
        "execution_count": None,
    }


def nb(*cells):
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": list(cells),
    }


def write(rel_path: str, notebook: dict) -> None:
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", path)


NOTEBOOKS: dict[str, dict] = {}


def add_lesson01() -> None:
    base = "lessons/01_stack_queue_deque"
    lesson = nb(
        md("# Stack / Queue / Deque на потоке заказов"),
        code(LOAD_DATA + "\nfrom collections import deque"),
        md("## 1. Подготовка событий"),
        code(
            "events = None\n"
            "assert events is not None\n"
            "assert {'order_id', 'action'} <= set(events.columns)\n"
            "print(events.head())"
        ),
        md("## 2. Stack: undo последних шагов"),
        code(
            "stack = []\n"
            "last_undo = None\n"
            "assert last_undo is not None\n"
            "print(last_undo)"
        ),
        md("## 3. Queue: FIFO-обработка"),
        code(
            "queue = deque()\n"
            "first_done = None\n"
            "assert first_done is not None\n"
            "print(first_done)"
        ),
        md("## 4. Deque: буфер с двух сторон"),
        code(
            "buffer = deque(maxlen=5)\n"
            "snapshot = None\n"
            "assert snapshot is not None and len(snapshot) == 5\n"
            "print(snapshot)"
        ),
    )
    hw = nb(
        md("# ДЗ: структуры потока заказов"),
        code(LOAD_DATA + "\nfrom collections import deque"),
        md("## 1. Реализовать undo-стек для 6 операций"),
        code(
            "ops = ['join_orders', 'drop_na', 'make_delay', 'group_state', 'kmeans', 'report']\n"
            "undo_order = []\n"
            "assert len(undo_order) == len(ops)\n"
            "assert undo_order[0] == 'report'\n"
            "print(undo_order)"
        ),
        md("## 2. Очередь заказов с приоритетом late"),
        code(
            "q = deque()\n"
            "late_first = None\n"
            "assert late_first is not None\n"
            "print(late_first)"
        ),
        md("## 3. Короткая нота"),
        code("STRUCT_NOTE = ''\nassert len(STRUCT_NOTE) > 120\nprint(STRUCT_NOTE)"),
    )
    sol = nb(
        md("# Решения: stack/queue/deque\n\n" + SOL_BANNER),
        code(LOAD_DATA + "\nfrom collections import deque"),
        code(
            "events = df[['order_id', 'is_late']].head(10).copy()\n"
            "events['action'] = np.where(events['is_late'] == 1, 'expedite', 'standard')\n"
            "stack = []\n"
            "for step in ['join_orders', 'drop_na', 'make_delay', 'group_state']:\n"
            "    stack.append(step)\n"
            "last_undo = stack.pop()\n"
            "queue = deque(events['order_id'].tolist())\n"
            "first_done = queue.popleft()\n"
            "buffer = deque(maxlen=5)\n"
            "for oid in events['order_id'].tolist():\n"
            "    buffer.append(oid)\n"
            "snapshot = list(buffer)\n"
            "ops = ['join_orders', 'drop_na', 'make_delay', 'group_state', 'kmeans', 'report']\n"
            "undo_order = list(reversed(ops))\n"
            "late_ids = df.loc[df['is_late'] == 1, 'order_id'].head(3).tolist()\n"
            "normal_ids = df.loc[df['is_late'] == 0, 'order_id'].head(3).tolist()\n"
            "q = deque(normal_ids)\n"
            "for oid in reversed(late_ids):\n"
            "    q.appendleft(oid)\n"
            "late_first = q[0]\n"
            "STRUCT_NOTE = (\n"
            "    'Stack подходит для undo preprocessing, потому что отменяем последнее действие. '\n"
            "    'Queue и deque подходят для потока заказов: FIFO и быстрые операции с концов буфера.'\n"
            ")\n"
            "print(events.head())\n"
            "print(last_undo, first_done, snapshot)\n"
            "print(undo_order, late_first)\n"
            "print(STRUCT_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson02() -> None:
    base = "lessons/02_practice_buffers"
    lesson = nb(
        md("# Практика буферов: поток заказов"),
        code(LOAD_DATA + "\nfrom collections import deque"),
        md("## 1. Буфер последних 7 заказов"),
        code(
            "recent = deque(maxlen=7)\n"
            "for oid in df['order_id']:\n"
            "    pass\n"
            "assert len(recent) == 7\n"
            "print(list(recent))"
        ),
        md("## 2. Две очереди: late и normal"),
        code(
            "late_q = deque()\nnormal_q = deque()\n"
            "n_late = None\nn_norm = None\n"
            "assert n_late is not None and n_norm is not None\n"
            "print(n_late, n_norm)"
        ),
        md("## 3. Симуляция 12 тиков обработки"),
        code(
            "processed = []\n"
            "assert len(processed) == 12\n"
            "print(processed)"
        ),
    )
    hw = nb(
        md("# ДЗ: буфер и очередь"),
        code(LOAD_DATA + "\nfrom collections import deque"),
        md("## 1. Sliding mean delivery_days (окно 5)"),
        code(
            "means = []\n"
            "assert len(means) >= 10\n"
            "assert all(isinstance(x, float) for x in means)\n"
            "print(means[:5])"
        ),
        md("## 2. Нота про пиковую нагрузку"),
        code("LOAD_NOTE = ''\nassert len(LOAD_NOTE) > 120\nprint(LOAD_NOTE)"),
    )
    sol = nb(
        md("# Решения: практика буферов\n\n" + SOL_BANNER),
        code(LOAD_DATA + "\nfrom collections import deque"),
        code(
            "recent = deque(maxlen=7)\n"
            "for oid in df['order_id']:\n"
            "    recent.append(oid)\n"
            "late_q, normal_q = deque(), deque()\n"
            "for row in df[['order_id', 'is_late']].itertuples(index=False):\n"
            "    if row.is_late == 1:\n"
            "        late_q.append(row.order_id)\n"
            "    else:\n"
            "        normal_q.append(row.order_id)\n"
            "processed = []\n"
            "for _ in range(12):\n"
            "    if late_q:\n"
            "        processed.append(late_q.popleft())\n"
            "    elif normal_q:\n"
            "        processed.append(normal_q.popleft())\n"
            "window = deque(maxlen=5)\n"
            "means = []\n"
            "for d in df['delivery_days'].tolist():\n"
            "    window.append(float(d))\n"
            "    if len(window) == 5:\n"
            "        means.append(float(np.mean(window)))\n"
            "LOAD_NOTE = (\n"
            "    'Deque с maxlen позволяет держать скользящее окно без ручного удаления старых элементов. '\n"
            "    'В пике late-очередь обрабатываем отдельно, чтобы видеть накопление критичных заказов.'\n"
            ")\n"
            "print(list(recent))\n"
            "print(len(late_q), len(normal_q))\n"
            "print(processed)\n"
            "print(means[:5])\n"
            "print(LOAD_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson03() -> None:
    base = "lessons/03_set_dict_freq"
    lesson = nb(
        md("# Set и Dict: уникальность и частоты late"),
        code(LOAD_DATA),
        md("## 1. Уникальные id через set"),
        code(
            "unique_orders = None\n"
            "assert unique_orders is not None\n"
            "assert len(unique_orders) == len(df)\n"
            "print(len(unique_orders))"
        ),
        md("## 2. Частоты late по customer_state"),
        code(
            "freq = {}\n"
            "assert len(freq) >= 3\n"
            "print(freq)"
        ),
        md("## 3. Late-rate по seller_state"),
        code(
            "rate = {}\n"
            "assert len(rate) >= 3\n"
            "print(rate)"
        ),
    )
    hw = nb(
        md("# ДЗ: membership и count"),
        code(LOAD_DATA),
        md("## 1. Найти all states c late-rate > 0.6"),
        code(
            "bad_states = set()\n"
            "assert isinstance(bad_states, set)\n"
            "print(bad_states)"
        ),
        md("## 2. Словарь top-5 seller_id по числу late"),
        code(
            "top_late = {}\n"
            "assert len(top_late) <= 5\n"
            "print(top_late)"
        ),
    )
    sol = nb(
        md("# Решения: set/dict частоты\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        code(
            "unique_orders = set(df['order_id'])\n"
            "freq: dict[str, dict[str, int]] = {}\n"
            "for r in df[['customer_state', 'is_late']].itertuples(index=False):\n"
            "    st = r.customer_state\n"
            "    if st not in freq:\n"
            "        freq[st] = {'late': 0, 'total': 0}\n"
            "    freq[st]['total'] += 1\n"
            "    freq[st]['late'] += int(r.is_late)\n"
            "rate = {k: v['late'] / v['total'] for k, v in freq.items()}\n"
            "seller_count: dict[str, int] = {}\n"
            "for r in df[['seller_id', 'is_late']].itertuples(index=False):\n"
            "    if r.is_late == 1:\n"
            "        seller_count[r.seller_id] = seller_count.get(r.seller_id, 0) + 1\n"
            "bad_states = {k for k, v in rate.items() if v > 0.6}\n"
            "top_late = dict(sorted(seller_count.items(), key=lambda x: x[1], reverse=True)[:5])\n"
            "print('unique:', len(unique_orders))\n"
            "print('freq:', freq)\n"
            "print('rate:', {k: round(v, 3) for k, v in rate.items()})\n"
            "print('bad_states:', bad_states)\n"
            "print('top_late:', top_late)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson04() -> None:
    base = "lessons/04_practice_membership_counts"
    lesson = nb(
        md("# Практика membership и долей"),
        code(LOAD_DATA),
        md("## 1. Проверка membership для контрольного списка"),
        code(
            "probe_ids = df['order_id'].head(5).tolist() + ['ol_99999']\n"
            "found = None\n"
            "assert found is not None and len(found) == len(probe_ids)\n"
            "print(found)"
        ),
        md("## 2. Dict со срезом по двум ключам: (seller_state, customer_state)"),
        code(
            "pair_rate = {}\n"
            "assert len(pair_rate) >= 5\n"
            "print(pair_rate)"
        ),
        md("## 3. Сегменты с долей late выше глобальной"),
        code(
            "hot_segments = []\n"
            "assert hot_segments is not None\n"
            "print(hot_segments[:5])"
        ),
    )
    hw = nb(
        md("# ДЗ: сегменты и membership"),
        code(LOAD_DATA),
        md("## 1. Отметить 10 заказов для ручной проверки"),
        code(
            "watch = set()\n"
            "assert len(watch) == 10\n"
            "print(watch)"
        ),
        md("## 2. Пояснение по качеству сегментации"),
        code("SEG_NOTE = ''\nassert len(SEG_NOTE) > 120\nprint(SEG_NOTE)"),
    )
    sol = nb(
        md("# Решения: membership/counts practice\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        code(
            "known = set(df['order_id'])\n"
            "probe_ids = df['order_id'].head(5).tolist() + ['ol_99999']\n"
            "found = [oid in known for oid in probe_ids]\n"
            "pair_bucket: dict[tuple[str, str], dict[str, int]] = {}\n"
            "for r in df[['seller_state', 'customer_state', 'is_late']].itertuples(index=False):\n"
            "    key = (r.seller_state, r.customer_state)\n"
            "    if key not in pair_bucket:\n"
            "        pair_bucket[key] = {'late': 0, 'total': 0}\n"
            "    pair_bucket[key]['total'] += 1\n"
            "    pair_bucket[key]['late'] += int(r.is_late)\n"
            "pair_rate = {k: v['late'] / v['total'] for k, v in pair_bucket.items()}\n"
            "global_rate = float(df['is_late'].mean())\n"
            "hot_segments = sorted(\n"
            "    [(k, round(v, 3)) for k, v in pair_rate.items() if v > global_rate],\n"
            "    key=lambda x: x[1],\n"
            "    reverse=True,\n"
            ")\n"
            "watch = set(df.sort_values(['delay_days', 'freight_value'], ascending=False)['order_id'].head(10))\n"
            "SEG_NOTE = (\n"
            "    'Сегмент полезен, если в нём достаточно наблюдений и устойчивая доля late. '\n"
            "    'Слишком мелкие сегменты дают шум и могут вести к ложным операционным решениям.'\n"
            ")\n"
            "print(found)\n"
            "print('global_rate=', round(global_rate, 3))\n"
            "print('hot_segments=', hot_segments[:6])\n"
            "print('watch=', watch)\n"
            "print(SEG_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson05() -> None:
    base = "lessons/05_kmeans_dbscan"
    lesson = nb(
        md("# KMeans и DBSCAN на логистических признаках"),
        code(
            LOAD_DATA
            + "\nfrom sklearn.cluster import KMeans, DBSCAN\n"
            "from sklearn.preprocessing import StandardScaler\n"
        ),
        md("## 1. Матрица признаков"),
        code(
            "features = ['delivery_days', 'freight_value', 'delay_days']\n"
            "X = None\n"
            "assert X is not None and X.shape[1] == 3\n"
            "print(X.head())"
        ),
        md("## 2. KMeans(k=3)"),
        code(
            "labels_km = None\n"
            "assert labels_km is not None\n"
            "assert len(labels_km) == len(df)\n"
            "print(pd.Series(labels_km).value_counts())"
        ),
        md("## 3. DBSCAN(eps=0.9, min_samples=4)"),
        code(
            "labels_db = None\n"
            "assert labels_db is not None\n"
            "assert len(labels_db) == len(df)\n"
            "print(pd.Series(labels_db).value_counts())"
        ),
        md("## 4. Сравнение профилей кластеров"),
        code(
            "profile = None\n"
            "assert profile is not None\n"
            "print(profile)"
        ),
    )
    hw = nb(
        md("# ДЗ: кластеры и шум"),
        code(
            LOAD_DATA
            + "\nfrom sklearn.cluster import KMeans, DBSCAN\n"
            "from sklearn.preprocessing import StandardScaler\n"
        ),
        md("## 1. Перебор k = 2..5"),
        code(
            "k_table = None\n"
            "assert k_table is not None and len(k_table) == 4\n"
            "print(k_table)"
        ),
        md("## 2. Нота про выбор между KMeans и DBSCAN"),
        code("CLUSTER_NOTE = ''\nassert len(CLUSTER_NOTE) > 150\nprint(CLUSTER_NOTE)"),
    )
    sol = nb(
        md("# Решения: kmeans/dbscan\n\n" + SOL_BANNER),
        code(
            LOAD_DATA
            + "\nfrom sklearn.cluster import KMeans, DBSCAN\n"
            "from sklearn.preprocessing import StandardScaler\n"
        ),
        code(
            "features = ['delivery_days', 'freight_value', 'delay_days']\n"
            "X = df[features].copy()\n"
            "scaler = StandardScaler()\n"
            "Xs = scaler.fit_transform(X)\n"
            "km = KMeans(n_clusters=3, random_state=53, n_init=10)\n"
            "labels_km = km.fit_predict(Xs)\n"
            "db = DBSCAN(eps=0.9, min_samples=4)\n"
            "labels_db = db.fit_predict(Xs)\n"
            "tmp = df.copy()\n"
            "tmp['cluster_km'] = labels_km\n"
            "tmp['cluster_db'] = labels_db\n"
            "profile = tmp.groupby('cluster_km')[features + ['is_late']].mean().round(2)\n"
            "rows = []\n"
            "for k in (2, 3, 4, 5):\n"
            "    m = KMeans(n_clusters=k, random_state=53, n_init=10)\n"
            "    lbl = m.fit_predict(Xs)\n"
            "    rows.append({'k': k, 'inertia': float(m.inertia_), 'n_clusters': int(pd.Series(lbl).nunique())})\n"
            "k_table = pd.DataFrame(rows)\n"
            "CLUSTER_NOTE = (\n"
            "    'KMeans удобен, когда хотим фиксированное число сегментов. '\n"
            "    'DBSCAN лучше ловит шум и аномалии, но чувствителен к eps/min_samples и масштабу признаков.'\n"
            ")\n"
            "print(pd.Series(labels_km).value_counts())\n"
            "print(pd.Series(labels_db).value_counts())\n"
            "print(profile)\n"
            "print(k_table)\n"
            "print(CLUSTER_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson06() -> None:
    base = "lessons/06_practice_clusters_anomalies"
    lesson = nb(
        md("# Практика: кластеры и аномалии, итоговый отчёт"),
        code(
            LOAD_DATA
            + "\nfrom sklearn.cluster import KMeans, DBSCAN\n"
            "from sklearn.preprocessing import StandardScaler\n"
        ),
        md("## 1. Получить кластеры и шум"),
        code(
            "clustered = None\n"
            "assert clustered is not None\n"
            "assert {'cluster_km', 'cluster_db'} <= set(clustered.columns)\n"
            "print(clustered.head())"
        ),
        md("## 2. Топ аномалий"),
        code(
            "anomalies = None\n"
            "assert anomalies is not None and len(anomalies) >= 3\n"
            "print(anomalies[['order_id', 'delay_days', 'freight_value']])"
        ),
        md("## 3. Acceptance checklist"),
        code(
            "acceptance = pd.Series([False, False, False, False], index=['structures', 'counts', 'clusters', 'anomalies'])\n"
            "assert bool(acceptance.all())\n"
            "print(acceptance)"
        ),
        md("## 4. REPORT для хаба"),
        code(
            "REPORT = ''\n"
            "READY = False\n"
            "assert len(REPORT) > 250\n"
            "assert READY is True\n"
            "print(REPORT)"
        ),
    )
    hw = nb(
        md("# ДЗ: финальный отчёт по модулю"),
        code(
            LOAD_DATA
            + "\nfrom sklearn.cluster import KMeans, DBSCAN\n"
            "from sklearn.preprocessing import StandardScaler\n"
        ),
        md("## 1. Executive summary"),
        code("EXEC = ''\nassert len(EXEC) > 150\nprint(EXEC)"),
        md("## 2. Ограничения и следующий шаг"),
        code("LIMITS = ''\nNEXT = ''\nassert len(LIMITS) > 120 and len(NEXT) > 120\nprint(LIMITS)\nprint(NEXT)"),
    )
    sol = nb(
        md("# Решения: итоговый отчёт\n\n" + SOL_BANNER),
        code(
            LOAD_DATA
            + "\nfrom sklearn.cluster import KMeans, DBSCAN\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from collections import deque\n"
        ),
        code(
            "stream = df[['order_id', 'is_late']].copy()\n"
            "stack = []\n"
            "for step in ['prepare', 'count', 'cluster', 'report']:\n"
            "    stack.append(step)\n"
            "queue = deque(stream['order_id'].tolist())\n"
            "structures_ok = bool(stack.pop() == 'report' and len(queue) == len(df))\n"
            "state_count = {}\n"
            "for r in df[['customer_state', 'is_late']].itertuples(index=False):\n"
            "    if r.customer_state not in state_count:\n"
            "        state_count[r.customer_state] = {'late': 0, 'total': 0}\n"
            "    state_count[r.customer_state]['total'] += 1\n"
            "    state_count[r.customer_state]['late'] += int(r.is_late)\n"
            "counts_ok = len(state_count) >= 3\n"
            "features = ['delivery_days', 'freight_value', 'delay_days']\n"
            "Xs = StandardScaler().fit_transform(df[features])\n"
            "km = KMeans(n_clusters=3, random_state=54, n_init=10)\n"
            "db = DBSCAN(eps=0.9, min_samples=4)\n"
            "clustered = df.copy()\n"
            "clustered['cluster_km'] = km.fit_predict(Xs)\n"
            "clustered['cluster_db'] = db.fit_predict(Xs)\n"
            "clusters_ok = clustered['cluster_km'].nunique() == 3\n"
            "is_noise = clustered['cluster_db'] == -1\n"
            "top_delay = clustered['delay_days'].rank(method='first', ascending=False) <= 5\n"
            "anomalies = clustered[is_noise | top_delay].sort_values(['delay_days', 'freight_value'], ascending=False).head(8)\n"
            "anomalies_ok = len(anomalies) >= 3\n"
            "acceptance = pd.Series(\n"
            "    [structures_ok, counts_ok, clusters_ok, anomalies_ok],\n"
            "    index=['structures', 'counts', 'clusters', 'anomalies'],\n"
            ")\n"
            "REPORT = (\n"
            "    f'Поток из {len(df)} заказов обработан с явным использованием stack/queue/deque и частот через dict. '\n"
            "    f\"KMeans выделил {clustered['cluster_km'].nunique()} сегмента доставки, DBSCAN пометил \"\n"
            "    f\"{int((clustered['cluster_db'] == -1).sum())} шумовых наблюдений. \"\n"
            "    'Аномалии совпадают с высокими delay_days и freight_value, что указывает на рискованные маршруты и нагрузку хаба. '\n"
            "    'Ограничение: учебный slim и ручной выбор параметров DBSCAN; выводы требуют проверки на полном Olist-срезе.'\n"
            ")\n"
            "READY = bool(acceptance.all())\n"
            "EXEC = (\n"
            "    'Сегментация показывает, что часть late-заказов концентрируется в кластерах с высоким delivery_days и freight_value. '\n"
            "    'Рекомендуем отдельный мониторинг этих сегментов и ранний буфер для потенциальных опозданий.'\n"
            ")\n"
            "LIMITS = (\n"
            "    'DBSCAN чувствителен к масштабу и eps, а KMeans фиксирует число кластеров заранее. '\n"
            "    'Поэтому результаты интерпретируем как рабочую гипотезу, а не финальную истину.'\n"
            ")\n"
            "NEXT = (\n"
            "    'Следующий шаг: повторить анализ на большем real Olist-срезе, добавить географические признаки и формальный протокол оценки.'\n"
            ")\n"
            "print(clustered[['cluster_km', 'cluster_db']].head())\n"
            "print(anomalies[['order_id', 'delay_days', 'freight_value']])\n"
            "print(acceptance)\n"
            "print('READY=', READY)\n"
            "print(REPORT)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


BUILDERS = [
    add_lesson01,
    add_lesson02,
    add_lesson03,
    add_lesson04,
    add_lesson05,
    add_lesson06,
]


def main() -> None:
    if not DATA_CSV.exists():
        raise SystemExit(f"Missing {DATA_CSV}. Run data/make_slim.py first.")
    for b in BUILDERS:
        b()
    for rel, content in NOTEBOOKS.items():
        write(rel, content)
    print(f"done: {len(NOTEBOOKS)} notebooks in 6 lessons")


if __name__ == "__main__":
    main()
