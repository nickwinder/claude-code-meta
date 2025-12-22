# Customization Guide

How to customize generated Claude Code projects and the Claude Code Mastery meta-project itself.

## Customizing Generated Projects

After creating a project with Claude Code Mastery, you can customize it to fit your exact needs.

### 1. Modifying Permissions

Edit `.claude/settings.json` in your project:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm:*)",           // Keep existing
      "Bash(yarn:*)",          // Keep existing
      "Bash(docker:*)"         // Add new permission
    ],
    "deny": [
      "Read(.env)",            // Keep existing
      "Bash(rm -rf:*)"         // Add new restriction
    ],
    "defaultMode": "acceptEdits"
  }
}
```

**Permission patterns**:
- Tool-specific: `Bash(command:*)`, `Read(path/*)`, `WebFetch(domain:example.com)`
- Wildcards: `*` matches any characters
- Deny takes precedence over allow

### 2. Adding MCP Servers

Add to `.mcp.json`:

```json
{
  "mcpServers": {
    "existing-server": {
      "type": "http",
      "url": "https://example.com/mcp"
    },
    "new-server": {
      "type": "stdio",
      "command": "npx",
      "args": ["@scope/package-name"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

Or use the CLI:

```bash
cd your-project
claude mcp add --transport stdio new-server -- npx @scope/package-name
```

### 3. Creating Custom Skills

1. **Create skill directory**:
   ```bash
   mkdir -p .claude/skills/my-custom-skill
   ```

2. **Create SKILL.md**:
   ```markdown
   ---
   name: my-custom-skill
   description: This skill should be used when [specific scenario]. It [what it does].
   ---

   # My Custom Skill

   ## Overview
   [What this skill does]

   ## Workflow
   1. [Step 1]
   2. [Step 2]
   3. [Step 3]

   ## Examples
   [Concrete examples]
   ```

3. **Test the skill**:
   Open Claude Code and try invoking: "Use my-custom-skill to..."

### 4. Adding Custom Agents

Create `.claude/agents/my-agent.md`:

```markdown
---
name: my-agent
description: Use this agent when [scenario]. Provides [expertise].
model: sonnet
---

You are a [role] with expertise in [areas].

## Responsibilities
1. [Responsibility 1]
2. [Responsibility 2]

## Approach
[How the agent should work]
```

### 5. Updating CLAUDE.md

Edit `.claude/CLAUDE.md` to add project-specific guidelines:

```markdown
# My Project

## Purpose
[Clear project purpose]

## Workflows
[Describe your specific workflows]

## Coding Standards
[Your standards and conventions]

## Available Skills
- my-custom-skill: [description]

## Available Agents
- my-agent: [description]
```

### 6. Adding Project-Specific Rules

Create `.claude/rules/my-rules.md`:

```markdown
# My Custom Rules

## Code Style
- Use 2 spaces for indentation
- Max line length: 100 characters
- Use single quotes for strings

## Testing
- All features must have tests
- Minimum coverage: 80%

## Documentation
- Public APIs must be documented
- Include examples in docstrings
```

Reference in CLAUDE.md:

```markdown
## Rules
See `.claude/rules/my-rules.md` for project-specific conventions.
```

## Customizing Claude Code Mastery

### Adding New Templates

1. **Create template directory**:
   ```bash
   mkdir -p templates/my-template/.claude
   ```

2. **Create template files**:
   ```bash
   touch templates/my-template/.claude/settings.json.template
   touch templates/my-template/.claude/CLAUDE.md.template
   touch templates/my-template/.gitignore.template
   touch templates/my-template/README.md.template
   ```

3. **Use template variables**:
   - `{{PROJECT_NAME}}` - Project display name
   - `{{PROJECT_PATH}}` - Absolute path
   - `{{PROJECT_TYPE}}` - Template name
   - `{{TIMESTAMP}}` - Creation time
   - `{{DESCRIPTION}}` - Project description

4. **Update init_project.py**:
   Add your template name to the choices:
   ```python
   parser.add_argument(
       '--template',
       choices=['base', 'software-dev', '...', 'my-template'],
       help='Template to use'
   )
   ```

### Adding MCP Servers to Registry

Edit `.claude/skills/project-creator/references/mcp_servers.md`:

```markdown
### my-new-server
- **Purpose**: What it does
- **Transport**: stdio|http|sse
- **Install**: `claude mcp add ...`
- **Config**:
```json
{
  "type": "...",
  "url": "..." or "command": "..."
}
```
- **Use cases**: When to recommend
- **Docs**: Link to documentation
```

### Customizing Skill Patterns

Edit `.claude/agents/skill-generator.md` to add new skill patterns for specific domains.

### Updating Best Practices

Edit `.claude/skills/project-creator/references/best_practices.md` with your organization's conventions.

### Customizing Project Types

Edit `.claude/skills/project-creator/references/project_types.md` to add or modify project type patterns.

## Advanced Customization

### Custom Script Integration

Add helper scripts to generated projects:

1. **Create script template**:
   ```bash
   mkdir -p templates/my-template/scripts
   ```

2. **Add script with template variables**:
   ```python
   #!/usr/bin/env python3
   """
   {{PROJECT_NAME}} - Custom Script
   """

   PROJECT_PATH = "{{PROJECT_PATH}}"

   # Script logic here
   ```

3. **Script gets copied** during project initialization

### Multi-File Skills

Create complex skills with multiple resources:

```
.claude/skills/complex-skill/
├── SKILL.md                    # Main skill definition
├── scripts/
│   ├── helper.py               # Python helper
│   └── process.sh              # Bash helper
├── references/
│   ├── api-docs.md             # API documentation
│   └── examples.md             # Usage examples
└── templates/
    └── config.json.template    # Config template
```

Reference in SKILL.md:

```markdown
## Resources

### Scripts
- `scripts/helper.py`: [description]
- `scripts/process.sh`: [description]

### References
- [API Documentation](references/api-docs.md)
- [Examples](references/examples.md)

### Templates
Use `templates/config.json.template` for configuration.
```

### Environment-Specific Settings

Create local settings that override project settings:

`.claude/settings.local.json` (gitignored):

```json
{
  "permissions": {
    "allow": [
      "Bash(my-custom-command:*)"
    ]
  },
  "env": {
    "LOCAL_ENV_VAR": "value"
  }
}
```

Precedence: Local > Project > User > Enterprise

### Custom Validation Rules

Extend `scripts/validate_project.py`:

```python
def validate_custom_rule(project_path: Path) -> tuple[bool, str]:
    """Custom validation logic."""
    # Your validation code
    return True, "Custom validation passed"

# Add to validate_project function
valid, message = validate_custom_rule(project_dir)
if not valid:
    errors.append(f"Custom rule: {message}")
```

## Tips and Best Practices

### 1. Start Small
- Begin with minimal customization
- Add features as needed
- Avoid over-engineering

### 2. Test Changes
- Validate JSON/YAML syntax
- Test skills before committing
- Run validation script

### 3. Document Customizations
- Update CLAUDE.md
- Add comments to configs
- Explain non-obvious choices

### 4. Version Control
- Commit project settings
- Gitignore local settings
- Track template changes

### 5. Iterate
- Refine based on usage
- Remove unused features
- Simplify complex setups

## Troubleshooting Customizations

### Permission Denied

**Problem**: Claude can't access a tool or file

**Solution**:
1. Check `.claude/settings.json` permissions
2. Add required permission to `allow` array
3. Verify pattern matches (use wildcards correctly)

### Skill Not Loading

**Problem**: Skill doesn't appear or work

**Solution**:
1. Verify YAML frontmatter format
2. Check for syntax errors
3. Ensure `name` and `description` are present
4. Validate file is in `.claude/skills/skill-name/SKILL.md`

### MCP Server Not Working

**Problem**: MCP server fails to connect

**Solution**:
1. Verify installation: `claude mcp list`
2. Check environment variables are set
3. Test connection manually
4. Review `.mcp.json` syntax

### Template Variables Not Substituting

**Problem**: `{{VARIABLE}}` appears in generated files

**Solution**:
1. Check template file has `.template` extension
2. Verify variable name is correct
3. Ensure `init_project.py` is being used
4. Check for typos in variable names

## Examples

### Example 1: Adding Docker Support

**Goal**: Add Docker commands to software-dev projects

**Steps**:

1. Edit project's `.claude/settings.json`:
   ```json
   {
     "permissions": {
       "allow": [
         "Bash(docker:*)",
         "Bash(docker-compose:*)"
       ]
     }
   }
   ```

2. Create Docker skill:
   ```bash
   mkdir -p .claude/skills/docker-helper
   ```

3. Create `.claude/skills/docker-helper/SKILL.md`:
   ```yaml
   ---
   name: docker-helper
   description: This skill should be used when working with Docker containers. It helps with building, running, and debugging containers.
   ---

   # Docker Helper

   ## Workflow
   1. Determine Docker operation needed
   2. Execute appropriate docker command
   3. Handle errors and provide feedback
   ```

### Example 2: Custom Data Validation

**Goal**: Add custom validation for running tracker

**Steps**:

1. Create validation skill:
   ```markdown
   ---
   name: validate-workout
   description: Validate workout data before logging
   ---

   # Validate Workout

   ## Validation Rules
   - Distance: > 0, < 50 miles
   - Duration: > 0, < 300 minutes
   - Pace: Calculated from distance/duration
   - Heart rate: 40-220 bpm (if provided)
   - Date: Valid format, not in future
   ```

2. Reference in log-workout skill:
   ```markdown
   ## Workflow
   1. Gather workout data
   2. **Use validate-workout skill** for validation
   3. Store if valid
   4. Report errors if invalid
   ```

## Additional Resources

- [Claude Code Documentation](https://code.claude.com/docs)
- [MCP Protocol](https://modelcontextprotocol.io)
- [JSON Schema](https://json-schema.org/)
- [YAML Specification](https://yaml.org/)

---

For questions or issues, refer to the main [README.md](../README.md) or Claude Code documentation.
