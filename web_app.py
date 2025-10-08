# web_app.py
import gradio as gr
import numpy as np
from src.predictor import DigitPredictor
from src.image_processor import preprocess_image

# Cargar el modelo entrenado
predictor = DigitPredictor("model.h5")
predictor.load_model()

def predict_digit(image):
    """
    Función que recibe una imagen (ruta temporal),
    la preprocesa y devuelve el dígito predicho.
    """
    if image is None:
        return "No se ha cargado ninguna imagen"
    img_array = preprocess_image(image)
    prediction = predictor.predict(img_array)
    return f"Predicción: {prediction}"

# Interfaz de Gradio
demo = gr.Interface(
    fn=predict_digit,
    inputs=gr.Image(type="filepath", label="Sube o dibuja un número"),
    outputs=gr.Textbox(label="Resultado"),
    title="🧠 Reconocimiento de Dígitos MNIST",
    description="Sube, arrastra o dibuja un dígito (0–9) para que el modelo lo reconozca.",
    allow_flagging="never"
)

if __name__ == "__main__":
    demo.launch()
