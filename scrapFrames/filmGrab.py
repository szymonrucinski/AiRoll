import time
import os
import sys
import numpy as np
import requests
from selenium import webdriver
from conf import IMAGES_LIMIT, OPTIONS, BASE_DIR, DATASET_DIR, BROWSER

OPTIONS.add_experimental_option("excludeSwitches", ["enable-logging"])


def clear():

    if os.name == 'nt':
        _ = os.system('cls')

    else:
        _ = os.system('clear')


def count_files(HOME_FOLDER):
    noOfFiles = 0
    noOfDir = 0

    for base, dirs, files in os.walk(HOME_FOLDER):
        for directories in dirs:
            noOfDir += 1
        for Files in files:
            noOfFiles += 1

    print('Number of files', noOfFiles)
    print('Number of Directories', noOfDir)
    print('Total:', (noOfDir + noOfFiles))
    print("================================")
    return noOfFiles


def get_movie_name_from_url(movie_link):
    folder_name = movie_link[33:]
    folder_name = folder_name.replace('/', '')
    return folder_name


def go_to_movie_page(movie_link):
    BROWSER.get(movie_link)
    all_images = BROWSER.find_elements_by_class_name("bwg-a")
    images_links = [elem.get_attribute('href') for elem in all_images]
    mkdir_and_save(images_links, movie_link)


def save_links_to_file(links):
    print("Saving")
    Array = np.array(links)
    np.savetxt(os.path.join(BASE_DIR, "links.txt"), np.array(Array), fmt="%s")


def mkdir_and_save(images_links, movie_link):
    folder_name = get_movie_name_from_url(movie_link)
    img_dir = os.path.join(BASE_DIR, f"dataset/{folder_name}")
    if count_files(DATASET_DIR) >= IMAGES_LIMIT:
        download_completed()

    if not os.path.exists(img_dir):
        os.makedirs(img_dir, exist_ok=True)
        for i, link in enumerate(images_links):
            filename = os.path.basename(f"{folder_name}-{i}.png")
            print(f"Downloading -> {filename}")
            file_path = os.path.join(img_dir, filename)
            with requests.get(link, stream=True) as r:
                try:
                    r.raise_for_status()
                except BaseException:
                    continue
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content():
                        if chunk:
                            f.write(chunk)
    clear()


def download_completed():
    print("FINISHED OBTAINING DATA")
    sys.exit()


def main():
    main_page = 'https://film-grab.com/movies-a-z/'
    BROWSER.get(main_page)

    movie_titles = BROWSER.find_elements_by_class_name("title")
    links = [elem.get_attribute('href') for elem in movie_titles]
    filtered_links = []
    for link in links:
        folder_name = get_movie_name_from_url(link)
        movie_folder = os.path.join(BASE_DIR, f"dataset/{folder_name}")
        if not os.path.exists(movie_folder):
            filtered_links.append(link)

    save_links_to_file(links)

    for movie_link in filtered_links:
        go_to_movie_page(movie_link)
        time.sleep(10)


main()
