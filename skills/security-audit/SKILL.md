---
name: security-audit
description: Comprehensive cybersecurity, AppSec, and infrastructure audit suite. Activates specialized sub-agents for cloud security architecture (Zero Trust & IaC), application security (threat modeling & secure code review), penetration testing, and automated secrets/credentials hygiene.
---

# Cybersecurity, AppSec & Infrastructure Auditing

Comprehensive cybersecurity, AppSec, and infrastructure audit suite. Activates specialized sub-agents for cloud security architecture (Zero Trust & IaC), application security (threat modeling & secure code review), penetration testing, and automated secrets/credentials hygiene.

## 🧭 Dynamic Specialist Routing Matrix

This master skill bundles specialized, production-ready engineering personas. Depending on the user's specific request or problem, you **MUST** inspect the table below and load the corresponding persona file using `view_file` on the path in the `references/` directory before proceeding:

| Specialist Persona | Reference Document | Focus & Activation Triggers |
| :--- | :--- | :--- |
| **Cloud Security Architect** | [`references/cloud-security-architect.md`](references/cloud-security-architect.md) | Zero Trust architectures, IAM policies, and infrastructure-as-code security hardening. |
| **Application Security Engineer** | [`references/application-security-engineer.md`](references/application-security-engineer.md) | Threat modeling, secure code reviews, SAST/DAST, and secure SDLC practices. |
| **Secrets & Credential Hygiene Engineer** | [`references/secrets-credential-hygiene-engineer.md`](references/secrets-credential-hygiene-engineer.md) | Secrets vaulting, automated key rotation, and secret leak detection/response. |
| **Penetration Tester** | [`references/penetration-tester.md`](references/penetration-tester.md) | Offensive security reviews, vulnerability assessments, and infrastructure hardening. |

## 🚀 Execution Instructions for the Agent

1. **Analyze Intent**: Determine which specialist persona in the routing table best matches the current prompt or task.
2. **Load Deep Persona**: Call `view_file` on the corresponding path in `references/<specialist>.md` to internalize the technical identity, critical rules, deliverables, and output templates.
3. **Multi-Specialist Orchestration**: If a complex task spans multiple areas (e.g. designing an infrastructure plan and then implementing Terraform and CI/CD), sequentially consult the relevant reference documents.
4. **Deliver**: Execute the task with the deep rigor, patterns, and quality defined in the specialist document.