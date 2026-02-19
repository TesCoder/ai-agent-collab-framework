# Operator Mental Model (Human) — Single Page

## What this system is
A multi-agent “work factory” for improving a website without losing control.  
You (human) are the ultimate authority. Agent A is the orchestrator + QA gate. Agent B is the implementer. Agents C/D produce content + funnel specs (no code).

## The cast (who does what)
**Agent A — Strategy & QA (the traffic cop)**  
- Chooses next work, writes Work Packets, enforces constraints.  
- Reviews checkpoints and signs off.  
- Keeps work moving (anti-stall), but does not edit code.

**Agent B — Implementation (the hands)**  
- Edits code, runs commands, captures proof.  
- Must follow packet scope + diff-budget + checkpoints.  
- Uses non-3000 ports only.

**Agent C — Content/SEO (no code)**  
- Produces briefs/outlines/drafts in `content/`.  
- Must include schema + internal linking + CTA/event needs.

**Agent D — Funnel/Offers (no code)**  
- Produces funnel/offer specs in `funnel/` + `offers/`.  
- Must not “fill gaps” without dependencies being explicitly resolved.

**Agent 0 — Diagnostics only**  
- Helps debug specific issues. Cannot run projects/packets. No approvals.

## The only control surface you need (Work Packets + Checkpoints)
**A Work Packet is the “contract”**  
If it’s not in a Work Packet, it’s not authorized work.

A good Work Packet always includes:  
- `Implementer:` exact instance ID (e.g., B or B-hotfix)  
- `Resource targets:` file paths + shared components + runtime resources (ports)  
- `Diff-budget:` defaults or explicit restriction override (tier ceiling still applies)  
- Acceptance criteria: what “done” means  
- Verification steps: how to prove it  
- Reporting requirements: what evidence must be logged

**A Checkpoint is the “gate”**  
Agent B must stop and request review when: multi-file work, shared component/pattern work, first-time pattern, ~20–30% into a rollout, uncertainty.

At a checkpoint, you expect: what changed (files), proof snippet/diff, evidence bundle item(s), clear question or “request approval to continue.”  
Agent A replies with: approved (Yes/No), corrections, next authorized slice.

## Your daily operating loop (simple and repeatable)
- Pick the lane  
  - Normal: mainline packets go to B  
  - Hotfix lane: use B-hotfix (parallel corrective lane)  
  - Mainline should continue unless you explicitly pause it.
- Issue a Work Packet  
  - One packet per implementer at a time unless you explicitly want concurrency.
- Wait for checkpoint or completion evidence  
  - If multi-file/shared-component: you will see a checkpoint.  
  - If single-file tiny change: you’ll see completion + evidence.
- Approve or correct  
  - Approve only with proof/evidence.  
  - If evidence is missing: treat as not done.
- Close the slice  
  - Once closed, don’t reopen without new facts (regression/failed verification/new scope).

---
## Quick Reference Table — Roles After Initial Scan (Updated 12312025 & Canonical)

| Agent | Primary Role | Is analysis-only allowed after initial scan? | What “execution” **means now** | Hard rule that governs post-scan behavior |
| --- | --- | --- | --- | --- |
| **Agent A** (Strategy & QA) | Orchestration, Work Packets, QA | ❌ **No** (beyond readiness) | Issuing Work Packets, recording Checkpoint Reviews, updating Approval Ledger & reports | **May never end a cycle without enqueueing work, blocking explicitly, or declaring no remaining items** |
| **Agent B** (Implementation & Delivery) | Code & verification | ❌ **Never** | File diffs, builds, runtime verification, evidence bundles logged | **If a valid Work Packet exists, B must execute immediately — summaries are violations** |
| **Agent C** (Content & SEO) | Content discovery → production | ⚠️ **Only if NO executable Work Packet exists** | Briefs, outlines, drafts, logged with execution evidence | **If a C Work Packet exists and no `BLOCKING QUESTIONS — DO NOT PROCEED` header is present, C must execute in the same turn** |
| **Agent D** (Funnels & Offers) | Funnel & offer specs | ⚠️ **Only until dependencies are resolved** | Funnel/offer specs, CTA → form → event wiring artifacts | **Execution is mandatory once a D Work Packet exists unless the Dependency Gate triggers `BLOCKED`** |


---
## Concurrency mental model (avoid collisions)
Two packets may run in parallel only if resource targets do not overlap: no shared files, no shared components likely to be modified, no shared runtime resources (ports/build pipeline). If there’s any doubt: sequence by default.

---

## Port rule (important, easy)
- Port 3000 is reserved for you (Human).  
- Agents must use 3001+.  
- Agents should prefer port-scoped stopping over broad pkill.  
- Agents must never touch 3000 (start/stop/free).

## Evidence you should demand (minimum viable proof)
For code work (Agent B), expect at least:  
- A real snippet/diff from the modified file (Write & Verify), **plus** one evidence item relevant to the change (schema test output/snippet, analytics dataLayer proof, UI screenshot, build output if relevant).  
No evidence = not complete.

## Closure rules (keep things from dragging)
Once a slice is declared CLOSED, it stays closed unless: regression, failed verification, scope correction (“actually touched X”), higher-priority directive overrides. Avoid optional follow-ups after closure. Determinism wins.

## Escalation triggers (when you should step in)
Escalate / intervene if you see:  
- repeated missing evidence (“ghost work”),  
- repeated guardrail violations (scope creep, broad kills, touching forbidden files),  
- contradictory instructions between agents,  
- environment/tooling failures blocking execution across commands.

## What you say (operator shorthand)
- To start any agent’s real work: `Begin normal operation`  
- To keep a specific agent constrained: “Only execute packets whose Implementer matches your instance ID.”  
- To force sequencing: “Do not run concurrently; queue next packet only after prior is CLOSED.”  
- To pause intentionally: “STOP after checkpoint and wait.”  
- To clear a temporary pause (Agent B behavior): “proceed” / “continue” / “resume”

