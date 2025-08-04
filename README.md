# WTF (Where's The Fault)

**WTF** is your all-in-one debugging sidekick, designed to help developers of all skill levels collect logs, track outputs, and scream into the void—all with a single command.
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
TODO how to build package

## How to install
TODO deploy to pypi to easily install (i.e. pip install wtf)
TODO build on a few linux distros to deploy
