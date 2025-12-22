# MCP Server Registry

Last updated: 2025-01-15

Curated registry of MCP servers organized by category. This registry is automatically updated when older than 7 days.

## Development Tools

### github
- **Purpose**: GitHub API integration for repositories, issues, pull requests
- **Transport**: http
- **Install**: `claude mcp add --transport http github https://api.githubcopilot.com/mcp/`
- **Config**:
```json
{
  "type": "http",
  "url": "https://api.githubcopilot.com/mcp/"
}
```
- **Use cases**: Software development projects, open source contributions
- **Docs**: https://github.com/features/copilot

### git
- **Purpose**: Local git repository operations
- **Transport**: stdio
- **Install**: `claude mcp add --transport stdio git -- npx -y @modelcontextprotocol/server-git`
- **Use cases**: Any project with version control

### gitlab
- **Purpose**: GitLab API integration
- **Transport**: http
- **Use cases**: GitLab-hosted projects

## Databases

### postgres
- **Purpose**: PostgreSQL database queries and management
- **Transport**: stdio
- **Install**: `claude mcp add --transport stdio postgres -e DATABASE_URL=postgresql://localhost:5432/db -- npx @modelcontextprotocol/server-postgres`
- **Config**:
```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["@modelcontextprotocol/server-postgres"],
  "env": {
    "DATABASE_URL": "${DATABASE_URL:-postgresql://localhost:5432/defaultdb}"
  }
}
```
- **Use cases**: Applications using PostgreSQL

### sqlite
- **Purpose**: SQLite database operations
- **Transport**: stdio
- **Install**: `claude mcp add --transport stdio sqlite -- npx @modelcontextprotocol/server-sqlite`
- **Use cases**: Local data storage, prototyping

### mongodb
- **Purpose**: MongoDB database operations
- **Transport**: stdio
- **Use cases**: Applications using MongoDB

## File Operations

### filesystem
- **Purpose**: Enhanced file system access beyond built-in tools
- **Transport**: stdio
- **Install**: `claude mcp add --transport stdio filesystem -- npx @modelcontextprotocol/server-filesystem`
- **Use cases**: Projects requiring extensive file operations

## Search & Knowledge

### brave-search
- **Purpose**: Web search using Brave Search API
- **Transport**: stdio
- **Install**: `claude mcp add --transport stdio brave-search -e BRAVE_API_KEY=your_key -- npx @modelcontextprotocol/server-brave-search`
- **Config**:
```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["@modelcontextprotocol/server-brave-search"],
  "env": {
    "BRAVE_API_KEY": "${BRAVE_API_KEY}"
  }
}
```
- **Use cases**: Content research, fact-checking

### google-search
- **Purpose**: Google Search integration
- **Transport**: stdio
- **Use cases**: Research-heavy projects

## Productivity

### notion
- **Purpose**: Notion workspace integration
- **Transport**: http
- **Use cases**: Knowledge management, documentation

### slack
- **Purpose**: Slack workspace integration
- **Transport**: http
- **Use cases**: Team communication, notifications

### google-drive
- **Purpose**: Google Drive file access
- **Transport**: http
- **Use cases**: Document collaboration

## Cloud Services

### aws
- **Purpose**: AWS service integration
- **Transport**: stdio
- **Use cases**: Cloud infrastructure management

### gcp
- **Purpose**: Google Cloud Platform integration
- **Transport**: stdio
- **Use cases**: GCP resource management

## Data & Analytics

### jupyter
- **Purpose**: Jupyter notebook integration
- **Transport**: stdio
- **Use cases**: Data analysis projects

### pandas
- **Purpose**: Data manipulation with pandas
- **Transport**: stdio
- **Use cases**: Data analysis, data science

## Notes

### Command Syntax
- **CRITICAL**: When using `claude mcp add` with environment variables, the CORRECT order is:
  ```
  claude mcp add --transport stdio server-name -e KEY=value -- command
  ```
- The server name comes FIRST (right after --transport)
- Then environment variables with `-e KEY=value` (or `--env KEY=value`)
- Then the `--` separator
- Then the command to run the MCP server
- Example: `claude mcp add --transport stdio myserver -e API_KEY=123 -- npx package`

### Security
- **NEVER use real credentials** in examples or documentation
- Use placeholder values like `your_key`, `your_token`, or `PLACEHOLDER_VALUE`
- Always use environment variable expansion: `${VAR}` or `${VAR:-default}`
- Add `.env` files to `.gitignore`

### Configuration
- Environment variables use `${VAR:-default}` syntax for expansion
- Project-scoped servers go in `.mcp.json` at project root
- User-scoped servers stored in `~/.claude.json`
- Always validate MCP server sources before installation
