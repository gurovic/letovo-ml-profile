#!/usr/bin/env python3
"""Generate operational KTP for grade 8 → docs/ktp/08.md (module themes block).

Нагрузка: 4 ч/нед × 34 недели = 136 акад. ч → 68 пар (1 пара = 2 ч).
При сокращении — режем обзорные/интеграционные темы, не строки «Практика: …».
"""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "docs" / "ktp" / "08.md"

TARGET_PAIRS = 68
HOURS_PER_WEEK = 4
WEEKS = 34

# pairs ranges computed from theme counts
MODULES = [
    {
        "title": "Модуль 1. Оценка недвижимости: функции и inference pipeline",
        "scenario": "Стажёры агентства недвижимости создают прототип оценщика квартир и модуля text_stats.",
        "note": "Пара 1 — вводная; пары 2–6 — введение и отработка; 7 — рекурсия и pipeline; 8 — артефакт (сборка и сдача).",
        "module_path": "modules/08_01_functions_recursion/",
        "themes": [
            "ИИ, машинное обучение и профиль 8–11: цели, траектория, модули и артефакты, организация обучения",
            "Функция как отображение — predict_price, batch_predict, MAE, выбор коэффициента",
            "Параметры и return — describe_numbers, min_max_scale, grade_stats",
            "Практика: proto-EDA и transform-функции",
            "Scope и отладка — accuracy, баги return/scope",
            "Практика: confusion_counts, журнал багов",
            "Рекурсия на данных; lambda / HOF / apply_pipeline",
            "Артефакт text_stats — сборка, сдача, рефлексия модуля",
        ],
    },
    {
        "title": "Модуль 2. Краткосрочная аренда: pandas и линейная регрессия",
        "scenario": "Аналитики краткосрочной аренды «StayLocal» прогнозируют ночную цену объявлений (Airbnb-стиль, Porto) по таблице listings.",
        "module_path": "modules/08_02_carsharing_pandas_lr/",
        "themes": [
            "pandas: read_csv, DataFrame, object / feature / target",
            "Практика: выборка строк/столбцов, фильтры, типы",
            "EDA: describe(), scatter признак → цена",
            "train/test split; LinearRegression fit/predict (один признак)",
            "Практика: MSE, R², сравнение прогнозов",
            "try/except при загрузке и очистке CSV",
            "Практика: другой признак, сравнение метрик; обзор нескольких признаков",
            "Мини-отчёт для отдела аналитики — сборка и сдача",
        ],
    },
    {
        "title": "Модуль 3. Расследование на «Титанике»: EDA и статистика",
        "scenario": "Историческое общество поручило выяснить, кто выживал чаще, только анализом данных.",
        "module_path": "modules/08_03_titanic_eda/",
        "themes": [
            "Загрузка Titanic, первичный осмотр; пути и сохранение графиков",
            "Практика: осмотр таблицы, файлы, первые срезы",
            "Среднее, медиана, std — вручную и в pandas",
            "Практика: квартили, boxplot, группы",
            "Выборка, sampling bias; нормальное распределение и ЦПТ (интуитивно); пропуски",
            "Практика: гистограммы, сравнение групп, стратегии пропусков",
            "Письменный вывод по EDA без модели — сборка и сдача",
        ],
    },
    {
        "title": "Модуль 4. Распознавание цифр: вероятность и kNN",
        "scenario": "Почтовый сервис автоматизирует чтение индексов на конвертах.",
        "module_path": "modules/08_04_mnist_knn/",
        "themes": [
            "Вероятность класса, частота; комбинаторика и перебор",
            "Практика: вероятность, множества, train/test как разбиение",
            "kNN: идея ближайших соседей; min-max scaling",
            "Практика: baseline kNN на подвыборке MNIST",
            "accuracy и F1; выбор k",
            "Практика: метрики; itertools — перебор k и признаков",
        ],
    },
    {
        "title": "Модуль 5. Интернет-магазин: Feature Engineering и lambda",
        "scenario": "CRM маркетплейса (данные Olist) собирает RFM-признаки покупателей и preprocessing-pipeline.",
        "module_path": "modules/08_05_shop_feature_engineering/",
        "data_note": "данные: [data/README.md](../../modules/08_05_shop_feature_engineering/data/README.md) (Olist → slim; CSV ещё не собран)",
        "themes": [
            "Числовые и категориальные признаки; lambda и .apply (схема orders/customers/payments)",
            "Практика: apply, новые столбцы на строке заказа",
            "Группировки и агрегаты → Recency / Frequency / Monetary",
            "Практика: агрегаты и производные признаки (без метки churn)",
            "Логирование preprocessing; raise — валидация входа",
            "Практика и сдача: цепочка preprocessing raw → клиент×RFM",
        ],
    },
    {
        "title": "Модуль 6. A/B-тест стартапа и статистический вывод",
        "scenario": "Стартап тестирует два дизайна лендинга и ищет факторы конверсии.",
        "module_path": "modules/08_06_ab_startup/",
        "themes": [
            "H₀/H₁ и метрика конверсии; p-value через симуляцию",
            "Практика: перестановочный тест",
            "Доверительный интервал; корреляция — ограничения",
            "Практика: ДИ и корреляция на данных стартапа",
            "A/B: риск подглядывания; множественная линейная регрессия",
            "Практика и отчёт: регрессия + интерпретация",
        ],
    },
    {
        "title": "Модуль 7. Массивы: поиск и сортировка",
        "scenario": "Банк «Надёжный» ищет транзакции в отсортированных логах.",
        "module_path": "modules/08_07_bank_arrays_search/",
        "themes": [
            "Линейный и бинарный поиск — идея и сложность",
            "Практика: поиск в логах транзакций",
            "Сортировка выбором; mergesort; quicksort (обзорно)",
            "Практика: реализовать и сравнить сортировки",
            "sorted(key=); метод двух указателей",
            "Практика: ключи сортировки и два указателя",
            "Сравнение O(n²) vs O(n log n); интеграция алгоритмического блока",
        ],
    },
    {
        "title": "Модуль 8. Структуры данных, кластеризация и аномалии",
        "scenario": "Операционный хаб маркетплейса (данные Olist): опоздания доставки, частоты, кластеры и аномальные заказы.",
        "module_path": "modules/08_08_logistics_clustering/",
        "data_note": "данные: [data/README.md](../../modules/08_08_logistics_clustering/data/README.md) (Olist → `orders_slim` + `is_late`; CSV ещё не собран)",
        "themes": [
            "Стек, очередь, deque — буфер и отмена шагов (поток заказов)",
            "Практика: стек / очередь / deque на потоке событий",
            "set и dict как hash map — уникальность, частоты опозданий",
            "Практика: membership, счётчики, доля late по сегментам",
            "k-means; DBSCAN — кластеры, плотность, выбросы",
            "Практика: кластеризация и аномалии на признаках доставки",
        ],
    },
    {
        "title": "Модуль 9. Динамическое программирование и игры",
        "scenario": "Курьерская служба «Мгновение» оптимизирует маршруты и размен.",
        "module_path": "modules/08_09_courier_dp/",
        "themes": [
            "Мемоизация; DP 1D (размен, максимум)",
            "Практика: DP 1D",
            "DP 2D: табличный переход",
            "Практика: DP 2D",
            "Игровая задача win/lose; когда DP уместен в инженерии",
        ],
    },
    {
        "title": "Модуль 10. Отток клиентов: логистическая регрессия и venv",
        "scenario": "Кампания банка (UCI Bank Marketing): прогноз отклика на депозит, порог при дисбалансе; эксперимент в venv. (Имя папки `churn_logreg` — историческое.)",
        "module_path": "modules/08_10_churn_logreg/",
        "data_note": "данные: [data/README.md](../../modules/08_10_churn_logreg/data/README.md) (UCI; **без `duration`** в признаках; CSV ещё не собран)",
        "themes": [
            "Логистическая регрессия — вероятность, сигмоида, порог; запрет leakage `duration`",
            "Практика: fit/predict, выбор порога (без `duration`)",
            "Метрики на несбалансированных классах",
            "Практика: метрики; CLI — запуск скрипта",
            "venv, requirements.txt, README эксперимента — сдача",
        ],
    },
    {
        "title": "Модуль 11. Виртуальный полигон: производная и градиентный спуск",
        "scenario": "Испытатели на полигоне изучают рельеф и ищут минимум градиентным спуском.",
        "note": "Обязательный модуль: интуиция производной и интеграла для 9 класса.",
        "module_path": "modules/08_11_virtual_polygon/",
        "themes": [
            "Производная как скорость изменения (интуитивно)",
            "Практика: численный градиентный спуск на 1D-функции",
            "Интеграл — площадь под кривой (обзорно); связь с loss",
            "Практика: движение к минимуму loss; рефлексия года",
        ],
    },
]


def pair_ranges() -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    n = 1
    for mod in MODULES:
        start = n
        n += len(mod["themes"])
        ranges.append((start, n - 1))
    return ranges


def render_modules() -> str:
    total = sum(len(m["themes"]) for m in MODULES)
    if total != TARGET_PAIRS:
        raise ValueError(f"expected {TARGET_PAIRS} pairs, got {total}")

    ranges = pair_ranges()
    lines = [
        "# КТП: 8 класс",
        "",
        "Статус: Draft 3",
        "",
        "Канонический документ профиля. Справочник `reference/` — только для сравнения, **не редактируется**.",
        "",
        "| Параметр | Значение |",
        "|---|---|",
        f"| Нагрузка | {HOURS_PER_WEEK} ч/нед |",
        f"| Учебных недель | {WEEKS} |",
        f"| Пар (тем) | {TARGET_PAIRS} |",
        "| Правило | 1 тема = 1 пара = 2 академических часа |",
        f"| Академических часов | {HOURS_PER_WEEK * WEEKS} (= {TARGET_PAIRS} × 2) |",
        "",
        "**Отработка:** строки «Практика: …» — серия задач на уже введённый навык (Foundation §5 принцип 8, Pedagogy §2). При дефиците часов сокращать число новых тем и обзорных пар, не практику.",
        "",
        "Индекс КТП: [07_KTP.md](../07_KTP.md).",
        "",
        "**Описания модулей** (1–2 абзаца для учителя): [08_module_descriptions.md](08_module_descriptions.md).",
        "",
        "**Стек после 8 класса** (уметь + API): [08_tech_stack_skills.md](08_tech_stack_skills.md).",
        "",
        "### Сетка модулей (после перехода 5→4 ч/нед)",
        "",
        "| Модуль | Пар | Диапазон КТП | Было |",
        "|---|---:|---|---|",
    ]
    old = [10, 10, 9, 8, 7, 8, 9, 8, 6, 6, 4]
    for i, mod in enumerate(MODULES):
        a, b = ranges[i]
        lines.append(
            f"| M{i + 1} | {len(mod['themes'])} | {a}–{b} | {old[i]} |"
        )
    lines.extend(["", "---", ""])

    n = 0
    for i, mod in enumerate(MODULES):
        cnt = len(mod["themes"])
        a, b = ranges[i]
        lines.append(f"## {mod['title']} ({cnt} пар)")
        lines.append("")
        lines.append(f"**Сюжет:** {mod['scenario']}")
        if mod.get("note"):
            lines.append("")
            lines.append(f"*{mod['note']}*")
        if mod.get("module_path"):
            lines.append("")
            mat = (
                f"**Материалы:** [{mod['module_path']}](../../{mod['module_path']}) "
                f"(пары {a}–{b})"
            )
            if mod.get("data_note"):
                mat += f" · {mod['data_note']}"
            lines.append(mat)
        lines.append("")
        lines.append("| # | Тема |")
        lines.append("|---|---|")
        for theme in mod["themes"]:
            n += 1
            lines.append(f"| {n} | {theme} |")
        lines.append("")

    lines.extend(
        [
            "---",
            "",
            "## Алгоритмический блок (обязательный)",
            "",
            "- Модуль 7 — массивы: поиск и сортировка (**введение + практика**)",
            "- Модуль 8 — структуры данных (до кучи не включительно; **введение + практика**)",
            "- Модуль 9 — DP, финал: игровые задачи (**введение + практика**)",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    body = render_modules()
    if OUT.exists():
        old = OUT.read_text(encoding="utf-8")
        marker = "## Карта инструментов"
        if marker in old:
            body = body.rstrip() + "\n\n---\n\n\n" + old[old.index(marker) :]
    OUT.write_text(body, encoding="utf-8")
    print(f"wrote {OUT} ({TARGET_PAIRS} pairs, {HOURS_PER_WEEK} h/wk × {WEEKS} wk)")


if __name__ == "__main__":
    main()
