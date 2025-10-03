import tensorflow as tf
from tensorflow.keras import layers, models  # type: ignore
import numpy as np
import matplotlib.pyplot as plt

class DigitModel:
    def __init__(self):
        self.model = None
        self.history = None

    def build_model(self):
        """Construye un modelo CNN basado en el ejemplo MNIST del PDF."""
        self.model = models.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dense(10, activation='softmax')
        ])
        self.model.compile(optimizer='adam',
                         loss='sparse_categorical_crossentropy',
                         metrics=['accuracy'])

    def train(self, epochs=5):
        """Entrena el modelo con el dataset MNIST."""
        # Cargar MNIST
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
        x_train = x_train.astype('float32') / 255.0
        x_test = x_test.astype('float32') / 255.0
        x_train = np.expand_dims(x_train, -1)
        x_test = np.expand_dims(x_test, -1)

        # Entrenar
        self.history = self.model.fit(x_train, y_train, epochs=epochs,
                                   validation_data=(x_test, y_test), verbose=1)

        # Visualizar curvas de aprendizaje (inspirado en página 17 del PDF)
        plt.plot(self.history.history['accuracy'], label='accuracy')
        plt.plot(self.history.history['val_accuracy'], label='val_accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.show()

    def save_model(self, filepath='model.h5'):
        """Guarda el modelo entrenado."""
        self.model.save(filepath)
        print(f"Modelo guardado en {filepath}")

    def load_model(self, filepath='model.h5'):
        """Carga un modelo previamente guardado."""
        self.model = tf.keras.models.load_model(filepath)