import pytest
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


def test_writing_to_db():
    doc_ref = DB.collection(u'test').document(u'alovelace')
    doc_ref.set({
        u'first': u'Ada',
        u'last': u'Lovelace',
        u'born': 1815
    })
    doc = doc_ref.get()

    assert doc.exists == True


def test_updating_db():
    doc_ref = DB.collection(u'test').document(u'alovelace')
    doc_ref.update({
        u'first': u'Adrianna',
    })
    doc = doc_ref.get()
    result_dict = doc.to_dict()

    assert result_dict.get('first') == 'Adrianna'


def test_removing_from_db():
    doc_ref = DB.collection(u'test').document(u'alovelace')
    doc_ref.update({
        u'first': firestore.DELETE_FIELD,
    })
    doc = doc_ref.get()
    result_dict = doc.to_dict()

    assert result_dict.get('first') == None


def test_get_names_of_all_collection_in_db():
    doc_ref = DB.collection('0A_LIST_OF_MOVIES')
    doc = doc_ref.get()
    all_movie_titles_in_db = []
    for movie_title in doc:
        all_movie_titles_in_db.append(movie_title.id)

    assert all_movie_titles_in_db != []
