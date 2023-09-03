import aiohttp
import asyncio
import time
from discord import Webhook

from listings import get_listings
from db_interaction import *
from logs import *

create_db()

WEBHOOK_URL = 'https://discord.com/api/webhooks/1146434191546921074/OPHgwupeGo9kE--WXnFpO1wQJsOhfkdhoTBRRs6_4Z9Evt_TfjjmDq8YCvnJ5bNj193D'

async def send_listing(listing):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(WEBHOOK_URL, session=session)
        message_struct = f"""Address: {listing["address"]}\nPrice: {listing["price"]}\nBeds: {listing["beds"]}\nBaths: {listing["baths"]}\nProperty Type: {listing["property_type"]}\nURL: {listing["url"]}
        """
        await webhook.send(message_struct, username='DaftLandlords')

def listing_event():
    listings_dict = get_listings()
    existing_ids = db_select_existing_listings()
    scrapes_id = db_insert_scrapes(listings_dict)
    new_listings = 0
    for listing in listings_dict["listings"]:
        if listing["id"] not in existing_ids:
            db_insert_listings(listing, scrapes_id)
            asyncio.run(send_listing(listing))
            new_listings += 1
    message = f"""Number New Listings: {new_listings}"""
    asyncio.run(send_log_discord(message, "INFO"))


def run_scraper_periodically():
    start_time = time.time()
    while True:
        if (time.time() - start_time) > 43200:
            db_remove_all_data()
            message = f"""Database cleared!"""
            asyncio.run(send_log_discord(message, "DELETE"))
            start_time = time.time()
        listing_event()
        time.sleep(20)


if __name__ == "__main__":
    try:
        try:
            message = f"""Bot started"""
            asyncio.run(send_log_discord(message, "INFO"))
            run_scraper_periodically()
            message = f"""Bot stopped"""
            asyncio.run(send_log_discord(message, "INFO"))
        except Exception as e:
            message = f"""{e}"""
            asyncio.run(send_log_discord(message, "ERROR"))
    except KeyboardInterrupt:
        message = f"""Bot stopped"""
        asyncio.run(send_log_discord(message, "STOP"))