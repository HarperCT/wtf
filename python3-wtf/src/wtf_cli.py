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
def cli(timeout, output_dir):
    """WheresTheFault CLI tool. Collect logs from all plugins with 1 simple command!"""
    click.echo("[WheresTheFault] Initializing WheresTheFault...")
    task = WheresTheFault(timeout=timeout, output_dir=Path(output_dir))
    click.echo(f"[WheresTheFault] Running with timeout={timeout} and output_dir='{output_dir}'")
    task.main_runner()
    click.echo("[WheresTheFault] Done.")

if __name__ == '__main__':
    cli()