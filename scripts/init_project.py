#!/usr/bin/env python3
"""
Claude Code Project Initializer

Creates new Claude Code projects from templates with variable substitution.
Uses only Python standard library for maximum portability.
"""

import argparse
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path


def substitute_variables(content: str, variables: dict) -> str:
    """
    Substitute template variables in content.

    Variables use {{VARIABLE_NAME}} syntax.
    """
    for key, value in variables.items():
        placeholder = f"{{{{{key}}}}}"
        content = content.replace(placeholder, str(value))
    return content


def copy_template_file(src: Path, dest: Path, variables: dict):
    """
    Copy a template file to destination with variable substitution.

    If filename ends with .template, remove that extension.
    """
    # Determine destination filename
    if dest.name.endswith('.template'):
        dest = dest.parent / dest.name[:-9]  # Remove .template extension

    # Read source file
    try:
        content = src.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        # Binary file, just copy
        shutil.copy2(src, dest)
        return

    # Substitute variables
    content = substitute_variables(content, variables)

    # Write to destination
    dest.write_text(content, encoding='utf-8')
    print(f"  Created: {dest.relative_to(dest.parents[len(dest.parents)-1])}")


def copy_template_tree(template_dir: Path, project_path: Path, variables: dict):
    """
    Recursively copy template directory to project path with variable substitution.
    """
    for item in template_dir.rglob('*'):
        if item.is_file():
            # Calculate relative path
            rel_path = item.relative_to(template_dir)
            dest_path = project_path / rel_path

            # Create parent directories
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy file with substitution
            copy_template_file(item, dest_path, variables)


def create_project(
    path: str,
    template: str,
    name: str,
    description: str = None
) -> bool:
    """
    Create a new Claude Code project from a template.

    Args:
        path: Absolute path where project should be created
        template: Template name (base, software-dev, content-creation, etc.)
        name: Display name for the project
        description: Optional project description

    Returns:
        True if successful, False otherwise
    """
    # Convert to Path objects
    project_path = Path(path).resolve()
    script_dir = Path(__file__).parent
    meta_project_root = script_dir.parent
    template_dir = meta_project_root / "templates" / template

    # Validation
    if not template_dir.exists():
        print(f"Error: Template '{template}' not found at {template_dir}", file=sys.stderr)
        print(f"Available templates: {', '.join([t.name for t in (meta_project_root / 'templates').iterdir() if t.is_dir()])}")
        return False

    if project_path.exists():
        response = input(f"Warning: {project_path} already exists. Continue and potentially overwrite files? (y/N): ")
        if response.lower() != 'y':
            print("Aborted.")
            return False

    # Prepare variables for substitution
    variables = {
        'PROJECT_NAME': name,
        'PROJECT_PATH': str(project_path),
        'PROJECT_TYPE': template,
        'TIMESTAMP': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'DESCRIPTION': description or f"A {template} project created with Claude Code Mastery"
    }

    print(f"\nCreating project: {name}")
    print(f"Location: {project_path}")
    print(f"Template: {template}\n")

    # Create project directory
    project_path.mkdir(parents=True, exist_ok=True)

    # Copy template tree
    try:
        copy_template_tree(template_dir, project_path, variables)
        print(f"\n✓ Project created successfully at {project_path}")
        print(f"\nNext steps:")
        print(f"  1. cd {project_path}")
        print(f"  2. Open in Claude Code")
        print(f"  3. Review .claude/CLAUDE.md for project guidelines")
        return True
    except Exception as e:
        print(f"\nError creating project: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Create a new Claude Code project from a template',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 init_project.py --path /Users/me/projects/my-app --template software-dev --name "My App"
  python3 init_project.py --path ~/running-tracker --template personal-tracker --name "Running Tracker" --description "Track my running workouts"
        """
    )

    parser.add_argument(
        '--path',
        required=True,
        help='Absolute path where the project should be created'
    )

    parser.add_argument(
        '--template',
        required=True,
        choices=['base', 'software-dev', 'content-creation', 'personal-tracker', 'data-analysis', 'automation'],
        help='Template to use for the project'
    )

    parser.add_argument(
        '--name',
        required=True,
        help='Display name for the project'
    )

    parser.add_argument(
        '--description',
        help='Optional project description'
    )

    args = parser.parse_args()

    success = create_project(
        path=args.path,
        template=args.template,
        name=args.name,
        description=args.description
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
