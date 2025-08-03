#!/bin/python3

import click
from main import WheresTheFault
from pathlib import Path

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
    multiple=True,
    type=str,
    help='Specify a plugin and its arguments, e.g. --plugin tshark enpxx enpyyy. Can be used multiple times.'
)
def cli(timeout: click.IntRange, output_dir: click.Path, plugin: str | None = None):
    """WheresTheFault CLI tool. Collect logs from all plugins with 1 simple command!"""
    click.echo("[WheresTheFault] Initializing WheresTheFault...")
    if plugin:
        plugin = list[plugin]
    task = WheresTheFault(timeout=timeout, output_dir=Path(output_dir), plugin_args=plugin)
    click.echo(f"[WheresTheFault] Running with timeout={timeout}, output_dir='{output_dir} and plugin_args={plugin}'")
    task.main_runner()
    click.echo("[WheresTheFault] Done.")

if __name__ == '__main__':
    cli()