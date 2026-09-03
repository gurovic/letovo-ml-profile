#!/usr/bin/env python3
"""Wipe and republish grade-8 Canvas course (6465) for KTP Draft 4.

Lesson notebooks (Ноутбук урока) are unpublished (hidden from students).
Plan + solutions stay unpublished. Homework assignments stay published.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from canvas_api import (  # noqa: E402
    canvas_delete,
    canvas_get,
    canvas_post,
    canvas_put,
    require_canvas_auth,
)
from publish_canvas_lesson import (  # noqa: E402
    ARTIFACT_PROJECT_ITEM_TITLE,
    ARTIFACT_STARTER_CODE_ITEM_TITLE,
    ARTIFACT_STARTER_README_ITEM_TITLE,
    ARTIFACT_SUBMIT_TITLE,
    HOMEWORK_ITEM_TITLE,
    LESSON_ITEM_TITLE,
    PLAN_ITEM_TITLE,
    SOLUTIONS_ITEM_TITLE,
    PairPreset,
    add_artifact_extras,
    add_artifact_submit_item,
    add_feedback_quiz_item,
    add_homework_assignment_item,
    add_module_item,
    publish_orientation_pair,
    upsert_lesson_page,
)

COURSE_ID = 6465
GIST_USER = "gurovic"

MODULES: list[tuple[str, str, int, int]] = [
    ("08_01_functions_recursion", "Модуль 1. Оценка недвижимости: функции и inference pipeline", 1, 8),
    ("08_02_carsharing_pandas_lr", "Модуль 2. Краткосрочная аренда: pandas и линейная регрессия", 9, 16),
    ("08_03_titanic_eda", "Модуль 3. Расследование на «Титанике»: EDA и статистика", 17, 24),
    ("08_04_mnist_knn", "Модуль 4. Распознавание цифр: вероятность и kNN", 25, 30),
    ("08_05_shop_feature_engineering", "Модуль 5. Интернет-магазин: Feature Engineering и lambda", 31, 37),
    ("08_06_ab_startup", "Модуль 6. A/B-тест стартапа и статистический вывод", 38, 43),
    ("08_07_bank_arrays_search", "Модуль 7. Массивы: поиск и сортировка", 44, 47),
    ("08_08_logistics_clustering", "Модуль 8. Структуры данных, кластеризация и аномалии", 48, 50),
    ("08_10_churn_logreg", "Модуль 9. Отток клиентов: логистическая регрессия", 51, 54),
    ("08_11_virtual_polygon", "Модуль 10. Виртуальный полигон: производная и градиентный спуск", 55, 58),
    ("08_09_courier_dp", "Модуль 11 (доп.). Динамическое программирование и игры", 59, 63),
]


@dataclass
class LessonSlot:
    pair: int
    module_dir: str
    folder: str
    title: str
    orientation: bool = False
    artifact: bool = False

    @property
    def path(self) -> Path:
        return ROOT / "modules" / self.module_dir / "lessons" / self.folder

    @property
    def page_url(self) -> str:
        return f"para-{self.pair}-plan-uroka-dlia-priepodavatielia"

    @property
    def page_title(self) -> str:
        return self.page_url

    @property
    def subheader(self) -> str:
        short = self.title
        if len(short) > 90:
            short = short[:87] + "…"
        return f"Пара {self.pair}. {short}"


def parse_lesson_meta(lesson_md: Path) -> tuple[int | None, str]:
    text = lesson_md.read_text(encoding="utf-8")
    pair = None
    m = re.search(r"Пара КТП\s*\|\s*\*?\*?(\d+)\*?\*?", text)
    if m:
        pair = int(m.group(1))
    title = lesson_md.parent.name
    m = re.search(r"Название урока\s*\|\s*(.+?)\s*\|", text)
    if m:
        title = m.group(1).strip()
    return pair, title


def active_lesson_folders(module_dir: str) -> list[Path]:
    lessons = ROOT / "modules" / module_dir / "lessons"
    out = []
    for d in sorted(lessons.iterdir()):
        if not d.is_dir() or d.name.startswith("_"):
            continue
        if (d / "LESSON.md").exists():
            out.append(d)
    return out


def build_slots() -> list[LessonSlot]:
    slots: list[LessonSlot] = []
    for module_dir, _name, start, end in MODULES:
        folders = active_lesson_folders(module_dir)
        expected = end - start + 1
        if len(folders) != expected:
            raise SystemExit(
                f"{module_dir}: expected {expected} lesson folders for pairs {start}-{end}, got {len(folders)}: {[f.name for f in folders]}"
            )
        for i, folder in enumerate(folders):
            pair = start + i
            parsed_pair, title = parse_lesson_meta(folder / "LESSON.md")
            if parsed_pair is not None and parsed_pair != pair:
                print(
                    f"WARN {module_dir}/{folder.name}: LESSON pair={parsed_pair}, catalog={pair}",
                    file=sys.stderr,
                )
            orientation = pair == 1 and module_dir.startswith("08_01")
            artifact = folder.name.startswith("08_artifact") or (
                module_dir.startswith("08_01") and pair == 8
            )
            slots.append(
                LessonSlot(
                    pair=pair,
                    module_dir=module_dir,
                    folder=folder.name,
                    title=title,
                    orientation=orientation,
                    artifact=artifact,
                )
            )
    return slots


def wipe_course(course_id: int) -> None:
    modules = canvas_get(f"courses/{course_id}/modules", paginate=True)
    for mod in modules:
        mid = mod["id"]
        print(f"DELETE module {mid} {mod.get('name')}")
        canvas_delete(f"courses/{course_id}/modules/{mid}")
        time.sleep(0.15)

    assignments = canvas_get(f"courses/{course_id}/assignments", paginate=True)
    for a in assignments:
        aid = a["id"]
        print(f"DELETE assignment {aid} {a.get('name')}")
        canvas_delete(f"courses/{course_id}/assignments/{aid}")
        time.sleep(0.1)


def ensure_module(course_id: int, name: str, position: int) -> int:
    modules = canvas_get(f"courses/{course_id}/modules", paginate=True)
    for mod in modules:
        if mod.get("name") == name:
            canvas_put(
                f"courses/{course_id}/modules/{mod['id']}",
                {"module[published]": "true", "module[position]": str(position)},
            )
            return int(mod["id"])
    created = canvas_post(
        f"courses/{course_id}/modules",
        {
            "module[name]": name,
            "module[published]": "true",
            "module[position]": str(position),
        },
    )
    return int(created["id"])


def load_gist_map(module_dir: str) -> dict[int, str]:
    path = ROOT / "modules" / module_dir / "canvas_gist_map.json"
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    out: dict[int, str] = {}
    for k, v in raw.items():
        if isinstance(v, dict) and v.get("gist_id"):
            out[int(k)] = v["gist_id"]
        elif isinstance(v, str):
            out[int(k)] = v
    return out


def save_gist_map(module_dir: str, mapping: dict[int, str]) -> None:
    path = ROOT / "modules" / module_dir / "canvas_gist_map.json"
    payload = {
        str(k): {"gist_id": v, "gist_url": f"https://gist.github.com/{GIST_USER}/{v}"}
        for k, v in sorted(mapping.items())
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def create_gist(lesson_dir: Path) -> str:
    files = [
        lesson_dir / name
        for name in ("lesson.ipynb", "homework.ipynb", "solutions.ipynb")
        if (lesson_dir / name).exists()
    ]
    # include small csv helpers if present (common in lessons)
    for name in sorted(lesson_dir.glob("*.csv")):
        if name.stat().st_size < 2_000_000:
            files.append(name)
    if not files:
        raise SystemExit(f"No notebooks in {lesson_dir}")
    cmd = [
        "gh",
        "gist",
        "create",
        *[str(f) for f in files],
        "--public",
        "--desc",
        f"8ML {lesson_dir.parent.parent.name}/{lesson_dir.name}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise SystemExit(result.stderr or result.stdout or "gist create failed")
    gist_url = result.stdout.strip().splitlines()[-1]
    return gist_url.rstrip("/").split("/")[-1]


def colab(gist_id: str, filename: str) -> str:
    return f"https://colab.research.google.com/gist/{GIST_USER}/{gist_id}/{filename}"


def ensure_gists(slots: list[LessonSlot], *, force_new: bool = False) -> dict[int, str]:
    by_module: dict[str, dict[int, str]] = {}
    all_map: dict[int, str] = {}
    for slot in slots:
        if slot.orientation or slot.artifact:
            continue
        if not (slot.path / "lesson.ipynb").exists():
            print(f"SKIP gist (no lesson.ipynb): pair {slot.pair} {slot.path}")
            continue
        mmap = by_module.setdefault(slot.module_dir, load_gist_map(slot.module_dir))
        if not force_new and slot.pair in mmap:
            all_map[slot.pair] = mmap[slot.pair]
            continue
        print(f"CREATE gist pair {slot.pair} {slot.folder} …")
        gist_id = create_gist(slot.path)
        mmap[slot.pair] = gist_id
        all_map[slot.pair] = gist_id
        save_gist_map(slot.module_dir, mmap)
        time.sleep(0.4)
    return all_map


def publish_standard_pair(
    course_id: int,
    module_id: int,
    slot: LessonSlot,
    gist_id: str,
) -> dict:
    lesson_url = colab(gist_id, "lesson.ipynb")
    homework_url = (
        colab(gist_id, "homework.ipynb")
        if (slot.path / "homework.ipynb").exists()
        else lesson_url
    )
    solutions_url = (
        colab(gist_id, "solutions.ipynb")
        if (slot.path / "solutions.ipynb").exists()
        else None
    )

    page = upsert_lesson_page(
        course_id,
        title=slot.page_title,
        markdown_path=slot.path / "LESSON.md",
        page_url=slot.page_url,
        lesson_colab_url=lesson_url,
        homework_colab_url=homework_url,
    )
    resolved_page_url = page.get("url", slot.page_url)

    payloads = [
        {
            "module_item[title]": slot.subheader,
            "module_item[type]": "SubHeader",
            "module_item[indent]": "0",
        },
        {
            "module_item[title]": PLAN_ITEM_TITLE,
            "module_item[type]": "Page",
            "module_item[page_url]": resolved_page_url,
            "module_item[indent]": "1",
            "module_item[published]": "false",
        },
    ]
    if solutions_url:
        payloads.append(
            {
                "module_item[title]": SOLUTIONS_ITEM_TITLE,
                "module_item[type]": "ExternalUrl",
                "module_item[external_url]": solutions_url,
                "module_item[indent]": "1",
                "module_item[published]": "false",
                "module_item[new_tab]": "true",
            }
        )
    payloads.append(
        {
            "module_item[title]": LESSON_ITEM_TITLE,
            "module_item[type]": "ExternalUrl",
            "module_item[external_url]": lesson_url,
            "module_item[indent]": "1",
            "module_item[published]": "false",  # hidden from students
            "module_item[new_tab]": "true",
        }
    )

    items = [add_module_item(course_id, module_id, p) for p in payloads]
    # Force unpublished (Canvas sometimes ignores on create)
    for item in items:
        if item.get("title") == LESSON_ITEM_TITLE:
            canvas_put(
                f"courses/{course_id}/modules/{module_id}/items/{item['id']}",
                {"module_item[published]": "false"},
            )

    hw = None
    if (slot.path / "homework.ipynb").exists():
        hw = add_homework_assignment_item(
            course_id,
            module_id,
            homework_colab_url=homework_url,
        )
    feedback = add_feedback_quiz_item(course_id, module_id)

    return {
        "pair": slot.pair,
        "page": resolved_page_url,
        "items": [i.get("id") for i in items],
        "homework": (hw or {}).get("assignment_id"),
        "feedback": (feedback or {}).get("quiz_id"),
        "gist_id": gist_id,
    }


def publish_artifact_pair8(course_id: int, module_id: int, slot: LessonSlot) -> dict:
    preset = PairPreset(
        subheader=slot.subheader,
        page_title=slot.page_title,
        page_url=slot.page_url,
        lesson_dir=slot.folder,
        artifact=True,
        skip_homework=True,
    )
    # PairPreset.lesson_md is hardcoded to 08_01 lessons root — monkey via path check
    # Use orientation publish with local markdown path override through upsert directly.
    page = upsert_lesson_page(
        course_id,
        title=slot.page_title,
        markdown_path=slot.path / "LESSON.md",
        page_url=slot.page_url,
        lesson_colab_url="",
        homework_colab_url="",
    )
    resolved = page.get("url", slot.page_url)
    add_module_item(
        course_id,
        module_id,
        {
            "module_item[title]": slot.subheader,
            "module_item[type]": "SubHeader",
            "module_item[indent]": "0",
        },
    )
    add_module_item(
        course_id,
        module_id,
        {
            "module_item[title]": PLAN_ITEM_TITLE,
            "module_item[type]": "Page",
            "module_item[page_url]": resolved,
            "module_item[indent]": "1",
            "module_item[published]": "false",
        },
    )
    # Reuse artifact extras: docs as for former pair 9 + submit as former pair 10
    extras = add_artifact_extras(course_id, module_id, 9, preset)
    submit = add_artifact_submit_item(course_id, module_id)
    feedback = add_feedback_quiz_item(course_id, module_id)
    return {
        "pair": 8,
        "page": resolved,
        "artifact": True,
        "extras": extras,
        "submit": submit,
        "feedback": feedback,
    }


def publish_all(course_id: int, slots: list[LessonSlot], gist_map: dict[int, str]) -> dict:
    module_ids: dict[str, int] = {}
    for pos, (module_dir, name, _s, _e) in enumerate(MODULES, start=1):
        mid = ensure_module(course_id, name, pos)
        module_ids[module_dir] = mid
        print(f"MODULE {pos} id={mid} {name}")

    results = {"modules": module_ids, "pairs": {}}
    for slot in slots:
        mid = module_ids[slot.module_dir]
        print(f"PUBLISH pair {slot.pair}: {slot.folder}")
        if slot.orientation:
            preset = PairPreset(
                subheader=slot.subheader,
                page_title=slot.page_title,
                page_url=slot.page_url,
                lesson_dir=slot.folder,
                orientation=True,
                skip_homework=True,
            )
            # orientation uses MODULE_ROOT hardcoded — call upsert + items manually
            page = upsert_lesson_page(
                course_id,
                title=slot.page_title,
                markdown_path=slot.path / "LESSON.md",
                page_url=slot.page_url,
                lesson_colab_url="",
                homework_colab_url="",
            )
            resolved = page.get("url", slot.page_url)
            add_module_item(
                course_id,
                mid,
                {
                    "module_item[title]": slot.subheader,
                    "module_item[type]": "SubHeader",
                    "module_item[indent]": "0",
                },
            )
            add_module_item(
                course_id,
                mid,
                {
                    "module_item[title]": PLAN_ITEM_TITLE,
                    "module_item[type]": "Page",
                    "module_item[page_url]": resolved,
                    "module_item[indent]": "1",
                    "module_item[published]": "false",
                },
            )
            results["pairs"][slot.pair] = {
                "orientation": True,
                "page": resolved,
                "feedback": add_feedback_quiz_item(course_id, mid),
            }
        elif slot.artifact:
            results["pairs"][slot.pair] = publish_artifact_pair8(course_id, mid, slot)
        else:
            gist_id = gist_map.get(slot.pair)
            if not gist_id:
                raise SystemExit(f"Missing gist for pair {slot.pair}")
            results["pairs"][slot.pair] = publish_standard_pair(
                course_id, mid, slot, gist_id
            )
        time.sleep(0.2)
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wipe", action="store_true")
    parser.add_argument("--gists", action="store_true", help="Ensure gists (create missing)")
    parser.add_argument("--force-new-gists", action="store_true")
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--all", action="store_true", help="wipe + gists + publish")
    parser.add_argument("--course-id", type=int, default=COURSE_ID)
    args = parser.parse_args()

    if args.all:
        args.wipe = args.gists = args.publish = True

    if not (args.wipe or args.gists or args.publish):
        parser.error("Pass --wipe / --gists / --publish or --all")

    require_canvas_auth()
    slots = build_slots()
    print(f"Slots: {len(slots)} (expect 63)")

    if args.wipe:
        wipe_course(args.course_id)

    gist_map: dict[int, str] = {}
    if args.gists or args.publish:
        gist_map = ensure_gists(slots, force_new=args.force_new_gists)
        # fill from existing maps even if --publish without --gists recreating
        if not args.gists:
            for slot in slots:
                if slot.orientation or slot.artifact:
                    continue
                mmap = load_gist_map(slot.module_dir)
                if slot.pair in mmap:
                    gist_map[slot.pair] = mmap[slot.pair]

    if args.publish:
        # ensure all needed gists present
        missing = [
            s.pair
            for s in slots
            if not s.orientation and not s.artifact and s.pair not in gist_map
        ]
        if missing:
            print(f"Creating missing gists for pairs: {missing}")
            gist_map.update(ensure_gists([s for s in slots if s.pair in missing], force_new=True))
        out = publish_all(args.course_id, slots, gist_map)
        out_path = ROOT / "modules" / "canvas_publish_draft4.json"
        out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
