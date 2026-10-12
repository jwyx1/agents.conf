# Master Skills & Specialized Agents Router

Este enrutador organiza las 5 suites de skills maestras en **4 Agentes Especializados de Primer Nivel**. Cuando el usuario invoque un agente (`@planner`, `@coder`, `@devops`, `@auditor`) o solicite una tarea afín, se activan las skills y sub-personas correspondientes:

---

## 🏛️ Agentes Especializados y Matriz de Skills

| Agente | Tag | Skills Asociadas | Sub-personas Disponibles (`references/`) | Propósito Central & Modos Ponytail |
| :--- | :--- | :--- | :--- | :--- |
| **Architect Planner** | `@planner` | `architecture-planning`, `ponytail-audit`, `ponytail-debt` | `master-plan-architect.md`, `backend-architect.md`, `api-platform-engineer.md`, `software-architect.md` | Arquitectura de sistemas, planes de implementación (Markdown), contratos y Red Teaming sin ejecutar código. Aplica YAGNI y auditoría completa (`ponytail-audit`). |
| **Polyglot Coder** | `@coder` | `languages-code`, `ponytail` | `rust-refactoring-specialist.md`, `frontend-developer.md`, `mcp-builder.md`, `webassembly-engineer.md` | Implementación de código en Rust, TypeScript, Go, Wasm y MCP servers. Aplica `ponytail [lite\|full\|ultra]` (solución más corta y completa, stdlib primero, test de lógica). |
| **Platform DevOps** | `@devops` | `platform-devops`, `ponytail` | `devops-automator.md`, `platform-engineer.md`, `sre-site-reliability-engineer.md`, `database-reliability-engineer.md`, `developer-tooling-engineer.md`, `finops-engineer.md` | Infraestructura, Docker, Kubernetes, CI/CD, Terraform, SRE, DB HA y FinOps. Aplica `ponytail [lite\|full\|ultra]` para automatizaciones mínimas reproducibles. |
| **Security & QA Auditor** | `@auditor` | `review-quality`, `security-audit`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain` | `code-reviewer.md`, `minimal-change-engineer.md`, `test-automation-engineer.md`, `api-tester.md`, `cloud-security-architect.md`, `application-security-engineer.md`, `secrets-credential-hygiene-engineer.md`, `penetration-tester.md`, `git-workflow-master.md`, `technical-writer.md` | Auditoría unificada de calidad y seguridad. `ponytail-review` (Must fix / Should fix / Nice to have con diff mínimo), `ponytail-audit`, `ponytail-debt` (control de rot) y `ponytail-gain`. |

---

## 🧭 Flujos de Trabajo Multi-Agente Soportados

1. **Flujo Aplicación**: `@planner` (diseño) $\rightarrow$ `@coder` (implementación) $\rightarrow$ `@auditor` (validación QA y seguridad).
2. **Flujo Infraestructura / Plataforma**: `@planner` (arquitectura de infra/cloud) $\rightarrow$ `@devops` (IaC, Docker, K8s, CI/CD) $\rightarrow$ `@auditor` (auditoría Zero Trust y tests de resiliencia).
3. **Flujo Full-Stack / Integral**: `@planner` $\rightarrow$ `@coder` + `@devops` $\rightarrow$ `@auditor`.

---

## 🛡️ Reglas de Gobernanza
- Siempre se respeta la pausa obligatoria de revisión del usuario tras la entrega de un plan por `@planner` según lo establecido en `rules/governance.md`.