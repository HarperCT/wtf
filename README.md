# WTF (Where's The Fault)

**WTF** is your all-in-one debugging sidekick, designed to help developers of all skill levels collect logs, track outputs, and scream into the void - all with a single command.
This was designed for the intern out on site and when the senior says "get the logs and send them to me" you can run 1 simple command and it will collect them all in one .zip file!

Currently built for Python 12.2.3

## How to use
### Using the CLI
WTF has a CLI interface that you can define all variables through. For plugins that require specific args to parse you can use the `--plugin` option like:
`python3 wtf_cli.py -t 10 -o /tmp/ -p tshark "interface_name --hexdump"`
or use `python3 wtf_cli.py --help` for more complete options

#### How the --plugins arg works
You can use multiple instances of the --plugin argument to generate multiple of the same plugin or to specify multiple different plugins. This allows users to run multiple commands of the same time in different subprocesses. They will generate 2 different file logs captured in the wtf_output.zip
Example:
--plugin tshark "-i enpxxx" --plugin tshark "-i enpyyy --hexdump"

### Using the TUI
TODO make a TUI

### Using a UI
TODO make a UI

## How to build
### Manual
1. Use python3 -m build from python3_wtf/src/directory (wherepyproject.toml` lives).
2. dist/ folder will be created, containing .tar.gz and .whl packages.
3. Activate virtual env - source {venv_name}/bin/activate
4. Run pip install path/to/dist/python3_wtf-{version}.{hash}.tar.gz
5. You can now use wtf-cli in the virtual env cli

### Using Scripts
1. Navigate to {project_root_dir}/tools
2. Run ./linux_setup.sh
3. Run ./build.sh
4. The newly built packages will be stored in {project_root_dir}/python3_wtf/src/dist/

## How to install
TODO deploy to pypi to easily install (i.e. pip install wtf)
TODO build on a few linux distros to deploy
