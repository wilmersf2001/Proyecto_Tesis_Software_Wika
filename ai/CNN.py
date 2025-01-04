import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model
import time
from utils.Constants import Constants


class ModeloCNN:

    @staticmethod
    def guardar_detectar_mano(categoria):
        cantidad_manos = 0
        imagen = cv2.imread(Constants.URL_IMGS +
                            '/capture/fotografia_mano.jpg')
        H, W, _ = imagen.shape

        if categoria == 'VOCALES':
            model = load_model(Constants.URL_MODEL_CNN_VOCALES)
            index_to_parameter = {0: 'A', 1: 'E', 2: 'I', 3: 'O', 4: 'U'}
        elif categoria == 'CONSONANTES':
            model = load_model(Constants.URL_MODEL_CNN_CONSONANTES)
            index_to_parameter = {0: 'B', 1: 'C', 2: 'D', 3: 'F', 4: 'G', 5: 'H', 6: 'K', 7: 'L', 8: 'M',
                                  9: 'N', 10: 'P', 11: 'Q', 12: 'R', 13: 'S', 14: 'T', 15: 'V', 16: 'W', 17: 'X', 18: 'Y', 19: 'Z'}
        elif categoria == 'NUMEROS':
            model = load_model(Constants.URL_MODEL_CNN_NUMEROS)
            index_to_parameter = {0: '0', 1: '1', 2: '2', 3: '3',
                                  4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9'}
        elif categoria == 'PALABRAS':
            model = load_model(Constants.URL_MODEL_CNN_PALABRAS)
            index_to_parameter = {0: 'ABRAZAR', 1: 'CASA', 2: 'CODO', 3: 'CORTAR', 4: 'DISCULPAR', 5: 'DORMIR', 6: 'ENFERMO', 7: 'HORA',
                                  8: 'MIO', 9: 'QUIEN', 10: 'TOMAR', 11: 'TRABAJO', 12: 'TU', 13: 'YO', 14: 'ZAPATO'}
        else:
            return None
        
        if categoria == 'PALABRAS':
            # Inicializar Mediapipe
            mp_hands = mp.solutions.hands
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing_styles = mp.solutions.drawing_styles
            hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

            # Convertir imagen a RGB y procesarla con Mediapipe
            frame_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                data_aux = []
                x_ = []
                y_ = []

                # Dibujar los puntos de referencia en la imagen
                for hand_landmarks in results.multi_hand_landmarks:
                    cantidad_manos = len(results.multi_hand_landmarks)
                    mp_drawing.draw_landmarks(
                        imagen,  # imagen para dibujar
                        hand_landmarks,  # puntos de referencia
                        mp_hands.HAND_CONNECTIONS,  # conexiones de la mano
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )

                    # Extraer y normalizar puntos de referencia
                    for landmark in hand_landmarks.landmark:
                        x = landmark.x
                        y = landmark.y
                        x_.append(x)
                        y_.append(y)

                    for i in range(len(hand_landmarks.landmark)):
                        data_aux.append(x_[i] - min(x_))
                        data_aux.append(y_[i] - min(y_))

                # Rellenar con ceros si falta información de la segunda mano
                if cantidad_manos == 1:
                    data_aux.extend([0] * (84 - len(data_aux)))  # Completa hasta 84 valores

                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10
                x2 = int(max(x_) * W) + 10
                y2 = int(max(y_) * H) + 10
                
                region_mano = imagen[y1:y2, x1:x2]

                # Validar que la región no esté vacía
                if region_mano.size == 0:
                    return 'undetected', 'forbidden'

                if len(data_aux) == 84:  # Asegurar que el vector tiene el tamaño correcto
                    probabilities = model.predict(np.asarray([data_aux]))[0]

                    if np.max(probabilities) > 0.9:
                        predicted_class = np.argmax(probabilities)
                        predicted_character = index_to_parameter.get(predicted_class, 'Desconocido')
                    else:
                        predicted_character = "undetected"
                else:
                    predicted_character = "invalid input size"

                # Dibujar rectángulo en la imagen y guardar la región de la mano
                cv2.rectangle(imagen, (x1, y1), (x2, y2), (0, 0, 0), 4)
                region_mano = imagen[y1:y2, x1:x2]
                nombre_mano_cap = "foto_mano_" + str(time.time()) + ".jpeg"
                cv2.imwrite(Constants.URL_IMGS + '/hands/' + nombre_mano_cap, region_mano)

                return nombre_mano_cap, predicted_character
            else:
                return 'undetected', 'forbidden'
        else:
            # Inicializar Mediapipe
            mp_hands = mp.solutions.hands
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing_styles = mp.solutions.drawing_styles
            hands = mp_hands.Hands(static_image_mode=True,
                                   min_detection_confidence=0.3)

            # Convertir imagen a RGB y procesarla con Mediapipe
            frame_rgb = cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                data_aux = []
                x_ = []
                y_ = []

                # Dibujar los puntos de referencia en la imagen
                for hand_landmarks in results.multi_hand_landmarks:
                    cantidad_manos = len(results.multi_hand_landmarks)
                    mp_drawing.draw_landmarks(
                        imagen,  # imagen para dibujar
                        hand_landmarks,  # puntos de referencia
                        mp_hands.HAND_CONNECTIONS,  # conexiones de la mano
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

                    # Extraer y normalizar puntos de referencia
                    for landmark in hand_landmarks.landmark:
                        x = landmark.x
                        y = landmark.y
                        x_.append(x)
                        y_.append(y)

                    for i in range(len(hand_landmarks.landmark)):
                        data_aux.append(x_[i] - min(x_))
                        data_aux.append(y_[i] - min(y_))

                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10
                x2 = int(max(x_) * W) - 10
                y2 = int(max(y_) * H) - 10

                if cantidad_manos == 1:
                    probabilities = model.predict(np.asarray([data_aux]))[0]

                    if np.max(probabilities) > 0.9:
                        predicted_class = np.argmax(probabilities)
                        predicted_character = index_to_parameter.get(predicted_class, 'Desconocido')
                    else:
                        predicted_character = "undetected"
                else:
                    predicted_character = "forbidden"

                # Dibujar rectángulo en la imagen y guardar la región de la mano
                cv2.rectangle(imagen, (x1, y1), (x2, y2), (0, 0, 0), 4)
                region_mano = imagen[y1:y2, x1:x2]
                nombre_mano_cap = "foto_mano_" + str(time.time()) + ".jpeg"
                cv2.imwrite(Constants.URL_IMGS + '/hands/' + nombre_mano_cap, region_mano)

                return nombre_mano_cap, predicted_character
            else:
                return 'undetected', 'forbidden'
        
        
        
        
        
        
    
        
        
        
        
