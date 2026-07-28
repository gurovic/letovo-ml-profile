#!/usr/bin/env python3
"""Generate lesson notebooks for module 08_05 (KTP pairs 30-35).

Source of truth for .ipynb: edit this file, then run it.
Pattern: stubs + asserts in lesson/homework; full solutions.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
ORDERS_CSV = DATA_DIR / "orders_slim.csv"
CUSTOMERS_CSV = DATA_DIR / "customers_slim.csv"
PAYMENTS_CSV = DATA_DIR / "payments_slim.csv"

SOL_BANNER = (
    "**Для преподавателя.** Эталон к `lesson.ipynb` и `homework.ipynb`. "
    "Не показывать ученикам до сдачи."
)

LOAD_DATA = (
    "from pathlib import Path\n"
    "import pandas as pd\n\n\n"
    "def _find(name: str) -> Path:\n"
    "    for p in (Path(name), Path(f'../../data/{name}'), Path(f'../data/{name}')):\n"
    "        if p.exists():\n"
    "            return p.resolve()\n"
    "    raise FileNotFoundError(f'{name} не найден — положите slim CSV рядом с ноутбуком')\n\n\n"
    "ORDERS_PATH = _find('orders_slim.csv')\n"
    "CUSTOMERS_PATH = _find('customers_slim.csv')\n"
    "PAYMENTS_PATH = _find('payments_slim.csv')\n\n"
    "orders = pd.read_csv(ORDERS_PATH, parse_dates=['order_purchase_timestamp'])\n"
    "if 'order_delivered_customer_date' in orders.columns:\n"
    "    orders['order_delivered_customer_date'] = pd.to_datetime(\n"
    "        orders['order_delivered_customer_date'], errors='coerce'\n"
    "    )\n"
    "customers = pd.read_csv(CUSTOMERS_PATH)\n"
    "payments = pd.read_csv(PAYMENTS_PATH)\n"
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


def copy_csv(lesson_dir: str) -> None:
    base = ROOT / lesson_dir
    base.mkdir(parents=True, exist_ok=True)
    for src in (ORDERS_CSV, CUSTOMERS_CSV, PAYMENTS_CSV):
        dest = base / src.name
        shutil.copy2(src, dest)
        print("copied", src.name, "->", dest)


NOTEBOOKS: dict[str, dict] = {}

LESSON_DIRS = [
    "lessons/01_feature_types_apply",
    "lessons/02_practice_apply_orders",
    "lessons/03_rfm_groupby",
    "lessons/04_practice_aggregates",
    "lessons/05_logging_raise",
    "lessons/06_practice_pipeline",
]


def add_lesson01() -> None:
    """Pair 30: feature types, apply, merges."""
    base = "lessons/01_feature_types_apply"
    lesson = nb(
        md(
            "# Типы признаков и `apply` на заказах\n\n"
            "Первый шаг в feature engineering: понять, какие столбцы у нас есть и какие признаки из них можно собрать."
        ),
        code(LOAD_DATA),
        md("## 1. Размеры трёх таблиц"),
        code(
            "n_orders = None\n"
            "n_customers = None\n"
            "n_payments = None\n"
            "assert n_orders == 3500\n"
            "assert n_customers == 778\n"
            "assert n_payments == 3500\n"
            "print(n_orders, n_customers, n_payments)"
        ),
        md("## 2. Типы столбцов: числовые и категориальные"),
        code(
            "order_num = None\n"
            "order_cat = None\n"
            "payment_num = None\n"
            "payment_cat = None\n"
            "assert order_num is not None and order_cat is not None\n"
            "assert payment_num is not None and payment_cat is not None\n"
            "assert 'order_status' in order_cat\n"
            "assert 'payment_value' in payment_num\n"
            "print(order_num, order_cat, payment_num, payment_cat)"
        ),
        md("## 3. Соединяем оплаты с заказами"),
        code(
            "orders_pay = None\n"
            "mean_payment = None\n"
            "assert orders_pay is not None and mean_payment is not None\n"
            "assert orders_pay.shape[0] == 3500\n"
            "assert 100 < float(mean_payment) < 700\n"
            "print(orders_pay.shape, round(float(mean_payment), 2))"
        ),
        md("## 4. `apply` + lambda: дни до доставки"),
        code(
            "orders_pay['days_to_deliver'] = None\n"
            "mean_days = None\n"
            "assert 'days_to_deliver' in orders_pay.columns\n"
            "assert mean_days is not None and 0 < float(mean_days) < 60\n"
            "print(round(float(mean_days), 2))"
        ),
        md("## 5. Бин для суммы оплаты"),
        code(
            "orders_pay['payment_bin'] = None\n"
            "bin_counts = None\n"
            "assert 'payment_bin' in orders_pay.columns\n"
            "assert bin_counts is not None and int(bin_counts.sum()) == len(orders_pay)\n"
            "print(bin_counts)"
        ),
        md(
            "## 6. Нота про `customer_state`\n\n"
            "Запишите `STATE_NOTE`: зачем признак штата может быть полезен, и почему его нельзя использовать бездумно."
        ),
        code(
            "STATE_NOTE = ''\n"
            "assert len(STATE_NOTE) > 80\n"
            "print(STATE_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: типы признаков и первые трансформации"),
        code(LOAD_DATA),
        md("### A. Закрепление"),
        md("## 1. Диапазон дат покупок"),
        code(
            "min_date = None\n"
            "max_date = None\n"
            "assert min_date is not None and max_date is not None\n"
            "assert str(min_date.date()) == '2017-01-01'\n"
            "assert str(max_date.date()) == '2018-08-31'\n"
            "print(min_date, max_date)"
        ),
        md("## 2. Доли типов оплаты"),
        code(
            "pay_share = None\n"
            "assert pay_share is not None\n"
            "assert abs(float(pay_share.sum()) - 1.0) < 1e-9\n"
            "assert float(pay_share.get('credit_card', 0)) > 0.6\n"
            "print(pay_share.round(3))"
        ),
        md("### B. Вызов"),
        md("## 3. Признак `is_card` и средний чек"),
        code(
            "payments['is_card'] = None\n"
            "mean_card = None\n"
            "mean_other = None\n"
            "assert set(payments['is_card'].unique()) <= {0, 1}\n"
            "assert mean_card is not None and mean_other is not None\n"
            "print(round(float(mean_card), 2), round(float(mean_other), 2))"
        ),
        md("## 4. Почему `apply` здесь уместен"),
        code(
            "APPLY_NOTE = ''\n"
            "assert len(APPLY_NOTE) > 120\n"
            "print(APPLY_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: типы и `apply`\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        md("## Урок. 1-6"),
        code(
            "n_orders, n_customers, n_payments = len(orders), len(customers), len(payments)\n"
            "order_num = orders.select_dtypes(include='number').columns.tolist()\n"
            "order_cat = orders.select_dtypes(exclude='number').columns.tolist()\n"
            "payment_num = payments.select_dtypes(include='number').columns.tolist()\n"
            "payment_cat = payments.select_dtypes(exclude='number').columns.tolist()\n"
            "orders_pay = orders.merge(payments, on='order_id', how='left')\n"
            "mean_payment = float(orders_pay['payment_value'].mean())\n"
            "orders_pay['days_to_deliver'] = orders_pay.apply(\n"
            "    lambda r: (r['order_delivered_customer_date'] - r['order_purchase_timestamp']).days\n"
            "    if pd.notna(r['order_delivered_customer_date']) else pd.NA,\n"
            "    axis=1,\n"
            ")\n"
            "mean_days = float(orders_pay['days_to_deliver'].dropna().mean())\n"
            "orders_pay['payment_bin'] = pd.cut(\n"
            "    orders_pay['payment_value'], bins=[-1, 100, 300, 1000, 10_000], labels=['small', 'mid', 'big', 'very_big']\n"
            ")\n"
            "bin_counts = orders_pay['payment_bin'].value_counts(dropna=False)\n"
            "STATE_NOTE = (\n"
            "    'Штат может отражать логистику и платёжные привычки: доля card, средний чек, скорость доставки. '\n"
            "    'Но это прокси-признак, он может ловить шум и территориальные перекосы, поэтому нужен контроль валидацией.'\n"
            ")\n"
            "print(n_orders, n_customers, n_payments)\n"
            "print(order_num, order_cat)\n"
            "print(round(mean_payment, 2), round(mean_days, 2))\n"
            "print(bin_counts)\n"
            "print(STATE_NOTE)"
        ),
        md("## ДЗ. 1-4"),
        code(
            "min_date = orders['order_purchase_timestamp'].min()\n"
            "max_date = orders['order_purchase_timestamp'].max()\n"
            "pay_share = payments['payment_type'].value_counts(normalize=True)\n"
            "payments['is_card'] = (payments['payment_type'] == 'credit_card').astype(int)\n"
            "mean_card = float(payments.loc[payments['is_card'] == 1, 'payment_value'].mean())\n"
            "mean_other = float(payments.loc[payments['is_card'] == 0, 'payment_value'].mean())\n"
            "APPLY_NOTE = (\n"
            "    'Через apply удобно считать признак из нескольких столбцов строки, например дни до доставки. '\n"
            "    'Когда формула работает в рамках одного столбца, лучше векторная операция: она короче и быстрее.'\n"
            ")\n"
            "print(min_date, max_date)\n"
            "print(pay_share.round(3))\n"
            "print(round(mean_card, 2), round(mean_other, 2))\n"
            "print(APPLY_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson02() -> None:
    """Pair 31: practice on order-level transforms."""
    base = "lessons/02_practice_apply_orders"
    lesson = nb(
        md("# Практика: `apply` и признаки заказа"),
        code(LOAD_DATA),
        md("## 1. `order_month` и `weekday`"),
        code(
            "orders['order_month'] = None\n"
            "orders['weekday'] = None\n"
            "assert 'order_month' in orders.columns and 'weekday' in orders.columns\n"
            "assert orders['order_month'].between(1, 12).all()\n"
            "assert orders['weekday'].between(0, 6).all()\n"
            "print(orders[['order_month', 'weekday']].head())"
        ),
        md("## 2. `is_card` в оплатах и join"),
        code(
            "payments['is_card'] = None\n"
            "joined = None\n"
            "assert joined is not None\n"
            "assert joined.shape[0] == 3500\n"
            "assert 'is_card' in joined.columns\n"
            "print(joined.shape)"
        ),
        md("## 3. Задержка доставки и выбросы"),
        code(
            "joined['days_to_deliver'] = None\n"
            "p99_delay = None\n"
            "n_outliers = None\n"
            "assert p99_delay is not None and n_outliers is not None\n"
            "assert float(p99_delay) > 0\n"
            "assert int(n_outliers) >= 1\n"
            "print(round(float(p99_delay), 2), int(n_outliers))"
        ),
        md("## 4. Проверка форм после объединений"),
        code(
            "shape_ok = None\n"
            "assert shape_ok is True\n"
            "print('shape check:', shape_ok)"
        ),
        md("## 5. Challenge: бины задержки доставки"),
        code(
            "joined['delay_bin'] = None\n"
            "delay_counts = None\n"
            "assert delay_counts is not None\n"
            "assert int(delay_counts.sum()) == int(joined['days_to_deliver'].notna().sum())\n"
            "print(delay_counts)"
        ),
    )
    hw = nb(
        md("# ДЗ: признаки заказа (практика)"),
        code(LOAD_DATA),
        md("### A. Закрепление"),
        md("## 1. Средний чек по месяцам"),
        code(
            "orders['order_month'] = orders['order_purchase_timestamp'].dt.month\n"
            "joined = orders.merge(payments, on='order_id', how='left')\n"
            "month_mean = None\n"
            "assert month_mean is not None and len(month_mean) >= 12\n"
            "print(month_mean.head())"
        ),
        md("## 2. Доля card по дням недели"),
        code(
            "payments['is_card'] = (payments['payment_type'] == 'credit_card').astype(int)\n"
            "joined = joined.merge(payments[['order_id', 'is_card']], on='order_id', how='left')\n"
            "joined['weekday'] = joined['order_purchase_timestamp'].dt.weekday\n"
            "weekday_card = None\n"
            "assert weekday_card is not None and len(weekday_card) == 7\n"
            "print(weekday_card)"
        ),
        md("### B. Вызов"),
        md("## 3. Короткий лог преобразований"),
        code(
            "log_steps = []\n"
            "# добавьте в лог 4-5 шагов своей обработки\n"
            "assert len(log_steps) >= 4\n"
            "print(log_steps)"
        ),
        md("## 4. Нота о выбросах"),
        code(
            "OUTLIER_NOTE = ''\n"
            "assert len(OUTLIER_NOTE) > 120\n"
            "print(OUTLIER_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: практика apply и join\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        md("## Урок. 1-5"),
        code(
            "orders['order_month'] = orders['order_purchase_timestamp'].dt.month\n"
            "orders['weekday'] = orders['order_purchase_timestamp'].dt.weekday\n"
            "payments['is_card'] = (payments['payment_type'] == 'credit_card').astype(int)\n"
            "joined = orders.merge(payments, on='order_id', how='left')\n"
            "joined['days_to_deliver'] = joined.apply(\n"
            "    lambda r: (r['order_delivered_customer_date'] - r['order_purchase_timestamp']).days\n"
            "    if pd.notna(r['order_delivered_customer_date']) else pd.NA,\n"
            "    axis=1,\n"
            ")\n"
            "p99_delay = float(joined['days_to_deliver'].dropna().quantile(0.99))\n"
            "n_outliers = int((joined['days_to_deliver'] > p99_delay).sum())\n"
            "shape_ok = (joined.shape[0] == len(orders) == len(payments))\n"
            "clean_delay = joined['days_to_deliver'].dropna()\n"
            "joined.loc[clean_delay.index, 'delay_bin'] = pd.cut(\n"
            "    clean_delay, bins=[-1, 3, 7, 14, 365], labels=['0-3', '4-7', '8-14', '15+']\n"
            ")\n"
            "delay_counts = joined['delay_bin'].value_counts().sort_index()\n"
            "print(joined.shape, round(p99_delay, 2), n_outliers, shape_ok)\n"
            "print(delay_counts)"
        ),
        md("## ДЗ. 1-4"),
        code(
            "orders['order_month'] = orders['order_purchase_timestamp'].dt.month\n"
            "joined = orders.merge(payments, on='order_id', how='left')\n"
            "month_mean = joined.groupby('order_month')['payment_value'].mean().sort_index()\n"
            "joined['is_card'] = (joined['payment_type'] == 'credit_card').astype(int)\n"
            "joined['weekday'] = joined['order_purchase_timestamp'].dt.weekday\n"
            "weekday_card = joined.groupby('weekday')['is_card'].mean().sort_index()\n"
            "log_steps = [\n"
            "    'loaded tables',\n"
            "    'created order_month and weekday',\n"
            "    'joined payments to orders',\n"
            "    'computed days_to_deliver and p99 threshold',\n"
            "    'binned delays into categories',\n"
            "]\n"
            "OUTLIER_NOTE = (\n"
            "    'Выбросы по задержке полезны как сигнал проблемной логистики, но их нельзя автоматически выбрасывать. '\n"
            "    'Для части клиентов это реальные кейсы, и они влияют на бизнес-решение, а не только на среднее значение.'\n"
            ")\n"
            "print(month_mean.head())\n"
            "print(weekday_card)\n"
            "print(log_steps)\n"
            "print(OUTLIER_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson03() -> None:
    """Pair 32: RFM via groupby."""
    base = "lessons/03_rfm_groupby"
    lesson = nb(
        md("# RFM через `groupby`"),
        code(LOAD_DATA),
        md("## 1. Склеиваем заказы и оплаты"),
        code(
            "orders_pay = None\n"
            "assert orders_pay is not None and orders_pay.shape[0] == 3500\n"
            "print(orders_pay.shape)"
        ),
        md("## 2. Строим таблицу клиента с R, F, M"),
        code(
            "rfm = None\n"
            "assert rfm is not None\n"
            "assert {'customer_id', 'Recency', 'Frequency', 'Monetary'} <= set(rfm.columns)\n"
            "assert len(rfm) == 778\n"
            "print(rfm.head())"
        ),
        md("## 3. Опорная дата и смысл Recency"),
        code(
            "ref_date = None\n"
            "WHEN_RECENCY = ''\n"
            "assert ref_date is not None\n"
            "assert len(WHEN_RECENCY) > 80\n"
            "print(ref_date, WHEN_RECENCY)"
        ),
        md("## 4. Describe для R/F/M"),
        code(
            "stats = None\n"
            "f_mean = None\n"
            "m_mean = None\n"
            "assert stats is not None\n"
            "assert 3.5 < float(f_mean) < 5.5\n"
            "assert 250 < float(m_mean) < 450\n"
            "print(stats)"
        ),
        md("## 5. Топ-5 клиентов по Monetary"),
        code(
            "top5 = None\n"
            "assert top5 is not None and len(top5) == 5\n"
            "assert top5['Monetary'].is_monotonic_decreasing\n"
            "print(top5)"
        ),
    )
    hw = nb(
        md("# ДЗ: RFM и интерпретация"),
        code(LOAD_DATA),
        md("### A. Закрепление"),
        md("## 1. Доли клиентов по уровню Frequency"),
        code(
            "rfm = None\n"
            "freq_bin_share = None\n"
            "assert rfm is not None and freq_bin_share is not None\n"
            "assert abs(float(freq_bin_share.sum()) - 1.0) < 1e-9\n"
            "print(freq_bin_share)"
        ),
        md("## 2. Топ-10 по Recency (самые давние покупки)"),
        code(
            "top_recency = None\n"
            "assert top_recency is not None and len(top_recency) == 10\n"
            "print(top_recency[['customer_id', 'Recency']])"
        ),
        md("### B. Вызов"),
        md("## 3. Нота про клиентов с высоким M и низким F"),
        code(
            "RFM_NOTE = ''\n"
            "assert len(RFM_NOTE) > 150\n"
            "print(RFM_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: RFM и groupby\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        md("## Урок. 1-5"),
        code(
            "orders_pay = orders.merge(payments, on='order_id', how='left')\n"
            "ref_date = orders['order_purchase_timestamp'].max()\n"
            "rfm = (\n"
            "    orders_pay.groupby('customer_id')\n"
            "    .agg(\n"
            "        last_purchase=('order_purchase_timestamp', 'max'),\n"
            "        Frequency=('order_id', 'nunique'),\n"
            "        Monetary=('payment_value', 'sum'),\n"
            "    )\n"
            "    .reset_index()\n"
            ")\n"
            "rfm['Recency'] = (ref_date - rfm['last_purchase']).dt.days\n"
            "rfm = rfm[['customer_id', 'Recency', 'Frequency', 'Monetary']]\n"
            "WHEN_RECENCY = (\n"
            "    'Recency всегда считается относительно одной опорной даты для всей таблицы, '\n"
            "    'иначе значения между клиентами не сопоставимы.'\n"
            ")\n"
            "stats = rfm[['Recency', 'Frequency', 'Monetary']].describe().round(2)\n"
            "f_mean = float(rfm['Frequency'].mean())\n"
            "m_mean = float(rfm['Monetary'].mean())\n"
            "top5 = rfm.sort_values('Monetary', ascending=False).head(5)\n"
            "print(ref_date)\n"
            "print(stats)\n"
            "print('F mean:', round(f_mean, 2), 'M mean:', round(m_mean, 2))\n"
            "print(top5)"
        ),
        md("## ДЗ. 1-3"),
        code(
            "orders_pay = orders.merge(payments, on='order_id', how='left')\n"
            "ref_date = orders['order_purchase_timestamp'].max()\n"
            "rfm = (\n"
            "    orders_pay.groupby('customer_id')\n"
            "    .agg(last_purchase=('order_purchase_timestamp', 'max'), Frequency=('order_id', 'nunique'), Monetary=('payment_value', 'sum'))\n"
            "    .reset_index()\n"
            ")\n"
            "rfm['Recency'] = (ref_date - rfm['last_purchase']).dt.days\n"
            "rfm = rfm[['customer_id', 'Recency', 'Frequency', 'Monetary']]\n"
            "rfm['freq_bin'] = pd.cut(rfm['Frequency'], bins=[0, 2, 5, 100], labels=['1-2', '3-5', '6+'])\n"
            "freq_bin_share = rfm['freq_bin'].value_counts(normalize=True).sort_index()\n"
            "top_recency = rfm.sort_values('Recency', ascending=False).head(10)\n"
            "RFM_NOTE = (\n"
            "    'Клиент с высоким Monetary и низким Frequency обычно делает редкие, но крупные покупки. '\n"
            "    'Ему может подойти отдельная коммуникация: не частые скидки, а персональные дорогие предложения.'\n"
            ")\n"
            "print(freq_bin_share)\n"
            "print(top_recency[['customer_id', 'Recency']])\n"
            "print(RFM_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson04() -> None:
    """Pair 33: practice with extra aggregates."""
    base = "lessons/04_practice_aggregates"
    lesson = nb(
        md("# Практика: расширяем RFM агрегатами"),
        code(LOAD_DATA),
        md("## 1. Базовый RFM"),
        code(
            "rfm = None\n"
            "assert rfm is not None and len(rfm) == 778\n"
            "assert {'Recency', 'Frequency', 'Monetary'} <= set(rfm.columns)\n"
            "print(rfm.head())"
        ),
        md("## 2. Добавляем `share_card`"),
        code(
            "rfm_plus = None\n"
            "assert rfm_plus is not None\n"
            "assert 'share_card' in rfm_plus.columns\n"
            "assert float(rfm_plus['share_card'].min()) >= 0 and float(rfm_plus['share_card'].max()) <= 1\n"
            "print(rfm_plus[['customer_id', 'share_card']].head())"
        ),
        md("## 3. Добавляем среднюю задержку доставки"),
        code(
            "assert 'avg_days_to_deliver' in rfm_plus.columns\n"
            "n_notna_delay = None\n"
            "assert n_notna_delay is not None and int(n_notna_delay) > 500\n"
            "print('with delivery avg:', n_notna_delay)"
        ),
        md("## 4. Связь Frequency и Monetary"),
        code(
            "corr_fm = None\n"
            "CORR_NOTE = ''\n"
            "assert corr_fm is not None\n"
            "assert -1 <= float(corr_fm) <= 1\n"
            "assert len(CORR_NOTE) > 80\n"
            "print(round(float(corr_fm), 3), CORR_NOTE)"
        ),
        md("## 5. Проверка границ и отсутствие метки churn"),
        code(
            "assert 'churn' not in rfm_plus.columns\n"
            "assert (rfm_plus['Frequency'] >= 1).all()\n"
            "assert (rfm_plus['Monetary'] > 0).all()\n"
            "print(rfm_plus.shape)"
        ),
    )
    hw = nb(
        md("# ДЗ: практикум по агрегатам"),
        code(LOAD_DATA),
        md("### A. Закрепление"),
        md("## 1. Альтернатива: `n_states` на клиента"),
        code(
            "customer_states = None\n"
            "n_states = None\n"
            "assert customer_states is not None and n_states is not None\n"
            "assert int(n_states.max()) >= 1\n"
            "print(n_states.describe())"
        ),
        md("## 2. Ранжирование по композитному score"),
        code(
            "scored = None\n"
            "top10 = None\n"
            "assert scored is not None and top10 is not None and len(top10) == 10\n"
            "print(top10[['customer_id', 'score']])"
        ),
        md("### B. Вызов"),
        md("## 3. Почему нельзя сравнивать несмасштабированные R/F/M"),
        code(
            "SCALE_NOTE = ''\n"
            "assert len(SCALE_NOTE) > 140\n"
            "print(SCALE_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: практикум агрегатов\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        md("## Урок. 1-5"),
        code(
            "orders_pay = orders.merge(payments, on='order_id', how='left')\n"
            "orders_full = orders_pay.merge(customers[['customer_id', 'customer_state']], on='customer_id', how='left')\n"
            "ref_date = orders['order_purchase_timestamp'].max()\n"
            "rfm = (\n"
            "    orders_full.groupby('customer_id')\n"
            "    .agg(\n"
            "        last_purchase=('order_purchase_timestamp', 'max'),\n"
            "        Frequency=('order_id', 'nunique'),\n"
            "        Monetary=('payment_value', 'sum'),\n"
            "    )\n"
            "    .reset_index()\n"
            ")\n"
            "rfm['Recency'] = (ref_date - rfm['last_purchase']).dt.days\n"
            "card_share = orders_full.groupby('customer_id')['payment_type'].apply(lambda s: float((s == 'credit_card').mean()))\n"
            "delivery = orders_full.assign(\n"
            "    days_to_deliver=(orders_full['order_delivered_customer_date'] - orders_full['order_purchase_timestamp']).dt.days\n"
            ").groupby('customer_id')['days_to_deliver'].mean()\n"
            "rfm_plus = rfm.merge(card_share.rename('share_card'), on='customer_id', how='left')\n"
            "rfm_plus = rfm_plus.merge(delivery.rename('avg_days_to_deliver'), on='customer_id', how='left')\n"
            "rfm_plus = rfm_plus[['customer_id', 'Recency', 'Frequency', 'Monetary', 'share_card', 'avg_days_to_deliver']]\n"
            "n_notna_delay = int(rfm_plus['avg_days_to_deliver'].notna().sum())\n"
            "corr_fm = float(rfm_plus['Frequency'].corr(rfm_plus['Monetary']))\n"
            "CORR_NOTE = (\n"
            "    'Связь F и M обычно положительная: больше заказов — выше суммарная выручка. '\n"
            "    'Но корреляция не идеальна, потому что у части клиентов редкие, но дорогие заказы.'\n"
            ")\n"
            "print(rfm_plus.head())\n"
            "print('corr:', round(corr_fm, 3), 'rows with delivery avg:', n_notna_delay)\n"
            "print(CORR_NOTE)"
        ),
        md("## ДЗ. 1-3"),
        code(
            "orders_pay = orders.merge(payments, on='order_id', how='left')\n"
            "orders_full = orders_pay.merge(customers[['customer_id', 'customer_state']], on='customer_id', how='left')\n"
            "ref_date = orders['order_purchase_timestamp'].max()\n"
            "rfm = (\n"
            "    orders_full.groupby('customer_id')\n"
            "    .agg(last_purchase=('order_purchase_timestamp', 'max'), Frequency=('order_id', 'nunique'), Monetary=('payment_value', 'sum'))\n"
            "    .reset_index()\n"
            ")\n"
            "rfm['Recency'] = (ref_date - rfm['last_purchase']).dt.days\n"
            "customer_states = orders_full.groupby('customer_id')['customer_state'].nunique()\n"
            "n_states = customer_states\n"
            "scored = rfm.copy()\n"
            "scored['score'] = scored['Monetary'] / scored['Monetary'].mean() + scored['Frequency'] / scored['Frequency'].mean()\n"
            "top10 = scored.sort_values('score', ascending=False).head(10)\n"
            "SCALE_NOTE = (\n"
            "    'Recency измеряется в днях, Monetary — в денежных единицах, Frequency — в штуках. '\n"
            "    'Если складывать их как есть, признак с большим масштабом доминирует. '\n"
            "    'Перед единым score нужно нормировать или явно задавать веса.'\n"
            ")\n"
            "print(n_states.describe())\n"
            "print(top10[['customer_id', 'score']])\n"
            "print(SCALE_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson05() -> None:
    """Pair 34: logging and raise validation."""
    base = "lessons/05_logging_raise"
    lesson = nb(
        md("# Логирование шагов и `raise` для контракта данных"),
        code(LOAD_DATA),
        md("## 1. Лог шагов обработки"),
        code(
            "log_steps = []\n"
            "# добавьте минимум 5 шагов (строки)\n"
            "assert len(log_steps) >= 5\n"
            "print(log_steps)"
        ),
        md("## 2. Функция валидации"),
        code(
            "def validate_orders(frame):\n"
            "    # ваш код\n"
            "    return True\n\n\n"
            "ok = validate_orders(orders.merge(payments, on='order_id', how='left'))\n"
            "assert ok is True\n"
            "print(ok)"
        ),
        md("## 3. Проверка: отрицательная сумма -> raise"),
        code(
            "bad_row = orders.merge(payments, on='order_id', how='left').head(3).copy()\n"
            "bad_row.loc[bad_row.index[0], 'payment_value'] = -10\n"
            "error_text = ''\n"
            "try:\n"
            "    validate_orders(bad_row)\n"
            "except ValueError as e:\n"
            "    error_text = str(e)\n"
            "assert len(error_text) > 0\n"
            "print(error_text)"
        ),
        md("## 4. Проверка: пропуск даты -> raise"),
        code(
            "bad_dates = orders.merge(payments, on='order_id', how='left').head(5).copy()\n"
            "bad_dates.loc[bad_dates.index[0], 'order_purchase_timestamp'] = pd.NaT\n"
            "error_date = ''\n"
            "try:\n"
            "    validate_orders(bad_dates)\n"
            "except ValueError as e:\n"
            "    error_date = str(e)\n"
            "assert len(error_date) > 0\n"
            "print(error_date)"
        ),
        md("## 5. `LOG_NOTE`"),
        code(
            "LOG_NOTE = ''\n"
            "assert len(LOG_NOTE) > 120\n"
            "print(LOG_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: лог и валидация"),
        code(LOAD_DATA),
        md("### A. Закрепление"),
        md("## 1. Мини-валидатор оплат"),
        code(
            "def validate_payments(frame):\n"
            "    return True\n\n\n"
            "result = validate_payments(payments)\n"
            "assert result is True\n"
            "print(result)"
        ),
        md("## 2. Тест на плохую оплату"),
        code(
            "bad = payments.head(3).copy()\n"
            "bad.loc[bad.index[0], 'payment_value'] = -1\n"
            "msg = ''\n"
            "try:\n"
            "    validate_payments(bad)\n"
            "except ValueError as e:\n"
            "    msg = str(e)\n"
            "assert len(msg) > 0\n"
            "print(msg)"
        ),
        md("### B. Вызов"),
        md("## 3. Почему контракт нужен до модели"),
        code(
            "CONTRACT_NOTE = ''\n"
            "assert len(CONTRACT_NOTE) > 150\n"
            "print(CONTRACT_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: логирование и raise\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        md("## Урок. 1-5"),
        code(
            "orders_pay = orders.merge(payments, on='order_id', how='left')\n"
            "log_steps = [\n"
            "    'loaded orders/customers/payments',\n"
            "    'merged orders with payments by order_id',\n"
            "    'parsed purchase timestamp',\n"
            "    'validated payment_value and mandatory dates',\n"
            "    'ready for feature engineering',\n"
            "]\n\n"
            "def validate_orders(frame):\n"
            "    if (frame['payment_value'] < 0).any():\n"
            "        bad_idx = int(frame.index[frame['payment_value'] < 0][0])\n"
            "        raise ValueError(f'negative payment_value at row {bad_idx}')\n"
            "    if frame['order_purchase_timestamp'].isna().any():\n"
            "        bad_idx = int(frame.index[frame['order_purchase_timestamp'].isna()][0])\n"
            "        raise ValueError(f'missing order_purchase_timestamp at row {bad_idx}')\n"
            "    return True\n\n\n"
            "ok = validate_orders(orders_pay)\n"
            "bad_row = orders_pay.head(3).copy()\n"
            "bad_row.loc[bad_row.index[0], 'payment_value'] = -10\n"
            "try:\n"
            "    validate_orders(bad_row)\n"
            "except ValueError as e:\n"
            "    error_text = str(e)\n"
            "bad_dates = orders_pay.head(5).copy()\n"
            "bad_dates.loc[bad_dates.index[0], 'order_purchase_timestamp'] = pd.NaT\n"
            "try:\n"
            "    validate_orders(bad_dates)\n"
            "except ValueError as e:\n"
            "    error_date = str(e)\n"
            "LOG_NOTE = (\n"
            "    'Лог делает pipeline воспроизводимым: видно порядок шагов и место сбоя. '\n"
            "    'Raise останавливает обработку на невалидных данных до того, как ошибка попадёт в признаки и отчёт.'\n"
            ")\n"
            "print(ok)\n"
            "print(log_steps)\n"
            "print(error_text)\n"
            "print(error_date)\n"
            "print(LOG_NOTE)"
        ),
        md("## ДЗ. 1-3"),
        code(
            "def validate_payments(frame):\n"
            "    if frame['payment_value'].isna().any():\n"
            "        raise ValueError('payment_value has missing values')\n"
            "    if (frame['payment_value'] < 0).any():\n"
            "        raise ValueError('payment_value must be non-negative')\n"
            "    return True\n\n\n"
            "result = validate_payments(payments)\n"
            "bad = payments.head(3).copy()\n"
            "bad.loc[bad.index[0], 'payment_value'] = -1\n"
            "try:\n"
            "    validate_payments(bad)\n"
            "except ValueError as e:\n"
            "    msg = str(e)\n"
            "CONTRACT_NOTE = (\n"
            "    'Контракт фиксирует, какие данные pipeline считает допустимыми. '\n"
            "    'Без этого модель может учиться на испорченных строках, и ошибка проявится позже, '\n"
            "    'когда уже непонятно, на каком шаге она возникла.'\n"
            ")\n"
            "print(result)\n"
            "print(msg)\n"
            "print(CONTRACT_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson06() -> None:
    """Pair 35: preprocessing pipeline."""
    base = "lessons/06_practice_pipeline"
    lesson = nb(
        md("# Практика: функция `preprocess_customers(...)`"),
        code(LOAD_DATA),
        md("## 1. Каркас функции"),
        code(
            "def preprocess_customers(orders_df, customers_df, payments_df):\n"
            "    log = []\n"
            "    features = None\n"
            "    return features, log\n\n\n"
            "features, log = preprocess_customers(orders, customers, payments)\n"
            "assert features is not None and log is not None\n"
            "print(type(features), len(log))"
        ),
        md("## 2. Требования к выходной таблице"),
        code(
            "required_cols = ['customer_id', 'Recency', 'Frequency', 'Monetary', 'share_card', 'avg_days_to_deliver']\n"
            "assert all(c in features.columns for c in required_cols)\n"
            "assert len(features) == 778\n"
            "print(features.head())"
        ),
        md("## 3. Acceptance checklist"),
        code(
            "acceptance = pd.Series(\n"
            "    [False, False, False, False, False],\n"
            "    index=['has_rfm', 'has_extra_features', 'validated_input', 'has_log', 'saved_preview'],\n"
            ")\n"
            "assert bool(acceptance.all())\n"
            "print(acceptance)"
        ),
        md("## 4. Сохранить preview"),
        code(
            "preview_path = 'features_preview.csv'\n"
            "# features.to_csv(preview_path, index=False)\n"
            "saved = None\n"
            "assert saved is True\n"
            "print(preview_path)"
        ),
        md("## 5. Итоговый REPORT"),
        code(
            "REPORT = ''\n"
            "READY = False\n"
            "assert len(REPORT) > 250\n"
            "assert READY is True\n"
            "print(REPORT)"
        ),
    )
    hw = nb(
        md("# ДЗ: улучшение preprocessing pipeline"),
        code(LOAD_DATA),
        md("### A. Закрепление"),
        md("## 1. Повторный запуск функции"),
        code(
            "def preprocess_customers(orders_df, customers_df, payments_df):\n"
            "    return None, []\n\n\n"
            "features, log = preprocess_customers(orders, customers, payments)\n"
            "assert features is not None\n"
            "assert len(log) >= 4\n"
            "print(features.shape, log)"
        ),
        md("## 2. Проверка стабильности результата"),
        code(
            "features2, _ = preprocess_customers(orders, customers, payments)\n"
            "same_shape = None\n"
            "assert same_shape is True\n"
            "print(same_shape)"
        ),
        md("### B. Вызов"),
        md("## 3. Что вынести в следующий модуль"),
        code(
            "NEXT_NOTE = ''\n"
            "assert len(NEXT_NOTE) > 120\n"
            "print(NEXT_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: preprocessing pipeline\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        md("## Урок. 1-5"),
        code(
            "def preprocess_customers(orders_df, customers_df, payments_df):\n"
            "    log = []\n"
            "    orders_local = orders_df.copy()\n"
            "    customers_local = customers_df.copy()\n"
            "    payments_local = payments_df.copy()\n"
            "    log.append('copied input frames')\n"
            "    if (payments_local['payment_value'] < 0).any():\n"
            "        raise ValueError('negative payment_value in payments')\n"
            "    if orders_local['order_purchase_timestamp'].isna().any():\n"
            "        raise ValueError('missing order_purchase_timestamp in orders')\n"
            "    log.append('validated input contracts')\n"
            "    merged = orders_local.merge(payments_local, on='order_id', how='left')\n"
            "    merged = merged.merge(customers_local[['customer_id', 'customer_state']], on='customer_id', how='left')\n"
            "    log.append('merged orders, payments, customers')\n"
            "    merged['days_to_deliver'] = (\n"
            "        merged['order_delivered_customer_date'] - merged['order_purchase_timestamp']\n"
            "    ).dt.days\n"
            "    ref_date = merged['order_purchase_timestamp'].max()\n"
            "    base = (\n"
            "        merged.groupby('customer_id')\n"
            "        .agg(\n"
            "            last_purchase=('order_purchase_timestamp', 'max'),\n"
            "            Frequency=('order_id', 'nunique'),\n"
            "            Monetary=('payment_value', 'sum'),\n"
            "            avg_days_to_deliver=('days_to_deliver', 'mean'),\n"
            "        )\n"
            "        .reset_index()\n"
            "    )\n"
            "    base['Recency'] = (ref_date - base['last_purchase']).dt.days\n"
            "    share_card = merged.groupby('customer_id')['payment_type'].apply(\n"
            "        lambda s: float((s == 'credit_card').mean())\n"
            "    )\n"
            "    features = base.merge(share_card.rename('share_card'), on='customer_id', how='left')\n"
            "    features = features[['customer_id', 'Recency', 'Frequency', 'Monetary', 'share_card', 'avg_days_to_deliver']]\n"
            "    log.append('built customer features RFM + extras')\n"
            "    return features, log\n\n\n"
            "features, log = preprocess_customers(orders, customers, payments)\n"
            "required_cols = ['customer_id', 'Recency', 'Frequency', 'Monetary', 'share_card', 'avg_days_to_deliver']\n"
            "acceptance = pd.Series(\n"
            "    [\n"
            "        all(c in features.columns for c in required_cols),\n"
            "        {'share_card', 'avg_days_to_deliver'} <= set(features.columns),\n"
            "        any('validated' in step for step in log),\n"
            "        len(log) >= 4,\n"
            "        False,\n"
            "    ],\n"
            "    index=['has_rfm', 'has_extra_features', 'validated_input', 'has_log', 'saved_preview'],\n"
            ")\n"
            "preview_path = Path('features_preview.csv')\n"
            "features.to_csv(preview_path, index=False)\n"
            "acceptance.loc['saved_preview'] = preview_path.exists()\n"
            "REPORT = (\n"
            "    f'Собран preprocessing для {len(features)} клиентов на slim-данных заказов. '\n"
            "    'Контракт входа проверяет отрицательные оплаты и пропуски даты покупки. '\n"
            "    'На выходе таблица клиентских признаков: Recency, Frequency, Monetary, доля card и средняя задержка доставки. '\n"
            "    'Лог фиксирует ключевые шаги и позволяет воспроизвести результат. '\n"
            "    'Preview сохранён в features_preview.csv; модель в этом модуле не обучается.'\n"
            ")\n"
            "READY = bool(acceptance.all())\n"
            "print(features.head())\n"
            "print(log)\n"
            "print(acceptance)\n"
            "print('READY:', READY)"
        ),
        md("## ДЗ. 1-3"),
        code(
            "def preprocess_customers(orders_df, customers_df, payments_df):\n"
            "    log = []\n"
            "    orders_local = orders_df.copy()\n"
            "    payments_local = payments_df.copy()\n"
            "    if (payments_local['payment_value'] < 0).any():\n"
            "        raise ValueError('negative payment_value')\n"
            "    log.append('validated payments')\n"
            "    merged = orders_local.merge(payments_local, on='order_id', how='left')\n"
            "    log.append('merged orders-payments')\n"
            "    ref_date = merged['order_purchase_timestamp'].max()\n"
            "    features = (\n"
            "        merged.groupby('customer_id')\n"
            "        .agg(last_purchase=('order_purchase_timestamp', 'max'), Frequency=('order_id', 'nunique'), Monetary=('payment_value', 'sum'))\n"
            "        .reset_index()\n"
            "    )\n"
            "    features['Recency'] = (ref_date - features['last_purchase']).dt.days\n"
            "    features = features[['customer_id', 'Recency', 'Frequency', 'Monetary']]\n"
            "    log.append('built base RFM')\n"
            "    return features, log\n\n\n"
            "features, log = preprocess_customers(orders, customers, payments)\n"
            "features2, _ = preprocess_customers(orders, customers, payments)\n"
            "same_shape = features.shape == features2.shape\n"
            "NEXT_NOTE = (\n"
            "    'В следующий модуль стоит вынести масштабирование и выбор признаков под конкретную модель, '\n"
            "    'а также автоматическую проверку качества на train/validation. '\n"
            "    'Текущий шаг уже даёт стабильную инженерную заготовку признаков.'\n"
            ")\n"
            "print(features.shape, log)\n"
            "print('same shape:', same_shape)\n"
            "print(NEXT_NOTE)"
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
    required = [ORDERS_CSV, CUSTOMERS_CSV, PAYMENTS_CSV]
    missing = [p for p in required if not p.exists()]
    if missing:
        raise SystemExit(f"Missing CSV files: {missing}")
    for builder in BUILDERS:
        builder()
    for rel, notebook in NOTEBOOKS.items():
        write(rel, notebook)
    for d in LESSON_DIRS:
        copy_csv(d)
    print(f"done: {len(NOTEBOOKS)} notebooks in {len(LESSON_DIRS)} lessons")


if __name__ == "__main__":
    main()
