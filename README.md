# AI Orchestration Blueprint

A framework for orchestrating multi-AI workflows between Claude (via MCP) and ChatGPT, with built-in security scanning and version control.

## Architecture

Two AIs with distinct roles, coordinated through structured prompts and documented state:

- **ChatGPT** — planning, strategy, high-level review
- **Claude** — execution via MCP (filesystem, git, security tooling)
- **Handoffs** — structured prompt templates + journal-based state

### MCP Servers (Claude Desktop)

| Server | Purpose |
|--------|---------|
| filesystem | Secure file operations (scoped directories) |
| git | Repository management (uvx-based) |
| memory | Context persistence across sessions |
| github | Remote repo integration |
| semgrep | Security scanning and code analysis |
| sequential-thinking | Complex multi-step reasoning |
| brave-search | Web search |
| windows-mcp | Windows system automation |

## Project Structure

```
ai-orchestration-blueprint/
├── .github/workflows/
│   └── semgrep.yml              # CI security scanning
├── .claude/commands/
│   ├── diagnose-mcp.md          # MCP diagnostics slash command
│   └── fix-issue.md             # Issue fix slash command
├── journals/
│   └── Journal.md               # Session state and progress tracking
├── mcp-config/
│   ├── claude_desktop_config.example.json
│   └── claude_code_settings.example.json
├── policies/
│   ├── .eslintrc.json
│   ├── .prettierrc.json
│   └── semgrep-notes.md
├── prompts/
│   ├── plan_orchestration.txt   # Role assignment
│   ├── code_review.txt          # Review workflow
│   ├── refactor.txt             # Refactoring guidance
│   ├── summarize_long.txt       # Long-form summarization
│   └── test_generation.txt      # Test creation
├── reports/                     # Generated analysis output
├── tests/playwright/            # E2E test scaffolding
├── git-status.bat               # Enhanced git status utility
├── Claude-Session.ps1           # Session launcher
├── Toggle-ClaudeMCP.ps1         # MCP toggle utility
├── repair-mcp-servers.bat       # MCP repair script
├── CLAUDE.md                    # Claude-specific instructions
└── .env.example                 # Environment variable template
```

## Setup

### Prerequisites

- Claude Desktop with MCP support (v0.13+)
- Python 3.12+ with `uv` (`pip install uv`)
- Node.js 18+
- Git
- GitHub account with personal access token (repo + workflow permissions)

### Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/yakub268/ai-orchestration-blueprint.git
   cd ai-orchestration-blueprint
   ```

2. Install UV:
   ```bash
   pip install uv
   ```

3. Configure Claude Desktop — edit `%APPDATA%\Claude\claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-filesystem",
                  "C:\\path\\to\\ai-orchestration-blueprint"]
       },
       "git": {
         "command": "uvx",
         "args": ["mcp-server-git", "--repository",
                  "C:\\path\\to\\ai-orchestration-blueprint"]
       },
       "memory": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-memory"]
       },
       "github": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-github"],
         "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_token_here" }
       }
     }
   }
   ```
   See `mcp-config/` for full example configs.

4. Copy `.env.example` to `.env` and fill in your tokens.

5. Restart Claude Desktop (fully — check Task Manager). The hammer icon in the bottom-right confirms MCP servers loaded.

## Workflow (7 Phases)

| Phase | Role | Action |
|-------|------|--------|
| 1. Plan | ChatGPT | Numbered action plan with role assignments |
| 2. Execute | Claude + MCP | Implement using filesystem/git MCPs |
| 3. Scan | Claude + Semgrep | Security scan before commit |
| 4. Review | ChatGPT | Code review against `prompts/code_review.txt` |
| 5. Commit | Claude + Git MCP | Conventional commit messages |
| 6. Document | Both | Update journals, comments, docs |
| 7. Deploy | Claude + Git MCP | Push, trigger CI, monitor Actions |

## Security

- Semgrep CI runs on every push (`p/ci` ruleset)
- MCP filesystem access scoped to explicitly configured directories
- No secrets in repo — use `.env` (already in `.gitignore`)
- GitHub tokens use minimal required permissions

## Troubleshooting

**Git MCP 404 error** — The npm package was archived in late 2024. Use the Python version:
```json
{ "git": { "command": "uvx", "args": ["mcp-server-git", "--repository", "C:\\your\\repo"] } }
```

**MCP servers not appearing** — Verify `%APPDATA%\Claude\claude_desktop_config.json` syntax, use double backslashes for Windows paths, close Claude fully (Task Manager), restart as Administrator. Logs at `%APPDATA%\Claude\logs\`.

**Semgrep CI failing** — Run local scan via Semgrep MCP before pushing. Verify GitHub token has `workflow` permission.

## Tech Stack

- **Claude Desktop** — MCP host
- **Model Context Protocol** — AI-to-tool bridge
- **Semgrep** — Static analysis and security scanning
- **GitHub Actions** — CI/CD
- **Python / uvx** — Git MCP server runtime
- **Node.js / npx** — Other MCP servers

## License

MIT — see [LICENSE](LICENSE)

## Links

- [GitHub Repository](https://github.com/yakub268/ai-orchestration-blueprint)
- [MCP Documentation](https://modelcontextprotocol.io)
- [Semgrep Rules](https://semgrep.dev/docs/)
- [Claude Desktop](https://claude.ai/download)
