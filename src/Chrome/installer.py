"""Installer has many purposes. it can install and handle WebDriver"""
import __init__
from src.lib import MIDI_DATA_DIR
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import selenium.webdriver.chrome.options as selenium_options


def install_driver(headless=False, download_mode=False):
    """recommended: install WebDriver into a global variable"""
    OPTIONS = Options()
    if headless:
        OPTIONS.add_argument('--headless')
        OPTIONS.add_argument('--disable-gpu')
    OPTIONS.add_argument(
        "--user-data-dir=./src/Chrome/preferences")

    if download_mode:
        OPTIONS.add_experimental_option('prefs', {
            'download.default_directory': MIDI_DATA_DIR,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True
        })

    OPTIONS.page_load_strategy = 'normal'
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=OPTIONS)
