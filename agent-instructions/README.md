# Agent instructions (how to activate)

This folder contains **system prompts** for:
- Agent A — Strategy & QA (orchestrator)
- Agent B — Implementation & Delivery
- Agent C — Content & SEO
- Agent D — Funnel & Offers
- Agent 0 — ad-hoc diagnostics (read-only helper)

Hard rule: **one agent per chat** (never mix prompts).

## Canonical operating mode (recommended)

This system is designed to be **file-backed**:
- Agent A writes Work Packets into today’s daily report under the active project.
- Implementers read the daily report and log work to their inbox files.
- Agent A merges inbox → daily and records approvals.

The protocol lives in `../AGENT_COLLAB_FRAMEWORK.md`.

## Activation order (human operator)

### 1) Agent A (orchestrator) — start first

In a new chat:
1) Paste `AgentA_SystemPrompt_Strategy-QA.md` as the system prompt.
2) Paste `Agent_UserKickoff_Guide.md` as the first user message (canonical kickoff for any agent).

### 2) Implementers (B/C/D) — only after Agent A issues Work Packets

For each implementer, open a new chat and paste the matching system prompt:
- Agent B → `AgentB_SystemPrompt_Implementer-Delivery.md`
- Agent C → `AgentC_SystemPrompt_Content-SEO.md`
- Agent D → `AgentD_SystemPrompt_Funnel-Offers.md`

Then send: `Begin normal operation`  
(Or paste `Agent_UserKickoff_Guide.md` as the first user message.)  
(Implementers will read their Work Packets from the project’s daily report.)

## Readiness test (optional, safe)

In any agent chat (after loading the system prompt), send exactly:
- `Run readiness test`

Readiness mode is non-destructive (no writes).

## Related docs

- Activation checklist: `../docs/activation-checklist.md`
- Folder safety policy: `../policy/FOLDER_ISOLATION_POLICY.md`
- Readiness suite: `readiness-test/readiness-suite.md`
