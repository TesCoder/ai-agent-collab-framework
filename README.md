# AI Agent Collaboration Framework

Coordinate multiple AI agents on real work **without losing control**.

This repo provides a **file-backed operating protocol** (plus a small linter + runnable demo) for running multiple AI chats in parallel while keeping scope, evidence, and approvals auditable.

- **Before**: work drifts, approvals are implicit, and you can’t tell what actually changed.
- **After**: every change is **explicitly authorized** (Work Packets), **checkpointed**, **evidenced**, and **closed** in an Approval Ledger.

**Example inputs**

- “Instrument CTA clicks and prove `window.dataLayer` events fire.”
- “Ship JSON-LD schema across templates and attach validator output.”
- “Draft 6 SEO briefs with acceptance criteria and handoff.”
- “Run a production verification sweep for canonical + OG tags.”

Live docs (GitHub Pages): [tescoder.github.io/ai-agent-collab-framework](https://tescoder.github.io/ai-agent-collab-framework/)

## Who it’s for

- Teams/operators coordinating **multiple AI chats** on the same initiative (engineering, content, SEO, growth)
- Anyone who needs **auditability**: explicit scope, evidence you can verify, and approvals you can point to

## Why this matters

Multi-agent work fails in predictable ways: hidden scope creep, “done” with no proof, and unclear ownership when something breaks. This framework turns “agent output” into an **execution pipeline** you can review like production work.

## What’s included

- **Work Packets**: explicit authorization, scope boundaries, acceptance criteria, verification steps (`AGENT_COLLAB_FRAMEWORK.md`)
- **Checkpoints + evidence**: QA gates that prevent “ghost work” and late-stage surprises
- **Auditable reporting model**: daily report + append-only implementer inbox updates (merge + closure)
- **Reference prompts**: system prompts for Agent A–D (plus a diagnostics-only Agent 0) (`agent-instructions/`)
- **Runnable demo + tooling**: example packet + a dependency-free linter (`examples/`, `tools/packetlint.py`)

## Demo (visual + end-to-end)

- Visual (architecture diagram): `docs/architecture.svg`

<img src="docs/architecture.svg" alt="Architecture diagram" width="900" />

- End-to-end (copy/paste walkthrough): `examples/end-to-end-demo/README.md`

## Quickstart (copy/paste)

### Requirements

- An **LLM chat/prompt interface that supports system prompts** (e.g. Cursor, ChatGPT, Claude, etc.)
- Python 3.x (stdlib only) for the included linter/tests

### 1) Verify this repo (1 command)

```bash
bash run.sh
```

### 2) Start using it (file-backed mode)

1. Copy the template project:
   - `projects/_template/` → `projects/<your-project-slug>/`

2. Follow the activation checklist:
   - `docs/activation-checklist.md`
   - (Optional) New-project checklist: `NEW_PROJECT_CHECKLIST.md`

3. In your LLM interface, open separate chats (isolation rule) and paste prompts:
   - **Agent A (Strategy/QA/orchestrator)**:
     - `agent-instructions/AgentA_SystemPrompt_Strategy-QA.md` (system prompt)
     - `agent-instructions/Agent_UserKickoff_Guide.md` (first user message; canonical kickoff for any agent)
   - **Implementers** (as needed):
     - Agent B: `agent-instructions/AgentB_SystemPrompt_Implementer-Delivery.md`
     - Agent C: `agent-instructions/AgentC_SystemPrompt_Content-SEO.md`
     - Agent D: `agent-instructions/AgentD_SystemPrompt_Funnel-Offers.md`

4. In implementer chats, send: `Begin normal operation` (or paste the kickoff guide above)

### 3) Try the included Work Packet demo (lint-only, safe)

```bash
python3 tools/packetlint.py examples/end-to-end-demo/work-packet.md
```

## How it works (3-step flow)

1) **Operator → Agent A**: Agent A writes a Work Packet (scope + acceptance criteria + verification) into today’s daily report.
2) **Implementer (B/C/D)**: executes only what’s authorized and logs evidence to an **append-only inbox** update.
3) **Agent A**: merges inbox → daily report, then records closure in the **Approval Ledger**.

**Artifacts you can inspect**

- Work Packet example: `examples/end-to-end-demo/work-packet.md`
- Implementer evidence update: `examples/end-to-end-demo/implementer-inbox-update.md`
- Merge + approval ledger example: `examples/end-to-end-demo/agent-a-merge-and-approval.md`

## System boundaries (what this is / isn’t)

- **This is**: a protocol + prompts + templates + minimal tooling you run inside your chat tool.
- **This is not**: a background “agent runtime” that autonomously executes code for you. Execution is gated by Work Packets, checkpoints, and evidence.

## Repository layout

- `AGENT_COLLAB_FRAMEWORK.md`: the core operating protocol (Work Packets, checkpoints, evidence, anti-stall rules)
- `agent-instructions/`: system prompts for Agents A–D (+ a diagnostics-only Agent 0)
- `policy/`: safety + folder isolation rules
- `docs/`: operator docs (activation, troubleshooting, diagrams)
- `projects/_template/`: a copyable project skeleton (create new projects by copying this)
- `examples/`: end-to-end examples you can copy/paste
- `tools/packetlint.py`: dependency-free Work Packet linter
- `tests/`: unit tests for the linter
- `run.sh`: one-command lint + test runner

## Production-minded guardrails

- **Isolation by default**: one agent per chat (`docs/activation-checklist.md`)
- **Explicit authorization**: implementers act only on Work Packets with an `Implementer: <ID>` line
- **Evidence-first workflow**: no completion claims without diffs/snippets/logs/screenshots (as applicable)
- **Safe write boundaries**: folder isolation policy (`policy/FOLDER_ISOLATION_POLICY.md`)

## Safety / what not to publish

- Don’t include secrets, PHI, private spreadsheets, or anything covered by NDAs in Work Packets, reports, or evidence artifacts.
- Prefer synthesized/redacted examples in `examples/`.

## Troubleshooting

See `docs/troubleshooting.md`.

## Contributing

See `CONTRIBUTING.md`.

## License

MIT (see `LICENSE`).

## Author

- `github.com/TesCoder`