# TODO List for development
## Core
- Synchronus runner
    - Maybe a python class that will handle that
- command line running
    - Basic cmd file that can be run
- plugins active
    - How to activate a plugin?
        - Auto detect?
        - Specified in command line?
- unittest


## Extra parts
- Settings file
    - Find type
    - make it work
- Service style
    - Make it run indefinately
    - Ditch (?) logs after x time
        - i.e. rolling logger but with .zip files
- Build
    - Build in linux package formats
        - Fedora
        - Ubuntu
    - Windows
- UI
    - Make a simple UI to display for selecting different plugin types
    - Want something that will be able to select "overall" debugger
        - i.e. memory
        - i.e. cpu usage
        - i.e. slow network
- Plugins
    - Make original plugins for a few basic operations
        - Austin
        - Journalctl
        - Networking
        - Top
        - Tshark
- github ci
    - post build & deploy
- Create readme for how to create new plugin
