# mcpi-scratch
**Program RaspberryJuice and Minecraft: Pi Edition through Scratch 2.0!**

MCPi-Scratch is a Scratch extension and client application which allows for control of Minecraft: Pi Edition and Bukkit servers with the RaspberryJuice plugin, through Scratch.

## Installation
On a stock Raspberry Pi (or other Debian/Ubuntu machine), this command should install mcpi-scratch:
```sh
curl https://github.com/denosawr/mcpi-scratch/install.sh | sh
```

Otherwise, to install on another machine, make sure you have Python 2 and pip installed. Then, `git clone` this repo, install all relevant packages (`pip install -r requirements.txt`). Then, to get started, run the Python backend (`python mcpi-scratch.py`) and install the Scratch extension.

## Implemented features

MCPi-Scratch exposes a few new blocks to Scratch.
* get block at (`<X>`, `<Y>`, `<Z>`) -> returns `<block type>`
* set block at (`<X>`, `<Y>`, `<Z>`) to `<block type>`
* stood on block -> returns `<block type>`
* post `<message>` to chat
* set player position to (`<X>`, `<Y>`, `<Z>`)
* forward/back/left/right <n> blocks
* get position x/y/z -> returns `<position along X/Y/Z axis>`
