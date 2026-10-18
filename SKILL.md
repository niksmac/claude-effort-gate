---
name: effort-gate
description: "Use at the start of every session to set the effort level (low, medium, high, xhigh, max) for the session via CLAUDE_CODE_EFFORT_LEVEL, prompting interactively when attended. Trigger phrases: effort, set effort, effort level."
---

# effort-gate

This plugin sets the session effort level before other work.

## Automatic (SessionStart)

On every new/resumed/cleared session, the `SessionStart` hook runs `scripts/session_start.py`:

- In an attended (interactive) session, it prompts on `/dev/tty` for an effort level (defaulting to the last-used one) with a 15s timeout.
- In a non-attended session (`-p`), it uses the last-used level (or `high`).
- It writes `export CLAUDE_CODE_EFFORT_LEVEL=<level>` to `$CLAUDE_ENV_FILE`, so the level applies to the whole session (highest precedence). It also remembers the choice in `~/.claude/effort-gate-state.json`.

Override anytime during a session with `/effort <level>`.

Levels: low, medium, high (recommended default), xhigh (Opus 4.7 only), max.

## Manual

Run `/ask-effort` to re-prompt and record a choice (applies next session).
