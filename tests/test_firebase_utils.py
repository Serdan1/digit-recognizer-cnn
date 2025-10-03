# tests/test_firebase_utils.py
import unittest
from unittest.mock import patch, MagicMock
from src.firebase_utils import FirebaseUploader

class TestFirebaseUploader(unittest.TestCase):

    @patch('src.firebase_utils.firebase_admin.initialize_app')
    @patch('src.firebase_utils.credentials.Certificate')
    @patch('src.firebase_utils.storage.bucket')
    def test_upload_image(self, mock_bucket, mock_cert, mock_init):
        # Simulamos bucket y blob
        mock_blob = MagicMock()
        mock_blob.public_url = "https://fakeurl.com/image.jpg"
        mock_bucket.return_value.blob.return_value = mock_blob

        uploader = FirebaseUploader(
            cred_path='fake_path.json',
            bucket_name='proyecto-mnist-dashboard.firebasestorage.app'
        )

        # Creamos un archivo temporal de prueba
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(b"fake image data")
            tmp_path = tmp.name

        url = uploader.upload_image(tmp_path)
        self.assertEqual(url, "https://fakeurl.com/image.jpg")

if __name__ == '__main__':
    unittest.main()
