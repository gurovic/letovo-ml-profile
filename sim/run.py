"""
run.py — точка входа CLI для симуляции.

Использование:
    python sim/run.py                          # 100 студентов, 8 класс
    python sim/run.py --students 20            # 20 студентов
    python sim/run.py --students 1 --verbose   # один студент с полным логом
    python sim/run.py --seed 42                # воспроизводимый запуск
    python sim/run.py --out sim/results/run1.md  # сохранить отчёт

Результат выводится в stdout и опционально сохраняется в файл.
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

# добавляем sim/ в путь поиска модулей
sys.path.insert(0, str(Path(__file__).parent))

from evaluator import EvalConfig, format_aggregate_report, run_evaluation
from examiner import examine, format_report
from parse_curriculum import pairs_with_tags
from student import StudentConfig, simulate_student, state_summary


def cmd_run(args: argparse.Namespace) -> None:
    if args.students == 1 or args.verbose:
        _run_single(args)
    else:
        _run_batch(args)


def _run_single(args: argparse.Namespace) -> None:
    pairs = pairs_with_tags()
    seed = args.seed if args.seed else random.randint(1, 10**9)
    rng = random.Random(seed)

    cfg = StudentConfig()
    result = simulate_student(pairs, rng=rng, config=cfg, student_id=1)
    report = examine(result)

    output_lines = [format_report(report)]

    if args.verbose:
        output_lines.append("\n## Детальный лог пар\n")
        for entry in result.pair_log:
            if entry["events"]:
                evts = "; ".join(
                    f"{e['tag']}: {e['old'].value}→{e['new'].value}"
                    for e in entry["events"]
                )
                output_lines.append(f"Пара {entry['pair_id']} [{entry['module']}]: {evts}")

        output_lines.append(f"\n**Итог по состояниям:** {state_summary(result)}")

    output = "\n".join(output_lines)
    _output(output, args)


def _run_batch(args: argparse.Namespace) -> None:
    cfg = EvalConfig(
        n_students=args.students,
        seed=args.seed if args.seed else 0,
        grade=args.grade,
    )
    agg = run_evaluation(cfg)
    output = format_aggregate_report(agg)
    _output(output, args)


def _output(text: str, args: argparse.Namespace) -> None:
    print(text)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        print(f"\n--- Отчёт сохранён: {out_path} ---", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Симуляция студентов профиля ML и оценка программы."
    )
    parser.add_argument(
        "--students", type=int, default=100,
        help="Количество студентов для симуляции (default: 100)"
    )
    parser.add_argument(
        "--grade", type=int, default=8,
        help="Класс (default: 8)"
    )
    parser.add_argument(
        "--seed", type=int, default=0,
        help="Random seed (default: 0 = случайный)"
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Подробный лог по парам (только для --students 1)"
    )
    parser.add_argument(
        "--out", type=str, default=None,
        help="Путь для сохранения отчёта (например, sim/results/run.md)"
    )
    args = parser.parse_args()
    cmd_run(args)


if __name__ == "__main__":
    main()
