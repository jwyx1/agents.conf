#!/usr/bin/env bash
set -euo pipefail

# agy.conf installer & linker
# Installs or symlinks agy configuration to ~/.gemini/

TARGET_DIR="${GEMINI_DIR:-$HOME/.gemini}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Installing agy configuration to: ${TARGET_DIR}"

mkdir -p "${TARGET_DIR}/config/rules"
mkdir -p "${TARGET_DIR}/config/skills"
mkdir -p "${TARGET_DIR}/scripts"

# Copy or link rules
echo "--> Syncing rules..."
cp -r "${REPO_DIR}/rules/"* "${TARGET_DIR}/config/rules/"

# Copy or link skills
echo "--> Syncing skills..."
cp -r "${REPO_DIR}/skills/"* "${TARGET_DIR}/config/skills/"

# Copy scripts
echo "--> Syncing scripts..."
cp -r "${REPO_DIR}/scripts/"* "${TARGET_DIR}/scripts/"
chmod +x "${TARGET_DIR}/scripts/"*.py 2>/dev/null || true

# Config and manifest
echo "--> Syncing base config files..."
[ -f "${REPO_DIR}/config.json" ] && cp "${REPO_DIR}/config.json" "${TARGET_DIR}/config/config.json"
[ -f "${REPO_DIR}/import_manifest.json" ] && cp "${REPO_DIR}/import_manifest.json" "${TARGET_DIR}/config/import_manifest.json"
[ -f "${REPO_DIR}/mcp_config.json" ] && cp "${REPO_DIR}/mcp_config.json" "${TARGET_DIR}/config/mcp_config.json"

# Root GEMINI.md
if [ -f "${REPO_DIR}/GEMINI.md" ]; then
  echo "--> Syncing GEMINI.md..."
  cp "${REPO_DIR}/GEMINI.md" "${TARGET_DIR}/GEMINI.md"
fi

# Verification of modern CLI tools
echo "--> Verifying Modern CLI Tooling availability:"
for bin in rg fd bat eza sd procs; do
  if command -v "$bin" >/dev/null 2>&1; then
    echo "  [OK] $bin found"
  else
    echo "  [WARN] $bin missing (install via package manager or cargo)"
  fi
done

echo "==> Installation complete! Ready for Antigravity, Cursor, Copilot, Windsurf & Claude."
