import discord
import mcping

# Create and Initialize() a discord Client
from static.rooms import ChatRooms

client = discord.Client()
badwords = open("/opt/scripts/discord_bot/badwords.txt", "r").read().splitlines()


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

    # If it contains profanity
    if any(word in message.content.split(' ') for word in badwords):
        word = [word for word in badwords if word in message.content.split(' ')]
        await message.delete()
        await message.author.send(
            'Please keep the chat clean (Bad word: __{0}__), else I\'ll rip your friggin\' arms off. \N{SERIOUS FACE WITH SYMBOLS COVERING MOUTH}'.format(
                word[0])
        )

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
            ping = mcping.ping('127.0.0.1')

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
client.run('ODgyMjk5MzcyNTc3MTEyMDY1.YS5XUg.iEMOg_ePoL9RxYonyL3FeFiPSho')
