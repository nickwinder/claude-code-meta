# Claude Code Mastery - Meta-Project

This is a specialized meta-project that creates optimized Claude Code project setups for different purposes.

## Purpose

When users request a new Claude Code project setup, this project provides:
- Interactive discovery of project requirements
- Research-driven recommendations for MCP servers and integrations
- Custom skill generation tailored to the project domain
- Complete project scaffolding with best practices

## Key Principles

1. **Interactive First**: Always ask clarifying questions before generating
2. **Research Current**: Check for latest integrations and best practices
3. **Customize Always**: Generate domain-specific skills, not generic ones
4. **Educate Users**: Explain recommendations and provide documentation

## Workflow

Use the `project-creator` skill to orchestrate all project creation tasks. This skill:
- Gathers requirements through targeted questions
- Researches and recommends appropriate MCP servers
- Designs custom skills using the `skill-generator` agent
- Scaffolds complete project structure with templates
- Handles MCP server installation interactively
- Validates generated projects
- Provides comprehensive documentation

## Available Skills

- **project-creator**: Main orchestration skill for creating new Claude Code projects

## Available Agents

- **project-architect**: Expert in designing project structure and selecting integrations
- **skill-generator**: Generates custom skills tailored to specific project domains

## Project Structure

This meta-project contains:
- `templates/`: Base templates for common project types
- `scripts/`: Python utilities for project creation and validation
- `.claude/skills/project-creator/references/`: Curated knowledge base
  - `mcp_servers.md`: Registry of MCP servers by category
  - `project_types.md`: Common project patterns
  - `best_practices.md`: Claude Code conventions
- `docs/`: User-facing documentation
- `examples/`: Sample generated projects for reference

## Usage

To create a new project, simply ask:
- "Create a project for [purpose]"
- "Set up a Claude Code project for [task]"
- "I need a project for [domain]"

The `project-creator` skill will guide you through the process.
