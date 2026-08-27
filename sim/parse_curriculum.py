"""
parse_curriculum.py — парсер учебных материалов.

Читает материалы уроков в modules/08_*/lessons/* и возвращает список пар:
    [(pair_id: int, module: str, concept_tags: list[str]), ...]

Источники для каждой пары:
  - LESSON.md (теория/сценарий)
  - lesson.ipynb (теория + практика)
  - homework.ipynb
  - solutions.ipynb (важно: фиксируем реально используемые концепты, даже если
    они не были заявлены в теме пары)
"""

from __future__ import annotations

import re
import json
from pathlib import Path
from typing import NamedTuple


REPO_ROOT = Path(__file__).parent.parent
MODULES_DIR = REPO_ROOT / "modules"


class Pair(NamedTuple):
    pair_id: int
    module: str      # e.g. "M1"
    raw_topic: str   # aggregated text from lesson materials


CONCEPT_RULES: list[tuple[str, str]] = [
    (r"\bdef\b|функц|return|параметр", "python_functions"),
    (r"scope|отладк|баг|assert|try|except|raise|logging", "python_debugging"),
    (r"рекурси|lambda|hof|pipeline", "python_advanced_functions"),
    (r"pandas|dataframe|read_csv|groupby|rfm|preprocessing|apply", "data_tabular_ops"),
    (r"eda|describe|scatter|гистограмм|boxplot|квартил|пропуск|выброс", "data_eda"),
    (r"train/test|split|выборк", "data_splitting"),
    (r"вероятност|комбинатор|h₀|h1|p-value|перестановочн|доверительн|корреляц", "math_stats_inference"),
    (r"mae|mse|r²|accuracy|f1|метрик|confusion|дисбаланс", "ml_metrics"),
    (r"knn|ближайш|выбор k|min-max", "ml_knn"),
    (r"linearregression|линейн(ая|ой) регресс", "ml_linear_regression"),
    (r"логистическ|сигмоид|порог|leakage|duration", "ml_logreg_classification"),
    (r"k-means|dbscan|кластер|аномали", "ml_clustering_anomaly"),
    (r"поиск|сортиров|бинарн|линейн|mergesort|quicksort|двух указател", "alg_search_sort"),
    (r"dp|динамическ|мемоизац|табличн|игров", "alg_dp_games"),
    (r"стек|очеред|deque|dict|set|hash", "alg_data_structures"),
    (r"производн|градиент|интеграл|loss", "math_calculus_optimization"),
    (r"venv|requirements|cli|скрипта", "eng_tooling_repro"),
    (r"артефакт|сборк|сдач|отч[её]т|рефлекси", "eng_artifact_delivery"),
]


def _extract_topic_tags(raw: str) -> list[str]:
    """Нарезает общий текст пары на короткие фрагменты для сопоставления."""
    raw = re.sub(r"`([^`]+)`", r"\1", raw)
    raw = re.sub(r"\([^)]*\)", " ", raw)
    raw = re.sub(r"\s+", " ", raw)

    parts = re.split(r"\s+[—–-]\s+|;|:|,|\.", raw)
    tags: list[str] = []
    for part in parts:
        part = part.strip(" ,.")
        if len(part) > 2:
            tags.append(part)
    return tags


def _normalize_to_concepts(tags: list[str]) -> list[str]:
    """Преобразует сырые теги в канонические мини-темы (повторяемые между парами)."""
    concepts: set[str] = set()
    for tag in tags:
        low = tag.lower()
        for pattern, concept in CONCEPT_RULES:
            if re.search(pattern, low):
                concepts.add(concept)
    # fallback: если не нашли ни одной концепции, оставляем укороченный raw-тег
    if not concepts:
        for tag in tags:
            cleaned = re.sub(r"\s+", " ", tag.strip().lower())
            if cleaned:
                concepts.add(f"raw:{cleaned[:60]}")
    return sorted(concepts)


def _read_text_file(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _read_notebook_text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return ""

    chunks: list[str] = []
    for cell in data.get("cells", []):
        source = cell.get("source", [])
        if isinstance(source, list):
            chunks.append("".join(source))
        elif isinstance(source, str):
            chunks.append(source)
    return "\n".join(chunks)


def _module_to_label(module_dir_name: str) -> str:
    m = re.match(r"^08_(\d+)_", module_dir_name)
    if not m:
        return "M?"
    return f"M{int(m.group(1)) - 0}"


def parse_materials(modules_dir: Path = MODULES_DIR) -> list[Pair]:
    """Парсит материалы уроков модулей 8 класса → список Pair."""
    pairs: list[Pair] = []
    pair_counter = 0

    module_dirs = sorted(
        [p for p in modules_dir.glob("08_*") if p.is_dir() and (p / "lessons").exists()]
    )
    for module_dir in module_dirs:
        module_label = _module_to_label(module_dir.name)
        lesson_dirs = sorted([p for p in (module_dir / "lessons").glob("*") if p.is_dir()])
        for lesson_dir in lesson_dirs:
            lesson_md = _read_text_file(lesson_dir / "LESSON.md")
            lesson_nb = _read_notebook_text(lesson_dir / "lesson.ipynb")
            hw_nb = _read_notebook_text(lesson_dir / "homework.ipynb")
            sol_nb = _read_notebook_text(lesson_dir / "solutions.ipynb")

            combined = "\n".join([
                f"[module] {module_dir.name}",
                f"[lesson] {lesson_dir.name}",
                lesson_md,
                lesson_nb,
                hw_nb,
                sol_nb,
            ])
            if not combined.strip():
                continue

            pair_counter += 1
            pairs.append(Pair(pair_id=pair_counter, module=module_label, raw_topic=combined))

    return pairs


def pairs_with_tags(path: Path | None = None) -> list[tuple[int, str, list[str]]]:
    """Возвращает (pair_id, module, [concept_tags]) по материалам уроков."""
    pairs = [
        (p.pair_id, p.module, _normalize_to_concepts(_extract_topic_tags(p.raw_topic)))
        for p in parse_materials(MODULES_DIR)
    ]
    if not pairs:
        raise ValueError(
            "Materials parser returned 0 lesson pairs. "
            "Check modules/08_*/lessons structure and notebook files."
        )
    return pairs


if __name__ == "__main__":
    for pid, mod, tags in pairs_with_tags():
        print(f"{pid:3d} [{mod}]  {tags}")
