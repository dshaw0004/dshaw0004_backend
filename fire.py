import os

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("fire.json")
app1 = firebase_admin.initialize_app(cred)

app1 = firebase_admin.initialize_app(
    credentials.Certificate("pyapps_config.json"))
