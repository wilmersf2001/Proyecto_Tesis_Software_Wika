import tkinter as tk

from database.query.User import insert_user
from utils.CameraController import CameraController
from utils.Constants import Constants
from utils.UtilFuctions import buscar_usuario_por_nombre
from styles.Buttons import btn_image_style, btn_continuar_style, btn_registrado_style
from styles.Labels import lb_registrar_style, lb_name_user_style
from utils.Modals import Modals


class CreateAccountView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.frame_izq = tk.Frame(self)
        self.frame_izq.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.imagenes = {}

        self.frame_der = tk.Frame(self, bg='#bdebff')
        self.frame_der.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        canvas = tk.Canvas(self, width=5, bg="#2196f3")
        canvas.create_line(
            0, 0, 0, self.winfo_screenheight(), width=3)
        canvas.pack(side=tk.LEFT, fill=tk.Y)

        self.lb_registrar = tk.Label(
            self.frame_der, text="Wika quiere conocerte:\n ¿Deseas registrarte?")
        self.lb_registrar.config(**lb_registrar_style)
        self.lb_registrar.pack(expand=True)

        imagen_perfil_tk = self.master.get_image('perfil', '', 200, 200)
        self.imagenes['perfil'] = imagen_perfil_tk
        self.lb_imagen_registrar = tk.Label(
            self.frame_izq, image=imagen_perfil_tk)
        self.lb_imagen_registrar.pack(expand=True)

        imagen_registrarme_tk = self.master.get_image(
            'deseo_registrarme', '', 230, 52)
        self.imagenes['deseo_registrarme'] = imagen_registrarme_tk
        self.btn_habilitar_camara = tk.Button(
            self.frame_der, image=imagen_registrarme_tk, command=self.habilitar_camara)
        self.btn_habilitar_camara.config(**btn_image_style)
        self.btn_habilitar_camara.pack(pady=20)

        self.btn_registrado = tk.Button(self.frame_der, text="Ya tienes cuenta? Inicia Sesión",
                                        command=self.go_to_inicio)
        self.btn_registrado.config(**btn_registrado_style)
        self.btn_registrado.pack(pady=20)

        imagen_omitir_tk = self.master.get_image('omitir', '', 130, 35)
        self.imagenes['omitir'] = imagen_omitir_tk
        self.btn_skip = tk.Button(
            self.frame_der, image=imagen_omitir_tk, command=self.go_to_categories)
        self.btn_skip.config(**btn_continuar_style)
        self.btn_skip.pack(expand=True, pady=20)

    def habilitar_camara(self):
        self.app_instance = CameraController(self.frame_izq, True)

        self.btn_registrado.pack_forget()

        self.lb_registrar.config(
            text="¿Cómo te llamas?")

        self.lb_ingresar_nombre = tk.Label(
            self.frame_der, text="Introduce tu nombre:")
        self.lb_ingresar_nombre.config(**lb_name_user_style)
        self.lb_ingresar_nombre.pack(pady=20, padx=1)

        self.nombre_entrada = tk.Entry(self.frame_der, width=30,
                                       font=("Arial", 18))
        self.nombre_entrada.pack(pady=20)

        imagen_tomar_foto_tk = self.master.get_image('tomar_foto', '', 250, 72)
        self.imagenes['tomar_foto'] = imagen_tomar_foto_tk
        self.btn_tomar_foto = tk.Button(
            self.frame_der, image=imagen_tomar_foto_tk, command=self.capturar_imagen)
        self.btn_tomar_foto.config(**btn_image_style)
        self.btn_tomar_foto.pack(pady=20)

        image_cancelar_tk = self.master.get_image('cancelar', '', 150, 55)
        self.imagenes['cancelar'] = image_cancelar_tk
        self.btn_cancelar = tk.Button(
            self.frame_der, image=image_cancelar_tk, command=self.cancelar)
        self.btn_cancelar.config(**btn_continuar_style)
        self.btn_cancelar.pack(expand=True, pady=20)

        self.lb_imagen_registrar.pack_forget()
        self.btn_habilitar_camara.pack_forget()
        self.btn_skip.pack_forget()

    def capturar_imagen(self):
        modals = Modals(self)
        nombre = self.nombre_entrada.get().strip()

        if nombre == "":
            modals.alert(
                "El nombre es requerido. \nPor favor, inténtalo de nuevo.")
            return

        nombre = nombre.split()[0].upper()

        if buscar_usuario_por_nombre(nombre):
            modals.alert(
                "El nombre ya existe. \nPor favor, inténtalo de nuevo.")
            return

        with_face = self.app_instance.tomar_foto(
            Constants.URL_IMGS+"/users/"+nombre + ".jpg")

        if not with_face:
            modals.alert(
                "No se detectó tu rostro. \nPor favor, inténtalo de nuevo.")
            return

        self.app_instance.detener_camara()
        self.app_instance = None

        insert_user(nombre)

        self.lb_registrar.config(
            text=f"Hola ¡{nombre.upper()}!\n¡Bienvenido a Wika!")

        self.nombre_entrada.delete(0, tk.END)
        self.lb_ingresar_nombre.pack_forget()

        imagen_user_tk = self.master.get_image('usuario', nombre)
        self.imagenes['usuario'] = imagen_user_tk
        self.lb_imagen_registrar.config(image=imagen_user_tk)
        self.lb_imagen_registrar.pack(expand=True)

        self.nombre_entrada.pack_forget()

        image_registrar_otro_user_tk = self.master.get_image(
            'registrar_otro_usuario', '', 250, 70)
        self.imagenes['registrar_otro_usuario'] = image_registrar_otro_user_tk
        self.btn_habilitar_camara.config(image=image_registrar_otro_user_tk)
        self.btn_habilitar_camara.pack(pady=20)

        self.btn_registrado.pack(pady=20)
        self.btn_registrado.config(text="¿Desea cambiar sesión?")

        imagen_continuar_tk = self.master.get_image(
            'continuar', nombre, 160, 55)
        self.imagenes['continuar'] = imagen_continuar_tk
        self.btn_skip.config(image=imagen_continuar_tk)
        self.btn_skip.pack(expand=True, pady=20)

        self.btn_tomar_foto.pack_forget()
        self.btn_cancelar.pack_forget()

        modals.alert("¡Registro exitoso!\n¡Bienvenido a Wika!")

    def cancelar(self):
        if self.app_instance:
            self.app_instance.detener_camara()
            self.app_instance = None

        self.lb_imagen_registrar.pack(expand=True)
        self.btn_habilitar_camara.pack(pady=20)
        self.btn_registrado.pack(pady=20)
        self.btn_skip.pack(expand=True, pady=20)

        self.lb_registrar.config(
            text="Wika quiere conocerte:\n ¿Deseas registrarte?")

        self.lb_ingresar_nombre.pack_forget()
        self.nombre_entrada.pack_forget()
        self.btn_tomar_foto.pack_forget()
        self.btn_cancelar.pack_forget()

    def go_to_inicio(self):
        self.master.show_inicio_view()

    def go_to_categories(self):
        self.master.show_categories_view()
