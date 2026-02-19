# New Project Checklist (multi-agent)

## 1. Project Identity & Scope (REQUIRED)
Confirm these before any agent begins work:
- [ ] PROJECT_NAME chosen (human-readable; e.g., BrandName)
- [ ] PROJECT_SLUG chosen (lowercase, kebab-case; e.g., brand-name)
- [ ] Diagnostic vs Implementation mode decided:
  - [ ] Diagnostics-only (read-only)
  - [ ] Full implementation (code edits allowed)

## 2. Canonical Paths (SET ONCE)
Declare these values explicitly at kickoff (manual config or kickoff prompt):
```
PROJECT_NAME   = <PROJECT_NAME>
PROJECT_ROOT   = projects/<project-slug>
REPORTS_ROOT   = projects/<project-slug>/reports
CODEBASE_PATH  = ~/Documents/GitHub/<codebase>  # diagnostics may reference, not edit
SHARED_TOOLS   = projects/<project-slug>/shared-tools
```
Checklist:
- [ ] Paths use the same project slug everywhere
- [ ] No agent hardcodes a project name outside these variables
- [ ] Diagnostics agents are explicitly marked read-only

## 3. Project Skeleton (FILES & DIRECTORIES)
Create by copying `projects/_template/` and renaming it to `projects/<project-slug>/`.

### Required files
- [ ] PROJECT_ROOT/README.md
- [ ] PROJECT_ROOT/PROJECT_STATUS.md

### Reports
- [ ] REPORTS_ROOT/_TEMPLATE_daily-update.md
- [ ] REPORTS_ROOT/daily/
- [ ] REPORTS_ROOT/audits/
- [ ] REPORTS_ROOT/experiments/
- [ ] REPORTS_ROOT/vendor/
- [ ] REPORTS_ROOT/assets/

### Logs
- [ ] PROJECT_ROOT/logs/
- [ ] PROJECT_ROOT/logs/local/ (dev / environment notes)

### Work coordination
- [ ] PROJECT_ROOT/work-packets/incoming/
- [ ] PROJECT_ROOT/work-packets/active/
- [ ] PROJECT_ROOT/work-packets/done/

### Project content (create only if applicable)
- [ ] PROJECT_ROOT/analysis/
- [ ] PROJECT_ROOT/implementation/
- [ ] PROJECT_ROOT/content/

## 4. Agent Configuration Check
Confirm before activating agents:
- [ ] Agent 0 (Diagnostics) — read-only; no project initiation; no repo edits
- [ ] Agent A (Strategy / QA) — can write to reports only; owns Work Packets and approvals
- [ ] Agent B (Implementation) — owns CODEBASE_PATH; no report edits outside evidence sections
- [ ] Agent C / D (Content / Funnel) — write only within PROJECT_ROOT/content|funnel|offers

## 5. Reporting Discipline (NON-NEGOTIABLE)
- [ ] Daily reports are immutable after date rollover
- [ ] All execution authority lives in today’s daily report
- [ ] Status summaries are non-authoritative
- [ ] Approvals live only in:
  - Approval Ledger
  - Checkpoint Review

## 6. Diagnostics Safety Checks
If diagnostics are enabled:
- [ ] CODEBASE_PATH labeled “reference only”
- [ ] No agent claims to have edited code unless explicitly authorized
- [ ] No Work Packets issued by diagnostic agents
- [ ] Observations logged as recommendations, not actions

## 7. First-Day Readiness Test
Before real work begins:
- [ ] Daily report exists for today
- [ ] All agents confirm correct paths
- [ ] One dry-run diagnostic question answered without edits
- [ ] Human confirms: “Begin normal operation”

## 8. Drift Prevention (ONGOING)
- [ ] Do not rename project slug midstream
- [ ] Do not duplicate paths with different casing
- [ ] Do not move reports into code repos
- [ ] Do not let agents infer missing variables

## Definition of “Project Ready”
A project is considered READY when:
- [ ] All checklist items above are checked
- [ ] At least one daily report exists
- [ ] Agent roles are unambiguous
- [ ] Diagnostic vs implementation authority is explicit
