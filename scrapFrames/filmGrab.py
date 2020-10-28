import time
import os
import sys
import numpy as np
import requests
from PIL import Image
from selenium import webdriver
from conf import IMAGES_LIMIT, BASE_DIR, DATASET_DIR
from firebaseOperations import writing_to_db, movie_already_in_db, get_names_of_all_collection_in_db


OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_experimental_option("excludeSwitches", ["enable-logging"])
BROWSER = webdriver.Chrome(
    options=OPTIONS, executable_path=r'C:\chromedriver\chromedriver.exe')
ALL_ROOT_LINKS = []
ALL_PHOTOS = []


def clear_cli():

    if os.name == 'nt':
        _ = os.system('cls')

    else:
        _ = os.system('clear')


def count_movies_in_db():
    number_of_movies_in_db = len(get_names_of_all_collection_in_db())
    print("==============================================================")
    print('Number of all movies: ', number_of_movies_in_db, ' φ(゜▽゜*)♪')
    print("===============================================================")
    return number_of_movies_in_db


def get_movie_name_from_url(movie_link):
    folder_name = movie_link[33:]
    folder_name = folder_name.replace('/', '')
    return folder_name


def go_to_movie_page(movie_link):
    BROWSER.get(movie_link)
    all_images = BROWSER.find_elements_by_class_name("bwg-a")
    images_links = [elem.get_attribute('href') for elem in all_images]
    mkdir_and_save(images_links, movie_link)


def save_links_to_file(links, fileName):
    print("Saving")
    Array = np.array(links)
    np.savetxt(os.path.join(BASE_DIR, f"{fileName}"), np.array(Array), fmt="%s")


def save_images_on_my_pc(folder_name, img_dir, images_links):
    if not os.path.exists(folder_name, img_dir):
        os.makedirs(img_dir, exist_ok=True)
        for i, link in enumerate(images_links):
            filename = os.path.basename(f"{folder_name}-{i}.png")
            print(f"Downloading -> {filename}")
            file_path = os.path.join(img_dir, filename)
            with requests.get(link, stream=True) as resp:
                try:
                    resp.raise_for_status()
                except BaseException:
                    continue
                with open(file_path, 'wb') as f:
                    for chunk in resp.iter_content():
                        if chunk:
                            f.write(chunk)


def mkdir_and_save(images_links, movie_link):
    folder_name = get_movie_name_from_url(movie_link)
    if count_movies_in_db() >= IMAGES_LIMIT:
        download_completed()
    print(f"Adding {folder_name} to database ╰(*°▽°*)╯.")
    for i, link in enumerate(images_links):
        file_name = os.path.basename(f"{folder_name}-{i}.png")
        writing_to_db(folder_name, file_name, link)
    clear_cli()


def download_completed():
    print("FINISHED OBTAINING DATA")
    sys.exit()


def main():
    main_page = 'https://film-grab.com/movies-a-z/'
    BROWSER.get(main_page)

    print("Starting the super-complicated process (❁´◡`❁)")
    movie_titles = BROWSER.find_elements_by_class_name("title")
    links = [elem.get_attribute('href') for elem in movie_titles]

    titles_dict = get_names_of_all_collection_in_db()
    filtered_links = []

    for link in links:
        folder_name = get_movie_name_from_url(link)
        if not titles_dict.__contains__(folder_name):
            filtered_links.append(link)

    for movie_link in filtered_links:
        go_to_movie_page(movie_link)
        time.sleep(5)


main()
