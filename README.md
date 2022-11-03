## MC-PopziNet-Discord-Bot

The discord bot used by the Popzi.Net Minecraft discord channel

## Features
* Smart Profanity Filter
* Screenshot Channel Management
* Suggestion Emojis
* Online Listings

## Commands
* `!list` | `!online` - Shows who are online currently when ran in the #ingame channel


## Setup

### Standalone
1. Clone Git Repo
   1. `$ git clone https://github.com/P0pzi/MC-PopziNet-Discord-Bot.git`
2. Create Virtual Environment
   1. `$ python3 -m venv ./venv`
   3. `$ source ./venv/bin/activate`
   4. `$ python3 -m pip install -r ./requirements.txt`
3. Run the application
   1. `$ source ./venv/bin/activate`
   2. `$ python3 ./main.py`

### Docker - Portainer

1. Images > Build a new image
   1. Name: `example-image-name`
   2. URL: `https://github.com/P0pzi/MC-PopziNet-Discord-Bot/docker`
2. Containers > Add Container
   1. Name: `example-container-name`
   2. Image:  `example-image-name:latest`
3. Deploy
