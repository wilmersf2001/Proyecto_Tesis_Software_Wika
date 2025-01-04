import tkinter as tk
import cv2
from PIL import Image, ImageTk
from picamera2 import Picamera2
import threading


class CameraController:
    def __init__(self, frame_izq, is_recognition):
        self.clasificadorRostro = cv2.CascadeClassifier(
            f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')

        self.frame_izq = frame_izq
        self.is_recognition = is_recognition

        self.canvas = tk.Canvas(frame_izq, width=230, height=200)
        self.canvas.pack(pady=10)

        try:
            self.picam2 = Picamera2()
            self.picam2.configure(self.picam2.create_preview_configuration(
                main={"format": 'BGR888', "size": (450, 400)}))
            self.picam2.start()
        except RuntimeError as e:
            print(f"Error initializing camera: {e}")
            # Asegúrate de no tener una referencia a una cámara que no se pudo inicializar.
            self.picam2 = None

        if self.picam2:
            self.thread = threading.Thread(target=self.actualizar_camara)
            self.thread.daemon = True
            self.thread.start()

    def actualizar_camara(self):
        while self.picam2:
            frame = self.picam2.capture_array()
            if self.is_recognition:
                auxFrame = frame.copy()
                self.faces = self.clasificadorRostro.detectMultiScale(
                    frame, 1.2, 5)
                for (x, y, w, h) in self.faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    rostro = auxFrame[y:y+h, x:x+w]
                    rostro = cv2.resize(rostro, (240, 240),
                                        interpolation=cv2.INTER_CUBIC)

            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=img)

            self.canvas.img_tk = img_tk
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

            #self.frame_izq.after(50)

    def tomar_foto(self, nombre_foto):
        if not self.picam2:
            # Evita intentar capturar si la cámara no está inicializada.
            return False

        frame = self.picam2.capture_array()
        frame = cv2.resize(frame, (400, 350))
        img = Image.fromarray(frame)
        if self.is_recognition:
            if len(self.faces) > 0:
                img.save(nombre_foto)
                return True
            else:
                return False
        else:
            img.save(nombre_foto)
            return True

    def detener_camara(self):
        if self.picam2:
            self.picam2.stop()
            # Asegúrate de liberar correctamente la cámara.
            self.picam2.close()
            self.picam2 = None
        self.canvas.pack_forget()
