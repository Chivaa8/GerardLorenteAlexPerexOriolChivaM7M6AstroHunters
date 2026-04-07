import os
import firebase_admin
from firebase_admin import credentials, firestore

# Path to Firebase credentials
FIREBASE_JSON_PATH = "./astrogoa-897be-firebase-adminsdk-fbsvc-1e00e19622.json"

# Try to get from environment variable, fallback to local path
FIREBASE_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", FIREBASE_JSON_PATH)

def initialize_firebase():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
            print(f"Firebase initialized with: {FIREBASE_CREDENTIALS_PATH}")
    except Exception as e:
        print(f"Firebase error: {str(e)}")
        raise

def get_firestore_client():
    try:
        initialize_firebase()
        db = firestore.client()
        return db
    except Exception as e:
        print(f"Firestore error: {str(e)}")
        raise

# Initialize on module import
db = get_firestore_client()
