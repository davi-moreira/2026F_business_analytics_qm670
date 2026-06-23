#!/usr/bin/env bash
# course-manager :: ensure_mcp.sh
# Idempotently register the Brightspace (D2L) MCP server for THIS repo at PROJECT scope.
#
# Why project scope: the server config lands in ./.mcp.json so it travels with the repo.
# Commit .mcp.json — it carries NO secrets. Credentials live globally at ~/.brightspace-mcp/.
#
# Idempotent: we only add the server if THIS repo's ./.mcp.json does not already list it,
# so re-running setup is safe and never connects to Brightspace.
#
# READ-ONLY: this registration enables READ tools only. The future WRITE path
# (D2L Valence API) is intentionally NOT wired up here — see the EXTENSION POINT below.
set -euo pipefail

# ---- Config constants (swap here, or override via env) -----------------------
# Single source of truth for the launch package. This mirrors the constant documented
# at the top of references/mcp-and-auth.md — keep the two in sync. To swap the package
# or server name without editing files, export BRIGHTSPACE_MCP_PACKAGE / BRIGHTSPACE_MCP_NAME.
PACKAGE="${BRIGHTSPACE_MCP_PACKAGE:-brightspace-mcp-server@latest}"
SERVER_NAME="${BRIGHTSPACE_MCP_NAME:-brightspace}"
# We pass D2L_HEADLESS=false into the server env as requested. IMPORTANT (verified against
# the package source): this package does NOT currently read D2L_HEADLESS — the EFFECTIVE
# control is the "headless": false field in ~/.brightspace-mcp/config.json (written by the
# one-time setup wizard), and first-time auth is force-visible anyway when no session exists.
# We still set the env var: it is harmless and future-proofs the recipe if the package adopts it.
HEADLESS="${D2L_HEADLESS:-false}"

# ---- Preflight ---------------------------------------------------------------
command -v claude  >/dev/null 2>&1 || { echo "ERROR: 'claude' CLI not found on PATH." >&2; exit 3; }
command -v npx     >/dev/null 2>&1 || { echo "ERROR: 'npx' (Node.js) not found on PATH; the MCP launches via npx." >&2; exit 3; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: 'python3' not found on PATH (used for the idempotency check)." >&2; exit 3; }

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
MCP_JSON="$ROOT/.mcp.json"

# ---- Idempotency check (PROJECT-scoped) -------------------------------------
# We want THIS repo's own ./.mcp.json to list the server so it travels with the repo. We check
# that file directly rather than `claude mcp get`, which resolves across ALL scopes and would
# falsely report "already registered" if a same-named server exists at user/local scope —
# leaving this repo with no committable .mcp.json. Reading .mcp.json never triggers a login.
if [ -f "$MCP_JSON" ] && python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if sys.argv[2] in (d.get("mcpServers") or {}) else 1)' "$MCP_JSON" "$SERVER_NAME" 2>/dev/null; then
  echo "OK: MCP server '$SERVER_NAME' is already in $MCP_JSON (no change)."
  echo "    Inspect with: claude mcp get $SERVER_NAME"
  exit 0
fi

# ---- Register at project scope ----------------------------------------------
echo "Registering MCP server '$SERVER_NAME' at PROJECT scope (-> ./.mcp.json) ..."
# Flags come BEFORE the name; `--` separates the server name from the launch command.
claude mcp add \
  --scope project \
  --transport stdio \
  --env "D2L_HEADLESS=${HEADLESS}" \
  "$SERVER_NAME" \
  -- npx -y "$PACKAGE"

# ---- EXTENSION POINT: future WRITE path (D2L Valence API) --------------------
# This skill is READ-ONLY today. To add writes later, do NOT silently bolt mutating
# tools onto this registration. Wire a SEPARATE, explicitly-confirmed Valence path
# (OAuth 2.0 against brightspace_base_url from .course/config.json), and gate every
# mutating call behind explicit user confirmation. Keep reads and writes separable.
# ------------------------------------------------------------------------------

echo
echo "DONE registering. Next steps:"
echo "  1) Approve the project MCP server when Claude Code prompts you"
echo "     (project-scope servers from .mcp.json start as 'Pending approval')."

# ---- Credentials advisory (existence check ONLY — never read the file contents) ----
# The server reads nothing until a one-time setup wizard writes ~/.brightspace-mcp/config.json.
# That file holds your Brightspace password in plaintext (file-perm protected); this script
# NEVER reads, prints, or copies it. We only check whether it EXISTS.
CRED="$HOME/.brightspace-mcp/config.json"
if [ -f "$CRED" ]; then
  echo "  2) Credentials already present at ~/.brightspace-mcp/config.json — you are set."
  echo "     (Re-auth if a session expired:  npx -y $PACKAGE auth )"
else
  echo "  2) Run the ONE-TIME setup wizard YOURSELF in a terminal (it opens a visible"
  echo "     browser for SSO + Duo/MFA on your phone; do NOT let an agent type your password):"
  echo "        npx -y $PACKAGE setup        # add your institution's SSO preset if any, e.g. --purdue"
  echo "     It writes ~/.brightspace-mcp/config.json (set \"headless\": false there to keep"
  echo "     the browser visible for future logins)."
fi
echo "  3) './.mcp.json' is safe to commit — it contains NO secrets."
