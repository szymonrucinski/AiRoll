import time
import os
import sys
import numpy as np
import requests
import itertools
from PIL import Image
from selenium import webdriver
from conf import IMAGES_LIMIT, BASE_DIR, DATASET_DIR
from urllib.parse import unquote 
from selenium import webdriver
OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(
options=OPTIONS, executable_path=r'C:\chromedriver\chromedriver.exe')   

def search(query, N):
    # For one word queries it will be ok, for complex ones should encode first
    
    # driver.get(f'https://duckduckgo.com/?q={query}&t=h_&iax=images&ia=images&iaf=size%3ALarge')
    driver.get(f'https://duckduckgo.com/?q={query}&t=h_&iax=images&ia=images') 

    for _ in itertools.repeat(None, N):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")



    # For now it's working with this class, not sure if it will never change
    img_tags = driver.find_elements_by_class_name('tile--img__img') 

    for tag in img_tags:
        src = tag.get_attribute('data-src')
        src = unquote(src)
        src = src.split('=', maxsplit=1)
        src = src[1]
        yield src

    driver.close()

if __name__ == '__main__':
    from pprint import pprint
    imgs_urls = list(search("portrait",10))
    print(imgs_urls)
    print(len(imgs_urls))
