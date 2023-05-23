from Chrome.installer import install_driver, By, ActionChains, Keys
import time
import sqlite3
from pprint import pprint


def get_genres():
    DRIVER.get("https://www.midiworld.com/files/")
    genres_div = DRIVER.find_elements(By.CLASS_NAME, "w2")

    genre_names = list(map(lambda genre: genre.text, genres_div))

    genre_urls = list(
        map(lambda genre: genre.get_attribute("href"), genres_div))
    return list(zip(genre_names, genre_urls))


def add_genres(genres_data: list):
    insert_command = f'''INSERT OR IGNORE INTO genres (Genre, Genre_URL) VALUES (?, ?)'''
    freeMIDI_db_cursor.executemany(insert_command, genres_data)
    freeMIDI_db_conn.commit()


if __name__ == '__main__':
    #
    DRIVER = install_driver()
    freeMIDI_db_conn = sqlite3.connect('data/db/midiworld_com.sqlite3')
    freeMIDI_db_cursor = freeMIDI_db_conn.cursor()
    #

    genres_data = get_genres()
    add_genres(genres_data)

    #
    freeMIDI_db_cursor.close()
    freeMIDI_db_conn.close()
