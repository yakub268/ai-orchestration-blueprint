# AI Orchestration Blueprint

## Project Overview
Production-grade MCP architecture and AI tooling infrastructure for Windows 11 development environments. Repository: github.com/yakub268/ai-orchestration-blueprint

## Environment
- **OS**: Windows 11
- **Node.js**: 24.8.0
- **Python**: 3.12
- **Git**: 2.51.0
- **RAM**: 32GB
- **CPU**: 16 cores

## MCP Server Stack
| Server | Status | Purpose |
|--------|--------|---------|
| filesystem | ✅ Active | File operations |
| git | ✅ Active | Repository management (@cyanheads/git-mcp-server) |
| memory | ✅ Active | Context persistence |
| sequential-thinking | ✅ Active | Complex reasoning |

## Directory Structure
```
C:\dev\projects\ai-orchestration-blueprint\
├── claude_config_*.json   # Various config iterations
├── claude_logs.txt        # Debug logs
└── README.md              # Project documentation
```

## Configuration Paths
- **Claude Desktop Config**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Claude Logs**: `%APPDATA%\Claude\logs\`
- **Global npm modules**: `%APPDATA%\npm\node_modules\`

## Common Commands
```powershell
# Check MCP server status
npm list -g --depth=0 | Select-String "modelcontextprotocol|cyanheads"

# View Claude Desktop logs
Get-Content "$env:APPDATA\Claude\logs\mcp.log" -Tail 50

# Install MCP server globally
npm install -g @modelcontextprotocol/server-<name>

# Test MCP server
npx @modelcontextprotocol/inspector
```

## Windows-Specific Notes
- Use full paths to `node.exe` and `npx.cmd` in MCP configs
- Double backslashes required in JSON: `C:\\\\Program Files\\\\`
- Run PowerShell as Administrator for npm global installs
- GitHub Copilot conflicts with Claude Desktop MCP - use separate VS Code config

## Known Issues & Solutions
| Issue | Solution |
|-------|----------|
| "Cannot connect to MCP server" | Use full path to npx.cmd |
| Copilot Chat broken | Remove MCP from Claude Desktop, use .vscode/mcp.json |
| npm ENOENT errors | Run CMD instead of PowerShell |

## Git Workflow
- CI/CD running at 100% pass rate
- Commit with conventional commit messages
- Full 7-phase execution: Plan → Execute → Scan → Review → Commit → Document → Deploy
