# MCP Server Installation - Command Syntax Reference

**Last Updated**: 2025-01-15

This document provides the DEFINITIVE syntax for `claude mcp add` commands based on official CLI help output.

## Critical Rules

### Order of Arguments

The command must follow this EXACT order:

```
claude mcp add --transport TYPE SERVER_NAME [options] -- COMMAND [args...]
```

1. `claude mcp add`
2. `--transport TYPE` (stdio, http, or sse)
3. `SERVER_NAME` (the name you want to give this server)
4. Environment variables (if needed): `-e KEY=value` or `--env KEY=value`
5. `--` separator (for stdio only)
6. Command to run (for stdio) or URL (for http/sse)

### Examples from Official CLI Help

```bash
# HTTP server
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# SSE server
claude mcp add --transport sse asana https://mcp.asana.com/sse

# stdio server with environment variables
claude mcp add --transport stdio airtable --env AIRTABLE_API_KEY=YOUR_KEY -- npx -y airtable-mcp-server
```

## Common Mistakes

### ❌ WRONG - Environment variables before server name
```bash
claude mcp add --transport stdio -e API_KEY=123 myserver -- npx package
```

### ✅ CORRECT - Server name first, then environment variables
```bash
claude mcp add --transport stdio myserver -e API_KEY=123 -- npx package
```

### ❌ WRONG - Missing -- separator
```bash
claude mcp add --transport stdio myserver -e API_KEY=123 npx package
```

### ✅ CORRECT - Include -- separator before command
```bash
claude mcp add --transport stdio myserver -e API_KEY=123 -- npx package
```

## Real-World Examples

### Strava MCP Server
```bash
claude mcp add --transport stdio strava \
  -e STRAVA_CLIENT_ID=your_id \
  -e STRAVA_CLIENT_SECRET=your_secret \
  -e STRAVA_REFRESH_TOKEN=your_token \
  -- npx -y @r-huijts/strava-mcp
```

### PostgreSQL
```bash
claude mcp add --transport stdio postgres \
  -e DATABASE_URL=postgresql://localhost:5432/db \
  -- npx @modelcontextprotocol/server-postgres
```

### Brave Search
```bash
claude mcp add --transport stdio brave-search \
  -e BRAVE_API_KEY=your_key \
  -- npx @modelcontextprotocol/server-brave-search
```

### GitHub (HTTP - no env vars needed)
```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

## Flag Reference

### Environment Variables
- Both `-e` and `--env` are supported
- Format: `-e KEY=value` or `--env KEY=value`
- Can be repeated: `-e KEY1=val1 -e KEY2=val2`
- Must come AFTER server name, BEFORE `--` separator

### Scope
- `-s, --scope <scope>` - Configuration scope (local, user, or project)
- Default: "local"

### Transport
- `-t, --transport <transport>` - Transport type (stdio, sse, http)
- Required for clarity (though stdio is default)

### Headers (for HTTP/SSE)
- `-H, --header <header...>` - Set WebSocket headers
- Format: `-H "X-Api-Key: abc123"`

## Security Best Practices

1. **Never hardcode credentials** in documentation
   - ✗ `-e API_KEY=sk-abc123def456`
   - ✓ `-e API_KEY=your_key`

2. **Use environment variable expansion** in .mcp.json
   - ✓ `"API_KEY": "${API_KEY}"`
   - ✓ `"API_KEY": "${API_KEY:-default_value}"`

3. **Use placeholder values** in examples
   - `your_key`, `your_token`, `PLACEHOLDER_VALUE`, `YOUR_KEY`

## Troubleshooting

### "Invalid environment variable format: X"
**Cause**: Server name is in the wrong position (likely after -e flags)
**Fix**: Move server name to right after `--transport TYPE`

### "command not found: --transport"
**Cause**: Shell line continuation issue (space after backslash `\ `)
**Fix**: Remove spaces after backslashes, or use single-line command

### "Error: Unknown option: --env"
**Cause**: This should NOT happen - both `--env` and `-e` are supported
**Fix**: Verify you're using latest Claude CLI version

## Quick Reference Card

```bash
# Template
claude mcp add --transport stdio NAME -e KEY=VAL -- COMMAND

# Single env var
claude mcp add --transport stdio myserver -e API_KEY=123 -- npx package

# Multiple env vars
claude mcp add --transport stdio myserver \
  -e KEY1=val1 \
  -e KEY2=val2 \
  -- npx package

# No env vars
claude mcp add --transport stdio myserver -- npx package

# HTTP (no -- separator)
claude mcp add --transport http myserver https://api.example.com/mcp/
```

## Official Documentation

- Claude CLI Help: `claude mcp add --help`
- MCP Protocol: https://modelcontextprotocol.io
- Claude Code Docs: https://code.claude.com/docs/en/mcp.md
