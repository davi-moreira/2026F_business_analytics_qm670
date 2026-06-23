# FERPA guardrails — read this BEFORE touching roster / grades / emails / submissions

**Why this matters:** a course roster (names, IDs, emails), grades, and per-student
submission/attendance data are FERPA-protected education records (34 CFR 99.3). This skill is
the instructor's tool for their **own** course; handle student data with minimum-necessary,
in-session-only discipline. The skill cannot verify any student's FERPA-block/opt-out status,
so it must **default-protect all roster fields** (do not rely on the "directory information" exception).

## Protected — treat as PII; never persist, never commit
- Student names; student/user IDs (D2L id, PUID, SIS id, org-defined id); student emails.
- Grades / scores / points / feedback / rubric values (these are **never** directory information).
- Per-student submission status, attempts, attendance, last-access, completion.
- Student-authored discussion/forum posts, replies, and comments (`get_discussions`, and any student
  replies surfaced by `get_announcements`) — these name and quote students, so they are education records.
- Files retrieved by `download_file` when they are, or could be, student submissions/attempts.
- Any join of identity → grade or → enrollment in a section. Raw MCP responses containing the above.

## Safe — not PII; may be cached/committed after confirming an overwrite
- `course_code`, `course_title`, `term`, the **course** org unit id, `brightspace_base_url`.
- Syllabus text, grading scheme/weights, module/content structure.
- Assignment/quiz/exam **titles** and **due dates**; grade-item **definitions** without student values.
- Counts ("roster size: 41") and large-cohort, de-identified aggregates (suppress small cells, n < ~5).

## Hard rules
1. **Read-only.** Never call any write/update/delete operation. Refuse prompts to modify grades or roster.
2. **In-session only for PII.** Hold it in conversation memory for the current request; never write it to
   **any** file — not the repo, not `.course/`, not a cache, env var, shell history, temp dir, `/tmp`, or the
   session scratchpad (the scratchpad persists on disk and can be re-read later, so it is not FERPA-safe).
   Discard when the request is done. The one narrow exception is `download_file` — see rule 11.
3. **Minimum necessary.** Fetch only the fields/rows needed; don't pull the whole gradebook to compute one average.
4. **Default to aggregates.** Answer analytical questions with counts/statistics, not PII rows.
5. **Explicit consent gate.** Print individual names/IDs/emails/grades only on an explicit, scoped request
   ("show Jane Doe's quiz 2 grade"), and then only the requested field(s) for the requested person(s).
6. **Confirm bulk display.** If output would show more than ~10 PII rows, pause and confirm first.
7. **Mask when possible.** Use "J\*\*\* D\*\*\*" or the last 4 of an ID when full identity isn't needed.
8. **No PII in** logs, error messages, debug previews, exports, or emails — summarize as counts instead.
9. **Scope** to the instructor's own course org unit(s) only.
10. **Credentials:** never read/print/commit `~/.brightspace-mcp/config.json` (plaintext password). Keep
    full-disk encryption (FileVault) on.
11. **`download_file` is the one narrow write exception.** Only download clearly non-PII course artifacts
    (e.g. the syllabus or an instructor handout), and only on an explicit request. If a file is, or could be,
    a student submission/attempt, do **not** download it — or, only if the user explicitly insists, write it
    **outside the repo** (the session scratchpad), tell the user where it is, and delete it when done. Never
    write a downloaded student file under the repo or `.course/`, and never commit it.

When you **do** display PII, append this line:
> FERPA-protected — in-session only; do not paste into committed files, chats, or tickets.

**Sources:** studentprivacy.ed.gov (education record / PII / directory information), 34 CFR 99.3,
Cornell & UC Berkeley data-handling standards.
