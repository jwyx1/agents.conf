"""Laya AI Sidecar for Antigravity (agy) CLI.

Non-autoregressive System 1 decision engine for zero-latency guardrails,
subagent swarm dispatching, model tier selection, and secret filtering.
"""

from laya_agy_sidecar.models import (
    DecisionChoice,
    DecisionScore,
    DecisionNoul,
    GuardrailResult,
    RouteResult,
)
from laya_agy_sidecar.engine import LayaEngine
from laya_agy_sidecar.guardrail import CommandGuardrail
from laya_agy_sidecar.router import SwarmRouter
from laya_agy_sidecar.secret_scanner import SecretScanner

__version__ = "0.1.0"
__all__ = [
    "DecisionChoice",
    "DecisionScore",
    "DecisionNoul",
    "GuardrailResult",
    "RouteResult",
    "LayaEngine",
    "CommandGuardrail",
    "SwarmRouter",
    "SecretScanner",
]
