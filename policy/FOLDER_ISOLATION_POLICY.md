# Folder isolation policy

_Last updated: Feb 17, 2026_

This policy defines **which folders autonomous agents may read/write** when using this repo in **file-backed mode** (Work Packets + reports on disk).

Goal: keep the system safe, auditable, and resistant to prompt drift.

---

# 1) Purpose

- Prevent agents from deleting, renaming, or corrupting strategic files  
- Ensure all agent actions are **additive only**  
- Preserve long-term institutional knowledge  
- Maintain safe execution boundaries  
- Protect prompts and system instructions from drift  

---

# 2) Access matrix (canonical)

| Folder / File | Agent A (Strategy/QA) | Implementers (B/C/D) | Description |
|---------------|----------------------|----------------------|-------------|
| `AGENT_COLLAB_FRAMEWORK.md` | Read only | Read only | Core workflow rules (publishable, protected). |
| `agent-instructions/` | Read only | Read only | System prompts (publishable, protected). |
| `policy/` | Read only | Read only | Guardrails and policies (protected). |
| `README.md` | Read only | Read only | Repo metadata (protected). |
| `projects/<slug>/PROJECT_STATUS.md` | Read only* | Read only | Project source of truth. (*Maintainer-controlled edits only.) |
| `projects/<slug>/analysis/` | Read only | Read only | Strategy/context docs; immutable. |
| `projects/<slug>/implementation/` | Read only | Read only | Milestones/patterns; immutable references. |
| `projects/<slug>/reports/daily/` | **Write** | No write | Daily report (Agent A only). |
| `projects/<slug>/reports/inbox/` | Read | **Write (append-only)** | Implementer updates (merged by Agent A). |
| `projects/<slug>/reports/assets/` | Write | Write | Evidence artifacts (screenshots, manifests). |
| `projects/<slug>/reports/microtests/` | Read | Write | Micro-test logs/proof. |
| `projects/<slug>/logs/` | Read | Write | Session logs (timestamps, env notes). |
| `CODEBASE_PATH` (external code repo) | No write | **Write to explicit Work Packet targets only** | Implementers edit only files named in Work Packets. |

`PROJECT_STATUS.md` editability: maintainer-controlled. If you allow Agent A to edit it, scope that permission explicitly (e.g., “status/phase section only”).

---

# 3) Restricted paths (no write)

Protected (repo root):
- `AGENT_COLLAB_FRAMEWORK.md`
- `agent-instructions/`
- `policy/`
- `README.md`

Protected (per project):
- `projects/<slug>/analysis/`
- `projects/<slug>/implementation/`
- `projects/<slug>/PROJECT_STATUS.md` (unless maintainer explicitly permits edits)

Agents may **read but never write** to these paths.

---

# 4) Agent A permissions

- **READ-ONLY**: protected docs + project strategy/pattern references  
- **WRITE**: `projects/<slug>/reports/daily/YYYY-MM-DD-update.md` (briefs, merges, approvals, QA)  
- **NEVER** modify repo code or protected files

---

# 5) Implementer permissions (Agent B/C/D)

### Implementers can write ONLY to:
- `projects/<slug>/reports/inbox/Agent<AGENT_INSTANCE_ID>_YYYY-MM-DD.md` (append-only)
- `projects/<slug>/reports/assets/` (evidence artifacts)
- `projects/<slug>/reports/microtests/` (micro-test logs/proof)
- `projects/<slug>/logs/` (session logs)
- Specific code files named in Work Packets (in the external `CODEBASE_PATH`)

### Implementers are forbidden from:
- Deleting or renaming files  
- Editing protected docs (`agent-instructions/`, `AGENT_COLLAB_FRAMEWORK.md`, `README.md`)  
- Modifying patterns without Agent A approval  

---

# 6) Session micro-test (implementers)

Before any real work, implementers should write a tiny, safe proof entry to:
- `projects/<slug>/logs/`
- `projects/<slug>/reports/microtests/`

(Exact filenames vary by agent instance; follow the system prompt.)

1. Append session timestamp to `PROJECT_ROOT/logs/AGENTB_Implementer_Log.md`  
2. Append micro-test entry to `REPORTS_ROOT/microtests/ZZZ-agent-b-microtest.md` (or `ZZZ-agent-<AGENT_INSTANCE_ID>-microtest.md` for suffixed instances)  
3. Reopen both files; capture the last 3 lines of each.  
4. Append proof to `REPORTS_ROOT/microtests/ZZZ-agent-b-microtest-proof.md` (or `ZZZ-agent-<AGENT_INSTANCE_ID>-microtest-proof.md`), containing those last 3 lines.  

If micro-test fails → stop work.

---

# 7) Write & verify protocol (implementers)

For EVERY file edit:

1. Write change  
2. Reopen file  
3. Paste proof (changed lines or diff) in the inbox update  
4. Attach required Evidence Bundle  

If mismatch → log blockage & stop.

---

# 8) Summary

This policy ensures:

- Safe autonomous operation  
- Zero destructive actions  
- Preservation of strategic docs  
- Clear boundaries for each agent  
- Reproducible multi-agent execution  

This repo stores the policy at `policy/FOLDER_ISOLATION_POLICY.md`.

If you prefer each project to be self-contained, you can copy this policy into:
- `projects/<slug>/FOLDER_ISOLATION_POLICY.md`
