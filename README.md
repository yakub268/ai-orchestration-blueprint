# AI Orchestration Blueprint (Windows-first, $0 extra)

This repo coordinates **ChatGPT (web/Plus)** for planning/review with **Claude (Desktop/Code)** for local execution via MCPs. Free **GitHub Actions** runs **Semgrep** on every push/PR. Playwright is scaffolded but disabled by default. No Docker. No OpenAI API.

## Modes (Copilot Coexistence)
- **Mode A (Claude MCP ON / Copilot OFF)**: `%APPDATA%/Claude/claude_desktop_config.json` active; disable VS Code `GitHub.copilot*`.
- **Mode B (Copilot ON / Claude MCP OFF)**: rename that config to `.disabled`; enable `GitHub.copilot*`.

## Daily Runbook
See `journals/Journal.md` and the master playbook.

## CI
- Free Semgrep on each push/PR (`.github/workflows/semgrep.yml`).
- Lint/test steps are optional and gated.

## Memory
- Default: Basic file/SQLite through Claude’s Memory MCP + `journals/Journal.md` / `CLAUDE.md`.
- Pilots (off by default): Mem0/OpenMemory; see `.env.example`.
