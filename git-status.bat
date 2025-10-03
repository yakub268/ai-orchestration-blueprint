@echo off
REM ============================================================================
REM Git Status Viewer - Enhanced Version
REM ============================================================================
REM Description: Displays comprehensive git repository status information
REM Usage: git-status.bat [path-to-repo]
REM Example: git-status.bat C:\dev\my-project
REM If no path provided, uses current directory
REM ============================================================================

setlocal enabledelayedexpansion

REM Determine target directory
if "%~1"=="" (
    set "TARGET_DIR=%CD%"
    echo [INFO] Using current directory: %CD%
) else (
    set "TARGET_DIR=%~1"
    echo [INFO] Target directory: %~1
)

REM Check if directory exists
if not exist "%TARGET_DIR%" (
    echo [ERROR] Directory does not exist: %TARGET_DIR%
    pause
    exit /b 1
)

REM Change to target directory
cd /d "%TARGET_DIR%" 2>nul
if errorlevel 1 (
    echo [ERROR] Cannot access directory: %TARGET_DIR%
    pause
    exit /b 1
)

REM Check if git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if this is a git repository
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Not a git repository: %TARGET_DIR%
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo                          GIT REPOSITORY STATUS
echo ============================================================================
echo Repository: %TARGET_DIR%
echo.

REM Display current branch with remote tracking
echo --- BRANCH INFORMATION ---
git branch --show-current
for /f "tokens=*" %%i in ('git rev-parse --abbrev-ref --symbolic-full-name @{u} 2^>nul') do (
    echo Tracking: %%i
    
    REM Check ahead/behind status
    for /f "tokens=1,2" %%a in ('git rev-list --left-right --count HEAD...@{u} 2^>nul') do (
        if not "%%a"=="0" echo Ahead by %%a commit(s)
        if not "%%b"=="0" echo Behind by %%b commit(s)
    )
)
echo.

REM Display remote information
echo --- REMOTE REPOSITORIES ---
git remote -v
echo.

REM Display repository status
echo --- WORKING TREE STATUS ---
git status --short --branch
echo.

REM Count changes
for /f %%i in ('git diff --name-only ^| find /c /v ""') do set MODIFIED=%%i
for /f %%i in ('git diff --cached --name-only ^| find /c /v ""') do set STAGED=%%i
for /f %%i in ('git ls-files --others --exclude-standard ^| find /c /v ""') do set UNTRACKED=%%i

echo Summary:
echo   - Modified files: %MODIFIED%
echo   - Staged files: %STAGED%
echo   - Untracked files: %UNTRACKED%
echo.

REM Display recent commits
echo --- RECENT COMMITS (Last 5) ---
git log --oneline --decorate -5
echo.

REM Display stash information
for /f %%i in ('git stash list ^| find /c /v ""') do (
    if not "%%i"=="0" (
        echo --- STASH ENTRIES ---
        git stash list
        echo.
    )
)

echo ============================================================================
echo Scan completed at %DATE% %TIME%
echo ============================================================================
echo.

pause
endlocal
