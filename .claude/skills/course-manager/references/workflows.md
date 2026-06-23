# Ongoing management workflows

The active course is **always** resolved from `.course/config.json`
(`python3 "${CLAUDE_SKILL_DIR}/scripts/course_config.py" show`). Pass its `d2l_org_unit_id`
to MCP tools that need a course. Every workflow below states what it **reads** and what (if anything)
it **writes** locally, and **confirms before overwriting any local file**.

Before any roster / grades / emails / per-student data, read `ferpa.md`.

## Conventions

- **Non-PII** artifacts (syllabus text, module structure, assignment schedule) **may** be cached under
  `.course/cache/` and committed — but only after you confirm an overwrite with the user.
- **PII** (roster, participant emails, grades, per-student submissions) is **in-session only**: display in
  the terminal, never write to a file. See `ferpa.md`.

## 1. Refresh syllabus
- **Reads:** `get_syllabus` (for the active org unit).
- **Writes (optional, confirm first):** `.course/cache/syllabus.md` — non-PII.
- Steps: `course_config.py show` → `get_syllabus` → summarize → ask before writing/overwriting the cache file.

## 2. Pull content / module structure
- **Reads:** `get_course_content`.
- **Writes (optional, confirm):** `.course/cache/modules.json` (module/topic structure only, non-PII).

## 3. List roster  *(FERPA — PII)*
- **Reads:** `get_roster` (and `get_classlist_emails` only if emails are explicitly needed).
- **Writes:** **nothing** by default — never persisted.
- Output: **counts/roles by default** (e.g. "41 students, 1 TA"). Show individual names/emails only on an
  explicit, scoped request; confirm before printing more than ~10 rows; append a privacy reminder. See `ferpa.md`.

## 4. Upcoming assignments & due dates
- **Reads:** `get_upcoming_due_dates` and/or `get_assignments`.
- **Writes (optional, confirm):** `.course/cache/assignments.json` — **titles + due dates only** (non-PII).
  Never include per-student submission/attempt data.
- Output: sorted by due date, nearest first.

## 5. Diff Brightspace vs local course materials
- **Reads:** `get_course_content` + `get_assignments` + `get_syllabus`; and local files
  (e.g. `schedule.qmd`, `material.qmd`, `syllabus.qmd`, `lecture_slides/`).
- **Writes (optional, confirm):** `.course/cache/diff-report.md` — structure only, **no PII**.
- Steps: pull the Brightspace structure → map it to local files → report what exists in one place but not the
  other, plus title/due-date mismatches → **never auto-edit**; present the diff and let the user decide.

## Grades  *(FERPA — most sensitive; not a default workflow)*
- **Reads:** `get_my_grades`. **In-session only.** Never persist, never commit.
- Default to **aggregates** (mean, n) with small-cell suppression (n < ~5). Show individual scores only on an
  explicit, scoped request. See `ferpa.md`.

## Announcements & discussions
- **Reads:** `get_announcements` (instructor-authored text is safe) / `get_discussions` *(PII — student posts)*.
- **Writes:** nothing. Discussion bodies and any student replies are **in-session only** — never cache them.
  Distinguish instructor text (safe) from student-authored replies/posts (PII). See `ferpa.md`.

## Downloading files  *(FERPA — handle with care)*
- `download_file` writes a file to disk by design. Only download clearly non-PII artifacts (syllabus, handouts)
  on an explicit request. If the file is or could be a student submission, do **not** persist it — or, only on
  explicit user insistence, write it **outside** the repo (session scratchpad) and delete it after. Never under
  `.course/`, never committed. See `ferpa.md` rule 11.

## Failure handling (quick map)

| Symptom | Action |
| --- | --- |
| MCP not registered | run `scripts/ensure_mcp.sh` (setup mode) |
| Server "Pending approval" / tools missing | approve the project server in Claude Code, then retry |
| `check_auth` fails / Duo needed | user runs the setup/auth wizard (visible browser, approve Duo) — see `mcp-and-auth.md` |
| `.course/config.json` missing | run first-time setup |
| config malformed/incomplete | `course_config.py validate` prints the exact problem; fix the JSON |
| course can't be matched | `course_config.py match` returns low confidence → show full `get_my_courses` list, ask user to pick by `org_unit_id`; **never guess** |
