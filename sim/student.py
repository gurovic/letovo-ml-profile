"""
student.py — вероятностная модель памяти студента.

Модель памяти (spacing effect, 4 состояния):

    unseen  ──p_met──►  met  ──p_practiced──►  practiced  ──p_mastered──►  mastered
                          │                        │                            │
                     (gap > W1)              (gap > W2)               p_forget/pair
                          ▼                        ▼                            ▼
                       forgotten               forgotten                   forgotten

Параметры (настраиваемые через StudentConfig):
  p_met         вероятность перехода unseen→met при первой встрече     0.90
  p_practiced   вероятность перехода met→practiced при 2-й встрече     0.75
  p_mastered    вероятность перехода practiced→mastered при 3-й        0.85
  p_forget_m    вероятность забыть mastered за одну пару               0.02
  window_1      макс. пар между 1-й и 2-й встречей для practiced       8
  window_2      макс. пар между 2-й и 3-й встречей для mastered        12

  student_capacity ~ Beta(alpha=8, beta=2) масштабирует все p_* кроме p_forget
  (сильный студент — p ближе к 1; слабый — ниже базы)

Формат одного прогона:
    simulate_student(pairs, rng, config) -> SimResult
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator


class MemState(str, Enum):
    UNSEEN = "unseen"
    MET = "met"
    PRACTICED = "practiced"
    MASTERED = "mastered"
    FORGOTTEN = "forgotten"


@dataclass
class StudentConfig:
    p_met: float = 0.90
    p_practiced: float = 0.75
    p_mastered: float = 0.85
    p_forget_mastered: float = 0.02
    window_1: int = 8    # пар между 1-й и 2-й встречей
    window_2: int = 12   # пар между 2-й и 3-й встречей
    # Beta-параметры для сэмплирования capacity
    capacity_alpha: float = 8.0
    capacity_beta: float = 2.0


@dataclass
class TopicRecord:
    state: MemState = MemState.UNSEEN
    encounter_count: int = 0
    last_encounter_pair: int = -1   # pair_id последней встречи
    second_encounter_pair: int = -1 # pair_id 2-й встречи (нужен для окна→mastered)


@dataclass
class SimResult:
    student_id: int
    capacity: float                          # сэмплированное из Beta
    topic_states: dict[str, TopicRecord]     # tag → запись
    pair_log: list[dict]                     # лог по парам для отладки


def _scale_p(p: float, capacity: float) -> float:
    """Масштабирует вероятность capacity-фактором ∈ [0, 1]."""
    # capacity ~ Beta(8,2) со средним 0.8; масштаб линейно
    return min(1.0, p * capacity)


def _beta_sample(rng: random.Random, alpha: float, beta: float) -> float:
    """Сэмплирует из Beta(alpha, beta) через гамма-аппроксимацию."""
    x = rng.gammavariate(alpha, 1.0)
    y = rng.gammavariate(beta, 1.0)
    return x / (x + y)


def simulate_student(
    pairs: list[tuple[int, str, list[str]]],
    rng: random.Random | None = None,
    config: StudentConfig | None = None,
    student_id: int = 0,
) -> SimResult:
    """
    Прогоняет одного студента через список пар КТП.

    pairs: [(pair_id, module, [topic_tags]), ...]
           — результат parse_curriculum.pairs_with_tags()

    Возвращает SimResult с итоговым состоянием по каждому тегу.
    """
    if rng is None:
        rng = random.Random()
    if config is None:
        config = StudentConfig()

    capacity = _beta_sample(rng, config.capacity_alpha, config.capacity_beta)
    topics: dict[str, TopicRecord] = {}
    pair_log: list[dict] = []

    for pair_id, module, tags in sorted(pairs, key=lambda x: x[0]):
        pair_events: list[dict] = []

        for tag in tags:
            if tag not in topics:
                topics[tag] = TopicRecord()

            rec = topics[tag]
            old_state = rec.state
            new_state = _transition(rec, pair_id, capacity, rng, config)
            rec.state = new_state

            if new_state != old_state:
                pair_events.append({"tag": tag, "old": old_state, "new": new_state})

        # decay: mastered-темы могут забыться между парами
        for tag, rec in topics.items():
            if rec.state == MemState.MASTERED:
                if rng.random() < config.p_forget_mastered:
                    rec.state = MemState.PRACTICED   # деградация до practiced, не до unseen
                    pair_events.append({"tag": tag, "old": MemState.MASTERED, "new": MemState.PRACTICED, "decay": True})

        pair_log.append({"pair_id": pair_id, "module": module, "events": pair_events})

    return SimResult(
        student_id=student_id,
        capacity=capacity,
        topic_states=topics,
        pair_log=pair_log,
    )


def _transition(
    rec: TopicRecord,
    pair_id: int,
    capacity: float,
    rng: random.Random,
    cfg: StudentConfig,
) -> MemState:
    """Вычисляет новое состояние записи при встрече темы на паре pair_id."""
    state = rec.state

    if state in (MemState.UNSEEN, MemState.FORGOTTEN):
        # первая (или повторная после забывания) встреча
        if rng.random() < _scale_p(cfg.p_met, capacity):
            rec.encounter_count = 1
            rec.last_encounter_pair = pair_id
            rec.second_encounter_pair = -1
            return MemState.MET
        return state  # не «взял» тему

    elif state == MemState.MET:
        gap = pair_id - rec.last_encounter_pair
        if gap > cfg.window_1:
            # слишком поздно — забыл
            rec.encounter_count = 0
            return MemState.FORGOTTEN
        if rng.random() < _scale_p(cfg.p_practiced, capacity):
            rec.encounter_count = 2
            rec.second_encounter_pair = pair_id
            rec.last_encounter_pair = pair_id
            return MemState.PRACTICED
        rec.last_encounter_pair = pair_id
        return MemState.MET

    elif state == MemState.PRACTICED:
        base_pair = rec.second_encounter_pair if rec.second_encounter_pair >= 0 else rec.last_encounter_pair
        gap = pair_id - base_pair
        if gap > cfg.window_2:
            rec.encounter_count = 0
            return MemState.FORGOTTEN
        if rng.random() < _scale_p(cfg.p_mastered, capacity):
            rec.encounter_count = 3
            rec.last_encounter_pair = pair_id
            return MemState.MASTERED
        rec.last_encounter_pair = pair_id
        return MemState.PRACTICED

    elif state == MemState.MASTERED:
        # закрепление: можно усилить (без изменения состояния, просто обновить счётчик)
        rec.encounter_count += 1
        rec.last_encounter_pair = pair_id
        return MemState.MASTERED

    return state


def state_summary(result: SimResult) -> dict[str, int]:
    """Подсчитывает количество тем в каждом состоянии."""
    counts: dict[str, int] = {s.value: 0 for s in MemState}
    for rec in result.topic_states.values():
        counts[rec.state.value] += 1
    return counts


if __name__ == "__main__":
    from parse_curriculum import pairs_with_tags

    pairs = pairs_with_tags()
    rng = random.Random(42)
    result = simulate_student(pairs, rng=rng, student_id=1)

    print(f"Student capacity: {result.capacity:.3f}")
    print("State summary:", state_summary(result))
    print("\nTop mastered topics:")
    for tag, rec in sorted(result.topic_states.items(), key=lambda x: x[1].state.value):
        if rec.state == MemState.MASTERED:
            print(f"  {tag}")
