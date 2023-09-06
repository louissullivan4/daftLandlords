import datetime as dt
import aiohttp
from discord import Webhook

WEBHOOK_URL = 'https://discord.com/api/webhooks/1147654103594438776/EYJmZqC2dqYqCRZJK-i7q89NdiKMtsFE3yy7l6kX9NxcXWN70jToqvp5yXLTaZ812SAC'

async def send_log_discord(message, type_msg):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(WEBHOOK_URL, session=session)
        message_struct = """```%stime: %s, type: %s, message: %s%s```""" % ("{", dt.datetime.now().strftime("%H:%M:%S"), type_msg, message, "}")
        await webhook.send(message_struct, username='DaftLandlords')