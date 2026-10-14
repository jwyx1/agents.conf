"""High-Speed Secret & Credential Leak Scanner.

Scans prompts, tool outputs, and environment variables for accidental leaks.
"""

import re
import time
from typing import Any, Dict, List
from laya_agy_sidecar.models import SecretScanResult


class SecretScanner:
    """Pre-commit and outbound secret leak scanner."""

    SECRET_PATTERNS = [
        (r"\bAKIA[0-9A-Z]{16}\b", "AWS Access Key ID"),
        (r"\bghp_[0-9a-zA-Z]{36}\b", "GitHub Personal Access Token"),
        (r"\bgithub_pat_[0-9a-zA-Z_]{82}\b", "GitHub Fine-Grained Personal Access Token"),
        (r"\bglpat-[0-9a-zA-Z\-]{20,}\b", "GitLab Personal Access Token"),
        (r"\bxox[baprs]-[0-9a-zA-Z]{10,48}\b", "Slack Token"),
        (r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----", "Private Cryptographic Key"),
        (r"(?i)\b(?:api[_-]?key|bearer|token|secret|password)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-\.]{16,})['\"]?", "Generic API Secret/Token Assignment"),
    ]

    def scan(self, text: str, sanitize: bool = True) -> SecretScanResult:
        """Scan text for credentials and optionally sanitize them."""
        start = time.perf_counter()
        findings: List[Dict[str, Any]] = []
        sanitized = text

        for pattern, label in self.SECRET_PATTERNS:
            for match in re.finditer(pattern, text):
                findings.append({
                    "type": label,
                    "match": match.group(0)[:6] + "..." if len(match.group(0)) > 6 else "***",
                    "start": match.start(),
                    "end": match.end(),
                })
                if sanitize:
                    sanitized = sanitized.replace(match.group(0), f"***REDACTED_{label.upper().replace(' ', '_')}***")

        latency = (time.perf_counter() - start) * 1000.0

        return SecretScanResult(
            contains_secrets=len(findings) > 0,
            leak_count=len(findings),
            findings=findings,
            sanitized_text=sanitized if sanitize else None,
            latency_ms=round(latency, 2),
        )
