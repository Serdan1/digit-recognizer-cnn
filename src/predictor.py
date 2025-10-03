# src/predictor.py
import tensorflow as tf
import numpy as np

class DigitPredictor:
    def __init__(self, model_path: str = "model.h5"):
        """
        Inicializa el predictor con la ruta al modelo entrenado.
        """
        self.model_path = model_path
        self.model = None

    def load_model(self):
        """
        Carga el modelo entrenado desde la ruta especificada.
        """
        try:
            self.model = tf.keras.models.load_model(self.model_path)
            print(f"✅ Modelo cargado correctamente desde {self.model_path}")
        except Exception as e:
            raise RuntimeError(f"Error al cargar el modelo: {e}")

    def predict(self, image_array: np.ndarray) -> int:
        """
        Predice el dígito contenido en la imagen preprocesada.
        image_array debe tener forma (1, 28, 28, 1).
        Devuelve el dígito más probable (0–9).
        """
        if self.model is None:
            raise ValueError("El modelo no está cargado. Llama a load_model() primero.")

        predictions = self.model.predict(image_array)
        predicted_label = int(np.argmax(predictions, axis=1)[0])
        return predicted_label
