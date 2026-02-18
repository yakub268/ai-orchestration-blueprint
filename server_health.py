"""
MCP Server Health Monitor — Checks server availability and restarts failed instances.

Designed for long-running AI agent sessions where MCP servers may drop connections.
"""

import json
import time
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class HealthCheck:
    """Result of a server health check."""
    server_name: str
    healthy: bool
    latency_ms: float
    timestamp: datetime
    error: Optional[str] = None


@dataclass
class ServerMetrics:
    """Accumulated metrics for a server."""
    total_checks: int = 0
    failures: int = 0
    total_latency_ms: float = 0.0
    last_failure: Optional[datetime] = None
    consecutive_failures: int = 0

    @property
    def availability(self) -> float:
        if self.total_checks == 0:
            return 0.0
        return (self.total_checks - self.failures) / self.total_checks

    @property
    def avg_latency_ms(self) -> float:
        successful = self.total_checks - self.failures
        if successful == 0:
            return 0.0
        return self.total_latency_ms / successful


class HealthMonitor:
    """
    Monitors MCP server health and triggers recovery actions.

    Tracks availability, latency, and consecutive failures per server.
    Supports configurable thresholds for alerting and auto-restart.
    """

    def __init__(
        self,
        check_interval_s: int = 60,
        max_consecutive_failures: int = 3,
        restart_cooldown_s: int = 300,
    ):
        self.check_interval_s = check_interval_s
        self.max_consecutive_failures = max_consecutive_failures
        self.restart_cooldown_s = restart_cooldown_s
        self.metrics: dict[str, ServerMetrics] = {}
        self.history: list[HealthCheck] = []

    def record_check(self, check: HealthCheck) -> None:
        """Record a health check result."""
        if check.server_name not in self.metrics:
            self.metrics[check.server_name] = ServerMetrics()

        m = self.metrics[check.server_name]
        m.total_checks += 1
        self.history.append(check)

        if check.healthy:
            m.total_latency_ms += check.latency_ms
            m.consecutive_failures = 0
        else:
            m.failures += 1
            m.last_failure = check.timestamp
            m.consecutive_failures += 1
            logger.warning(
                "Server %s failed (%d consecutive): %s",
                check.server_name,
                m.consecutive_failures,
                check.error,
            )

    def needs_restart(self, server_name: str) -> bool:
        """Check if a server has exceeded the failure threshold."""
        m = self.metrics.get(server_name)
        if not m:
            return False

        if m.consecutive_failures < self.max_consecutive_failures:
            return False

        # Respect cooldown to prevent restart loops
        if m.last_failure:
            cooldown_until = m.last_failure + timedelta(seconds=self.restart_cooldown_s)
            if datetime.now() < cooldown_until:
                return False

        return True

    def get_report(self) -> dict[str, dict]:
        """Generate a health report for all monitored servers."""
        report = {}
        for name, m in self.metrics.items():
            report[name] = {
                "availability": f"{m.availability:.1%}",
                "avg_latency_ms": f"{m.avg_latency_ms:.1f}",
                "total_checks": m.total_checks,
                "failures": m.failures,
                "consecutive_failures": m.consecutive_failures,
                "needs_restart": self.needs_restart(name),
            }
        return report

    def get_degraded_servers(self) -> list[str]:
        """Return list of servers below 95% availability."""
        return [
            name for name, m in self.metrics.items()
            if m.availability < 0.95 and m.total_checks >= 5
        ]


def check_config_health(config_path: str | Path) -> dict[str, str]:
    """Validate an MCP config file for common issues."""
    config_path = Path(config_path)
    issues = {}

    if not config_path.exists():
        return {"config": f"File not found: {config_path}"}

    try:
        with open(config_path) as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        return {"config": f"Invalid JSON: {e}"}

    servers = config.get("mcpServers", {})
    if not servers:
        issues["config"] = "No mcpServers defined"
        return issues

    for name, server in servers.items():
        if "command" not in server:
            issues[name] = "Missing 'command' field"
            continue

        cmd = server["command"]
        if cmd in ("npx", "uvx"):
            args = server.get("args", [])
            if not args:
                issues[name] = f"No args for {cmd} — missing package name"

        # Check for Windows path issues
        for arg in server.get("args", []):
            if isinstance(arg, str) and "\\" in arg and "\\\\" not in arg:
                issues[name] = f"Single backslash in path: {arg}"
                break

    return issues


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Demo: validate config files
    for config in Path("mcp-config").glob("*.json"):
        print(f"\nChecking {config.name}:")
        issues = check_config_health(config)
        if issues:
            for server, issue in issues.items():
                print(f"  [{server}] {issue}")
        else:
            print("  All servers configured correctly")

    # Demo: health monitoring
    monitor = HealthMonitor(max_consecutive_failures=3)
    servers = ["filesystem", "git", "memory", "sequential-thinking"]

    for server in servers:
        monitor.record_check(HealthCheck(
            server_name=server,
            healthy=True,
            latency_ms=45.0,
            timestamp=datetime.now(),
        ))

    # Simulate a failure
    monitor.record_check(HealthCheck(
        server_name="git",
        healthy=False,
        latency_ms=0,
        timestamp=datetime.now(),
        error="Connection refused",
    ))

    print("\nHealth Report:")
    for name, stats in monitor.get_report().items():
        print(f"  {name}: {stats['availability']} uptime, {stats['avg_latency_ms']}ms avg")
