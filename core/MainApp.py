import tkinter as tk
from PIL import Image, ImageTk

from view.UsersView import UsersView
from view.InicioView import InicioView
from view.CategoriesView import CategoriesView
from view.CreateAccountView import CreateAccountView
from view.SelectedParameterView import SelectedParameterView
from view.ParametersByCategoryView import ParametersByCategoryView
from view.ProgressByCategoryView import ProgressByCategoryView
from utils.Constants import Constants
from styles.Labels import lb_cargando_style


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        #self.attributes('-fullscreen', True)
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        #self.overrideredirect(True)

        self.current_view = None

        self.label_carga = tk.Label(self, text="Cargando...")
        self.label_carga.config(**lb_cargando_style)
        self.label_carga.pack(expand=True, fill=tk.BOTH)
        self.iniciar_carga()

    def show_inicio_view(self):
        if self.current_view is not None:
            self.current_view.destroy()
        self.current_view = InicioView(self)
        self.current_view.pack(expand=True, fill=tk.BOTH)

    def show_create_account_view(self):
        if self.current_view is not None:
            self.current_view.destroy()
        self.current_view = CreateAccountView(self)
        self.current_view.pack(expand=True, fill=tk.BOTH)

    def show_users_view(self):
        if self.current_view is not None:
            self.current_view.destroy()
        self.current_view = UsersView(self)
        self.current_view.pack(expand=True, fill=tk.BOTH)

    def show_categories_view(self):
        if self.current_view is not None:
            self.current_view.destroy()
        self.current_view = CategoriesView(self)
        self.current_view.pack(expand=True, fill=tk.BOTH)

    def show_category_selected_view(self, id_categoria, nombre_categoria):
        if self.current_view is not None:
            self.current_view.destroy()
        self.current_view = ParametersByCategoryView(
            self, id_categoria, nombre_categoria)
        self.current_view.pack(expand=True, fill=tk.BOTH)

    def show_selected_parameter_view(self, id_item, parametro, categoria, categoria_id):
        if self.current_view is not None:
            self.current_view.destroy()
        self.current_view = SelectedParameterView(
            self, id_item, parametro, categoria, categoria_id)
        self.current_view.pack(expand=True, fill=tk.BOTH)

    def show_progress_category_view(self, id_categoria, nombre_categoria):
        if self.current_view is not None:
            self.current_view.destroy()
        self.current_view = ProgressByCategoryView(
            self, id_categoria, nombre_categoria)
        self.current_view.pack(expand=True, fill=tk.BOTH)

    def get_image(self, referencia, parametro, ancho=None, alto=None):
        imagen = None

        if referencia == 'inicio':
            imagen = Image.open(Constants.URL_IMGS+'/wika.png')
        elif referencia == 'perfil':
            imagen = Image.open(Constants.URL_IMGS+'/perfil.png')
        elif referencia == 'usuario':
            imagen = Image.open(Constants.URL_IMGS +
                                '/users/' + parametro + '.jpg')
        elif referencia == 'undetected':
            imagen = Image.open(Constants.URL_IMGS + '/undetected.png')
        elif referencia == 'manos':
            imagen = Image.open(Constants.URL_IMGS+'/hands/' + parametro)
        elif referencia == 'vocales':
            imagen = Image.open(
                Constants.URL_IMGS+'/category_library/vocales/' + parametro + '.png')
        elif referencia == 'consonantes':
            imagen = Image.open(
                Constants.URL_IMGS+'/category_library/consonantes/' + parametro + '.png')
        elif referencia == 'numeros':
            imagen = Image.open(
                Constants.URL_IMGS+'/category_library/numeros/' + parametro + '.png')
        elif referencia == 'palabras':
            imagen = Image.open(
                Constants.URL_IMGS+'/category_library/palabras/' + parametro + '.png')
        elif referencia == 'regresar':
            imagen = Image.open(
                Constants.URL_IMGS+'/regresar.png')
        elif referencia == 'users':
            imagen = Image.open(
                Constants.URL_IMGS+'/users.png')
        elif referencia == 'registrarse':
            imagen = Image.open(
                Constants.URL_IMGS+'/registrarse.png')
        elif referencia == 'delete':
            imagen = Image.open(
                Constants.URL_IMGS+'/icon_borrar.png')
        elif referencia == 'iniciar_aprendizaje':
            imagen = Image.open(
                Constants.URL_IMGS+'/iniciar_aprendizaje.png')
        elif referencia == 'tomar_foto':
            imagen = Image.open(
                Constants.URL_IMGS+'/tomar_foto.png')
        elif referencia == 'deseo_registrarme':
            imagen = Image.open(
                Constants.URL_IMGS+'/deseo_registrarme.png')
        elif referencia == 'cancelar':
            imagen = Image.open(
                Constants.URL_IMGS+'/cancelar.png')
        elif referencia == 'omitir':
            imagen = Image.open(
                Constants.URL_IMGS+'/omitir.png')
        elif referencia == 'registrar_otro_usuario':
            imagen = Image.open(
                Constants.URL_IMGS+'/registrar_otro_usuario.png')
        elif referencia == 'continuar':
            imagen = Image.open(
                Constants.URL_IMGS+'/continuar.png')
        elif referencia == 'progreso':
            imagen = Image.open(
                Constants.URL_IMGS+'/progreso.png')

        if ancho and alto:
            imagen = imagen.resize((ancho, alto))
        imagen_tk = ImageTk.PhotoImage(imagen)
        self.imagen_inicio = imagen_tk

        return imagen_tk

    def iniciar_carga(self, i=0):
        if i <= 100:
            self.label_carga.config(text=f"Cargando... {i}%")
            # Cambio de 50 a 5
            self.after(5, lambda: self.iniciar_carga(i + 1))
        else:
            self.label_carga.destroy()
            self.show_inicio_view()

