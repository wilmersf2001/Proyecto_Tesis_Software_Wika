import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
from mediapipe.python.solutions.holistic import Holistic
from utils.UtilFuctions import create_folder, draw_keypoints, mediapipe_detection, there_hand
from utils.Constants import Constants
from picamera2 import Picamera2
import threading
import os


class CameraControllerLsp:
    def __init__(self, frame_izq):
        self.frame_izq = frame_izq
        self.margin_frame = 2
        self.min_cant_frames = 5
        self.path = Constants.WORD_PATH
        self.max_images = 15
        self.count_frame = 0
        self.frames = []

        create_folder(self.path)
        self.clear_existing_images()  # Limpiar imágenes existentes al inicializar

        self.canvas = tk.Canvas(frame_izq, width=230, height=200)
        self.canvas.pack(pady=10)

        self.holistic_model = Holistic()

        # Inicialización de Picamera2
        try:
            self.picam2 = Picamera2()
            self.picam2.configure(self.picam2.create_preview_configuration(
                main={"format": 'RGB888', "size": (450, 400)}))
            self.picam2.start()
        except RuntimeError as e:
            print(f"Error initializing camera: {e}")
            self.picam2 = None

        if self.picam2:
            self.thread = threading.Thread(target=self.actualizar_camara)
            self.thread.daemon = True
            self.thread.start()

    def clear_existing_images(self):
        """Elimina todas las imágenes existentes en la carpeta especificada."""
        for filename in os.listdir(self.path):
            file_path = os.path.join(self.path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Eliminado: {file_path}")
            except Exception as e:
                print(f"Error al eliminar {file_path}: {e}")

    def actualizar_camara(self):
        while self.picam2:
            frame = self.picam2.capture_array()
            image, results = mediapipe_detection(frame, self.holistic_model)

            if there_hand(results):
                self.count_frame += 1
                if self.count_frame > self.margin_frame:
                    cv2.putText(image, 'Capturando...', Constants.FONT_POS,
                                Constants.FONT, Constants.FONT_SIZE, (255, 50, 0))
                    self.frames.append(np.asarray(frame))

                    if len(self.frames) >= self.max_images:
                        self.frames = self.frames[:self.max_images]
                        print("Guardando imágenes...")
                        self.save_frames(self.frames, self.path)
                        self.frames = []  # Limpiar frames después de guardar
                        cv2.putText(image, 'Guardado', Constants.FONT_POS,
                                    Constants.FONT, Constants.FONT_SIZE, (0, 255, 0))
            else:
                if len(self.frames) > self.min_cant_frames + self.margin_frame:
                    self.frames = self.frames[:-self.margin_frame]
                    print("Guardando imágenes debido a la detección de mano...")
                    self.save_frames(self.frames, self.path)
                    self.frames = []  # Limpiar frames después de guardar
                    cv2.putText(image, 'Guardado', Constants.FONT_POS,
                                Constants.FONT, Constants.FONT_SIZE, (0, 255, 0))

                self.count_frame = 0
                cv2.putText(image, 'Listo para capturar...',
                            Constants.FONT_POS, Constants.FONT, Constants.FONT_SIZE, (0, 220, 100))

            draw_keypoints(image, results)

            image_rgb = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            img = Image.fromarray(image_rgb)
            img_tk = ImageTk.PhotoImage(image=img)

            self.canvas.img_tk = img_tk
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

    def save_frames(self, frames, path):
        # Asegúrate de que el directorio existe
        os.makedirs(path, exist_ok=True)

        for i, frame in enumerate(frames):
            filename = os.path.join(path, f'imagen_{i + 1}.jpg')
            # Guarda la imagen usando OpenCV
            if cv2.imwrite(filename, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)):
                print(f"Imagen {i + 1} guardada exitosamente en {filename}.")
            else:
                print(f"Error al guardar la imagen {i + 1} en {filename}.")

    def detener_camara(self):
        if self.picam2:
            self.picam2.stop()
            self.picam2.close()
            self.picam2 = None
        self.holistic_model.close()
        self.canvas.pack_forget()
