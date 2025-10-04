# src/firebase_utils.py
import firebase_admin
from firebase_admin import credentials, storage
import os
from datetime import datetime

class FirebaseUploader:
    def __init__(self, cred_path: str, bucket_name: str):
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {"storageBucket": bucket_name})
        self.bucket = storage.bucket()

    def upload_image(self, file_path: str, destination_path: str = None) -> str:
        """Sube una imagen a Firebase Storage y devuelve su URL pública."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No se encontró la imagen: {file_path}")

        if destination_path is None:
            filename = os.path.basename(file_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            destination_path = f"uploads/{timestamp}_{filename}"

        blob = self.bucket.blob(destination_path)
        blob.upload_from_filename(file_path)
        blob.make_public()

        print(f"🌐 URL Firebase: {blob.public_url}")
        return blob.public_url
