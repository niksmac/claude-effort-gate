# claude-effort-gate

A Claude Code plugin that prompts for and applies an [effort level](https://code.claude.com/docs/en/model-config#adjust-effort-level) at the start of every session.

Effort controls how much work Claude does per request (thinking depth, files read, steps taken). This plugin makes the choice deliberate instead of silently inheriting whatever was last used.

## How it works

On every new, resumed, or cleared session, a `SessionStart` hook runs `scripts/session_start.py`:

- **Interactive session:** prompts on `/dev/tty` for an effort level (`low`, `medium`, `high`, `xhigh`, `max`), defaulting to the last-used one, with a 15s timeout.
- **Non-interactive (`-p`):** uses the last-used level (or `high`) without prompting.
- Writes `export CLAUDE_CODE_EFFORT_LEVEL=<level>` to `$CLAUDE_ENV_FILE`, so the level applies to the whole session (highest precedence). Also remembers the choice in `~/.claude/effort-gate-state.json`.
- Runs `/effort <level>` as the first turn via `initialUserMessage`, so the level is applied even on models (e.g. Opus 4.7) that ignore the env var at launch (see [anthropics/claude-code#52534](https://github.com/anthropics/claude-code/issues/52534)).

Override anytime during a session with `/effort <level>`.

## Install

One-step install from the marketplace (Claude Code 2.1.275+):

```
/plugin install effort-gate --marketplace niksmac/claude-effort-gate
```

Or add the marketplace first, then install:

```
/plugin marketplace add niksmac/claude-effort-gate
/plugin install effort-gate@claude-effort-gate
```

Manual (no marketplace):

```bash
git clone https://github.com/niksmac/claude-effort-gate.git
claude --plugin-dir /path/to/claude-effort-gate
```

Or copy the directory into `~/.claude/skills/effort-gate` (auto-loads as `effort-gate@skills-dir`).

## Usage

- Start a session — you'll be prompted for an effort level (interactive) or the last-used level is applied (`-p`).
- `/ask-effort` — record a preferred level for future sessions (applies next session, or now via `/effort <level>`).

## Effort levels

| Level | When to use |
|---|---|
| `low` | Fast, minimal thinking — lookups, renames, boilerplate |
| `medium` | Balanced — routine coding |
| `high` | Thorough (recommended default) — debugging, refactors |
| `xhigh` | Opus 4.7 only — deeper reasoning for long-horizon work |
| `max` | Highest, no token cap — architecture, security reviews |

## Requirements

- Claude Code 2.1.213+ (for `initialUserMessage` / `CLAUDE_ENV_FILE` support in `SessionStart` hooks).

## License

MIT
