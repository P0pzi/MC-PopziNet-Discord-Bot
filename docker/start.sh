#!/bin/bash

# This script is by no means fancy.

# Make some directory files, because Docker is too stupid to do this apparently.
if [ ! -d "/PopziNet/bin)" ]; then
  mkdir /PopziNet/bin
fi

# Create venv
if [ ! -d "/PopziNet/bin/venv)" ]; then
  echo "Creating new venv..."
  python3 -m venv /PopziNet/bin/venv
  echo "venv created in /PopziNet/bin/venv"
else
   echo "venv already exists."
fi

# Clone git repo
echo "Cloning Github Repo..."
cd /PopziNet/bin || exit
git clone "${GITHUB_REPO_HTTPS}"
echo "Done"

echo "Downloading dependencies..."
/PopziNet/bin/venv/bin/python3 -m pip install -r /PopziNet/bin/MC-PopziNet-Discord-Bot/requirements.txt


echo "Starting Bot..."
cd /PopziNet/bin/MC-PopziNet-Discord-Bot/ || exit
/PopziNet/bin/venv/bin/python3 /PopziNet/bin/MC-PopziNet-Discord-Bot/main.py
