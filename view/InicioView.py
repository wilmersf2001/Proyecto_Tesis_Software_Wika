import tkinter as tk
import threading
from PIL import Image, ImageTk

from database.query.User import update_user_auth, logout_user
from utils.FrameCapture import FrameCapture
from ai.FaceDetection import ModeloFacedetection
from utils.Constants import Constants
from styles.Labels import lb_bienvenido_style
from styles.Buttons import btn_image_style
from utils.TextToSpeech import TextToSpeech


class InicioView(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bg="white")
        self.master = master
        self.frame_capture = FrameCapture(Constants.URL_IMGS + "/capture/fotografia_usuario.jpg")
        self.imagenes = {}
        
        self.name_user = ModeloFacedetection.reconocer_persona()

        label_bienvenido = tk.Label(self, text="¡WIKA TE DA LA BIENVENIDA!")
        label_bienvenido.config(**lb_bienvenido_style)
        label_bienvenido.pack(pady=10)

        imagen_tk = self.master.get_image('inicio', '', 200, 200)
        self.imagenes['inicio'] = imagen_tk
        self.label_imagen_inicio = tk.Label(self, image=imagen_tk, bg="white")
        self.label_imagen_inicio.pack(pady=10)

        imagen_iniciar_tk = self.master.get_image(
            'iniciar_aprendizaje', '', 218, 46)
        self.imagenes['iniciar'] = imagen_iniciar_tk
        btn_iniciar = tk.Button(self, image=imagen_iniciar_tk, bg="white",
                                command=self.go_to_create_account)
        btn_iniciar.config(**btn_image_style)

        if self.name_user:
            textBienvenida = f"BIENVENIDO {self.name_user.upper()} \n¡Iniciemos con el aprendizaje de lenguaje de señas!"
            
            # Ejecutar las dos tareas (audio y actualización de foto) en paralelo
            threading.Thread(target=self.call_text_to_speech, args=(textBienvenida,)).start()
            threading.Thread(target=self.update_user_image, args=(self.name_user,)).start()
            
            btn_iniciar.config(command=self.go_to_categories)
            update_user_auth(self.name_user.upper())
        else:
            logout_user()

        btn_iniciar.pack(pady=10)
    
    def call_text_to_speech(self, message):
        TextToSpeech.text_to_speech(message)
    
    def update_user_image(self, user_name):
        imagen_tk = self.master.get_image('usuario', user_name, 250, 250)
        self.label_imagen_inicio.config(image=imagen_tk)
        self.label_imagen_inicio.image = imagen_tk  # Necesario para evitar que la imagen sea recolectada por el GC

    def go_to_create_account(self):
        self.master.show_create_account_view()

    def go_to_categories(self):
        self.master.show_categories_view()
