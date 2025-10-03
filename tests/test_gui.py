# tests/test_gui.py
import unittest
from unittest.mock import patch
from src.gui import DigitRecognizerGUI

class TestGUI(unittest.TestCase):

    @patch('src.gui.DigitPredictor')
    @patch('src.gui.FirebaseUploader')
    def test_gui_initialization(self, mock_uploader, mock_predictor):
        gui = DigitRecognizerGUI(
            model_path="model.h5",
            firebase_cred="fake.json",
            firebase_bucket="fake-bucket"
        )
        self.assertIsNotNone(gui)

if __name__ == '__main__':
    unittest.main()
