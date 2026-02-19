import unittest
from pathlib import Path
import sys


# Allow importing tools/packetlint.py without packaging the repo.
REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = REPO_ROOT / "tools"
sys.path.insert(0, str(TOOLS_DIR))

import packetlint  # noqa: E402


class TestPacketLint(unittest.TestCase):
    def test_demo_packet_has_no_fatal_issues(self):
        md = (REPO_ROOT / "examples" / "end-to-end-demo" / "work-packet.md").read_text(encoding="utf-8")
        issues = packetlint.lint_work_packet(md)
        fatal = [i for i in issues if "placeholder" not in i.message.lower()]
        self.assertEqual(fatal, [])

    def test_missing_implementer_is_error(self):
        md = "## Work Packet: Test\n\n- Scope Class: DOCS_ONLY\n"
        issues = packetlint.lint_work_packet(md)
        self.assertTrue(any("Implementer" in i.message for i in issues))

    def test_invalid_scope_class_is_error(self):
        md = "## Work Packet: Test\n\n- Implementer: B\n- Scope Class: NOT_A_SCOPE\n"
        issues = packetlint.lint_work_packet(md)
        self.assertTrue(any("Invalid Scope Class" in i.message for i in issues))


if __name__ == "__main__":
    unittest.main()

