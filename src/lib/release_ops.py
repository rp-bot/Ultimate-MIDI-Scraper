from __init__ import *  # MIDI_DATA_DIR, RELEASES_DIR,TODAY
import os
import shutil


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

        print(f"Directory successfully zipped: {file_name}.{compression_format}\n")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == '__main__':

    zipper(MIDI_DATA_DIR, RELEASES_DIR, f"{TODAY}_midi_files")
