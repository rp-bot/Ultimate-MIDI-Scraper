from Chrome.installer import install_driver, By, ActionChains, Keys
from pprint import pprint
import time
import sqlite3

DRIVER = install_driver()

conn = sqlite3.connect('data/db/UltimateMidi.sqlite3')
c = conn.cursor()

STR_TABLE = str.maketrans({"-": "_", " ": "_"})


def retrieve_from_genres():
    select_data = '''SELECT * FROM genres'''
    c.execute(select_data)
    rows = c.fetchall()
    return rows


def add_artists_bands(genre_list):
    # c = conn.cursor()

    # create_table = '''CREATE TABLE IF NOT EXISTS artists_bands (ID INTEGER PRIMARY KEY,genre TEXT,url TEXT)'''
    # c.execute(create_table)
    # conn.commit()

    DRIVER.switch_to.window(DRIVER.window_handles[-1])
    artists = DRIVER.find_elements(By.CLASS_NAME, "genre-band-container")
    for i, artist in enumerate(artists):
        artist_name = artist.text
        artist_url = artist.find_elements(
            By.TAG_NAME, "a")[2].get_attribute("href")
        insert_data = f'''INSERT OR IGNORE INTO {genre_list[1].translate(STR_TABLE)} (artist_ID, artist_name, artist_url) VALUES (?, ?, ?)'''

        c.execute(insert_data, [i, artist_name, artist_url])
        conn.commit()
        print(artist_name)
    # time.sleep(60)


def create_genre_table(genre_list):

    create_table = f'''CREATE TABLE IF NOT EXISTS {genre_list[1].translate(STR_TABLE)} (artist_ID INTEGER PRIMARY KEY,artist_name TEXT,artist_url TEXT)'''
    c.execute(create_table)


def create_urls_table(genre_list):
    create_table = f'''CREATE TABLE IF NOT EXISTS {genre_list[1].translate(STR_TABLE)}_songs ("artist_ID" INTEGER,"artist_name" TEXT,"song_name" TEXT,"song_url" TEXT, FOREIGN KEY("artist_ID") REFERENCES {genre_list[1].translate(STR_TABLE)}("artist_ID"))'''
    c.execute(create_table)


if __name__ == '__main__':
    genres = retrieve_from_genres()

    for genre in genres:
        # create_genre_table(genre)
        print(genre)
        # DRIVER.execute_script(f"window.open('{genre[2]}');")
        # add_artists_bands(genre)
        # create_urls_table(genre)

        # pprint(genre)
    c.close()
    conn.close()
