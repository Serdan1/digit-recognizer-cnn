# scripts/train_model.py
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import numpy as np
import os

# Para reproducibilidad
tf.random.set_seed(42)
np.random.seed(42)

def build_model():
    model = models.Sequential([
        layers.Input(shape=(28,28,1)),
        layers.Conv2D(32, (3,3), activation='relu'),
        layers.MaxPooling2D((2,2)),
        layers.Conv2D(64, (3,3), activation='relu'),
        layers.MaxPooling2D((2,2)),
        layers.Conv2D(64, (3,3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

print("Cargando MNIST...")
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0
x_train = x_train[..., None]
x_test = x_test[..., None]

model = build_model()
model.summary()

os.makedirs("models", exist_ok=True)
checkpoint = ModelCheckpoint("models/best_model.h5", save_best_only=True, monitor="val_accuracy", mode="max")
earlystop = EarlyStopping(monitor="val_accuracy", patience=3, restore_best_weights=True)

history = model.fit(
    x_train, y_train,
    epochs=10,
    batch_size=64,
    validation_data=(x_test, y_test),
    callbacks=[checkpoint, earlystop],
    verbose=1
)

# Guardar modelo final
model.save("model.h5")
print("✅ Modelo entrenado y guardado en model.h5")
