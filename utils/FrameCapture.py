import os
from picamera2 import Picamera2
from PIL import Image

class FrameCapture:
    def __init__(self, nombre_foto):  # Asegúrate de que este argumento esté presente
        self.picam2 = None
        try:
            # Inicializa y configura Picamera2
            self.picam2 = Picamera2()
            self.picam2.configure(self.picam2.create_preview_configuration(
                main={"format": 'BGR888', "size": (450, 400)}))
            self.picam2.start()

            # Captura la imagen y la guarda con el nombre especificado
            self.capturar_imagen(nombre_foto)

            # Libera la cámara después de capturar la imagen
            self.detener_camara()
        except Exception as e:
            print(f"Error al inicializar o capturar la cámara: {e}")
            if self.picam2:
                self.detener_camara()  # Asegura que se libere en caso de error

    def capturar_imagen(self, nombre_foto):
        if self.picam2 is None:
            print("La cámara no está inicializada")
            return

        # Captura un frame y guarda la imagen
        frame = self.picam2.capture_array()
        if frame is not None:
            img = Image.fromarray(frame)
            img.save(nombre_foto)
            print(f"Imagen guardada como {nombre_foto}")
        else:
            print("No se pudo capturar la imagen: frame es None")

    def detener_camara(self):
        if self.picam2:
            self.picam2.stop()
            self.picam2.close()
            self.picam2 = None
            print("Cámara detenida y liberada.")

