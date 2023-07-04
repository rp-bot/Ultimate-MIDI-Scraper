import os
import numpy as np


def max_even_distribution(main_folder, percentile):
    # List all folders
    folders = [os.path.join(main_folder, f) for f in os.listdir(
        main_folder) if os.path.isdir(os.path.join(main_folder, f))]

    # Count the number of files in each folder
    file_counts = [len([f for f in os.listdir(folder) if os.path.isfile(
        os.path.join(folder, f))]) for folder in folders]
    print([os.path.basename(folder) for folder in folders], file_counts)
    # Calculate the specified percentile
    files_percentile = int(np.percentile(file_counts, percentile))

    print(
        f"The maximum number of files that can be evenly distributed, based on the {percentile}th percentile, is {files_percentile}")


midi_files_dir = os.path.join(os.getcwd(), "data", "MIDIdata")
max_even_distribution(midi_files_dir, 25)
