import os

from datetime import datetime

from mcstatus import JavaServer
from discord import Embed

from static.rooms import ChatRooms


async def check_online_status(message):
    channel_id = message.channel.id

    if channel_id not in [
        ChatRooms.INGAME.value,
        ChatRooms.MOD_DEVELOPMENT_BOT.value
    ]:
        return

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