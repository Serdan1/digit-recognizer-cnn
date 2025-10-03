# tests/test_predictor.py
import unittest
import tensorflow as tf
import numpy as np
from src.predictor import DigitPredictor
import os

class TestDigitPredictor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # ⚡ Generamos un modelo simple si no existe model.h5
        if not os.path.exists("model.h5"):
            print("⚡ Generando modelo de prueba para predictor...")
            model = tf.keras.Sequential([
                tf.keras.layers.Input(shape=(28, 28, 1)),
                tf.keras.layers.Conv2D(8, (3, 3), activation="relu"),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(10, activation="softmax")
            ])
            model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
            x = np.random.rand(100, 28, 28, 1).astype("float32")
            y = np.random.randint(0, 10, size=(100,))
            model.fit(x, y, epochs=1, verbose=0)
            model.save("model.h5")
            print("✅ Modelo de prueba guardado como model.h5")

    def setUp(self):
        self.predictor = DigitPredictor("model.h5")
        self.predictor.load_model()

    def test_predict_shape_and_output(self):
        x = np.random.rand(1, 28, 28, 1).astype("float32")
        pred = self.predictor.predict(x)
        self.assertIsInstance(pred, int)

    def test_predict_raises_if_not_loaded(self):
        p = DigitPredictor("model.h5")
        with self.assertRaises(RuntimeError):
            p.predict(np.random.rand(1, 28, 28, 1).astype("float32"))
