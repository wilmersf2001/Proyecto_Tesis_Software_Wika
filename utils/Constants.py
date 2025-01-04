import cv2

class Constants:
    URL_IMGS = "/home/wika/Documentos/proyecto-wika/assets/imgs"
    URL_DATABASE = "/home/wika/Documentos/proyecto-wika/database/db_wika.db"
    URL_MODEL_CNN_CONSONANTES = "/home/wika/Documentos/proyecto-wika/assets/models/model_consonantes.keras"
    URL_MODEL_CNN_VOCALES = "/home/wika/Documentos/proyecto-wika/assets/models/model_vocales.keras"
    URL_MODEL_CNN_NUMEROS = "/home/wika/Documentos/proyecto-wika/assets/models/model_numeros.keras"
    URL_MODEL_CNN_PALABRAS = "/home/wika/Documentos/proyecto-wika/assets/models/model_palabras.keras"
    
    FRAME_ACTIONS_PATH = '/home/wika/Documentos/proyecto-wika/assets/imgs/frames_words'
    DATA_PATH = "/home/wika/Documentos/proyecto-wika/assets/models/data_palabras"
    MODELS_PATH = "/home/wika/Documentos/proyecto-wika/assets/models/models_palabras"
    WORD_PATH = "/home/wika/Documentos/proyecto-wika/assets/imgs/frames_words"

    MAX_LENGTH_FRAMES = 15
    LENGTH_KEYPOINTS = 1662
    MIN_LENGTH_FRAMES = 5
    MODEL_NAME = f"actions_{MAX_LENGTH_FRAMES}.keras"

    FONT = cv2.FONT_HERSHEY_PLAIN
    FONT_SIZE = 1.5
    FONT_POS = (5, 30)