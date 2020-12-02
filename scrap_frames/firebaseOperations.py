import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

BASE_DIR = os.path.join(os.path.dirname(__file__), '.')
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
        u'closeUp': 0,
        u'detail': 0,
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

set_all_to_is_beingReviewed_to_false()

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
