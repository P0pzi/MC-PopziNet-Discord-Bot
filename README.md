## MC-PopziNet-Discord-Bot

The discord bot used by the Popzi.Net Minecraft discord channel

## Features
* Smart Profanity Filter
* Screenshot Channel Managemnet
* Suggestion Emojis
* Online Listings

## Commands
* `!list` | `!online` - Shows who's online currently when ran in the #ingame channel


## Setup

1. Setup Server Environment
   1. `$ export CLIENT_SECRET="DISCORD_BOTS_SECRET_KEY_GOES_HERE"`
   2. `$ ssh-keygen -t ed25519 -C "YOUR_GITHUB_USERNAME_OR_EMAIL"`
      1. Note - Leave the filename field blank if this is your first time running this command (else it won't create the `~/.ssh/` directory)
   3. `$ touch ~/.ssh/config`
   4. `$ nano ~/.ssh/config`
       1. ```bash 
          Host GIVE_ME_A_NAME
          HostName github.com
          AddKeysToAgent yes
          PreferredAuthentications publickey
          IdentityFile ~/.ssh/FILE_NAME_CREATED_WITH_SSH-KEYGEN
          ```
    5. `$ cat ~/.ssh/FILE_NAME_CREATED_WITH_SSH-KEYGEN.pub`
       1. Should look something like `ssh-ed25519 AABAC3EzaC1lZDI12TE5AAA4IGW15dZfJiOll71kh+UL3K4Ik0tZj21e1HLJ/C1FHl1e YOUR_GITHUB_USERNAME_OR_EMAIL`
       
2. Setup Github Deployment Key
   1. Go to [Settings > Deployment Key](https://github.com/P0pzi/MC-PopziNet-Discord-Bot/settings/keys)
   2. Add Deploy Key
      1. Title: Anything
      2. Key: Paste the contents of `~/.ssh/FILE_NAME_CREATED_WITH_SSH-KEYGEN.pub`
      3. Add Key
3. Clone Git Repo
   1. `$ git clone git@GIVE_ME_A_NAME:P0pzi/MC-PopziNet-Discord-Bot.git`
4. Create Virtual Environment
   1. `$ apt install virtualenv -y`
   2. `$ virtualenv ./venv`
   3. `$ source ./venv/bin/activate`
   4. `$ python3 -m pip install -r ./requirements.txt`
5. Run the application
   1. `$ source ./venv/bin/activate`
   2. `$ python3 ./main.py`

