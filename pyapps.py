from random import randint

from firebase_admin import firestore

from fire import app2

db = firestore.client(app2)


def get_all_app_info():
    ref = db.collection("appInfo")
    docs = ref.stream()
    all_messages = []
    for doc in docs:
        #        print(f"{doc.id} => {doc.to_dict()}")
        all_messages.append(doc.to_dict())
#    print(all_messages)
    return all_messages


def add_new_app(name: str, description: str, appURL: str):

    no_of_message = randint(1, 99999) * randint(5, 77635)
    doc_ref = db.collection("allInfo").document(f"devp{no_of_message}")
    doc_ref.set({"name": name, "description": description,
                "appURL": appURL})


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
