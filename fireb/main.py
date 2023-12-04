import os

import firebase_admin
from firebase_admin import cert, credentials

cred = credentials.RefreshToken("/etc/secrets/fire.json")
app = firebase_admin.initialize_app(cred)
