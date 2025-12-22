# Supported Project Types

Detailed guide to the project templates available in Claude Code Mastery.

## Overview

Claude Code Mastery provides six pre-built templates optimized for different use cases. Each template includes:

- Pre-configured permissions
- Recommended MCP servers
- Suggested custom skills
- Domain-specific guidelines
- Best practices

## Template Selection Guide

Use this flowchart to select the right template:

```
What are you building?

├─ Writing code/apps? → software-dev
├─ Writing content/articles? → content-creation
├─ Tracking personal data? → personal-tracker
├─ Analyzing data/datasets? → data-analysis
├─ Creating automation scripts? → automation
└─ Something else? → base
```

---

## 1. Software Development (`software-dev`)

**Best for:**
- Web applications (frontend, backend, fullstack)
- API development
- CLI tools and utilities
- Libraries and packages
- Mobile applications

**Permissions:**
```json
{
  "allow": [
    "Bash(npm:*)", "Bash(yarn:*)", "Bash(node:*)",
    "Bash(python3:*)", "Bash(pip:*)", "Bash(pytest:*)",
    "Bash(git:*)", "Bash(cargo:*)", "Bash(go:*)",
    "WebFetch(domain:github.com)",
    "WebFetch(domain:stackoverflow.com)"
  ]
}
```

**Recommended MCP Servers:**
- `github` - Repository and issue management
- `git` - Local git operations
- `postgres` or `sqlite` - Database access

**Suggested Skills:**
- `code-review` - Automated code review
- `test-runner` - Execute and analyze tests
- `deploy-helper` - Deployment assistance
- `refactor-guide` - Refactoring suggestions

**Suggested Agents:**
- `senior-developer` - Architecture guidance
- `qa-engineer` - Testing and quality
- `devops-specialist` - Deployment and infrastructure

**Example Projects:**
- REST API with Node.js
- React web application
- Python CLI tool
- Rust systems programming

---

## 2. Content Creation (`content-creation`)

**Best for:**
- Blog writing
- Article creation
- Social media content
- Email newsletters
- Marketing copy
- Documentation

**Permissions:**
```json
{
  "allow": [
    "WebSearch",
    "WebFetch(domain:*)",
    "Bash(wc:*)"
  ]
}
```

**Recommended MCP Servers:**
- `brave-search` - Web research
- `notion` - Knowledge management (optional)
- `google-drive` - Document collaboration (optional)

**Suggested Skills:**
- `draft-content` - Content creation with guidelines
- `seo-optimize` - SEO analysis and improvements
- `publish-workflow` - Multi-platform publishing
- `research-topic` - Research and source gathering

**Suggested Agents:**
- `content-strategist` - Content planning
- `seo-specialist` - SEO optimization
- `copy-editor` - Grammar and style

**Example Projects:**
- Technical blog
- Marketing content library
- Newsletter management
- Social media calendar

---

## 3. Personal Tracking (`personal-tracker`)

**Best for:**
- Fitness and health tracking
- Habit tracking
- Finance tracking
- Time tracking
- Goal tracking
- Any personal data logging

**Permissions:**
```json
{
  "allow": [
    "Bash(python3:*)",
    "Bash(ls:*)", "Bash(cat:*)", "Bash(grep:*)"
  ]
}
```

**Recommended MCP Servers:**
- `sqlite` - Local database storage
- `filesystem` - Enhanced file operations (optional)

**Suggested Skills:**
- `log-entry` - Structured data entry with validation
- `analyze-trends` - Statistical analysis and insights
- `generate-report` - Automated reporting
- `export-data` - Data export (CSV, JSON, PDF)

**Suggested Agents:**
- `data-analyst` - Trend analysis
- `report-generator` - Report automation

**Data Structure:**
```
project/
├── data/
│   └── entries/      # JSON files organized by month
├── scripts/          # Analysis scripts
├── reports/          # Generated reports
└── .claude/
```

**Example Projects:**
- Running workout tracker
- Daily habit tracker
- Personal finance log
- Time and productivity tracker
- Health metrics tracker

---

## 4. Data Analysis (`data-analysis`)

**Best for:**
- Statistical analysis
- Data visualization
- Machine learning experiments
- Research projects
- Business intelligence
- Scientific computing

**Permissions:**
```json
{
  "allow": [
    "Bash(python3:*)", "Bash(pip:*)",
    "Bash(jupyter:*)",
    "WebFetch(domain:pypi.org)"
  ]
}
```

**Recommended MCP Servers:**
- `postgres` or `sqlite` - Database access
- `jupyter` - Notebook integration
- `pandas` - Data manipulation (if available)

**Suggested Skills:**
- `load-data` - Data ingestion and validation
- `clean-data` - Data cleaning and preprocessing
- `analyze-dataset` - Statistical analysis
- `visualize-trends` - Chart generation
- `export-results` - Result reporting

**Suggested Agents:**
- `data-scientist` - Analysis methodology
- `ml-engineer` - Machine learning guidance

**Data Structure:**
```
project/
├── data/
│   ├── raw/          # Original data
│   ├── processed/    # Cleaned data
│   └── interim/      # Intermediate steps
├── notebooks/        # Jupyter notebooks
├── scripts/          # Python scripts
├── reports/          # Analysis reports
├── figures/          # Visualizations
└── .claude/
```

**Example Projects:**
- Sales data analysis
- Scientific research analysis
- Machine learning experiments
- Business intelligence dashboard
- A/B test analysis

---

## 5. Automation (`automation`)

**Best for:**
- Task automation scripts
- Workflow automation
- DevOps scripting
- System administration
- Data pipelines
- Scheduled tasks

**Permissions:**
```json
{
  "allow": [
    "Bash(python3:*)", "Bash(bash:*)", "Bash(sh:*)",
    "Bash(chmod:*)", "Bash(curl:*)", "Bash(wget:*)"
  ],
  "deny": [
    "Bash(rm -rf:*)"
  ]
}
```

**Recommended MCP Servers:**
- `github` - Repository management
- `aws` or `gcp` - Cloud automation (if applicable)

**Suggested Skills:**
- `create-script` - Script generation with error handling
- `schedule-task` - Cron/scheduling assistance
- `monitor-jobs` - Job monitoring
- `troubleshoot` - Debugging assistance

**Suggested Agents:**
- `devops-engineer` - Infrastructure guidance
- `sysadmin` - System administration

**Script Structure:**
```
project/
├── scripts/
│   ├── bash/         # Shell scripts
│   └── python/       # Python scripts
├── config/           # Configuration files
├── logs/             # Execution logs
└── .claude/
```

**Example Projects:**
- Backup automation
- Log processing pipeline
- Deployment scripts
- System monitoring
- Data synchronization

---

## 6. Base (`base`)

**Best for:**
- Projects that don't fit other categories
- Custom use cases
- Starting point for unique projects
- Minimal setup preference

**Permissions:**
```json
{
  "allow": [
    "Bash(ls:*)", "Bash(cat:*)", "Bash(grep:*)"
  ]
}
```

**Recommended MCP Servers:**
- None by default (add as needed)

**Suggested Skills:**
- None by default (create custom skills)

**Structure:**
```
project/
├── .claude/
│   ├── settings.json
│   └── CLAUDE.md
├── .gitignore
└── README.md
```

**When to Use:**
- Need maximum control and customization
- Building something unique
- Want to start minimal and add incrementally
- Combining multiple purposes

---

## Template Comparison

| Feature | software-dev | content-creation | personal-tracker | data-analysis | automation | base |
|---------|--------------|------------------|------------------|---------------|------------|------|
| Code execution | ✓ | - | ✓ | ✓ | ✓ | - |
| Web search | - | ✓ | - | - | - | - |
| Git integration | ✓ | - | - | - | ✓ | - |
| Database access | Optional | - | ✓ | ✓ | - | - |
| Data analysis | - | - | ✓ | ✓ | - | - |
| Script generation | ✓ | - | - | ✓ | ✓ | - |
| Custom skills | 3-4 | 3-4 | 3-4 | 3-4 | 3-4 | 0 |
| MCP servers | 2-3 | 1-2 | 1-2 | 2-3 | 1-2 | 0 |

## Customization

All templates can be customized after creation:

1. **Add/Remove Permissions**: Edit `.claude/settings.json`
2. **Add MCP Servers**: Update `.mcp.json`
3. **Create Skills**: Add to `.claude/skills/`
4. **Add Agents**: Create in `.claude/agents/`
5. **Update Guidelines**: Modify `.claude/CLAUDE.md`

See [customization-guide.md](customization-guide.md) for details.

## Getting Help

If you're unsure which template to use:

1. Start with `base` template
2. Add permissions and integrations incrementally
3. Create custom skills as needs arise
4. Iterate based on experience

Or simply describe your project to Claude and let the `project-creator` skill recommend the best template for you!
