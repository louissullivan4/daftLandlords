import sqlite3

def create_db():
    db_connection = sqlite3.connect('daftLandlords.db')
    cursor = db_connection.cursor()
    create_daftLandlords_Scrapes_query = '''
    CREATE TABLE IF NOT EXISTS daftLandlords_Scrapes (
        scrapes_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        time TEXT,
        listing_count INTEGER
    )
    '''
    create_daftLandlords_Listings_query = '''
    CREATE TABLE IF NOT EXISTS daftLandlords_Listings (
        listings_id TEXT PRIMARY KEY,
        scrapes_id INT,
        address TEXT,
        price TEXT,
        beds TEXT,
        baths TEXT,
        property_type TEXT,
        url TEXT
    )
    '''
    cursor.execute(create_daftLandlords_Scrapes_query)
    cursor.execute(create_daftLandlords_Listings_query)
    db_connection.commit()
    db_connection.close()

def db_get_all_listings():
    db_connection = sqlite3.connect('daftLandlords.db')
    cursor = db_connection.cursor()

    select_daftLandlords_Listings_query = '''
    SELECT *
    FROM daftLandlords_Listings
    '''
    cursor.execute(select_daftLandlords_Listings_query)
    listings = cursor.fetchall()

    db_connection.close()
    return listings

def db_select_existing_listings():
    db_connection = sqlite3.connect('daftLandlords.db')
    cursor = db_connection.cursor()

    select_daftLandlords_Listings_query = '''
    SELECT listings_id
    FROM daftLandlords_Listings
    '''
    cursor.execute(select_daftLandlords_Listings_query)
    existing_ids = []
    for row in cursor.fetchall():
        existing_ids.append(row[0])

    db_connection.close()
    return existing_ids

def db_insert_scrapes(listing_dict):
    db_connection = sqlite3.connect('daftLandlords.db')
    cursor = db_connection.cursor()

    insert_daftLandlords_Scrapes_query = '''
    INSERT INTO daftLandlords_Scrapes (date, time, listing_count)
    VALUES (?, ?, ?)
    '''
    cursor.execute(insert_daftLandlords_Scrapes_query, (listing_dict["date_retrieved"], listing_dict["time_retrieved"], listing_dict["listing_count"]))
    db_connection.commit()
    db_connection.close()
    return cursor.lastrowid

def db_insert_listings(listing, scrapes_id):
    db_connection = sqlite3.connect('daftLandlords.db')
    cursor = db_connection.cursor()

    insert_daftLandlords_Listings_query = '''
    INSERT INTO daftLandlords_Listings (listings_id, scrapes_id, address, price, beds, baths, property_type, url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''
    cursor.execute(insert_daftLandlords_Listings_query, (listing["id"], scrapes_id, listing["address"], listing["price"], listing["beds"], listing["baths"], listing["property_type"], listing["url"]))
    db_connection.commit()
    db_connection.close()

def db_remove_scrape_id(scrape_id):
    db_connection = sqlite3.connect('daftLandlords.db')
    cursor = db_connection.cursor()

    delete_daftLandlords_Scrapes_query = '''
    DELETE FROM daftLandlords_Listings
    WHERE scrapes_id = ?
    '''
    cursor.execute(delete_daftLandlords_Scrapes_query, (scrape_id,))
    db_connection.commit()
    db_connection.close()

def db_remove_listing_id(listing_id):
    db_connection = sqlite3.connect('daftLandlords.db')
    cursor = db_connection.cursor()

    delete_daftLandlords_Listings_query = '''
    DELETE FROM daftLandlords_Listings
    WHERE listings_id = ?
    '''
    cursor.execute(delete_daftLandlords_Listings_query, (listing_id,))
    db_connection.commit()
    db_connection.close()

def db_remove_all_data():
    db_connection = sqlite3.connect('daftLandlords.db')
    cursor = db_connection.cursor()

    delete_daftLandlords_Scrapes_query = '''
    DELETE FROM daftLandlords_Scrapes
    '''
    delete_daftLandlords_Listings_query = '''
    DELETE FROM daftLandlords_Listings
    '''
    delete_daftLandlords_seq = '''
    DELETE FROM sqlite_sequence
    '''
    cursor.execute(delete_daftLandlords_Scrapes_query)
    cursor.execute(delete_daftLandlords_Listings_query)
    cursor.execute(delete_daftLandlords_seq)
    db_connection.commit()
    db_connection.close()