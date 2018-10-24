#!/bin/bash

INSTALLDIR=$1

if [ -z "$1" ]; then
   INSTALLDIR="~/Documents/MCPiScratch"
fi

if [ -d "$INSTALLDIR" ]; then
  # Control will enter here if $DIRECTORY exists.
    echo "Directory $INSTALLDIR already exists! Remove it first."
    exit 1
fi


echo "Installing Python and Pip, if not already installed..."
sudo apt install python python-pip -y

echo "Cloning MCPi-Scratch to folder from https://github.com/denosawr/MCPi-scratch..."
git clone https://github.com/denosawr/MCPi-Scratch.git $INSTALLDIR
cd $INSTALLDIR

echo "Installing requirements..."
pip install --user -r requirements.txt

echo "Installing extensions to Scratch..."
python installfiles/modifyExtensionsJson.py
mv installfiles/mcpi-scratch.png /usr/lib/scratch2/medialibrarythumbnails
mv mcpi-scratch.js /usr/lib/scratch2/scratch_extensions

