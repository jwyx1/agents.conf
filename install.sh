#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# agy.conf — Universal Installer & Live Linker
# Connects Antigravity, Claude Code, GitHub Copilot, Cursor & Windsurf.
# ==============================================================================

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat << 'EOF'
Usage: ./install.sh [options]

Options:
  --link        (Default) Create live symlinks so modifications directly update Git.
  --copy        Copy files statically into ~/.gemini instead of linking.
  --help, -h    Show this help message.
EOF
}

MODE="link"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --link) MODE="link"; shift ;;
    --copy) MODE="copy"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
done

if [ "$MODE" = "link" ]; then
  echo "==> Setting up Live Multi-Agent Symlinks via agy-conf..."
  "${REPO_DIR}/bin/agy-conf" link
else
  TARGET_DIR="${GEMINI_DIR:-$HOME/.gemini}"
  echo "==> Statically installing agy configuration to: ${TARGET_DIR}"
  mkdir -p "${TARGET_DIR}/config/rules"
  mkdir -p "${TARGET_DIR}/config/skills"
  mkdir -p "${TARGET_DIR}/scripts"

  cp -r "${REPO_DIR}/rules/"* "${TARGET_DIR}/config/rules/"
  cp -r "${REPO_DIR}/skills/"* "${TARGET_DIR}/config/skills/"
  cp -r "${REPO_DIR}/scripts/"* "${TARGET_DIR}/scripts/"
  chmod +x "${TARGET_DIR}/scripts/"*.py 2>/dev/null || true

  [ -f "${REPO_DIR}/config.json" ] && cp "${REPO_DIR}/config.json" "${TARGET_DIR}/config/config.json"
  [ -f "${REPO_DIR}/import_manifest.json" ] && cp "${REPO_DIR}/import_manifest.json" "${TARGET_DIR}/config/import_manifest.json"
  [ -f "${REPO_DIR}/mcp_config.json" ] && cp "${REPO_DIR}/mcp_config.json" "${TARGET_DIR}/config/mcp_config.json"
  [ -f "${REPO_DIR}/GEMINI.md" ] && cp "${REPO_DIR}/GEMINI.md" "${TARGET_DIR}/GEMINI.md"

  "${REPO_DIR}/bin/agy-conf" install-bin
fi

echo "==> Installation complete! Run 'agy-conf status' for diagnostics."
