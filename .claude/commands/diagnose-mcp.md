Diagnose MCP server connection issues for: $ARGUMENTS

1. Check if the server package is installed globally:
   ```powershell
   npm list -g --depth=0 | Select-String "$ARGUMENTS"
   ```

2. Verify Node.js paths:
   ```powershell
   where node
   where npx
   ```

3. Check Claude Desktop logs for errors:
   ```powershell
   Get-Content "$env:APPDATA\Claude\logs\mcp.log" -Tail 100 | Select-String -Pattern "error|fail|disconnect" -CaseSensitive:$false
   ```

4. Verify the server can start manually:
   ```powershell
   node "C:\Users\yakub\AppData\Roaming\npm\node_modules\@modelcontextprotocol\server-$ARGUMENTS\dist\index.js"
   ```

5. If errors found, provide specific resolution steps based on common Windows issues:
   - ENOENT: Use full path to npx.cmd
   - Permission denied: Run as Administrator
   - Module not found: Reinstall with `npm install -g`
