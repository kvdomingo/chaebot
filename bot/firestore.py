from firebase_admin import firestore_async, initialize_app

initialize_app()


def get_firestore_client():
    return firestore_async.client()
