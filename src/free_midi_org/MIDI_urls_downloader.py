from Chrome.installer import install_driver, By, ActionChains, Keys, NoSuchElementException
import time
import sqlite3
from pprint import pprint
from songs_downloader import create_genre_queries
from tqdm import tqdm
from lib import STR_TABLE


def get_genres():
    select_genres = '''SELECT * FROM genres'''
    url_db_cursor.execute(select_genres)
    rows = url_db_cursor.fetchall()
    return rows


def get_all_urls(genres):
    urls_dict = {}
    for genre in genres:
        fetch_urls = f'''SELECT * FROM {genre[1].translate(STR_TABLE)}_songs'''
        try:
            url_db_cursor.execute(fetch_urls)
            urls_list = url_db_cursor.fetchall()
            urls_dict.update({genre[1].translate(STR_TABLE): urls_list})
        except sqlite3.OperationalError:
            continue

    return urls_dict


def add_dl_urls(data: list):
    push_command = f'''INSERT OR IGNORE INTO dl_urls (artist_ID, artist_name, song_name,song_url, download_url, genre) VALUES (?, ?, ?, ?, ?, ?)'''
    try:
        midi_db_cursor.execute(push_command, data)
        midi_db_conn.commit()
    except ValueError:
        pass


def get_dl_url(artist: tuple, genre: str):
    try:
        DRIVER.get(artist[3])
        download_link = DRIVER.find_element(
            By.ID, "downloadmidi").get_attribute("href")
        return artist+(download_link, genre,)
    except NoSuchElementException:
        pass


def download_MIDI(urls_dict: dict):
    # Create a queue to store the results

    for genre, artists in tqdm(urls_dict.items(), desc="Genres completed: "):
        if list(urls_dict.keys()).index(genre) > 5:
            for i, artist in tqdm(enumerate(artists), desc=f"Artists in {genre} completed: ", leave=False):
                data = get_dl_url(artist, genre)
                add_dl_urls(data)


if __name__ == '__main__':

    url_db_conn = sqlite3.connect('data/db/UltimateMidi.sqlite3')
    url_db_cursor = url_db_conn.cursor()

    midi_db_conn = sqlite3.connect('data/db/AllMIDI.sqlite3')
    midi_db_cursor = midi_db_conn.cursor()

    DRIVER = install_driver(headless=True)

    genres = get_genres()

    all_urls_dict = get_all_urls(genres)

    download_MIDI(all_urls_dict)

    url_db_cursor.close()
    url_db_conn.close()

    midi_db_cursor.close()
    midi_db_conn.close()
