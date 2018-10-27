#!/bin/bash

INSTALLDIR=$2
BRANCH=$1

if [ -z "$2" ]; then
   INSTALLDIR=~/Documents/MCPiScratch
fi

if [ -z "$1" ]; then
    BRANCH="master"
fi

if [ -d "$INSTALLDIR" ]; then
  # Control will enter here if $DIRECTORY exists.
    echo "Directory $INSTALLDIR already exists! Remove it first."
    exit 1
fi


echo "Installing Python, Pip and sed, if not already installed..."
sudo apt-get install python python-pip -y > /dev/null

echo "Cloning MCPi-Scratch to folder from https://github.com/denosawr/mcpi-scratch..."
git clone --quiet https://github.com/denosawr/MCPi-Scratch.git $INSTALLDIR --branch $BRANCH
cd $INSTALLDIR

echo "Installing requirements..."
pip install --quiet --user -r requirements.txt

echo "Installing extensions to Scratch..."
sudo python installfiles/modifyExtensionsJson.py
sudo cp -f installfiles/mcpi-scratch.png /usr/lib/scratch2/medialibrarythumbnails
sudo cp -f mcpi-scratch/mcpi-scratch.js /usr/lib/scratch2/scratch_extensions

echo "Installing desktop executable..."
chmod +x mcpi-scratch/mcpi-scratch-server.py
sed -i -e "s/Icon=.*/Icon=$(realpath installfiles/mcpi-scratch.png | sed 's_/_\\/_g')/" installfiles/mcpi-scratch-server.desktop
sed -i -e "s/Exec=.*/Exec=lxterminal --command=\"\/bin\/bash -c 'python -i $(realpath mcpi-scratch/mcpi-scratch-server.py | sed 's_/_\\/_g')'\"/" installfiles/mcpi-scratch-server.desktop
cp -f installfiles/mcpi-scratch-server.desktop ~/.local/share/applications/
cp -f installfiles/mcpi-scratch-server.desktop ~/Desktop

echo "Complete! Use the launcher to get started."
