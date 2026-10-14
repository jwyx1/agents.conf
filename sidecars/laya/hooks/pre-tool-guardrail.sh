#!/usr/bin/env bash
# ==============================================================================
# Antigravity (agy) Pre-Tool Command Guardrail Hook
# Uses Laya AI System 1 Decision Engine (sub-5ms) to intercept destructive commands
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_BIN="$PROJECT_ROOT/.venv/bin"

if [[ ! -x "$VENV_BIN/laya-sidecar" ]]; then
    echo "⚠️  [Laya Guardrail] Sidecar binary not found at $VENV_BIN/laya-sidecar. Skipping check."
    exit 0
fi

COMMAND_TO_CHECK="${1:-}"

if [[ -z "$COMMAND_TO_CHECK" ]]; then
    exit 0
fi

# Run fast evaluation
set +e
VERDICT_JSON="$("$VENV_BIN/laya-sidecar" guardrail "$COMMAND_TO_CHECK" --json 2>/dev/null)"
EXIT_CODE=$?
set -e

if [[ $EXIT_CODE -eq 0 ]]; then
    # Safe to proceed
    exit 0
elif [[ $EXIT_CODE -eq 2 ]]; then
    # Critical risk - hard block
    echo "🛑 [LAYA CRITICAL GUARD] Command blocked by System 1 Decision Gate:" >&2
    echo "   Command: $COMMAND_TO_CHECK" >&2
    exit 2
else
    # High/medium risk - alert
    echo "⚠️  [LAYA SAFETY ALERT] High risk operation flagged:" >&2
    echo "   Command: $COMMAND_TO_CHECK" >&2
    exit 1
fi
