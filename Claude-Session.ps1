<#
.SYNOPSIS
    Claude session management utilities
.DESCRIPTION
    Helps manage Claude Desktop sessions, view logs, and optimize usage
.NOTES
    Run from PowerShell
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("logs", "clear-logs", "config", "restart")]
    [string]$Action = "logs"
)

$LogPath = "$env:APPDATA\Claude\logs"
$ConfigPath = "$env:APPDATA\Claude\claude_desktop_config.json"

switch ($Action) {
    "logs" {
        Write-Host "`n=== Recent Claude Desktop Logs ===" -ForegroundColor Cyan
        
        # MCP connection logs
        $mcpLog = Join-Path $LogPath "mcp.log"
        if (Test-Path $mcpLog) {
            Write-Host "`n--- MCP Server Status ---" -ForegroundColor Yellow
            Get-Content $mcpLog -Tail 30 | Select-String -Pattern "connected|error|fail|start" -CaseSensitive:$false | 
                ForEach-Object { Write-Host $_ }
        }
        
        # Error patterns
        Write-Host "`n--- Recent Errors ---" -ForegroundColor Red
        Get-ChildItem $LogPath -Filter "*.log" | ForEach-Object {
            Get-Content $_.FullName -Tail 100 | Select-String -Pattern "error|exception|fail" -CaseSensitive:$false |
                Select-Object -First 10 | ForEach-Object { Write-Host $_ }
        }
    }
    "clear-logs" {
        Write-Host "Clearing Claude Desktop logs..." -ForegroundColor Yellow
        Get-ChildItem $LogPath -Filter "*.log" | Remove-Item -Force
        Write-Host "Logs cleared" -ForegroundColor Green
    }
    "config" {
        Write-Host "`n=== Current Claude Desktop Config ===" -ForegroundColor Cyan
        if (Test-Path $ConfigPath) {
            Get-Content $ConfigPath | ConvertFrom-Json | ConvertTo-Json -Depth 10
        } else {
            Write-Host "Config not found at $ConfigPath" -ForegroundColor Red
        }
    }
    "restart" {
        Write-Host "Stopping Claude Desktop..." -ForegroundColor Yellow
        Get-Process -Name "Claude*" -ErrorAction SilentlyContinue | Stop-Process -Force
        Start-Sleep -Seconds 2
        
        # Verify stopped
        $remaining = Get-Process -Name "Claude*" -ErrorAction SilentlyContinue
        if ($remaining) {
            Write-Host "Some Claude processes still running, force killing..." -ForegroundColor Red
            $remaining | Stop-Process -Force
            Start-Sleep -Seconds 1
        }
        
        Write-Host "Starting Claude Desktop..." -ForegroundColor Yellow
        Start-Process "$env:LOCALAPPDATA\Programs\Claude\Claude.exe"
        Write-Host "Claude Desktop restarted" -ForegroundColor Green
    }
}

Write-Host "`nUsage:"
Write-Host "  .\Claude-Session.ps1 -Action logs        # View recent logs"
Write-Host "  .\Claude-Session.ps1 -Action clear-logs  # Clear all logs"
Write-Host "  .\Claude-Session.ps1 -Action config      # View current config"
Write-Host "  .\Claude-Session.ps1 -Action restart     # Restart Claude Desktop"
