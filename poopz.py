from typing import Any

import os
import mcping
import discord
from discord import Intents

from modules.profanity import Profanity
from static.rooms import ChatRooms


class PoopzClient(discord.Client):
    def __init__(self, **options: Any):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(intents=intents, **options)

        self.profanity_module = Profanity()

    async def on_ready(self):
        print(f'We have logged on as {self.user}!')

    async def on_message(self, message):
        # If the person who sent the message is us
        if message.author == self.user:
            return  # Return nothing. Ignore it.

        self.profanity_module\
            .reset()\
            .set_message(message)\
            .check()

        if self.profanity_module.has_profane_words:
            await message.delete()
            await message.author.send(self.profanity_module.get_message_reply())
            # Can return here, nothing else to do with the message.
            return

        # If it was a message sent in the #suggestions room add reactions to it
        if message.channel.id == ChatRooms.SUGGESTIONS.value:
            await message.add_reaction('\N{THUMBS UP SIGN}')
            await message.add_reaction('\N{THUMBS DOWN SIGN}')

            # If a message is sent to our ingame channel
            if message.channel.id == ChatRooms.INGAME.value:

                # If the message starts with !online or !list
                if message.content.startswith('!online') or message.content.startswith('!list'):
                    # Ping the server to query player info
                    ping = mcping.ping(os.getenv('MC_SERVER_IP'), int(os.getenv('MC_SERVER_PORT')))

                    # Change the <Players> to <Strings>
                    names = [player.name for player in ping.players]

                    # Create an embed message and send it
                    embedded = discord.Embed(
                        title="Online Players - Mc.Popzi.Net",
                        description="\n".join(names), color=0x00ff00
                    )
                    await message.channel.send(embed=embedded)

        # If a message is sent to our screenshots channel
        if message.channel.id == ChatRooms.SCREENSHOTS.value:
            # If it's not got any screenshots in it
            if not message.attachments:
                await message.delete()
                await message.author.send(
                    'Please keep this channel to screenshots only, or I will hunt you down ' +
                    'and feast on your body. \N{POULTRY LEG}\N{FORK AND KNIFE}'
                )

