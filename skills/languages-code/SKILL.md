---
name: languages-code
description: Specialized polyglot engineering suite for Go, Rust, TypeScript, and modern web. Activates specialized sub-agents for Rust refactoring and ownership hardening, modern frontend/TypeScript development, Model Context Protocol (MCP) server development, and WebAssembly compilation.
---

# Polyglot Engineering (Go, Rust, TypeScript & Web)

Specialized polyglot engineering suite for Go, Rust, TypeScript, and modern web. Activates specialized sub-agents for Rust refactoring and ownership hardening, modern frontend/TypeScript development, Model Context Protocol (MCP) server development, and WebAssembly compilation.

## 🧭 Dynamic Specialist Routing Matrix

This master skill bundles specialized, production-ready engineering personas. Depending on the user's specific request or problem, you **MUST** inspect the table below and load the corresponding persona file using `view_file` on the path in the `references/` directory before proceeding:

| Specialist Persona | Reference Document | Focus & Activation Triggers |
| :--- | :--- | :--- |
| **Rust Refactoring Specialist** | [`references/rust-refactoring-specialist.md`](references/rust-refactoring-specialist.md) | Repository-scale Rust refactoring, ownership improvements, panic hardening, and Clippy fixes. |
| **Frontend Developer** | [`references/frontend-developer.md`](references/frontend-developer.md) | Modern TypeScript/JavaScript, React/Vue/component implementation, and web performance optimization. |
| **MCP Server Builder** | [`references/mcp-builder.md`](references/mcp-builder.md) | Model Context Protocol (MCP) servers, tool adapters, custom resources, and agent extensions. |
| **WebAssembly Engineer** | [`references/webassembly-engineer.md`](references/webassembly-engineer.md) | Compiling Rust/Go to Wasm, boundary marshalling, WASI runtimes, and near-native tuning. |

## 🚀 Execution Instructions for the Agent

1. **Analyze Intent**: Determine which specialist persona in the routing table best matches the current prompt or task.
2. **Load Deep Persona**: Call `view_file` on the corresponding path in `references/<specialist>.md` to internalize the technical identity, critical rules, deliverables, and output templates.
3. **Multi-Specialist Orchestration**: If a complex task spans multiple areas (e.g. designing an infrastructure plan and then implementing Terraform and CI/CD), sequentially consult the relevant reference documents.
4. **Deliver**: Execute the task with the deep rigor, patterns, and quality defined in the specialist document.