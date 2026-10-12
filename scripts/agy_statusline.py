#!/usr/bin/env python3
import sys
import json

def fmt_tokens(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}k"
    return str(n)

try:
    data = json.load(sys.stdin)
except Exception:
    data = {}

# Agents list
agents = "@planner | @coder | @devops | @auditor"

# Context Window & Tokens
cw = data.get("context_window", {}) or {}
in_tok = cw.get("total_input_tokens", 0) or 0
out_tok = cw.get("total_output_tokens", 0) or 0
tot_tok = in_tok + out_tok
ctx_size = cw.get("context_window_size", 1048576) or 1048576
used_pct = cw.get("used_percentage", 0) or 0.0

tok_str = f"{fmt_tokens(tot_tok)}/{fmt_tokens(ctx_size)}"

# Quota (5h and weekly remaining)
quota = data.get("quota", {}) or {}
g5h = quota.get("gemini-5h", {})
g_wk = quota.get("gemini-weekly", {})

quota_parts = []
if g5h and "remaining_fraction" in g5h:
    pct_5h = int(round(g5h["remaining_fraction"] * 100))
    quota_parts.append(f"{pct_5h}% (5h)")
if g_wk and "remaining_fraction" in g_wk:
    pct_wk = int(round(g_wk["remaining_fraction"] * 100))
    quota_parts.append(f"{pct_wk}% (wk)")

quota_str = f" │ ⚡ Quota: {', '.join(quota_parts)}" if quota_parts else ""

# Final single-line status bar
print(f"🤖 {agents} │ 📊 Tokens: {tok_str} ({used_pct:.1f}%){quota_str}")
