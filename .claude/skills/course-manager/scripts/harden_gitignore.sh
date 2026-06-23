#!/usr/bin/env bash
# course-manager :: harden_gitignore.sh
# Ensure this repo's .gitignore blocks credential- and FERPA-bearing files.
# Idempotent: appends a clearly-marked block only if it is not already present.
#
# Design: the skill keeps student PII (roster, grades, submissions) IN-SESSION and never
# writes it to disk. The patterns below are a defense-in-depth safety net, designed to:
#   - catch obvious credential / token files and unambiguous PII-dump names, but
#   - NOT use broad globs (grades*.csv, students*.csv, *secret*, *token*.json) that would
#     silently exclude legitimate analytics teaching material, and
#   - protect the skill's own write area with a SAFE-BY-DEFAULT allowlist: everything under
#     .course/ is ignored except the course config and four sanctioned non-PII cache files.
#
# Intentionally NOT ignored (committable, no secrets/PII): .course/config.json and .mcp.json.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
GI="$ROOT/.gitignore"
MARK="# >>> course-manager (credentials + FERPA) >>>"
ENDMARK="# <<< course-manager (credentials + FERPA) <<<"

if [ -f "$GI" ] && grep -qF "$MARK" "$GI"; then
  echo "OK: .gitignore already hardened (course-manager block present)."
  exit 0
fi

{
  printf '\n%s\n' "$MARK"
  cat <<'PATTERNS'
# --- Brightspace MCP credentials / tokens (canonical home is ~/.brightspace-mcp/) ---
# Tightened to credential-specific names so ordinary course material is never clobbered
# (e.g. a "tokenization_demo.json" dataset or "secretary_notes.md" survive).
**/.brightspace-mcp/
.brightspace-mcp.json
.env
.env.*
*.credentials
*.secret
secrets.*
*-secret.*
secrets/
auth_token*.json
*.token.json
# --- FERPA safety net: unambiguous student-record / MCP-dump names (repo-wide) ---
# This skill keeps roster/grades/submissions IN-SESSION and never writes them to disk; these
# only catch clearly-named accidental dumps. They deliberately avoid broad globs that would
# hit legitimate datasets. If you ever must keep an exported PII file, put it under .course/
# (auto-ignored below) or name it *.pii.* — and never commit it.
*.pii.*
*-pii.*
pii/
student_data/
_student_records/
mcp_response*.json
brightspace_*.json
d2l_*.json
*.d2l.json
*.roster.cache
submissions/
**/submissions/
*.ferpa
# --- .course/ allowlist (SAFE BY DEFAULT) ---
# Ignore everything the skill might write under .course/, then re-include ONLY the course
# config and the four sanctioned NON-PII cache artifacts. Anything unexpected written here
# (a roster dump, a downloaded submission, a stray cache file) stays ignored by default.
.course/*
!.course/config.json
!.course/cache/
.course/cache/*
!.course/cache/syllabus.md
!.course/cache/modules.json
!.course/cache/assignments.json
!.course/cache/diff-report.md
PATTERNS
  printf '%s\n' "$ENDMARK"
} >> "$GI"

echo "Hardened $GI with credential + FERPA ignore patterns."
echo "Note: .course/config.json and .mcp.json remain committable (no secrets/PII)."
echo "      Everything else under .course/ is ignored by default; only the 4 sanctioned"
echo "      non-PII cache files (syllabus.md, modules.json, assignments.json, diff-report.md)"
echo "      are allowed through. Student PII is never written to disk by this skill."
