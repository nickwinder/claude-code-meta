#!/usr/bin/env python3
"""
Claude Code Project Validator

Validates Claude Code project structure and configuration files.
Uses only Python standard library.
"""

import argparse
import json
import re
import sys
from pathlib import Path


def validate_json(file_path: Path) -> tuple[bool, str]:
    """Validate JSON file syntax."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, "Valid JSON"
    except json.JSONDecodeError as e:
        return False, f"JSON syntax error: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"


def validate_yaml_frontmatter(file_path: Path) -> tuple[bool, str]:
    """Validate YAML frontmatter in Markdown files."""
    try:
        content = file_path.read_text(encoding='utf-8')

        # Check if file starts with ---
        if not content.startswith('---\n'):
            return False, "Missing YAML frontmatter (should start with ---)"

        # Find closing ---
        lines = content.split('\n')
        closing_index = None
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == '---':
                closing_index = i
                break

        if closing_index is None:
            return False, "YAML frontmatter not properly closed (missing second ---)"

        # Extract frontmatter
        frontmatter = '\n'.join(lines[1:closing_index])

        # Basic YAML validation (check for key: value pattern)
        required_fields = {'name', 'description'}
        found_fields = set()

        for line in frontmatter.split('\n'):
            line = line.strip()
            if ':' in line:
                key = line.split(':')[0].strip()
                found_fields.add(key)

        missing = required_fields - found_fields
        if missing:
            return False, f"Missing required frontmatter fields: {', '.join(missing)}"

        return True, "Valid YAML frontmatter"

    except Exception as e:
        return False, f"Error reading file: {e}"


def validate_permissions(settings_file: Path) -> tuple[bool, str]:
    """Validate permission patterns in settings.json."""
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            settings = json.load(f)

        if 'permissions' not in settings:
            return True, "No permissions configured"

        permissions = settings['permissions']

        # Validate allow patterns
        if 'allow' in permissions:
            for pattern in permissions['allow']:
                # Basic pattern validation
                if not isinstance(pattern, str):
                    return False, f"Invalid permission pattern (not a string): {pattern}"

        # Validate deny patterns
        if 'deny' in permissions:
            for pattern in permissions['deny']:
                if not isinstance(pattern, str):
                    return False, f"Invalid permission pattern (not a string): {pattern}"

        return True, "Valid permissions"

    except Exception as e:
        return False, f"Error validating permissions: {e}"


def validate_mcp_config(mcp_file: Path) -> tuple[bool, str]:
    """Validate .mcp.json configuration."""
    try:
        with open(mcp_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        if 'mcpServers' not in config:
            return False, "Missing 'mcpServers' key"

        servers = config['mcpServers']
        if not isinstance(servers, dict):
            return False, "'mcpServers' must be an object"

        for name, server_config in servers.items():
            # Check required fields
            if 'type' not in server_config:
                return False, f"Server '{name}' missing 'type' field"

            server_type = server_config['type']
            if server_type not in ['stdio', 'http', 'sse']:
                return False, f"Server '{name}' has invalid type: {server_type}"

            # Validate based on type
            if server_type == 'stdio':
                if 'command' not in server_config:
                    return False, f"stdio server '{name}' missing 'command' field"
            elif server_type in ['http', 'sse']:
                if 'url' not in server_config:
                    return False, f"{server_type} server '{name}' missing 'url' field"

        return True, "Valid MCP configuration"

    except Exception as e:
        return False, f"Error validating MCP config: {e}"


def validate_project(project_path: str) -> bool:
    """
    Validate a Claude Code project.

    Returns:
        True if validation passes, False otherwise
    """
    project_dir = Path(project_path).resolve()

    if not project_dir.exists():
        print(f"Error: Project directory does not exist: {project_dir}", file=sys.stderr)
        return False

    print(f"Validating project: {project_dir}\n")

    errors = []
    warnings = []

    # Check required files
    required_files = [
        '.claude/settings.json',
        '.claude/CLAUDE.md'
    ]

    print("Checking required files...")
    for file_rel in required_files:
        file_path = project_dir / file_rel
        if not file_path.exists():
            errors.append(f"Missing required file: {file_rel}")
        else:
            print(f"  ✓ {file_rel}")

    # Validate JSON files
    print("\nValidating JSON files...")
    json_files = [
        '.claude/settings.json',
        '.mcp.json'
    ]

    for file_rel in json_files:
        file_path = project_dir / file_rel
        if file_path.exists():
            valid, message = validate_json(file_path)
            if valid:
                print(f"  ✓ {file_rel}: {message}")

                # Additional validation for specific files
                if file_rel == '.claude/settings.json':
                    valid_perms, perms_message = validate_permissions(file_path)
                    if valid_perms:
                        print(f"    ✓ Permissions: {perms_message}")
                    else:
                        errors.append(f"{file_rel}: {perms_message}")

                elif file_rel == '.mcp.json':
                    valid_mcp, mcp_message = validate_mcp_config(file_path)
                    if valid_mcp:
                        print(f"    ✓ MCP config: {mcp_message}")
                    else:
                        errors.append(f"{file_rel}: {mcp_message}")
            else:
                errors.append(f"{file_rel}: {message}")

    # Validate skills
    print("\nValidating skills...")
    skills_dir = project_dir / '.claude' / 'skills'
    if skills_dir.exists():
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
        if skill_dirs:
            for skill_dir in skill_dirs:
                skill_md = skill_dir / 'SKILL.md'
                if skill_md.exists():
                    valid, message = validate_yaml_frontmatter(skill_md)
                    if valid:
                        print(f"  ✓ {skill_dir.name}/SKILL.md: {message}")
                    else:
                        errors.append(f"Skill '{skill_dir.name}': {message}")
                else:
                    warnings.append(f"Skill '{skill_dir.name}' missing SKILL.md")
        else:
            print("  No skills found")
    else:
        print("  Skills directory does not exist")

    # Validate agents
    print("\nValidating agents...")
    agents_dir = project_dir / '.claude' / 'agents'
    if agents_dir.exists():
        agent_files = list(agents_dir.glob('*.md'))
        if agent_files:
            for agent_file in agent_files:
                valid, message = validate_yaml_frontmatter(agent_file)
                if valid:
                    print(f"  ✓ {agent_file.name}: {message}")
                else:
                    errors.append(f"Agent '{agent_file.name}': {message}")
        else:
            print("  No agents found")
    else:
        print("  Agents directory does not exist")

    # Print summary
    print("\n" + "="*60)
    if errors:
        print(f"\n❌ Validation failed with {len(errors)} error(s):\n")
        for error in errors:
            print(f"  • {error}")

    if warnings:
        print(f"\n⚠️  {len(warnings)} warning(s):\n")
        for warning in warnings:
            print(f"  • {warning}")

    if not errors and not warnings:
        print("\n✓ All validations passed!")

    return len(errors) == 0


def main():
    parser = argparse.ArgumentParser(
        description='Validate a Claude Code project structure and configuration'
    )

    parser.add_argument(
        'path',
        help='Path to the Claude Code project to validate'
    )

    args = parser.parse_args()

    success = validate_project(args.path)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
