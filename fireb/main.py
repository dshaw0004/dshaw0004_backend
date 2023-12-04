import firebase_admin
from firebase_admin import credentials

import os


cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "dshaw-0004",
  "private_key_id": os.getenv("private_key_id"),
  "private_key": os.getenv("private_key"),
  "client_email": "firebase-adminsdk-r7ru2@dshaw-0004.iam.gserviceaccount.com",
  "client_id": "108663384489570320244",
  "auth_uri": os.getenv("auth_uri"),
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-r7ru2%40dshaw-0004.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
)
app = firebase_admin.initialize_app(cred)



