from Chrome.installer import install_driver, By, ActionChains, Keys
import time
import sqlite3
from pprint import pprint

DRIVER = install_driver()

conn = sqlite3.connect('data/db/UltimateMidi.sqlite3')
c = conn.cursor()


def add_data(table_name, data):

    # create_table = f'''CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER PRIMARY KEY,genre TEXT,url TEXT)'''
    # c.execute(create_table)
    # conn.commit()

    insert_data = f'''INSERT OR IGNORE INTO {table_name} (genre, url)VALUES (?, ?)'''

    c.executemany(insert_data, data)

    conn.commit()


def get_genres():
    genres = []
    genre_tab = DRIVER.find_element(By.XPATH, '//*[@id="mainContent"]/div[7]')
    genre_list = genre_tab.find_elements(By.TAG_NAME, "a")

    time.sleep(1)

    for genre in genre_list:
        link = genre.get_attribute("href")
        genres.append((
            genre.text,
            link
        ))

    add_data("genres", genres)
    return genres


def get_other_categories():
    categories = []
    categ_tab = DRIVER.find_element(By.XPATH, '//*[@id="mainContent"]/div[9]')
    categ_list = categ_tab.find_elements(By.TAG_NAME, "a")

    time.sleep(1)

    for categ in categ_list:
        link = categ.get_attribute("href")
        categories.append((
            categ.text,
            link
        ))

    add_data("genres", categories)
    return categories


if __name__ == '__main__':
    DRIVER.get("https://freemidi.org/all")
    # x = get_genres()
    all_categories = get_other_categories()
    pprint(all_categories)
    add_data('genres', all_categories)
    c.close()
    conn.close()
