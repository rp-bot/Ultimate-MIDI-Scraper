from Chrome.installer import install_driver, By, ActionChains, Keys
from pprint import pprint
import time
import sqlite3
from tqdm import tqdm


conn = sqlite3.connect('data/db/UltimateMidi.sqlite3')
c = conn.cursor()

STR_TABLE = str.maketrans({"-": "_", " ": "_"})


def create_genre_queries():
    select_genres = '''SELECT * FROM genres'''
    c.execute(select_genres)
    rows = c.fetchall()

    select_artists_commands = []
    for genre in rows:
        select_artists_commands.append(
            (genre[1], f'''SELECT * FROM {genre[1].translate(STR_TABLE)}'''))

    return select_artists_commands


def get_artists(genre_queries):
    artists = {}
    for genre, query in genre_queries:
        c.execute(query)
        rows = c.fetchall()
        artists.update({genre: rows})
    return artists


def find_urls(elem: list):
    urls = []
    song_names = []
    for each in elem:
        for each_a_tag in each.find_elements(By.TAG_NAME, "a"):
            song_names.append(each_a_tag.text)
            urls.append(each_a_tag.get_attribute("href"))
    return song_names, urls


def make_data(song_names: list, song_urls: list, artist: list, div):
    structured_data = []
    for song_name, song_url in zip(song_names, song_urls):
        structured_data.append((artist[0], artist[1], song_name, song_url))
    return structured_data


def download_songs(artists_dict: dict):
    from_7 = artists_dict.items()
    print(type(from_7))
    for i, genre in tqdm(enumerate(artists_dict.items()), desc="genres: "):
        # loop through each genre
        if i < 6:
            continue
        else:
            for artist in tqdm(genre[1], desc=f"artists in {genre[0]}", leave=False):
                DRIVER.get(artist[2])
                url_divs = DRIVER.find_elements(
                    By.CLASS_NAME, "artist-song-cell")
                song_names, song_urls = find_urls(url_divs)
                insert_data = f'''INSERT OR IGNORE INTO {genre[0].translate(STR_TABLE)}_songs (artist_ID, artist_name, song_name, song_url) VALUES (?, ?, ?, ?)'''

                data = make_data(song_names, song_urls, artist, url_divs)
                # DRIVER.quit()
                c.executemany(insert_data, data)
                conn.commit()


if __name__ == '__main__':
    DRIVER = install_driver()
    genre_queries = create_genre_queries()
    artists = get_artists(genre_queries)
    download_songs(artists)
    pprint("done")
