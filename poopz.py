import asyncio

from datetime import datetime, timedelta
from typing import Any
from mcstatus import JavaServer

import os
from discord.ext import commands
from discord import Intents, Embed, utils

from modules.profanity import ProfanityModule
from modules.strike import StrikeModule
from static.rooms import ChatRooms


class PoopzClient(commands.Bot):
    def __init__(self, **options: Any):
        intents = Intents.default()
        intents.message_content = True

        super().__init__(command_prefix="!", intents=intents, **options)

        self.profanity_module = ProfanityModule()
        self.strike_module = StrikeModule()

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

            muted = self.strike_module.strike(message.author.id)
            if muted:
                muted_person = self.strike_module.get(message.author.id)
                minutes_muted = round(muted_person.next_mute_time / 60)
                await message.author.timeout(utils.utcnow() + timedelta(minutes=minutes_muted))
                await message.author.send(
                    f"""
                        You have been muted for {minutes_muted} minutes for excessive use of profanity.
                        Keep it clean in the future.
                    """
                )

                admin_channel = self.get_channel(ChatRooms.MOD_CHAT.value)
                await admin_channel.send(
                    f"""
                    {message.author.display_name} has been muted for {minutes_muted} minutes for excessive use of profanity.
                    """
                )

            else:
                await message.author.send(self.profanity_module.get_message_reply())

            # Can return here, nothing else to do with the message.
            return

        # If it was a message sent in the #suggestions room add reactions to it
        if message.channel.id == ChatRooms.SUGGESTIONS.value:
            await asyncio.gather(
                message.add_reaction('\N{THUMBS UP SIGN}'),
                message.add_reaction('\N{THUMBS DOWN SIGN}')
            )

        # If a message is sent to our ingame channel
        if message.channel.id == ChatRooms.INGAME.value or message.channel.id == ChatRooms.MOD_DEVELOPMENT_BOT.value:

            # If the message starts with !online or !list
            if message.content.startswith('!online') or message.content.startswith('!list'):

                server = JavaServer.lookup(os.getenv('MC_SERVER_IP') + ":" + os.getenv('MC_SERVER_PORT'))
                status = server.status()
                query = server.query()

                # Create an embed message and send it
                embedded = Embed(title="Online Players - Mc.Popzi.Net", color=0x00ff00)
                embedded.add_field(name="Online", value="{0}/{1}".format(status.players.online, status.players.max))
                embedded.add_field(name="RT", value="{0}ms".format(round(status.latency, 2)))
                embedded.add_field(name="Version", value="{0} ({1})".format(status.version.name, status.version.protocol))
                embedded.add_field(name="Players", value="\n".join(query.players.names))
                embedded.timestamp = datetime.now()
                embedded.set_thumbnail(url="https://i.imgur.com/QKzkLzr.png")  # Todo: Move to popzi.net

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

        await self.process_commands(message)
