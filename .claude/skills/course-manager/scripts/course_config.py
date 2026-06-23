#!/usr/bin/env python3
"""course-manager :: course_config.py

Deterministic helpers for the per-repo course config at .course/config.json.

Subcommands
  validate   Check the config exists, is valid JSON, and has all required fields.
  show       Print the active course identity (the skill resolves the course from here).
  init       Create .course/config.json from provided fields. Refuses to overwrite an
             existing file unless --force is given (never overwrites silently).
  match      Fuzzy-match a query against a JSON list of Brightspace courses (from the MCP)
             and rank candidates, so the right course can be picked deterministically.

Privacy: this file NEVER reads credentials (~/.brightspace-mcp/) and NEVER stores student
PII. The config holds only non-sensitive course identity, which is safe to commit.

Exit codes: 0 ok | 2 usage/validation error | 3 missing file | 4 malformed JSON
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from difflib import SequenceMatcher

REQUIRED_FIELDS = [
    "course_code",
    "course_title",
    "term",
    "d2l_org_unit_id",
    "brightspace_base_url",
]
DEFAULT_PATH = os.path.join(".course", "config.json")

# Keys we inspect when matching MCP course objects (covers common D2L / Valence shapes).
NAME_KEYS = [
    "course_title", "course_code", "title", "name", "Name",
    "OrgUnitName", "Code", "CourseOfferingName", "courseName",
]
ID_KEYS = [
    "d2l_org_unit_id", "org_unit_id", "OrgUnitId", "Identifier", "Id", "id",
]


def _err(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)


def _read_text(src: str) -> str:
    """Read from stdin ('-') or a file path, with a clear error instead of a traceback."""
    if src == "-":
        return sys.stdin.read()
    try:
        with open(src, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError as e:
        _err(f"cannot read '{src}': {e}")
        sys.exit(2)


def _load(path: str) -> dict:
    """Load config, exiting with a clear, actionable message on any problem."""
    if not os.path.exists(path):
        _err(f"course config not found at '{path}'.")
        print(
            "  -> This repo has no course yet. Run first-time SETUP "
            "(see the course-manager skill) to create it.",
            file=sys.stderr,
        )
        sys.exit(3)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as e:
        _err(f"'{path}' is not valid JSON: {e}")
        print("  -> Open the file and fix the JSON syntax, then re-run.", file=sys.stderr)
        sys.exit(4)
    if not isinstance(data, dict):
        _err(f"'{path}' must contain a JSON object, got {type(data).__name__}.")
        sys.exit(4)
    return data


def _missing(data: dict) -> list[str]:
    problems = []
    for f in REQUIRED_FIELDS:
        v = data.get(f)
        empty = (
            v is None
            or (isinstance(v, str) and not v.strip())
            or (isinstance(v, (list, dict)) and not v)
        )
        if empty:
            problems.append(f)
    return problems


# --------------------------------------------------------------------------- validate
def cmd_validate(args: argparse.Namespace) -> int:
    data = _load(args.path)
    problems = _missing(data)
    if problems:
        _err(f"'{args.path}' is missing required field(s): {', '.join(problems)}")
        print(f"  -> Required: {', '.join(REQUIRED_FIELDS)}", file=sys.stderr)
        return 2
    if not args.quiet:
        print(f"OK: '{args.path}' is valid (all required fields present).")
    return 0


# ------------------------------------------------------------------------------- show
def cmd_show(args: argparse.Namespace) -> int:
    data = _load(args.path)
    problems = _missing(data)
    if problems:
        _err(f"config is incomplete; missing: {', '.join(problems)}")
        return 2
    if args.json:
        print(json.dumps({k: data.get(k) for k in REQUIRED_FIELDS}, indent=2, ensure_ascii=False))
        return 0
    print("Active course (resolved from {}):".format(args.path))
    print(f"  course_code         : {data['course_code']}")
    print(f"  course_title        : {data['course_title']}")
    print(f"  term                : {data['term']}")
    print(f"  d2l_org_unit_id     : {data['d2l_org_unit_id']}")
    print(f"  brightspace_base_url: {data['brightspace_base_url']}")
    return 0


# ------------------------------------------------------------------------------- init
def cmd_init(args: argparse.Namespace) -> int:
    # Assemble the record either from --from-json or from individual flags.
    record: dict = {}
    if args.from_json:
        try:
            record = json.loads(_read_text(args.from_json))
        except json.JSONDecodeError as e:
            _err(f"--from-json payload is not valid JSON: {e}")
            return 2
        if not isinstance(record, dict):
            _err("--from-json must be a JSON object.")
            return 2
    for f in REQUIRED_FIELDS:
        v = getattr(args, f)
        if v is not None:
            record[f] = v

    problems = _missing(record)
    if problems:
        _err(f"cannot init: missing required field(s): {', '.join(problems)}")
        print(f"  -> Provide every field: {', '.join(REQUIRED_FIELDS)}", file=sys.stderr)
        print("     (via flags like --course_code, or a JSON object on --from-json -)", file=sys.stderr)
        return 2

    # Never overwrite silently. The config may already exist and be hand-edited.
    if os.path.exists(args.path) and not args.force:
        _err(f"'{args.path}' already exists; refusing to overwrite.")
        print("  -> Edit it by hand, or pass --force to replace it intentionally.", file=sys.stderr)
        return 2

    os.makedirs(os.path.dirname(args.path) or ".", exist_ok=True)
    # Keep only the known fields, in canonical order (no surprise extra keys, no PII).
    clean = {f: record[f] for f in REQUIRED_FIELDS}
    with open(args.path, "w", encoding="utf-8") as fh:
        json.dump(clean, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"Wrote course config -> {args.path}")
    print("  (no secrets, no student PII — safe to commit)")
    return 0


# ------------------------------------------------------------------------------ match
def _first(obj: dict, keys: list[str]):
    for k in keys:
        if k in obj and obj[k] not in (None, ""):
            return obj[k]
    return None


def _norm(s: str) -> str:
    # Lowercase, split letter<->digit boundaries ("ABC1234" -> "abc 1234"), collapse punctuation,
    # so a spaced query like "ABC 1234" and an unspaced label like "ABC1234 ..." tokenize the same.
    s = str(s).lower()
    s = re.sub(r"(?<=[a-z])(?=[0-9])|(?<=[0-9])(?=[a-z])", " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def _score(query: str, hay: str) -> float:
    """Blend sequence similarity with token-overlap so 'ABC 1234' matches 'ABC1234 ...'."""
    q, h = _norm(query), _norm(hay)
    if not q or not h:
        return 0.0
    seq = SequenceMatcher(None, q, h).ratio()
    qt, ht = set(q.split()), set(h.split())
    overlap = len(qt & ht) / len(qt) if qt else 0.0
    substr = 1.0 if q in h else 0.0
    return max(seq, overlap, substr) if substr else (0.65 * seq + 0.35 * overlap)


def cmd_match(args: argparse.Namespace) -> int:
    try:
        courses = json.loads(_read_text(args.courses))
    except json.JSONDecodeError as e:
        _err(f"--courses payload is not valid JSON: {e}")
        return 2
    # Accept either a bare array or a wrapper like {"courses": [...]} / {"items": [...]}.
    if isinstance(courses, dict):
        for k in ("courses", "items", "results", "data"):
            if isinstance(courses.get(k), list):
                courses = courses[k]
                break
    if not isinstance(courses, list) or not courses:
        _err("--courses must be a non-empty JSON array of course objects.")
        return 2

    name_keys = args.name_keys.split(",") if args.name_keys else NAME_KEYS
    id_keys = args.id_keys.split(",") if args.id_keys else ID_KEYS

    ranked = []
    for c in courses:
        if not isinstance(c, dict):
            continue
        label_parts = [str(_first(c, [k])) for k in name_keys if _first(c, [k])]
        oid = _first(c, id_keys)
        # Never serialize an unlabeled object: if non-course JSON is ever piped in, dumping it
        # could print roster-shaped PII. Fall back to a generic placeholder with just the id.
        label = " | ".join(dict.fromkeys(label_parts)) or f"<unlabeled course {oid}>"
        # Score each name field AND the joined label; take the best.
        candidates = label_parts + ([" ".join(label_parts)] if len(label_parts) > 1 else [])
        s = max((_score(args.query, p) for p in candidates), default=0.0)
        ranked.append({"score": round(s, 3), "org_unit_id": oid, "label": label})

    ranked.sort(key=lambda r: r["score"], reverse=True)
    top = ranked[: args.top]
    best = top[0] if top else None
    # Decide confidence ONCE so text and --json modes agree (the anti-guessing gate must not
    # be bypassable by asking for JSON, or the skill could auto-pick the wrong course).
    confident = bool(best) and best["score"] >= args.threshold

    if args.json:
        print(json.dumps({
            "confident": confident,
            "threshold": args.threshold,
            "matches": [{k: r[k] for k in ("score", "org_unit_id", "label")} for r in top],
        }, indent=2, ensure_ascii=False))
    else:
        print(f"Top {len(top)} match(es) for query: {args.query!r}")
        for i, r in enumerate(top, 1):
            print(f"  {i}. score={r['score']:.3f}  org_unit_id={r['org_unit_id']}  {r['label']}")
        sys.stdout.flush()  # keep the advisory (stderr) after the list (stdout) in a merged view
        if not confident:
            print(
                f"\n  No confident match (best score "
                f"{best['score'] if best else 0:.3f} < threshold {args.threshold}).",
                file=sys.stderr,
            )
            print("  -> Do NOT guess. Show the full list and ask the user to pick by org_unit_id.", file=sys.stderr)

    return 0 if confident else 2


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="course_config.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="validate .course/config.json")
    v.add_argument("--path", default=DEFAULT_PATH)
    v.add_argument("--quiet", action="store_true")
    v.set_defaults(func=cmd_validate)

    s = sub.add_parser("show", help="print the active course identity")
    s.add_argument("--path", default=DEFAULT_PATH)
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_show)

    i = sub.add_parser("init", help="create .course/config.json (refuses to overwrite)")
    i.add_argument("--path", default=DEFAULT_PATH)
    i.add_argument("--force", action="store_true", help="overwrite an existing config intentionally")
    i.add_argument("--from-json", help="read a JSON object of fields from a file or '-' (stdin)")
    for f in REQUIRED_FIELDS:
        i.add_argument(f"--{f}", help=f"set {f}")
    i.set_defaults(func=cmd_init)

    m = sub.add_parser("match", help="rank Brightspace courses against a query")
    m.add_argument("--courses", required=True, help="JSON array (or wrapper) of courses; file or '-' (stdin)")
    m.add_argument("--query", required=True, help="course code/title to search for")
    m.add_argument("--top", type=int, default=5)
    m.add_argument("--threshold", type=float, default=0.45, help="min score to consider confident")
    m.add_argument("--name-keys", help="comma-separated keys to read course names from")
    m.add_argument("--id-keys", help="comma-separated keys to read org unit ids from")
    m.add_argument("--json", action="store_true")
    m.set_defaults(func=cmd_match)
    return p


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
