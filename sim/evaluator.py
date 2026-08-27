"""
evaluator.py — оценщик программы.

Запускает N студентов, прогоняет каждого через экзамен,
агрегирует результаты и формирует markdown-отчёт с рекомендациями.

Основные метрики агрегации:
  - pass_rate по каждой компетенции (% студентов, прошедших порог)
  - mean/std overall_score
  - % студентов с полным портретом выпускника
  - топ-10 тем с наименьшей долей mastered (системные пробелы программы)
  - топ-10 тем с наибольшей долей mastered (сильные стороны)
  - распределение capacity (mean/std)
"""

from __future__ import annotations

import random
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from examiner import COMPETENCY_LABELS, ExamReport, examine
from parse_curriculum import pairs_with_tags
from student import MemState, SimResult, simulate_student, StudentConfig


@dataclass
class EvalConfig:
    n_students: int = 100
    seed: int = 0          # 0 = случайный при каждом запуске
    grade: int = 8
    student_config: StudentConfig = field(default_factory=StudentConfig)


@dataclass
class AggregateReport:
    n_students: int
    run_at: str
    grade: int
    # портрет выпускника
    graduate_profile_rate: float          # доля с all-passed
    overall_mean: float
    overall_std: float
    capacity_mean: float
    capacity_std: float
    # по компетенциям
    competency_pass_rates: dict[str, float]   # key → rate 0..1
    # темы
    weak_topics: list[tuple[str, float]]      # (tag, mastered_rate) — топ-10 слабых
    strong_topics: list[tuple[str, float]]    # (tag, mastered_rate) — топ-10 сильных
    # рекомендации
    recommendations: list[str]


def run_evaluation(config: EvalConfig | None = None) -> AggregateReport:
    if config is None:
        config = EvalConfig()

    seed = config.seed if config.seed != 0 else random.randint(1, 10**9)
    master_rng = random.Random(seed)

    pairs = pairs_with_tags()

    reports: list[ExamReport] = []
    all_topic_states: dict[str, list[MemState]] = defaultdict(list)

    for i in range(config.n_students):
        student_rng = random.Random(master_rng.randint(0, 2**31))
        result = simulate_student(
            pairs,
            rng=student_rng,
            config=config.student_config,
            student_id=i + 1,
        )
        report = examine(result)
        reports.append(report)

        for tag, rec in result.topic_states.items():
            all_topic_states[tag].append(rec.state)

    # агрегация
    graduate_rate = sum(1 for r in reports if r.graduate_profile_met) / len(reports)
    overall_scores = [r.overall_score for r in reports]
    capacities = [r.capacity for r in reports]

    competency_pass_rates: dict[str, float] = {}
    for key in COMPETENCY_LABELS:
        passed = sum(
            1 for r in reports
            if any(c.passed for c in r.competencies if c.key == key)
        )
        competency_pass_rates[key] = passed / len(reports)

    # mastered rate по темам
    topic_mastered_rate: dict[str, float] = {}
    for tag, states in all_topic_states.items():
        mastered = sum(1 for s in states if s == MemState.MASTERED)
        topic_mastered_rate[tag] = mastered / len(states)

    sorted_topics = sorted(topic_mastered_rate.items(), key=lambda x: x[1])
    weak_topics = sorted_topics[:10]
    strong_topics = list(reversed(sorted_topics[-10:]))

    recommendations = _generate_recommendations(
        competency_pass_rates,
        graduate_rate,
        weak_topics,
        config,
    )

    return AggregateReport(
        n_students=config.n_students,
        run_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        grade=config.grade,
        graduate_profile_rate=round(graduate_rate, 3),
        overall_mean=round(statistics.mean(overall_scores), 3),
        overall_std=round(statistics.stdev(overall_scores) if len(overall_scores) > 1 else 0.0, 3),
        capacity_mean=round(statistics.mean(capacities), 3),
        capacity_std=round(statistics.stdev(capacities) if len(capacities) > 1 else 0.0, 3),
        competency_pass_rates={k: round(v, 3) for k, v in competency_pass_rates.items()},
        weak_topics=[(t, round(r, 3)) for t, r in weak_topics],
        strong_topics=[(t, round(r, 3)) for t, r in strong_topics],
        recommendations=recommendations,
    )


def _generate_recommendations(
    pass_rates: dict[str, float],
    graduate_rate: float,
    weak_topics: list[tuple[str, float]],
    config: EvalConfig,
) -> list[str]:
    recs: list[str] = []

    if graduate_rate < 0.5:
        recs.append(
            f"Критично: только {graduate_rate*100:.0f}% студентов формируют полный портрет выпускника. "
            "Рассмотрите увеличение числа встреч с ключевыми темами или пересмотр окон повторения."
        )
    elif graduate_rate < 0.75:
        recs.append(
            f"Портрет выпускника формируется у {graduate_rate*100:.0f}% студентов. "
            "Возможно усиление: добавить пары повторения или домашние задания на слабые темы."
        )

    for key, label in COMPETENCY_LABELS.items():
        rate = pass_rates.get(key, 0.0)
        if rate < 0.6:
            recs.append(
                f"Компетенция «{label}»: только {rate*100:.0f}% студентов достигают порога. "
                "Рекомендуется добавить дополнительную практику по этой компетенции."
            )

    if weak_topics:
        names = ", ".join(f"«{t}»" for t, _ in weak_topics[:3])
        recs.append(
            f"Системные пробелы (низкий mastered rate): {names}. "
            "Эти темы встречаются редко или с большим разрывом между встречами — добавьте повторение."
        )

    if not recs:
        recs.append("Программа обеспечивает формирование портрета выпускника у большинства студентов.")

    return recs


def format_aggregate_report(report: AggregateReport) -> str:
    lines = [
        f"# Отчёт оценщика программы — {report.grade} класс",
        f"Запуск: {report.run_at}  |  Студентов: {report.n_students}",
        "",
        "## Сводка",
        f"| Метрика | Значение |",
        "|---|---|",
        f"| Портрет выпускника сформирован | **{report.graduate_profile_rate*100:.0f}%** |",
        f"| Средний итоговый балл | {report.overall_mean:.3f} ± {report.overall_std:.3f} |",
        f"| Средняя успеваемость (capacity) | {report.capacity_mean:.3f} ± {report.capacity_std:.3f} |",
        "",
        "## Компетенции (% студентов прошли порог 0.65)",
        "| Компетенция | Pass rate |",
        "|---|---|",
    ]
    for key, label in COMPETENCY_LABELS.items():
        rate = report.competency_pass_rates.get(key, 0.0)
        flag = "✓" if rate >= 0.65 else "✗"
        lines.append(f"| {label} | {rate*100:.0f}% {flag} |")

    lines += [
        "",
        "## Слабые темы (топ-10 по низкому mastered rate)",
        "| Тема | Mastered rate |",
        "|---|---|",
    ]
    for tag, rate in report.weak_topics:
        lines.append(f"| {tag} | {rate*100:.0f}% |")

    lines += [
        "",
        "## Сильные темы (топ-10 по высокому mastered rate)",
        "| Тема | Mastered rate |",
        "|---|---|",
    ]
    for tag, rate in report.strong_topics:
        lines.append(f"| {tag} | {rate*100:.0f}% |")

    lines += ["", "## Рекомендации"]
    for i, rec in enumerate(report.recommendations, 1):
        lines.append(f"{i}. {rec}")

    return "\n".join(lines)


if __name__ == "__main__":
    config = EvalConfig(n_students=100)
    agg = run_evaluation(config)
    print(format_aggregate_report(agg))
