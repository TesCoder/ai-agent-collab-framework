# Project template

Copy this folder to create a new project:

1) Duplicate `projects/_template/` → `projects/<your-project-slug>/`
2) Update placeholders in:
   - `PROJECT_STATUS.md`
   - `README.md` (this file)
3) Ensure a daily reports template exists:
   - `REPORTS_ROOT/_TEMPLATE_daily-update.md`

## Canonical paths (convention)

- `PROJECT_ROOT`: `projects/<project-slug>`
- `REPORTS_ROOT`: `projects/<project-slug>/reports`
- `CODEBASE_PATH`: absolute path to the codebase repo (if implementation is enabled)

## What lives where

- `PROJECT_STATUS.md`: source of truth (priorities, constraints, verification checklist)
- `REPORTS_ROOT/daily/`: Agent A only (Work Packets, approvals, merges)
- `REPORTS_ROOT/inbox/`: implementers append-only updates (merged into daily by Agent A)
- `shared-tools/`: project-specific scripts + templates (optional)
