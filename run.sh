#!/usr/bin/env bash
set -euo pipefail

echo "[1/2] Lint demo Work Packet"
python3 tools/packetlint.py examples/end-to-end-demo/work-packet.md

echo "[2/2] Run unit tests"
python3 -m unittest discover -s tests -p "test_*.py"

echo "OK"

