#!/usr/bin/env python3
"""Fix 'Дальше' links and UNIT calendars after Draft 4 folder renumbers."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOD = ROOT / "modules"

# module -> ordered (pair, folder, role)
GRIDS = {
    "08_01_functions_recursion": [
        (1, "01_intro_profile", "ориентация"),
        (2, "02_function_as_mapping", "введение"),
        (3, "03_parameters_and_return", "введение"),
        (4, "04_practice_transform", "отработка"),
        (5, "05_scope_and_debugging", "введение"),
        (6, "06_practice_metrics", "отработка"),
        (7, "07_recursion_pipeline", "введение"),
        (8, "08_artifact", "интеграция"),
    ],
    "08_02_carsharing_pandas_lr": [
        (9, "01_pandas_dataframe", "введение + фильтры"),
        (10, "02_eda_scatter", "введение"),
        (11, "03_train_test_lr", "введение"),
        (12, "04_practice_metrics", "отработка"),
        (13, "05_try_except_csv", "введение"),
        (14, "06_practice_features", "отработка"),
        (15, "07_report_build", "интеграция"),
        (16, "08_report_submit", "интеграция"),
    ],
    "08_03_titanic_eda": [
        (17, "01_load_inspect_paths", "введение"),
        (18, "02_practice_inspect", "отработка"),
        (19, "03_mean_median_std", "введение"),
        (20, "04_practice_boxplot", "отработка"),
        (21, "05_bias_clt_missing", "введение"),
        (22, "06_practice_groups", "отработка"),
        (23, "07_kmeans_dbscan_eda", "введение"),
        (24, "08_eda_report", "интеграция"),
    ],
    "08_04_mnist_knn": [
        (25, "01_probability_frequency", "введение"),
        (26, "02_practice_split", "отработка"),
        (27, "03_knn_scaling", "введение"),
        (28, "04_practice_knn_baseline", "отработка"),
        (29, "05_accuracy_f1_val", "введение"),
        (30, "06_practice_search_metrics", "отработка"),
    ],
    "08_05_shop_feature_engineering": [
        (31, "01_feature_types_apply", "введение"),
        (32, "02_merge_join", "введение"),
        (33, "03_practice_apply_orders", "отработка"),
        (34, "04_rfm_groupby", "введение"),
        (35, "05_practice_aggregates", "отработка"),
        (36, "06_logging_raise", "введение"),
        (37, "07_practice_pipeline", "отработка"),
    ],
    "08_06_ab_startup": [
        (38, "01_hypotheses_pvalue", "введение"),
        (39, "02_practice_permutation", "отработка"),
        (40, "03_ci_correlation", "введение"),
        (41, "04_practice_ci_corr", "отработка"),
        (42, "05_peeking_multireg", "введение"),
        (43, "06_practice_report", "отработка"),
    ],
    "08_07_bank_arrays_search": [
        (44, "01_linear_binary_search", "введение"),
        (45, "02_practice_search_logs", "отработка"),
        (46, "03_sorted_key_complexity", "введение"),
        (47, "04_practice_keys", "отработка"),
    ],
    "08_08_logistics_clustering": [
        (48, "01_set_dict_freq", "введение"),
        (49, "02_practice_membership_counts", "отработка"),
        (50, "03_practice_clusters_anomalies", "отработка"),
    ],
    "08_10_churn_logreg": [
        (51, "01_logreg_sigmoid_threshold", "введение"),
        (52, "02_practice_fit_threshold", "отработка"),
        (53, "03_imbalance_metrics", "введение"),
        (54, "04_practice_metrics_cli", "отработка"),
    ],
    "08_11_virtual_polygon": [
        (55, "01_derivative_intuition", "введение"),
        (56, "02_practice_gd_1d", "отработка"),
        (57, "03_integral_loss_overview", "введение"),
        (58, "04_practice_min_loss_year_reflect", "отработка"),
    ],
    "08_09_courier_dp": [
        (59, "01_memo_dp1d", "введение"),
        (60, "02_practice_dp1d", "отработка"),
        (61, "03_dp2d", "введение"),
        (62, "04_practice_dp2d", "отработка"),
        (63, "05_games_when_dp", "интеграция"),
    ],
}

NEXT_MODULE = {
    "08_01_functions_recursion": "модуль 2 (pandas / LR)",
    "08_02_carsharing_pandas_lr": "модуль 3 (Titanic EDA)",
    "08_03_titanic_eda": "модуль 4 (kNN)",
    "08_04_mnist_knn": "модуль 5 (Feature Engineering)",
    "08_05_shop_feature_engineering": "модуль 6 (A/B)",
    "08_06_ab_startup": "модуль 7 (поиск / сложность)",
    "08_07_bank_arrays_search": "модуль 8 (set/dict / аномалии)",
    "08_08_logistics_clustering": "модуль 9 (логистическая регрессия)",
    "08_10_churn_logreg": "модуль 10 (полигон / GD)",
    "08_11_virtual_polygon": "доп. модуль 11 (DP) или конец года",
    "08_09_courier_dp": "конец года / резерв",
}


def fix_dalshe(module: str, grid: list) -> None:
    lessons = MOD / module / "lessons"
    for i, (pair, folder, _role) in enumerate(grid):
        md = lessons / folder / "LESSON.md"
        if not md.exists():
            continue
        text = md.read_text(encoding="utf-8")
        if i + 1 < len(grid):
            np, nf, _ = grid[i + 1]
            new = f"| **Дальше** | [пара {np}](../{nf}/LESSON.md) |"
        else:
            new = f"| **Дальше** | {NEXT_MODULE.get(module, 'следующий модуль')} |"
        text2, n = re.subn(r"\| \*\*Дальше\*\* \|[^\n]+", new, text, count=1)
        if n:
            md.write_text(text2, encoding="utf-8")
            print(f"  Дальше {module}/{folder}")


def rewrite_unit_calendar(module: str, grid: list) -> None:
    path = MOD / module / "UNIT.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    rows = ["| Пара | Роль | План |", "|---|---|---|"]
    for p, folder, role in grid:
        rows.append(f"| {p} | {role} | [{folder}](lessons/{folder}/LESSON.md) |")
    block = "\n".join(rows)
    # replace first calendar-like table after "календарь"
    m = re.search(
        r"(### Для преподавателя: календарь пар\n\n)(\| Пара \|.*?)(\n\n---)",
        text,
        re.S,
    )
    if m:
        text = text[: m.start(2)] + block + text[m.end(2) :]
        path.write_text(text, encoding="utf-8")
        print(f"  UNIT calendar {module}")
    else:
        print(f"  UNIT calendar skip {module}")


def main() -> None:
    for module, grid in GRIDS.items():
        print(module)
        fix_dalshe(module, grid)
        rewrite_unit_calendar(module, grid)
    print("DONE")


if __name__ == "__main__":
    main()
