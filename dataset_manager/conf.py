import time
import os
import requests
from selenium import webdriver

IMAGES_LIMIT = 5000
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__))
DATASET_DIR = os.path.join(
    BASE_DIR, "dataset")
ASSETS_DIR = os.path.join(
    BASE_DIR, "assets_filterFrame")
