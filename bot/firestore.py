import json
import os

from django.conf import settings
from firebase_admin import credentials, firestore_async, initialize_app

if (adc := os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")) is None:
    creds = credentials.Certificate(str(settings.BASE_DIR / "gcp_sa_key.json"))
else:
    creds = credentials.Certificate(json.loads(adc))


initialize_app(creds)


def get_firestore_client():
    return firestore_async.client()
