"""Command and Tool Argument Pre-Execution Guardrails.

Protects against catastrophic agent execution in sub-40ms runtime checks.
"""

import re
import time
from typing import List
from laya_agy_sidecar.engine import LayaEngine
from laya_agy_sidecar.models import GuardrailResult


class CommandGuardrail:
    """Pre-execution security & safety evaluator for agy CLI tools."""

    CRITICAL_PATTERNS = [
        (r"\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f?|-rf|-fr)\s+(/\s*|\.\s*|\*|~|/home/?\b|/etc/?\b|/usr/?\b|/var/?\b)", "Recursive root or sensitive directory deletion"),
        (r"\bdd\s+if=.*of=(/dev/sd|/dev/nvme|/dev/vd|/dev/null)", "Direct raw block device overwriting"),
        (r"\bmkfs(\.\w+)?\s+/dev/", "Filesystem format operation"),
        (r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:", "Fork bomb detected"),
        (r"\bchmod\s+(-R\s+)?(777|000)\s+(/|~|/etc|/bin|/usr)", "Global insecure permission alteration on system roots"),
        (r"\bDROP\s+(DATABASE|SCHEMA)\b", "Destructive SQL drop database query"),
        (r"\bTRUNCATE\s+TABLE\b", "Destructive SQL truncate table query"),
    ]

    HIGH_RISK_PATTERNS = [
        (r"\bgit\s+push\s+.*--force\b", "Force pushing git branch, potential history loss"),
        (r"\bgit\s+reset\s+--hard\b", "Hard git reset discarding uncommitted work"),
        (r"\bgit\s+clean\s+-[a-zA-Z]*f", "Force cleaning untracked git files"),
        (r"\bDROP\s+TABLE\b", "Destructive SQL drop table query"),
        (r"\bDELETE\s+FROM\s+\w+\s*;?\s*$", "Unconstrained SQL delete without WHERE clause"),
        (r"\bdocker\s+system\s+prune\s+-a\b", "Pruning all docker containers, images, and volumes"),
        (r"\bkill\s+-9\s+1\b", "Killing system init process (PID 1)"),
    ]

    MEDIUM_RISK_PATTERNS = [
        (r"\bsudo\s+pacman\s+-R\w*\b", "Package removal with administrative privileges"),
        (r"\bsudo\s+systemctl\s+(stop|disable)\b", "Stopping systemd service"),
        (r"\bpkill\s+-f\b", "Pattern-based process termination"),
        (r"\bcurl\b.*\|\s*(bash|sh)\b", "Piping remote script directly to shell interpreter"),
    ]

    def __init__(self, engine: LayaEngine = None):
        self.engine = engine or LayaEngine()

    def evaluate(self, command: str) -> GuardrailResult:
        """Evaluate a shell command and return a safety verdict."""
        start = time.perf_counter()
        reasons: List[str] = []
        risk_level = "LOW"
        action = "ALLOW"
        cmd_clean = command.strip()

        # 1. Critical pattern matching
        for pattern, desc in self.CRITICAL_PATTERNS:
            if re.search(pattern, cmd_clean, re.IGNORECASE):
                reasons.append(desc)
                risk_level = "CRITICAL"
                action = "BLOCK"
                break

        # 2. High risk pattern matching
        if risk_level != "CRITICAL":
            for pattern, desc in self.HIGH_RISK_PATTERNS:
                if re.search(pattern, cmd_clean, re.IGNORECASE):
                    reasons.append(desc)
                    risk_level = "HIGH"
                    action = "CONFIRM"

        # 3. Medium risk pattern matching
        if risk_level not in ("CRITICAL", "HIGH"):
            for pattern, desc in self.MEDIUM_RISK_PATTERNS:
                if re.search(pattern, cmd_clean, re.IGNORECASE):
                    reasons.append(desc)
                    risk_level = "MEDIUM"
                    action = "CONFIRM"

        # 4. Neural System 1 Noul verdict validation
        noul_res = self.engine.noul(
            state=f"Proposed command: `{cmd_clean}`",
            question="is_this_command_destructive_or_dangerous"
        )

        if noul_res.value and noul_res.confidence > 0.85 and risk_level == "LOW":
            risk_level = "HIGH"
            action = "CONFIRM"
            reasons.append(f"Model classified action as destructive (confidence: {noul_res.confidence:.2%})")

        latency = (time.perf_counter() - start) * 1000.0

        return GuardrailResult(
            command=cmd_clean,
            is_safe=(action == "ALLOW"),
            risk_level=risk_level,
            confidence=noul_res.confidence,
            reasons=reasons or ["Command identified as safe for automated execution."],
            recommended_action=action,
            latency_ms=round(latency, 2),
        )
