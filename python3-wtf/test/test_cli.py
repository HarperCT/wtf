from click.testing import CliRunner
from wtf_cli import cli

def test_cli_required_options(tmp_path):
    # Run CLI with required options and check output
    runner = CliRunner()
    result = runner.invoke(cli, ['-t', '3', '-o', str(tmp_path)])
    assert result.exit_code == 0
    assert "[WheresTheFault] Initializing WheresTheFault..." in result.output
    assert f"[WheresTheFault] Running with timeout=3 and output_dir='{tmp_path}'" in result.output
    assert "[WheresTheFault] Done." in result.output

def test_cli_missing_timeout(tmp_path):
    runner = CliRunner()
    # Missing timeout should cause error
    result = runner.invoke(cli, ['-o', str(tmp_path)])
    assert result.exit_code != 0
    assert "Missing option '-t' / '--timeout'" in result.output

def test_cli_invalid_timeout(tmp_path):
    runner = CliRunner()
    # Timeout must be positive integer
    result = runner.invoke(cli, ['-t', '0', '-o', str(tmp_path)])
    assert result.exit_code != 0
    assert "Invalid value for '-t' / '--timeout'" in result.output

def test_cli_invalid_output_dir():
    runner = CliRunner()
    # Provide a path that does not exist
    result = runner.invoke(cli, ['-t', '5', '-o', '/non/existing/path'])
    assert result.exit_code != 0
    assert "Invalid value for '-o' / '--output-dir'" in result.output