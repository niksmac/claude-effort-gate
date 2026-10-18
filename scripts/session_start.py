#!/usr/bin/env python3
"""SessionStart hook: set the session effort level before other work."""
import json
import os
import select
import sys
from pathlib import Path

STATE_FILE = Path.home() / ".claude" / "effort-gate-state.json"
VALID = {"low", "medium", "high", "xhigh", "max"}
ALIASES = {
    "l": "low", "lo": "low", "low": "low",
    "m": "medium", "med": "medium", "medium": "medium",
    "h": "high", "hi": "high", "high": "high",
    "x": "xhigh", "xh": "xhigh", "xhigh": "xhigh",
    "max": "max",
}


def read_state():
    try:
        data = json.loads(STATE_FILE.read_text())
        if data.get("last_effort") in VALID:
            return data
    except (OSError, ValueError, json.JSONDecodeError):
        pass
    return {}


def parse_choice(raw):
    raw = (raw or "").strip().lower()
    if raw == "" or raw in ("skip", "default", "auto", "d"):
        return None
    return ALIASES.get(raw)


def prompt_tty(default):
    try:
        tty = open("/dev/tty", "r+", buffering=1)
    except OSError:
        return None
    try:
        tty.write("\neffort-gate: choose effort for this session\n")
        tty.write("  [l]ow  [m]edium  [h]igh  [x]high  [max]  (default: %s)\n" % default)
        tty.write("  Enter choice (or Enter for default): ")
        tty.flush()
        r, _, _ = select.select([tty], [], [], 15.0)
        if not r:
            tty.write("\ntimed out; using default '%s'\n" % default)
            tty.flush()
            return None
        return parse_choice(tty.readline())
    finally:
        try:
            tty.close()
        except Exception:
            pass


def main():
    try:
        json.load(sys.stdin)
    except (ValueError, json.JSONDecodeError):
        pass

    state = read_state()
    remembered = state.get("last_effort") if state.get("last_effort") in VALID else None
    default_level = remembered or "high"

    attended = os.environ.get("CLAUDE_CODE_SESSION_ATTENDED") == "1"
    chosen = prompt_tty(default_level) if attended else None
    level = chosen if chosen in VALID else default_level

    env_file = os.environ.get("CLAUDE_ENV_FILE")
    applied_via = None
    if env_file:
        try:
            with open(env_file, "a") as f:
                f.write("export CLAUDE_CODE_EFFORT_LEVEL=%s\n" % level)
            applied_via = "CLAUDE_ENV_FILE"
        except OSError:
            applied_via = None

    try:
        STATE_FILE.write_text(json.dumps({"last_effort": level}, indent=2) + "\n")
    except OSError:
        pass

    if applied_via:
        context = (
            "effort-gate: effort set to '%s' for this session via CLAUDE_CODE_EFFORT_LEVEL. "
            "Override anytime with /effort <level>." % level
        )
    else:
        context = (
            "effort-gate: could not apply effort automatically (no CLAUDE_ENV_FILE). "
            "Please run /effort %s." % level
        )

    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
            "initialUserMessage": "/effort %s" % level,
        },
        "systemMessage": "effort-gate: effort = %s" % level,
    }
    print(json.dumps(out))
    sys.exit(0)


if __name__ == "__main__":
    main()
