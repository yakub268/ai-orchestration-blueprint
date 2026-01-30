@echo off
echo ============================================
echo  MCP Server Repair Script
echo  Generated: 2025-12-19
echo ============================================
echo.

echo [1/4] Installing missing @modelcontextprotocol/server-memory...
call npm install -g @modelcontextprotocol/server-memory
if %errorlevel% neq 0 (
    echo ERROR: Failed to install server-memory
    pause
    exit /b 1
)
echo.

echo [2/4] Installing @modelcontextprotocol/server-sequential-thinking...
call npm install -g @modelcontextprotocol/server-sequential-thinking
if %errorlevel% neq 0 (
    echo ERROR: Failed to install server-sequential-thinking
    pause
    exit /b 1
)
echo.

echo [3/4] Clearing npm cache to fix token issues...
call npm cache clean --force
echo.

echo [4/4] Verifying installations...
echo.
echo Installed MCP packages:
call npm list -g --depth=0 2>nul | findstr /i "modelcontextprotocol cyanheads"
echo.

echo ============================================
echo  Repair Complete!
echo ============================================
echo.
echo Next steps:
echo   1. Close Claude Desktop completely
echo   2. Run: copy /Y "%APPDATA%\Claude\claude_desktop_config_FIXED.json" "%APPDATA%\Claude\claude_desktop_config.json"
echo   3. Restart Claude Desktop
echo.
pause
