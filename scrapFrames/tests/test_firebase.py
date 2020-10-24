import pytest
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

CRED = credentials.Certificate('D:\Programowanie\AI\scrapFrames\key.json')
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