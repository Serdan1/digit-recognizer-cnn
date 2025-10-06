import tensorflow as tf
import numpy as np
import os

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
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"No se encontró el modelo en la ruta: {self.model_path}")

        try:
            self.model = tf.keras.models.load_model(self.model_path)
            print(f"✅ Modelo cargado correctamente desde {self.model_path}")
            # Mostramos info útil
            self.model.summary()
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

        # Verificar forma de entrada
        if image_array.shape != (1, 28, 28, 1):
            raise ValueError(f"La imagen tiene forma {image_array.shape}, se esperaba (1, 28, 28, 1)")

        # Realizar predicción
        predictions = self.model.predict(image_array)
        predicted_label = int(np.argmax(predictions, axis=1)[0])

        # Debug: ver probabilidades
        probs = predictions[0]
        top3_idx = np.argsort(probs)[::-1][:3]
        print("🔍 Top 3 predicciones:")
        for idx in top3_idx:
            print(f"   {idx} → {probs[idx]:.4f}")

        return predicted_label
