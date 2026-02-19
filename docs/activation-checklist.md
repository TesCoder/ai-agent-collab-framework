# Activation checklist (human operator)

This repo is a **multi-agent operating system** built around:
- **Isolation** (one agent per chat)
- **Work Packets** (explicit authorization)
- **Checkpoints + evidence** (QA gates)

Prereq: you’ll need an **LLM chat/prompt interface that supports system prompts** (e.g. Cursor, ChatGPT, Claude, etc.) so you can run separate chats for Agents A–D.

Use this checklist to start cleanly.

## 1) Create or pick a project

- If you already have a project folder under `projects/<project-slug>/`, open:
  - `projects/<project-slug>/PROJECT_STATUS.md`
  - `projects/<project-slug>/reports/_TEMPLATE_daily-update.md`
- If you need a new project, use `NEW_PROJECT_CHECKLIST.md` and copy the skeleton from `projects/_template/`.

## 2) Open chats (isolation rule)

- **Chat A**: Agent A (Strategy/QA)
- **Chat B**: Agent B (Implementer)
- **Chat C**: Agent C (Content/SEO) (optional)
- **Chat D**: Agent D (Funnel/Offers) (optional)

Hard rule: **never mix agents in one chat**.

## 3) Start with Agent A

In Chat A:
1) Paste `agent-instructions/AgentA_SystemPrompt_Strategy-QA.md` as the system prompt.
2) Paste `agent-instructions/Agent_UserKickoff_Guide.md` as the first user message (canonical kickoff for any agent).

Agent A will:
- create (or select) today’s daily report for the active project
- read `PROJECT_STATUS.md`
- issue Work Packets for B/C/D

## 4) Activate implementers using Work Packets

For each implementer lane that has a Work Packet:
- Open the correct agent chat (B/C/D).
- Paste that agent’s system prompt:
  - `agent-instructions/AgentB_SystemPrompt_Implementer-Delivery.md`
  - `agent-instructions/AgentC_SystemPrompt_Content-SEO.md`
  - `agent-instructions/AgentD_SystemPrompt_Funnel-Offers.md`
- Then send: `Begin normal operation` (or paste the kickoff guide above)
  - Implementers read their Work Packets from the project’s daily report.

Optional (chat-only mode):
- If you are not using file-backed reports, you may paste the Work Packet block directly into the chat instead.

## 5) Run the end-to-end demo (safe)

If you want to see the format end-to-end before doing real work:

- Read: `examples/end-to-end-demo/README.md`
- Run (one command): `python3 tools/packetlint.py examples/end-to-end-demo/work-packet.md`

## 6) If something feels “stuck”

- Use the `...` rescan token in the relevant agent chat to force a fresh read of today’s report (the prompts define exact behavior).
- If a missing file/link is the issue, search the repo for the path and either:
  - update the reference to the correct location, or
  - add a placeholder file under `docs/` or `shared-tools/` to keep the system self-contained.
