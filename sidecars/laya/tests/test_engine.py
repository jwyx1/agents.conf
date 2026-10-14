"""Unit tests for Laya decision engine."""

from laya_agy_sidecar.engine import LayaEngine


def test_engine_choice_primitive():
    engine = LayaEngine()
    choices = ["python", "rust", "kubernetes"]
    result = engine.choice(
        state="We need to write a fast systems program with zero garbage collection.",
        question="which_programming_language",
        choices=choices,
    )
    assert result.choice == "rust"
    assert result.confidence > 0.4
    assert result.latency_ms >= 0.0


def test_engine_noul_primitive_safety():
    engine = LayaEngine()
    destructive_res = engine.noul(
        state="rm -rf /home/jwx",
        question="is_this_command_destructive",
    )
    assert destructive_res.value is True
    assert destructive_res.confidence >= 0.85

    safe_res = engine.noul(
        state="ls -la /home/jwx",
        question="is_this_command_destructive",
    )
    assert safe_res.value is False


def test_engine_score_primitive():
    engine = LayaEngine()
    res = engine.score(state="System running smoothly", question="health_score")
    assert 0.0 <= res.score <= 1.0
    assert res.confidence > 0.0
