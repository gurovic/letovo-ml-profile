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


def _debug_enabled() -> bool:
    env = load_env()
    flag = (
        env.get("CANVAS_API_DEBUG")
        or os.environ.get("CANVAS_API_DEBUG")
        or "1"
    ).strip().lower()
    return flag not in ("0", "false", "no", "off")


def _debug_log_path() -> Path:
    """Append-only log so agent can paste Canvas traffic into chat."""
    return ROOT / ".canvas_api.log"


def _emit_debug(line: str) -> None:
    print(line, flush=True)
    try:
        with _debug_log_path().open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except OSError:
        pass


def _log_request(
    method: str,
    req_url: str,
    *,
    data: dict[str, str] | None = None,
) -> None:
    """Log Canvas API call to stdout + `.canvas_api.log` (token never logged).

    Default on; set ``CANVAS_API_DEBUG=0`` to silence.
    """
    if not _debug_enabled():
        return
    _emit_debug(f"CANVAS {method} {req_url}")
    if data:
        shown: dict[str, str] = {}
        for k, v in data.items():
            if len(v) > 240:
                shown[k] = v[:240] + f"…(+{len(v) - 240} chars)"
            else:
                shown[k] = v
        _emit_debug(f"CANVAS body: {json.dumps(shown, ensure_ascii=False)}")


def _request(
    method: str,
    path: str,
    *,
    params: dict | None = None,
    data: dict[str, str] | None = None,
    paginate: bool = False,
) -> object:
    api_url, token = canvas_config()
    if path.startswith("http"):
        url = path
    else:
        url = f"{api_url}/{path.lstrip('/')}"

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    all_items: list = []

    while url:
        req_url = url
        if params and not path.startswith("http"):
            sep = "&" if "?" in req_url else "?"
            req_url = req_url + sep + urllib.parse.urlencode(params)
            params = None

        _log_request(method, req_url, data=data)
        body = urllib.parse.urlencode(data).encode("utf-8") if data is not None else None
        req = urllib.request.Request(req_url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read().decode("utf-8")
                link = resp.headers.get("Link", "")
                if _debug_enabled():
                    _emit_debug(f"CANVAS <- {resp.status} ({len(raw)} bytes)")
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            if _debug_enabled():
                _emit_debug(f"CANVAS <- {e.code} ERROR: {detail[:500]}")
            print(f"HTTP {e.code}: {detail}", file=sys.stderr)
            sys.exit(1)

        payload = json.loads(raw) if raw else None

        if paginate and isinstance(payload, list):
            all_items.extend(payload)
            url = _next_link(link)
            continue

        if paginate and isinstance(payload, list):
            return all_items
        return payload

    return all_items if paginate else None


def canvas_get(path: str, params: dict | None = None, *, paginate: bool = False) -> object:
    return _request("GET", path, params=params, paginate=paginate)


def canvas_post(path: str, data: dict[str, str]) -> object:
    return _request("POST", path, data=data)


def canvas_put(path: str, data: dict[str, str]) -> object:
    return _request("PUT", path, data=data)


def canvas_delete(path: str) -> object:
    return _request("DELETE", path)


def canvas_upload_course_file(
    course_id: int,
    file_path: Path,
    *,
    parent_folder_path: str = "/artifact",
    content_type: str | None = None,
    on_duplicate: str = "overwrite",
) -> dict:
    """Upload a local file to a course (Canvas 3-step file upload). Token never logged."""
    file_path = Path(file_path)
    raw_bytes = file_path.read_bytes()
    ctype = content_type or "application/octet-stream"
    if file_path.suffix.lower() == ".zip":
        ctype = "application/zip"

    init = canvas_post(
        f"courses/{course_id}/files",
        {
            "name": file_path.name,
            "size": str(len(raw_bytes)),
            "content_type": ctype,
            "parent_folder_path": parent_folder_path,
            "on_duplicate": on_duplicate,
        },
    )
    if not isinstance(init, dict) or "upload_url" not in init:
        raise SystemExit(f"Unexpected file upload init response: {init!r}")

    upload_url = str(init["upload_url"])
    upload_params = dict(init.get("upload_params") or {})
    boundary = f"----CanvasBoundary{os.urandom(8).hex()}"
    parts: list[bytes] = []
    for key, value in upload_params.items():
        parts.append(f"--{boundary}\r\n".encode())
        parts.append(
            f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode()
        )
        parts.append(str(value).encode("utf-8"))
        parts.append(b"\r\n")
    parts.append(f"--{boundary}\r\n".encode())
    parts.append(
        (
            f'Content-Disposition: form-data; name="file"; '
            f'filename="{file_path.name}"\r\n'
            f"Content-Type: {ctype}\r\n\r\n"
        ).encode()
    )
    parts.append(raw_bytes)
    parts.append(b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    body = b"".join(parts)

    _emit_debug(f"CANVAS POST {upload_url} (multipart file {file_path.name}, {len(raw_bytes)} bytes)")
    req = urllib.request.Request(
        upload_url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            status = resp.status
            raw = resp.read().decode("utf-8")
            location = resp.headers.get("Location")
            _emit_debug(f"CANVAS <- {status} upload ({len(raw)} bytes)")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        _emit_debug(f"CANVAS <- {e.code} ERROR: {detail[:500]}")
        print(f"HTTP {e.code}: {detail}", file=sys.stderr)
        sys.exit(1)

    # Some Canvas installs return JSON file; others redirect to confirm URL.
    if location:
        confirmed = canvas_get(location if location.startswith("http") else location.lstrip("/"))
        if isinstance(confirmed, dict):
            return confirmed
    if raw:
        try:
            payload = json.loads(raw)
            if isinstance(payload, dict) and payload.get("id"):
                return payload
        except json.JSONDecodeError:
            pass
    files = canvas_get(
        f"courses/{course_id}/files",
        {"search_term": file_path.name},
        paginate=True,
    )
    if isinstance(files, list) and files:
        return files[0]
    raise SystemExit("File upload finished but file object not found")


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


MODULE_1_NAME = "Модуль 1. Оценка недвижимости: функции и inference pipeline"


def _default_account_id() -> int:
    env = load_env()
    if env.get("CANVAS_ACCOUNT_ID"):
        return int(env["CANVAS_ACCOUNT_ID"])
    accounts = canvas_get("accounts", paginate=True)
    if not accounts:
        print("Error: no Canvas accounts available for course creation.", file=sys.stderr)
        sys.exit(1)
    return int(accounts[0]["id"])


def _find_course_by_code(code: str) -> dict | None:
    courses = canvas_get(
        "courses",
        {"search_term": code, "enrollment_state": "active"},
        paginate=True,
    )
    for course in courses:
        if course.get("course_code") == code or course.get("name") == code:
            return course
    return None


def cmd_accounts(args: argparse.Namespace) -> None:
    data = canvas_get("accounts", paginate=True)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    for account in data:
        print(f"{account.get('id')}\t{account.get('name', '')}")


def cmd_create_course(args: argparse.Namespace) -> None:
    account_id = args.account_id or _default_account_id()
    payload = {
        "course[name]": args.name,
        "course[course_code]": args.code or args.name,
    }
    if args.enroll_me:
        payload["course[enroll_me]"] = "true"
    result = canvas_post(f"accounts/{account_id}/courses", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_create_module(args: argparse.Namespace) -> None:
    payload = {"module[name]": args.name}
    if args.position is not None:
        payload["module[position]"] = str(args.position)
    result = canvas_post(f"courses/{args.course_id}/modules", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_init_8ml(args: argparse.Namespace) -> None:
    course = _find_course_by_code("8ML")
    if course:
        print(f"Course 8ML already exists: id={course['id']}", file=sys.stderr)
        course_id = int(course["id"])
    else:
        account_id = args.account_id or _default_account_id()
        course = canvas_post(
            f"accounts/{account_id}/courses",
            {
                "course[name]": "8ML",
                "course[course_code]": "8ML",
                "course[enroll_me]": "true",
            },
        )
        course_id = int(course["id"])
        print(f"Created course 8ML: id={course_id}", file=sys.stderr)

    modules = canvas_get(f"courses/{course_id}/modules", paginate=True)
    module_name = args.module_name or MODULE_1_NAME
    existing = next((m for m in modules if m.get("name") == module_name), None)
    if existing:
        print(
            json.dumps(
                {"course_id": course_id, "module": existing, "created": False},
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    module = canvas_post(
        f"courses/{course_id}/modules",
        {"module[name]": module_name},
    )
    print(
        json.dumps(
            {"course_id": course_id, "module": module, "created": True},
            ensure_ascii=False,
            indent=2,
        )
    )


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

    c = sub.add_parser("accounts", help="Accounts available for course creation")
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_accounts)

    c = sub.add_parser("create-course", help="Create a new course")
    c.add_argument("--name", required=True)
    c.add_argument("--code", help="Course code (default: same as name)")
    c.add_argument("--account-id", type=int, help="Canvas account id (default: first available)")
    c.add_argument("--enroll-me", action="store_true", help="Enroll current user as teacher")
    c.set_defaults(func=cmd_create_course)

    c = sub.add_parser("create-module", help="Create an empty module in a course")
    c.add_argument("course_id", type=int)
    c.add_argument("--name", required=True)
    c.add_argument("--position", type=int)
    c.set_defaults(func=cmd_create_module)

    c = sub.add_parser(
        "init-8ml",
        help="Create course 8ML and module 1 (idempotent)",
    )
    c.add_argument("--account-id", type=int)
    c.add_argument("--module-name", help=f"Default: {MODULE_1_NAME}")
    c.set_defaults(func=cmd_init_8ml)

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
