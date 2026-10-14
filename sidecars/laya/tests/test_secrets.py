"""Unit tests for secret and credential leak scanner."""

from laya_agy_sidecar.secret_scanner import SecretScanner


def test_clean_text_no_secrets():
    scanner = SecretScanner()
    res = scanner.scan("This is a public documentation file with no credentials.")
    assert res.contains_secrets is False
    assert res.leak_count == 0


def test_aws_key_detection_and_redaction():
    scanner = SecretScanner()
    raw = "Deploying with key AKIAIOSFODNN7EXAMPLE to us-east-1"
    res = scanner.scan(raw, sanitize=True)
    assert res.contains_secrets is True
    assert res.leak_count == 1
    assert "AKIAIOSFODNN7EXAMPLE" not in res.sanitized_text
    assert "REDACTED" in res.sanitized_text


def test_github_pat_detection():
    scanner = SecretScanner()
    raw = "git remote set-url origin https://ghp_123456789012345678901234567890123456@github.com/org/repo"
    res = scanner.scan(raw, sanitize=True)
    assert res.contains_secrets is True
    assert "ghp_" not in res.sanitized_text
