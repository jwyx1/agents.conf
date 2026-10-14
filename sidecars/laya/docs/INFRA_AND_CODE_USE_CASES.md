# Practical Engineering Guide: Laya AI for Infrastructure & Code Automation

## 📌 TL;DR
> This guide outlines how to use **Laya AI (`laya-sidecar`)** as a real-time, sub-2ms System 1 decision engine for day-to-day **DevOps / Infrastructure** and **Software Engineering** tasks.
> - **Infrastructure Defense:** Blocks destructive actions in Terraform/OpenTofu (`destroy -auto-approve`), Kubernetes (`delete namespace`, `drain`), Docker (`prune -a --volumes`), and scans manifests for leaked cloud keys.
> - **Code & Agent Optimization:** Instantly routes prompts to the best subagent (`@platform-devops`, `@languages-code`, `@security-audit`), selects the cheapest/fastest LLM tier (`flash_lite` vs `flash` vs `pro`), and protects Git history against unconstrained force-pushes.
> - **Modes of Operation:** Can be run manually via CLI, wrapped via shell launcher (`agy-smart`), or configured as an automated background guardrail via Antigravity's `hooks.json` (`PreToolUse`).

---

## 1. Operating Modes: Manual vs. Automatic

| Mode | Behavior | Activation Method |
| :--- | :--- | :--- |
| **Manual CLI Mode** | Run commands on-demand to test snippets, audit commands, or check prompts. | `laya-sidecar <subcommand> "..."` |
| **Smart Launcher Mode** | Intercepts your user prompt before `agy` runs, selecting the optimal subagent and Ponytail skill/level in <1ms. | `hooks/agy-smart-router.sh "prompt"` |
| **Native Antigravity Hook Mode** | Completely automatic in every session. `agy` checks every tool call with Laya before execution. | Configured via `~/.gemini/config/hooks.json` |

---

## 2. Infrastructure & Cloud Engineering Use Cases

### 🏗️ 1. Blast-Radius Protection in Terraform / OpenTofu
* **The Risk:** An AI agent refactoring IaC modules might run an unconstrained destruction plan that wipes databases, VPC networks, or state backends.
* **Command Check:**
  ```bash
  laya-sidecar guardrail "terraform destroy -auto-approve"
  # Verdict: 🛑 Action: BLOCK | Risk: CRITICAL (0.5ms)
  ```
  ```bash
  laya-sidecar guardrail "tofu apply -target=module.vpc"
  # Verdict: ✅ Action: ALLOW | Risk: LOW (0.8ms)
  ```
* **Guardrail Behavior:** Hard-blocks `-auto-approve` on destructive plans, forcing manual human inspection of the Terraform plan file.

---

### ☸️ 2. Kubernetes & Helm Cluster Safety Gates
* **The Risk:** Agents debugging cluster issues might accidentally delete vital namespaces, wipe PersistentVolumeClaims, or evict workloads.
* **Command Check:**
  ```bash
  laya-sidecar guardrail "kubectl delete namespace production"
  # Verdict: 🛑 Action: BLOCK | Risk: CRITICAL (0.7ms)
  ```
  ```bash
  laya-sidecar guardrail "kubectl get pods -n kube-system"
  # Verdict: ✅ Action: ALLOW | Risk: LOW (0.4ms)
  ```
* **Guardrail Behavior:** Restricts destructive verbs (`delete`, `drain`, `cordon`, `scale --replicas=0`) in production contexts while allowing read-only observability.

---

### 🐳 3. Docker Daemon & Volume Wipe Prevention
* **The Risk:** Mass pruning of stopped containers or unnamed volumes can delete local database states and development cache layers.
* **Command Check:**
  ```bash
  laya-sidecar guardrail "docker system prune -a --volumes -f"
  # Verdict: ⚠️  Action: CONFIRM | Risk: HIGH (0.6ms)
  ```
  ```bash
  laya-sidecar guardrail "docker compose up -d postgres"
  # Verdict: ✅ Action: ALLOW | Risk: LOW (0.5ms)
  ```

---

### 🔑 4. Secret & Credential Leak Interceptor in Manifests
* **The Risk:** Agents generating Kubernetes Secrets, `.tfvars`, or Dockerfiles might leave raw AWS access keys or plaintext passwords in code files.
* **Scan Command:**
  ```bash
  laya-sidecar scan "$(cat deployment.yaml)"
  # Verdict: 🚨 Found 1 potential secrets (0.6ms): AWS Access Key ID (AKIA...)
  ```
* **Sanitization:** Automatically redacts matched credentials with `***REDACTED_AWS_ACCESS_KEY_ID***`.

---

## 3. Code Development & Engineering Use Cases

### 🎯 1. Instant Subagent Swarm Dispatching
* Avoids spending 1,500ms and ~500 prompt tokens on an LLM just to decide which subagent to launch:
  ```bash
  laya-sidecar route "Configure a Prometheus Helm chart and create an Alertmanager rule"
  # 🎯 Target Subagent: platform-devops | Model: flash (medium effort)
  ```
  ```bash
  laya-sidecar route "Write an async worker pool in Go using channels and mutexes"
  # 🎯 Target Subagent: languages-code  | Model: flash (medium effort)
  ```
  ```bash
  laya-sidecar route "Perform a penetration test and look for SQL injection vulnerabilities"
  # 🎯 Target Subagent: security-audit  | Model: pro (high effort)
  ```

---

### 🛡️ 2. Git Safety & Branch Protection
* Prevents agents from discarding uncommitted changes or rewriting shared Git history:
  ```bash
  laya-sidecar guardrail "git reset --hard HEAD~5"
  # Verdict: ⚠️  Action: CONFIRM | Risk: HIGH (0.8ms)
  ```
  ```bash
  laya-sidecar guardrail "git push origin main --force"
  # Verdict: ⚠️  Action: CONFIRM | Risk: HIGH (0.7ms)
  ```

---

### ✂️ 3. Dynamic Subagent & Ponytail Skill Routing
* Code implementation / bug fixes &rarr; `@coder` (`languages-code`) with `ponytail` (level: `full` or `ultra` for strict YAGNI).
* PR / commit / diff inspection &rarr; `@auditor` (`review-quality`) with `ponytail-review`.
* Full repository audit &rarr; `@planner` (`architecture-planning`) or `@auditor` with `ponytail-audit`.
* Shortcut technical debt audit &rarr; Any agent with `ponytail-debt`.

---

## 4. Automatic Hook Integration Recipe (`hooks.json`)

To have `agy` execute this guardrail automatically on every single terminal command:

1. Place hook handler in `/home/jwx/Projects/personal/laya-agy-sidecar/hooks/native_hook.py`.
2. Register in `~/.gemini/config/hooks.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "/home/jwx/Projects/personal/laya-agy-sidecar/.venv/bin/python /home/jwx/Projects/personal/laya-agy-sidecar/hooks/native_hook.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```
