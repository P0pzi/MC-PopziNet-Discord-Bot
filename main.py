import os
import discord
import mcping

# Create and Initialize() a discord Client
from modules.profanity import Profanity
from static.rooms import ChatRooms

from dotenv import load_dotenv

# Ensure Environmental variables are set
load_dotenv()
assert os.getenv('CLIENT_SECRET')
assert os.getenv('MC_SERVER_IP')
assert os.getenv('MC_SERVER_PORT')

# Create and Initialize() a discord Client
client = discord.Client()


# If an on_ready() event is called, say we're ready
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# If a on_message() event is called, figure out what to do
@client.event
async def on_message(message):
    # If the person who sent the message is us
    if message.author == client.user:
        return  # Return nothing. Ignore it.

    profanity = Profanity(message)
    if profanity.has_profanity:
        await message.delete()
        await message.author.send(profanity.get_message_reply())

    # If it was a message sent in the #suggestions room
    # (Room ID 705786147200303104) add reactions to it
    if message.channel.id == ChatRooms.SUGGESTIONS:
        await message.add_reaction('\N{THUMBS UP SIGN}')
        await message.add_reaction('\N{THUMBS DOWN SIGN}')

    # If a message is sent to our ingame channel
    if message.channel.id == ChatRooms.INGAME:

        # If the message starts with !online or !list
        if message.content.startswith('!online') or message.content.startswith('!list'):

            # Ping the server to query player info
            ping = mcping.ping(os.getenv('MC_SERVER_IP'), int(os.getenv('MC_SERVER_PORT')))

            # Change the <Players> to <Strings>
            names = []
            for player in ping.players:
                names.append(player.name)

            # Create an embed message and send it
            embedded = discord.Embed(
                title="Online Players - Mc.Popzi.Net",
                description="\n".join(names), color=0x00ff00
            )
            await message.channel.send(embed=embedded)

    # If a message is sent to our screenshots channel
    if message.channel.id == ChatRooms.SCREENSHOTS:
        # If it's not got any screenshots in it
        if not message.attachments:
            await message.delete()
            await message.author.send(
                'Please keep this channel to screenshots only, or I will hunt you down ' +
                'and feast on your body. \N{POULTRY LEG}\N{FORK AND KNIFE}'
            )


# Login & Run our client using our secret password
client.run(os.getenv('CLIENT_SECRET'))
