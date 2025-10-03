# tests/test_image_processor.py
import unittest
import numpy as np
from PIL import Image
import os
from src.image_processor import load_and_preprocess_image

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        # Crear imagen temporal 100x100 en escala de grises
        self.temp_image_path = "temp_test_image.jpg"
        img = Image.new('L', (100, 100), color=128)  # gris medio
        img.save(self.temp_image_path)

    def tearDown(self):
        # Eliminar imagen temporal
        if os.path.exists(self.temp_image_path):
            os.remove(self.temp_image_path)

    def test_load_and_preprocess_image(self):
        arr = load_and_preprocess_image(self.temp_image_path)
        self.assertEqual(arr.shape, (1, 28, 28, 1), "La forma de la imagen procesada debe ser (1, 28, 28, 1)")
        self.assertTrue(np.all(arr >= 0.0) and np.all(arr <= 1.0), "Los valores deben estar normalizados entre 0 y 1")

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            load_and_preprocess_image("no_existe.jpg")

if __name__ == '__main__':
    unittest.main()
