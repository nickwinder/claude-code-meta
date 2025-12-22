# Claude Code Best Practices

Best practices and conventions for Claude Code project setup.

## Project Structure

### Directory Organization

**Do:**
- Use `.claude/` directory for all Claude Code configuration
- Keep skills in `.claude/skills/skill-name/` directories
- Keep agents in `.claude/agents/` as `.md` files
- Use modular rules in `.claude/rules/` for complex projects

**Don't:**
- Put configuration files in project root (except `.mcp.json`)
- Mix Claude config with application code
- Create deeply nested directory structures

### File Naming

**Do:**
- Use kebab-case for skill and agent names (`code-reviewer`, not `codeReviewer`)
- Use `SKILL.md` (uppercase) for skill definitions
- Use `.template` extension for template files
- Use descriptive names that indicate purpose

**Don't:**
- Use spaces in file names
- Use special characters except hyphens and underscores
- Create generic names like `skill1.md` or `agent.md`

## Skill Design

### Skill Structure

**Good Skill:**
```yaml
---
name: analyze-code
description: Analyze code quality, identify issues, and suggest improvements for maintainability and performance
---

# Analyze Code

## Overview
This skill performs comprehensive code analysis...

## Workflow
1. Read target files
2. Analyze for common issues
3. Generate report

## Output
Structured report with...
```

**Poor Skill:**
```yaml
---
name: skill1
description: Does code stuff
---

Do code analysis.
```

### Skill Naming

**Do:**
- Use imperative verb-noun format: `review-code`, `deploy-app`, `analyze-data`
- Be specific: `log-workout` not `log-data`
- Match domain terminology

**Don't:**
- Use vague names: `helper`, `utility`, `tool`
- Use gerunds: `reviewing-code`, `deploying-app`
- Use generic terms: `do-thing`, `process`

### Skill Descriptions

**Do:**
- Start with "This skill should be used when..."
- Include specific use cases and examples
- Mention what inputs are needed
- Describe expected outputs

**Don't:**
- Write vague descriptions: "Helps with code"
- Forget to mention when to use the skill
- Assume Claude knows the context

### Skill Scope

**Do:**
- Keep skills focused on one capability
- Create multiple small skills rather than one large skill
- Make skills composable

**Don't:**
- Create mega-skills that do everything
- Duplicate functionality across skills
- Make skills too granular (one-liners)

## Agent Design

### Agent Purpose

**Do:**
- Create agents for specialized domains or roles
- Give agents clear expertise areas
- Define specific scenarios when to use each agent

**Don't:**
- Create agents that overlap heavily
- Make agents too general-purpose
- Forget to document agent capabilities

### Agent Prompts

**Do:**
- Define role clearly: "You are a senior backend engineer..."
- List specific expertise areas
- Provide concrete examples
- Set expectations for output format

**Don't:**
- Write generic prompts
- Forget to specify tools needed
- Leave behavior undefined

## Permission Management

### Permission Patterns

**Whitelist Approach (Recommended):**
```json
{
  "allow": [
    "Bash(npm:*)",
    "Bash(git:*)",
    "WebFetch(domain:github.com)"
  ],
  "deny": []
}
```

**Specific Over Broad:**
```json
{
  "allow": [
    "Bash(npm run test:*)",    // Specific test commands
    "Bash(npm run build:*)"    // Specific build commands
  ]
}
```

**Not:**
```json
{
  "allow": ["Bash(*)"]  // Too broad
}
```

### Sensitive Data

**Do:**
- Explicitly deny sensitive files:
```json
{
  "deny": [
    "Read(./.env)",
    "Read(./.env.*)",
    "Read(./secrets/**)",
    "Read(**/*.key)",
    "Read(**/*.pem)"
  ]
}
```

**Don't:**
- Allow unrestricted file access
- Commit secrets to repository
- Put API keys in `.claude/settings.json`

## Environment Variables

### MCP Server Configuration

**Do:**
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

**Don't:**
```json
{
  "env": {
    "DATABASE_URL": "postgresql://user:password@localhost:5432/db"  // Hardcoded secrets
  }
}
```

### Environment Variable Format

**Do:**
- Use expansion syntax: `${VAR:-default}`
- Provide sensible defaults
- Document required variables
- Use descriptive variable names

**Don't:**
- Hardcode values
- Use unclear variable names
- Forget to document variables

## Documentation

### CLAUDE.md

**Do:**
- Explain project purpose clearly
- Document workflows and processes
- List available skills and agents
- Include usage examples
- Keep updated as project evolves

**Don't:**
- Leave CLAUDE.md generic
- Forget to update after changes
- Write novels (keep concise)

### README.md

**Do:**
- Provide quick start instructions
- Link to detailed documentation
- Explain project structure
- Include setup requirements

**Don't:**
- Duplicate CLAUDE.md content
- Write for Claude (write for humans)
- Forget installation steps

## Version Control

### What to Commit

**Do commit:**
- `.claude/settings.json` (shared team settings)
- `.claude/CLAUDE.md` (project memory)
- `.claude/skills/` (project skills)
- `.claude/agents/` (project agents)
- `.mcp.json` (project MCP servers)
- `.gitignore` with Claude exclusions

**Don't commit:**
- `.claude/settings.local.json` (personal settings)
- `.claude.local.md` (personal notes)
- Secrets or API keys
- User-specific MCP servers in `.mcp.json`

### .gitignore

**Always include:**
```gitignore
.claude/settings.local.json
.claude.local.md
.env
.env.*
```

## Testing & Validation

### Before Committing

**Do:**
- Validate JSON syntax in settings and MCP configs
- Test YAML frontmatter in skills/agents
- Verify permission patterns work
- Test MCP server connections
- Review CLAUDE.md for accuracy

**Don't:**
- Commit without testing
- Assume configurations work
- Skip validation

### Validation Tools

**Use:**
```bash
# Validate JSON
python3 -m json.tool .claude/settings.json

# Validate project structure
python3 scripts/validate_project.py /path/to/project
```

## Naming Conventions Summary

| Item | Convention | Example |
|------|------------|---------|
| Skill directory | kebab-case | `log-workout/` |
| Skill name | kebab-case | `log-workout` |
| Agent file | kebab-case.md | `code-reviewer.md` |
| Agent name | kebab-case | `code-reviewer` |
| Template files | name.template | `settings.json.template` |
| Environment vars | UPPER_SNAKE_CASE | `DATABASE_URL` |

## Common Pitfalls

### Avoid These Mistakes

1. **Over-permissioning**: Granting too many permissions "just in case"
2. **Under-documentation**: Not explaining what skills/agents do
3. **Hardcoded values**: Putting secrets or environment-specific values in configs
4. **Generic naming**: Using vague names that don't describe purpose
5. **Monolithic skills**: Creating one massive skill instead of focused ones
6. **Forgetting validation**: Not testing configs before committing
7. **Stale documentation**: Not updating CLAUDE.md when project changes

## Progressive Enhancement

### Start Simple

1. Begin with base template
2. Add only necessary permissions
3. Create 1-2 core skills
4. Test thoroughly
5. Gradually add complexity

### Iterate Based on Need

- Add skills as needs arise
- Add agents when specialized expertise needed
- Add MCP servers when integrations needed
- Don't premature optimize

## Security Checklist

- [ ] Sensitive files excluded via `deny` permissions
- [ ] No hardcoded secrets in configuration
- [ ] Environment variables used for credentials
- [ ] `.gitignore` includes `.env` and local files
- [ ] Destructive commands restricted
- [ ] External URLs whitelisted by domain
- [ ] API keys in environment, not config files

## Quality Checklist

- [ ] All JSON files validated
- [ ] YAML frontmatter correct
- [ ] Skill descriptions are specific
- [ ] Agent prompts are detailed
- [ ] CLAUDE.md documents workflows
- [ ] README has setup instructions
- [ ] Examples work as documented
- [ ] Project structure is clean

Follow these practices to create maintainable, secure, and effective Claude Code projects!
