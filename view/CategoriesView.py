import tkinter as tk
from tkinter import ttk

from database.query.User import get_user_auth
from database.query.Progress import get_progress_by_user, get_progress_user_by_category
from database.query.Category import get_all_categories
from styles.Buttons import btn_image_style, btn_category_style, btn_registrarme_style


class CategoriesView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.imagenes = {}
        categorias = get_all_categories()
        self.user = get_user_auth()[1] if get_user_auth() else "invitado"
        self.user_id = get_user_auth()[0] if get_user_auth() else 0
        fila = 0
        col = 0
        self.progress = get_progress_by_user(
            get_user_auth()[0]) if get_user_auth() else 0

        self.frame_izq = tk.Frame(self, bg='#2196f3', width=180)
        self.frame_izq.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_izq.pack_propagate(False)

        self.frame_der = tk.Frame(self, bg='white')
        self.frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        boton_regresar = tk.Button(
            self.frame_izq, text="REGISTRARSE", command=self.go_to_create_account)
        boton_regresar.config(**btn_registrarme_style)
        boton_regresar.pack(fill=tk.X, padx=40, pady=25)

        label_inferior = tk.Label(
            self.frame_izq, text=self.user)
        label_inferior.pack(side=tk.BOTTOM, padx=40, pady=25)

        if self.user != "invitado":
            imagen_tk = self.master.get_image('users', '', 80, 80)
            self.imagenes['users'] = imagen_tk
            boton_regresar = tk.Button(
                self.frame_izq, image=imagen_tk, command=self.go_to_users)
            boton_regresar.config(**btn_image_style)
            boton_regresar.pack(fill=tk.X, padx=50, pady=25)

            self.progress_label = tk.Label(
                self.frame_izq, text=f"{self.progress}% del curso")
            self.progress_label.pack(side=tk.BOTTOM, padx=40, pady=5)

            self.progress_bar = ttk.Progressbar(
                self.frame_izq, orient="horizontal", length=150, mode="determinate")
            self.progress_bar.pack(side=tk.BOTTOM, padx=40, pady=5)
            self.update_progress_bar(self.progress)

        for i, (id_categoria, nombre_categoria) in enumerate(categorias):

            if (get_progress_user_by_category(self.user_id, id_categoria) == 100):
                imagen_tk = self.master.get_image(
                    nombre_categoria.lower(), nombre_categoria+"_complete", 200, 150)
            else:
                imagen_tk = self.master.get_image(
                    nombre_categoria.lower(), nombre_categoria, 200, 150)

            self.imagenes[nombre_categoria] = imagen_tk
            boton = tk.Button(self.frame_der, image=imagen_tk,
                              command=lambda id_categoria=id_categoria, nombre_categoria=nombre_categoria: self.go_to_category_selected_view(id_categoria, nombre_categoria))
            boton.config(**btn_category_style)
            boton.grid(row=fila, column=col, padx=5, pady=(10, 20))
            col += 1
            if col > 1:
                col = 0
                fila += 1

        for i in range(2):
            self.frame_der.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.frame_der.grid_columnconfigure(i, weight=1)

    def go_to_create_account(self):
        self.master.show_create_account_view()

    def go_to_users(self):
        self.master.show_users_view()

    def go_to_category_selected_view(self, id_categoria, nombre_categoria):
        self.master.show_category_selected_view(id_categoria, nombre_categoria)

    def update_progress_bar(self, progress):
        self.progress_bar['value'] = progress
