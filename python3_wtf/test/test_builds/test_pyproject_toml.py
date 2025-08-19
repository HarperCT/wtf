import unittest
import tempfile
import pathlib
import subprocess
import sys
import venv

class TestPython3WTFBuild(unittest.TestCase):
    PROJECT_DIR = pathlib.Path("python3_wtf/src")

    def test_build_creates_dist(self):
        """Test that building the package produces .whl and .tar.gz files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            build_dir = pathlib.Path(tmpdir)
            # Run the build in the python3_wtf directory
            subprocess.run(
                [sys.executable, "-m", "build", "--outdir", str(build_dir)],
                check=True,
                cwd=self.PROJECT_DIR
            )

            wheel = next(build_dir.glob("*.whl"), None)
            sdist = next(build_dir.glob("*.tar.gz"), None)
            self.assertIsNotNone(wheel, "No wheel file found")
            self.assertIsNotNone(sdist, "No sdist file found")

    def test_package_installation(self):
        """Test that the built wheel can be installed in a temporary venv."""
        with tempfile.TemporaryDirectory() as tmpdir, tempfile.TemporaryDirectory() as venv_dir:
            build_dir = pathlib.Path(tmpdir)
            subprocess.run(
                [sys.executable, "-m", "build", "--outdir", str(build_dir)],
                check=True,
                cwd=self.PROJECT_DIR
            )
            wheel = next(build_dir.glob("*.whl"), None)
            self.assertIsNotNone(wheel, "No wheel file found for installation test")

            # Create a temporary venv
            venv.create(venv_dir, with_pip=True)
            python_bin = pathlib.Path(venv_dir) / "bin" / "python"

            # Install the wheel into the venv
            subprocess.run([python_bin, "-m", "pip", "install", str(wheel)], check=True)

            # Check import
            subprocess.run(
                [python_bin, "-c", "import python3_wtf"],
                check=True
            )

    def test_cli_runs(self):
        """Test that CLI entry points work in a clean environment."""
        with tempfile.TemporaryDirectory() as tmpdir, tempfile.TemporaryDirectory() as venv_dir:
            build_dir = pathlib.Path(tmpdir)
            subprocess.run(
                [sys.executable, "-m", "build", "--outdir", str(build_dir)],
                check=True,
                cwd=self.PROJECT_DIR
            )
            wheel = next(build_dir.glob("*.whl"), None)
            self.assertIsNotNone(wheel, "No wheel file found for CLI test")

            # Create a temporary venv
            venv.create(venv_dir, with_pip=True)
            python_bin = pathlib.Path(venv_dir) / "bin" / "python"

            # Install the wheel
            subprocess.run([python_bin, "-m", "pip", "install", str(wheel)], check=True)

            # Run the CLI
            subprocess.run([python_bin, "-m", "python3_wtf.wtf_cli", "--help"], check=True)