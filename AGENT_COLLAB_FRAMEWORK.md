# 🤖 Multi-Agent Collaboration Framework
This document describes how autonomous AI agents can coordinate work (strategy/QA, implementation, content, funnels) using project docs plus a separate application codebase.

---

## 0. Orientation Checklist
- Read `PROJECT_STATUS.md` completely before touching code.
- Skim `README.md` for repository structure and workflow reminders.
- Use `analysis/` docs for competitive context (strategy inputs).
- Use `implementation/` docs for copy/paste patterns (execution inputs).
- Tool catalog sweep (MANDATORY, project-agnostic):
  - At the start of every operational session, each agent MUST open the project tool catalog:
    - `${SHARED_TOOLS}/scripts/README.md`
  - Treat this file as the canonical “what tools exist + how to run them” index for the active project.
  - If `${SHARED_TOOLS}/scripts/README.md` is missing:
    - STOP and report: `BLOCKED: shared-tools/scripts/README.md not found for this project.`
  - Rule: Agents MUST NOT wait for the human to mention a script/tool by name if it is already documented in the tool catalog.

- Log every working session in `REPORTS_ROOT/` using the reporting template below.
- Review known execution-layer constraints in §12 (⚠️ Sandbox / Permissions) before diagnosing build or dev-server failures.

- Filesystem safety: Do NOT create directories by default. If a needed directory is missing, stop and ask for approval; only create it when explicitly authorized (e.g., “mkdir approved”) and only for the approved absolute path(s).
- REPORTS_ROOT write assertion: Before creating or modifying ANY report file, verify the absolute target path begins with REPORTS_ROOT exactly. If not, STOP, do not write or mkdir, and log BLOCKED. Agents should echo the resolved absolute report path internally before writing; mismatch = BLOCKED. Relative paths are not permitted.

### Daily reporting 

- Use `REPORTS_ROOT/daily/YYYY-MM-DD-update.md` as the shared daily log curated by Agent A.
- Agents B/C/D may jot progress in their own inbox files under `REPORTS_ROOT/inbox/Agent<AGENT_ID>_YYYY-MM-DD.md`; Agent A may merge as needed (no strict filename/marker enforcement).
- Before making status/approval claims, prefer a quick check of today’s daily report and any relevant inbox entries; if unclear, ask for confirmation instead of blocking.

### MKDIR Authorization (Work Packet Only)
- Default: Agents MUST NOT create directories.
- Only Agent A may authorize directory creation, and ONLY by writing an explicit MKDIR authorization block inside a Work Packet.
- MKDIR authorization MUST be:
  - explicit (no implied permission),
  - scoped to specific paths (absolute paths only),
  - limited to the current Work Packet (single-use).

- MKDIR authorization may NOT be used to create top-level directories.
- Creation of any top-level directory requires explicit human approval and may NOT be authorized by Agent A.
- Human approval must be given explicitly in-chat and may not be inferred from prior decisions.

**Definition — Top-level directory:**
A directory whose parent is a repository root or a first-order project root
(e.g., `projects/`, `reports/`, `content/`, `components/`, `pages/`).

Subdirectories within an existing, human-defined structure
(e.g., `<project_root>/reports/experiments/`)
are NOT considered top-level.

- Absence of an MKDIR AUTHORIZATION block means directory creation is forbidden.

**Required Work Packet block (verbatim):**
```text
MKDIR AUTHORIZATION:
- Approved: YES
- Allowed paths (absolute only):
  - <ABS_PATH_1>
  - <ABS_PATH_2>
- Purpose: <one sentence>
- Scope: Create listed directories only if missing; no other mkdir permitted.
```

### Agent C Watchdog (Session-Level Guardrail)
If an Agent C-owned Work Packet is active (i.e., `Implementer: C` exists in TODAY’s daily report and is not CLOSED/BLOCKED/EXHAUSTED):
- Agent C’s first operational response after freshness sweep MUST include:
  (a) the session micro-test evidence (per Agent C’s system prompt), AND
  (b) execution of one slice (or `PARTIAL:` / `BLOCKED:` with evidence).
- “Status-only” replies after acknowledging executable work are forbidden.
- If a prior turn ended with “next action is …” (or any equivalent next-step statement) and no execution evidence was produced, the next non-HOLD turn must begin with `EXECUTE:` or `PARTIAL:` (not recap).
- This rule applies even if the prior turn was informational, unless an explicit HOLD was issued in that same turn.

---

## 1. Role Definitions

| Agent | Focus | Primary Inputs | Core Outputs |
|-------|-------|----------------|--------------|
| **Agent A — Strategy & QA** | Translate business/SEO priorities into actionable work packets; validate finished work. | `PROJECT_STATUS.md` §§1–5, `analysis/*.md`, prior `REPORTS_ROOT/` updates. | Task briefs, acceptance criteria, QA sign-off notes, updates to `REPORTS_ROOT/daily/YYYY-MM-DD-update.md`. |
| **Agent B — Implementation & Delivery** | Ship code changes in Next.js repo following established patterns; run verifications. | `implementation/*.md`, codebase, briefs from Agent A. | PR-ready diffs, verification logs, implementation notes added to `REPORTS_ROOT/`. |
| **Agent C — Content & SEO Production** | Produce briefs, outlines, and drafts mapped to keyword clusters and audience/service hubs; ensure SEO compliance before handoff. | `analysis/*.md`, Comprehensive Plan, `content/` workspace, `kpi/events-dictionary_kpi.md`. | Briefs, outlines, drafts with on-page SEO checks and CTA targets logged in `REPORTS_ROOT/`. |
| **Agent D — Funnel & Offer Orchestration** | Design funnels (guides, webinars, quiz, consult), offer pages, and CTA → form → event wiring requirements. | Comprehensive Plan, `PROJECT_STATUS.md` §3, `funnel/`, `offers/`, `kpi/events-dictionary_kpi.md`. | Funnel specs, offer requirements, wiring checklists, and payload maps placed in `REPORTS_ROOT/` and relevant `funnel/`/`offers/` docs. |

> Only Agent A authors Work Packets; packets without an Implementer field are invalid.
> Agents B/C/D may not write to `PROJECT_STATUS.md` unless explicitly instructed by the maintainer.
> Agent A may update `PROJECT_STATUS.md` status/phase sections immediately when closing a Work Packet or milestone; other edits require maintainer approval. Agents B/C/D remain read-only.

- Lane D (Agent D) is non-code: it MUST NOT run dev servers or perform code edits. Any D packet must be docs/spec or production verification-only, per its system prompt.

All agents must keep changes additive and align with the verification checklist in `PROJECT_STATUS.md` §7.

Execution Gating Invariant — Questions

Across ALL agents and ALL Work Packets:

- ONLY a section titled exactly:
  “BLOCKING QUESTIONS — DO NOT PROCEED”
  may pause execution.

- Any other questions, uncertainties, or confirmations
  (including “open questions”, “questions needing confirmation”, or similar)
  are NON-BLOCKING by definition.

Agents are FORBIDDEN from inferring blockage from question wording.
If defaults are provided or allowed, execution MUST continue.

Any pause in execution caused by NON-BLOCKING questions
(including “open questions”, “questions needing confirmation”, or similar)
constitutes a PROTOCOL VIOLATION.

Required action:
- The agent MUST log the violation under “### Risks / Blockers” in the current day’s report.
- The log entry MUST explicitly state:
  “Execution paused due to non-blocking questions (protocol violation).”

- Questions asked outside a Work Packet (e.g., in chat) do NOT pause execution
  unless the active Work Packet itself contains
  “BLOCKING QUESTIONS — DO NOT PROCEED”.

### Primary-Work Non-Displacement Rule (ALL AGENTS)

Status relays, alignment scans (including `...`), and cross-agent awareness are SECONDARY.

Hard rule:
- Secondary reporting MUST NOT displace an agent’s primary deliverable execution.
- If `...` is invoked mid-deliverable:
  - Provide the minimal role-scoped response,
  - Then immediately resume primary work without waiting.
Cross-agent summaries require an explicit human request.

### Folder Governance & Documentation Destinations
- **`implementation/` — milestone snapshots.** Agent B adds new summary files only when a self-contained body of work finishes (e.g., CTA analytics rollout, schema coverage, new funnel). Use descriptive names like `implementation/2025-12-04-cta-analytics-upgrade.md` and include objective, files touched, implementation notes, verification steps, and observed impact. Existing files in `implementation/` are immutable references—never edit or delete them.
- **`REPORTS_ROOT/` — incremental activity log.** After each working block (even for small fixes), Agent B appends to `REPORTS_ROOT/daily/YYYY-MM-DD-update.md` covering tasks completed, files touched, issues/risks, and explicit review asks for Agent A. One file per day keeps the audit trail linear.
- **`content/` — briefs → outlines → drafts.** Agent C stores keyword clusters, content briefs, outlines, and drafts for articles, guides, webinars, and quiz flows under `content/articles`, `content/guides`, `content/webinars`, and `content/quiz`.
- **`funnel/` and `offers/` — funnel blueprints & offer specs.** Agent D keeps funnel blueprints (`funnel/webinar`, `funnel/guide-download`, `funnel/consult`) and offer requirements (`offers/essays-only`, `offers/comprehensive`, `offers/full-support`).
- **`kpi/` — analytics dictionary.** Shared source for event names, parameters, and naming conventions (CTA, form, webinar, guide, quiz, package events).
- **Never modify** `analysis/`, `implementation/` history files, `PROJECT_STATUS.md`, or `README.md` unless the maintainer explicitly assigns that work. Agent B focuses on new additive notes; Agent A double-checks placement.
- **Agent A’s oversight.** If Agent B lands a milestone summary inside `reports/`, Agent A instructs them to promote it into a dedicated `implementation/` file before sign-off.
- **`analysis/` — strategy & competitive context.**
  Used for:
  - market/competitor analysis
  - SEO and acquisition recommendations
  - positioning and differentiation inputs
  - roadmap rationale

- **Canonical Strategic Reference (project-scoped).**
  The file defined by `CANONICAL_STRATEGIC_REFERENCE` in `PROJECT_VARS.md`
  is the authoritative strategic source for:
  - service architecture
  - content clusters
  - offers & funnels
  - tracking/KPIs
  - differentiation themes

  Enforcement:
  - Agent A MUST consult this reference when selecting or prioritizing Work Packets.
  - Agent A MUST validate completed work against this reference during QA.
  - Agents C and D MUST align briefs, outlines, and funnel specs to it when applicable.


**Decision Rule for Agent B**

| Work Type | Destination |
|-----------|-------------|
| Site-wide CTA analytics instrumentation | `implementation/cta-events-upgrade.md` |
| Fixing a typo or updating a single page component | `REPORTS_ROOT/daily/YYYY-MM-DD-update.md` |
| Completing schema coverage across all service pages | `implementation/service-schema-phase-complete.md` |
| Adding breadcrumbs to one new page | `REPORTS_ROOT/daily/YYYY-MM-DD-update.md` |

If in doubt, ask: *“Is this work a durable deliverable or routine progress?”* Durable deliverables go to `implementation/`; everything else lives in `reports/`.

### Additional Responsibilities & Oversight
- **Agent A – Strategic Oversight.** Continuously validate structural SEO (schema, canonical, breadcrumbs), metadata completeness, CTA analytics consistency, scalability of patterns, and cross-page consistency. Capture optional roadmap ideas under “Strategic Insights” in the daily report when needed.
- **Agent B – Checkpoint Pauses.** Must halt work and request a checkpoint whenever a task spans multiple files, introduces or edits a shared pattern/component, implements a pattern for the first time, produces uncertain results, or after ~20–30% of a large rollout. Do not resume until Agent A explicitly approves.
- **Escalation expectation.** If checkpoint cycles stall or either agent spots the triggers documented in `Escalation.txt` (e.g., repeated structural failures, contradictory direction, material SEO risk), pause immediately and alert the human owner.

### Milestone-Summary Consolidation Rules
- **Trigger:** Any deliverable that required a checkpoint, touched multiple files/pages, or completed a roadmap milestone must be consolidated into `implementation/YYYY-MM-DD-<slug>.md` within 24 hours of completion.
- **Authoring flow:** Agent B drafts the consolidated summary by pulling the Work Packet, checkpoint notes, Evidence Bundle highlights, retrospective bullets/scores, and QA sign-off. Agent A reviews for accuracy before the milestone is considered done.
- **Content checklist:** Objective, scope, files touched, implementation highlights, verification artifacts (or links), checkpoint outcome, retrospective scores (see §7.2), lessons learned, and recommended next steps. This prevents daily logs from fragmenting and keeps long-lived history per milestone.

---

## 2. Collaboration Loop

| Step | Owner | Inputs | Output / Destination |
|------|-------|--------|----------------------|
| **0. Sync** | A, B, C, D | Latest `PROJECT_STATUS.md`, open `reports/` entries | Confirm active priorities (default: CTA analytics, sitemap build, raw `<Head>` audit; add content/funnel tasks when scheduled). |
| **1. Task Sourcing** | Agent A | `PROJECT_STATUS.md` §3, current project analysis/roadmap doc(s) | Select task, note its priority, success metrics, and dependencies. |
| **2. Work Packet Draft** | Agent A | Selected task + `analysis/` context + `implementation/` patterns | Fill the Work Packet Template (Section 3) and drop it into `REPORTS_ROOT/daily/YYYY-MM-DD-update.md` under “Briefs”. |
| **3. Checkpoint Review (NEW)** | Agent A ↔ Agent B/C/D | Work Packet + first 20–30% of execution | Agent B/C/D posts “Checkpoint Summary”; Agent A replies with “Checkpoint Review” before work continues. Mandatory for multi-file tasks or shared patterns. |
| **4. Build & Verify** | Agent B/C/D | Approved checkpoint + `implementation/QUICK_IMPLEMENTATION_GUIDE.md` | Complete work, run verification steps, attach artifacts (screenshots, Rich Results output). |
| **5. QA & Acceptance** | Agent A | Agent B/C/D verification notes, `PROJECT_STATUS.md` §7 checklist | QA results appended to same `reports/` entry; flag blockers back to Step 0 if needed. |
| **6. Close Out** | Agent B/C/D (primary) | Final diff, QA sign-off | Update Phase board inside `PROJECT_STATUS.md` §3 or leave comment for maintainer; note residual risks. |

---

## 3. Work Packet Template (Agent A → Agent B handoff)

Paste the following block into `REPORTS_ROOT/daily/YYYY-MM-DD-update.md` for each task:

```
## Work Packet: <Task Name>  (Priority: High/Medium/Low)
- Source Doc & Section: <e.g., PROJECT_STATUS.md §3.1 CTA Analytics>
- Implementer: <AGENT_INSTANCE_ID> (required; e.g., B, B-hotfix. If missing, packet is INVALID and not authorized for execution.)
- Scope Class: <DOCS_ONLY | VERIFICATION_ONLY | CODE_CHANGE>
- Approval Required?: <YES | NO>
- Closure rule:
  - If Scope Class == DOCS_ONLY AND Approval Required == NO:
    - Implementer MUST NOT request approval.
    - Implementer MUST end their update with: `Status: COMPLETE (docs-only) — No approval requested.`
    - Agent A MUST auto-review and log closure upon evidence (same operational cycle -- unless deferred by HOLD).
  - Evidence definition (DOCS_ONLY):
    - A direct link to the exact document section modified, OR
    - A pasted diff / quoted block of the added or changed text.
- Business Outcome: <1–2 sentences tying back to analysis insights>
- Code Targets (ONLY these files may be edited):
  - <exact paths>

- Explicitly Forbidden Files / Components:
  - Any file not listed above
  - All shared components unless explicitly listed
  - Examples (if applicable): components/SEOHead.js, layout shells, schema utilities

- Required Patterns: <SEOHead, SchemaScript, Breadcrumbs, FAQ, GTM events, etc.>
- Acceptance Criteria:
  1. ...
  2. ...
- Verification Steps:
  - Run ...
  - Validate ...
- RRT cadence (MUST specify one):
  - Option A (default): Per-template sampling + bounded retries + alternate evidence
  - Option B (strict): Per-page RRT evidence required for every listed URL
- If Option A is used, list:
  - Templates covered
  - Representative URL per template
  - Retry policy (attempts + timeout)
  - Alternate evidence bundle requirements
- Reporting: <fields Agent B must log (files touched, commands, screenshots)>
### Questions Classification (Execution Gating) — HARD RULE

Only ONE header can stop execution:

BLOCKING QUESTIONS — DO NOT PROCEED

- If (and only if) a Work Packet includes a subsection whose header is exactly:
  “BLOCKING QUESTIONS — DO NOT PROCEED”
  then the Implementer MUST STOP and wait for answers before continuing.

All other question lists are NON-BLOCKING by default:

Open Questions (Non-Blocking)

- Any questions listed under “Open Questions (Non-Blocking)” MUST:
  (a) include a proposed default, and
  (b) MUST NOT delay execution.
- The Implementer MUST proceed immediately using the proposed defaults and log the defaults/assumptions in today’s daily report.

ENFORCEMENT:
- If a packet contains questions but does NOT contain the exact header
  “BLOCKING QUESTIONS — DO NOT PROCEED”,
  those questions are automatically NON-BLOCKING and execution MUST continue.

```

Authoring Rule (Agent A):

- If any questions are listed in a Work Packet, they MUST be placed under one of the two approved headers:
  “Open Questions (Non-Blocking)” OR “BLOCKING QUESTIONS — DO NOT PROCEED”.
- Mixing question types or inventing new headers is forbidden.

Agent B replies inline under the same heading with:

```
### Implementation Notes
- Commits/Diffs: <summary>
- Commands Run: <npm install, npm run build, etc.>
- Validation Results: <Rich Results test, lint, manual QA>
- Follow-ups Needed: <if any>
```

---

## 4. Checkpoint Review (Mid-Task Oversight)

Checkpoints are mandatory whenever:
- A rollout spans multiple files/pages.
- A shared component or new pattern (SEOHead, SchemaScript, CTA tracking, etc.) is introduced or modified.
- Content clusters, briefs, or service/offer templates are being defined; Agent C checkpoints after the first cluster/outline.
- Funnel wiring (CTA → form → event) or new lead magnet/webinar/quiz flow is being set up; Agent D checkpoints after the first path is wired.
- Offer accuracy (pricing/tiers) needs validation before wider rollout.
- Approximately 20–30% of a large task is complete (first 2–3 pages, first batch of CTAs).
- Requirements are unclear or results feel uncertain.

Decision reminder (Agent C): if creating a guide or webinar, place the brief in `content/` and notify Agent D to open the matching funnel spec in `funnel/` before implementation begins.

Agent B pauses work and posts the following block inside the current daily report:

```
### Checkpoint Summary (Agent B)
- Work completed so far:
- Files modified:
- Patterns applied:
- Sample diffs / screenshots:
- Questions / uncertainties:
- Requesting approval to proceed.
```

Agent A responds inline:

```
### Checkpoint Review (Agent A)
- Review notes:
- Corrections required:
- Structural / SEO concerns:
- Approved to continue? Yes / No
```

Agent B must not continue until Agent A explicitly approves. If instructions conflict or checkpoints stall, defer to the escalation rules (Section 9).

> **Quickline rule:** Any task touching more than one page or editing shared patterns requires a checkpoint after the first few implementations.

### Waiting State Exclusivity Rule

At any moment, ONLY ONE of the following may be true:
- Implementer waiting on Reviewer approval
- Reviewer waiting on Implementer evidence

They may NOT coexist.

If evidence is posted:
→ Reviewer is active, Implementer is NOT waiting.
If evidence is missing:
→ Implementer is active, Reviewer is NOT waiting.

Any report stating mutual waiting is INVALID and must be corrected immediately.

---

## 5. Active Task Board (mirrors `PROJECT_STATUS.md` §3)

Use the active project's `PROJECT_STATUS.md` §3 to populate this table. The rows below are generic templates—replace them with the project's real tasks and references.

| Priority | Task | Agent A Responsibilities | Agent B Responsibilities | Key References |
|----------|------|-------------------------|--------------------------|----------------|
| High | CTA & conversion tracking | Define target CTAs and analytics payloads per the current strategy doc. | Instrument CTA/UI surfaces in the codebase; guard analytics calls; verify event firing. | `PROJECT_STATUS.md` §3, project analytics/quick-reference doc. |
| High | Sitemap & robots hygiene | Confirm sitemap scope, exclusions, and publish cadence; capture edge cases. | Ensure build outputs sitemap/robots, verify deployment behavior. | `PROJECT_STATUS.md` §3, project build/deploy notes. |
| High | Metadata / `<Head>` audit | Inventory legacy head/meta tags; define replacement order and required fields. | Implement shared head/meta component; verify canonical/OG/Twitter tags. | `PROJECT_STATUS.md` §3, implementation guide for the current codebase. |
| Medium | Content rollout | Outline topics from the current content plan/keyword clusters; specify schema needs. | Scaffold pages/posts, apply schema, add internal links and CTAs. | Project content plan (`analysis/`), implementation guide. |
| Medium | Internal linking architecture | Design related-link targets/data model per clusters or hubs. | Build/extend linking component and populate data per plan. | Project internal-linking plan, implementation guide. |
| Medium | Schema coverage | Maintain schema inventory; state required type per template/page. | Apply schema components or JSON-LD to new/updated pages; verify output. | Project schema guidelines, implementation guide. |

Update this table whenever priorities change and copy the latest version into the next `reports/` update when priorities shift.

---

## 6. Reference Map

Use the current project's equivalents for each reference below; update filenames as needed.

| Doc | Purpose for Agents |
|-----|--------------------|
| `PROJECT_STATUS.md` | Source of truth for status, priorities, patterns, verification checklist. |
| `analysis/` docs (current project) | Competitive/SEO insights, content plan, roadmap/backlog seeds, quick reference for CTA/funnel messaging. |
| `implementation/` docs (current project) | Patterns/paste-ready components, build/deploy notes, recent implementation status logs. |
| `reports/` | Living log of work packets, checkpoints, QA notes, strategic insights. |
| `Escalation.txt` | Human escalation triggers for Agents A & B. |

---

## 7. Reporting & QA Protocol

1. **File Naming:** `REPORTS_ROOT/daily/YYYY-MM-DD-update.md`. One file per working day; both agents append to the same entry.
2. **Sections per report file:**
   - `### Briefs` (Agent A)
   - `### Implementation Updates` (Agent B)
   - `### Checkpoint Summary` / `### Checkpoint Review` (as needed)
   - `### QA & Verification` (Agent A, referencing §7 checklist in `PROJECT_STATUS.md`)
   - `### Strategic Insights` (Agent A, optional)
   - `### Risks / Blockers` (either agent)

### Execution Evidence Flag (REQUIRED — ALL IMPLEMENTERS)
Any entry written under an Implementer’s update section (e.g., `### Implementation Updates (Agent C)`) MUST include this line:

- Execution evidence?: YES / NO

### No Intent Without Evidence (HARD — implementers)

Definition:
- “Intent without evidence” = any language implying work is being done (or will be done) without including an artifact in the SAME update.

When an implementer has authorized work (valid packet + not HOLD/STOP/WAIT):
- The update MUST include at least one Evidence Bundle item (§8) in the SAME entry, OR
- The update MUST be explicitly blocked:
  `Status: BLOCKED — <one concrete reason>.`

Forbidden phrases (non-exhaustive) unless paired with SAME-entry evidence:
- “executing”, “applying”, “proceeding”, “continuing”, “working on”, “will do”, “next I will”, “about to”

Required replacement styles (pick one, include evidence):
- `Completed <step>; evidence:` + (diff/snippet/log)
- `PARTIAL: <step done>; evidence:` + (diff/snippet/log) + `Remaining: <smallest next slice>`
- `Status: BLOCKED — <reason>.` + (evidence of blocker)

Violation handling:
- If an entry contains intent language without evidence, it is INVALID and MUST be moved to `### Risks / Blockers` with the explicit sentence:
  `Execution paused due to intent-without-evidence (protocol violation).`

Rules:
- If the entry includes any claim of next steps (e.g., “Next: …”, “next action …”, “proceed to …”, “no open blockers”), then `Execution evidence?:` MUST be `YES` and the entry MUST include at least one Evidence Bundle item (or a brief/draft snippet for Agent C).
- Entries that only restate plans/next steps while `Execution evidence?: NO` are INVALID and must be moved to `### Risks / Blockers` with the explicit sentence:
  “Execution paused due to status-only acknowledgment (protocol violation).”

### Status Line (REQUIRED — ALL IMPLEMENTERS)
Every timestamped entry under any `### Implementation Updates (Agent X)` section MUST include exactly one `Status:` line using ONE of the canonical forms below. (This requirement applies only to Implementation Updates and does not apply to Checkpoint Reviews or Closure Logs.)

Canonical Status forms (verbatim):
- `Status: COMPLETE (docs-only) — No approval requested.`
- `Status: COMPLETE — Approval requested.`  (use only if the Work Packet says Approval Required?: YES)
- `Status: NEEDS REVIEW — Waiting on Agent A to close.`
- `Status: BLOCKED — <one concrete reason>.`

Rules:
- Docs-only + no-approval work MUST use: `Status: COMPLETE (docs-only) — No approval requested.`
- “awaiting review / awaiting closure / pending review” phrasing is FORBIDDEN outside the canonical `Status:` line.
- If `Status: COMPLETE (docs-only) — No approval requested.` is present AND evidence is present, Agent A is responsible for same-cycle closure logging (no approval request required).

#### Approval Trigger Enforcement (HARD)

Any implementer update that requires Agent A review MUST do BOTH:

1) Include one of the exact approval trigger phrases (verbatim, case-insensitive):
   - `Requesting approval to proceed`
   - `Requesting approval to proceed? Yes`
   - `awaiting review`
   - `approval requested`

2) End with this exact status line:
   - `Status: NEEDS REVIEW — Waiting on Agent A to close.`

If an update does NOT require review, it MUST end with:
- `Status: COMPLETE (docs-only) — No approval requested.`

🚫 Forbidden:
- “pending review”
- “awaiting closure”
- “ready for review”
- any non-canonical variant

Enforcement:
- If ANY approval trigger phrase appears anywhere in TODAY’s report,
  Agent A MUST perform same-cycle Checkpoint Review and record the decision in today’s daily log.
- Absence of a canonical Status line is a protocol violation.

3. **Verification Requirements (from `PROJECT_STATUS.md` §7):**
   - Confirm `SEOHead` usage
   - Validate JSON-LD in Google Rich Results Test
   - Check breadcrumbs + FAQ render visually
   - Ensure CTA events appear in `window.dataLayer` (include new funnel events: `webinar_signup`, `guide_download`, `quiz_start`, `quiz_complete`, `package_cta_click`)
   - Regenerate sitemap post-build
   - Confirm required business contact info is present (if applicable)
4. **Hand-off Rule:** QA sign-off must cite which checklist items passed/failed and link to evidence (console logs, screenshots, Rich Results output).

### Daily reporting and approvals (lightweight)
- Use today’s `REPORTS_ROOT/daily/YYYY-MM-DD-update.md` as the shared log; check it before status/approval claims.
- Record approvals/notes in today’s daily log when evidence is present.
- Inbox files are optional scratch pads for implementer updates; Agent A may merge as needed, but authoritative state comes from today’s daily report.
- Status calls and overrides should reference today’s daily log (use the newest timestamped entries; treat “Status At A Glance” as mirror-only if present).

---

### 7.1 Post-Milestone Checkpoint Retrospective

Whenever a checkpoint-triggered or multi-file/multi-page deliverable finishes (e.g., CTA analytics rollout, schema batch, `<Head>` conversions), the working day’s report must include a “Checkpoint Retrospective” section directly after QA & Verification and before Strategic Insights. Minimum 3 bullets (ideally 5–10) covering:
- What went smoothly (patterns, briefs, naming, code structure).
- What caused pauses or rework (unclear criteria, missing patterns, ambiguity).
- Checkpoint effectiveness (did early review prevent downstream corrections?).
- Verification load (which evidence categories were easy/difficult).
- Brief clarity improvements and risks to monitor for next phases.

Agent B drafts the retrospective; Agent A can append notes during QA sign-off.

---

### 7.2 Retrospective Scoring Rubric

Score each category on a 1–5 scale (1 = blocker, 3 = acceptable, 5 = exemplary) and record the numbers in the daily report. These scores roll into milestone summaries.

| Category | 1 | 3 | 5 |
|----------|---|---|---|
| **Brief Clarity** | Requirements unclear / missing | Needed clarifications | Exceptionally clear, easily reusable |
| **Pattern Fit & Structural Integrity** | Schema/SEOHead errors or rework | Minor adjustments needed | Patterns applied flawlessly across files |
| **Checkpoint Effectiveness** | Missed checkpoint or issues found late | Caught some issues | Prevented all downstream rework |
| **Evidence Bundle Quality** | Required proof missing/incomplete | Meets minimum rule | Comprehensive, future-proof artifacts |
| **Delivery Confidence** | Open blockers remain | Ready with caveats | Fully verified, hand-off ready |

Agent B proposes the scores during the retrospective; Agent A confirms/updates them during QA. Persist these scores in the milestone consolidation file for trend tracking.

---

## 8. Evidence Bundle Requirements (Agent B/C/D)

Every checkpoint and final delivery must include at least one relevant proof from the list below.
Select the evidence types that match the task’s acceptance criteria.

1. **Schema Verification**
   - Rich Results Test output (URL or screenshot)
   - Inline JSON-LD snippet showing correct structure
2. **Analytics Verification**
   - Console output of `window.dataLayer.push` firing
   - Screenshot of GA DebugView (optional)
3. **SEOHead / Metadata**
   - Screenshot of the page `<head>` (OG/Twitter/canonical tags)
   - Dump of computed meta tags from devtools
4. **Code-Level Evidence**
   - Code diff snippet (before/after)
   - File list or import statements highlighting changes
5. **UI Rendering**
   - Screenshot of rendered UI (breadcrumbs, FAQs, CTAs, etc.)
   - Short video/GIF if interaction matters (optional)
6. **Next.js Build Outputs** *(when the task affects builds/sitemaps)*
   - `npm run build` log showing success
   - Generated `sitemap.xml` / `robots.txt` artifacts
7. **Content Evidence (Agent C)**
   - Brief → outline → draft progression with keyword cluster mapping and on-page SEO checklist (H1/H2s, meta, internal links, CTA targets).
   - Originality confirmation (plagiarism/AI score if available).
8. **Funnel Evidence (Agent D)**
   - CTA → form → event map with payloads matching `kpi/events-dictionary_kpi.md`.
   - Screenshot or link of the funnel page showing offer/CTA placement and successful form path.
9. **Other**
   - Any proof directly tied to the task’s acceptance criteria.

**Minimum rule:** include at least one schema check, one metadata/analytics check, or one code diff—whichever is most applicable—to avoid blind approvals.

Attach evidence directly under the relevant Work Packet, Checkpoint Summary, or QA section in the day’s report. Screenshots should be embedded inline (Markdown image or link to `reports/assets/`), and code diffs should be fenced in code blocks for readability.

---

## 9. Knowledge Injection Tips

- When defining new funnels or content, pull messaging cues from the current project's quick-reference/strategy doc (CTA language, trust signals).
- For expansion topics, use competitor clusters or topic hubs from the current project's analysis/roadmap doc.
- Tie every work packet to expected impact metrics listed in `PROJECT_STATUS.md` §8 to prioritize objectively.

---

## 10. Escalation Criteria

- **Agent A escalations:** If checkpoints repeatedly fail, structural SEO regresses, or requirements conflict, pause the task and alert the human owner.
- **Agent B escalations:** Escalate when Agent A signs off on structural errors, provides contradictory or non-actionable direction, blocks progress without justification, misunderstands significant technical issues, or dismisses SEO/analytics risks. After two failed clarification attempts, stop and escalate.
- **Rule:** Once any trigger from `Escalation.txt` fires, halt work immediately and wait for the human owner’s guidance before resuming.

---

## 11. Ready-Made Prompts for Agents

**Agent A Prompt Starter**
```
Review PROJECT_STATUS.md §3 and the current project's analysis/roadmap doc(s).
Produce a Work Packet using the template in AGENT_COLLAB_FRAMEWORK.md §3 for <task>.
State schema requirements, CTA analytics expectations, checkpoint trigger(s), and verification checklist items. If the work is a milestone, remind Agent B to plan the retrospective scores and implementation summary.
```

**Agent B Prompt Starter**
```
Open the application codebase at CODEBASE_PATH and execute the Work Packet titled "<task>".
Pause after the first checkpoint slice (~20–30% of work), post the Checkpoint Summary, and wait for approval.
Use implementation/QUICK_IMPLEMENTATION_GUIDE.md for patterns.
Return diffs, commands, Rich Results + dataLayer verification notes, final QA evidence, retrospective scores, and (if applicable) the consolidated implementation summary file.
```

---

## 12. AI-Specific Guardrails

### 12.1 Non-Destructive Rule (Agent B)
- Do not delete, rename, or move any file/directory. Only do so when a Work Packet explicitly says “delete <path>” or “rename <old> → <new>”.
- Modify only the files called out in the Work Packet (plus associated tests if needed). If another file needs changes, stop, log it under “Follow-ups Needed,” and wait for Agent A to update the brief.

### Unauthorized File Touch — Automatic BLOCKED

If Agent B edits any file that is NOT listed in the active Work Packet’s
“Code Targets” section:

- The slice is automatically INVALID.
- The correct state is BLOCKED.
- Required action:
  - Revert the unauthorized file immediately, OR
  - Obtain explicit written authorization via packet revision.

Intent, benefit, or correctness are irrelevant.
Scope violation overrides technical merit.

### 12.2 Write & Verify Protocol (Agent B)
For every edit:
1. Apply the change.
2. Immediately reopen the file.
3. Paste the exact lines added/changed or a before/after diff snippet into the daily report.
4. If the actual file content differs from the intended change, treat the task as failed, log it under “Risks / Blockers,” and do not mark the work complete.

Agent B may not declare a task done without attaching at least one relevant Evidence Bundle artifact (§8).

### 12.3 Session Micro-Test (Agent B)
At the start of each session:
1. Append `YYYY-MM-DD HH:MM (local tz) – Agent B session start.` to `logs/AGENTB_Implementer_Log.md`.
2. Append `YYYY-MM-DD – Micro-test write OK.` to the agent’s canonical microtest file
(as defined in the agent’s system prompt; under `REPORTS_ROOT/microtests/`).
3. Reopen both files and append the last three lines of each into:
   `REPORTS_ROOT/microtests/ZZZ-agent-b-microtest-proof.md` (or `ZZZ-agent-<AGENT_INSTANCE_ID>-microtest-proof.md` for suffixed instances).
   Do NOT place micro-test proof in inbox or the daily report.

If any step fails, Agent B must stop, note it under “Risks / Blockers,” and request help before touching other files.

### 12.4 Reviewer Restrictions (Agent A)
- Agent A must not write to repository files; it only reviews and updates reports.
- Agent A must not sign off QA unless each claimed change includes a diff/snippet and at least one Evidence Bundle item.
- For multi-file or shared-pattern tasks, Agent A should spot-check at least 2–3 of the files Agent B reports as changed.

### 12.5 Pattern Scope (Agent B)
- Use only patterns documented in `implementation/QUICK_IMPLEMENTATION_GUIDE.md` or explicitly defined in the Work Packet. Creating new schema/pattern structures requires Agent A to define them first.

### SHARED COMPONENT SCOPE LOCK (HARD RULE)
Definition — Shared Component:
Any component imported by more than one page, layout, or route group
(e.g., SEOHead, layout shells, schema utilities, CTA primitives).

Rules:
- Agent B MUST NOT edit any shared component unless ALL of the following are true:
  1) The Work Packet explicitly lists the shared component file path under “Code Targets”, AND

- If a solution appears to “require” touching a shared component but the packet does not authorize it:
  → STOP immediately.
  → Do NOT implement a workaround.
  → Log under “Follow-ups Needed” and request packet revision.

Invariant:
Perceived necessity does NOT imply permission.
Silence means NO.

### 12.6 Auto-Retros Trigger
- Whenever a checkpoint-triggered or multi-file task concludes, Agent B must fill the “Checkpoint Retrospective” and “Retrospective Scores” sections before starting new work. Agent A should remind Agent B of this requirement when assigning milestone-scale tasks.

---
## 13. Shorthand Command Alias — “...” (CANONICAL)

The token `...` means:

> “Re-open TODAY’S daily report fresh and respond strictly according to what is written there — but ONLY within the agent’s role scope unless the human explicitly requests a cross-agent summary.”

### Fresh-Read Proof (MANDATORY)
Any response to `...` MUST include a minimal verbatim quote from the reopened daily report:

Fresh-read proof:
- File: REPORTS_ROOT/daily/YYYY-MM-DD-update.md (or the project’s equivalent authoritative daily path)
- Section scanned: <e.g., ### Briefs (Agent A)>
- Verbatim quote: <at least one exact line that includes the timestamp you are relying on>

Enforcement:
- If the agent cannot provide the verbatim quote, it MUST respond ONLY with:
  BLOCKED: Unable to re-open and quote authoritative daily report lines for “...”.
- Any “...” response without Fresh-read proof is a protocol violation.

Rules (ALL AGENTS — HARD):

- `...` ALWAYS resolves to TODAY’S daily report.
- If the agent initially opens a non-today file:
  → It MUST discard all observations from that file,
  → Re-open TODAY’S file fresh,
  → Then answer only from TODAY’S file.

- If the human corrects the date (e.g., “today is the 29th”):
  → The agent MUST re-open the corrected date’s daily report fresh,
    even if another daily file was opened moments earlier.

Failure to re-open the correct date after a correction is a protocol violation.

### “No newer entries” Wording Constraint (HARD)
When responding to `...`, the agent MUST NOT state or imply that the daily report has “no newer entries after <timestamp>” unless the scan included:
- `### Checkpoint Summary`
- `### Checkpoint Review`
AND (if Active-Packet Override applies) the relevant implementer `### Implementation Updates` sections.

If the scan is limited to a subset of sections, the agent MUST use this exact phrasing:
- “No newer entries after <timestamp> **in the sections scanned above** (refreshed just now). Other sections may contain newer entries.”

Precedence Note:
If Agent A has any active or queued Work Packets, the Active-Packet Override
supersedes role-scoped minimization for `...` responses.

### 13.1 Role-Scoped Scan (DEFAULT)

Unless the human explicitly asks for a cross-agent status roundup (examples: “summarize everyone,” “what’s Agent B doing,” “full project state”),
the agent MUST scan and report ONLY:

- (Always) the authoritative date assertion + daily report path
- (Always) the agent’s OWN role-relevant sections
- (Optionally) ONE-LINE pointer if other-agent updates exist (no details)

#### Active-Packet Override (HARD)
If the requesting agent (especially Agent A) has issued or currently has **any active or queued Work Packets** to implementers (B/C/D or variants),
then `...` MUST ALSO scan the implementers’ update sections for those implementers and surface the newest timestamp(s), even if a cross-agent roundup was not requested.

Definition — Active or Queued Work Packet:
Any Work Packet logged in TODAY’S daily report that has not been explicitly marked
CLOSED, BLOCKED, or EXHAUSTED in today’s daily report (Checkpoint Review).

Missing Implementer Section Rule (HARD)
If Active-Packet Override applies AND an expected implementer update section
does not exist in the daily report, the agent MUST state:
“Implementer update section not present; cannot assert global freshness.”

Agents MUST NOT paraphrase other agents’ work under `...`; only point to section + timestamp unless explicitly requested.

- Implementer scan targets when Active-Packet Override is triggered:
  - `### Implementation Updates (Agent B)` (or the implementer’s equivalent section label)
  - `### Implementation Updates (Agent C)` (or the implementer’s equivalent section label)
  - `### Implementation Updates (Agent D)` (or the implementer’s equivalent section label)

Rules:
- Do NOT summarize other agents’ work unless explicitly requested.
- DO surface: section name + exact timestamp + one-line “impact on active packet” note if it affects execution gating.
- The phrase “No newer entries after <timestamp>” MUST only be used if the scan covered ALL required sections under this override.

Role scope (minimum scan targets by agent):
- Agent A (Strategy/QA):
  1) `### Checkpoint Summary`
  2) `### Checkpoint Review`
  3) `### Briefs (Agent A)` (for next packet issuance)
  4) (If Active-Packet Override triggered) relevant implementer `### Implementation Updates` sections

- Agent B (Implementation):
  1) `### Briefs (Agent A)` (Work Packets with matching Implementer)
  2) `### Checkpoint Review (Agent A)`
  3) `### Implementation Updates (Agent <AGENT_INSTANCE_ID>)` (self; exact instance match)

- Agent C (Content/SEO):
  1) `### Briefs (Agent A)` (Work Packets with Implementer matching Agent C instance)
  2) `### Content Evidence (Agent C)` if present
  3) `### Risks / Blockers` ONLY for items explicitly tagged Agent C or content dependencies
  4) `### Implementation Updates (Agent <AGENT_INSTANCE_ID>)` (self; exact instance match)

- Agent D (Funnel/Offers):
  1) `### Briefs (Agent A)` (Work Packets with Implementer matching Agent D instance)
  2) `### Funnel Evidence (Agent D)` if present
  3) `### Risks / Blockers` ONLY for items explicitly tagged Agent D or funnel dependencies
  4) `### Implementation Updates (Agent <AGENT_INSTANCE_ID>)` (self; exact instance match)

### 13.2 Cross-Agent Roundup (ONLY IF ASKED)

If (and only if) the human explicitly requests cross-agent status,
the agent MAY additionally scan:
- `### Implementation Updates`

Even then:
- Do NOT re-state other agents’ evidence bundles unless explicitly asked to review/QA.
- Prefer pointing to the section + latest timestamp rather than summarizing.

Response requirements (ALL uses of `...`):
- Cite file path.
- Cite section name(s) that were scanned (per role scope).
- Cite exact timestamp(s) seen.
- If nothing new exists, explicitly state:
  “No newer entries after <timestamp> (refreshed just now).”


If the agent cannot perform the re-open:
→ Respond ONLY with `BLOCKED: Unable to re-open authoritative file.`

---

By following this framework, four autonomous agents (A: Strategy/QA, B: Implementation, C: Content/SEO, D: Funnel/Offers) can operate in parallel while staying aligned with the authoritative materials already in this folder.

