import tkinter as tk
from tkinter import ttk

from database.query.User import get_user_auth
from database.query.Item import get_items_by_category
from database.query.Progress import get_progress_user_by_category, exist_parameter_in_progress_user
from styles.Buttons import btn_image_style, btn_continuar_style


class ParametersByCategoryView(tk.Frame):
    def __init__(self, master, id_categoria, nombre_categoria):
        super().__init__(master)
        self.master = master
        self.nombre_categoria = nombre_categoria
        self.id_categoria = id_categoria
        items = get_items_by_category(self.id_categoria)
        self.imagenes = {}
        self.user = get_user_auth()[1] if get_user_auth() else "invitado"
        self.user_id = get_user_auth()[0] if get_user_auth() else 0
        self.progress_category = get_progress_user_by_category(
            get_user_auth()[0], self.id_categoria) if get_user_auth() else 0

        self.frame_izq = tk.Frame(self, bg='#2196f3', width=180)
        self.frame_izq.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_izq.pack_propagate(False)

        self.frame_der = tk.Frame(self, bg='#fff')
        self.frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        imagen_tk = self.master.get_image('regresar', '', 80, 80)
        self.imagenes['regresar'] = imagen_tk
        boton_regresar = tk.Button(
            self.frame_izq, image=imagen_tk, command=self.go_to_categories)
        boton_regresar.config(**btn_image_style)
        boton_regresar.pack(fill=tk.X, padx=50, pady=25)

        numero_columnas = self.get_number_columns(self.id_categoria)

        width, height = self.get_witdh_height(self.id_categoria)

        label_inferior = tk.Label(
            self.frame_izq, text=self.user)
        label_inferior.pack(side=tk.BOTTOM, padx=40, pady=25)

        if self.user != "invitado":
            imagen_tk = self.master.get_image('progreso', '', 80, 80)
            self.imagenes['progreso'] = imagen_tk
            boton_regresar = tk.Button(
                self.frame_izq, image=imagen_tk, command=self.go_to_progress_category_view)
            boton_regresar.config(**btn_image_style)
            boton_regresar.pack(fill=tk.X, padx=50, pady=25)

            self.progress_label = tk.Label(
                self.frame_izq, text=f"{self.progress_category}%\n" + " " + self.nombre_categoria.lower())
            self.progress_label.pack(side=tk.BOTTOM, padx=40, pady=5)

            self.progress_bar = ttk.Progressbar(
                self.frame_izq, orient="horizontal", length=150, mode="determinate")
            self.progress_bar.pack(side=tk.BOTTOM, padx=40, pady=5)
            self.update_progress_bar(self.progress_category)

        for i, (id_item, parametro, categoria, categoria_id) in enumerate(items):
            row = i // numero_columnas
            col = i % numero_columnas

            if (exist_parameter_in_progress_user(
                    self.user_id, id_item)):
                imagen_tk = self.master.get_image(
                    categoria.lower(), f"parametros/opacidad/{parametro}", width, height)
            else:
                imagen_tk = self.master.get_image(
                    categoria.lower(), f"parametros/sin_opacidad/{parametro}", width, height)

            self.imagenes[parametro] = imagen_tk
            boton = tk.Button(self.frame_der, image=imagen_tk,
                              command=lambda id_item=id_item, parametro=parametro, categoria=categoria, categoria_id=categoria_id: self.go_to_selected_parameter_view(id_item, parametro, categoria, categoria_id))
            boton.config(**btn_continuar_style)

            boton.grid(row=row, column=col, padx=5, pady=(10, 20))

        for i in range(items.__len__() // numero_columnas + 1):
            self.frame_der.grid_rowconfigure(i, weight=1)
        for i in range(numero_columnas):
            self.frame_der.grid_columnconfigure(i, weight=1)

    def go_to_categories(self):
        self.master.show_categories_view()

    def go_to_selected_parameter_view(self, id_item, parametro, categoria, categoria_id):
        self.master.show_selected_parameter_view(
            id_item, parametro, categoria, categoria_id)

    def go_to_progress_category_view(self):
        self.master.show_progress_category_view(
            self.id_categoria, self.nombre_categoria)

    def get_number_columns(self, id_categoria):
        if id_categoria == 1:
            return 3
        return 4

    def get_witdh_height(self, categoria_id):
        if categoria_id == 1:
            return 150, 150
        elif categoria_id == 2:
            return 100, 100
        elif categoria_id == 3:
            return 60, 60
        else:
            return 100, 50

    def update_progress_bar(self, progress_category):
        self.progress_bar['value'] = progress_category
