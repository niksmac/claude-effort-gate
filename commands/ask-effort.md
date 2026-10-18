---
name: ask-effort
description: Record a preferred effort level for future sessions (applies next session).
---

Record the user's preferred effort level for future sessions.

1. Ask the user (via AskUserQuestion) which level they want: low, medium, high, xhigh (Opus 4.7 only), or max. Offer the last-used level as recommended if known.
2. Save it by running `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/record_choice.py" <level>`.
3. Tell the user the choice applies starting next session (or now via /effort <level>).