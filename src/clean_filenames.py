import os
import string
import sqlite3
from tqdm import tqdm


def sanitize_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized_filename = ''.join(c for c in filename if c in valid_chars)
    sanitized_filename = sanitized_filename.replace(' ', '_')
    return sanitized_filename


def rename_files(database, main_folder):
    # Connect to the database
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Iterate over genres
    cursor.execute('SELECT song_ID, artist_name, song_name FROM dl_urls')
    songs = {sanitize_filename(f'{artist_name}_{song_name}.mid')
                               : id for id, artist_name, song_name in cursor.fetchall()}

    # Recursively iterate over all files in the main folder
    for dirpath, dirnames, filenames in tqdm(os.walk(main_folder)):
        for filename in filenames:

            # Check if the file exists in the songs dictionary
            if filename in songs:
                song_id = songs[filename]

                # Rename the file
                old_path = os.path.join(dirpath, filename)
                new_filename = str(song_id) + '.mid'  # Include the extension
                new_path = os.path.join(dirpath, new_filename)
                try:
                    os.rename(old_path, new_path)
                except FileExistsError:
                    print(f"{old_path} already exists, continuing...")
                    continue

    # Close the connection
    conn.close()


midi_db = os.path.join(os.getcwd(), "data", "db", "AllMIDI.sqlite3")
midi_files_dir = os.path.join(os.getcwd(), "data", "MIDIdata")
rename_files(midi_db, midi_files_dir)
# print()
