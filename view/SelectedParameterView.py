import time
import tkinter as tk
from tkinter import ttk
import threading
from gpiozero import LED
from time import sleep
from utils.CameraController import CameraController
from utils.CameraControllerLsp import CameraControllerLsp
from ai.LstmModelo import SignLanguageModelEvaluator
from utils.TextToSpeech import TextToSpeech
from ai.CNN import ModeloCNN
from utils.Constants import Constants
from database.query.User import get_user_auth
from database.query.Progress import get_progress_user_by_category, aumentar_correctas_progress, aumentar_incorrectas_progress
from styles.Buttons import btn_image_style, btn_continuar_style
from styles.Labels import lb_seleccion_titulo_style, lb_seleccion_parametro_style, lb_seleccion_subtitulo_style, lb_conteo_style, lb_correcto_style, lb_incorrecto_style

ledSuccess = LED(19)
ledError = LED(26)

class SelectedParameterView(tk.Frame):
    def __init__(self, master, id_parametro, parametro, categoria, categoria_id):
        super().__init__(master)
        self.master = master
        self.id_parametro = id_parametro
        self.parametro = parametro
        self.categoria = categoria
        self.categoria_id = categoria_id
        self.imagenes = {}
        self.user = get_user_auth()[1] if get_user_auth() else "invitado"
        self.progress_category = get_progress_user_by_category(
            get_user_auth()[0], self.categoria_id) if get_user_auth() else 0

        self.frame_izq = tk.Frame(self, bg='#2196f3', width=180)
        self.frame_izq.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_izq.pack_propagate(False)

        self.frame_der = tk.Frame(self, bg='white')
        self.frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.resultado = ''

        imagen_tk = self.master.get_image('regresar', '', 80, 80)
        self.imagenes['regresar'] = imagen_tk
        boton_regresar = tk.Button(
            self.frame_izq, image=imagen_tk, command=lambda: self.go_to_category_selected_view(self.categoria_id, self.categoria))
        boton_regresar.config(**btn_image_style)
        boton_regresar.pack(fill=tk.X, padx=50, pady=25)

        label_inferior = tk.Label(
            self.frame_izq, text=self.user)
        label_inferior.pack(side=tk.BOTTOM, padx=40, pady=25)

        if self.user != "invitado":
            self.progress_label = tk.Label(
                self.frame_izq, text=f"{self.progress_category}%\n" + " " + self.categoria.lower())
            self.progress_label.pack(side=tk.BOTTOM, padx=40, pady=5)

            self.progress_bar = ttk.Progressbar(
                self.frame_izq, orient="horizontal", length=150, mode="determinate")
            self.progress_bar.pack(side=tk.BOTTOM, padx=40, pady=5)
            self.update_progress_bar(self.progress_category)

        lb_titulo = tk.Label(self.frame_der,
                             text="EL PARAMETRO SELECCIONADO ES: ")
        lb_titulo.config(**lb_seleccion_titulo_style)
        lb_titulo.pack(pady=(10, 0))

        lb_parametro = tk.Label(self.frame_der, text=self.parametro)
        lb_parametro.config(**lb_seleccion_parametro_style)
        lb_parametro.pack(pady=(0, 10))

        self.lb_txt_seleccionado = tk.Label(
            self.frame_der, text="Recuerda ensayar la palabra, letra o vocal seleccionada antes de iniciar la \nprueba de aprendizaje. ¡Tú puedes!")
        self.lb_txt_seleccionado.config(**lb_seleccion_subtitulo_style)
        self.lb_txt_seleccionado.pack()

        imagen_tk = self.master.get_image(self.categoria.lower(),
                                          f"representacion/{self.parametro}", 150, 150)
        self.imagen_seleccionado = tk.Label(self.frame_der, image=imagen_tk)
        self.imagen_seleccionado.pack(pady=(15,10))

        self.button_iniciar = tk.Button(
            self.frame_der, text="Iniciar Predicción", command=lambda: self.iniciar_prediccion())
        self.button_iniciar.config(**btn_continuar_style)
        self.button_iniciar.pack(pady=10)

    def go_to_category_selected_view(self, id_categoria, nombre_categoria):
        self.master.show_category_selected_view(id_categoria, nombre_categoria)

    def iniciar_prediccion(self):
        self.lb_txt_seleccionado.config(
            text="¡Muy bien! Ahora, vamos a iniciar la predicción. \nTienes 5 segundos ¡Concéntrate!")
        self.imagen_seleccionado.pack_forget()
        self.button_iniciar.pack_forget()

        # Crear e iniciar el hilo para la captura y predicción
        thread = threading.Thread(target=self.ejecutar_prediccion)
        thread.start()

    def ejecutar_prediccion(self):
        contador = 5
        self.app_instance = CameraController(self.frame_der, False)
        self.lb_conteo = tk.Label(self.frame_der, text="5")
        self.lb_conteo.config(**lb_conteo_style)
        self.lb_conteo.pack(pady=5)
             
        for i in range(contador, 0, -1):
            self.lb_conteo.config(text=str(i))
            time.sleep(1)

        self.lb_conteo.pack_forget()
        self.lb_txt_seleccionado.pack_forget()
    
        #Categorías generales (vocales, consonantes, números)
        self.app_instance.tomar_foto(
            Constants.URL_IMGS+"/capture/fotografia_mano.jpg")
        self.app_instance.detener_camara()
        nombre_mano_cap, predicted_character = ModeloCNN.guardar_detectar_mano(
            self.categoria)

        # Luego del procesamiento, actualizar la UI en el hilo principal
        self.master.after(0, self.actualizar_interfaz,
                          nombre_mano_cap, predicted_character)
    
    
    def actualizar_interfaz(self, nombre_mano_cap, predicted_character):
        print(nombre_mano_cap, predicted_character)

        if nombre_mano_cap == 'undetected' and predicted_character == 'forbidden':
            self.respuesta = 'No posicionaste bien la mano, inténtalo de nuevo'
            imagen_tk = self.master.get_image('undetected', '', 164, 167)
            self.imagen_seleccionado = tk.Label(
                self.frame_der, image=imagen_tk)
            self.imagen_seleccionado.pack(pady=10)
            self.call_text_to_speech(self.respuesta)
        else:
            imagen_tk = self.master.get_image(
                'manos', nombre_mano_cap, 160, 200)
            self.imagen_seleccionado = tk.Label(
                self.frame_der, image=imagen_tk)
            self.imagen_seleccionado.pack(pady=10)

        if predicted_character == 'forbidden':
            self.respuesta = "Ups! ocurrió un error al detectar la seña,\nintenta de nuevo."
            lb_no_detectado = tk.Label(self.frame_der, text=self.respuesta)
            lb_no_detectado.config(**lb_incorrecto_style)
            lb_no_detectado.pack(pady=10)
        elif predicted_character == 'undetected':
            self.respuesta = "¡No se detectó ninguna seña!, \nintenta de nuevo."
            lb_no_detectado = tk.Label(
                self.frame_der, text=self.respuesta)
            lb_no_detectado.config(**lb_incorrecto_style)
            lb_no_detectado.pack(expand=True)
            self.start_parallel_feedback(self.respuesta, ledError)
        else:
            if predicted_character == self.parametro:
                if get_user_auth():
                    aumentar_correctas_progress(
                        get_user_auth()[0], self.id_parametro)
                    
                self.respuesta = f"¡Correcto! La seña detectada es: {predicted_character}"
                lb_correcto = tk.Label(
                    self.frame_der, text=self.respuesta)
                lb_correcto.config(**lb_correcto_style)
                lb_correcto.pack(pady=10)
                self.start_parallel_feedback(self.respuesta, ledSuccess)
            else:
                if get_user_auth():
                    aumentar_incorrectas_progress(
                        get_user_auth()[0], self.id_parametro)
                    
                self.respuesta = f"¡Incorrecto! La seña detectada es: {predicted_character}"
                lb_incorrecto = tk.Label(
                    self.frame_der, text=self.respuesta)
                lb_incorrecto.config(**lb_incorrecto_style)
                lb_incorrecto.pack(expand=True)
                self.start_parallel_feedback(self.respuesta, ledError)

        self.frame_der.update_idletasks()

    def update_progress_bar(self, progress_category):
        self.progress_bar['value'] = progress_category
    
    def start_parallel_feedback(self, message, led):
        # Crear subprocesos para realizar las tareas en paralelo
        threading.Thread(target=self.handle_led, args=(led,)).start()
        threading.Thread(target=self.call_text_to_speech, args=(message,)).start()
        threading.Thread(target=self.update_ui_feedback, args=(message,)).start()

    def handle_led(self, led):
        led.on()
        sleep(3)
        led.off()

    def update_ui_feedback(self, message):
        # Aquí puedes agregar lógica adicional si es necesario
        print(f"Actualizando UI con el mensaje: {message}")
    
    def call_text_to_speech(self, message):
        TextToSpeech.text_to_speech(message)
    
