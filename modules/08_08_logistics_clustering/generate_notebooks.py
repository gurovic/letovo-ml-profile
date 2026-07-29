#!/usr/bin/env python3
"""Generate the 18 student/teacher notebooks for module 08_08.

The generator is the source of truth.  Student notebooks contain unfinished
work plus executable contracts; teacher notebooks mirror every section.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_CSV = ROOT / "data" / "orders_slim.csv"

LESSON_DIRS = [
    "lessons/01_stack_queue_deque",
    "lessons/02_practice_buffers",
    "lessons/03_set_dict_freq",
    "lessons/04_practice_membership_counts",
    "lessons/05_kmeans_dbscan",
    "lessons/06_practice_clusters_anomalies",
]

LOAD_DATA = """from pathlib import Path
import numpy as np
import pandas as pd


def find_orders_csv() -> Path:
    for path in (Path("orders_slim.csv"), Path("../../data/orders_slim.csv")):
        if path.exists():
            return path.resolve()
    raise FileNotFoundError(
        "orders_slim.csv не найден рядом с ноутбуком или в ../../data/"
    )


CSV_PATH = find_orders_csv()
DATE_COLUMNS = [
    "order_purchase_timestamp",
    "order_estimated_delivery_date",
    "order_delivered_customer_date",
]
df = pd.read_csv(CSV_PATH, parse_dates=DATE_COLUMNS)
assert len(df) > 0
assert df["order_id"].notna().all()
print(f"Загружено заказов: {len(df)}")
"""

CLUSTER_IMPORTS = """
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler

FEATURES = ["delivery_days", "freight_value", "delay_days"]
"""

SOL_BANNER = (
    "**Для преподавателя.** Полный эталон к `lesson.ipynb` и "
    "`homework.ipynb`; ученикам до сдачи не показывать."
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


def nb(cells: list[dict]) -> dict:
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": cells,
    }


def student_notebook(title: str, setup: str, sections: list[tuple[str, str]]) -> dict:
    cells = [md(f"# {title}"), code(setup)]
    for text, source in sections:
        cells.extend((md(text), code(source)))
    return nb(cells)


def solution_notebook(
    title: str, setup: str, sections: list[tuple[str, str]]
) -> dict:
    cells = [md(f"# Решения: {title}\n\n{SOL_BANNER}"), code(setup)]
    for heading, source in sections:
        cells.extend((md(heading), code(source)))
    return nb(cells)


def write(relative: str, notebook: dict) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {relative}: {len(notebook['cells'])} cells")


def add(base: str, lesson: dict, homework: dict, solutions: dict) -> None:
    write(f"{base}/lesson.ipynb", lesson)
    write(f"{base}/homework.ipynb", homework)
    write(f"{base}/solutions.ipynb", solutions)


def lesson01() -> None:
    base = LESSON_DIRS[0]
    setup = LOAD_DATA + "\nfrom collections import deque\n"
    lesson = student_notebook(
        "Stack, queue и deque: смысл операций",
        setup,
        [
            (
                "## 1. Поток событий\n\n"
                "Возьмите первые 12 заказов. Для каждого сохраните кортеж "
                "`(order_id, action)`, где action — `late_review` или `standard`.",
                """events = None  # TODO: список из 12 кортежей
assert isinstance(events, list) and len(events) == min(12, len(df))
assert all(isinstance(item, tuple) and len(item) == 2 for item in events)
assert {item[1] for item in events} <= {"late_review", "standard"}
print(events[:3])
""",
            ),
            (
                "## 2. Stack: последнее действие отменяется первым\n\n"
                "Добавьте четыре шага подготовки в список `history`. Снимите "
                "последний шаг методом `pop()` в `undone`.",
                """steps = ["load", "drop_missing", "make_delay", "scale"]
history = []  # TODO
undone = None  # TODO
assert history == steps[:-1]
assert undone == "scale"
print("осталось:", history, "| отменено:", undone)
""",
            ),
            (
                "## 3. Функция undo\n\n"
                "Реализуйте `undo(stack)`: пустой stack возвращает `None`, "
                "непустой — удаляет и возвращает последний элемент.",
                """def undo(stack):
    # TODO
    ...


trial = ["load", "filter"]
removed = undo(trial)
assert removed == "filter" and trial == ["load"]
assert undo([]) is None
""",
            ),
            (
                "## 4. Queue: первый пришёл — первый обработан\n\n"
                "Переложите ids событий в `deque`, затем обработайте три через "
                "`popleft()`. Порядок должен совпасть с входом.",
                """queue = deque()  # TODO
processed = []  # TODO
assert len(processed) == min(3, len(events))
assert processed == [item[0] for item in events[:3]]
assert len(queue) == len(events) - len(processed)
print(processed)
""",
            ),
            (
                "## 5. Deque: срочное событие в начало\n\n"
                "Создайте очередь из обычных ids. Один late-id добавьте слева "
                "методом `appendleft`; он должен стать следующим.",
                """normal_ids = df.loc[df["is_late"].eq(0), "order_id"].head(5).tolist()
late_id = df.loc[df["is_late"].eq(1), "order_id"].iloc[0]
dispatch = None  # TODO: deque
next_id = None  # TODO: снять слева
assert isinstance(dispatch, deque)
assert next_id == late_id
assert list(dispatch) == normal_ids
""",
            ),
            (
                "## 6. Ограниченный буфер\n\n"
                "`deque(maxlen=5)` хранит только пять последних событий. "
                "Пропустите через него все ids и сохраните снимок.",
                """recent = deque(maxlen=5)
# TODO: append каждого order_id
snapshot = None  # TODO: обычный list
assert snapshot == df["order_id"].tail(min(5, len(df))).tolist()
assert recent.maxlen == 5
print(snapshot)
""",
            ),
            (
                "## 7. Выбор структуры по операции\n\n"
                "Заполните решения ровно словами `stack`, `queue`, `deque`: "
                "отмена шага; честная обработка; срочное добавление с двух концов.",
                """choices = {
    "undo_preprocessing": None,  # TODO
    "fifo_orders": None,         # TODO
    "urgent_both_ends": None,    # TODO
}
assert choices == {
    "undo_preprocessing": "stack",
    "fifo_orders": "queue",
    "urgent_both_ends": "deque",
}
""",
            ),
            (
                "## 8. Эксперимент: нарушенная семантика\n\n"
                "Обработайте одни события слева и справа. В `ORDER_NOTE` "
                "объясните, какой вариант сохраняет порядок поступления.",
                """q_left = deque(item[0] for item in events)
q_right = deque(item[0] for item in events)
left_order = []   # TODO
right_order = []  # TODO
ORDER_NOTE = ""   # TODO: не менее 80 символов
assert left_order == [item[0] for item in events]
assert right_order == list(reversed(left_order))
assert len(ORDER_NOTE) >= 80
print(ORDER_NOTE)
""",
            ),
            (
                "## 9. Самостоятельно: журнал с двумя undo\n\n"
                "Выполните пять шагов, отмените два и верните словарь "
                "`audit` с оставшейся историей и порядком отмены.",
                """pipeline = ["load", "clean", "join", "scale", "cluster"]
audit = None  # TODO
assert isinstance(audit, dict)
assert audit["remaining"] == pipeline[:3]
assert audit["undone"] == ["cluster", "scale"]
""",
            ),
        ],
    )
    homework = student_notebook(
        "ДЗ: stack, queue и deque",
        setup,
        [
            ("### Part A — обязательно\n\n## A1. Полная отмена", "ops = [\"load\", \"clean\", \"scale\", \"cluster\", \"report\"]\nundo_order = []  # TODO\nassert undo_order == list(reversed(ops))\n"),
            ("## A2. FIFO-проверка\n\nПроведите первые 10 ids через очередь.", "source_ids = df[\"order_id\"].head(10).tolist()\nfifo = None  # TODO\nassert fifo == source_ids\n"),
            ("## A3. Сначала late\n\nДве очереди, late обрабатываются раньше normal; внутри групп FIFO.", "late_ids = df.loc[df[\"is_late\"].eq(1), \"order_id\"].head(4).tolist()\nnormal_ids = df.loc[df[\"is_late\"].eq(0), \"order_id\"].head(4).tolist()\npriority_order = None  # TODO\nassert priority_order == late_ids + normal_ids\n"),
            ("### Challenge\n\n## B1. Обобщённый диспетчер\n\nНапишите функцию с двумя deque и лимитом обработки.", """def dispatch_orders(late, normal, limit):
    # TODO: копии входных очередей, late раньше normal
    ...


result = dispatch_orders(deque(late_ids), deque(normal_ids), 5)
assert result == (late_ids + normal_ids)[:5]
assert len(result) <= 5
"""),
            ("## B2. Инженерное обоснование", "STRUCTURE_NOTE = \"\"  # TODO: сравните операции трёх структур\nassert len(STRUCTURE_NOTE) >= 180\nassert all(word in STRUCTURE_NOTE.lower() for word in [\"stack\", \"queue\", \"deque\"])\n"),
        ],
    )
    solutions = solution_notebook(
        "stack, queue и deque",
        setup,
        [
            ("## Урок. 1. Поток событий", "events = [(r.order_id, \"late_review\" if r.is_late else \"standard\") for r in df.head(12).itertuples()]\nassert len(events) == min(12, len(df))\nprint(events[:3])\n"),
            ("## Урок. 2–3. Stack и undo", """steps = ["load", "drop_missing", "make_delay", "scale"]
history = []
for step in steps:
    history.append(step)
undone = history.pop()

def undo(stack):
    return stack.pop() if stack else None

trial = ["load", "filter"]
removed = undo(trial)
assert undone == "scale" and removed == "filter" and undo([]) is None
"""),
            ("## Урок. 4. FIFO queue", "queue = deque(item[0] for item in events)\nprocessed = [queue.popleft() for _ in range(min(3, len(queue)))]\nassert processed == [item[0] for item in events[:3]]\n"),
            ("## Урок. 5. Срочное событие", "normal_ids = df.loc[df[\"is_late\"].eq(0), \"order_id\"].head(5).tolist()\nlate_id = df.loc[df[\"is_late\"].eq(1), \"order_id\"].iloc[0]\ndispatch = deque(normal_ids)\ndispatch.appendleft(late_id)\nnext_id = dispatch.popleft()\nassert next_id == late_id and list(dispatch) == normal_ids\n"),
            ("## Урок. 6. Ограниченный буфер", "recent = deque(maxlen=5)\nfor oid in df[\"order_id\"]:\n    recent.append(oid)\nsnapshot = list(recent)\nassert snapshot == df[\"order_id\"].tail(min(5, len(df))).tolist()\n"),
            ("## Урок. 7. Семантика операций", "choices = {\"undo_preprocessing\": \"stack\", \"fifo_orders\": \"queue\", \"urgent_both_ends\": \"deque\"}\nassert set(choices.values()) == {\"stack\", \"queue\", \"deque\"}\n"),
            ("## Урок. 8. Два порядка", "q_left = deque(item[0] for item in events)\nq_right = deque(item[0] for item in events)\nleft_order = [q_left.popleft() for _ in range(len(q_left))]\nright_order = [q_right.pop() for _ in range(len(q_right))]\nORDER_NOTE = \"popleft сохраняет FIFO: первым обработан первый пришедший заказ; pop справа разворачивает поток и меняет смысл очереди.\"\nassert right_order == list(reversed(left_order)) and len(ORDER_NOTE) >= 80\n"),
            ("## Урок. 9. Журнал", "pipeline = [\"load\", \"clean\", \"join\", \"scale\", \"cluster\"]\nhistory = pipeline.copy()\nundone_two = [history.pop(), history.pop()]\naudit = {\"remaining\": history, \"undone\": undone_two}\nassert audit[\"remaining\"] == pipeline[:3]\n"),
            ("## ДЗ. A1–A3", "ops = [\"load\", \"clean\", \"scale\", \"cluster\", \"report\"]\nstack = ops.copy()\nundo_order = [stack.pop() for _ in range(len(stack))]\nsource_ids = df[\"order_id\"].head(10).tolist()\nq = deque(source_ids)\nfifo = [q.popleft() for _ in range(len(q))]\nlate_ids = df.loc[df[\"is_late\"].eq(1), \"order_id\"].head(4).tolist()\nnormal_ids = df.loc[df[\"is_late\"].eq(0), \"order_id\"].head(4).tolist()\npriority_order = late_ids + normal_ids\nassert undo_order == list(reversed(ops)) and fifo == source_ids\n"),
            ("## ДЗ. Challenge", """def dispatch_orders(late, normal, limit):
    late, normal = deque(late), deque(normal)
    result = []
    while len(result) < limit and (late or normal):
        result.append(late.popleft() if late else normal.popleft())
    return result

result = dispatch_orders(deque(late_ids), deque(normal_ids), 5)
STRUCTURE_NOTE = (
    "Stack задаёт LIFO и подходит для undo. Queue задаёт FIFO и сохраняет порядок потока. "
    "Deque поддерживает быстрые операции с обоих концов: обычные события справа, срочные слева. "
    "Выбор определяется смыслом операции, а не названием контейнера."
)
assert result == (late_ids + normal_ids)[:5] and len(STRUCTURE_NOTE) >= 180
"""),
        ],
    )
    add(base, lesson, homework, solutions)


def lesson02() -> None:
    base = LESSON_DIRS[1]
    setup = LOAD_DATA + "\nfrom collections import deque\n"
    lesson = student_notebook(
        "Практика: буферы потока заказов",
        setup,
        [
            ("## 1. Последние семь событий\n\nЗаполните ограниченный deque всем потоком.", "recent = deque(maxlen=7)\n# TODO\nassert list(recent) == df[\"order_id\"].tail(min(7, len(df))).tolist()\n"),
            ("## 2. Скользящее окно\n\nФункция возвращает средние каждого полного окна.", """def rolling_mean(values, width):
    # TODO: deque(maxlen=width)
    ...


means5 = rolling_mean(df["delivery_days"].tolist(), 5)
assert len(means5) == max(0, len(df) - 4)
assert all(isinstance(x, float) for x in means5)
"""),
            ("## 3. Две очереди\n\nРазделите поток на late и normal без изменения внутреннего порядка.", "late_q, normal_q = deque(), deque()\n# TODO\nassert len(late_q) + len(normal_q) == len(df)\nassert list(late_q) == df.loc[df[\"is_late\"].eq(1), \"order_id\"].tolist()\n"),
            ("## 4. Три late, затем один normal\n\nСимулируйте цикл до 12 обработок.", "processed = []  # TODO: список пар (order_id, group)\nassert len(processed) == min(12, len(df))\nassert all(group in {\"late\", \"normal\"} for _, group in processed)\nassert sum(group == \"normal\" for _, group in processed[:4]) <= 1\n"),
            ("## 5. Остаток очередей\n\nПроверьте закон сохранения числа событий.", "remaining = None  # TODO\nassert remaining == len(df) - len(processed)\nassert remaining == len(late_q) + len(normal_q)\n"),
            ("## 6. Буфер для отмены ошибочной разметки\n\nПоследние действия хранятся в stack.", "labels = [(oid, \"checked\") for oid in df[\"order_id\"].head(6)]\nreverted = []  # TODO: отменить два действия через pop\nassert [x[0] for x in reverted] == df[\"order_id\"].head(6).tail(2).iloc[::-1].tolist()\nassert len(labels) == 4\n"),
            ("## 7. Дедупликация соседних событий\n\nУдалите только последовательные повторы, используя последний элемент deque.", "raw = [\"A\", \"A\", \"B\", \"B\", \"A\", \"C\", \"C\"]\ncompact = None  # TODO\nassert compact == [\"A\", \"B\", \"A\", \"C\"]\n"),
            ("## 8. Эксперимент с квотой\n\nСравните квоты late 1 и 3 на первых 16 обработках.", "orders_by_quota = {}  # TODO: quota -> список групп\nassert set(orders_by_quota) == {1, 3}\nassert all(len(v) == min(16, len(df)) for v in orders_by_quota.values())\nQUOTA_NOTE = \"\"  # TODO: >= 100 символов\nassert len(QUOTA_NOTE) >= 100\n"),
            ("## 9. Самостоятельно: функция процессора\n\nВерните обработанные ids и остатки обеих очередей.", """def process_stream(frame, limit):
    # TODO
    ...


done, late_left, normal_left = process_stream(df, min(15, len(df)))
assert len(done) == min(15, len(df))
assert len(done) + late_left + normal_left == len(df)
assert len(done) == len(set(done))
"""),
        ],
    )
    homework = student_notebook(
        "ДЗ: обработка потока структурами",
        setup,
        [
            ("### Part A — обязательно\n\n## A1. Окно freight_value", "freight_means = None  # TODO: rolling_mean, окно 4\nassert len(freight_means) == max(0, len(df) - 3)\nassert all(x >= 0 for x in freight_means)\n"),
            ("## A2. Буфер пиковых задержек\n\nХраните последние 8 delay_days и максимум после каждого полного окна.", "window_max = []  # TODO\nassert len(window_max) == max(0, len(df) - 7)\nassert all(isinstance(x, (int, float, np.number)) for x in window_max)\n"),
            ("## A3. Round-robin двух очередей\n\nЧередуйте late и normal, пока одна не опустеет.", "alternating = []  # TODO: пары (id, group)\nassert len(alternating) > 0\nassert all(alternating[i][1] != alternating[i + 1][1] for i in range(len(alternating) - 1))\n"),
            ("### Challenge\n\n## B1. Динамическая квота", """def adaptive_dispatch(frame, limit, threshold):
    # TODO: если late-очередь длиннее threshold, брать late; иначе чередовать
    ...


adaptive = adaptive_dispatch(df, min(20, len(df)), 3)
assert len(adaptive) == min(20, len(df))
assert len(adaptive) == len(set(adaptive))
"""),
            ("## B2. Решение для ops", "BUFFER_NOTE = \"\"  # TODO: риск голодания normal и выбранная защита\nassert len(BUFFER_NOTE) >= 180\nassert \"deque\" in BUFFER_NOTE.lower()\n"),
        ],
    )
    solutions = solution_notebook(
        "практика буферов",
        setup,
        [
            ("## Урок. 1. Последние события", "recent = deque(maxlen=7)\nfor oid in df[\"order_id\"]:\n    recent.append(oid)\nassert list(recent) == df[\"order_id\"].tail(min(7, len(df))).tolist()\n"),
            ("## Урок. 2. Скользящее среднее", """def rolling_mean(values, width):
    window, result = deque(maxlen=width), []
    for value in values:
        window.append(float(value))
        if len(window) == width:
            result.append(float(sum(window) / width))
    return result

means5 = rolling_mean(df["delivery_days"].tolist(), 5)
assert len(means5) == max(0, len(df) - 4)
"""),
            ("## Урок. 3–5. Очереди и квота", """late_q, normal_q = deque(), deque()
for row in df[["order_id", "is_late"]].itertuples(index=False):
    (late_q if row.is_late else normal_q).append(row.order_id)
processed = []
while len(processed) < min(12, len(df)) and (late_q or normal_q):
    for _ in range(3):
        if late_q and len(processed) < min(12, len(df)):
            processed.append((late_q.popleft(), "late"))
    if normal_q and len(processed) < min(12, len(df)):
        processed.append((normal_q.popleft(), "normal"))
remaining = len(late_q) + len(normal_q)
assert len(processed) + remaining == len(df)
"""),
            ("## Урок. 6. Отмена разметки", "labels = [(oid, \"checked\") for oid in df[\"order_id\"].head(6)]\nreverted = [labels.pop(), labels.pop()]\nassert len(labels) == 4 and len(reverted) == 2\n"),
            ("## Урок. 7. Соседние повторы", "raw = [\"A\", \"A\", \"B\", \"B\", \"A\", \"C\", \"C\"]\nbuffer = deque()\nfor event in raw:\n    if not buffer or buffer[-1] != event:\n        buffer.append(event)\ncompact = list(buffer)\nassert compact == [\"A\", \"B\", \"A\", \"C\"]\n"),
            ("## Урок. 8. Эксперимент квот", """def group_order(frame, quota, limit):
    lq = deque(frame.loc[frame["is_late"].eq(1), "order_id"])
    nq = deque(frame.loc[frame["is_late"].eq(0), "order_id"])
    groups = []
    while len(groups) < limit and (lq or nq):
        for _ in range(quota):
            if lq and len(groups) < limit:
                lq.popleft(); groups.append("late")
        if nq and len(groups) < limit:
            nq.popleft(); groups.append("normal")
        if not lq:
            while nq and len(groups) < limit:
                nq.popleft(); groups.append("normal")
    return groups

orders_by_quota = {q: group_order(df, q, min(16, len(df))) for q in (1, 3)}
QUOTA_NOTE = "Квота 3 быстрее уменьшает очередь late, но normal ждут дольше. Квота 1 даёт более ровное обслуживание, хотя критичный хвост сокращается медленнее."
assert len(QUOTA_NOTE) >= 100
"""),
            ("## Урок. 9. Процессор", """def process_stream(frame, limit):
    lq = deque(frame.loc[frame["is_late"].eq(1), "order_id"])
    nq = deque(frame.loc[frame["is_late"].eq(0), "order_id"])
    done = []
    while len(done) < limit and (lq or nq):
        done.append((lq if lq else nq).popleft())
    return done, len(lq), len(nq)

done, late_left, normal_left = process_stream(df, min(15, len(df)))
assert len(done) + late_left + normal_left == len(df)
"""),
            ("## ДЗ. A1–A2. Окна", "freight_means = rolling_mean(df[\"freight_value\"].tolist(), 4)\nwindow = deque(maxlen=8)\nwindow_max = []\nfor value in df[\"delay_days\"]:\n    window.append(float(value))\n    if len(window) == 8:\n        window_max.append(max(window))\nassert len(window_max) == max(0, len(df) - 7)\n"),
            ("## ДЗ. A3. Чередование", "lq = deque(df.loc[df[\"is_late\"].eq(1), \"order_id\"])\nnq = deque(df.loc[df[\"is_late\"].eq(0), \"order_id\"])\nalternating = []\nwhile lq and nq:\n    alternating.extend([(lq.popleft(), \"late\"), (nq.popleft(), \"normal\")])\nassert all(alternating[i][1] != alternating[i + 1][1] for i in range(len(alternating) - 1))\n"),
            ("## ДЗ. Challenge", """def adaptive_dispatch(frame, limit, threshold):
    lq = deque(frame.loc[frame["is_late"].eq(1), "order_id"])
    nq = deque(frame.loc[frame["is_late"].eq(0), "order_id"])
    result, turn_late = [], True
    while len(result) < limit and (lq or nq):
        if lq and (len(lq) > threshold or turn_late or not nq):
            result.append(lq.popleft())
        else:
            result.append(nq.popleft())
        turn_late = not turn_late
    return result

adaptive = adaptive_dispatch(df, min(20, len(df)), 3)
BUFFER_NOTE = (
    "Deque даёт O(1) для снятия события слева. При постоянном приоритете late очередь normal может голодать. "
    "Защита — квота или чередование: после нескольких late обязательно обработать normal, сохранив FIFO внутри групп."
)
assert len(adaptive) == min(20, len(df)) and len(BUFFER_NOTE) >= 180
"""),
        ],
    )
    add(base, lesson, homework, solutions)


def lesson03() -> None:
    base = LESSON_DIRS[2]
    setup = LOAD_DATA
    lesson = student_notebook(
        "Set и dict: уникальность и частоты",
        setup,
        [
            ("## 1. Уникальные заказы\n\nПреобразуйте ids в set и найдите число дублей.", "unique_orders = None  # TODO\nduplicate_count = None  # TODO\nassert isinstance(unique_orders, set)\nassert duplicate_count == len(df) - len(unique_orders)\n"),
            ("## 2. Быстрая membership-проверка\n\nДля шести probes получите список bool.", "known = set(df[\"order_id\"])\nprobes = df[\"order_id\"].head(5).tolist() + [\"missing_order\"]\nfound = None  # TODO\nassert found == [True, True, True, True, True, False]\n"),
            ("## 3. Частота customer_state\n\nСоберите dict циклом, без value_counts.", "customer_counts = {}  # TODO\nassert sum(customer_counts.values()) == len(df)\nassert set(customer_counts) == set(df[\"customer_state\"])\n"),
            ("## 4. Late по customer_state\n\nЗначение — число late-заказов.", "customer_late = {}  # TODO\nassert set(customer_late) == set(customer_counts)\nassert sum(customer_late.values()) == int(df[\"is_late\"].sum())\n"),
            ("## 5. Доля late\n\nРазделите late на total для каждого региона.", "customer_rate = None  # TODO\nassert set(customer_rate) == set(customer_counts)\nassert all(0 <= value <= 1 for value in customer_rate.values())\n"),
            ("## 6. Seller_state тем же алгоритмом\n\nВерните вложенный dict `late`/`total`.", "seller_stats = {}  # TODO\nassert set(seller_stats) == set(df[\"seller_state\"])\nassert sum(v[\"total\"] for v in seller_stats.values()) == len(df)\nassert sum(v[\"late\"] for v in seller_stats.values()) == int(df[\"is_late\"].sum())\n"),
            ("## 7. Сортировка частот\n\nСписок пар `(state, late_count)` по убыванию.", "late_ranking = None  # TODO\nassert len(late_ranking) == len(customer_late)\nassert all(late_ranking[i][1] >= late_ranking[i + 1][1] for i in range(len(late_ranking) - 1))\n"),
            ("## 8. Частота и доля — разные вопросы\n\nНазовите лидеров по count и rate. Проверьте размер обоих сегментов: высокий rate на малом числе заказов не равен большому объёму late.", "leader_count = None  # TODO\nleader_rate = None   # TODO\nRATE_NOTE = \"\"       # TODO: >= 100 символов\nassert leader_count in customer_counts and leader_rate in customer_counts\nassert len(RATE_NOTE) >= 100\n"),
            ("## 9. Самостоятельно: функция счётчика", """def late_stats(frame, segment_column):
    # TODO: segment -> {"late": int, "total": int, "rate": float}
    ...


stats = late_stats(df, "seller_state")
assert set(stats) == set(df["seller_state"])
assert all(set(v) == {"late", "total", "rate"} for v in stats.values())
assert sum(v["total"] for v in stats.values()) == len(df)
"""),
        ],
    )
    homework = student_notebook(
        "ДЗ: set, dict и частоты",
        setup,
        [
            ("### Part A — обязательно\n\n## A1. Уникальные продавцы", "seller_ids = None  # TODO\nassert isinstance(seller_ids, set)\nassert len(seller_ids) == df[\"seller_id\"].nunique()\n"),
            ("## A2. Late по seller_id", "seller_late = {}  # TODO\nassert sum(seller_late.values()) == int(df[\"is_late\"].sum())\nassert set(seller_late) <= seller_ids\n"),
            ("## A3. Top-5", "top5_sellers = None  # TODO: список пар\nassert 1 <= len(top5_sellers) <= 5\nassert all(top5_sellers[i][1] >= top5_sellers[i + 1][1] for i in range(len(top5_sellers) - 1))\n"),
            ("### Challenge\n\n## B1. Универсальная таблица", "state_table = None  # TODO: DataFrame из late_stats\nassert isinstance(state_table, pd.DataFrame)\nassert {\"segment\", \"late\", \"total\", \"rate\"} <= set(state_table.columns)\nassert len(state_table) == df[\"seller_state\"].nunique()\n"),
            ("## B2. Интерпретация", "FREQUENCY_NOTE = \"\"  # TODO: count против rate и размер сегмента\nassert len(FREQUENCY_NOTE) >= 180\nassert \"late\" in FREQUENCY_NOTE.lower()\n"),
        ],
    )
    solutions = solution_notebook(
        "set, dict и частоты",
        setup,
        [
            ("## Урок. 1–2. Set и membership", "unique_orders = set(df[\"order_id\"])\nduplicate_count = len(df) - len(unique_orders)\nknown = unique_orders\nprobes = df[\"order_id\"].head(5).tolist() + [\"missing_order\"]\nfound = [oid in known for oid in probes]\nassert found[-1] is False\n"),
            ("## Урок. 3. Частоты customer_state", "customer_counts = {}\nfor state in df[\"customer_state\"]:\n    customer_counts[state] = customer_counts.get(state, 0) + 1\nassert sum(customer_counts.values()) == len(df)\n"),
            ("## Урок. 4–5. Late count и rate", "customer_late = {state: 0 for state in customer_counts}\nfor row in df[[\"customer_state\", \"is_late\"]].itertuples(index=False):\n    customer_late[row.customer_state] += int(row.is_late)\ncustomer_rate = {state: customer_late[state] / customer_counts[state] for state in customer_counts}\nassert sum(customer_late.values()) == int(df[\"is_late\"].sum())\n"),
            ("## Урок. 6. Статистика seller_state", "seller_stats = {}\nfor row in df[[\"seller_state\", \"is_late\"]].itertuples(index=False):\n    bucket = seller_stats.setdefault(row.seller_state, {\"late\": 0, \"total\": 0})\n    bucket[\"total\"] += 1\n    bucket[\"late\"] += int(row.is_late)\nassert sum(v[\"total\"] for v in seller_stats.values()) == len(df)\n"),
            ("## Урок. 7–8. Рейтинг и смысл", "late_ranking = sorted(customer_late.items(), key=lambda item: item[1], reverse=True)\nleader_count = max(customer_late, key=customer_late.get)\nleader_rate = max(customer_rate, key=customer_rate.get)\nRATE_NOTE = \"Count показывает объём late-заказов и зависит от размера региона. Rate отвечает на вопрос о доле проблем внутри региона; без total маленький сегмент может выглядеть главным риском случайно.\"\nassert len(RATE_NOTE) >= 100\n"),
            ("## Урок. 9. Универсальная функция", """def late_stats(frame, segment_column):
    result = {}
    for row in frame[[segment_column, "is_late"]].itertuples(index=False, name=None):
        segment, is_late = row
        bucket = result.setdefault(segment, {"late": 0, "total": 0, "rate": 0.0})
        bucket["total"] += 1
        bucket["late"] += int(is_late)
    for bucket in result.values():
        bucket["rate"] = bucket["late"] / bucket["total"]
    return result

stats = late_stats(df, "seller_state")
assert sum(v["total"] for v in stats.values()) == len(df)
"""),
            ("## ДЗ. A1–A3", "seller_ids = set(df[\"seller_id\"])\nseller_late = {}\nfor row in df.loc[df[\"is_late\"].eq(1), [\"seller_id\"]].itertuples(index=False):\n    seller_late[row.seller_id] = seller_late.get(row.seller_id, 0) + 1\ntop5_sellers = sorted(seller_late.items(), key=lambda item: item[1], reverse=True)[:5]\nassert set(seller_late) <= seller_ids\n"),
            ("## ДЗ. Challenge", "rows = [{\"segment\": segment, **values} for segment, values in late_stats(df, \"seller_state\").items()]\nstate_table = pd.DataFrame(rows).sort_values([\"rate\", \"total\"], ascending=False)\nFREQUENCY_NOTE = \"Late count нужен для оценки объёма работы, late rate — для сравнения качества сегментов. Оба числа читаются вместе с total: высокая доля на двух заказах слабее как основание для решения, чем устойчивая доля на сотнях.\"\nassert len(FREQUENCY_NOTE) >= 180\n"),
        ],
    )
    add(base, lesson, homework, solutions)


def lesson04() -> None:
    base = LESSON_DIRS[3]
    setup = LOAD_DATA
    lesson = student_notebook(
        "Практика: membership, счётчики и сегменты",
        setup,
        [
            ("## 1. Контрольный список\n\nПроверьте ids через set, верните dict id -> bool.", "known = set(df[\"order_id\"])\nprobes = df[\"order_id\"].sample(min(8, len(df)), random_state=52).tolist() + [\"missing\"]\ncheck = None  # TODO\nassert isinstance(check, dict) and len(check) == len(probes)\nassert check[\"missing\"] is False\n"),
            ("## 2. Пересечение множеств\n\nСравните customer_state и seller_state.", "customer_states = None  # TODO\nseller_states = None    # TODO\nshared_states = None    # TODO\nassert shared_states == customer_states & seller_states\nassert shared_states <= customer_states and shared_states <= seller_states\n"),
            ("## 3. Счётчик пар регионов\n\nКлюч `(seller_state, customer_state)`.", "pair_total = {}  # TODO\nassert sum(pair_total.values()) == len(df)\nassert all(isinstance(key, tuple) and len(key) == 2 for key in pair_total)\n"),
            ("## 4. Late по паре\n\nСоберите второй счётчик с теми же ключами.", "pair_late = {}  # TODO\nassert set(pair_late) == set(pair_total)\nassert sum(pair_late.values()) == int(df[\"is_late\"].sum())\n"),
            ("## 5. Доля late пары", "pair_rate = None  # TODO\nassert set(pair_rate) == set(pair_total)\nassert all(0 <= value <= 1 for value in pair_rate.values())\n"),
            ("## 6. Минимальный размер сегмента\n\nОставьте пары с total >= 3 (или >=1, если данных мало).", "MIN_SIZE = 3 if len(df) >= 30 else 1\neligible = None  # TODO\nassert all(pair_total[key] >= MIN_SIZE for key in eligible)\nassert set(eligible) <= set(pair_total)\n"),
            ("## 7. Выше глобальной доли\n\nСписок `(pair, rate, total)` по убыванию rate. Глобальная доля здесь — линия сравнения, а не доказательство причины задержек.", "global_rate = float(df[\"is_late\"].mean())\nhot_segments = None  # TODO\nassert all(rate > global_rate and total >= MIN_SIZE for _, rate, total in hot_segments)\nassert all(hot_segments[i][1] >= hot_segments[i + 1][1] for i in range(len(hot_segments) - 1))\n"),
            ("## 8. Watchlist заказов\n\nИз hot-сегментов соберите set ids, затем пересеките с late.", "watch = None  # TODO\nassert isinstance(watch, set)\nassert watch <= set(df.loc[df[\"is_late\"].eq(1), \"order_id\"])\n"),
            ("## 9. Самостоятельно: отчёт сегмента", """def segment_report(frame, seller_state, customer_state):
    # TODO: total, late, rate, order_ids
    ...


example_pair = next(iter(pair_total))
report = segment_report(df, *example_pair)
assert set(report) == {"total", "late", "rate", "order_ids"}
assert report["total"] == len(report["order_ids"])
assert 0 <= report["rate"] <= 1
"""),
        ],
    )
    homework = student_notebook(
        "ДЗ: membership и late-rate",
        setup,
        [
            ("### Part A — обязательно\n\n## A1. Наблюдаемые продавцы", "watch_sellers = set(df.sort_values(\"delay_days\", ascending=False)[\"seller_id\"].head(10))\nflags = None  # TODO: seller_id -> bool для каждой строки\nassert len(flags) == len(df)\nassert all(isinstance(x, (bool, np.bool_)) for x in flags)\n"),
            ("## A2. Seller rate\n\nИспользуйте собственный dict-счётчик.", "seller_rate = None  # TODO\nassert set(seller_rate) == set(df[\"seller_state\"])\nassert all(0 <= x <= 1 for x in seller_rate.values())\n"),
            ("## A3. Надёжные сегменты\n\nОставьте seller_state с total не ниже медианы.", "reliable = None  # TODO: список (state, total, rate)\nassert all(total >= 1 and 0 <= rate <= 1 for _, total, rate in reliable)\nassert len(reliable) > 0\n"),
            ("### Challenge\n\n## B1. Три ключа\n\nСегмент `(seller_state, customer_state, is_late)`.", "cube = {}  # TODO\nassert sum(cube.values()) == len(df)\nassert all(isinstance(key, tuple) and len(key) == 3 for key in cube)\n"),
            ("## B2. Рекомендация", "SEGMENT_NOTE = \"\"  # TODO: минимум размера, rate и ограничение\nassert len(SEGMENT_NOTE) >= 200\nassert \"rate\" in SEGMENT_NOTE.lower()\n"),
        ],
    )
    solutions = solution_notebook(
        "membership и счётчики",
        setup,
        [
            ("## Урок. 1–2. Membership и множества", "known = set(df[\"order_id\"])\nprobes = df[\"order_id\"].sample(min(8, len(df)), random_state=52).tolist() + [\"missing\"]\ncheck = {oid: oid in known for oid in probes}\ncustomer_states = set(df[\"customer_state\"])\nseller_states = set(df[\"seller_state\"])\nshared_states = customer_states & seller_states\nassert check[\"missing\"] is False\n"),
            ("## Урок. 3–4. Счётчики пар", "pair_total, pair_late = {}, {}\nfor row in df[[\"seller_state\", \"customer_state\", \"is_late\"]].itertuples(index=False):\n    key = (row.seller_state, row.customer_state)\n    pair_total[key] = pair_total.get(key, 0) + 1\n    pair_late[key] = pair_late.get(key, 0) + int(row.is_late)\nassert sum(pair_total.values()) == len(df)\n"),
            ("## Урок. 5–7. Доли и фильтр", "pair_rate = {key: pair_late[key] / total for key, total in pair_total.items()}\nMIN_SIZE = 3 if len(df) >= 30 else 1\neligible = {key: pair_rate[key] for key, total in pair_total.items() if total >= MIN_SIZE}\nglobal_rate = float(df[\"is_late\"].mean())\nhot_segments = sorted([(key, rate, pair_total[key]) for key, rate in eligible.items() if rate > global_rate], key=lambda row: row[1], reverse=True)\nassert all(total >= MIN_SIZE for _, _, total in hot_segments)\n"),
            ("## Урок. 8. Watchlist", "hot_pairs = {pair for pair, _, _ in hot_segments}\nwatch = {row.order_id for row in df.itertuples() if (row.seller_state, row.customer_state) in hot_pairs and row.is_late}\nassert watch <= set(df.loc[df[\"is_late\"].eq(1), \"order_id\"])\n"),
            ("## Урок. 9. Отчёт сегмента", """def segment_report(frame, seller_state, customer_state):
    part = frame[frame["seller_state"].eq(seller_state) & frame["customer_state"].eq(customer_state)]
    total, late = len(part), int(part["is_late"].sum())
    return {"total": total, "late": late, "rate": late / total if total else 0.0, "order_ids": part["order_id"].tolist()}

example_pair = next(iter(pair_total))
report = segment_report(df, *example_pair)
assert report["total"] == len(report["order_ids"])
"""),
            ("## ДЗ. A1. Наблюдаемые продавцы", "watch_sellers = set(df.sort_values(\"delay_days\", ascending=False)[\"seller_id\"].head(10))\nflags = [seller in watch_sellers for seller in df[\"seller_id\"]]\nassert len(flags) == len(df)\n"),
            ("## ДЗ. A2–A3. Seller rate", "seller_total, seller_late = {}, {}\nfor row in df[[\"seller_state\", \"is_late\"]].itertuples(index=False):\n    seller_total[row.seller_state] = seller_total.get(row.seller_state, 0) + 1\n    seller_late[row.seller_state] = seller_late.get(row.seller_state, 0) + int(row.is_late)\nseller_rate = {s: seller_late[s] / seller_total[s] for s in seller_total}\nmedian_total = float(np.median(list(seller_total.values())))\nreliable = [(s, seller_total[s], seller_rate[s]) for s in seller_total if seller_total[s] >= median_total]\nassert reliable\n"),
            ("## ДЗ. Challenge", "cube = {}\nfor row in df[[\"seller_state\", \"customer_state\", \"is_late\"]].itertuples(index=False):\n    key = (row.seller_state, row.customer_state, int(row.is_late))\n    cube[key] = cube.get(key, 0) + 1\nSEGMENT_NOTE = \"Сначала применяем минимум размера сегмента, затем сравниваем late rate с общей долей. Малый сегмент с rate 1.0 может быть случайностью. Решение — мониторить крупные устойчивые пары и не считать связь причиной задержки без дополнительных данных.\"\nassert sum(cube.values()) == len(df) and len(SEGMENT_NOTE) >= 200\n"),
        ],
    )
    add(base, lesson, homework, solutions)


def lesson05() -> None:
    base = LESSON_DIRS[4]
    setup = LOAD_DATA + CLUSTER_IMPORTS
    lesson = student_notebook(
        "KMeans и DBSCAN: сегменты доставки",
        setup,
        [
            ("## 1. Матрица признаков\n\nТолько delivery_days, freight_value, delay_days.", "X = None  # TODO\nassert isinstance(X, pd.DataFrame)\nassert list(X.columns) == FEATURES and X.shape == (len(df), 3)\nassert X.notna().all().all()\n"),
            ("## 2. Почему нужен общий масштаб\n\nПосчитайте range каждого признака.", "feature_range = None  # TODO\nassert set(feature_range.index) == set(FEATURES)\nassert (feature_range >= 0).all()\n"),
            ("## 3. StandardScaler\n\nОбучите scaler и преобразуйте X.", "scaler = StandardScaler()\nXs = None  # TODO\nassert Xs is not None and Xs.shape == X.shape\nassert np.allclose(Xs.mean(axis=0), 0, atol=1e-7)\n"),
            ("## 4. KMeans, k=3\n\nФиксируйте random_state=53, n_init=10.", "kmeans = None  # TODO\nlabels_km = None  # TODO\nassert len(labels_km) == len(df)\nassert set(labels_km) <= {0, 1, 2}\nassert len(set(labels_km)) == min(3, len(df))\n"),
            ("## 5. Размеры кластеров", "cluster_sizes = None  # TODO: Series\nassert int(cluster_sizes.sum()) == len(df)\nassert len(cluster_sizes) == len(set(labels_km))\n"),
            ("## 6. Профили KMeans\n\nСредние признаки и is_late только для описания.", "clustered = df.assign(cluster_km=labels_km)\nprofile_km = None  # TODO\nassert set(FEATURES + [\"is_late\"]) <= set(profile_km.columns)\nassert len(profile_km) == len(set(labels_km))\n"),
            ("## 7. DBSCAN\n\nИспользуйте eps=0.9, min_samples=4.", "dbscan = None  # TODO\nlabels_db = None  # TODO\nassert len(labels_db) == len(df)\nassert all(isinstance(int(x), int) for x in labels_db)\n"),
            ("## 8. Шум и кластеры DBSCAN\n\nМетка -1 означает шум.", "n_noise = None  # TODO\nn_db_clusters = None  # TODO, без -1\nassert n_noise == int(np.sum(np.asarray(labels_db) == -1))\nassert 0 <= n_noise <= len(df) and n_db_clusters >= 0\n"),
            ("## 9. Эксперимент eps\n\nДля 0.5, 0.9, 1.3 сохраните число кластеров и шума.", "eps_table = None  # TODO: DataFrame eps, clusters, noise\nassert isinstance(eps_table, pd.DataFrame) and len(eps_table) == 3\nassert {\"eps\", \"clusters\", \"noise\"} <= set(eps_table.columns)\nassert eps_table[\"noise\"].between(0, len(df)).all()\n"),
            ("## 10. Самостоятельно: интерпретация\n\nОпишите кластеры, не называя это предсказанием.", "CLUSTER_NOTE = \"\"  # TODO: >= 180 символов\nassert len(CLUSTER_NOTE) >= 180\nassert \"predict\" not in CLUSTER_NOTE.lower() and \"классифик\" not in CLUSTER_NOTE.lower()\n"),
        ],
    )
    homework = student_notebook(
        "ДЗ: параметры кластеризации",
        setup,
        [
            ("### Part A — обязательно\n\n## A1. KMeans k=2..5", "k_rows = []  # TODO: k, inertia, smallest_cluster\nk_table = pd.DataFrame(k_rows)\nassert len(k_table) == 4\nassert {\"k\", \"inertia\", \"smallest_cluster\"} <= set(k_table.columns)\n"),
            ("## A2. Профиль k=4", "labels4 = None  # TODO\nprofile4 = None  # TODO\nassert len(labels4) == len(df)\nassert isinstance(profile4, pd.DataFrame) and len(profile4) == min(4, len(df))\n"),
            ("## A3. DBSCAN eps=0.6..1.4", "db_rows = []  # TODO: шаг 0.2\nscan_table = pd.DataFrame(db_rows)\nassert len(scan_table) == 5\nassert {\"eps\", \"clusters\", \"noise\"} <= set(scan_table.columns)\n"),
            ("### Challenge\n\n## B1. Устойчивость KMeans\n\nСравните random_state 0..4 по inertia.", "inertias = []  # TODO\nassert len(inertias) == 5\nassert all(value > 0 for value in inertias)\n"),
            ("## B2. Выбор алгоритма", "MODEL_NOTE = \"\"  # TODO: KMeans vs DBSCAN, масштаб и параметры\nassert len(MODEL_NOTE) >= 220\nassert all(word in MODEL_NOTE for word in [\"KMeans\", \"DBSCAN\", \"StandardScaler\"])\n"),
        ],
    )
    solutions = solution_notebook(
        "KMeans и DBSCAN",
        setup,
        [
            ("## Урок. 1–3. Признаки и масштаб", "X = df[FEATURES].copy()\nfeature_range = X.max() - X.min()\nscaler = StandardScaler()\nXs = scaler.fit_transform(X)\nassert Xs.shape == X.shape and np.allclose(Xs.mean(axis=0), 0, atol=1e-7)\n"),
            ("## Урок. 4–5. KMeans", "kmeans = KMeans(n_clusters=min(3, len(df)), random_state=53, n_init=10)\nlabels_km = kmeans.fit_predict(Xs)\ncluster_sizes = pd.Series(labels_km).value_counts().sort_index()\nassert int(cluster_sizes.sum()) == len(df)\n"),
            ("## Урок. 6. Описательные профили", "clustered = df.assign(cluster_km=labels_km)\nprofile_km = clustered.groupby(\"cluster_km\")[FEATURES + [\"is_late\"]].mean().round(2)\nassert len(profile_km) == len(set(labels_km))\nprint(profile_km)\n"),
            ("## Урок. 7–8. DBSCAN", "dbscan = DBSCAN(eps=0.9, min_samples=4)\nlabels_db = dbscan.fit_predict(Xs)\nn_noise = int(np.sum(labels_db == -1))\nn_db_clusters = len(set(labels_db) - {-1})\nassert 0 <= n_noise <= len(df)\n"),
            ("## Урок. 9. Эксперимент eps", "eps_rows = []\nfor eps in (0.5, 0.9, 1.3):\n    labels = DBSCAN(eps=eps, min_samples=4).fit_predict(Xs)\n    eps_rows.append({\"eps\": eps, \"clusters\": len(set(labels) - {-1}), \"noise\": int(np.sum(labels == -1))})\neps_table = pd.DataFrame(eps_rows)\nassert len(eps_table) == 3\n"),
            ("## Урок. 10. Интерпретация", "CLUSTER_NOTE = \"KMeans разделил заказы на три группы по совместному масштабу срока, стоимости доставки и задержки. Средняя is_late помогает описать уже найденные группы, но не является входным признаком и не превращает анализ в предсказание. DBSCAN отдельно показывает плотные области и редкие точки.\"\nassert len(CLUSTER_NOTE) >= 180\n"),
            ("## ДЗ. A1. Перебор k", "k_rows = []\nfor k in range(2, 6):\n    model = KMeans(n_clusters=min(k, len(df)), random_state=53, n_init=10)\n    labels = model.fit_predict(Xs)\n    k_rows.append({\"k\": k, \"inertia\": float(model.inertia_), \"smallest_cluster\": int(pd.Series(labels).value_counts().min())})\nk_table = pd.DataFrame(k_rows)\nassert len(k_table) == 4\n"),
            ("## ДЗ. A2. Профиль k=4", "model4 = KMeans(n_clusters=min(4, len(df)), random_state=53, n_init=10)\nlabels4 = model4.fit_predict(Xs)\nprofile4 = df.assign(cluster=labels4).groupby(\"cluster\")[FEATURES + [\"is_late\"]].mean()\nassert len(profile4) == min(4, len(df))\n"),
            ("## ДЗ. A3. Сетка DBSCAN", "db_rows = []\nfor eps in np.arange(0.6, 1.41, 0.2):\n    labels = DBSCAN(eps=float(eps), min_samples=4).fit_predict(Xs)\n    db_rows.append({\"eps\": round(float(eps), 1), \"clusters\": len(set(labels) - {-1}), \"noise\": int(np.sum(labels == -1))})\nscan_table = pd.DataFrame(db_rows)\nassert len(scan_table) == 5\n"),
            ("## ДЗ. Challenge", "inertias = []\nfor seed in range(5):\n    model = KMeans(n_clusters=min(3, len(df)), random_state=seed, n_init=10).fit(Xs)\n    inertias.append(float(model.inertia_))\nMODEL_NOTE = \"StandardScaler нужен, чтобы freight_value не подавлял признаки дней. KMeans требует заранее выбрать число групп и даёт сегмент каждой точке. DBSCAN ищет плотные области, может оставить шум и чувствителен к eps. Алгоритм выбирают по операционному вопросу, а параметры проверяют экспериментом.\"\nassert len(inertias) == 5 and len(MODEL_NOTE) >= 220\n"),
        ],
    )
    add(base, lesson, homework, solutions)


def lesson06() -> None:
    base = LESSON_DIRS[5]
    setup = LOAD_DATA + CLUSTER_IMPORTS
    lesson = student_notebook(
        "Практика: кластеры и список аномалий",
        setup,
        [
            ("## 1. Подготовка без утечки смысла\n\nМасштабируйте только три FEATURES; is_late не входит.", "X = None  # TODO\nXs = None  # TODO\nassert list(X.columns) == FEATURES\nassert \"is_late\" not in X.columns and Xs.shape == X.shape\n"),
            ("## 2. KMeans-сегменты", "labels_km = None  # TODO: k=3, seed=54, n_init=10\nassert len(labels_km) == len(df)\nassert len(set(labels_km)) == min(3, len(df))\n"),
            ("## 3. DBSCAN-шум", "labels_db = None  # TODO: eps=0.9, min_samples=4\nassert len(labels_db) == len(df)\nassert set(np.unique(labels_db))\n"),
            ("## 4. Общая таблица", "clustered = None  # TODO: копия df + cluster_km + cluster_db\nassert isinstance(clustered, pd.DataFrame) and len(clustered) == len(df)\nassert {\"cluster_km\", \"cluster_db\"} <= set(clustered.columns)\n"),
            ("## 5. Профили для ops\n\nСредние, медианы, размер и late-rate для описания.", "profiles = None  # TODO\nassert isinstance(profiles, pd.DataFrame)\nassert {\"size\", \"delivery_days_mean\", \"freight_median\", \"delay_mean\", \"late_rate\"} <= set(profiles.columns)\n"),
            ("## 6. Кандидаты DBSCAN\n\nМетка -1 — кандидат, но не автоматическая ошибка.", "noise_candidates = None  # TODO\nassert isinstance(noise_candidates, pd.DataFrame)\nassert set(noise_candidates.index) <= set(clustered.index)\nassert (noise_candidates[\"cluster_db\"] == -1).all()\n"),
            ("## 7. Страховка для малого набора\n\nДобавьте top-5 delay к DBSCAN-кандидатам.", "top_delay_idx = None  # TODO\ncandidate_idx = None  # TODO: объединение set\nassert len(top_delay_idx) == min(5, len(df))\nassert set(top_delay_idx) <= candidate_idx\n"),
            ("## 8. Ранжирование аномалий\n\nСоздайте severity из стандартизированных delay/freight.", "anomalies = None  # TODO: кандидаты, severity, сортировка\nassert isinstance(anomalies, pd.DataFrame) and len(anomalies) >= min(5, len(df))\nassert \"severity\" in anomalies.columns\nassert anomalies[\"severity\"].is_monotonic_decreasing\n"),
            ("## 9. Обоснование каждой строки\n\nКолонка reason с конкретным наблюдением.", "reasons = None  # TODO: список строк той же длины\nassert len(reasons) == len(anomalies)\nassert all(isinstance(text, str) and len(text) >= 35 for text in reasons)\nanomalies = anomalies.assign(reason=reasons)\n"),
            ("## 10. Самостоятельно: записка хабу", "OPS_NOTE = \"\"  # TODO: 250+ символов, число сегментов/кандидатов, действие, ограничение\nassert len(OPS_NOTE) >= 250\nassert str(len(anomalies)) in OPS_NOTE\nassert \"is_late\" in OPS_NOTE\n"),
        ],
    )
    homework = student_notebook(
        "ДЗ: кластерный отчёт для хаба",
        setup,
        [
            ("### Part A — обязательно\n\n## A1. Повторяемый pipeline", """def cluster_orders(frame, eps=0.9):
    # TODO: вернуть копию с cluster_km и cluster_db
    ...


result = cluster_orders(df)
assert len(result) == len(df)
assert {"cluster_km", "cluster_db"} <= set(result.columns)
"""),
            ("## A2. Таблица аномалий\n\nНе более 12 строк, DBSCAN noise или top-delay.", "anomaly_table = None  # TODO\nassert isinstance(anomaly_table, pd.DataFrame)\nassert 1 <= len(anomaly_table) <= min(12, len(df))\nassert {\"order_id\", \"delay_days\", \"freight_value\", \"cluster_db\"} <= set(anomaly_table.columns)\n"),
            ("## A3. Проверки качества", "checks = {\"rows_preserved\": None, \"three_features\": None, \"late_not_feature\": None, \"ranked\": None}  # TODO\nassert set(checks.values()) == {True}\n"),
            ("### Challenge\n\n## B1. Чувствительность списка\n\nСравните anomaly ids при eps 0.7 и 1.1.", "ids_07 = set()  # TODO\nids_11 = set()  # TODO\njaccard = None  # TODO\nassert 0 <= jaccard <= 1\nassert isinstance(ids_07, set) and isinstance(ids_11, set)\n"),
            ("## B2. Executive note", "EXECUTIVE_NOTE = \"\"  # TODO: 300+ символов, наблюдение/действие/ограничение\nassert len(EXECUTIVE_NOTE) >= 300\nassert all(word in EXECUTIVE_NOTE.lower() for word in [\"кластер\", \"аномал\", \"огранич\"])\n"),
        ],
    )
    solutions = solution_notebook(
        "кластеры и аномалии",
        setup,
        [
            ("## Урок. 1. Матрица", "X = df[FEATURES].copy()\nXs = StandardScaler().fit_transform(X)\nassert \"is_late\" not in X and Xs.shape == X.shape\n"),
            ("## Урок. 2–4. Две кластеризации", "labels_km = KMeans(n_clusters=min(3, len(df)), random_state=54, n_init=10).fit_predict(Xs)\nlabels_db = DBSCAN(eps=0.9, min_samples=4).fit_predict(Xs)\nclustered = df.copy()\nclustered[\"cluster_km\"] = labels_km\nclustered[\"cluster_db\"] = labels_db\nassert len(clustered) == len(df)\n"),
            ("## Урок. 5. Профили", "profiles = clustered.groupby(\"cluster_km\").agg(size=(\"order_id\", \"size\"), delivery_days_mean=(\"delivery_days\", \"mean\"), freight_median=(\"freight_value\", \"median\"), delay_mean=(\"delay_days\", \"mean\"), late_rate=(\"is_late\", \"mean\")).round(2)\nassert int(profiles[\"size\"].sum()) == len(df)\nprint(profiles)\n"),
            ("## Урок. 6–7. Кандидаты", "noise_candidates = clustered[clustered[\"cluster_db\"].eq(-1)].copy()\ntop_delay_idx = clustered.nlargest(min(5, len(df)), \"delay_days\").index.tolist()\ncandidate_idx = set(noise_candidates.index) | set(top_delay_idx)\nassert set(top_delay_idx) <= candidate_idx\n"),
            ("## Урок. 8. Severity", "z = pd.DataFrame(Xs, columns=FEATURES, index=df.index)\nseverity = 0.7 * z[\"delay_days\"] + 0.3 * z[\"freight_value\"]\nanomalies = clustered.loc[sorted(candidate_idx)].copy()\nanomalies[\"severity\"] = severity.loc[anomalies.index]\nanomalies = anomalies.sort_values(\"severity\", ascending=False)\nassert anomalies[\"severity\"].is_monotonic_decreasing\n"),
            ("## Урок. 9. Причины", "reasons = []\nfor row in anomalies.itertuples():\n    source = \"DBSCAN пометил как шум\" if row.cluster_db == -1 else \"входит в top-delay\"\n    reasons.append(f\"{source}; delay={row.delay_days} дней, freight={row.freight_value:.1f}.\")\nanomalies = anomalies.assign(reason=reasons)\nassert all(len(text) >= 35 for text in reasons)\n"),
            ("## Урок. 10. Записка хабу", "OPS_NOTE = f\"Получено {clustered['cluster_km'].nunique()} KMeans-сегмента и {len(anomalies)} кандидатов для ручной проверки. Сначала проверить верхние строки severity: сочетание задержки и стоимости доставки. is_late использован только для описания профилей, не как признак. Список не доказывает ошибку: DBSCAN чувствителен к eps, а высокий delay может иметь штатную причину.\"\nassert len(OPS_NOTE) >= 250 and str(len(anomalies)) in OPS_NOTE\n"),
            ("## ДЗ. A1. Pipeline", """def cluster_orders(frame, eps=0.9):
    values = StandardScaler().fit_transform(frame[FEATURES])
    result = frame.copy()
    result["cluster_km"] = KMeans(n_clusters=min(3, len(frame)), random_state=54, n_init=10).fit_predict(values)
    result["cluster_db"] = DBSCAN(eps=eps, min_samples=4).fit_predict(values)
    return result

result = cluster_orders(df)
assert len(result) == len(df)
"""),
            ("## ДЗ. A2. Таблица аномалий", "top_idx = set(result.nlargest(min(8, len(result)), \"delay_days\").index)\nnoise_idx = set(result.index[result[\"cluster_db\"].eq(-1)])\nchosen = list(top_idx | noise_idx)\nanomaly_table = result.loc[chosen].sort_values([\"delay_days\", \"freight_value\"], ascending=False).head(min(12, len(result)))\nassert 1 <= len(anomaly_table) <= min(12, len(df))\n"),
            ("## ДЗ. A3. Quality gate", "checks = {\"rows_preserved\": len(result) == len(df), \"three_features\": len(FEATURES) == 3, \"late_not_feature\": \"is_late\" not in FEATURES, \"ranked\": anomaly_table[\"delay_days\"].is_monotonic_decreasing}\nassert set(checks.values()) == {True}\n"),
            ("## ДЗ. Challenge", """def anomaly_ids(frame, eps):
    result = cluster_orders(frame, eps)
    ids = set(result.loc[result["cluster_db"].eq(-1), "order_id"])
    ids.update(result.nlargest(min(5, len(result)), "delay_days")["order_id"])
    return ids

ids_07, ids_11 = anomaly_ids(df, 0.7), anomaly_ids(df, 1.1)
union = ids_07 | ids_11
jaccard = len(ids_07 & ids_11) / len(union) if union else 1.0
EXECUTIVE_NOTE = (
    f"Кластерный анализ описывает типичные режимы доставки, а список аномалий выделяет заказы для ручной проверки. "
    f"При eps 0.7 и 1.1 сходство списков равно {jaccard:.2f}, поэтому состав зависит от настройки DBSCAN. "
    "Операционное действие: проверить первые заказы по задержке и стоимости, затем связать их с маршрутами. "
    "Ограничение: кластер не является причиной задержки, а аномалия не означает ошибку; is_late служит только описанием."
)
assert 0 <= jaccard <= 1 and len(EXECUTIVE_NOTE) >= 300
"""),
        ],
    )
    add(base, lesson, homework, solutions)


def main() -> None:
    if not DATA_CSV.exists():
        raise SystemExit(f"Missing {DATA_CSV}")
    for lesson_dir in LESSON_DIRS:
        destination = ROOT / lesson_dir / DATA_CSV.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(DATA_CSV, destination)
        print(f"copied {DATA_CSV.name} -> {lesson_dir}")
    for builder in (lesson01, lesson02, lesson03, lesson04, lesson05, lesson06):
        builder()
    print("done: 18 notebooks and 6 CSV copies")


if __name__ == "__main__":
    main()
