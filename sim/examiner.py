"""
examiner.py — экзаменатор.

Принимает SimResult одного студента, маппит итоговые состояния тем
на 5 компетенций Foundation §3 и выдаёт ExamReport.

Логика оценки:
  - Для каждой компетенции собираем теги, которые к ней относятся.
  - Каждый тег имеет вес (из competency_map.yaml → weights, иначе 1.0).
  - Балл по компетенции = взвешенная доля тем в состоянии mastered/practiced.
    mastered → 1.0 × weight
    practiced → 0.6 × weight
    met → 0.2 × weight
    forgotten/unseen → 0.0

  - Итоговый балл нормируется в [0, 1].
  - Порог «сформировано»: score ≥ 0.65.

Профиль выпускника (Foundation §3, пять пунктов):
  C1  программирует как инженер
  C2  работает с данными
  C3  применяет ML
  C4  мыслит математически
  C5  создаёт артефакты
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from student import MemState, SimResult

COMPETENCY_MAP_PATH = Path(__file__).parent / "competency_map.yaml"

COMPETENCY_LABELS = {
    "C1_programming": "Программирует как инженер",
    "C2_data": "Работает с данными",
    "C3_ml": "Применяет ML",
    "C4_math": "Мыслит математически",
    "C5_artifacts": "Создаёт артефакты",
}

STATE_SCORE = {
    MemState.MASTERED: 1.0,
    MemState.PRACTICED: 0.6,
    MemState.MET: 0.2,
    MemState.FORGOTTEN: 0.0,
    MemState.UNSEEN: 0.0,
}

PASS_THRESHOLD = 0.65


def _load_map(path: Path = COMPETENCY_MAP_PATH) -> tuple[dict[str, list[str]], dict[str, float]]:
    """Загружает competency_map.yaml → (competency_patterns, weights)."""
    data: dict[str, Any] = yaml.safe_load(path.read_text(encoding="utf-8"))
    competencies: dict[str, list[str]] = {}
    for key in COMPETENCY_LABELS:
        competencies[key] = [p.lower() for p in data.get(key, [])]
    weights: dict[str, float] = {k.lower(): float(v) for k, v in data.get("weights", {}).items()}
    return competencies, weights


def _tag_weight(tag: str, weights: dict[str, float]) -> float:
    tag_lower = tag.lower()
    for pattern, w in weights.items():
        if pattern in tag_lower:
            return w
    return 1.0


def _tag_matches(tag: str, patterns: list[str]) -> bool:
    tag_lower = tag.lower()
    return any(p in tag_lower for p in patterns)


@dataclass
class CompetencyScore:
    key: str
    label: str
    score: float          # 0.0–1.0
    passed: bool
    contributing_tags: list[str]   # теги, попавшие в эту компетенцию
    gap_tags: list[str]            # важные теги в состоянии unseen/forgotten


@dataclass
class ExamReport:
    student_id: int
    capacity: float
    competencies: list[CompetencyScore]
    overall_score: float        # среднее по компетенциям
    graduate_profile_met: bool  # True если все C1–C5 passed
    gap_summary: list[str]      # топ-5 «пробелов» (теги с низким баллом и высоким весом)


def examine(result: SimResult, map_path: Path = COMPETENCY_MAP_PATH) -> ExamReport:
    """Оценивает SimResult → ExamReport."""
    competencies_patterns, weights = _load_map(map_path)

    comp_scores: list[CompetencyScore] = []

    for comp_key, label in COMPETENCY_LABELS.items():
        patterns = competencies_patterns.get(comp_key, [])
        total_weight = 0.0
        earned_weight = 0.0
        contributing: list[str] = []
        gaps: list[str] = []

        for tag, rec in result.topic_states.items():
            if not _tag_matches(tag, patterns):
                continue
            w = _tag_weight(tag, weights)
            total_weight += w
            earned = STATE_SCORE[rec.state] * w
            earned_weight += earned
            contributing.append(tag)
            if rec.state in (MemState.UNSEEN, MemState.FORGOTTEN, MemState.MET):
                gaps.append(tag)

        score = (earned_weight / total_weight) if total_weight > 0 else 0.0
        comp_scores.append(CompetencyScore(
            key=comp_key,
            label=label,
            score=round(score, 3),
            passed=score >= PASS_THRESHOLD,
            contributing_tags=contributing,
            gap_tags=gaps,
        ))

    overall = sum(c.score for c in comp_scores) / len(comp_scores) if comp_scores else 0.0
    all_passed = all(c.passed for c in comp_scores)

    # топ-5 пробелов по весу × (1 - score)
    gap_candidates: list[tuple[float, str]] = []
    for tag, rec in result.topic_states.items():
        if rec.state in (MemState.UNSEEN, MemState.FORGOTTEN):
            w = _tag_weight(tag, weights)
            gap_candidates.append((w, tag))
    gap_candidates.sort(reverse=True)
    top_gaps = [g for _, g in gap_candidates[:5]]

    return ExamReport(
        student_id=result.student_id,
        capacity=round(result.capacity, 3),
        competencies=comp_scores,
        overall_score=round(overall, 3),
        graduate_profile_met=all_passed,
        gap_summary=top_gaps,
    )


def format_report(report: ExamReport) -> str:
    lines = [
        f"## Результат экзамена — студент #{report.student_id}",
        f"Capacity: {report.capacity:.3f}  |  Итоговый балл: {report.overall_score:.3f}  |  "
        f"Портрет выпускника: {'✓ сформирован' if report.graduate_profile_met else '✗ не сформирован'}",
        "",
        "| Компетенция | Балл | Статус |",
        "|---|---|---|",
    ]
    for c in report.competencies:
        status = "✓" if c.passed else "✗"
        lines.append(f"| {c.label} | {c.score:.2f} | {status} |")

    if report.gap_summary:
        lines += ["", "**Топ пробелов:**"]
        for g in report.gap_summary:
            lines.append(f"- {g}")

    return "\n".join(lines)


if __name__ == "__main__":
    import random
    import sys
    sys.path.insert(0, str(Path(__file__).parent))

    from parse_curriculum import pairs_with_tags
    from student import simulate_student

    pairs = pairs_with_tags()
    rng = random.Random(42)
    result = simulate_student(pairs, rng=rng, student_id=1)
    report = examine(result)
    print(format_report(report))
