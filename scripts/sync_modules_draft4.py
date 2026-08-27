#!/usr/bin/env python3
"""Align modules 08_04…08_11 (+ light M1/M5 merge slot) to KTP Draft 4 by renumbering / moving.

Does not rewrite lesson topics: only pair numbers, folder moves, README/UNIT calendars.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOD = ROOT / "modules"


def set_pair_in_lesson(lesson_md: Path, new_pair: int) -> None:
    text = lesson_md.read_text(encoding="utf-8")
    text2, n = re.subn(
        r"(\| Пара КТП \| \*\*)\d+(\*\*)",
        rf"\g<1>{new_pair}\2",
        text,
        count=1,
    )
    if n:
        lesson_md.write_text(text2, encoding="utf-8")
        print(f"  pair {new_pair}: {lesson_md.parent.name}")


def bump_pairs(module: str, mapping: dict[str, int]) -> None:
    """mapping: folder name -> new KTP pair number."""
    base = MOD / module / "lessons"
    print(module)
    for folder, pair in mapping.items():
        md = base / folder / "LESSON.md"
        if md.exists():
            set_pair_in_lesson(md, pair)
        else:
            print(f"  MISSING {md}")


def move_to_archive(module: str, folders: list[str]) -> None:
    base = MOD / module / "lessons"
    arch = base / "_archive_draft3"
    arch.mkdir(exist_ok=True)
    for name in folders:
        src = base / name
        if src.exists() and src.is_dir():
            dst = arch / name
            if dst.exists():
                shutil.rmtree(dst)
            shutil.move(str(src), str(dst))
            print(f"  archive {name}")


def write_readme(module: str, title: str, pairs: list[tuple[int, str, str]], note: str = "") -> None:
    lines = [
        f"# {title}",
        "",
        f"**Класс:** 8  ",
        f"**КТП:** пары **{pairs[0][0]}–{pairs[-1][0]}** (Draft 4)  ",
        "**Статус:** материалы; сетка выровнена под Draft 4 (перенос/сдвиг, без переписывания тем)",
        "",
    ]
    if note:
        lines += [note, ""]
    lines += ["## Уроки", "", "| Пара | Папка | Роль |", "|---|---|---|"]
    for p, folder, role in pairs:
        lines.append(f"| {p} | [{folder}](lessons/{folder}/) | {role} |")
    lines += ["", f"Unit Planner: [UNIT.md](UNIT.md).", ""]
    path = MOD / module / "README.md"
    # Keep existing README body after first heading if long? Prefer replace short calendar README.
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote README {module}")


def patch_unit_duration(module: str, n_pairs: int, start: int, end: int) -> None:
    path = MOD / module / "UNIT.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"\*\*Длительность:\*\*[^\n]+",
        f"**Длительность:** {n_pairs} пар по КТП ({n_pairs * 2} академических часов) — Draft 4",
        text,
        count=1,
    )
    text = re.sub(
        r"\| Длительность \(оценка\) \|[^\n]+",
        f"| Длительность (оценка) | {n_pairs * 2} академических часов ({n_pairs} пар КТП {start}–{end}) |",
        text,
        count=1,
    )
    path.write_text(text, encoding="utf-8")
    print(f"  patched UNIT duration {module}")


def main() -> None:
    # --- M4: +1 ---
    bump_pairs(
        "08_04_mnist_knn",
        {
            "01_probability_frequency": 25,
            "02_practice_split": 26,
            "03_knn_scaling": 27,
            "04_practice_knn_baseline": 28,
            "05_accuracy_f1_val": 29,
            "06_practice_search_metrics": 30,
        },
    )
    write_readme(
        "08_04_mnist_knn",
        "Распознавание цифр: вероятность и kNN",
        [
            (25, "01_probability_frequency", "введение"),
            (26, "02_practice_split", "отработка"),
            (27, "03_knn_scaling", "введение"),
            (28, "04_practice_knn_baseline", "отработка"),
            (29, "05_accuracy_f1_val", "введение"),
            (30, "06_practice_search_metrics", "отработка"),
        ],
    )
    patch_unit_duration("08_04_mnist_knn", 6, 25, 30)

    # --- M5: insert merge slot by copying 01 ---
    m5 = MOD / "08_05_shop_feature_engineering" / "lessons"
    merge_dst = m5 / "02_merge_join"
    if not merge_dst.exists():
        # shift existing 02..06 up numerically via temp names
        order = [
            "06_practice_pipeline",
            "05_logging_raise",
            "04_practice_aggregates",
            "03_rfm_groupby",
            "02_practice_apply_orders",
        ]
        for name in order:
            src = m5 / name
            if src.exists():
                src.rename(m5 / f"_tmp_{name}")
        # recreate numbered folders
        mapping_rename = [
            ("_tmp_02_practice_apply_orders", "03_practice_apply_orders"),
            ("_tmp_03_rfm_groupby", "04_rfm_groupby"),
            ("_tmp_04_practice_aggregates", "05_practice_aggregates"),
            ("_tmp_05_logging_raise", "06_logging_raise"),
            ("_tmp_06_practice_pipeline", "07_practice_pipeline"),
        ]
        for a, b in mapping_rename:
            src = m5 / a
            if src.exists():
                src.rename(m5 / b)
        shutil.copytree(m5 / "01_feature_types_apply", merge_dst)
        # mark LESSON for merge pair
        md = merge_dst / "LESSON.md"
        t = md.read_text(encoding="utf-8")
        t = re.sub(r"(\| Пара КТП \| \*\*)\d+(\*\*)", r"\g<1>32\2", t, count=1)
        t = re.sub(
            r"\| Название урока \|[^\n]+",
            "| Название урока | Объединение таблиц: merge / join (материалы из пары типов/apply; фокус на join) |",
            t,
            count=1,
        )
        md.write_text(t, encoding="utf-8")
        print("08_05: created 02_merge_join from 01")
    bump_pairs(
        "08_05_shop_feature_engineering",
        {
            "01_feature_types_apply": 31,
            "02_merge_join": 32,
            "03_practice_apply_orders": 33,
            "04_rfm_groupby": 34,
            "05_practice_aggregates": 35,
            "06_logging_raise": 36,
            "07_practice_pipeline": 37,
        },
    )
    write_readme(
        "08_05_shop_feature_engineering",
        "Интернет-магазин: Feature Engineering и lambda",
        [
            (31, "01_feature_types_apply", "введение"),
            (32, "02_merge_join", "введение (merge; из материалов 01)"),
            (33, "03_practice_apply_orders", "отработка"),
            (34, "04_rfm_groupby", "введение"),
            (35, "05_practice_aggregates", "отработка"),
            (36, "06_logging_raise", "введение"),
            (37, "07_practice_pipeline", "отработка / сдача"),
        ],
        note="Пара 32 — отдельный слот merge/join по КТП; ноутбуки скопированы из 01 (тема не писалась с нуля).",
    )
    patch_unit_duration("08_05_shop_feature_engineering", 7, 31, 37)

    # --- M6: +2 ---
    bump_pairs(
        "08_06_ab_startup",
        {
            "01_hypotheses_pvalue": 38,
            "02_practice_permutation": 39,
            "03_ci_correlation": 40,
            "04_practice_ci_corr": 41,
            "05_peeking_multireg": 42,
            "06_practice_report": 43,
        },
    )
    write_readme(
        "08_06_ab_startup",
        "A/B-тест стартапа и статистический вывод",
        [
            (38, "01_hypotheses_pvalue", "введение"),
            (39, "02_practice_permutation", "отработка"),
            (40, "03_ci_correlation", "введение"),
            (41, "04_practice_ci_corr", "отработка"),
            (42, "05_peeking_multireg", "введение"),
            (43, "06_practice_report", "отработка / отчёт"),
        ],
    )
    patch_unit_duration("08_06_ab_startup", 6, 38, 43)

    # --- M7: keep 01,02,05→03,06→04; archive sorts ---
    m7 = MOD / "08_07_bank_arrays_search" / "lessons"
    move_to_archive(
        "08_07_bank_arrays_search",
        ["03_selection_merge_quick", "04_practice_sorts"],
    )
    # rename 05→03, 07→ absorb into 03 calendar as complexity; 06→04
    if (m7 / "05_sorted_key_two_pointers").exists():
        if (m7 / "03_sorted_key_complexity").exists():
            shutil.rmtree(m7 / "03_sorted_key_complexity")
        (m7 / "05_sorted_key_two_pointers").rename(m7 / "03_sorted_key_complexity")
    if (m7 / "07_complexity_integration").exists():
        # keep as material next to 03 — move into 03 as subfolder extra
        extra = m7 / "03_sorted_key_complexity" / "complexity_integration_extra"
        if not extra.exists() and (m7 / "07_complexity_integration").exists():
            shutil.move(str(m7 / "07_complexity_integration"), str(extra))
            print("  nested 07 into 03 as extra")
    if (m7 / "06_practice_keys_pointers").exists():
        if (m7 / "04_practice_keys").exists():
            shutil.rmtree(m7 / "04_practice_keys")
        (m7 / "06_practice_keys_pointers").rename(m7 / "04_practice_keys")
    bump_pairs(
        "08_07_bank_arrays_search",
        {
            "01_linear_binary_search": 44,
            "02_practice_search_logs": 45,
            "03_sorted_key_complexity": 46,
            "04_practice_keys": 47,
        },
    )
    # note in 03 LESSON about KTP wording
    md46 = m7 / "03_sorted_key_complexity" / "LESSON.md"
    if md46.exists():
        t = md46.read_text(encoding="utf-8")
        t = re.sub(
            r"\| Название урока \|[^\n]+",
            "| Название урока | Сложность O(·); sorted(key=); set/dict O(1) (материалы Draft 3; two-pointers — по времени) |",
            t,
            count=1,
        )
        md46.write_text(t, encoding="utf-8")
    write_readme(
        "08_07_bank_arrays_search",
        "Массивы: поиск и сортировка",
        [
            (44, "01_linear_binary_search", "введение"),
            (45, "02_practice_search_logs", "отработка"),
            (46, "03_sorted_key_complexity", "введение"),
            (47, "04_practice_keys", "отработка"),
        ],
        note="Реализации mergesort/quicksort и лишние пары Draft 3 — в `lessons/_archive_draft3/`.",
    )
    patch_unit_duration("08_07_bank_arrays_search", 4, 44, 47)

    # --- M8: keep 03,04,06; archive stack and kmeans intro (copy already in M3) ---
    move_to_archive(
        "08_08_logistics_clustering",
        ["01_stack_queue_deque", "02_practice_buffers", "05_kmeans_dbscan"],
    )
    m8 = MOD / "08_08_logistics_clustering" / "lessons"
    if (m8 / "03_set_dict_freq").exists():
        (m8 / "03_set_dict_freq").rename(m8 / "01_set_dict_freq")
    if (m8 / "04_practice_membership_counts").exists():
        (m8 / "04_practice_membership_counts").rename(m8 / "02_practice_membership_counts")
    if (m8 / "06_practice_clusters_anomalies").exists():
        (m8 / "06_practice_clusters_anomalies").rename(m8 / "03_practice_clusters_anomalies")
    bump_pairs(
        "08_08_logistics_clustering",
        {
            "01_set_dict_freq": 48,
            "02_practice_membership_counts": 49,
            "03_practice_clusters_anomalies": 50,
        },
    )
    write_readme(
        "08_08_logistics_clustering",
        "Структуры данных, кластеризация и аномалии",
        [
            (48, "01_set_dict_freq", "введение"),
            (49, "02_practice_membership_counts", "отработка"),
            (50, "03_practice_clusters_anomalies", "отработка"),
        ],
        note="Стек/очередь и введение k-means — в `_archive_draft3/` (k-means intro скопирован в M3 пара 23).",
    )
    patch_unit_duration("08_08_logistics_clustering", 3, 48, 50)

    # --- M9 logreg: 51–54; archive venv ---
    move_to_archive("08_10_churn_logreg", ["05_venv_requirements_readme"])
    bump_pairs(
        "08_10_churn_logreg",
        {
            "01_logreg_sigmoid_threshold": 51,
            "02_practice_fit_threshold": 52,
            "03_imbalance_metrics": 53,
            "04_practice_metrics_cli": 54,
        },
    )
    md54 = MOD / "08_10_churn_logreg" / "lessons" / "04_practice_metrics_cli" / "LESSON.md"
    if md54.exists():
        t = md54.read_text(encoding="utf-8")
        t = re.sub(
            r"\| Название урока \|[^\n]+",
            "| Название урока | Практика: метрики (CLI в материалах — по желанию; venv — 9 класс) |",
            t,
            count=1,
        )
        md54.write_text(t, encoding="utf-8")
    write_readme(
        "08_10_churn_logreg",
        "Отток клиентов: логистическая регрессия",
        [
            (51, "01_logreg_sigmoid_threshold", "введение"),
            (52, "02_practice_fit_threshold", "отработка"),
            (53, "03_imbalance_metrics", "введение"),
            (54, "04_practice_metrics_cli", "отработка"),
        ],
        note="Пара venv/requirements — в `_archive_draft3/` (по КТП Draft 4 → 9 класс).",
    )
    patch_unit_duration("08_10_churn_logreg", 4, 51, 54)

    # --- M10 polygon: 65–68 → 55–58 ---
    bump_pairs(
        "08_11_virtual_polygon",
        {
            "01_derivative_intuition": 55,
            "02_practice_gd_1d": 56,
            "03_integral_loss_overview": 57,
            "04_practice_min_loss_year_reflect": 58,
        },
    )
    write_readme(
        "08_11_virtual_polygon",
        "Виртуальный полигон: производная и градиентный спуск",
        [
            (55, "01_derivative_intuition", "введение"),
            (56, "02_practice_gd_1d", "отработка"),
            (57, "03_integral_loss_overview", "введение"),
            (58, "04_practice_min_loss_year_reflect", "отработка / рефлексия"),
        ],
    )
    patch_unit_duration("08_11_virtual_polygon", 4, 55, 58)

    # --- M1 light: ensure README says 1–8 ---
    write_readme(
        "08_01_functions_recursion",
        "Оценка недвижимости: функции и inference pipeline",
        [
            (1, "01_intro_profile", "ориентация"),
            (2, "02_function_as_mapping", "введение"),
            (3, "03_parameters_and_return", "введение"),
            (4, "04_practice_transform", "отработка"),
            (5, "05_scope_and_debugging", "введение"),
            (6, "06_practice_metrics", "отработка"),
            (7, "07_recursion_pipeline", "введение"),
            (8, "08_artifact", "интеграция"),
        ],
        note="Сетка пар уже 1–8; темы не менялись.",
    )
    patch_unit_duration("08_01_functions_recursion", 8, 1, 8)

    print("DONE")


if __name__ == "__main__":
    main()
