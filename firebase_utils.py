import firebase_admin
from firebase_admin import credentials, firestore, storage

def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_creds.json")
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'fir-creds-e50d2'
        })

def get_db():
    init_firebase()
    return firestore.client()

def get_bucket():
    init_firebase()
    return storage.bucket()

def save_user_info(user_id, info):
    db = get_db()
    # Use merge=True so only provided fields are updated, not all fields overwritten
    db.collection("users").document(user_id).set(info, merge=True)

def save_truth(user_id, question, answer):
    db = get_db()
    truth_entry = {
        "question": question,
        "answer": answer,
        "timestamp": firestore.SERVER_TIMESTAMP
    }
    db.collection("users").document(user_id).collection("truths").add(truth_entry)

def save_dare(user_id, challenge, response):
    db = get_db()
    dare_entry = {
        "challenge": challenge,
        "response": response,
        "timestamp": firestore.SERVER_TIMESTAMP
    }
    db.collection("users").document(user_id).collection("dares").add(dare_entry)

def upload_file(file_bytes, file_name):
    bucket = get_bucket()
    blob = bucket.blob(file_name)
    blob.upload_from_string(file_bytes)
    return blob.public_url