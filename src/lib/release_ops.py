from __init__ import *  # MIDI_DATA_DIR, RELEASES_DIR,TODAY
import os
import string
import re
import shutil
from tqdm import tqdm


def zipper(directory_path: str, destination_path: str, file_name: str, compression_format="zip"):

    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return

    try:
        # Zip the directory
        print("\nZipping...\n")
        shutil.make_archive(file_name, compression_format, directory_path)

        # Move the zipped file to the current working directory
        shutil.move(f"{file_name}.zip", destination_path)

        print(
            f"Directory successfully zipped: {file_name}.{compression_format}\n")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def sanitize_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized_filename = ''.join(c for c in filename if c in valid_chars)
    sanitized_filename = sanitized_filename.replace(' ', '_')
    return sanitized_filename


def rename_files_in_directory(directory_path):
    for filename in tqdm(os.listdir(directory_path)):
        if os.path.isfile(os.path.join(directory_path, filename)):
            new_filename = sanitize_filename(filename)
            if new_filename != filename:
                os.rename(os.path.join(directory_path, filename),
                          os.path.join(directory_path, new_filename))


if __name__ == '__main__':
    # rename_files_in_directory(os.path.join(MIDI_DATA_DIR, "country"))
    zipper(MIDI_DATA_DIR, RELEASES_DIR, f"{TODAY}_midi_files")
