#!/usr/bin/env python3
"""
MCP Server Registry Updater

Automatically updates the MCP server registry from web sources.
Uses only Python standard library.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError


def check_registry_age(registry_path: Path) -> tuple[bool, int]:
    """
    Check if the registry file is stale (older than 7 days).

    Returns:
        (is_stale, age_in_days) tuple
    """
    if not registry_path.exists():
        return True, 999  # File doesn't exist, definitely stale

    modified_time = datetime.fromtimestamp(registry_path.stat().st_mtime)
    age = datetime.now() - modified_time
    age_days = age.days

    return age_days > 7, age_days


def fetch_url(url: str, timeout: int = 10) -> str:
    """
    Fetch content from a URL.

    Args:
        url: URL to fetch
        timeout: Request timeout in seconds

    Returns:
        Content as string, or None if failed
    """
    try:
        headers = {
            'User-Agent': 'Claude-Code-Meta/1.0'
        }
        req = Request(url, headers=headers)
        with urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8')
    except URLError as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Unexpected error fetching {url}: {e}", file=sys.stderr)
        return None


def parse_mcp_servers_from_web() -> list[dict]:
    """
    Fetch and parse MCP servers from web sources.

    This is a placeholder implementation. In a real system, you would:
    1. Fetch from modelcontextprotocol.io registry
    2. Parse GitHub repositories
    3. Check official Claude documentation

    Returns:
        List of server dictionaries
    """
    servers = []

    # Placeholder: In reality, you would fetch and parse from actual sources
    # For now, return empty list to avoid breaking the script
    print("Note: Web fetching not yet implemented. Using local registry only.")

    return servers


def merge_servers(local_servers: list[dict], web_servers: list[dict]) -> list[dict]:
    """
    Merge local and web server lists, preserving local customizations.

    Args:
        local_servers: Servers from local registry
        web_servers: Servers fetched from web

    Returns:
        Merged server list
    """
    # Create dict by server name for easy lookup
    merged = {s['name']: s for s in local_servers}

    # Add new servers from web
    for server in web_servers:
        name = server['name']
        if name not in merged:
            merged[name] = server
        else:
            # Update web-sourced fields but keep local customizations
            if 'custom' not in merged[name]:
                merged[name] = server

    return list(merged.values())


def format_registry_markdown(servers: list[dict]) -> str:
    """
    Format servers list as Markdown registry.

    Args:
        servers: List of server dictionaries

    Returns:
        Formatted Markdown string
    """
    # Group by category
    categories = {}
    for server in servers:
        category = server.get('category', 'Other')
        if category not in categories:
            categories[category] = []
        categories[category].append(server)

    # Build Markdown
    md = "# MCP Server Registry\n\n"
    md += f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    md += "Curated registry of MCP servers organized by category.\n\n"

    for category in sorted(categories.keys()):
        md += f"## {category}\n\n"
        for server in sorted(categories[category], key=lambda s: s['name']):
            md += f"### {server['name']}\n\n"
            md += f"- **Purpose**: {server.get('purpose', 'N/A')}\n"
            md += f"- **Transport**: {server.get('transport', 'stdio')}\n"

            if 'install' in server:
                md += f"- **Install**: `{server['install']}`\n"

            if 'config' in server:
                md += f"- **Config**:\n```json\n{json.dumps(server['config'], indent=2)}\n```\n"

            if 'use_cases' in server:
                md += f"- **Use cases**: {server['use_cases']}\n"

            if 'docs' in server:
                md += f"- **Docs**: {server['docs']}\n"

            md += "\n"

    return md


def update_registry(registry_path: Path, force: bool = False) -> bool:
    """
    Update the MCP server registry.

    Args:
        registry_path: Path to the registry markdown file
        force: Force update even if not stale

    Returns:
        True if updated, False otherwise
    """
    print(f"Checking registry: {registry_path}")

    # Check if update needed
    is_stale, age_days = check_registry_age(registry_path)

    if not force and not is_stale:
        print(f"Registry is current (age: {age_days} days). No update needed.")
        return False

    print(f"Registry is stale (age: {age_days} days). Updating...")

    # Load local registry
    local_servers = []
    if registry_path.exists():
        print("Loading local registry...")
        # Note: Parsing Markdown is complex. For now, we'll just preserve the file
        # In a real implementation, you would parse the existing Markdown
        local_servers = []  # Placeholder

    # Fetch from web
    print("Fetching servers from web sources...")
    web_servers = parse_mcp_servers_from_web()

    if not web_servers and not local_servers:
        print("Warning: No servers found from web or local registry.", file=sys.stderr)
        return False

    # Merge
    merged_servers = merge_servers(local_servers, web_servers)

    # Format as Markdown
    markdown = format_registry_markdown(merged_servers)

    # Write to file
    try:
        registry_path.write_text(markdown, encoding='utf-8')
        print(f"✓ Registry updated successfully at {registry_path}")
        return True
    except Exception as e:
        print(f"Error writing registry: {e}", file=sys.stderr)
        return False


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Update the MCP server registry from web sources'
    )

    parser.add_argument(
        '--registry',
        help='Path to the registry markdown file (default: auto-detect)'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Force update even if registry is current'
    )

    args = parser.parse_args()

    # Determine registry path
    if args.registry:
        registry_path = Path(args.registry)
    else:
        # Auto-detect from script location
        script_dir = Path(__file__).parent
        registry_path = script_dir.parent / '.claude' / 'skills' / 'project-creator' / 'references' / 'mcp_servers.md'

    success = update_registry(registry_path, force=args.force)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
