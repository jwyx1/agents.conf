# Projects Directory Layout & Workflow Rules

When creating, organizing, saving, planning, or exporting files and repositories in `~/Projects/` (or `$PROJECTS_DIR`), strictly adhere to the Multi-Origin Workspace architecture:

## 1. Directory Structure
- `~/Projects/drafts/`:
  All preliminary thinking, research, technology comparisons, blueprints, RFCs, and markdown (`.md`) planning documents before software development begins.
- `~/Projects/personal/`:
  All original, user-created Git repositories and active development projects (e.g., `my-service`, `cli-tool`).
- `~/Projects/github.com/<org>/<repo>/`:
  All cloned third-party or upstream open-source repositories.

## 2. Project Lifecycle
1. **Ideation & Research:** Save new research, notes, and concept files directly into `~/Projects/drafts/<topic>.md`.
2. **Project Incubation:** When graduating an idea into an active project, initialize the new repository inside `~/Projects/personal/<project-name>/` and link the draft as the project's `README.md` or `docs/RFC.md`.
3. **Editor Default:** Open all code, configuration, and markdown files using VS Code (`code`).
