import firebase_admin
from firebase_admin import credentials, cert

import os


cred = credentials.Certificate(cert("/etc/secrets/fire.json"))
app = firebase_admin.initialize_app(cred)
