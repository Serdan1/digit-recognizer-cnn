# main.py
from src.gui import DigitRecognizerGUI

if __name__ == "__main__":
    app = DigitRecognizerGUI(
        model_path="model.h5",
        firebase_cred="proyecto-mnist-dashboard-firebase-adminsdk-fbsvc-57d1f6e9be.json",
        firebase_bucket="proyecto-mnist-dashboard.firebasestorage.app"
    )
    app.run()
