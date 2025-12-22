# Project Type Patterns

Common project patterns with recommended configurations for Claude Code projects.

## Software Development

**Typical Use Cases:**
- Web application development
- API backend development
- CLI tool creation
- Library/package development
- Mobile app development

**Recommended MCP Servers:**
- `github` - Version control integration
- `git` - Local repository operations
- `postgres` or `sqlite` - Database access (if applicable)

**Custom Skills:**
- `code-review` - Automated code review with project-specific standards
- `test-runner` - Execute test suites and report results
- `deploy-helper` - Deployment workflow assistance
- `refactor-guide` - Refactoring suggestions and patterns

**Agents:**
- `senior-developer` - Architecture and design guidance
- `qa-engineer` - Testing and quality assurance
- `devops-specialist` - Deployment and infrastructure

**Permissions:**
```json
{
  "allow": [
    "Bash(npm:*)", "Bash(yarn:*)", "Bash(pnpm:*)",
    "Bash(python3:*)", "Bash(pip:*)", "Bash(pytest:*)",
    "Bash(git:*)", "Bash(node:*)", "Bash(cargo:*)",
    "WebFetch(domain:github.com)",
    "WebFetch(domain:stackoverflow.com)"
  ]
}
```

**Directory Structure:**
```
project/
├── src/
├── tests/
├── docs/
├── .claude/
└── README.md
```

---

## Content Creation

**Typical Use Cases:**
- Blog writing
- Social media content
- Email newsletters
- Marketing copy
- Documentation

**Recommended MCP Servers:**
- `brave-search` or `google-search` - Research and fact-checking
- `notion` - Knowledge management (optional)
- `google-drive` - Document collaboration (optional)

**Custom Skills:**
- `draft-content` - Content creation with brand guidelines
- `seo-optimize` - SEO analysis and recommendations
- `publish-workflow` - Multi-platform publishing automation
- `research-topic` - Research and source gathering

**Agents:**
- `content-strategist` - Content planning and strategy
- `seo-specialist` - SEO optimization
- `copy-editor` - Grammar and style review

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

**Directory Structure:**
```
project/
├── content/
│   ├── drafts/
│   ├── published/
│   └── archive/
├── assets/
│   └── images/
├── .claude/
└── README.md
```

---

## Personal Tracking

**Typical Use Cases:**
- Fitness/health tracking
- Habit tracking
- Finance tracking
- Time tracking
- Goal tracking

**Recommended MCP Servers:**
- `sqlite` - Local data storage
- `filesystem` - Enhanced file operations (optional)

**Custom Skills:**
- `log-entry` - Structured data entry with validation
- `analyze-trends` - Statistical analysis and insights
- `generate-report` - Automated reporting with visualizations
- `export-data` - Data export in various formats (CSV, JSON, PDF)

**Agents:**
- `data-analyst` - Trend analysis and insights
- `report-generator` - Automated report creation

**Permissions:**
```json
{
  "allow": [
    "Bash(python3:*)",
    "Bash(ls:*)", "Bash(cat:*)", "Bash(grep:*)"
  ]
}
```

**Directory Structure:**
```
project/
├── data/
│   └── entries/
├── scripts/
│   ├── analyze.py
│   └── export.py
├── reports/
├── .claude/
└── README.md
```

---

## Data Analysis

**Typical Use Cases:**
- Statistical analysis
- Data visualization
- Machine learning experiments
- Research projects
- Business intelligence

**Recommended MCP Servers:**
- `postgres` or `sqlite` - Database access
- `jupyter` - Notebook integration
- `pandas` - Data manipulation (if available as MCP)

**Custom Skills:**
- `load-data` - Data ingestion and validation
- `clean-data` - Data cleaning and preprocessing
- `analyze-dataset` - Statistical analysis
- `visualize-trends` - Chart and graph generation
- `export-results` - Result export and reporting

**Agents:**
- `data-scientist` - Analysis methodology and statistics
- `ml-engineer` - Machine learning guidance

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

**Directory Structure:**
```
project/
├── data/
│   ├── raw/
│   ├── processed/
│   └── interim/
├── notebooks/
├── scripts/
├── reports/
├── figures/
├── .claude/
└── README.md
```

---

## Automation

**Typical Use Cases:**
- Task automation scripts
- Workflow automation
- System administration
- DevOps scripts
- Data pipeline

**Recommended MCP Servers:**
- `github` - Repository management (for storing scripts)
- `aws` or `gcp` - Cloud automation (if applicable)

**Custom Skills:**
- `create-script` - Script generation with error handling
- `schedule-task` - Cron/scheduling assistance
- `monitor-jobs` - Job monitoring and alerting
- `troubleshoot` - Debugging and error analysis

**Agents:**
- `devops-engineer` - Infrastructure and automation
- `sysadmin` - System administration guidance

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

**Directory Structure:**
```
project/
├── scripts/
│   ├── bash/
│   └── python/
├── config/
├── logs/
├── .claude/
└── README.md
```

---

## Selection Guide

Use this guide to select the appropriate template:

| If your project involves... | Use template |
|------------------------------|--------------|
| Writing code, building apps | `software-dev` |
| Writing articles, blog posts | `content-creation` |
| Tracking personal data | `personal-tracker` |
| Analyzing datasets | `data-analysis` |
| Creating automation scripts | `automation` |
| None of the above | `base` |

## Customization

All templates can be customized by:
1. Modifying permissions in `.claude/settings.json`
2. Adding/removing MCP servers in `.mcp.json`
3. Creating domain-specific skills
4. Adding specialized agents
5. Updating CLAUDE.md with project-specific guidelines
