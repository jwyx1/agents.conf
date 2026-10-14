#!/usr/bin/env bash
# ==============================================================================
# agy-smart: Intelligent CLI Launcher powered by Laya System 1 Router
# Automatically selects the optimal subagent persona and model effort in <5ms
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_BIN="$PROJECT_ROOT/.venv/bin"
AGY_BIN="/usr/bin/agy"

# Base flags always enabled for user preference
BASE_FLAGS=(--dangerously-skip-permissions)

PROMPT="$*"

# If no arguments or if an existing flag like --agent, -c, --continue is passed directly:
if [[ -z "$PROMPT" ]] || [[ "$1" == --* ]] || [[ "$1" == -* ]]; then
    exec "$AGY_BIN" "${BASE_FLAGS[@]}" "$@"
fi

# Query Laya decision router
ROUTE_OUTPUT="$("$VENV_BIN/laya-sidecar" route "$PROMPT" --json 2>/dev/null || true)"

if [[ -n "$ROUTE_OUTPUT" ]]; then
    AGENT="$("$VENV_BIN/python" -c "import sys, json; print(json.load(sys.stdin)['target_subagent'])" <<< "$ROUTE_OUTPUT" 2>/dev/null || echo "languages-code")"
    CMD="$("$VENV_BIN/python" -c "import sys, json; print(json.load(sys.stdin)['suggested_command'])" <<< "$ROUTE_OUTPUT" 2>/dev/null || echo "/ponytail")"
    SKILL="$("$VENV_BIN/python" -c "import sys, json; print(json.load(sys.stdin)['recommended_ponytail_skill'])" <<< "$ROUTE_OUTPUT" 2>/dev/null || echo "ponytail")"

    echo "⚡ [Laya System 1] Auto-selected: @$AGENT | Ponytail: $CMD ($SKILL)" >&2
    exec "$AGY_BIN" "${BASE_FLAGS[@]}" --agent "$AGENT" "$@"
else
    exec "$AGY_BIN" "${BASE_FLAGS[@]}" "$@"
fi
