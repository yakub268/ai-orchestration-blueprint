<#
.SYNOPSIS
    Toggle Claude Desktop MCP configuration for GitHub Copilot compatibility
.DESCRIPTION
    Switches between full MCP config and minimal config to resolve 
    Claude Desktop + GitHub Copilot conflict (Issue #258332)
.NOTES
    Run from PowerShell as Administrator
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("full", "minimal", "status")]
    [string]$Mode = "status"
)

$ConfigPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$FullConfigPath = "$env:APPDATA\Claude\claude_desktop_config_OPTIMIZED.json"
$MinimalConfigPath = "$env:APPDATA\Claude\claude_desktop_config_MINIMAL.json"

# Create minimal config if it doesn't exist
$MinimalConfig = @{
    mcpServers = @{}
    preferences = @{
        chromeExtensionEnabled = $true
    }
} | ConvertTo-Json -Depth 10

if (-not (Test-Path $MinimalConfigPath)) {
    $MinimalConfig | Out-File -FilePath $MinimalConfigPath -Encoding utf8
    Write-Host "Created minimal config at $MinimalConfigPath" -ForegroundColor Green
}

function Get-CurrentMode {
    if (Test-Path $ConfigPath) {
        $config = Get-Content $ConfigPath | ConvertFrom-Json
        $serverCount = ($config.mcpServers.PSObject.Properties | Measure-Object).Count
        if ($serverCount -gt 0) {
            return "full"
        } else {
            return "minimal"
        }
    }
    return "unknown"
}

switch ($Mode) {
    "status" {
        $current = Get-CurrentMode
        Write-Host "`nCurrent Claude Desktop Mode: " -NoNewline
        if ($current -eq "full") {
            Write-Host "FULL MCP" -ForegroundColor Cyan
            Write-Host "  - All MCP servers enabled" -ForegroundColor Gray
            Write-Host "  - GitHub Copilot Chat may be broken" -ForegroundColor Yellow
        } elseif ($current -eq "minimal") {
            Write-Host "MINIMAL (Copilot-safe)" -ForegroundColor Green
            Write-Host "  - No MCP servers" -ForegroundColor Gray
            Write-Host "  - GitHub Copilot Chat works" -ForegroundColor Green
        } else {
            Write-Host "UNKNOWN" -ForegroundColor Red
        }
        Write-Host "`nUsage:"
        Write-Host "  .\Toggle-ClaudeMCP.ps1 -Mode full     # Enable all MCP servers"
        Write-Host "  .\Toggle-ClaudeMCP.ps1 -Mode minimal  # Disable MCP for Copilot compatibility"
    }
    "full" {
        if (Test-Path $FullConfigPath) {
            Copy-Item $FullConfigPath $ConfigPath -Force
            Write-Host "Switched to FULL MCP mode" -ForegroundColor Cyan
            Write-Host "Restart Claude Desktop to apply changes" -ForegroundColor Yellow
        } else {
            Write-Host "Full config not found at $FullConfigPath" -ForegroundColor Red
        }
    }
    "minimal" {
        Copy-Item $MinimalConfigPath $ConfigPath -Force
        Write-Host "Switched to MINIMAL mode (Copilot-safe)" -ForegroundColor Green
        Write-Host "Restart Claude Desktop to apply changes" -ForegroundColor Yellow
    }
}
