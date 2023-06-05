import __init__
import requests
from lib.db_ops import GetData
from lib import MIDI_DATA_DIR
from Chrome.installer import install_driver, By, ActionChains, Keys
import time
import shutil
import os
from tqdm import tqdm


def file_organizer(artist_name: str, song_name: str, genre: str):

    current_directory = os.getcwd()  # Get the current working directory
    # file_name = "example.mid"
    subdirectory = genre

    files = os.listdir(MIDI_DATA_DIR)
    new_file_name = f"{artist_name}_{song_name}.mid"

# Sort the files by modification time (most recent first)
    files.sort(key=lambda x: os.path.getmtime(
        os.path.join(MIDI_DATA_DIR, x)), reverse=True)

# Get the name of the last file created
    last_file = files[0]

    source_path = os.path.join(MIDI_DATA_DIR, last_file)
    destination_path = os.path.join(MIDI_DATA_DIR, subdirectory, last_file)

    subdirectory_path = os.path.join(MIDI_DATA_DIR, subdirectory)
    if not os.path.exists(subdirectory_path):
        os.makedirs(subdirectory_path)

    shutil.move(source_path, destination_path)
    new_destination_path = os.path.join(
        MIDI_DATA_DIR, subdirectory, new_file_name)
    os.rename(destination_path, new_destination_path)


def dir_cleanup():
    print("dir")


def download_all():
    all_midi = GetData(db="AllMIDI", table_name="dl_urls")
    all_midi_urls_list = all_midi.get_all()

    # loop through each url and download.
    for i, artist_i, artist_name, song_name, page_url, download_url, genre in tqdm(all_midi_urls_list, desc="Downloading all midi:"):
        if i > 13353:  # start from here   | 15265
            DRIVER.get(page_url)
            time.sleep(1)
            button = DRIVER.find_element(
                By.XPATH, '/html/body/div[2]/div[8]/div[1]/div/div[1]/div[3]/a[1]')
            button.click()  # start download
            time.sleep(1)
            file_organizer(artist_name, song_name, genre)


if __name__ == '__main__':
    DRIVER = install_driver( download_mode=True)

    download_all()

    # dir_cleanup()
