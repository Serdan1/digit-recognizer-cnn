import unittest
from src.model import DigitModel
import tensorflow as tf

class TestDigitModel(unittest.TestCase):
    def setUp(self):
        self.model = DigitModel()
        self.model.build_model()
        (x_train, y_train), _ = tf.keras.datasets.mnist.load_data()
        x_train = x_train.astype('float32') / 255.0
        x_train = tf.expand_dims(x_train, -1)[:100]  # Usar solo 100 muestras para test rápido
        y_train = y_train[:100]
        self.x_train = x_train
        self.y_train = y_train

    def test_model_build(self):
        """Verifica que el modelo se construya correctamente."""
        self.assertIsNotNone(self.model.model)
        self.assertEqual(len(self.model.model.layers), 8)

    def test_model_train(self):
        """Verifica que el modelo se entrene y devuelva métricas sin errores."""
        history = self.model.model.fit(self.x_train, self.y_train, epochs=1, verbose=0)
        accuracy = history.history['accuracy'][-1]
        self.assertGreaterEqual(accuracy, 0.10, "La accuracy debería ser > 0.10 tras 1 epoch de entrenamiento con pocas muestras")

    def test_model_save_load(self):
        """Verifica que el modelo se guarde y cargue correctamente."""
        self.model.train(epochs=1)
        self.model.save_model('test_model.h5')
        loaded_model = DigitModel()
        loaded_model.load_model('test_model.h5')
        self.assertIsNotNone(loaded_model.model)

if __name__ == '__main__':
    unittest.main()
