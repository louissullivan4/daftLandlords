import aiohttp
import asyncio
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
    print("done")

listing_event()
