## Work Packet: Publish-ready docs cleanup (demo)

- Source Doc & Section: `README.md` (repo root)
- Implementer: B
- Scope Class: DOCS_ONLY
- Approval Required?: NO
- Business Outcome: Make the repo self-contained and publish-ready (no broken links; clear quickstart).
- Code Targets (ONLY these files may be edited):
  - README.md
  - docs/activation-checklist.md
  - docs/troubleshooting.md

- Acceptance Criteria:
  1. README has a clear elevator pitch + quickstart.
  2. All README links resolve inside the repo.
  3. Docs are self-contained (no project-specific identifiers).

- Verification Steps:
  - Run: `python3 tools/packetlint.py examples/end-to-end-demo/work-packet.md`
  - Manually click README links (GitHub render) and confirm no 404s.

Open Questions (Non-Blocking)
- None.
