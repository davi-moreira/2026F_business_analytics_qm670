---
name: course-manager
description: Bootstraps and manages a single Brightspace (D2L) course per repository via the brightspace-mcp-server MCP. Use for first-time setup ("set up this course", "connect Brightspace", "register the MCP") and for ongoing management ("pull my syllabus", "sync course content", "list the roster", "what assignments are due", "diff Brightspace against my files"). Resolves the active course from .course/config.json so the course never needs re-specifying. Read-only and FERPA-aware: roster, emails, and grades stay in-session and are never written to disk or committed. Triggers on mentions of Brightspace, D2L, syllabus, roster, gradebook, course content or modules, due dates, or an org unit id. Invoke directly as /course-manager.
---

# course-manager

**How to invoke in a fresh course repo:** This skill lives at `.claude/skills/course-manager/` and is committed, so it travels with the repo to every clone. Open Claude Code in the repo root and type `/course-manager` (or just say "set up this course" / "pull my syllabus"). On the **first** run the repo has no course yet, so the skill enters **setup mode**: it registers the Brightspace MCP for this repo, helps you pick the right course from your Brightspace account, and saves that course's identity to `.course/config.json`. Every run after that it reads that file and goes straight to **management mode** — you never re-specify the course. Nothing about a specific course, ID, or term is baked into the skill; it is fully parameterized per repo.

Scripts resolve via `${CLAUDE_SKILL_DIR}` so they work regardless of the current directory.

## Step 0 — pick the mode
Run: `python3 "${CLAUDE_SKILL_DIR}/scripts/course_config.py" validate`
- exit **3** (no file) → **Setup mode**.
- exit **2** (incomplete) or **4** (malformed JSON) → report the exact message it printed; offer to fix the JSON by hand or re-run `init --force`.
- exit **0** → **Management mode**.

## Setup mode  (no `.course/config.json` yet)
Do these in order; stop and report clearly if any step fails (see `references/workflows.md` failure map).
1. **Register the MCP (idempotent):** `bash "${CLAUDE_SKILL_DIR}/scripts/ensure_mcp.sh"` — adds the `brightspace` server at **project scope** (→ committable `.mcp.json`) only if it is missing.
2. **Harden `.gitignore` (idempotent):** `bash "${CLAUDE_SKILL_DIR}/scripts/harden_gitignore.sh"` — blocks credential / roster / grade files.
3. **Approve + authenticate:** approve the project MCP server when Claude Code prompts. If `~/.brightspace-mcp/config.json` does not exist, the **user** runs the one-time setup wizard themselves (it opens a visible browser for SSO + Duo). **Never type the user's password for them.** Details: `references/mcp-and-auth.md`.
4. **List courses:** call the MCP tool `get_my_courses`. If it errors on auth, the wizard hasn't run or the session expired — see `references/mcp-and-auth.md`.
5. **Identify the course:** ask the user which course this repo is for, then rank candidates deterministically — pipe the `get_my_courses` JSON into `python3 "${CLAUDE_SKILL_DIR}/scripts/course_config.py" match --courses - --query "<their answer>"`. If no confident match, show the full list and ask them to pick by org unit id. **Never guess.**
6. **Save identity (never overwrites silently):** `python3 "${CLAUDE_SKILL_DIR}/scripts/course_config.py" init --course_code … --course_title … --term … --d2l_org_unit_id … --brightspace_base_url …` (or pipe a JSON object with `--from-json -`; the org unit id is the **course** org unit, not a student id). Then tell the user that `.course/config.json` and `.mcp.json` are safe to commit; credentials are not in the repo. Schema: `references/config-schema.md`.

## Management mode  (`.course/config.json` exists)
First resolve the active course: `python3 "${CLAUDE_SKILL_DIR}/scripts/course_config.py" show`, and pass its `d2l_org_unit_id` to MCP tools. Full read/write contracts are in `references/workflows.md`.
- **Refresh syllabus** — `get_syllabus` → optional `.course/cache/syllabus.md` (confirm overwrite).
- **Pull content / modules** — `get_course_content` → optional `.course/cache/modules.json`.
- **List roster** *(PII)* — `get_roster`; counts/roles by default; in-session only; never written.
- **Upcoming assignments / due dates** — `get_upcoming_due_dates` / `get_assignments`; sorted; titles + dates cacheable.
- **Diff vs local files** — compare Brightspace structure to local course materials; report only; **never auto-edit**.

Confirm before overwriting **any** local file. Read `references/ferpa.md` before roster / grades / emails.

## FERPA (non-negotiable)
Roster, emails, grades, and per-student submissions are FERPA-protected education records. Read-only; **in-session only**; aggregates by default; explicit, scoped consent before showing individuals; never persist or commit PII; never read or print credentials. Full rules: `references/ferpa.md`.

## Read-only today; writes are a future extension
This skill uses only read tools. The write path (the **D2L Valence API**) is intentionally **not** implemented — see the `EXTENSION POINT` in `references/mcp-and-auth.md` and `scripts/ensure_mcp.sh`.

## References
- `references/mcp-and-auth.md` — MCP package constant, real tool names, auth/Duo reality, idempotent recipe, project scope, write extension point.
- `references/config-schema.md` — `.course/config.json` schema and how to fill each field.
- `references/workflows.md` — per-workflow read/write contracts and the failure map.
- `references/ferpa.md` — student-data handling rules.
