# src/gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw
import numpy as np
from src.predictor import DigitPredictor
from src.image_processor import preprocess_image
from src.firebase_utils import FirebaseUploader


class DigitRecognizerGUI:
    def __init__(self, model_path="model.h5", firebase_cred=None, firebase_bucket=None):
        self.window = tk.Tk()
        self.window.title("Reconocimiento de Dígitos - MNIST")
        self.window.geometry("400x550")
        self.window.configure(bg="#f5f5f5")

        # Predictor
        self.predictor = DigitPredictor(model_path=model_path)
        try:
            self.predictor.load_model()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el modelo: {e}")

        # Firebase (opcional)
        self.firebase = None
        if firebase_cred and firebase_bucket:
            try:
                self.firebase = FirebaseUploader(firebase_cred, firebase_bucket)
                print("✅ Firebase inicializado correctamente")
            except Exception as e:
                print(f"⚠️ No se pudo inicializar Firebase: {e}")

        # Canvas para dibujar
        self.canvas = tk.Canvas(self.window, width=280, height=280, bg="white", cursor="cross")
        self.canvas.pack(pady=10)
        self.canvas.bind("<B1-Motion>", self.draw)

        # Imagen PIL para dibujar encima
        self.image = Image.new("L", (280, 280), color=255)
        self.draw_pil = ImageDraw.Draw(self.image)

        # Botones
        btn_frame = tk.Frame(self.window, bg="#f5f5f5")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Predecir", command=self.predict, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Limpiar", command=self.clear_canvas, bg="#f44336", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Cargar Imagen", command=self.load_image, bg="#2196F3", fg="white").grid(row=0, column=2, padx=5)

        # Resultado
        self.result_label = tk.Label(self.window, text="", font=("Helvetica", 48), bg="#f5f5f5")
        self.result_label.pack(pady=10)

        # URL Firebase
        self.url_label = tk.Label(self.window, text="", font=("Helvetica", 9), fg="blue", bg="#f5f5f5", wraplength=380, cursor="hand2")
        self.url_label.pack(pady=5)

    def draw(self, event):
        x, y = event.x, event.y
        r = 8  # Radio del pincel
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="black", outline="black")
        self.draw_pil.ellipse([x - r, y - r, x + r, y + r], fill=0)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (280, 280), color=255)
        self.draw_pil = ImageDraw.Draw(self.image)
        self.result_label.config(text="")
        self.url_label.config(text="", cursor="arrow")

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not file_path:
            return
        try:
            img_array = preprocess_image(file_path)
            prediction = self.predictor.predict(img_array)
            self.result_label.config(text=str(prediction))

            # Subir a Firebase si está disponible
            if self.firebase:
                url = self.firebase.upload_image(file_path)
                self.show_url(url)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar la imagen: {e}")

    def predict(self):
        # Guardar dibujo temporalmente
        temp_path = "temp_draw.jpg"
        self.image.save(temp_path)
        img_array = preprocess_image(temp_path)
        prediction = self.predictor.predict(img_array)
        self.result_label.config(text=str(prediction))

        # Subir a Firebase si está disponible
        if self.firebase:
            url = self.firebase.upload_image(temp_path)
            self.show_url(url)

    def show_url(self, url):
        """Muestra la URL en la etiqueta y permite abrirla en navegador al hacer clic."""
        self.url_label.config(text=url, fg="blue", cursor="hand2")
        self.url_label.bind("<Button-1>", lambda e: self.open_url(url))

    def open_url(self, url):
        import webbrowser
        webbrowser.open_new(url)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = DigitRecognizerGUI(
        model_path="model.h5",
        firebase_cred="proyecto-mnist-dashboard-firebase-adminsdk-fbsvc-57d1f6e9be.json",
        firebase_bucket="proyecto-mnist-dashboard.firebasestorage.app"
    )
    gui.run()
