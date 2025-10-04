# main.py
from src.gui import DigitRecognizerGUI

if __name__ == "__main__":
    app = DigitRecognizerGUI(model_path="model.h5")
    app.run()
