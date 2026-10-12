# Claude Code Guidelines

Consulte [AGENTS.md](AGENTS.md) para la especificación completa y canónica de este workspace.

## Directivas Esenciales

1. **Estilo de salida (ADHD)**:
   - Respuesta / comando / diff primero. Sin preámbulos ni despedidas.
   - Pasos numerados con una sola acción acotada.
   - Máximo 5 elementos por lista.
   - Tiempo estimado concreto (ej: "30 segundos", "2 minutos").
   - Tras cualquier cambio, muestra qué funciona ahora.

2. **Tooling CLI Moderno**:
   - Sustituye built-ins por: `rg`, `fd`, `bat -pp`, `eza -1 -a` (o `fd -d 1 -l -H .`), `sd`, `procs`.
   - Evita paginadores (`PAGER=cat`) y suprime colores ANSI (`--color=never`).

3. **Router de Agentes**:
   - `@planner`: Solo diseño y planes en Markdown (**cero ejecución de código**). Requiere aprobación humana.
   - `@coder`: Código quirúrgico en Rust, TS, Go, Wasm, MCP. Aplica Ponytail (diff mínimo, stdlib, tests de ramas).
   - `@devops`: Manifiestos mínimos y reproducibles para K8s, Docker, CI/CD, Terraform.
   - `@auditor`: Quality gate con `ponytail-review` (Must fix / Should fix / Nice to have) + auditoría de seguridad Zero Trust.

4. **Reglas y Skills**:
   - Reglas maestras: [rules/](rules/)
   - Habilidades y referencias: [skills/](skills/)
