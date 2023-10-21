import asyncio

from datetime import timedelta
from typing import Any

from discord.ext import commands
from discord import Intents, Embed, utils

from modules.profanity import ProfanityModule
from modules.status import check_online_status
from modules.strike import StrikeModule
from static.rooms import ChatRooms


class PoopzClient(commands.Bot):
    def __init__(self, **options: Any):
        intents = Intents.default()
        intents.message_content = True

        super().__init__(command_prefix="!", intents=intents, **options)
        # Make status commands
        for name in ['status', 'list', 'online']:
            self.command(name=name, pass_context=True)(check_online_status)

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
            embedded_message = Embed()
            embedded_message.add_field(name='Message', value=message.content)

            if muted:
                muted_person = self.strike_module.get(message.author.id)
                minutes_muted = round(muted_person.next_mute_time / 60)
                await message.author.timeout(utils.utcnow() + timedelta(minutes=minutes_muted))
                await message.author.send(
                    f"""
                        You have been muted for {minutes_muted} minutes for excessive use of profanity.
                        Keep it clean in the future.
                    """,
                    embed=embedded_message
                )

                admin_channel = self.get_channel(ChatRooms.MOD_CHAT.value)
                await admin_channel.send(
                    f"""
                    {message.author.display_name} has been muted for {minutes_muted} minutes for excessive use of profanity.
                    """
                )

            else:
                await message.author.send(self.profanity_module.get_message_reply(), embed=embedded_message)

            # Can return here, nothing else to do with the message.
            return

        # If it was a message sent in the #suggestions room add reactions to it
        if message.channel.id == ChatRooms.SUGGESTIONS.value:
            await asyncio.gather(
                message.add_reaction('\N{THUMBS UP SIGN}'),
                message.add_reaction('\N{THUMBS DOWN SIGN}')
            )

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
