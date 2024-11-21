import os

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("firekey.json")
app = firebase_admin.initialize_app(cred, name="appbank")
