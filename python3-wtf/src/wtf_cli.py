#!/bin/python3

import click
import ast
from main import WheresTheFault
from pathlib import Path

def parse_plugins(plugins_raw_arguments):
    plugin_args = []
    if plugins_raw_arguments:
        for name, arg_str in plugins_raw_arguments:
            parsed = None
            try:
                parsed = ast.literal_eval(arg_str)
                if not isinstance(parsed, list):
                    raise ValueError("Not a list")
            except (ValueError, SyntaxError):
                # Fall back to space-separated split
                parsed = arg_str.strip().split()

            if not isinstance(parsed, list):
                raise click.BadParameter(
                    f"Plugin args must be a valid list or a space-separated string, got: {arg_str}"
                )

            plugin_args.append((name, *parsed))
        return plugin_args

@click.command()
@click.option(
    '-t', '--timeout', 
    type=click.IntRange(min=1), 
    required=True,
    help='Timeout value in seconds (must be a positive integer)'
)
@click.option(
    '-o', '--output-dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, resolve_path=True),
    required=True,
    help='Path to an existing output directory'
)
@click.option(
    '-p', '--plugin',
    nargs=2,
    multiple=True,
    type=str,
    help='Specify plugin and its args: either as a list string (e.g. plugin_name \'["arg1", "arg2"]\') or a space-separated string (e.g. plugin_name "arg1 arg2" or for single' \
    'arg plugin: plugin_name arg)'
)
def cli(timeout: click.IntRange, output_dir: click.Path, plugin: str | None = None):
    """WheresTheFault CLI tool. Collect logs from all plugins with 1 simple command!"""
    click.echo("[WheresTheFault] Initializing WheresTheFault...")
    if plugin:
        plugin_args = parse_plugins(plugin)
    task = WheresTheFault(timeout=timeout, output_dir=Path(output_dir), plugin_args=plugin_args)
    click.echo(f"[WheresTheFault] Running with timeout={timeout}, output_dir='{output_dir} and plugin_args={plugin_args}'")
    task.main_runner()
    click.echo("[WheresTheFault] Done.")

if __name__ == '__main__':
    cli()