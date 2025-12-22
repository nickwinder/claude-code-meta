# Claude Code Mastery

A meta-project that specializes in creating optimized Claude Code project setups for different purposes.

## What is This?

Claude Code Mastery is a specialized Claude Code project that helps you create new, optimized Claude Code projects tailored to your specific needs. Think of it as a "project setup specialist" that:

- **Gathers your requirements** through interactive questions
- **Researches integrations** to find the best MCP servers for your use case
- **Generates custom skills** tailored to your project domain
- **Scaffolds complete projects** with best practices built-in
- **Handles MCP installation** interactively or provides clear instructions

## Quick Start

### 1. Open This Project in Claude Code

```bash
cd <project_location>
claude
```

### 2. Request a New Project

Simply ask Claude to create a project for your purpose:

```
Create a project for tracking my running workouts
```

or

```
Set up a Claude Code project for web application development
```

or

```
I need a project for data analysis with Python
```

### 3. Follow the Interactive Workflow

Claude will:
1. Ask clarifying questions about your needs
2. Recommend a template and integrations
3. Design custom skills for your workflows
4. Create the complete project structure
5. Help install MCP servers (with your approval)
6. Provide documentation and next steps

## Supported Project Types

| Project Type | Template | Best For |
|--------------|----------|----------|
| Software Development | `software-dev` | Web apps, APIs, CLI tools, libraries |
| Content Creation | `content-creation` | Blogs, articles, social media, marketing |
| Personal Tracking | `personal-tracker` | Fitness, habits, finance, goals |
| Data Analysis | `data-analysis` | Statistics, visualization, ML experiments |
| Automation | `automation` | Scripts, DevOps, workflows, tasks |
| Custom/Other | `base` | Any other purpose |

See [docs/supported-project-types.md](docs/supported-project-types.md) for detailed information.

## Features

### Interactive Discovery
- Asks targeted questions to understand your needs
- Validates requirements before proceeding
- Confirms understanding to ensure alignment

### Research-Driven Recommendations
- Auto-updates MCP server registry from web sources
- Researches latest integrations for your domain
- Scores and ranks recommendations by relevance

### Custom Skill Generation
- Uses `skill-generator` agent to create domain-specific skills
- Generates focused, well-documented skills
- Includes supporting scripts and references as needed

### Template Library
- Six pre-built templates for common use cases
- Variable substitution for personalization
- Easy to customize and extend

### MCP Server Integration
- Interactive installation (ask per server)
- Automatic configuration in `.mcp.json`
- Fallback to manual instructions if needed
- Environment variable handling

### Project Validation
- Validates JSON syntax
- Checks YAML frontmatter
- Verifies permission patterns
- Ensures configuration correctness

### Comprehensive Documentation
- Generates getting-started guides
- Documents available skills and agents
- Provides setup instructions
- Explains next steps

## How It Works

### Architecture

```
claude-code-meta/
├── .claude/
│   ├── skills/
│   │   └── project-creator/     # Main orchestration skill
│   │       ├── SKILL.md          # Complete workflow
│   │       └── references/       # Knowledge base
│   │           ├── mcp_servers.md
│   │           ├── project_types.md
│   │           └── best_practices.md
│   └── agents/
│       ├── project-architect.md  # Designs project structure
│       └── skill-generator.md    # Generates custom skills
├── templates/                    # Project templates
│   ├── base/
│   ├── software-dev/
│   ├── content-creation/
│   ├── personal-tracker/
│   ├── data-analysis/
│   └── automation/
├── scripts/                      # Python utilities
│   ├── init_project.py           # Project scaffolding
│   ├── validate_project.py       # Validation
│   ├── install_mcp.py            # MCP installation
│   └── update_registry.py        # Registry updates
└── docs/                         # Documentation
```

### Workflow

1. **Discovery**: Gather requirements through questions
2. **Research**: Select template, find MCP servers, design skills
3. **Recommendation**: Present plan and get approval
4. **Generation**: Create custom skills with agents
5. **Scaffolding**: Build project structure from template
6. **Integration**: Install MCP servers interactively
7. **Validation**: Verify project configuration
8. **Handoff**: Provide summary and next steps

## Example Usage

### Example 1: Running Tracker

**Request**: "Create a project for tracking my running workouts"

**Discovery**:
- Purpose: Running workout tracking
- Location: `/Users/you/running-tracker`
- Tasks: Log runs, analyze progress, export data

**Generated Project**:
```
running-tracker/
├── .claude/
│   ├── settings.json
│   ├── CLAUDE.md
│   └── skills/
│       ├── log-workout/          # Log runs with validation
│       ├── analyze-progress/     # Trends and insights
│       └── export-data/          # CSV/JSON export
├── data/workouts/
├── docs/getting-started.md
└── README.md
```

### Example 2: Web App Development

**Request**: "Set up a project for building a web application"

**Discovery**:
- Purpose: Web app development
- Location: `/Users/you/my-webapp`
- Stack: Node.js, React, PostgreSQL

**Generated Project**:
```
my-webapp/
├── .claude/
│   ├── settings.json             # npm, git, testing permissions
│   ├── CLAUDE.md
│   ├── skills/
│   │   ├── code-review/
│   │   ├── test-runner/
│   │   └── deploy-helper/
│   └── agents/
│       └── senior-developer.md
├── .mcp.json                     # github, git, postgres
├── docs/getting-started.md
└── README.md
```

## Requirements

- **Claude Code**: This project requires Claude Code CLI
- **Python 3.8+**: For utility scripts (standard library only)
- **Unix-like OS**: macOS or Linux (Windows with modifications)

## Documentation

- [Supported Project Types](docs/supported-project-types.md) - Detailed template guide
- [MCP Server Guide](docs/mcp-server-guide.md) - Available MCP servers
- [Customization Guide](docs/customization-guide.md) - How to customize templates

## Scripts

### init_project.py

Creates new project from template:

```bash
python3 scripts/init_project.py \
  --path /absolute/path/to/project \
  --template software-dev \
  --name "My Project"
```

### validate_project.py

Validates project configuration:

```bash
python3 scripts/validate_project.py /path/to/project
```

### install_mcp.py

Installs MCP server:

```bash
python3 scripts/install_mcp.py \
  --server github \
  --transport http \
  --url https://api.githubcopilot.com/mcp/ \
  --config /path/to/project/.mcp.json
```

### update_registry.py

Updates MCP server registry:

```bash
python3 scripts/update_registry.py --force
```

## Contributing

This is a personal project, but contributions are welcome:

1. Add new templates to `templates/`
2. Update MCP server registry in `.claude/skills/project-creator/references/mcp_servers.md`
3. Improve skill/agent prompts
4. Enhance documentation

## License

MIT License - feel free to use and modify

## Credits

Created using Claude Code best practices and patterns from the official documentation at https://code.claude.com/docs

---

**Built with ❤️ using Claude Code**
