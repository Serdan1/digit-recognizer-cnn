# tests/test_predictor.py
import unittest
import numpy as np
from src.predictor import DigitPredictor

class TestDigitPredictor(unittest.TestCase):
    def setUp(self):
        self.predictor = DigitPredictor("model.h5")
        self.predictor.load_model()

    def test_predict_shape_and_output(self):
        # Imagen sintética de 28x28 con ceros
        dummy_image = np.zeros((1, 28, 28, 1), dtype='float32')
        prediction = self.predictor.predict(dummy_image)
        self.assertIsInstance(prediction, int)
        self.assertTrue(0 <= prediction <= 9, "La predicción debe estar entre 0 y 9")

    def test_predict_raises_if_not_loaded(self):
        p = DigitPredictor("model.h5")
        dummy_image = np.zeros((1, 28, 28, 1), dtype='float32')
        with self.assertRaises(ValueError):
            p.predict(dummy_image)

if __name__ == '__main__':
    unittest.main()
