# Project shared tools (template)

This folder is for **project-specific scripts** used by agents and humans.

## Suggested scripts (optional)

- `merge_inboxes.*`: merge `REPORTS_ROOT/inbox/` into today’s `REPORTS_ROOT/daily/` (Agent A)
- `packetlint.*`: validate Work Packet formatting (human/CI)

## Rule

If a Work Packet or system prompt references a script by path, make sure that path exists for the active project.
