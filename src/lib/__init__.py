"""The lib module has a library of details or config functions, variables and classes to make the workflow dynamic"""
# init file for folder level 2,
import os
import sys
currentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# STR table
STR_TABLE = str.maketrans({"-": "_", " ": "_"})

# Path to MIDI data directory
path_to_MIDIdata = ['data', 'MIDIdata']
MIDI_DATA_DIR = os.path.join(os.path.abspath(''), *path_to_MIDIdata)