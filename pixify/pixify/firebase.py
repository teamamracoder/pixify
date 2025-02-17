import firebase_admin
from firebase_admin import credentials

# Path to your Firebase service account file
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)
