import aiohttp
import asyncio
import time
from discord import Webhook

from listings import get_listings
from db_interaction import *
from config import WEBHOOK_URL

create_db()

async def send_listing(listing):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(WEBHOOK_URL, session=session)
        message_struct = f"""
            Address: {listing["address"]}
            Price: {listing["price"]}
            Beds: {listing["beds"]}
            Baths: {listing["baths"]}
            Property Type: {listing["property_type"]}
            URL: {listing["url"]}
        """
        await webhook.send(message_struct, username='Landlords Are Pricks')

def listing_event():
    listings_dict = get_listings()
    existing_ids = db_select_existing_listings()
    scrapes_id = db_insert_scrapes(listings_dict)
    for listing in listings_dict["listings"]:
        if listing["id"] not in existing_ids:
            db_insert_listings(listing, scrapes_id)
            asyncio.run(send_listing(listing))
    print("Listing event complete")

def run_scraper_periodically():
    cycles = 0
    while True:
        listing_event()
        cycles += 1
        time.sleep(300)
    return cycles 

if __name__ == "__main__":
    "Running scraper every 5 minutes"
    # track how long program runs minutes
    start_time = time.time()    
    print("Starting scraper...")
    number_cycles = run_scraper_periodically()
    print("--- %s minutes ---" % ((time.time() - start_time)/60))
    print(f"Number of cycles: {number_cycles}")
    print("Scraper exited...")

    