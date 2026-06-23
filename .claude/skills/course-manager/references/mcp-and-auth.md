# Brightspace (D2L) MCP — facts, auth, and idempotent setup

## Config constant (swap here to change the server)

- **MCP launch package:** `brightspace-mcp-server@latest`  ← single source of truth; edit here to swap.
- **Server registration name:** `brightspace`
- Both are overridable at call time via env vars: `BRIGHTSPACE_MCP_PACKAGE`, `BRIGHTSPACE_MCP_NAME`.
- `scripts/ensure_mcp.sh` defaults to these same values — keep the two in sync, or override with the env vars.

## What this server is

- A **stdio** MCP server launched as `npx -y brightspace-mcp-server@latest`.
- It reads Brightspace by driving a real browser (Playwright) and intercepting the session token. It does **not** use the D2L Valence REST API, and it exposes **read-only** tools (no writes).
- Verified package: `brightspace-mcp-server` (RohanMuppa, MIT, Node 18+). Ships a `--purdue` SSO preset and supports other institutions via presets.

## Read tools exposed — use these EXACT names

| Capability | MCP tool |
| --- | --- |
| auth status | `check_auth` |
| list my courses | `get_my_courses` |
| syllabus | `get_syllabus` |
| content / modules | `get_course_content` |
| assignments | `get_assignments` |
| upcoming due dates | `get_upcoming_due_dates` |
| announcements *(instructor text safe; student replies are PII)* | `get_announcements` |
| roster *(PII)* | `get_roster` |
| participant emails *(PII)* | `get_classlist_emails` |
| grades *(PII)* | `get_my_grades` |
| discussions *(student posts — PII)* | `get_discussions` |
| download a file *(may be a student submission — PII)* | `download_file` |

MCP tool calls appear to Claude as `mcp__brightspace__<tool>`. Anything marked *(PII)* → read `ferpa.md` first.

## Credentials & auth — NEVER read, print, or commit these

- Credentials live globally at **`~/.brightspace-mcp/config.json`** (dir `0700`, file `0600`). It stores the Brightspace **password in plaintext**, protected only by file permissions. Treat it as a secret: never read its contents into context, never echo it, never copy it into the repo.
- **One-time setup wizard** (writes that file): `npx -y brightspace-mcp-server@latest setup` — add `--purdue` for Purdue SSO presets, or omit/choose another institution preset. **The user runs this themselves** in a terminal; an agent must never type the user's password. It opens a **visible browser** for SSO + Duo/MFA (approve the push on the phone, ~120s window).
- **Re-auth** when a session expires: `npx -y brightspace-mcp-server@latest auth`.
- **Headless control:** the package reads the `headless` field inside `config.json` (set it `false` to keep the browser visible), **not** a `D2L_HEADLESS` env var. First-time auth is force-visible anyway when no session exists. We still pass `D2L_HEADLESS=false` in the MCP env block as a harmless, future-proof setting (see `ensure_mcp.sh`); do not rely on it for visibility — rely on `config.headless=false`.

## Idempotent registration recipe

1. **Existence check** (does not connect or trigger a login for a pending project server): `claude mcp get brightspace`.
2. If missing, **register at PROJECT scope** so it travels with the repo via `./.mcp.json` (that file carries no secrets):

   ```
   claude mcp add --scope project --transport stdio --env D2L_HEADLESS=false brightspace -- npx -y brightspace-mcp-server@latest
   ```

   Flags come **before** the name; `--` separates the name from the launch command.
3. Prefer the bundled helper over typing this by hand: `bash "${CLAUDE_SKILL_DIR}/scripts/ensure_mcp.sh"` (idempotent).
4. After adding, the server shows as **"Pending approval"** — approve it in Claude Code before its tools become available.

## Scope: why `project`

- Project scope writes `./.mcp.json`, which is committable and shared with anyone who clones the repo. (For a checked-in project skill/server, `allowed-tools` and trust features apply only after the user accepts the workspace-trust dialog.)
- Credentials are **not** in `.mcp.json`; they are global per machine, so each machine runs the setup wizard once.

## EXTENSION POINT — future WRITE path (D2L Valence API)

This server has no write tools and does not use Valence. Writes (posting grades, creating announcements, editing content) are intentionally **out of scope** today. To add them later: integrate the official **D2L Valence REST API** (OAuth 2.0 / app+user key) against `brightspace_base_url`, as a **separate, explicitly-confirmed** path — gate every mutating call behind explicit user confirmation, and keep reads and writes separable. Do not fold writes into this read-only MCP. Mirror of the `EXTENSION POINT` comment in `scripts/ensure_mcp.sh`.
