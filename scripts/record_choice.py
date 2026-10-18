#!/usr/bin/env python3
"""Record the chosen effort level so the next session can offer it as default."""
import json
import sys
from pathlib import Path

STATE_FILE = Path.home() / ".claude" / "effort-gate-state.json"
VALID = {"low", "medium", "high", "xhigh", "max"}

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in VALID:
        print(f"usage: record_choice.py <{'|'.join(sorted(VALID))}>", file=sys.stderr)
        sys.exit(2)
    STATE_FILE.write_text(json.dumps({"last_effort": sys.argv[1]}, indent=2) + "\n")
    print(json.dumps({"recorded": sys.argv[1]}))

if __name__ == "__main__":
    main()
