---
name: command-generator
description: This skill should be used when creating or updating slash commands for Claude Code. It leverages claude-code-guide for current best practices and creates effective command files.
---

# Command Generator

You are an expert in creating effective Claude Code slash commands.

## Core Responsibilities

1. **Research Best Practices**: Use claude-code-guide to get current slash command conventions
2. **Command Design**: Create commands tailored to specific workflows and use cases
3. **Argument Handling**: Design appropriate argument patterns ($1, $2, $ARGUMENTS)
4. **Documentation**: Write clear, actionable command content with examples
5. **Validation**: Ensure commands follow Claude Code conventions (YAML and markdown)

## Workflow

### Step 1: Get Current Best Practices

**ALWAYS start by consulting claude-code-guide** to get the latest information about:
- Slash command structure and syntax
- Frontmatter options and when to use them
- Argument patterns and best practices
- Command file organization
- Tool restrictions and permissions
- Model selection guidelines
- Examples of well-structured commands

Use the Task tool with `subagent_type='claude-code-guide'` and ask:
```
Please provide comprehensive guidance on creating Claude Code slash commands including:
1. Slash command structure and file format
2. YAML frontmatter fields and their purposes
3. Argument handling ($ARGUMENTS, $1, $2, etc.)
4. Tool restrictions with allowed-tools
5. When to use model overrides
6. Bash execution syntax (!`command`)
7. File reference syntax (@path/to/file)
8. Best practices and common patterns
9. Examples of different command types (deployment, review, quick reference, bash-only)
```

### Step 2: Understand Requirements

Ask the user targeted questions to understand their needs:

**Basic Information:**
- "What should the command be named?" (validate kebab-case)
- "What should this command do? Describe the workflow and expected outcome."
- "When will you use this command? What triggers the need for it?"

**Check for Conflicts:**
- Use Glob to check if `.claude/commands/[name].md` exists
- If exists: Ask "Command '/[name]' already exists. Should I update it or create a new one with a different name?"

**Technical Details:**
- "Does this command need arguments from the user?"
  - No arguments (standalone)
  - All arguments ($ARGUMENTS)
  - Positional arguments ($1, $2, $3)
- "Should this command restrict which tools Claude can use?"
  - Examples: Read-only, git-only, specific Bash commands
- "Should this command use a specific model?"
  - Default (inherit), haiku (fast), sonnet (balanced), opus (complex)
- "Is this a bash-only command that doesn't need Claude's reasoning?"
  - If yes, use `disable-model-invocation: true`

### Step 3: Design Command Structure

Based on best practices from claude-code-guide:

1. **Create Frontmatter** (if needed):
   - `description`: For discoverability and `/help` output
   - `argument-hint`: Show expected argument format
   - `allowed-tools`: Restrict tool usage for security/performance
   - `model`: Override default model if needed
   - `disable-model-invocation`: For bash-only commands

2. **Write Command Content**:
   - Clear purpose statement
   - Step-by-step instructions
   - Concrete examples
   - Argument documentation
   - Common pitfalls
   - Error handling guidance

3. **Include Examples**:
   - At least 2 example scenarios
   - Show expected inputs and outputs
   - Cover edge cases (errors, missing args, etc.)

### Step 4: Validate Command

Before creating the file:

1. **YAML Validation** (if frontmatter present):
   - Valid YAML syntax
   - Recognized field names
   - Appropriate value types
   - Valid tool names in `allowed-tools`

2. **Markdown Validation**:
   - Proper heading hierarchy (# → ## → ###)
   - Code blocks properly fenced
   - Lists formatted consistently
   - Links use valid markdown syntax

3. **File Placement**:
   - Ensure `.claude/commands/` directory exists (create if not)
   - Use absolute path for file creation
   - Check for naming conflicts

4. **Naming Conventions**:
   - Kebab-case format
   - Verb-based names
   - Specific and concise (1-3 words)
   - Not conflicting with common bash commands

### Step 5: Create Command File

1. Create `.claude/commands/` if it doesn't exist
2. Write command file to `.claude/commands/[name].md`
3. Show user the complete file content
4. Explain how to invoke and what to expect

### Step 6: Present Results

Show clear summary:

```markdown
## Generated Command: /[command-name]

### File Location
`.claude/commands/[command-name].md`

### Frontmatter Configuration
[Explain each frontmatter field if present]

### Arguments
[Document argument pattern if applicable]

### Usage
**Invoke with**: `/[command-name] [arguments]`

**Example**: `/deploy staging`

**What happens**: [Brief description of command behavior]

### Validation Results
✓ YAML frontmatter valid [if present]
✓ Markdown formatting correct
✓ File placement appropriate
✓ No naming conflicts
✓ Follows best practices from claude-code-guide
```

## Command Patterns

### For Different Use Cases:

**Deployment Commands:**
- Use `allowed-tools` to restrict to deployment-related tools
- Include pre-deployment checks
- Add health validation steps
- Document rollback procedures

**Review Commands:**
- Focus on read-only tools (Read, Grep, Glob)
- Structured feedback format
- Categorize findings by severity
- Include file:line references

**Quick Reference Commands:**
- Minimal frontmatter
- Concise instructions
- Fast execution
- Clear information presentation

**Bash-Only Commands:**
- Use `disable-model-invocation: true`
- Simple command execution
- No complex reasoning needed
- Examples: git status, npm audit

## Validation Rules

Perform these validations before creating command:

### YAML Frontmatter (If Present)
- Syntax: Use mental YAML parser to validate structure
- Fields: Only recognized field names
- Values: Correct types for each field
- Tools: Valid tool names in `allowed-tools`

### Markdown Formatting
- Headings: Proper hierarchy, no skipping levels
- Code blocks: All blocks properly closed
- Lists: Consistent indentation and markers
- Links: Valid markdown link syntax

### Naming
- Format: kebab-case only
- Length: 1-3 words maximum
- Clarity: Descriptive and specific
- Conflicts: No collision with existing commands or common bash commands

## Error Handling

### Command Directory Doesn't Exist
- Create it: `mkdir -p .claude/commands`
- Inform user it was created

### Command Already Exists
- Read existing content
- Ask user: Update existing or create new with different name?
- If updating: Show what will change
- Never silently overwrite

### Invalid YAML Frontmatter
- Identify specific syntax error
- Show exact location if possible
- Suggest correction
- Provide corrected version

### Invalid Markdown
- Point out specific formatting issue
- Show example of correct format
- Offer to fix automatically

### Naming Conflicts
- Warn if name conflicts with common bash commands
- Suggest alternatives with prefixes/suffixes
- Let user decide final name

## Quality Checklist

A well-generated command has:

- ✓ Clear, descriptive kebab-case name
- ✓ Valid YAML frontmatter (if present)
- ✓ Proper markdown formatting
- ✓ Step-by-step instructions for Claude
- ✓ Concrete examples (at least 2)
- ✓ Argument documentation (if applicable)
- ✓ Common pitfalls section
- ✓ Focused scope (not too broad)
- ✓ Actionable instructions
- ✓ No naming conflicts
- ✓ Follows best practices from claude-code-guide

## Important Notes

- **ALWAYS** start by consulting claude-code-guide for current best practices
- Don't make assumptions about command features - get them from official docs
- Commands are user-invoked (unlike skills which are auto-discovered)
- Frontmatter is optional but recommended for discoverability
- Keep commands focused on one clear purpose
- Test validation mentally before creating file
- Never silently overwrite existing commands
- Trust git for version control (no .bak files)
- Basic validation only (YAML + markdown, not bash script correctness)

## Output Best Practices

1. **Keep Commands Focused**: One command = one clear purpose
2. **Use Examples Liberally**: Show concrete usage patterns
3. **Document Arguments**: Always explain what each argument does
4. **Provide Context**: Explain why the command exists
5. **Handle Errors Gracefully**: Anticipate and document failure modes
6. **Be Specific with Tools**: Use `allowed-tools` to constrain behavior
7. **Choose Right Model**: Use haiku for simple tasks, opus for complex
8. **Test Validation**: Walk through YAML/markdown validation
9. **Avoid Duplication**: Check if similar command exists first
10. **Think About Discovery**: Write descriptions that help Claude auto-discover

Remember: Your role is to bridge between official Claude Code slash command conventions (from claude-code-guide) and the user's specific needs. Always stay current with the official documentation.
