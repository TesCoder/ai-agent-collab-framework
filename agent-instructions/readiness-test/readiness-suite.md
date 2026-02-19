# Readiness suite (safe checks)

Readiness tests are meant to verify you can activate agents **without writing files or starting servers**.

## How to run

In an agent’s chat (after loading the system prompt), send exactly:
- `Run readiness test`

Each system prompt defines what it checks in **PRE-ACTIVATION READINESS MODE**.

## What “ready” means (human checklist)

- [ ] You can open and read the active project’s `PROJECT_STATUS.md`
- [ ] The project has a reports template at `projects/<slug>/reports/_TEMPLATE_daily-update.md`
- [ ] You know where the codebase lives (`CODEBASE_PATH`) if implementation is enabled
- [ ] You understand the isolation rule: one agent per chat

## If readiness fails

- Treat the failure as an environment/setup issue (not a project failure).
- Fix the missing file/path/permissions issue, then rerun readiness.
