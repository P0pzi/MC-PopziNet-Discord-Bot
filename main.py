import discord
import os

from dotenv import load_dotenv
from poopz import PoopzClient

# Ensure Environmental variables are set
load_dotenv()
assert os.getenv('CLIENT_SECRET')
assert os.getenv('MC_SERVER_IP')
assert os.getenv('MC_SERVER_PORT')

intents = discord.Intents.default()
intents.message_content = True
client = PoopzClient(intents=intents)
client.run(os.getenv('CLIENT_SECRET'))
