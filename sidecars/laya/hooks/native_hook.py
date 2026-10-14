#!/usr/bin/env python3
"""Antigravity (agy) Native PreToolUse Hook.

Interprets the PreToolUse contract on stdin, runs Laya System 1 Guardrail in <2ms,
and outputs the required decision JSON to stdout.
"""

import os
import sys
import json
from datetime import datetime, timezone
from laya_agy_sidecar.guardrail import CommandGuardrail

LOG_PATH = os.path.expanduser("~/.local/state/laya/guardrail.log")
SYMLINK_PATH = "/tmp/laya-guardrail.log"

def log_audit(decision: str, risk_level: str, latency_ms: float, cmd: str, reasons: list = None):
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        timestamp = datetime.now(timezone.utc).isoformat()
        reason_str = f" | reasons: {', '.join(reasons)}" if reasons else ""
        log_entry = f"[{timestamp}] [{decision.upper()}] [risk={risk_level}] [{latency_ms:.2f}ms] cmd={json.dumps(cmd)}{reason_str}\n"
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(log_entry)

        # Convenience symlink in /tmp
        if not os.path.exists(SYMLINK_PATH) and not os.path.islink(SYMLINK_PATH):
            try:
                os.symlink(LOG_PATH, SYMLINK_PATH)
            except OSError:
                pass
    except Exception:
        # Logging failure must never block or crash the hook
        pass

def main():
    cmd = ""
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({"decision": "allow"}))
            return

        payload = json.loads(raw_input)
        tool_call = payload.get("toolCall", {})
        tool_name = tool_call.get("name", "")
        args = tool_call.get("args", {})

        # Only evaluate command execution tools
        if tool_name == "run_command":
            cmd = args.get("CommandLine", "")
            if cmd:
                guard = CommandGuardrail()
                res = guard.evaluate(cmd)

                if res.risk_level == "CRITICAL":
                    log_audit("deny", res.risk_level, res.latency_ms, cmd, res.reasons)
                    out = {
                        "decision": "deny",
                        "reason": f"🛑 Blocked by Laya Guardrail: {', '.join(res.reasons)}"
                    }
                    print(json.dumps(out))
                    return
                elif res.risk_level in ("HIGH", "MEDIUM"):
                    log_audit("ask", res.risk_level, res.latency_ms, cmd, res.reasons)
                    out = {
                        "decision": "ask",
                        "reason": f"⚠️ Laya Safety Gate: {', '.join(res.reasons)}"
                    }
                    print(json.dumps(out))
                    return
                else:
                    log_audit("allow", res.risk_level, res.latency_ms, cmd)

        # Default: allow tool execution
        print(json.dumps({"decision": "allow"}))
    except Exception as e:
        log_audit("fallback_allow", "UNKNOWN", 0.0, cmd, [str(e)])
        # Fail open with warning on internal error to avoid locking agent
        print(json.dumps({"decision": "allow", "reason": f"Laya hook fallback: {str(e)}"}))

if __name__ == "__main__":
    main()
