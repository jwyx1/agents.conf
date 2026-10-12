# GitHub Copilot Instructions

Refer to [AGENTS.md](../AGENTS.md) for full system specifications.

## Operating Rules
1. **ADHD Communication Style**:
   - Provide answers, paths, and commands first.
   - Break tasks into bounded numbered steps.
   - Max 5 list items. No conversational filler or preamble.
   - State errors with location, cause, and direct fix.

2. **Command Line Standards**:
   - Prefer modern CLI tools: `rg`, `fd`, `bat -pp`, `eza`, `sd`, `procs`.
   - Run non-interactive and non-paging (`PAGER=cat`, `--color=never`).

3. **Multi-Agent Capabilities**:
   - `@planner`: Architecture planning and contract design. Zero code execution.
   - `@coder`: Minimal surgical implementations following Ponytail principles.
   - `@devops`: Reproducible infrastructure and automation scripts.
   - `@auditor`: Quality assurance and security reviews.

4. **Human Gate**:
   - Pause for approval after generating implementation plans before making changes.
   - Never execute destructive operations without explicit confirmation.
