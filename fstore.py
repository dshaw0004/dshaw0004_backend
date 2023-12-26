from random import randint

from firebase_admin import firestore

from fire import app1

db = firestore.client(app1)


def get_all_message():
    ref = db.collection("messages")
    docs = ref.stream()
    all_messages = []
    for doc in docs:
        #        print(f"{doc.id} => {doc.to_dict()}")
        all_messages.append(doc.to_dict())
#    print(all_messages)
    return all_messages


def add_new_message(message: str, senderName: str, senderContact: str):

    no_of_message = randint(1, 99999) * randint(5, 77635)
    doc_ref = db.collection("messages").document(f"devp{no_of_message}")
    doc_ref.set({"message": message, "senderName": senderName,
                "senderContact": senderContact})
