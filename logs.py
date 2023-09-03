import datetime as dt
import aiohttp
from discord import Webhook

WEBHOOK_URL = 'https://discord.com/api/webhooks/1147654109789437962/PYjCLKlzWPYhuNcrmqlRNPG91tsfUaiC8WWJVN4auXSxs_qsowkxijklxYI_0SM5fPtN'
MENTIONS_URL = 'https://discord.com/api/webhooks/1148017920077737994/1Ls5BbsPpwJp1o3N0zZFY9rJk3nMDjHmfOW6CE4Jg7mN6Wxdeo5Pz-LDg7McRLVReM8F'

async def send_log_discord(message, type_msg):
    async with aiohttp.ClientSession() as session:
        if type_msg == "ERROR":
            webhook = Webhook.from_url(MENTIONS_URL, session=session)
            message_struct = """```%stime: %s, type: %s, message: %s%s```""" % ("{", dt.datetime.now().strftime("%H:%M:%S"), type_msg, message, "}")
        webhook = Webhook.from_url(WEBHOOK_URL, session=session)
        message_struct = """```%stime: %s, type: %s, message: %s%s```""" % ("{", dt.datetime.now().strftime("%H:%M:%S"), type_msg, message, "}")
        await webhook.send(message_struct, username='DaftLandlords')