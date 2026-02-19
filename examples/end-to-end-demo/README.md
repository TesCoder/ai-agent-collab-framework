# End-to-end demo (Work Packet → evidence → approval)

This demo is intentionally small. It shows the **shape** of the workflow:

1) **Agent A** issues a Work Packet (authorization).
2) **Implementer** executes and logs **evidence** (append-only inbox update).
3) **Agent A** merges inbox → daily report and records approval/closure.

## Files in this folder

- `work-packet.md`: an example Work Packet (what “authorized work” looks like)
- `implementer-inbox-update.md`: an example implementer update with evidence
- `agent-a-merge-and-approval.md`: an example merge + approval ledger entry

## One-command lint (safe)

From the repo root:

```bash
python3 tools/packetlint.py examples/end-to-end-demo/work-packet.md
```

If you want to build your own packet, copy `work-packet.md` and replace the target files, acceptance criteria, and verification steps.
