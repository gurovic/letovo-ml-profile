#!/usr/bin/env python3
"""Post-publish audit for Canvas course 6465: garbage pages, story headers, duplicates."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from canvas_api import canvas_delete, canvas_get, canvas_put, require_canvas_auth  # noqa: E402
from publish_canvas_lesson import (  # noqa: E402
    FEEDBACK_ITEM_TITLE,
    FEEDBACK_ITEM_TITLE_LEGACY,
    add_feedback_quiz_item,
    apply_module_item_order,
    clean_canvas_title,
    feedback_target_position,
    is_feedback_item,
    plan_module_feedback_layout,
    split_module_into_pair_blocks,
)
from publish_canvas_module_stories import (  # noqa: E402
    DEFAULT_SLUG_RE,
    LEGACY_PAGE_SLUGS,
    MODULES,
    STORY_ITEM_TITLE,
    TAGLINE_TITLE_DUP_RE,
    extract_story,
    load_module_ids,
    title_is_tagline_duplicate,
)

COURSE_ID = 6465
LATIN_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
FILE_NAME_ITEM_RE = re.compile(r"\.(ipynb|md|zip)$", re.I)
EXPECTED_STORY_POSITION = 1

KNOWN_ITEM_TITLES = frozenset(
    {
        STORY_ITEM_TITLE,
        "План урока (для преподавателя)",
        "Решения (для преподавателя)",
        "Ноутбук урока",
        "Домашнее задание",
        FEEDBACK_ITEM_TITLE,
        FEEDBACK_ITEM_TITLE_LEGACY,
        "Материалы артефакта",
        "Сдача артефакта text_stats",
    }
)


def run_post_publish_audit(
    course_id: int = COURSE_ID,
    *,
    module_dirs: list[str] | None = None,
    quiet: bool = False,
) -> bool:
    """Вызывается publish-скриптами после записи в Canvas. True = без error."""
    report = audit_course(course_id, module_dirs=module_dirs)
    if not quiet:
        print_report(report)
    return report.ok


@dataclass
class Finding:
    severity: str  # error | warn
    code: str
    message: str
    module: str | None = None


@dataclass
class AuditReport:
    course_id: int
    findings: list[Finding] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not any(f.severity == "error" for f in self.findings)

    def add(self, severity: str, code: str, message: str, module: str | None = None) -> None:
        self.findings.append(Finding(severity, code, message, module))

    def to_dict(self) -> dict:
        return {
            "course_id": self.course_id,
            "ok": self.ok,
            "errors": sum(1 for f in self.findings if f.severity == "error"),
            "warnings": sum(1 for f in self.findings if f.severity == "warn"),
            "findings": [
                {
                    "severity": f.severity,
                    "code": f.code,
                    "message": f.message,
                    "module": f.module,
                }
                for f in self.findings
            ],
        }


def load_story_map(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    rows = json.loads(path.read_text(encoding="utf-8"))
    return {row["module"]: row for row in rows if isinstance(row, dict) and "module" in row}


def fetch_wiki_index(course_id: int) -> dict[str, dict]:
    pages = canvas_get(f"courses/{course_id}/pages", paginate=True)
    if not isinstance(pages, list):
        return {}
    return {str(p.get("url") or ""): p for p in pages if p.get("url")}


def wiki_title_for_url(wiki_index: dict[str, dict], url: str) -> str | None:
    page = wiki_index.get(url)
    if not page:
        return None
    return str(page.get("title") or "")


def audit_orphan_story_wikis(
    report: AuditReport,
    wiki_index: dict[str, dict],
    *,
    expected_urls: set[str],
    expected_titles: set[str],
) -> None:
    for url, page in wiki_index.items():
        title = str(page.get("title") or "")
        if DEFAULT_SLUG_RE.match(url) or url in LEGACY_PAGE_SLUGS:
            report.add(
                "error",
                "orphan_story_slug",
                f"Мусорная wiki-страница сюжета: slug `{url}` (title: {title!r})",
            )
            continue
        if url in expected_urls:
            continue
        matched_tagline = next(
            (t for t in expected_titles if title_is_tagline_duplicate(title, t)),
            None,
        )
        if not matched_tagline:
            continue
        if TAGLINE_TITLE_DUP_RE.search(url) or url.endswith("-2"):
            report.add(
                "error",
                "duplicate_tagline_wiki",
                f"Дубликат wiki с tagline: `{url}` (title: {title!r})",
            )
        else:
            report.add(
                "warn",
                "extra_tagline_wiki",
                f"Лишняя wiki с tagline {matched_tagline!r}: `{url}`",
            )


def audit_module_story(
    report: AuditReport,
    *,
    course_id: int,
    module_dir: str,
    module_id: int,
    default_slug: str,
    wiki_index: dict[str, dict],
    story_map_row: dict | None,
) -> None:
    unit_path = ROOT / "modules" / module_dir / "UNIT.md"
    tagline, _story = extract_story(unit_path)
    items = canvas_get(f"courses/{course_id}/modules/{module_id}/items", paginate=True)
    if not isinstance(items, list):
        report.add("error", "module_items", f"Не удалось прочитать items модуля {module_id}", module_dir)
        return

    story_items = [it for it in items if str(it.get("title") or "") == STORY_ITEM_TITLE]
    if len(story_items) == 0:
        report.add(
            "error",
            "story_missing",
            f"Нет пункта «{STORY_ITEM_TITLE}» в модуле {module_id}",
            module_dir,
        )
        return
    if len(story_items) > 1:
        ids = [it.get("id") for it in story_items]
        report.add(
            "error",
            "story_duplicate_item",
            f"Дубликаты «{STORY_ITEM_TITLE}»: item ids {ids}",
            module_dir,
        )

    story_item = story_items[0]
    pos = int(story_item.get("position") or 0)
    if pos != EXPECTED_STORY_POSITION:
        report.add(
            "warn",
            "story_position",
            f"«{STORY_ITEM_TITLE}» на position {pos}, ожидалось {EXPECTED_STORY_POSITION}",
            module_dir,
        )

    page_url = str(story_item.get("page_url") or "")
    if not page_url:
        report.add("error", "story_no_page", "У «Сюжет модуля» пустой page_url", module_dir)
        return

    if page_url == default_slug or DEFAULT_SLUG_RE.match(page_url):
        report.add(
            "error",
            "story_latin_slug",
            f"Сюжет ссылается на латинский slug `{page_url}` вместо translit tagline",
            module_dir,
        )

    wiki_title = wiki_title_for_url(wiki_index, page_url)
    if wiki_title is None:
        report.add(
            "error",
            "story_page_missing",
            f"Wiki `{page_url}` не найдена (item {story_item.get('id')})",
            module_dir,
        )
        return

    if wiki_title == page_url or DEFAULT_SLUG_RE.match(wiki_title):
        report.add(
            "error",
            "story_latin_title",
            f"Заголовок wiki = slug ({wiki_title!r}); ожидался tagline: {tagline!r}",
            module_dir,
        )
    elif wiki_title != tagline:
        report.add(
            "warn",
            "story_title_mismatch",
            f"Заголовок wiki {wiki_title!r} ≠ tagline из UNIT {tagline!r}",
            module_dir,
        )

    body = str((wiki_index.get(page_url) or {}).get("body") or "")
    if wiki_index.get(page_url) is None:
        full = canvas_get(f"courses/{report.course_id}/pages/{page_url}")
        body = str(full.get("body") or "")
    text = re.sub(r"<[^>]+>", "", body).strip()
    if len(text) < 40:
        report.add(
            "error",
            "story_body_empty",
            f"Wiki `{page_url}` без текста сюжета (≈{len(text)} симв.)",
            module_dir,
        )

    if story_map_row:
        mapped_url = str(story_map_row.get("page") or "")
        mapped_title = str(story_map_row.get("page_title") or "")
        if mapped_url and mapped_url != page_url:
            report.add(
                "warn",
                "story_map_url",
                f"canvas_module_stories.json: page {mapped_url!r} ≠ live {page_url!r}",
                module_dir,
            )
        if mapped_title and mapped_title != wiki_title:
            report.add(
                "warn",
                "story_map_title",
                f"canvas_module_stories.json: title {mapped_title!r} ≠ live {wiki_title!r}",
                module_dir,
            )

    # Пункты-слуги: title совпадает с latin slug (типичный мусор после старых публикаций)
    for it in items[:8]:
        title = str(it.get("title") or "")
        purl = str(it.get("page_url") or "")
        if it.get("type") == "Page" and title == purl and LATIN_SLUG_RE.match(title):
            if title != page_url:
                report.add(
                    "error",
                    "slug_titled_item",
                    f"Пункт модуля назван slug'ом: {title!r} (item {it.get('id')}, pos {it.get('position')})",
                    module_dir,
                )


def audit_module_item_titles(
    report: AuditReport,
    *,
    course_id: int,
    module_dir: str,
    module_id: int,
) -> None:
    items = canvas_get(f"courses/{course_id}/modules/{module_id}/items", paginate=True)
    if not isinstance(items, list):
        return
    for it in items:
        title = str(it.get("title") or "")
        itype = str(it.get("type") or "")
        if FILE_NAME_ITEM_RE.search(title):
            report.add(
                "error",
                "filename_item_title",
                f"Название элемента = имя файла: {title!r} ({itype}, item {it.get('id')})",
                module_dir,
            )
        if itype == "ExternalUrl" and "homework.ipynb" in title.lower():
            report.add(
                "error",
                "homework_external_url",
                f"ExternalUrl на homework (должен быть Assignment): {title!r}",
                module_dir,
            )
        if title.rstrip().endswith("|"):
            report.add(
                "error",
                "title_trailing_pipe",
                f"Заголовок элемента оканчивается на «|»: {title!r} ({itype}, item {it.get('id')})",
                module_dir,
            )
        if title.startswith("para-") and itype == "Page":
            report.add(
                "warn",
                "plan_slug_title",
                f"План назван slug'ом para-*: {title!r} (ожидал «План урока (для преподавателя)»)",
                module_dir,
            )


def audit_course(
    course_id: int = COURSE_ID,
    *,
    module_dirs: list[str] | None = None,
    map_path: Path | None = None,
    story_map_path: Path | None = None,
) -> AuditReport:
    report = AuditReport(course_id=course_id)
    map_path = map_path or ROOT / "modules" / "canvas_publish_draft4.json"
    story_map_path = story_map_path or map_path.parent / "canvas_module_stories.json"
    module_ids = load_module_ids(map_path)
    story_map = load_story_map(story_map_path)
    wiki_index = fetch_wiki_index(course_id)

    modules = MODULES
    if module_dirs:
        allowed = set(module_dirs)
        modules = [m for m in MODULES if m[0] in allowed]
        if not modules:
            report.add("error", "unknown_module", f"Неизвестные module_dirs: {module_dirs}")
            return report

    expected_urls: set[str] = set()
    expected_titles: set[str] = set()
    for module_dir, _num, default_slug in modules:
        mid = module_ids.get(module_dir)
        if not mid:
            report.add("error", "no_module_id", f"Нет module_id для {module_dir}", module_dir)
            continue
        tagline, _ = extract_story(ROOT / "modules" / module_dir / "UNIT.md")
        expected_titles.add(tagline)
        row = story_map.get(module_dir)
        if row and row.get("page"):
            expected_urls.add(str(row["page"]))
        audit_module_story(
            report,
            course_id=course_id,
            module_dir=module_dir,
            module_id=mid,
            default_slug=default_slug,
            wiki_index=wiki_index,
            story_map_row=row,
        )
        audit_module_item_titles(report, course_id=course_id, module_dir=module_dir, module_id=mid)
        story_items = canvas_get(f"courses/{course_id}/modules/{mid}/items", paginate=True)
        for it in story_items if isinstance(story_items, list) else []:
            if str(it.get("title") or "") == STORY_ITEM_TITLE and it.get("page_url"):
                expected_urls.add(str(it["page_url"]))

    audit_orphan_story_wikis(
        report,
        wiki_index,
        expected_urls=expected_urls,
        expected_titles=expected_titles,
    )
    return report


def fix_trailing_pipe_titles(course_id: int) -> list[dict]:
    """Исправить module items и wiki, у которых title заканчивается на |."""
    fixes: list[dict] = []
    modules = canvas_get(f"courses/{course_id}/modules", paginate=True)
    if isinstance(modules, list):
        for mod in modules:
            mid = int(mod["id"])
            items = canvas_get(f"courses/{course_id}/modules/{mid}/items", paginate=True)
            if not isinstance(items, list):
                continue
            for item in items:
                title = str(item.get("title") or "")
                cleaned = clean_canvas_title(title)
                if cleaned != title:
                    canvas_put(
                        f"courses/{course_id}/modules/{mid}/items/{item['id']}",
                        {"module_item[title]": cleaned},
                    )
                    fixes.append(
                        {
                            "kind": "module_item",
                            "module_id": mid,
                            "item_id": item.get("id"),
                            "before": title,
                            "after": cleaned,
                        }
                    )
    pages = canvas_get(f"courses/{course_id}/pages", paginate=True)
    if isinstance(pages, list):
        for page in pages:
            url = str(page.get("url") or "")
            title = str(page.get("title") or "")
            cleaned = clean_canvas_title(title)
            if url and cleaned != title:
                canvas_put(
                    f"courses/{course_id}/pages/{url}",
                    {"wiki_page[title]": cleaned},
                )
                fixes.append(
                    {
                        "kind": "wiki",
                        "url": url,
                        "before": title,
                        "after": cleaned,
                    }
                )
    return fixes


def _try_unpublish_item(course_id: int, module_id: int, item: dict) -> str:
    """true | hidden | skipped. Canvas File items sometimes refuse unpublish (403)."""
    item_id = item.get("id")
    title = str(item.get("title") or "")
    if title == STORY_ITEM_TITLE:
        canvas_put(
            f"courses/{course_id}/modules/{module_id}/items/{item_id}",
            {"module_item[published]": "true"},
        )
        return "visible"
    try:
        canvas_put(
            f"courses/{course_id}/modules/{module_id}/items/{item_id}",
            {"module_item[published]": "false"},
        )
        return "hidden"
    except SystemExit:
        # File / locked content: drop module item so students do not see it
        try:
            canvas_delete(f"courses/{course_id}/modules/{module_id}/items/{item_id}")
            return "removed"
        except SystemExit:
            print(
                f"WARN: could not hide item {item_id} ({item.get('type')}: {title!r})",
                file=sys.stderr,
            )
            return "skipped"


def hide_all_except_stories(
    course_id: int,
    *,
    map_path: Path,
) -> dict[str, int]:
    """Скрыть все пункты модулей, кроме «Сюжет модуля»; модули оставить опубликованными."""
    module_ids = load_module_ids(map_path)
    stats = {
        "modules": 0,
        "stories_visible": 0,
        "items_hidden": 0,
        "items_removed": 0,
        "items_skipped": 0,
        "assignments_hidden": 0,
    }
    for mid in module_ids.values():
        canvas_put(
            f"courses/{course_id}/modules/{mid}",
            {"module[published]": "true"},
        )
        stats["modules"] += 1
        items = canvas_get(f"courses/{course_id}/modules/{mid}/items", paginate=True)
        if not isinstance(items, list):
            continue
        for item in items:
            result = _try_unpublish_item(course_id, mid, item)
            if result == "visible":
                stats["stories_visible"] += 1
            elif result == "hidden":
                stats["items_hidden"] += 1
            elif result == "removed":
                stats["items_removed"] += 1
            else:
                stats["items_skipped"] += 1
    assignments = canvas_get(f"courses/{course_id}/assignments", paginate=True)
    if isinstance(assignments, list):
        for assignment in assignments:
            aid = assignment.get("id")
            if not aid:
                continue
            try:
                canvas_put(
                    f"courses/{course_id}/assignments/{aid}",
                    {"assignment[published]": "false"},
                )
                stats["assignments_hidden"] += 1
            except SystemExit:
                print(f"WARN: could not hide assignment {aid}", file=sys.stderr)
    return stats


def _delete_feedback_module_item(
    course_id: int,
    module_id: int,
    item: dict,
    *,
    delete_quiz: bool,
) -> None:
    item_id = item.get("id")
    quiz_id = item.get("content_id")
    if item_id:
        canvas_delete(f"courses/{course_id}/modules/{module_id}/items/{item_id}")
    if delete_quiz and quiz_id:
        try:
            canvas_delete(f"courses/{course_id}/quizzes/{quiz_id}")
        except SystemExit:
            print(f"WARN: could not delete quiz {quiz_id}", file=sys.stderr)


def _sync_feedback_item(
    course_id: int,
    module_id: int,
    item: dict,
    *,
    target_pos: int,
) -> tuple[bool, bool, bool]:
    """(moved, renamed, hidden)."""
    moved = renamed = hidden = False
    updates: dict[str, str] = {}
    if int(item.get("position") or 0) != target_pos:
        updates["module_item[position]"] = str(target_pos)
        moved = True
    if str(item.get("title") or "") != FEEDBACK_ITEM_TITLE:
        updates["module_item[title]"] = FEEDBACK_ITEM_TITLE
        renamed = True
    if item.get("published"):
        updates["module_item[published]"] = "false"
        hidden = True
    if updates:
        canvas_put(
            f"courses/{course_id}/modules/{module_id}/items/{item['id']}",
            updates,
        )
    quiz_id = item.get("content_id")
    if quiz_id:
        canvas_put(
            f"courses/{course_id}/quizzes/{quiz_id}",
            {
                "quiz[title]": FEEDBACK_ITEM_TITLE,
                "quiz[published]": "false",
            },
        )
    return moved, renamed, hidden


def ensure_hidden_feedback_quizzes(
    course_id: int,
    *,
    map_path: Path,
) -> dict[str, int]:
    """В каждом блоке пары — ровно один скрытый Quiz в самом конце блока."""
    from publish_canvas_module_stories import load_module_ids

    module_ids = load_module_ids(map_path)
    stats = {
        "modules": 0,
        "pairs": 0,
        "created": 0,
        "removed": 0,
        "moved": 0,
        "renamed": 0,
        "hidden": 0,
    }
    for mid in module_ids.values():
        stats["modules"] += 1
        items = canvas_get(f"courses/{course_id}/modules/{mid}/items", paginate=True)
        if not isinstance(items, list):
            continue

        desired, to_delete, missing_headers = plan_module_feedback_layout(items)
        blocks = split_module_into_pair_blocks(items)
        stats["pairs"] += len(blocks)

        for dup in to_delete:
            _delete_feedback_module_item(course_id, mid, dup, delete_quiz=True)
            stats["removed"] += 1

        if to_delete:
            items = canvas_get(f"courses/{course_id}/modules/{mid}/items", paginate=True)
            if not isinstance(items, list):
                continue
            desired, _, missing_headers = plan_module_feedback_layout(items)

        stats["moved"] += apply_module_item_order(course_id, mid, desired)

        if missing_headers:
            items = canvas_get(f"courses/{course_id}/modules/{mid}/items", paginate=True)
            if isinstance(items, list):
                blocks = split_module_into_pair_blocks(items)
                for header, block in blocks:
                    if str(header.get("title") or "") not in missing_headers:
                        continue
                    target_pos = feedback_target_position(block)
                    add_feedback_quiz_item(course_id, mid, position=target_pos)
                    stats["created"] += 1

        items = canvas_get(f"courses/{course_id}/modules/{mid}/items", paginate=True)
        if not isinstance(items, list):
            continue
        for it in items:
            if not is_feedback_item(it):
                continue
            _, renamed, hidden = _sync_feedback_item(
                course_id,
                mid,
                it,
                target_pos=int(it.get("position") or 0),
            )
            stats["renamed"] += int(renamed)
            stats["hidden"] += int(hidden)

    return stats


def print_report(report: AuditReport) -> None:
    data = report.to_dict()
    if report.ok and not data["warnings"]:
        print(f"Canvas controller: OK (course {report.course_id})")
        return
    print(f"Canvas controller: {'FAIL' if not report.ok else 'OK with warnings'} (course {report.course_id})")
    for f in report.findings:
        prefix = "ERROR" if f.severity == "error" else "WARN"
        mod = f" [{f.module}]" if f.module else ""
        print(f"  {prefix} {f.code}{mod}: {f.message}")
    print(f"  errors={data['errors']} warnings={data['warnings']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Canvas course after publish")
    parser.add_argument("--course-id", type=int, default=COURSE_ID)
    parser.add_argument(
        "--module",
        action="append",
        dest="modules",
        help="Limit to module dir, e.g. 08_01_functions_recursion (repeatable)",
    )
    parser.add_argument(
        "--map",
        type=Path,
        default=ROOT / "modules" / "canvas_publish_draft4.json",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON report")
    parser.add_argument("--quiet", action="store_true", help="Only exit code; no text unless errors")
    parser.add_argument(
        "--fix-titles",
        action="store_true",
        help="Remove trailing | from module item and wiki titles, then audit",
    )
    parser.add_argument(
        "--stories-only",
        action="store_true",
        help="Hide all module items except «Сюжет модуля» (modules stay visible)",
    )
    parser.add_argument(
        "--add-feedback",
        action="store_true",
        help="Один скрытый опрос «Опрос перед следующей парой» в конце каждой пары",
    )
    args = parser.parse_args()
    require_canvas_auth()
    if args.fix_titles:
        fixes = fix_trailing_pipe_titles(args.course_id)
        if fixes:
            print(f"Fixed {len(fixes)} titles:")
            for row in fixes:
                print(f"  {row['kind']}: {row['before']!r} → {row['after']!r}")
        else:
            print("No titles with trailing | found")
    if args.stories_only:
        stats = hide_all_except_stories(args.course_id, map_path=args.map)
        print(
            f"Stories-only mode: modules={stats['modules']} "
            f"stories_visible={stats['stories_visible']} "
            f"items_hidden={stats['items_hidden']} "
            f"items_removed={stats['items_removed']} "
            f"items_skipped={stats['items_skipped']} "
            f"assignments_hidden={stats['assignments_hidden']}"
        )
    if args.add_feedback:
        stats = ensure_hidden_feedback_quizzes(args.course_id, map_path=args.map)
        print(
            f"Feedback quizzes: pairs={stats['pairs']} created={stats['created']} "
            f"removed={stats['removed']} moved={stats['moved']} "
            f"renamed={stats['renamed']} hidden={stats['hidden']} "
            f"modules={stats['modules']}"
        )
    if args.stories_only or args.fix_titles or args.add_feedback:
        sys.exit(0)
    report = audit_course(
        args.course_id,
        module_dirs=args.modules,
        map_path=args.map,
    )
    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    elif not args.quiet:
        print_report(report)
    sys.exit(0 if report.ok else 1)


if __name__ == "__main__":
    main()
