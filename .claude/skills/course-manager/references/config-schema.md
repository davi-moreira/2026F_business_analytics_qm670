# `.course/config.json` — schema & how to fill it

Per-repo course identity. **No secrets, no student PII → safe to commit.** One course per repo;
the skill always resolves the active course from this file so you never re-specify it.

## Schema (all fields required, all strings)

Values below are **illustrative placeholders** — fill in your own course.

```json
{
  "course_code": "DEPT 1234",
  "course_title": "Course Title",
  "term": "YYYY Season",
  "d2l_org_unit_id": "123456",
  "brightspace_base_url": "https://<institution>.brightspace.com"
}
```

| field | meaning | where to get it |
| --- | --- | --- |
| `course_code` | catalog code, e.g. "DEPT 1234" | you / your syllabus |
| `course_title` | human-readable title | you / `get_my_courses` |
| `term` | semester label, e.g. "2026 Fall" or "Spring 2027" | you |
| `d2l_org_unit_id` | the **course** org unit id (the course shell — **not** a student/user id) | the `get_my_courses` result |
| `brightspace_base_url` | your Brightspace host | the browser URL / the setup wizard |

- `d2l_org_unit_id` identifies the course, not a person, so it is **not** PII.
- These values are generic and per-repo — nothing about a specific course is hard-coded in the skill itself.

## Managing it with the helper

`scripts/course_config.py` (exit codes: `0` ok · `2` usage/validation · `3` missing file · `4` malformed JSON):

- `validate [--path] [--quiet]` — confirm the file exists, is valid JSON, and has every required field.
- `show [--path] [--json]` — print the active course (use this to resolve the course at the start of any workflow).
- `init --course_code ... --course_title ... --term ... --d2l_org_unit_id ... --brightspace_base_url ...`
  (or `--from-json -` to read a JSON object from stdin) — **refuses to overwrite** an existing file unless `--force` (never overwrites silently).
- `match --courses - --query "<text>"` — fuzzy-rank `get_my_courses` output to find the right course; returns exit `2` and a "do not guess" hint when no candidate is confident.
