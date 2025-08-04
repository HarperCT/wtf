#!/bin/python3

import click
import ast
import json

from main import WheresTheFault
from pathlib import Path

SETTINGS_EXAMPLE = {
    "timeout": 5,
    "output_dir": "/tmp",
    "plugins": [
        {"plugin_name": ["arg1"]},
        {"plugin_name": ["arg1", "arg2"]}
    ]
}
def show_help_settings(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("\nJSON Settings Format Example:\n")
    click.echo(json.dumps(SETTINGS_EXAMPLE, indent=2))
    ctx.exit()

PLUGIN_CLI_EXAMPLES = """
Plugin Argument Formats:
  -p plugin_name '["arg1", "arg2"]'                                             # List style multiple args
  -p plugin_name "arg1 arg2"                                                    # String style multiple args
  -p plugin_name arg1                                                           # Single arg
  -p plugin_name "arg1 arg2" -p plugin_name "arg1 arg2" -p plugin_name arg1     # Multiple plugins mix of above
"""

def show_help_plugins(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(PLUGIN_CLI_EXAMPLES)
    ctx.exit()


def parse_plugins(plugins_raw_arguments):
    plugin_args = []
    for name, arg_str in plugins_raw_arguments:
        parsed = None
        try:
            parsed = ast.literal_eval(arg_str)
            if not isinstance(parsed, list):
                raise ValueError("Not a list")
        except (ValueError, SyntaxError):
            # Fall back to space-separated split — only if it's not a dict-like string
            if arg_str.strip().startswith("{") or ":" in arg_str:
                raise click.BadParameter(
                    f"Plugin args must be a valid list or a space-separated string, got: {arg_str}"
                )
            parsed = arg_str.strip().split()

        plugin_args.append((name, *parsed))
    return plugin_args

def parse_plugins_from_json(plugin_dicts):
    plugin_args = []
    for plugin_entry in plugin_dicts:
        if not isinstance(plugin_entry, dict) or len(plugin_entry) != 1:
            raise click.BadParameter(f"Each plugin in the JSON must be a single-key object, got: {plugin_entry}")
        for name, args in plugin_entry.items():
            if not isinstance(args, list):
                raise click.BadParameter(f"Plugin args must be a list for plugin '{name}', got: {args}")
            plugin_args.append((name, *args))
    return plugin_args

@click.command()
@click.option(
    '-t', '--timeout', 
    type=click.IntRange(min=1), 
    help='Timeout value in seconds (must be a positive integer)'
)
@click.option(
    '-o', '--output-dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, resolve_path=True),
    help='Path to an existing output directory'
)
@click.option(
    '-p', '--plugin',
    nargs=2,
    multiple=True,
    type=str,
    help="""Specify plugin configuration to run. Use --help-plugins to see formats."""
)
@click.option(
    '--settings', '-s',
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="Path to a JSON settings file. Use --help-settings to see format."
)
@click.option(
    '--help-settings',
    is_flag=True,
    expose_value=False,
    callback=show_help_settings,
    help="Show example JSON format for --settings and exit."
)
@click.option(
    '--help-plugins',
    is_flag=True,
    expose_value=False,
    callback=show_help_plugins,
    help="Show usage examples for the --plugin option and exit."
)
def cli(timeout: click.IntRange, output_dir: click.Path, plugin: str | None = None, settings: str = None):
    """WheresTheFault CLI tool. Collect logs from all plugins with 1 simple command!"""
    click.echo("[WheresTheFault] Initializing WheresTheFault...")
    config = {}

    if settings:
        with open(settings) as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError as e:
                raise click.BadParameter(f"Invalid JSON in settings file: {e}")
    try:
        timeout = timeout or config["timeout"]
        output_dir = output_dir or config["output_dir"]
        plugin_args = plugin or config.get("plugins", None)
    except KeyError as e:
        raise click.UsageError("[WheresTheFault] Missing required parameters: 'timeout' and/or 'output_dir' must be set either in the CLI or .json.")
        
    if plugin and isinstance(plugin, tuple):
        plugin_args = parse_plugins(plugin)
    elif isinstance(plugin_args, list) and all(isinstance(plugin, dict) for plugin in plugin_args):
        plugin_args = parse_plugins_from_json(plugin_args)
    else:
        click.echo("[WheresTheFault] No plugins provided")

    task = WheresTheFault(timeout=int(timeout), output_dir=Path(output_dir), plugin_args=plugin_args)
    click.echo(f"[WheresTheFault] Running with timeout={timeout}, output_dir='{output_dir}' and plugin_args={plugin_args}")
    task.main_runner()
    click.echo("[WheresTheFault] Done.")

if __name__ == '__main__':
    cli()