"""Pydantic data models for Laya decision primitives and sidecar results."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DecisionChoice(BaseModel):
    """Represents a discrete choice selected from candidate classes."""
    choice: str = Field(..., description="The selected option from candidate classes")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Calibrated confidence probability")
    distribution: Dict[str, float] = Field(
        default_factory=dict, description="Probability distribution across all choices"
    )
    latency_ms: float = Field(0.0, description="Inference latency in milliseconds")


class DecisionScore(BaseModel):
    """Represents a continuous score between 0.0 and 1.0."""
    score: float = Field(..., ge=0.0, le=1.0, description="Continuous score/rating")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Calibrated probability")
    latency_ms: float = Field(0.0, description="Inference latency in milliseconds")


class DecisionNoul(BaseModel):
    """Represents a calibrated boolean (yes/no) proposition."""
    value: bool = Field(..., description="Boolean verdict")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Calibrated confidence probability")
    latency_ms: float = Field(0.0, description="Inference latency in milliseconds")


class GuardrailResult(BaseModel):
    """Verdict from the pre-execution guardrail evaluation."""
    command: str
    is_safe: bool
    risk_level: str = Field(..., description="'LOW', 'MEDIUM', 'HIGH', or 'CRITICAL'")
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasons: List[str] = Field(default_factory=list)
    recommended_action: str = Field("ALLOW", description="'ALLOW', 'CONFIRM', or 'BLOCK'")
    latency_ms: float = Field(0.0)


class RouteResult(BaseModel):
    """Verdict from subagent and Ponytail skill routing."""
    prompt: str
    target_subagent: str
    subagent_confidence: float
    recommended_ponytail_skill: str = Field(..., description="Target Ponytail skill name, e.g. ponytail, ponytail-review, ponytail-audit")
    ponytail_level: Optional[str] = Field(None, description="Ponytail level: 'lite', 'full', 'ultra' or None")
    suggested_command: str = Field(..., description="Suggested slash command or activation parameter")
    reasoning: str
    latency_ms: float = Field(0.0)


class SecretScanResult(BaseModel):
    """Verdict from credential and secret leak inspection."""
    contains_secrets: bool
    leak_count: int = 0
    findings: List[Dict[str, Any]] = Field(default_factory=list)
    sanitized_text: Optional[str] = None
    latency_ms: float = Field(0.0)
