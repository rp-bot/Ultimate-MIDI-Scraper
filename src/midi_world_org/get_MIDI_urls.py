from Chrome.installer import install_driver, By, ActionChains, Keys
import time
import sqlite3
from pprint import pprint
import threading
import re
from tqdm import tqdm

ARTIST_NAME_PATTERN = r'\((.*?)\)'
SONG_TITLE_PATTERN = r'(.*?)\s+\('


def get_genres():
    select_genres = '''SELECT * FROM genres'''
    freeMIDI_db_cursor.execute(select_genres)
    rows = freeMIDI_db_cursor.fetchall()
    return rows


def add_page_urls(data: list):
    insert_command = f'''INSERT OR IGNORE INTO page_urls (genre_name, page_number, page_urls) VALUES (?, ?, ?)'''
    freeMIDI_db_cursor.executemany(insert_command, data)
    freeMIDI_db_conn.commit()


def add_ALL_MIDI(dl_links: list):
    insert_command = f'''INSERT OR IGNORE INTO dl_urls (artist_id, artist_name, song_name, song_url, download_url, genre) VALUES (?, ?, ?, ?, ?, ?)'''
    all_MIDI_db_cursor.executemany(insert_command, dl_links)
    all_MIDI_db_conn.commit()


def get_urls_in_genres(genres: list):
    for genre in genres[15:]:
        select_command = f"""SELECT * FROM page_urls WHERE genre_name = '{genre[1]}'"""
        freeMIDI_db_cursor.execute(select_command)
        rows = freeMIDI_db_cursor.fetchall()

        for i, row in enumerate(rows):
            DRIVER.get(row[-1])
            DRIVER.refresh()
            # DRIVER.implicitly_wait(5)
            time.sleep(2)
            ul = DRIVER.find_element(
                By.XPATH, '/html/body/div[1]/div[3]/div[1]/ul[1]')
            li_s = ul.find_elements(By.TAG_NAME, "li")
            midi_download_links = []
            for li in tqdm(li_s, desc=f"songs downloaded in page {i+1} of {row[1]}: ", leave=True):
                link = li.find_element(By.TAG_NAME, "a").get_attribute("href")
                try:
                    artist_name = re.findall(ARTIST_NAME_PATTERN, li.text)[0]
                except IndexError:
                    artist_name = None
                try:
                    song_title = re.findall(SONG_TITLE_PATTERN, li.text)[0]
                except IndexError:
                    song_title = None
                    continue
                midi_download_links.append(
                    (None, artist_name, song_title, row[-1], link, genre[1]))
            add_ALL_MIDI(midi_download_links)


if __name__ == '__main__':
    DRIVER = install_driver()
    #
    freeMIDI_db_conn = sqlite3.connect('data/db/midiworld_com.sqlite3')
    freeMIDI_db_cursor = freeMIDI_db_conn.cursor()

    all_MIDI_db_conn = sqlite3.connect('data/db/ALLMIDI.sqlite3')
    all_MIDI_db_cursor = all_MIDI_db_conn.cursor()
    #

    genres_list = get_genres()
    # get_urls_in_genres(genres_list)
    get_urls_in_genres(genres_list)

    #
    freeMIDI_db_cursor.close()
    freeMIDI_db_conn.close()
