import time
import os
import sys
import numpy as np
import requests
import glob

shot_type = ['extreme_wide_shot', 'full_shot', 'medium_shot','close_up_shot']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def save_images_on_my_pc(folder_dir, images_links,filename):
    print('downloading')
    for i, link in enumerate(images_links):
        file_name = f"{filename}-{i}.jpg"
        file_path = os.path.join(folder_dir, file_name)
        print(f"Downloading -> {file_name}")
        with requests.get(link, stream=True) as resp:
            try:
                resp.raise_for_status()
            except BaseException:
                continue
            with open(file_path, 'wb') as f: 
                for chunk in resp.iter_content():
                    if chunk:
                        f.write(chunk)

def start():
    text_files = glob.glob(BASE_DIR + "/**/fs.txt", recursive = True)
    for file in text_files:
        file_name = os.path.basename(file)
        f = open(file, 'r+')
        links = f.read().splitlines()
        f.close()
        folder_path = os.path.dirname(file)
        file_name = os.path.basename(file)
        file_name = file_name.replace('.txt','')
        folder_path = os.path.join(folder_path,'full_shot')
        print(file_name)
        save_images_on_my_pc(folder_path, links, file_name)

start()