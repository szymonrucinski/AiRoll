import os
import firebase_admin
import operator
import time
from urllib.request import urlretrieve
from get_project_root import root_path
# from fastai.vision.all import *
from firebase_admin import credentials
from firebase_admin import firestore
import requests
from pathlib import Path
import matplotlib.pyplot as plt
from typing import Optional
import typer

app = typer.Typer()


BASE_DIR = os.path.join(os.path.dirname(__file__))
KEY_NAME = os.path.basename("key.json")
KEY_DIR = os.path.join(BASE_DIR, KEY_NAME)

CRED = credentials.Certificate(KEY_DIR)
firebase_admin.initialize_app(CRED)
DB = firestore.client()


def writing_to_db(movie_name, frame_name, frame_url):
    list_ref = DB.collection('0A_LIST_OF_MOVIES').document(movie_name)
    list_ref.set({'wasTested': 0, 'isBeingReviewed':False})

    doc_ref = DB.collection(movie_name).document(frame_name)
    doc_ref.set({
        u'frameUrl': frame_url,
        u'extremeLongShot': 0,
        u'longshot': 0,
        u'fullshot':0,
        u'mediumShot': 0,
        u'mediumCloseUp': 0,
        u'closeUp': 0,
        u'detail': 0,
        u'ambiguous':0
    })

def updating_db():
    doc_ref = DB.collection(u'test').document(u'alovelace')
    doc_ref.update({
        u'first': u'Adrianna',
    })

def removing_from_db():
    doc_ref = DB.collection(u'test').document(u'alovelace')
    doc_ref.update({
        u'first': firestore.DELETE_FIELD,
    })

def get_names_of_all_collection_in_db():
    doc_ref = DB.collection('0A_LIST_OF_MOVIES')
    doc = doc_ref.get()
    all_movie_titles_in_db = []
    for movie_title in doc:
        all_movie_titles_in_db.append(movie_title.id)
    return all_movie_titles_in_db

def get_names_of_reviewed_movies():
    doc_ref = DB.collection('0A_LIST_OF_MOVIES').where(u'wasTested',u'==',1).stream()
    all_movie_titles_in_db = []
    for movie_title in doc_ref:
        all_movie_titles_in_db.append(movie_title.id)
    print(all_movie_titles_in_db)
    return all_movie_titles_in_db

def writing_a_title_to_movie_list(movie_name, frame_name, frame_url):
    list_ref = DB.collection(u'0A_LIST_OF_MOVIES').document(u'titles')
    list_ref.set({f'{movie_name}': 0,'isBeingReviewed':False,'wasTested': 0})
    doc_ref = DB.collection(movie_name).document(frame_name)
    doc_ref.set({
        u'frameUrl': frame_url,
        u'extremeLongShot': 0,
        u'longshot': 0,
        u'fullshot':0,
        u'mediumShot': 0,
        u'closeUp': 0,
        u'detail': 0,
    })

def set_all_to_is_beingReviewed_to_false():
    all_titles = get_names_of_all_collection_in_db()
    for title in all_titles:
         doc_ref = DB.collection(u'0A_LIST_OF_MOVIES').document(title)
         doc_ref.update({
        u'isBeingReviewed': False,
    })

# set_all_to_is_beingReviewed_to_false()

def delete_documents_in_collection(coll_name):
    batch_size = 100
    coll_ref = DB.collection(coll_name)
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f'Deleting doc {doc.id} => {doc.to_dict()}')
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_documents_in_collection(coll_ref)


def REMOVE_ALL_MOVIES():
    all_titles = get_names_of_all_collection_in_db()
    for title in all_titles:
        delete_documents_in_collection(title)
    print("ALL ELEMENTS REMOVED")


def movie_already_in_db(movie_name):
    titles_arr = get_names_of_all_collection_in_db()
    return titles_arr.__contains__(movie_name)

def get_digits_from(test_dict):
    res = [] 
    val =[]
    for a in test_dict.items(): 
        x = isinstance(a[1],int)
        if x: 
            res.append(a[0])
            val.append(a[1])
    max_index = val.index((max(val)))
    return res[max_index]


def get_all_photos():
    shots = {}
    titles = get_names_of_reviewed_movies()
    for title in titles:
        docs = DB.collection(title).stream()
        for photo in docs:
            dic = photo.to_dict()
            proper_shot = get_digits_from(dic)
            shots[str(photo.id)] = [proper_shot, dic['frameUrl']]
    return shots

def download_photos():
    frames = get_all_photos()
    if len(frames) == 0:
        print('No Frames were classified')
        return False
    
    for frame in frames.items():
        file_path = os.path.join(Path(__file__).parent.parent,'data','images',f'{frame[1][0]}')
        print(file_path)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_path = os.path.join(file_path,frame[0])
        urlretrieve(frame[1][1],file_path)
    print("Done")
    return True