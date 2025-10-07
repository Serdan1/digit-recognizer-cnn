# scripts/debug_single_image.py
from src.image_processor import preprocess_image
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import sys

if len(sys.argv) < 2:
    print("Usage: python scripts/debug_single_image.py path/to/image.jpg")
    sys.exit(1)

path = sys.argv[1]
model = load_model("model.h5")
arr = preprocess_image(path, debug_save_path="debug_processed.png")
print("Saved debug_processed.png")
print("Shape:", arr.shape)
preds = model.predict(arr)
print("Probs:", np.round(preds.flatten(), 4))
print("Predicted:", int(np.argmax(preds)))
