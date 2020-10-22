import time
import os
import numpy as np
import requests
from selenium import webdriver

IMAGES_LIMIT = 5000
OPTIONS = webdriver.ChromeOptions()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
OPTIONS.add_experimental_option("excludeSwitches", ["enable-logging"])
BROWSER = webdriver.Chrome(
    options=OPTIONS, executable_path=r'C:\chromedriver\chromedriver.exe')
    