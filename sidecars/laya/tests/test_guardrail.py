"""Unit tests for pre-execution command guardrails."""

import pytest
from laya_agy_sidecar.guardrail import CommandGuardrail


@pytest.fixture
def guardrail():
    return CommandGuardrail()


def test_guardrail_safe_command(guardrail):
    res = guardrail.evaluate("ls -lh /var/log")
    assert res.is_safe is True
    assert res.risk_level == "LOW"
    assert res.recommended_action == "ALLOW"


def test_guardrail_critical_rm_root(guardrail):
    res = guardrail.evaluate("rm -rf /")
    assert res.is_safe is False
    assert res.risk_level == "CRITICAL"
    assert res.recommended_action == "BLOCK"


def test_guardrail_critical_fork_bomb(guardrail):
    res = guardrail.evaluate(":(){ :|:& };:")
    assert res.is_safe is False
    assert res.risk_level == "CRITICAL"
    assert res.recommended_action == "BLOCK"


def test_guardrail_high_risk_git_force(guardrail):
    res = guardrail.evaluate("git push origin main --force")
    assert res.is_safe is False
    assert res.risk_level == "HIGH"
    assert res.recommended_action == "CONFIRM"


def test_guardrail_high_risk_sql_drop(guardrail):
    res = guardrail.evaluate("DROP DATABASE production_users")
    assert res.is_safe is False
    assert res.risk_level == "CRITICAL"
    assert res.recommended_action == "BLOCK"
