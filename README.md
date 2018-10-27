# mcpi-scratch
**Program RaspberryJuice and Minecraft: Pi Edition through Scratch 2.0!**

MCPi-Scratch is a Scratch extension and client application which allows for control of Minecraft: Pi Edition and Bukkit servers with the RaspberryJuice plugin, through Scratch.

## Installation on Raspberry Pi
On a stock Raspberry Pi running Raspbian, this command should install mcpi-scratch:
```sh
curl -s https://denosawr.github.io/mcpi-scratch/install.sh | sh
```

If you want to install the bleeding-edge version on the `develop` branch, instead use: `curl -s https://denosawr.github.io/mcpi-scratch/install.sh | sh -s <branch (e.g. develop) <folder to clone to>>`

When all that's done, open Scratch, click More Blocks, click Add an Extension and select MCPi-Scratch! You should see the blocks appear after clicking OK. On your desktop should be an executable; double click it to launch the server.

**Note that on any other Linux distro, or macOS or Windows, this will not work. Raspbian has a special version of Scratch distributed with it, which allows for custom extension installation. It's highly recommended that you use ScratchX.**

Otherwise, to install on another machine, make sure you have Python 2 and pip installed. Then, `git clone` this repo, install all relevant packages (`pip install -r requirements.txt`). Then, to get started, run the Python backend (`python mcpi-scratch.py`) and install the Scratch extension.

## Installation on ScratchX
ScratchX is an official custom version of Scratch 2.0 which supports JavaScript extensions. [Fire up ScratchX](https://scratchx.org/#scratch), head to More Blocks and tap on "Load Experimental Extension". Paste `https://denosawr.github.io/mcpi-scratch/mcpi-scratch.js` into the `paste url...` box, click Open, and the blocks should appear.

**TODO**: setting up server & stuff

## Implemented features

MCPi-Scratch exposes a few new blocks to Scratch.
* get block at (`<X>`, `<Y>`, `<Z>`) -> returns `<block type>`
* set block at (`<X>`, `<Y>`, `<Z>`) to `<block type>`
* stood on block -> returns `<block type>`
* post `<message>` to chat
* set player position to (`<X>`, `<Y>`, `<Z>`)
* forward/back/left/right <n> blocks
* get position x/y/z -> returns `<position along X/Y/Z axis>`


## Behind the scenes

Currently, MCPi-Scratch's server app (Python) is a Flask webserver. A goal is to eventually shift this to using websockets, which should be faster.

