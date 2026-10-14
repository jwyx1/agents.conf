"""Unit tests for subagent swarm and Ponytail skill router."""

import pytest
from laya_agy_sidecar.router import SwarmRouter


@pytest.fixture
def router():
    return SwarmRouter()


def test_route_devops(router):
    prompt = "Create a Docker compose file for nginx and configure a GitHub Actions CI/CD pipeline"
    res = router.dispatch(prompt)
    assert res.target_subagent == "platform-devops"
    assert res.recommended_ponytail_skill == "ponytail"
    assert res.ponytail_level == "full"
    assert res.suggested_command == "/ponytail full"


def test_route_security_review(router):
    prompt = "Perform an AppSec review on this PR and search for OWASP SQL injection vulnerabilities"
    res = router.dispatch(prompt)
    assert res.target_subagent == "security-audit"
    assert res.recommended_ponytail_skill == "ponytail-review"
    assert res.suggested_command == "/ponytail-review"


def test_route_architecture_audit(router):
    prompt = "Audit whole codebase and design a distributed system architecture and schema"
    res = router.dispatch(prompt)
    assert res.target_subagent == "architecture-planning"
    assert res.recommended_ponytail_skill == "ponytail-audit"
    assert res.suggested_command == "/ponytail-audit"


def test_route_code_ultra(router):
    prompt = "Implement a Rust service with strictly minimal dependencies, push back on bloat and yagni"
    res = router.dispatch(prompt)
    assert res.target_subagent == "languages-code"
    assert res.recommended_ponytail_skill == "ponytail"
    assert res.ponytail_level == "ultra"
    assert res.suggested_command == "/ponytail ultra"


def test_route_debt(router):
    prompt = "List all shortcut debt markers and see what we deferred"
    res = router.dispatch(prompt)
    assert res.recommended_ponytail_skill == "ponytail-debt"
    assert res.suggested_command == "/ponytail-debt"
