#!/bin/bash

INSTALLDIR=$1

if [ -z "$1" ]; then
   INSTALLDIR="~/Documents/MCPiScratch"
fi

echo "Installing Python and Pip, if not already installed..."
sudo apt install python python-pip -y > /dev/null

echo "Cloning MCPi-Scratch to folder from https://github.com/denosawr/MCPi-scratch..."
git clone --quiet -b develop https://github.com/denosawr/MCPi-Scratch.git $INSTALLDIR
cd $INSTALLDIR

echo "Installing requirements..."
pip install --quiet --user -r requirements.txt

echo "Installing extensions to Scratch..."
sudo python installfiles/modifyExtensionsJson.py
sudo mv installfiles/mcpi-scratch.png /usr/lib/scratch2/medialibrarythumbnails
sudo mv mcpi-scratch.js /usr/lib/scratch2/scratch_extensions

echo "Complete! Use the launcher to get started."
