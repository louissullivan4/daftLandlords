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
    while True:
        message = f"""Listing Event started at {time.strftime("%H:%M:%S", time.localtime(time.time()))}"""
        asyncio.run(send_log_discord(message, "INFO"))
        listing_event()
        message = f"""Listing Event completed at {time.strftime("%H:%M:%S", time.localtime(time.time()))}"""
        asyncio.run(send_log_discord(message, "INFO"))
        time.sleep(60)


if __name__ == "__main__":
    try:
        start_time = time.time()
        delete_time = time.time()
        if time.time() - delete_time > 43200:
            db_remove_all_data()
            message = f"""Database cleared at {time.strftime("%H:%M:%S", time.localtime(time.time()))}"""
            asyncio.run(send_log_discord(message, "DELETE"))
            delete_time = time.time()
        message = f"""Bot started at {time.strftime("%H:%M:%S", time.localtime(time.time()))}"""
        asyncio.run(send_log_discord(message, "INFO"))
        run_scraper_periodically()
        message = f"""Bot stopped at {time.strftime("%H:%M:%S", time.localtime(time.time()))}"""
        asyncio.run(send_log_discord(message, "INFO"))
    except KeyboardInterrupt:
        message = f"""Bot stopped at {time.strftime("%H:%M:%S", time.localtime(time.time()))}"""
        asyncio.run(send_log_discord(message, "INFO"))
