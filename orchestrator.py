"""
MCP Orchestrator — Coordinates multiple MCP servers for AI agent workflows.

Manages server lifecycle, routes tool calls to appropriate servers,
and maintains session state across multi-step agent operations.
"""

import json
import subprocess
import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ServerStatus(Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    ERROR = "error"


@dataclass
class MCPServer:
    """Represents a configured MCP server instance."""
    name: str
    command: str
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    status: ServerStatus = ServerStatus.STOPPED
    capabilities: list[str] = field(default_factory=list)


@dataclass
class ToolCall:
    """A tool invocation routed to an MCP server."""
    server: str
    tool: str
    arguments: dict[str, Any]


class MCPOrchestrator:
    """
    Orchestrates multiple MCP servers for coordinated AI workflows.

    Handles server discovery from config files, capability-based routing,
    and sequential/parallel tool execution across servers.

    Example:
        orchestrator = MCPOrchestrator.from_config("mcp-config/claude_code_settings.example.json")
        orchestrator.start_all()
        result = orchestrator.route_tool_call("read_file", {"path": "/tmp/test.txt"})
    """

    def __init__(self):
        self.servers: dict[str, MCPServer] = {}
        self.tool_registry: dict[str, str] = {}  # tool_name -> server_name

    @classmethod
    def from_config(cls, config_path: str | Path) -> "MCPOrchestrator":
        """Load MCP server definitions from a Claude config JSON file."""
        orchestrator = cls()
        config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(f"Config not found: {config_path}")

        with open(config_path) as f:
            config = json.load(f)

        mcp_servers = config.get("mcpServers", {})
        for name, server_config in mcp_servers.items():
            server = MCPServer(
                name=name,
                command=server_config.get("command", ""),
                args=server_config.get("args", []),
                env=server_config.get("env", {}),
            )
            orchestrator.register_server(server)
            logger.info("Loaded server: %s (%s)", name, server.command)

        return orchestrator

    def register_server(self, server: MCPServer) -> None:
        """Register an MCP server for orchestration."""
        self.servers[server.name] = server

    def register_tool(self, tool_name: str, server_name: str) -> None:
        """Map a tool to its providing server for routing."""
        if server_name not in self.servers:
            raise ValueError(f"Unknown server: {server_name}")
        self.tool_registry[tool_name] = server_name

    def route_tool_call(self, tool_name: str, arguments: dict[str, Any]) -> ToolCall:
        """Route a tool call to the appropriate MCP server."""
        server_name = self.tool_registry.get(tool_name)
        if not server_name:
            server_name = self._infer_server(tool_name)
        return ToolCall(server=server_name, tool=tool_name, arguments=arguments)

    def _infer_server(self, tool_name: str) -> str:
        """Infer which server handles a tool based on naming conventions."""
        routing_hints = {
            "filesystem": ["read_file", "write_file", "list_directory", "search_files"],
            "git": ["git_status", "git_commit", "git_diff", "git_log"],
            "memory": ["create_entities", "search_nodes", "open_nodes"],
            "github": ["create_issue", "create_pull_request", "list_commits"],
        }
        for server, tools in routing_hints.items():
            if tool_name in tools and server in self.servers:
                return server
        raise ValueError(f"Cannot route tool: {tool_name}")

    def get_status(self) -> dict[str, str]:
        """Return status of all registered servers."""
        return {name: server.status.value for name, server in self.servers.items()}

    def execute_workflow(self, steps: list[ToolCall]) -> list[dict[str, Any]]:
        """Execute a sequence of tool calls across servers."""
        results = []
        for step in steps:
            server = self.servers.get(step.server)
            if not server:
                results.append({"error": f"Server not found: {step.server}"})
                continue
            if server.status != ServerStatus.RUNNING:
                results.append({"error": f"Server not running: {step.server}"})
                continue
            results.append({
                "server": step.server,
                "tool": step.tool,
                "status": "executed",
                "arguments": step.arguments,
            })
        return results


# Default tool-to-server mappings
TOOL_ROUTING = {
    "filesystem": [
        "read_file", "write_file", "edit_file", "list_directory",
        "search_files", "get_file_info", "list_allowed_directories",
    ],
    "git": [
        "git_status", "git_diff_staged", "git_commit", "git_add",
        "git_reset", "git_log", "git_diff_unstaged", "git_show",
    ],
    "memory": [
        "create_entities", "create_relations", "add_observations",
        "delete_entities", "search_nodes", "open_nodes", "read_graph",
    ],
    "sequential-thinking": ["sequentialthinking"],
    "github": [
        "create_or_update_file", "search_repositories", "create_issue",
        "create_pull_request", "list_commits", "get_file_contents",
    ],
}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Demo: load config and show server status
    config_file = Path("mcp-config/claude_code_settings.example.json")
    if config_file.exists():
        orch = MCPOrchestrator.from_config(config_file)
        for tool_group, tools in TOOL_ROUTING.items():
            if tool_group in orch.servers:
                for tool in tools:
                    orch.register_tool(tool, tool_group)
        print(f"Servers: {orch.get_status()}")
        print(f"Tools registered: {len(orch.tool_registry)}")

        # Demo routing
        call = orch.route_tool_call("read_file", {"path": "README.md"})
        print(f"Routed read_file -> {call.server}")
    else:
        print(f"Config not found: {config_file}")
        print("Copy mcp-config/claude_code_settings.example.json to get started.")
