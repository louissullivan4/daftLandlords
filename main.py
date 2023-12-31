import aiohttp
import asyncio
import time
from discord import Webhook

from listings import get_listings
from db_interaction import *
from logs import *

create_db()

WEBHOOK_URL = 'https://discord.com/api/webhooks/1146434183162503208/g7SZB51SkbYTqJXNqNALzIwFT15wrVqOv7sH3tnoyUo62u2G5Ml897EwdKlfM6WhRDaj'

async def send_listing(listing):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(WEBHOOK_URL, session=session)
        message_struct = f"""Address: {listing["address"]}\nPrice: {listing["price"]}\nBeds: {listing["beds"]}\nBaths: {listing["baths"]}\nProperty Type: {listing["property_type"]}\nURL: {listing["url"]}
        """
        await webhook.send(message_struct, username='DaftLandlords')

def listing_event():
    try:
        listings_dict = get_listings()
        existing_ids = db_select_existing_listings()
        scrapes_id = db_insert_scrapes(listings_dict)
        new_listings = 0
        for listing in listings_dict["listings"]:
            if listing["id"] not in existing_ids:
                db_insert_listings(listing, scrapes_id)
                asyncio.run(send_listing(listing))
                new_listings += 1
        if new_listings > 0:
            message = f"""Number New Listings: {new_listings}"""
            asyncio.run(send_log_discord(message, "INFO"))
            print(message)
    except Exception as e:
        asyncio.run(send_log_discord(e, "ERROR"))
        print(e)
        


def run_scraper_periodically():
    start_time = time.time()
    while True:        
        if (time.time() - start_time) > 43200:
            db_remove_all_data()
            message = f"""Database cleared!"""
            asyncio.run(send_log_discord(message, "DELETE"))
            print(message)
            start_time = time.time()
        listing_event()
        time.sleep(20)


if __name__ == "__main__":
    try:
        message = f"""Bot started"""
        asyncio.run(send_log_discord(message, "INFO"))
        run_scraper_periodically()
        message = f"""Bot stopped"""
        asyncio.run(send_log_discord(message, "INFO"))
    except KeyboardInterrupt:
        message = f"""Bot stopped"""
        asyncio.run(send_log_discord(message, "STOP"))