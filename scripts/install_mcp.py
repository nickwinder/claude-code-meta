#!/usr/bin/env python3
"""
MCP Server Installation Helper

Assists with installing MCP servers and updating .mcp.json configuration.
Uses only Python standard library.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_command(command: list[str], dry_run: bool = False) -> tuple[bool, str]:
    """
    Execute a shell command.

    Args:
        command: Command and arguments as list
        dry_run: If True, print command but don't execute

    Returns:
        (success, output) tuple
    """
    if dry_run:
        print(f"[DRY RUN] Would execute: {' '.join(command)}")
        return True, "Dry run - not executed"

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Command failed: {e.stderr}"
    except Exception as e:
        return False, f"Error executing command: {e}"


def update_mcp_json(config_path: Path, server_name: str, server_config: dict) -> bool:
    """
    Update .mcp.json with new server configuration.

    Args:
        config_path: Path to .mcp.json file
        server_name: Name of the MCP server
        server_config: Server configuration dict

    Returns:
        True if successful, False otherwise
    """
    try:
        # Load existing config or create new
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = {"mcpServers": {}}

        # Ensure mcpServers key exists
        if 'mcpServers' not in config:
            config['mcpServers'] = {}

        # Add or update server
        config['mcpServers'][server_name] = server_config

        # Write back to file
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

        print(f"✓ Updated {config_path} with server '{server_name}'")
        return True

    except Exception as e:
        print(f"Error updating {config_path}: {e}", file=sys.stderr)
        return False


def install_mcp_server(
    server_name: str,
    transport: str,
    url: str = None,
    command: str = None,
    args: list[str] = None,
    env: dict = None,
    config_path: str = None,
    dry_run: bool = False
) -> bool:
    """
    Install an MCP server.

    Args:
        server_name: Name of the MCP server
        transport: Transport type (stdio, http, sse)
        url: URL for http/sse servers
        command: Command for stdio servers
        args: Arguments for stdio servers
        env: Environment variables
        config_path: Path to .mcp.json (optional)
        dry_run: If True, print actions but don't execute

    Returns:
        True if successful, False otherwise
    """
    print(f"\nInstalling MCP server: {server_name}")
    print(f"Transport: {transport}")

    # Build claude mcp add command
    # Correct order: claude mcp add --transport TYPE SERVER_NAME -e KEY=value -- command
    cmd = ['claude', 'mcp', 'add', '--transport', transport, server_name]

    if transport in ['http', 'sse']:
        if not url:
            print("Error: URL required for http/sse transport", file=sys.stderr)
            return False
        cmd.append(url)
    elif transport == 'stdio':
        if not command:
            print("Error: Command required for stdio transport", file=sys.stderr)
            return False
        # For stdio: server name is already added, now add -e flags, then --, then command
        if env:
            for key, value in env.items():
                cmd.extend(['-e', f'{key}={value}'])
        cmd.append('--')
        cmd.append(command)
        if args:
            cmd.extend(args)

    # Add scope if config_path is provided
    if config_path:
        cmd.extend(['--scope', 'project'])

    # Execute installation command
    print(f"Executing: {' '.join(cmd)}")
    success, output = run_command(cmd, dry_run)

    if success:
        print(f"✓ Installation command executed successfully")
        if output:
            print(output)

        # Update .mcp.json if config_path provided
        if config_path and not dry_run:
            config_file = Path(config_path)

            # Build server config
            server_config = {"type": transport}

            if transport in ['http', 'sse']:
                server_config['url'] = url
            elif transport == 'stdio':
                server_config['command'] = command
                if args:
                    server_config['args'] = args
                if env:
                    server_config['env'] = env

            update_mcp_json(config_file, server_name, server_config)

        return True
    else:
        print(f"✗ Installation failed: {output}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Install MCP servers and update configuration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Install HTTP server
  python3 install_mcp.py --server github --transport http --url https://api.githubcopilot.com/mcp/

  # Install stdio server
  python3 install_mcp.py --server postgres --transport stdio --command npx --args @modelcontextprotocol/server-postgres

  # Install and update project .mcp.json
  python3 install_mcp.py --server github --transport http --url https://api.githubcopilot.com/mcp/ --config /path/to/project/.mcp.json

  # Dry run (don't actually execute)
  python3 install_mcp.py --server github --transport http --url https://api.githubcopilot.com/mcp/ --dry-run
        """
    )

    parser.add_argument(
        '--server',
        required=True,
        help='Name of the MCP server'
    )

    parser.add_argument(
        '--transport',
        required=True,
        choices=['stdio', 'http', 'sse'],
        help='Transport type'
    )

    parser.add_argument(
        '--url',
        help='URL for http/sse servers'
    )

    parser.add_argument(
        '--command',
        help='Command for stdio servers'
    )

    parser.add_argument(
        '--args',
        nargs='+',
        help='Arguments for stdio servers'
    )

    parser.add_argument(
        '--env',
        nargs='+',
        help='Environment variables in KEY=VALUE format'
    )

    parser.add_argument(
        '--config',
        help='Path to .mcp.json file to update'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print commands but do not execute'
    )

    args = parser.parse_args()

    # Parse environment variables
    env_dict = None
    if args.env:
        env_dict = {}
        for env_var in args.env:
            if '=' in env_var:
                key, value = env_var.split('=', 1)
                env_dict[key] = value

    success = install_mcp_server(
        server_name=args.server,
        transport=args.transport,
        url=args.url,
        command=args.command,
        args=args.args,
        env=env_dict,
        config_path=args.config,
        dry_run=args.dry_run
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
