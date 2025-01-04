import os
import cv2
import numpy as np
from mediapipe.python.solutions.holistic import Holistic
from tensorflow.keras.models import load_model
from utils.UtilFuctions import extract_keypoints, get_actions, mediapipe_detection, there_hand
from utils.Constants import Constants


class SignLanguageModelEvaluator:
    def __init__(self):
        self.model_path = os.path.join(Constants.MODELS_PATH, Constants.MODEL_NAME)
        self.image_dir = Constants.FRAME_ACTIONS_PATH
        self.threshold = 0.8
        self.model = load_model(self.model_path)
        self.actions = get_actions(Constants.DATA_PATH)

    def evaluate(self):
        kp_sequence = []
        predictions = []

        # Verificar si hay imágenes en la carpeta
        image_paths = [os.path.join(self.image_dir, img) for img in os.listdir(self.image_dir) if img.endswith('.jpg') or img.endswith('.png')]
        
        if not image_paths:
            return ["No encontrado"]  # Retorna "No encontrado" si no hay imágenes

        with Holistic() as holistic_model:
            for image_path in image_paths:
                frame = cv2.imread(image_path)

                if frame is None:
                    continue

                image, results = mediapipe_detection(frame, holistic_model)
                kp_sequence.append(extract_keypoints(results))

                if len(kp_sequence) >= Constants.MAX_LENGTH_FRAMES and there_hand(results):
                    res = self.model.predict(np.expand_dims(kp_sequence[-Constants.MAX_LENGTH_FRAMES:], axis=0))[0]

                    if res[np.argmax(res)] > self.threshold:
                        prediction = self.actions[np.argmax(res)]
                        predictions.append(prediction)
                    else:
                        predictions.append("Unknown")

                    # Reset sequence after prediction
                    kp_sequence = []

            # Handle cases where the sequence is shorter than MAX_LENGTH_FRAMES
            if len(kp_sequence) > 0:
                res = self.model.predict(np.expand_dims(kp_sequence, axis=0))[0]
                if res[np.argmax(res)] > self.threshold:
                    prediction = self.actions[np.argmax(res)]
                    predictions.append(prediction)
                else:
                    predictions.append("Unknown")

        return predictions
