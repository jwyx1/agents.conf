"""Subagent Swarm and Model Tier Router for Antigravity (agy).

Directs prompts to specialized personas and optimal model sizes in sub-30ms.
"""

import time
from typing import Dict, List, Optional, Tuple
from laya_agy_sidecar.engine import LayaEngine
from laya_agy_sidecar.models import RouteResult


class SwarmRouter:
    """Intelligent dispatcher for agy CLI multi-agent sessions."""

    SUPPORTED_SUBAGENTS = [
        "architecture-planning",  # Systems architecture, RFCs, DB schema, OpenAPI
        "languages-code",         # Polyglot implementation (Rust, Go, TypeScript, Python)
        "platform-devops",        # Kubernetes, Docker, CI/CD, Terraform, SRE
        "review-quality",         # QA, minimal bug fixes, E2E tests, documentation
        "security-audit",         # AppSec, Zero Trust, secrets hygiene, penetration tests
    ]

    SUBAGENT_KEYWORDS: Dict[str, List[str]] = {
        "architecture-planning": ["architecture", "plan", "rfc", "design", "blueprint", "schema", "system", "masterplan", "ddd", "microservice"],
        "languages-code": ["rust", "go", "typescript", "python", "implement", "function", "refactor", "algorithm", "class", "code", "feature"],
        "platform-devops": ["docker", "kubernetes", "k8s", "terraform", "ci/cd", "pipeline", "helm", "devops", "prometheus", "sre", "deploy", "nginx"],
        "review-quality": ["review", "qa", "test", "coverage", "playwright", "cypress", "bug", "audit quality", "docs", "document", "unittest"],
        "security-audit": ["security", "audit", "cve", "owasp", "vulnerability", "pentest", "secret", "leak", "injection", "token", "auth"],
    }

    def __init__(self, engine: LayaEngine = None):
        self.engine = engine or LayaEngine()

    def route_subagent(self, prompt: str) -> str:
        """Route user prompt to the most suitable domain subagent."""
        p_lower = prompt.lower()

        # Keyword alignment
        best_agent = "languages-code"
        best_score = 0.0

        for agent, kws in self.SUBAGENT_KEYWORDS.items():
            score = sum(2.0 for kw in kws if kw in p_lower)
            if score > best_score:
                best_score = score
                best_agent = agent

        if best_score > 0:
            return best_agent

        # Fallback to Laya choice primitive
        choice_res = self.engine.choice(
            state=prompt,
            question="which_specialized_subagent_should_handle_this_task",
            choices=self.SUPPORTED_SUBAGENTS,
        )
        return choice_res.choice

    def route_ponytail(self, prompt: str, target_subagent: str) -> Tuple[str, Optional[str], str]:
        """Determine optimal Ponytail skill, level, and command for the given prompt and subagent."""
        p_lower = prompt.lower()

        # 1. Specialized Ponytail skills
        if any(w in p_lower for w in ["debt", "shortcut", "shortcuts", "deferred", "ledger", "ponytail-debt"]):
            return "ponytail-debt", None, "/ponytail-debt"

        if any(w in p_lower for w in ["gain", "impact", "savings", "ponytail-gain"]):
            return "ponytail-gain", None, "/ponytail-gain"

        if any(w in p_lower for w in ["audit repo", "audit whole", "whole repo", "audit codebase", "find bloat", "what can i delete", "ponytail-audit"]):
            return "ponytail-audit", None, "/ponytail-audit"

        if any(w in p_lower for w in ["review", "pr", "diff", "commit", "over-engineered", "ponytail-review"]):
            return "ponytail-review", None, "/ponytail-review"

        # 2. Core Ponytail levels (ultra, lite, full)
        if any(w in p_lower for w in ["ultra", "push back", "over-engineering", "bloat", "yagni", "strictly minimal", "simplest possible"]):
            return "ponytail", "ultra", "/ponytail ultra"

        if any(w in p_lower for w in ["lite", "options", "give choices", "alternatives", "draft"]):
            return "ponytail", "lite", "/ponytail lite"

        # 3. Defaults based on subagent domain
        if target_subagent in ("review-quality", "security-audit"):
            return "ponytail-review", None, "/ponytail-review"
        elif target_subagent == "architecture-planning":
            return "ponytail-audit", None, "/ponytail-audit"
        else:
            return "ponytail", "full", "/ponytail full"

    def dispatch(self, prompt: str) -> RouteResult:
        """Execute full routing analysis and generate execution metadata."""
        start = time.perf_counter()

        target_agent = self.route_subagent(prompt)
        skill, level, cmd = self.route_ponytail(prompt, target_agent)

        latency = (time.perf_counter() - start) * 1000.0

        reasoning = (
            f"Routed to '{target_agent}' with Ponytail skill '{skill}' "
            f"(level={level or 'n/a'}) via '{cmd}'."
        )

        return RouteResult(
            prompt=prompt,
            target_subagent=target_agent,
            subagent_confidence=0.92,
            recommended_ponytail_skill=skill,
            ponytail_level=level,
            suggested_command=cmd,
            reasoning=reasoning,
            latency_ms=round(latency, 2),
        )
