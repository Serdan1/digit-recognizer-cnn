# src/firebase_utils.py
import firebase_admin
from firebase_admin import credentials, storage
import os
from datetime import datetime

class FirebaseUploader:
    def __init__(self, cred_path: str, bucket_name: str):
        self.cred_path = cred_path
        self.bucket_name = bucket_name
        self._initialize_firebase()

    def _initialize_firebase(self):
        """Inicializa la app de Firebase si no está inicializada todavía."""
        if not firebase_admin._apps:
            print(f"🔐 Inicializando Firebase con credenciales: {self.cred_path}")
            cred = credentials.Certificate(self.cred_path)
            firebase_admin.initialize_app(cred, {
                'storageBucket': self.bucket_name
            })
        self.bucket = storage.bucket()

    def upload_image(self, file_path: str) -> str:
        """
        Sube una imagen a Firebase Storage y devuelve la URL pública.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

        filename = os.path.basename(file_path)
        # Nombre único para evitar colisiones
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        blob_name = f"uploads/{timestamp}_{filename}"
        blob = self.bucket.blob(blob_name)

        print(f"☁️ Subiendo {file_path} como {blob_name}...")
        blob.upload_from_filename(file_path)
        blob.make_public()
        print(f"✅ Imagen subida con éxito. URL: {blob.public_url}")

        return blob.public_url
