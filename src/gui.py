# src/gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import os

from src.image_processor import preprocess_image
from src.predictor import DigitPredictor
from src.firebase_utils import FirebaseUploader

class DigitRecognizerGUI:
    def __init__(self, model_path: str, firebase_cred: str, firebase_bucket: str):
        # Inicializar predictor y firebase
        self.predictor = DigitPredictor(model_path)
        self.predictor.load_model()
        self.uploader = FirebaseUploader(firebase_cred, firebase_bucket)

        # Crear ventana principal
        self.root = TkinterDnD.Tk()
        self.root.title("Digit Recognizer 🧠")
        self.root.geometry("400x500")

        # Label de instrucciones
        self.label = tk.Label(self.root, text="Arrastra una imagen .jpg aquí o haz clic para cargar",
                              bg="#f0f0f0", relief="ridge", width=50, height=10)
        self.label.pack(pady=20)

        # Soporte drag & drop
        self.label.drop_target_register(DND_FILES)
        self.label.dnd_bind('<<Drop>>', self.on_drop)

        # Botón de carga manual
        self.button = tk.Button(self.root, text="Cargar imagen", command=self.load_file)
        self.button.pack(pady=10)

        # Label para mostrar imagen
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)

        # Label de resultado
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 18))
        self.result_label.pack(pady=10)

    def on_drop(self, event):
        file_path = event.data.strip('{}')  # Quitar llaves en rutas con espacios
        self.process_image(file_path)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg")])
        if file_path:
            self.process_image(file_path)

    def process_image(self, file_path):
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

            # Mostrar imagen en GUI
            img = Image.open(file_path)
            img.thumbnail((200, 200))
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.configure(image=img_tk)
            self.image_label.image = img_tk

            # Preprocesar imagen y predecir
            processed = preprocess_image(file_path)
            prediction = self.predictor.predict(processed)
            self.result_label.config(text=f"Dígito reconocido: {prediction}")

            # Subir a Firebase
            url = self.uploader.upload_image(file_path)
            print(f"🌐 URL Firebase: {url}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{e}")

    def run(self):
        self.root.mainloop()
