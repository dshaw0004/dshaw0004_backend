from random import randint

from firebase_admin import firestore

from fire import app3
from dataclasses import dataclass
db = firestore.client(app3)


def get_all_app_info():
    '''
    out typing
    {"name": str, 'description': str, 'appLink': str, 'platform': str, 'thumbnail': str, "version": float}
    '''
    ref = db.collection("allInfo")
    docs = ref.stream()
    all_messages = []
    for doc in docs:
 #       print(f"{doc.id} => {doc.to_dict()}")
        data = doc.to_dict()
        all_messages.append(data)
#    print(all_messages)
    return all_messages


def add_new_app(app_info):
    ''' app_info must contain these  
    {"name": str, 'description': str, 'appLink': str, 'platform': str, 'thumbnail': str, "version": float}'''

    document_id = app_info['name'].replace(" ", '') + str(app_info['version'])

    doc_ref = db.collection("allInfo").document(f"{document_id}")
    doc_ref.set(app_info)


def get_all_suggestions():
    ref = db.collection("suggestions")
    docs = ref.stream()
    all_messages = []
    for doc in docs:
        #        print(f"{doc.id} => {doc.to_dict()}")
        all_messages.append(doc.to_dict())
#    print(all_messages)
    return all_messages


def add_new_suggestion(name: str, description: str, senderContact: str):

    no_of_message = randint(1, 99999) * randint(5, 77635)
    doc_ref = db.collection("suggestions").document(f"devp{no_of_message}")
    doc_ref.set({"name": name, "description": description,
                "senderContact": senderContact})
