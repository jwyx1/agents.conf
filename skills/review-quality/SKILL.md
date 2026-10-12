---
name: review-quality
description: Code review, quality assurance, and engineering workflow suite. Activates specialized sub-agents for objective code reviews, surgical minimal-change bug fixes, Git workflow mastery, Playwright/Cypress end-to-end test automation, API validation/load testing, and technical documentation.
---

# Code Review, Quality Assurance & Engineering Workflows

Code review, quality assurance, and engineering workflow suite. Activates specialized sub-agents for objective code reviews, surgical minimal-change bug fixes, Git workflow mastery, Playwright/Cypress end-to-end test automation, API validation/load testing, and technical documentation.

## 🧭 Dynamic Specialist Routing Matrix

This master skill bundles specialized, production-ready engineering personas. Depending on the user's specific request or problem, you **MUST** inspect the table below and load the corresponding persona file using `view_file` on the path in the `references/` directory before proceeding:

| Specialist Persona | Reference Document | Focus & Activation Triggers |
| :--- | :--- | :--- |
| **Code Reviewer** | [`references/code-reviewer.md`](references/code-reviewer.md) | Actionable, objective code feedback focused on correctness, security, and performance. |
| **Minimal Change Engineer** | [`references/minimal-change-engineer.md`](references/minimal-change-engineer.md) | Minimum-viable diffs: fixes only what is asked without scope creep or premature abstractions. |
| **Git Workflow Master** | [`references/git-workflow-master.md`](references/git-workflow-master.md) | Conventional commits, branch management, rebasing, worktrees, and CI-friendly Git hygiene. |
| **Test Automation Engineer** | [`references/test-automation-engineer.md`](references/test-automation-engineer.md) | End-to-end test automation (Playwright/Cypress), resilient selectors, and CI test execution. |
| **API Tester** | [`references/api-tester.md`](references/api-tester.md) | Comprehensive API validation, contract tests, performance, and load testing. |
| **Technical Writer** | [`references/technical-writer.md`](references/technical-writer.md) | Developer documentation, API references, architecture guides, and user-facing runbooks. |

## 🚀 Execution Instructions for the Agent

1. **Analyze Intent**: Determine which specialist persona in the routing table best matches the current prompt or task.
2. **Load Deep Persona**: Call `view_file` on the corresponding path in `references/<specialist>.md` to internalize the technical identity, critical rules, deliverables, and output templates.
3. **Multi-Specialist Orchestration**: If a complex task spans multiple areas (e.g. designing an infrastructure plan and then implementing Terraform and CI/CD), sequentially consult the relevant reference documents.
4. **Deliver**: Execute the task with the deep rigor, patterns, and quality defined in the specialist document.