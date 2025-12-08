#!/usr/bin/env python3
"""WheresTheFault CLI - Collect system debugging information from plugins."""
import click
import ast
import json
import os
from pathlib import Path
from python3_wtf.main import WheresTheFault

SETTINGS_EXAMPLE = {
    "timeout": 5,
    "output_dir": "/tmp",
    "max_concurrent": 16,
    "plugins": [
        {"austin": ["1234", "-i", "1000"]},
        {"tshark": ["-i", "eth0"]}
    ]
}

PLUGIN_CLI_EXAMPLES = """
Plugin Argument Formats:
  -p plugin_name '["arg1", "arg2"]'    # List style
  -p plugin_name "arg1 arg2"           # Space-separated
  -p plugin_name arg1                  # Single arg
  -p austin "1234 -i 1000"             # Multiple args for configurable plugin
"""


def show_help_settings(ctx, param, value):
    """Show JSON settings format example."""
    if not value or ctx.resilient_parsing:
        return
    click.echo("\nJSON Settings Format Example:\n")
    click.echo(json.dumps(SETTINGS_EXAMPLE, indent=2))
    ctx.exit()


def show_help_plugins(ctx, param, value):
    """Show plugin argument format examples."""
    if not value or ctx.resilient_parsing:
        return
    click.echo(PLUGIN_CLI_EXAMPLES)
    ctx.exit()


def parse_plugins(plugins_raw_arguments: tuple) -> list[tuple[str, ...]]:
    """
    Parse plugin arguments from CLI format.
    
    Supports:
    - List format: plugin_name '["arg1", "arg2"]'
    - Space-separated: plugin_name "arg1 arg2"
    - Single arg: plugin_name arg1
    """
    plugin_args = []
    for name, arg_str in plugins_raw_arguments:
        try:
            # Try to parse as Python literal (list)
            parsed = ast.literal_eval(arg_str)
            if not isinstance(parsed, list):
                raise ValueError("Not a list")
        except (ValueError, SyntaxError):
            # Fall back to space-separated split
            if arg_str.strip().startswith("{"):
                raise click.BadParameter(
                    f"Plugin args must be a list or space-separated string, got: {arg_str}"
                )
            parsed = arg_str.strip().split()

        plugin_args.append((name, *parsed))
    return plugin_args


def parse_plugins_from_json(plugin_dicts: list) -> list[tuple[str, ...]]:
    """Parse plugin arguments from JSON settings format."""
    plugin_args = []
    for plugin_entry in plugin_dicts:
        if not isinstance(plugin_entry, dict) or len(plugin_entry) != 1:
            raise click.BadParameter(
                f"Invalid plugin entry: {plugin_entry}. "
                "Each plugin must be a single-key object.",
                param_hint="plugins"
            )
        for name, args in plugin_entry.items():
            if not isinstance(args, list):
                raise click.BadParameter(
                    f"Plugin args for '{name}' must be a list, got: {args}",
                    param_hint="plugins"
                )
            plugin_args.append((name, *args))
    return plugin_args


def load_settings(settings_path: str) -> dict:
    """Load and validate JSON settings file."""
    try:
        with open(settings_path) as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        raise click.BadParameter(f"Invalid JSON in settings file: {e}")
    except IOError as e:
        raise click.BadParameter(f"Cannot read settings file: {e}")


@click.command()
@click.option(
    '-t', '--timeout',
    type=click.IntRange(min=1),
    help='Timeout in seconds for each plugin (default: from settings or 5)'
)
@click.option(
    '-o', '--output-dir',
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True
    ),
    help='Directory to save output archive (default: from settings or current dir)'
)
@click.option(
    '-c', '--max-concurrent',
    type=click.IntRange(min=0),
    help='Max concurrent plugins (0=unlimited, default: auto-scale with CPU)'
)
@click.option(
    '-p', '--plugin',
    nargs=2,
    multiple=True,
    type=str,
    metavar='NAME ARGS',
    help='Plugin to run with args. Use --help-plugins for examples'
)
@click.option(
    '-s', '--settings',
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help='JSON settings file. Use --help-settings for format'
)
@click.option(
    '--help-settings',
    is_flag=True,
    expose_value=False,
    callback=show_help_settings,
    help='Show JSON settings format and exit'
)
@click.option(
    '--help-plugins',
    is_flag=True,
    expose_value=False,
    callback=show_help_plugins,
    help='Show plugin argument examples and exit'
)
@click.option(
    '-q', '--quiet',
    is_flag=True,
    help='Suppress informational output'
)
def cli(
    timeout: int | None,
    output_dir: str | None,
    max_concurrent: int | None,
    plugin: tuple | None,
    settings: str | None,
    quiet: bool
):
    """
    WheresTheFault - Collect system debugging information from plugins.
    
    Examples:
      wtf -t 5 -o /tmp                          # Run all available plugins
      wtf -t 5 -o /tmp -p austin "1234"         # Run specific plugin
      wtf -s config.json                        # Use settings file
      wtf -t 5 -o /tmp -c 16                    # Custom concurrency
    """
    def log(msg: str):
        if not quiet:
            click.echo(msg)
    
    log("[WTF] Initializing...")
    
    # Load settings file if provided
    config = load_settings(settings) if settings else {}
    
    # Merge CLI args with config (CLI takes precedence)
    timeout = timeout or config.get("timeout", 5)
    output_dir = output_dir or config.get("output_dir", ".")
    max_concurrent = max_concurrent if max_concurrent is not None else config.get("max_concurrent")
    
    # Parse plugin arguments
    plugin_args = None
    if plugin:
        plugin_args = parse_plugins(plugin)
    elif "plugins" in config:
        plugin_args = parse_plugins_from_json(config["plugins"])
    
    if not plugin_args:
        log("[WTF] No specific plugins requested, will run all available plugins")
        plugin_args = []
    
    # Display configuration
    log(f"[WTF] Configuration:")
    log(f"  Timeout: {timeout}s")
    log(f"  Output: {output_dir}")
    log(f"  Concurrency: {max_concurrent if max_concurrent is not None else 'auto'}")
    if plugin_args:
        log(f"  Plugins: {len(plugin_args)} configured")
    
    # Run
    try:
        task = WheresTheFault(
            timeout=int(timeout),
            output_dir=Path(output_dir),
            plugin_args=plugin_args,
            max_concurrent=max_concurrent
        )
        task.main_runner()
        log("[WTF] Done!")
    except Exception as e:
        click.echo(f"[WTF] Error: {e}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    cli()
