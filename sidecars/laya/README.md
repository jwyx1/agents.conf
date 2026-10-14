# Laya AI Sidecar (`laya-sidecar`) for Antigravity (`agy`)

> **System 1 Non-Autoregressive Decision Sidecar** providing zero-latency command guardrails, subagent swarm routing, model tier selection, and credential leak interceptors for `agy` CLI workflows.

---

## 📌 Architecture Overview

```
User Prompt / Agent Action
         │
         ▼
┌───────────────────────────────────────────────┐
│     Laya AI System 1 Decision Gate            │
│       • Command Safety Guardrail (<2ms)       │
│       • Subagent Swarm Router (<1ms)          │
│       • Dynamic Ponytail Skill & Level Router (<1ms)│
│       • Outbound Secret Scanner (<1ms)        │
└───────────────────────────────────────────────┘
         │
         ▼
Antigravity (`agy`) Core Execution Engine (System 2 LLM)
```

---

## 🚀 Quick Start

### 1. Installation
```bash
cd /home/jwx/Projects/personal/laya-agy-sidecar
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. CLI Usage

#### **Pre-Execution Command Guardrail:**
```bash
# Safe command:
laya-sidecar guardrail "ls -la /var/log"
# Output: ✅ Action: ALLOW | Risk: LOW (0.8ms)

# High-risk command:
laya-sidecar guardrail "git push origin main --force"
# Output: ⚠️  Action: CONFIRM | Risk: HIGH (1.2ms)

# Critical destructive command:
laya-sidecar guardrail "rm -rf /"
# Output: 🛑 Action: BLOCK | Risk: CRITICAL (0.5ms)
```

#### **Subagent Swarm & Ponytail Skill Router:**
```bash
laya-sidecar route "Create a Terraform module for AWS VPC and EKS cluster"
# Output:
# 🎯 Target Subagent: platform-devops
# ✂️  Ponytail Skill:  ponytail (level: full)
# ⚡ Suggested Cmd:   /ponytail full
# ⏱️  Decision Time:  0.03ms
```

#### **Secret & Credential Scanner:**
```bash
laya-sidecar scan "export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE"
# Output: 🚨 Found 1 potential secrets (0.4ms): AWS Access Key ID
```

#### **Custom Non-Autoregressive Decisions:**
```bash
# Boolean Decision (Noul):
laya-sidecar decide --state "git reset --hard HEAD~1" --question "will_this_discard_uncommitted_work" --boolean

# Discrete Choice:
laya-sidecar decide --state "Write async tokio actor" --question "language" --choices rust python go
```

---

## 🔗 Integration with Antigravity (`agy`)

### Pre-Tool Hook (`hooks/pre-tool-guardrail.sh`)
Add to `hooks.json` or run before bash tool invocations:
```bash
/home/jwx/Projects/personal/laya-agy-sidecar/hooks/pre-tool-guardrail.sh "rm -rf /tmp/build"
```

### Smart CLI Launcher (`hooks/agy-smart-router.sh`)
Automatically selects the optimal subagent and reasoning effort:
```bash
/home/jwx/Projects/personal/laya-agy-sidecar/hooks/agy-smart-router.sh "Design a zero trust authentication flow"
```

---

## 🧪 Running Tests
```bash
pytest -v tests/
```
