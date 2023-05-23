"""Chrome is a module that handles all logic related to the selenium chromedriver."""
# init file for folder level 2,
import os
import sys
currentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)