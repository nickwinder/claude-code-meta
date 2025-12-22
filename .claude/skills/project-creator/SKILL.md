---
name: project-creator
description: This skill should be used when users want to create a new optimized Claude Code project setup for a specific purpose (software development, content creation, data analysis, personal tracking, automation, etc.). It orchestrates requirement gathering, integration research, custom skill generation, and complete project scaffolding.
---

# Project Creator

## Overview

This skill orchestrates the complete workflow for creating optimized Claude Code project setups. It handles interactive requirement gathering, integration research, custom skill generation, and project scaffolding.

## When to Use This Skill

Trigger this skill when users:
- Request creation of a new Claude Code project
- Ask for help setting up a project for a specific purpose
- Want a specialized Claude Code environment
- Need recommendations for project structure and integrations

## Main Workflow

### Phase 1: Discovery (Interactive Questioning)

Before generating anything, gather comprehensive requirements through targeted questions using the AskUserQuestion tool.

#### Required Questions

1. **Project Purpose & Domain**
   ```
   Question: "What will this project be used for?"
   Examples: software development, content creation, running tracker, data analysis, automation
   Follow-up: "What specific tasks or workflows will you be performing?"
   ```

2. **Project Location**
   ```
   Question: "Where should I create this project? (provide absolute path)"
   Example: /Users/username/projects/my-project
   Validation: Check that parent directory exists using ls command
   ```

3. **Custom Requirements** (Optional)
   ```
   Question: "Do you have specific requirements or constraints?"
   Examples: specific MCP servers, permissions, skills, or integrations
   ```

#### Confirmation
After gathering requirements, summarize understanding and confirm with user before proceeding.

### Phase 2: Research & Recommendations

1. **Auto-Update Check**
   - Check age of `references/mcp_servers.md` file
   - If older than 7 days, run `python3 scripts/update_registry.py --force`
   - Cache results for this session

2. **Template Selection**
   - Analyze project purpose against available templates
   - Review `references/project_types.md` for patterns
   - Select template: `base`, `software-dev`, `content-creation`, `personal-tracker`, `data-analysis`, or `automation`

3. **MCP Server Discovery**
   - Read `references/mcp_servers.md` for curated servers
   - Filter by project domain keywords
   - Use WebSearch to find domain-specific integrations: "MCP server for [domain] 2025"
   - Score servers by relevance, maturity, and use case fit
   - Select top 3-5 recommendations

4. **Best Practices Review**
   - Read `references/best_practices.md`
   - Read `references/project_types.md` for domain patterns
   - Apply relevant conventions

5. **Custom Skill Design**
   - Analyze workflows from user requirements
   - Design 2-4 core skills tailored to domain
   - Use verb-noun naming: `log-workout`, `analyze-progress`, `deploy-app`
   - Plan skill workflows and required resources

### Phase 3: Recommendation & Approval

Present a comprehensive plan to the user:

```
Based on your requirements, here's what I recommend:

**Template**: [template-name]
Reason: [why this template fits]

**MCP Servers**: (will ask interactively for each)
1. [server-name]: [purpose and benefit]
2. [server-name]: [purpose and benefit]
3. [server-name]: [purpose and benefit]

**Custom Skills**:
1. [skill-name]: [what it does]
2. [skill-name]: [what it does]
3. [skill-name]: [what it does]

**Project Structure**:
[key directories and their purposes]

Does this match your needs? Would you like to adjust anything?
```

Get user approval or iterate based on feedback.

### Phase 4: Custom Skill Generation

For each designed skill, invoke the `skill-generator` agent:

```
Use the Task tool with subagent_type='skill-generator'

Provide context:
- Project purpose and domain
- Skill name and description
- Expected workflow steps
- Required tools and resources
- Example use cases

Agent will generate:
- SKILL.md with proper YAML frontmatter
- Supporting scripts (if needed)
- Reference documentation
- Templates/assets
```

Store generated skill content for Phase 5.

### Phase 5: Project Scaffolding

1. **Execute init_project.py**
   ```bash
   python3 scripts/init_project.py \
     --path [absolute-path-from-user] \
     --template [selected-template] \
     --name "[project-name]" \
     --description "[project-description]"
   ```

2. **Install Custom Skills**
   For each generated skill from Phase 4:
   - Create directory: `[project-path]/.claude/skills/[skill-name]/`
   - Write `SKILL.md` file
   - Copy any scripts to `scripts/` subdirectory
   - Copy any references to `references/` subdirectory

3. **Generate Agents** (if designed in Phase 2)
   For each agent:
   - Create `[project-path]/.claude/agents/[agent-name].md`
   - Include YAML frontmatter with name, description, model

4. **Create Documentation**
   - Generate `docs/getting-started.md` with:
     - Quick start instructions
     - How to use each skill
     - How to invoke agents
     - MCP server setup (if pending)

### Phase 6: MCP Integration (Interactive Mode)

For each recommended MCP server:

1. **Present Server Information**
   ```
   MCP Server: [server-name]
   Purpose: [what it does]
   Benefits: [why it's useful for this project]
   Installation: [installation command]
   ```

2. **Ask User Choice**
   ```
   Use AskUserQuestion with options:
   - "Install now" (recommended)
   - "Provide manual instructions"
   ```

3. **If Install Now**:
   ```bash
   python3 scripts/install_mcp.py \
     --server [server-name] \
     --transport [http|stdio|sse] \
     --url [url-if-http] \
     --command [command-if-stdio] \
     --config [project-path]/.mcp.json
   ```
   Verify: Run `claude mcp list` to confirm

4. **If Manual Instructions**:
   - Append to `docs/setup-instructions.md`:
     ```markdown
     ## [server-name]

     Purpose: [description]

     Install:
     ```bash
     [installation-command]
     ```

     Configuration: Add to .mcp.json:
     ```json
     [config-json]
     ```
     ```

### Phase 7: Validation

1. **Execute validate_project.py**
   ```bash
   python3 scripts/validate_project.py [project-path]
   ```

2. **Review Output**
   - Check for JSON syntax errors
   - Verify YAML frontmatter valid
   - Confirm permissions well-formed
   - Ensure MCP configs valid

3. **Fix Issues**
   If validation finds errors:
   - Fix automatically if possible (JSON syntax)
   - Report to user if manual fix needed
   - Re-validate after fixes

### Phase 8: Handoff

1. **Generate Summary Report**
   ```markdown
   # Project Created Successfully!

   **Location**: [project-path]
   **Template**: [template-name]
   **Created**: [timestamp]

   ## Files Created
   - Configuration: [list]
   - Skills: [list with descriptions]
   - Agents: [list with descriptions]
   - Documentation: [list]

   ## MCP Servers
   ### Installed
   - [list of installed servers]

   ### Pending Manual Installation
   - [list with references to docs/setup-instructions.md]

   ## Next Steps
   1. Navigate to project: `cd [project-path]`
   2. [If MCP pending] Set up MCP servers (see docs/setup-instructions.md)
   3. [If env vars needed] Set environment variables: [list]
   4. Open in Claude Code: `claude`
   5. Test skills: Try "/[skill-name]" or describe a task
   6. Review documentation: Read docs/getting-started.md

   ## Available Skills
   - [skill-name]: [description]
   - [skill-name]: [description]

   ## Available Agents
   - [agent-name]: [description]
   ```

2. **Present to User**
   Display the summary report clearly formatted

## Helper Functions

### Template Selection Logic

```
Keywords → Template mapping:
- "software", "code", "app", "api", "development" → software-dev
- "blog", "content", "writing", "article", "social media" → content-creation
- "track", "log", "monitor", "fitness", "habit", "finance" → personal-tracker
- "data", "analysis", "visualization", "statistics", "ml" → data-analysis
- "automation", "script", "workflow", "devops", "task" → automation
- Default → base
```

### MCP Server Scoring

```
Score = (Relevance × 3) + (Maturity × 2) + (Fit × 2)

Relevance: Does it match project domain? (0-5)
Maturity: Well-documented and maintained? (0-5)
Fit: Solves specific user needs? (0-5)

Recommend if Score >= 15
Ask user if 10 <= Score < 15
Skip if Score < 10
```

### Skill Naming Patterns

```
Good names (verb-noun):
- log-workout (not log-data)
- analyze-progress (not analyze)
- deploy-app (not deploy)
- review-code (not reviewer)
- export-data (not export)

Bad names:
- helper, utility, tool (too vague)
- do-stuff, process (not descriptive)
- log-data-entry (too verbose)
```

## Error Handling

### Common Issues & Responses

1. **Parent directory doesn't exist**
   - Use AskUserQuestion: "The directory doesn't exist. Should I create it?"
   - If yes: mkdir -p [parent-dir]
   - If no: Ask for different path

2. **Project directory already exists**
   - Use AskUserQuestion: "Directory exists. Continue and potentially overwrite?"
   - If no: Ask for different path

3. **MCP server installation fails**
   - Report specific error
   - Automatically switch to manual instructions mode
   - Document in docs/setup-instructions.md

4. **Validation fails**
   - Report specific errors
   - Attempt automatic fixes (JSON formatting)
   - Re-validate after fixes

5. **Script execution errors**
   - Check Python availability
   - Verify script paths correct
   - Report detailed error messages

## Resources & References

### Available Resources

- **`references/mcp_servers.md`**: Curated MCP server registry by category
- **`references/project_types.md`**: Common project patterns and recommendations
- **`references/best_practices.md`**: Claude Code conventions and patterns

### Scripts

- **`scripts/init_project.py`**: Creates project structure from templates
- **`scripts/validate_project.py`**: Validates project configuration
- **`scripts/install_mcp.py`**: Installs MCP servers
- **`scripts/update_registry.py`**: Updates MCP server registry

### Agents

- **`project-architect`**: Expert in project design and architecture
- **`skill-generator`**: Generates custom skills for specific domains

## Examples

### Example 1: Running Tracker

**User Request**: "Create a project for tracking my running workouts"

**Discovery**:
- Purpose: Running workout tracking
- Tasks: Log runs, analyze progress, export data
- Location: /Users/user/running-tracker

**Recommendations**:
- Template: personal-tracker
- MCP Servers: sqlite (local data storage)
- Skills: log-workout, analyze-progress, export-data

**Generated Structure**:
```
/Users/user/running-tracker/
├── .claude/
│   ├── settings.json
│   ├── CLAUDE.md
│   └── skills/
│       ├── log-workout/SKILL.md
│       ├── analyze-progress/SKILL.md
│       └── export-data/SKILL.md
├── data/workouts/
├── docs/getting-started.md
└── README.md
```

### Example 2: Web App Development

**User Request**: "Set up a project for building a web application"

**Discovery**:
- Purpose: Web app development
- Tasks: Frontend/backend code, API development, testing
- Location: /Users/user/projects/my-webapp

**Recommendations**:
- Template: software-dev
- MCP Servers: github, git, postgres
- Skills: code-review, test-runner, deploy-helper

**Generated Structure**:
```
/Users/user/projects/my-webapp/
├── .claude/
│   ├── settings.json
│   ├── CLAUDE.md
│   ├── skills/
│   │   ├── code-review/SKILL.md
│   │   ├── test-runner/SKILL.md
│   │   └── deploy-helper/SKILL.md
│   └── agents/
│       └── senior-developer.md
├── .mcp.json
├── docs/getting-started.md
└── README.md
```

## Important Notes

- Always use absolute paths (not relative paths)
- Validate all JSON/YAML before writing
- Test MCP server configs when possible
- Document environment variables clearly
- Use the Task tool for invoking agents
- Keep user informed at each phase
- Handle errors gracefully with clear messages
- Provide comprehensive documentation

## Success Criteria

Project creation is successful when:
- ✓ All files generated without errors
- ✓ JSON/YAML syntax valid
- ✓ Skills have proper YAML frontmatter
- ✓ MCP servers installed or documented
- ✓ Documentation complete and helpful
- ✓ User understands next steps
- ✓ Validation passes
