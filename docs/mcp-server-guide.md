# MCP Server Guide

Comprehensive guide to MCP (Model Context Protocol) servers available for Claude Code projects.

## What are MCP Servers?

MCP servers extend Claude Code's capabilities by providing integrations with external services, databases, APIs, and tools. They allow Claude to:

- Access databases (PostgreSQL, SQLite, MongoDB)
- Integrate with version control (GitHub, GitLab)
- Search the web (Brave, Google)
- Connect to cloud services (AWS, GCP, Azure)
- Access productivity tools (Notion, Slack, Google Drive)

## Server Categories

### Development Tools

#### github
- **Purpose**: GitHub API integration for repositories, issues, pull requests, and actions
- **Transport**: HTTP
- **Installation**:
  ```bash
  claude mcp add --transport http github https://api.githubcopilot.com/mcp/
  ```
- **Use cases**: Software development, open source projects, CI/CD
- **Configuration**:
  ```json
  {
    "type": "http",
    "url": "https://api.githubcopilot.com/mcp/"
  }
  ```

#### git
- **Purpose**: Local git repository operations
- **Transport**: stdio
- **Installation**:
  ```bash
  claude mcp add --transport stdio git -- npx -y @modelcontextprotocol/server-git
  ```
- **Use cases**: Version control, commit history, branch management

#### gitlab
- **Purpose**: GitLab API integration
- **Transport**: HTTP
- **Use cases**: GitLab-hosted projects, CI/CD pipelines

---

### Databases

#### postgres
- **Purpose**: PostgreSQL database queries and management
- **Transport**: stdio
- **Installation**:
  ```bash
  claude mcp add --transport stdio postgres \
    -e DATABASE_URL=postgresql://localhost:5432/db \
    -- npx @modelcontextprotocol/server-postgres
  ```
- **Configuration**:
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
- **Use cases**: Web applications, data storage, complex queries
- **Required**: `DATABASE_URL` environment variable

#### sqlite
- **Purpose**: SQLite database operations
- **Transport**: stdio
- **Installation**:
  ```bash
  claude mcp add --transport stdio sqlite -- npx @modelcontextprotocol/server-sqlite
  ```
- **Use cases**: Local data storage, prototyping, personal projects
- **Benefits**: No server setup, file-based, portable

#### mongodb
- **Purpose**: MongoDB database operations
- **Transport**: stdio
- **Use cases**: Document storage, NoSQL applications

---

### File Operations

#### filesystem
- **Purpose**: Enhanced file system access beyond built-in tools
- **Transport**: stdio
- **Installation**:
  ```bash
  claude mcp add --transport stdio filesystem -- npx @modelcontextprotocol/server-filesystem
  ```
- **Use cases**: Complex file operations, batch processing

---

### Search & Knowledge

#### brave-search
- **Purpose**: Web search using Brave Search API
- **Transport**: stdio
- **Installation**:
  ```bash
  claude mcp add --transport stdio brave-search \
    -e BRAVE_API_KEY=your_key \
    -- npx @modelcontextprotocol/server-brave-search
  ```
- **Configuration**:
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
- **Use cases**: Content research, fact-checking, web integration
- **Required**: Brave Search API key

#### google-search
- **Purpose**: Google Search integration
- **Transport**: stdio
- **Use cases**: Research, content discovery
- **Required**: Google Search API credentials

---

### Productivity

#### notion
- **Purpose**: Notion workspace integration
- **Transport**: HTTP
- **Use cases**: Knowledge management, documentation, team wikis
- **Required**: Notion API token

#### slack
- **Purpose**: Slack workspace integration
- **Transport**: HTTP
- **Use cases**: Team communication, notifications, bot interactions
- **Required**: Slack API token

#### google-drive
- **Purpose**: Google Drive file access and management
- **Transport**: HTTP
- **Use cases**: Document collaboration, file storage
- **Required**: Google Drive API credentials

---

### Cloud Services

#### aws
- **Purpose**: AWS service integration (S3, Lambda, DynamoDB, etc.)
- **Transport**: stdio
- **Use cases**: Cloud infrastructure, serverless, storage
- **Required**: AWS credentials

#### gcp
- **Purpose**: Google Cloud Platform integration
- **Transport**: stdio
- **Use cases**: Cloud resources, BigQuery, Cloud Storage
- **Required**: GCP credentials

---

### Data & Analytics

#### jupyter
- **Purpose**: Jupyter notebook integration
- **Transport**: stdio
- **Use cases**: Data analysis, interactive computing
- **Required**: Jupyter installation

#### pandas
- **Purpose**: Data manipulation with pandas
- **Transport**: stdio
- **Use cases**: Data analysis, data science workflows

---

## Installation Methods

### Method 1: CLI Command

**IMPORTANT SYNTAX - Correct Order**:
1. `--transport` flag and type
2. Server name
3. Environment variables with `-e KEY=value` or `--env KEY=value`
4. `--` separator
5. Command to run

```bash
# HTTP server
claude mcp add --transport http server-name https://api.example.com/mcp/

# stdio server (no environment variables)
claude mcp add --transport stdio server-name -- npx package-name

# With environment variables (CORRECT order: name, then -e, then --, then command)
claude mcp add --transport stdio server-name -e API_KEY=value -- npx package-name

# Multiple environment variables
claude mcp add --transport stdio server-name \
  -e KEY1=value1 \
  -e KEY2=value2 \
  -- npx package-name
```

**Security Warning**: NEVER use real credentials in examples or documentation. Use placeholder values like `your_key`, `your_token`, or `PLACEHOLDER_VALUE`.

### Method 2: Manual .mcp.json

Create or edit `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "postgres": {
      "type": "stdio",
      "command": "npx",
      "args": ["@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL:-postgresql://localhost:5432/defaultdb}"
      }
    }
  }
}
```

### Method 3: Using install_mcp.py

```bash
python3 scripts/install_mcp.py \
  --server github \
  --transport http \
  --url https://api.githubcopilot.com/mcp/ \
  --config /path/to/project/.mcp.json
```

## Environment Variables

MCP servers support environment variable expansion:

### Syntax

```json
{
  "env": {
    "VAR_NAME": "${VAR_NAME}",                    // Required, no default
    "VAR_WITH_DEFAULT": "${VAR_NAME:-default}",   // Optional with default
    "COMPOSED": "${PREFIX}_${SUFFIX}"             // Composition
  }
}
```

### Setting Environment Variables

#### macOS/Linux

```bash
# Temporary (current session)
export DATABASE_URL="postgresql://localhost:5432/mydb"

# Permanent (add to ~/.zshrc or ~/.bashrc)
echo 'export DATABASE_URL="postgresql://localhost:5432/mydb"' >> ~/.zshrc
source ~/.zshrc
```

#### Project-specific

Create `.env` file (don't commit!):

```bash
DATABASE_URL=postgresql://localhost:5432/mydb
BRAVE_API_KEY=your_api_key_here
```

**Important**: Add `.env` to `.gitignore`!

## Verification

After installing MCP servers:

```bash
# List all configured servers
claude mcp list

# Get details about a specific server
claude mcp get server-name

# Test connection (in Claude Code)
# Ask Claude: "Can you list my GitHub repositories?"
```

## Recommended Servers by Project Type

### Software Development
- **Essential**: `github`, `git`
- **Optional**: `postgres` or `sqlite` (if using database)

### Content Creation
- **Essential**: `brave-search` or `google-search`
- **Optional**: `notion`, `google-drive`

### Personal Tracking
- **Essential**: `sqlite`
- **Optional**: `filesystem`

### Data Analysis
- **Essential**: `postgres` or `sqlite`
- **Optional**: `jupyter`, `pandas`

### Automation
- **Essential**: None (bash is usually sufficient)
- **Optional**: `aws` or `gcp` (for cloud automation)

## Security Best Practices

1. **Never hardcode credentials** in `.mcp.json`
   - ✗ `"API_KEY": "sk-123456"`
   - ✓ `"API_KEY": "${API_KEY}"`

2. **Use environment variable defaults** for non-sensitive values
   - ✓ `"DATABASE_URL": "${DATABASE_URL:-postgresql://localhost:5432/dev}"`

3. **Add `.env` to `.gitignore`**
   ```gitignore
   .env
   .env.*
   *.env
   ```

4. **Restrict permissions** in `.claude/settings.json`
   ```json
   {
     "permissions": {
       "deny": [
         "Read(.env)",
         "Read(.env.*)"
       ]
     }
   }
   ```

5. **Review MCP server source code** before installation
   - Only install from trusted sources
   - Check npm package reputation
   - Review GitHub repository

## Troubleshooting

### Server Not Found

```bash
# Check if server is installed
claude mcp list

# Reinstall
claude mcp remove server-name
claude mcp add --transport [type] server-name [url/command]
```

### Environment Variable Not Set

```bash
# Check if variable is set
echo $DATABASE_URL

# Set it
export DATABASE_URL="your-connection-string"

# Or add to .env file
echo 'DATABASE_URL=your-connection-string' >> .env
```

### Connection Failed

1. Verify server is running (for HTTP servers)
2. Check credentials are correct
3. Verify network connectivity
4. Check firewall settings
5. Review server logs

## Creating Custom MCP Servers

You can create custom MCP servers for your specific needs. See the official MCP documentation at https://modelcontextprotocol.io for guides on:

- MCP protocol specification
- Server implementation examples
- Client integration
- Best practices

## Additional Resources

- **MCP Registry**: https://modelcontextprotocol.io
- **Claude Code Documentation**: https://code.claude.com/docs/en/mcp.md
- **Community MCP Servers**: Search GitHub for "mcp-server"
- **Official Servers**: https://github.com/modelcontextprotocol

---

For more information on using MCP servers in your projects, see the [Customization Guide](customization-guide.md).
