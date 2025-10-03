# src/image_processor.py
from PIL import Image
import numpy as np
import os

def load_and_preprocess_image(image_path: str) -> np.ndarray:
    """
    Carga una imagen .jpg, la convierte a escala de grises, la redimensiona a 28x28 píxeles,
    la normaliza y le da la forma (1, 28, 28, 1) para el modelo.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"La imagen no existe: {image_path}")

    try:
        # Abrir imagen
        img = Image.open(image_path).convert('L')  # 'L' = escala de grises
        img = img.resize((28, 28))  # Redimensionar a 28x28

        # Convertir a numpy array y normalizar
        img_array = np.array(img).astype('float32') / 255.0

        # Expandir dimensiones para el modelo CNN: (1, 28, 28, 1)
        img_array = np.expand_dims(img_array, axis=(0, -1))

        return img_array
    except Exception as e:
        raise ValueError(f"No se pudo procesar la imagen: {e}")

# src/image_processor.py

# 👇 al final del archivo
preprocess_image = load_and_preprocess_image

