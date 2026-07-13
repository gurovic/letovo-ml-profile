#!/usr/bin/env python3
"""Canvas LMS API client for canvas.letovo.ru. Reads secrets from .env only."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"


def load_env(path: Path = ENV_PATH) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def canvas_config() -> tuple[str, str]:
    env = load_env()
    token = env.get("CANVAS_ACCESS_TOKEN") or os.environ.get("CANVAS_ACCESS_TOKEN")
    api_url = (
        env.get("CANVAS_API_URL")
        or os.environ.get("CANVAS_API_URL")
        or "https://canvas.letovo.ru/api/v1"
    ).rstrip("/")
    if not token:
        print(
            "Error: CANVAS_ACCESS_TOKEN not found. Copy .env.example to .env and set token.",
            file=sys.stderr,
        )
        sys.exit(1)
    return api_url, token


def canvas_get(path: str, params: dict | None = None, *, paginate: bool = False) -> object:
    api_url, token = canvas_config()
    if path.startswith("http"):
        url = path
    else:
        url = f"{api_url}/{path.lstrip('/')}"

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    all_items: list = []

    while url:
        req_url = url
        if params and not path.startswith("http"):
            sep = "&" if "?" in req_url else "?"
            req_url = req_url + sep + urllib.parse.urlencode(params)
            params = None

        req = urllib.request.Request(req_url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = resp.read().decode("utf-8")
                link = resp.headers.get("Link", "")
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            print(f"HTTP {e.code}: {detail}", file=sys.stderr)
            sys.exit(1)

        data = json.loads(body) if body else None

        if paginate and isinstance(data, list):
            all_items.extend(data)
            url = _next_link(link)
            continue

        if paginate and isinstance(data, list):
            return all_items
        return data

    return all_items if paginate else None


def _next_link(link_header: str) -> str | None:
    for part in link_header.split(","):
        if 'rel="next"' in part or "rel=next" in part:
            m = re.search(r"<([^>]+)>", part)
            if m:
                return m.group(1)
    return None


def cmd_self(_: argparse.Namespace) -> None:
    print(json.dumps(canvas_get("users/self"), ensure_ascii=False, indent=2))


def cmd_courses(args: argparse.Namespace) -> None:
    params = {"per_page": args.per_page}
    if args.search:
        params["search_term"] = args.search
    if args.all:
        params["include[]"] = "total_students"
    data = canvas_get("courses", {**params, "enrollment_state": "active"}, paginate=True)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    for c in data:
        print(f"{c.get('id')}\t{c.get('course_code', '')}\t{c.get('name', '')}")


def cmd_course(args: argparse.Namespace) -> None:
    print(json.dumps(canvas_get(f"courses/{args.course_id}"), ensure_ascii=False, indent=2))


def cmd_modules(args: argparse.Namespace) -> None:
    data = canvas_get(f"courses/{args.course_id}/modules", paginate=True)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    for m in data:
        print(f"{m.get('id')}\t{m.get('position')}\t{m.get('name')}\tstate={m.get('state')}")


def cmd_module_items(args: argparse.Namespace) -> None:
    path = f"courses/{args.course_id}/modules/{args.module_id}/items"
    data = canvas_get(path, paginate=True)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    for item in data:
        print(
            f"{item.get('id')}\t{item.get('type')}\t{item.get('title')}\t"
            f"url={item.get('html_url', '')}"
        )


def cmd_assignments(args: argparse.Namespace) -> None:
    data = canvas_get(f"courses/{args.course_id}/assignments", paginate=True)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    for a in data:
        print(f"{a.get('id')}\t{a.get('name')}\tdue={a.get('due_at')}")


def cmd_pages(args: argparse.Namespace) -> None:
    data = canvas_get(f"courses/{args.course_id}/pages", paginate=True)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    for p in data:
        print(f"{p.get('url')}\t{p.get('title')}\tupdated={p.get('updated_at')}")


def cmd_page(args: argparse.Namespace) -> None:
    page_url = args.page_url.strip("/")
    data = canvas_get(f"courses/{args.course_id}/pages/{page_url}")
    if args.body_only:
        print(data.get("body", ""))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_syllabus(args: argparse.Namespace) -> None:
    try:
        data = canvas_get(f"courses/{args.course_id}", params={"include[]": "syllabus_body"})
    except SystemExit:
        raise
    body = data.get("syllabus_body") if isinstance(data, dict) else None
    if args.body_only and body:
        print(body)
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_files(args: argparse.Namespace) -> None:
    data = canvas_get(f"courses/{args.course_id}/files", paginate=True)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    for f in data:
        print(f"{f.get('id')}\t{f.get('display_name')}\tsize={f.get('size')}")


def cmd_folders(args: argparse.Namespace) -> None:
    data = canvas_get(f"courses/{args.course_id}/folders", paginate=True)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_raw(args: argparse.Namespace) -> None:
    path = args.path.lstrip("/")
    params = {}
    if args.param:
        for p in args.param:
            k, _, v = p.partition("=")
            params[k] = v
    data = canvas_get(path, params or None, paginate=args.paginate)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Canvas LMS API helper (canvas.letovo.ru)")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("self", help="Current API user").set_defaults(func=cmd_self)

    c = sub.add_parser("courses", help="List active courses")
    c.add_argument("--search", help="Search term")
    c.add_argument("--all", action="store_true", help="Include extra fields")
    c.add_argument("--json", action="store_true")
    c.add_argument("--per-page", type=int, default=50)
    c.set_defaults(func=cmd_courses)

    c = sub.add_parser("course", help="Course details")
    c.add_argument("course_id", type=int)
    c.set_defaults(func=cmd_course)

    c = sub.add_parser("modules", help="Course modules")
    c.add_argument("course_id", type=int)
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_modules)

    c = sub.add_parser("module-items", help="Items in a module")
    c.add_argument("course_id", type=int)
    c.add_argument("module_id", type=int)
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_module_items)

    c = sub.add_parser("assignments", help="Course assignments")
    c.add_argument("course_id", type=int)
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_assignments)

    c = sub.add_parser("pages", help="Wiki pages list")
    c.add_argument("course_id", type=int)
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_pages)

    c = sub.add_parser("page", help="Single wiki page (url slug)")
    c.add_argument("course_id", type=int)
    c.add_argument("page_url", help="Page url slug from Canvas")
    c.add_argument("--body-only", action="store_true", help="Print HTML body only")
    c.set_defaults(func=cmd_page)

    c = sub.add_parser("syllabus", help="Course syllabus")
    c.add_argument("course_id", type=int)
    c.add_argument("--body-only", action="store_true")
    c.set_defaults(func=cmd_syllabus)

    c = sub.add_parser("files", help="Course files")
    c.add_argument("course_id", type=int)
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_files)

    c = sub.add_parser("folders", help="Course folders")
    c.add_argument("course_id", type=int)
    c.set_defaults(func=cmd_folders)

    c = sub.add_parser("raw", help="Raw GET path under /api/v1/")
    c.add_argument("path", help="e.g. courses/123/discussion_topics")
    c.add_argument("--param", action="append", help="query key=value")
    c.add_argument("--paginate", action="store_true")
    c.set_defaults(func=cmd_raw)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
