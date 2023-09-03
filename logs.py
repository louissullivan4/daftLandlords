import datetime as dt
import aiohttp
from discord import Webhook

WEBHOOK_URL = 'https://discord.com/api/webhooks/1147654109789437962/PYjCLKlzWPYhuNcrmqlRNPG91tsfUaiC8WWJVN4auXSxs_qsowkxijklxYI_0SM5fPtN'

async def send_log_discord(message, type_msg):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(WEBHOOK_URL, session=session)
        message_struct = """```%stime: %s, type: %s, message: %s%s```""" % ("{", dt.datetime.now().strftime("%H:%M:%S"), type_msg, message, "}")
        await webhook.send(message_struct, username='DaftLandlords')