# scripts/eval_model_on_mnist.py
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np

print("Cargando modelo model.h5 ...")
model = load_model("model.h5")
model.summary()

print("Cargando MNIST test set ...")
(_, _), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_test = x_test.astype('float32') / 255.0
x_test = x_test[..., None]

loss, acc = model.evaluate(x_test, y_test, verbose=1)
print("MNIST test accuracy:", acc)
