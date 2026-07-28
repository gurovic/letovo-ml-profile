#!/usr/bin/env python3
"""Generate lesson notebooks for module 08_10 (KTP pairs 60-64)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_CSV = ROOT / "data" / "bank_marketing_slim.csv"

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
    "CSV_PATH = _find('bank_marketing_slim.csv')\n"
    "df = pd.read_csv(CSV_PATH)\n"
    "target = (df['y'] == 'yes').astype(int)\n"
)


def md(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "source": source.splitlines(keepends=True),
        "outputs": [],
        "execution_count": None,
    }


def nb(*cells: dict) -> dict:
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
    base = "lessons/01_logreg_sigmoid_threshold"
    lesson = nb(
        md("# Логистическая регрессия: сигмоида, вероятность, порог"),
        code(LOAD_DATA + "\nyes_share = float(target.mean())\nprint('rows=', len(df), 'yes_share=', round(yes_share, 4))"),
        md("## 1. Зафиксировать leakage-правило: `duration` запрещен в признаках"),
        code(
            "candidate_features = [c for c in df.columns if c != 'y']\n"
            "feature_columns = None\n"
            "assert feature_columns is not None\n"
            "assert 'duration' not in feature_columns\n"
            "assert set(feature_columns).issubset(set(candidate_features))\n"
            "print(feature_columns[:6])"
        ),
        md("## 2. Реализовать сигмоиду"),
        code(
            "def sigmoid(z):\n"
            "    return None\n\n\n"
            "vals = np.array([-2.0, 0.0, 2.0])\n"
            "probs = sigmoid(vals)\n"
            "assert probs is not None\n"
            "assert np.all((probs > 0) & (probs < 1))\n"
            "assert abs(float(sigmoid(0.0)) - 0.5) < 1e-9\n"
            "print(probs)"
        ),
        md("## 3. Порог: вероятности -> метки"),
        code(
            "sample_proba = np.array([0.11, 0.37, 0.49, 0.51, 0.88])\n"
            "pred_05 = None\n"
            "pred_03 = None\n"
            "assert pred_05 is not None and pred_03 is not None\n"
            "assert list(pred_05) == [0, 0, 0, 1, 1]\n"
            "assert list(pred_03) == [0, 1, 1, 1, 1]\n"
            "print(pred_05, pred_03)"
        ),
        md("## 4. Короткий вывод"),
        code(
            "LEAKAGE_NOTE = ''\n"
            "assert 'duration' in LEAKAGE_NOTE.lower()\n"
            "assert len(LEAKAGE_NOTE) > 140\n"
            "print(LEAKAGE_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: порог и leakage"),
        code(LOAD_DATA),
        md("### A. Закрепление\n\n## 1. Посчитать долю positive при разных порогах"),
        code(
            "proba_demo = np.array([0.05, 0.16, 0.22, 0.41, 0.61, 0.74, 0.93])\n"
            "share_04 = None\n"
            "share_07 = None\n"
            "assert share_04 is not None and share_07 is not None\n"
            "assert 0.0 <= share_04 <= 1.0 and 0.0 <= share_07 <= 1.0\n"
            "assert share_04 >= share_07\n"
            "print(share_04, share_07)"
        ),
        md("## 2. Сформулировать правило по features"),
        code(
            "RULE = ''\n"
            "assert 'duration' in RULE.lower()\n"
            "assert len(RULE) > 120\n"
            "print(RULE)"
        ),
        md("### B. Вызов\n\n## 3. Почему высокий recall может быть полезен в кампании"),
        code(
            "RECALL_NOTE = ''\n"
            "assert len(RECALL_NOTE) > 150\n"
            "print(RECALL_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: сигмоида и порог\n\n" + SOL_BANNER),
        code(LOAD_DATA),
        code(
            "candidate_features = [c for c in df.columns if c != 'y']\n"
            "feature_columns = [c for c in candidate_features if c != 'duration']\n"
            "assert 'duration' not in feature_columns\n\n\n"
            "def sigmoid(z):\n"
            "    arr = np.asarray(z, dtype=float)\n"
            "    return 1.0 / (1.0 + np.exp(-arr))\n\n\n"
            "vals = np.array([-2.0, 0.0, 2.0])\n"
            "probs = sigmoid(vals)\n"
            "sample_proba = np.array([0.11, 0.37, 0.49, 0.51, 0.88])\n"
            "pred_05 = (sample_proba >= 0.50).astype(int)\n"
            "pred_03 = (sample_proba >= 0.30).astype(int)\n"
            "LEAKAGE_NOTE = (\n"
            "    'Столбец duration нельзя использовать в признаках: это значение известно только после звонка, '\n"
            "    'поэтому модель с ним не переносится в реальный процесс кампании.'\n"
            ")\n"
            "proba_demo = np.array([0.05, 0.16, 0.22, 0.41, 0.61, 0.74, 0.93])\n"
            "share_04 = float((proba_demo >= 0.4).mean())\n"
            "share_07 = float((proba_demo >= 0.7).mean())\n"
            "RULE = 'Перед fit формируем feature_columns и явно исключаем duration; проверяем это через assert.'\n"
            "RECALL_NOTE = (\n"
            "    'При ограниченном бюджете обзвона высокий recall помогает не потерять потенциальные yes-кейсы, '\n"
            "    'если команда готова принять больше ложных срабатываний и потом фильтровать их бизнес-правилами.'\n"
            ")\n"
            "print('features:', feature_columns[:8])\n"
            "print('sigmoid:', probs)\n"
            "print('pred_05=', pred_05, 'pred_03=', pred_03)\n"
            "print('share_04=', share_04, 'share_07=', share_07)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson02() -> None:
    base = "lessons/02_practice_fit_threshold"
    lesson = nb(
        md("# Практика: fit/predict и выбор порога"),
        code(
            LOAD_DATA
            + "\nfrom sklearn.linear_model import LogisticRegression\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import precision_score, recall_score, f1_score\n"
        ),
        md("## 1. Подготовить X без `duration` и разбить train/test"),
        code(
            "feature_columns = [c for c in df.columns if c not in ('y', 'duration')]\n"
            "X = None\n"
            "X_train, X_test, y_train, y_test = None, None, None, None\n"
            "assert X is not None\n"
            "assert 'duration' not in X.columns\n"
            "assert X_train is not None and X_test is not None\n"
            "print(X_train.shape, X_test.shape)"
        ),
        md("## 2. Обучить LogisticRegression"),
        code(
            "model = None\n"
            "assert model is not None\n"
            "proba_test = model.predict_proba(X_test)[:, 1]\n"
            "assert len(proba_test) == len(y_test)\n"
            "print(proba_test[:5])"
        ),
        md("## 3. Сравнить пороги 0.3 / 0.5 / 0.7"),
        code(
            "rows = []\n"
            "for thr in (0.3, 0.5, 0.7):\n"
            "    pred = None\n"
            "    # rows.append({'threshold': thr, 'precision': ..., 'recall': ..., 'f1': ...})\n"
            "\n"
            "table = pd.DataFrame(rows)\n"
            "assert len(table) == 3\n"
            "assert {'threshold', 'precision', 'recall', 'f1'} <= set(table.columns)\n"
            "print(table)"
        ),
    )
    hw = nb(
        md("# ДЗ: подбор порога под цель recall"),
        code(
            LOAD_DATA
            + "\nfrom sklearn.linear_model import LogisticRegression\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import precision_score, recall_score, f1_score\n"
        ),
        md("### A. Закрепление\n\n## 1. Найти минимальный порог с recall >= 0.70"),
        code(
            "best_threshold = None\n"
            "best_row = None\n"
            "assert best_threshold is not None and best_row is not None\n"
            "assert 0.10 <= best_threshold <= 0.90\n"
            "assert float(best_row['recall']) >= 0.70\n"
            "print(best_threshold, best_row)"
        ),
        md("### B. Вызов\n\n## 2. Короткая рекомендация для команды обзвона"),
        code(
            "TEAM_NOTE = ''\n"
            "assert len(TEAM_NOTE) > 150\n"
            "print(TEAM_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: fit и порог\n\n" + SOL_BANNER),
        code(
            LOAD_DATA
            + "\nfrom sklearn.linear_model import LogisticRegression\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import precision_score, recall_score, f1_score\n"
        ),
        code(
            "feature_columns = [c for c in df.columns if c not in ('y', 'duration')]\n"
            "X_raw = pd.get_dummies(df[feature_columns], drop_first=True)\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X_raw, target, test_size=0.25, random_state=61, stratify=target\n"
            ")\n"
            "model = LogisticRegression(max_iter=1200)\n"
            "model.fit(X_train, y_train)\n"
            "proba_test = model.predict_proba(X_test)[:, 1]\n"
            "rows = []\n"
            "for thr in (0.3, 0.5, 0.7):\n"
            "    pred = (proba_test >= thr).astype(int)\n"
            "    rows.append(\n"
            "        {\n"
            "            'threshold': thr,\n"
            "            'precision': float(precision_score(y_test, pred, zero_division=0)),\n"
            "            'recall': float(recall_score(y_test, pred, zero_division=0)),\n"
            "            'f1': float(f1_score(y_test, pred, zero_division=0)),\n"
            "        }\n"
            "    )\n"
            "table = pd.DataFrame(rows)\n"
            "best_threshold = None\n"
            "best_row = None\n"
            "for row in rows:\n"
            "    if row['recall'] >= 0.70:\n"
            "        best_threshold = row['threshold']\n"
            "        best_row = row\n"
            "        break\n"
            "if best_threshold is None:\n"
            "    best_threshold = rows[0]['threshold']\n"
            "    best_row = rows[0]\n"
            "TEAM_NOTE = (\n"
            "    f'Для пилота выбираем threshold={best_threshold:.2f}: recall={best_row['recall']:.3f}, '\n"
            "    f'precision={best_row['precision']:.3f}. Это снижает риск пропуска заинтересованных клиентов '\n"
            "    'при контролируемом росте ложных срабатываний.'\n"
            ")\n"
            "print(table)\n"
            "print('best_threshold=', best_threshold)\n"
            "print(TEAM_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson03() -> None:
    base = "lessons/03_imbalance_metrics"
    lesson = nb(
        md("# Дисбаланс и метрики: accuracy vs precision/recall/F1"),
        code(
            LOAD_DATA
            + "\nfrom sklearn.linear_model import LogisticRegression\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix\n"
        ),
        md("## 1. Baseline: всегда предсказывать `no`"),
        code(
            "y_true = target.to_numpy()\n"
            "baseline_pred = None\n"
            "acc_base = None\n"
            "recall_base = None\n"
            "assert baseline_pred is not None\n"
            "assert abs(float(recall_base)) < 1e-9\n"
            "print('acc_base=', acc_base, 'recall_base=', recall_base)"
        ),
        md("## 2. LogisticRegression без `duration`"),
        code(
            "feature_columns = [c for c in df.columns if c not in ('y', 'duration')]\n"
            "X = pd.get_dummies(df[feature_columns], drop_first=True)\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, target, test_size=0.25, random_state=62, stratify=target)\n"
            "model = LogisticRegression(max_iter=1200)\n"
            "model.fit(X_train, y_train)\n"
            "proba = model.predict_proba(X_test)[:, 1]\n"
            "pred = (proba >= 0.50).astype(int)\n"
            "assert len(pred) == len(y_test)\n"
            "print('pred_yes_share=', float(pred.mean()))"
        ),
        md("## 3. Матрица ошибок и метрики"),
        code(
            "cm = None\n"
            "metrics = None\n"
            "assert cm is not None and metrics is not None\n"
            "assert {'accuracy', 'precision', 'recall', 'f1'} <= set(metrics)\n"
            "print(cm)\n"
            "print(metrics)"
        ),
        md("## 4. Почему accuracy недостаточна"),
        code(
            "IMBALANCE_NOTE = ''\n"
            "assert len(IMBALANCE_NOTE) > 150\n"
            "print(IMBALANCE_NOTE)"
        ),
    )
    hw = nb(
        md("# ДЗ: сравнение порогов по F1"),
        code(
            LOAD_DATA
            + "\nfrom sklearn.linear_model import LogisticRegression\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import precision_score, recall_score, f1_score\n"
        ),
        md("### A. Закрепление\n\n## 1. Таблица метрик для порогов 0.2..0.8"),
        code(
            "thresholds = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]\n"
            "table = pd.DataFrame()\n"
            "assert len(table) == len(thresholds)\n"
            "assert {'threshold', 'precision', 'recall', 'f1'} <= set(table.columns)\n"
            "print(table)"
        ),
        md("### B. Вызов\n\n## 2. Выбрать порог по F1 и пояснить"),
        code(
            "best_thr = None\n"
            "NOTE = ''\n"
            "assert best_thr is not None\n"
            "assert len(NOTE) > 140\n"
            "print(best_thr)\n"
            "print(NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: дисбаланс и метрики\n\n" + SOL_BANNER),
        code(
            LOAD_DATA
            + "\nfrom sklearn.linear_model import LogisticRegression\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix\n"
        ),
        code(
            "y_true = target.to_numpy()\n"
            "baseline_pred = np.zeros_like(y_true)\n"
            "acc_base = float(accuracy_score(y_true, baseline_pred))\n"
            "recall_base = float(recall_score(y_true, baseline_pred, zero_division=0))\n"
            "feature_columns = [c for c in df.columns if c not in ('y', 'duration')]\n"
            "X = pd.get_dummies(df[feature_columns], drop_first=True)\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X, target, test_size=0.25, random_state=62, stratify=target\n"
            ")\n"
            "model = LogisticRegression(max_iter=1200)\n"
            "model.fit(X_train, y_train)\n"
            "proba = model.predict_proba(X_test)[:, 1]\n"
            "pred = (proba >= 0.50).astype(int)\n"
            "cm = confusion_matrix(y_test, pred)\n"
            "metrics = {\n"
            "    'accuracy': float(accuracy_score(y_test, pred)),\n"
            "    'precision': float(precision_score(y_test, pred, zero_division=0)),\n"
            "    'recall': float(recall_score(y_test, pred, zero_division=0)),\n"
            "    'f1': float(f1_score(y_test, pred, zero_division=0)),\n"
            "}\n"
            "rows = []\n"
            "for thr in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:\n"
            "    cur = (proba >= thr).astype(int)\n"
            "    rows.append(\n"
            "        {\n"
            "            'threshold': thr,\n"
            "            'precision': float(precision_score(y_test, cur, zero_division=0)),\n"
            "            'recall': float(recall_score(y_test, cur, zero_division=0)),\n"
            "            'f1': float(f1_score(y_test, cur, zero_division=0)),\n"
            "        }\n"
            "    )\n"
            "table = pd.DataFrame(rows)\n"
            "best_idx = int(table['f1'].idxmax())\n"
            "best_thr = float(table.loc[best_idx, 'threshold'])\n"
            "IMBALANCE_NOTE = (\n"
            "    'На дисбалансе accuracy может выглядеть высокой даже у модели, которая почти всегда говорит no. '\n"
            "    'Поэтому порог выбираем по precision/recall/F1 и проверяем матрицу ошибок.'\n"
            ")\n"
            "NOTE = (\n"
            "    f'По F1 лучшим оказался порог {best_thr:.2f}; он даёт баланс между пропусками yes и ложными срабатываниями. '\n"
            "    'Для бизнес-решения дополнительно смотрим recall как риск недозвона целевых клиентов.'\n"
            ")\n"
            "print('baseline acc=', acc_base, 'baseline recall=', recall_base)\n"
            "print('cm=\\n', cm)\n"
            "print(metrics)\n"
            "print(table)\n"
            "print(NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson04() -> None:
    base = "lessons/04_practice_metrics_cli"
    lesson = nb(
        md("# Практика CLI: запуск `train_cli.py` и проверка метрик"),
        code("import json\nimport subprocess\nimport sys\nfrom pathlib import Path"),
        md("## 1. Собрать команду запуска"),
        code(
            "script = Path('train_cli.py')\n"
            "data_path = Path('../../data/bank_marketing_slim.csv')\n"
            "cmd = None\n"
            "assert script.exists(), script\n"
            "assert data_path.exists(), data_path\n"
            "assert cmd is not None\n"
            "print(cmd)"
        ),
        md("## 2. Выполнить CLI и распарсить JSON"),
        code(
            "proc = None\n"
            "metrics = None\n"
            "assert proc is not None and metrics is not None\n"
            "assert proc.returncode == 0\n"
            "assert 'duration_in_features' in metrics\n"
            "assert metrics['duration_in_features'] is False\n"
            "print(metrics)"
        ),
        md("## 3. Acceptance чек-лист"),
        code(
            "ok = None\n"
            "assert ok is True\n"
            "print('CLI_OK=', ok)"
        ),
    )
    hw = nb(
        md("# ДЗ: сравнить пороги через CLI"),
        code("import json\nimport subprocess\nimport sys\nfrom pathlib import Path"),
        md("### A. Закрепление\n\n## 1. Запустить CLI для двух порогов"),
        code(
            "script = Path('train_cli.py')\n"
            "data_path = Path('../../data/bank_marketing_slim.csv')\n"
            "results = {}\n"
            "for thr in (0.35, 0.55):\n"
            "    pass\n"
            "assert set(results) == {0.35, 0.55}\n"
            "assert all('f1' in v for v in results.values())\n"
            "print(results)"
        ),
        md("### B. Вызов\n\n## 2. Рекомендация по порогу"),
        code(
            "CLI_NOTE = ''\n"
            "assert len(CLI_NOTE) > 140\n"
            "print(CLI_NOTE)"
        ),
    )
    sol = nb(
        md("# Решения: CLI-практика\n\n" + SOL_BANNER),
        code("import json\nimport subprocess\nimport sys\nfrom pathlib import Path"),
        code(
            "script = Path('train_cli.py')\n"
            "data_path = Path('../../data/bank_marketing_slim.csv')\n"
            "cmd = [\n"
            "    sys.executable,\n"
            "    str(script),\n"
            "    '--data',\n"
            "    str(data_path),\n"
            "    '--threshold',\n"
            "    '0.45',\n"
            "]\n"
            "proc = subprocess.run(cmd, capture_output=True, text=True, check=False)\n"
            "if proc.returncode != 0:\n"
            "    raise RuntimeError(proc.stderr or proc.stdout)\n"
            "metrics = json.loads(proc.stdout)\n"
            "ok = bool(\n"
            "    (not metrics['duration_in_features'])\n"
            "    and 0.0 <= metrics['accuracy'] <= 1.0\n"
            "    and 0.0 <= metrics['precision'] <= 1.0\n"
            "    and 0.0 <= metrics['recall'] <= 1.0\n"
            "    and 0.0 <= metrics['f1'] <= 1.0\n"
            ")\n"
            "results = {}\n"
            "for thr in (0.35, 0.55):\n"
            "    cmd_thr = [sys.executable, str(script), '--data', str(data_path), '--threshold', str(thr)]\n"
            "    proc_thr = subprocess.run(cmd_thr, capture_output=True, text=True, check=False)\n"
            "    if proc_thr.returncode != 0:\n"
            "        raise RuntimeError(proc_thr.stderr or proc_thr.stdout)\n"
            "    results[thr] = json.loads(proc_thr.stdout)\n"
            "better_thr = 0.35 if results[0.35]['f1'] >= results[0.55]['f1'] else 0.55\n"
            "CLI_NOTE = (\n"
            "    f'CLI-проверка показала, что threshold={better_thr:.2f} даёт лучший F1 на test. '\n"
            "    'Команда запуска воспроизводима, а запрет duration зафиксирован в самом скрипте через assert.'\n"
            ")\n"
            "print(metrics)\n"
            "print(results)\n"
            "print('CLI_OK=', ok)\n"
            "print(CLI_NOTE)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


def add_lesson05() -> None:
    base = "lessons/05_venv_requirements_readme"
    lesson = nb(
        md("# venv, requirements.txt и README эксперимента"),
        code(
            "import json\n"
            "import subprocess\n"
            "import sys\n"
            "from pathlib import Path\n"
            "from importlib.metadata import PackageNotFoundError, version\n"
        ),
        md("## 1. Чек-лист команд venv"),
        code(
            "venv_commands = None\n"
            "assert venv_commands is not None\n"
            "assert len(venv_commands) >= 4\n"
            "assert any('python -m venv .venv' in c for c in venv_commands)\n"
            "print('\\n'.join(venv_commands))"
        ),
        md("## 2. Сформировать requirements.txt (минимум numpy/pandas/scikit-learn)"),
        code(
            "requirements_text = None\n"
            "assert requirements_text is not None\n"
            "assert 'numpy' in requirements_text\n"
            "assert 'pandas' in requirements_text\n"
            "assert 'scikit-learn' in requirements_text\n"
            "print(requirements_text)"
        ),
        md("## 3. Подтянуть метрики из CLI и написать README эксперимента"),
        code(
            "exp_readme = ''\n"
            "assert 'duration' in exp_readme.lower()\n"
            "assert 'threshold' in exp_readme.lower()\n"
            "assert len(exp_readme) > 350\n"
            "print(exp_readme[:500])"
        ),
    )
    hw = nb(
        md("# ДЗ: финальная упаковка артефакта"),
        code("from pathlib import Path"),
        md("### A. Закрепление\n\n## 1. Создать шаблон структуры сдачи"),
        code(
            "tree_text = ''\n"
            "assert 'requirements.txt' in tree_text\n"
            "assert 'README.md' in tree_text\n"
            "assert len(tree_text) > 90\n"
            "print(tree_text)"
        ),
        md("### B. Вызов\n\n## 2. Риски воспроизводимости"),
        code(
            "RISKS = ''\n"
            "assert len(RISKS) > 160\n"
            "print(RISKS)"
        ),
    )
    sol = nb(
        md("# Решения: venv и README\n\n" + SOL_BANNER),
        code(
            "import json\n"
            "import subprocess\n"
            "import sys\n"
            "from pathlib import Path\n"
            "from importlib.metadata import PackageNotFoundError, version\n"
        ),
        code(
            "venv_commands = [\n"
            "    'python -m venv .venv',\n"
            "    '.venv\\\\Scripts\\\\activate  # Windows',\n"
            "    'python -m pip install -U pip',\n"
            "    'python -m pip install -r requirements.txt',\n"
            "]\n\n"
            "def pkg_line(pkg_name: str, alias: str | None = None) -> str:\n"
            "    try:\n"
            "        return f'{alias or pkg_name}=={version(pkg_name)}'\n"
            "    except PackageNotFoundError:\n"
            "        return f'{alias or pkg_name}>=0'\n\n\n"
            "requirements_text = '\\n'.join(\n"
            "    [\n"
            "        pkg_line('numpy'),\n"
            "        pkg_line('pandas'),\n"
            "        pkg_line('scikit-learn'),\n"
            "    ]\n"
            ") + '\\n'\n"
            "cli_script = Path('../04_practice_metrics_cli/train_cli.py')\n"
            "data_path = Path('../../data/bank_marketing_slim.csv')\n"
            "cmd = [sys.executable, str(cli_script), '--data', str(data_path), '--threshold', '0.45']\n"
            "proc = subprocess.run(cmd, capture_output=True, text=True, check=False)\n"
            "if proc.returncode != 0:\n"
            "    raise RuntimeError(proc.stderr or proc.stdout)\n"
            "metrics = json.loads(proc.stdout)\n"
            "exp_readme = (\n"
            "    '# Эксперимент: отклик на депозит (LogisticRegression)\\n\\n'\n"
            "    '## Цель\\n'\n"
            "    'Спрогнозировать `y` (yes/no) на срезе UCI Bank Marketing и выбрать рабочий порог.\\n\\n'\n"
            "    '## Leakage rule\\n'\n"
            "    'Столбец `duration` исключён из признаков (`assert duration not in features`).\\n\\n'\n"
            "    '## Запуск\\n'\n"
            "    '1. Создать venv.\\n'\n"
            "    '2. Установить зависимости из requirements.txt.\\n'\n"
            "    '3. Запустить CLI: `python train_cli.py --data ../../data/bank_marketing_slim.csv --threshold 0.45`.\\n\\n'\n"
            "    '## Результаты test\\n'\n"
            "    f\"- threshold: {metrics['threshold']:.2f}\\\\n\"\n"
            "    f\"- accuracy: {metrics['accuracy']:.3f}\\\\n\"\n"
            "    f\"- precision: {metrics['precision']:.3f}\\\\n\"\n"
            "    f\"- recall: {metrics['recall']:.3f}\\\\n\"\n"
            "    f\"- f1: {metrics['f1']:.3f}\\\\n\\n\"\n"
            "    '## Ограничения\\n'\n"
            "    'Это учебный slim-срез; порог и метрики требуют пересчёта на полном контуре данных.'\n"
            ")\n"
            "tree_text = (\n"
            "    'submission/\\n'\n"
            "    '  train_cli.py\\n'\n"
            "    '  requirements.txt\\n'\n"
            "    '  README.md\\n'\n"
            "    '  metrics.json\\n'\n"
            ")\n"
            "RISKS = (\n"
            "    'Без зафиксированных версий пакетов и явной инструкции по запуску коллега может получить другие метрики. '\n"
            "    'Второй риск - случайно добавить duration в признаки и получить нереалистично хороший результат.'\n"
            ")\n"
            "print('\\n'.join(venv_commands))\n"
            "print(requirements_text)\n"
            "print(exp_readme[:500])\n"
            "print(tree_text)\n"
            "print(RISKS)"
        ),
    )
    NOTEBOOKS[f"{base}/lesson.ipynb"] = lesson
    NOTEBOOKS[f"{base}/homework.ipynb"] = hw
    NOTEBOOKS[f"{base}/solutions.ipynb"] = sol


BUILDERS = [add_lesson01, add_lesson02, add_lesson03, add_lesson04, add_lesson05]


def main() -> None:
    if not DATA_CSV.exists():
        raise SystemExit(f"Missing {DATA_CSV}. Run data/make_bank_marketing_slim.py first.")
    for builder in BUILDERS:
        builder()
    for rel_path, notebook in NOTEBOOKS.items():
        write(rel_path, notebook)
    print(f"done: {len(NOTEBOOKS)} notebooks in 5 lessons")


if __name__ == "__main__":
    main()
