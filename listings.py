# web scrape for listings on https://www.daft.ie/property-for-rent/cork-city?showMap=false&sort=priceAsc

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import datetime as dt

def get_listings():
    final_listings_dict = {}
    listings_html = requests.get("https://www.daft.ie/property-for-rent/cork-city?showMap=false&sort=priceAsc")
    soup = BeautifulSoup(listings_html.text, 'html.parser')
    listing_count = int(soup.select('h1[data-testid="search-h1"]')[0].get_text().split()[0])
    total_listings = []
    if listing_count > 20:
        pages = listing_count // 20
        if listing_count % 20 != 0:
            pages += 1
        for page in range(pages):
            page_html = requests.get(f"https://www.daft.ie/property-for-rent/cork-city?showMap=false&sort=priceAsc&pageSize=20&from={page*20}")
            soup = BeautifulSoup(page_html.text, 'html.parser')
            listing_page = soup.select('ul[data-testid="results"] li')
            temp_list = []
            for house in listing_page:
                temp_dict = {}
                temp_dict["id"] = house.select('a')[0]['href'].split('/')[-1]
                temp_dict["address"] = house.select('h2[data-testid="address"]')[0].text
                temp_dict["price"] = house.select('div[data-testid="price"]')[0].text
                bed_info = house.select('div[data-testid="card-info"] p[data-testid="beds"]')
                temp_dict["beds"] = bed_info[0].text.split(' ')[0] if bed_info else "n/a"
                bath_info = house.select('div[data-testid="card-info"] p[data-testid="baths"]')
                temp_dict["baths"] = bath_info[0].text.split(' ')[0] if bath_info else "n/a"
                property_type = house.select('div[data-testid="card-info"] p[data-testid="property-type"]')
                temp_dict["property_type"] = property_type[0].text if property_type else "n/a"
                temp_dict["url"] = "https://www.daft.ie" + house.select('a')[0]['href']    
                temp_list.append(temp_dict)
            total_listings += temp_list
    final_listings_dict["listing_count"] = len(total_listings)
    final_listings_dict["listings"] = total_listings
    final_listings_dict["date_retrieved"] = dt.datetime.now().strftime("%d/%m/%Y")
    final_listings_dict["time_retrieved"] = dt.datetime.now().strftime("%H:%M:%S")
    # pprint(final_listings_dict)
    return final_listings_dict
 
get_listings()