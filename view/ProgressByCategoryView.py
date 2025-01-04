import tkinter as tk
from tkinter import ttk

from database.query.User import get_user_auth
from database.query.Progress import get_progress_user_by_category, get_all_progress_by_user_and_category
from styles.Buttons import btn_image_style
from styles.Labels import lb_seleccion_titulo_style


class ProgressByCategoryView(tk.Frame):
    def __init__(self, master, id_categoria, nombre_categoria):
        super().__init__(master)
        self.master = master
        self.nombre_categoria = nombre_categoria
        self.id_categoria = id_categoria
        self.imagenes = {}
        self.user = get_user_auth()[1] if get_user_auth() else "invitado"
        self.progress_category = get_progress_user_by_category(
            get_user_auth()[0], self.id_categoria) if get_user_auth() else 0
        self.progress_by_category = get_all_progress_by_user_and_category(
            get_user_auth()[0], self.id_categoria) if get_user_auth() else []

        self.frame_izq = tk.Frame(self, bg='#2196f3', width=180)
        self.frame_izq.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_izq.pack_propagate(False)

        self.frame_der = tk.Frame(self, bg='#fff')
        self.frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        lb_titulo = tk.Label(self.frame_der,
                             text="TU PROGRESO EN LA CATEGORÍA DE\n" + f" {self.nombre_categoria} ")
        lb_titulo.config(**lb_seleccion_titulo_style)
        lb_titulo.pack(expand=True, pady=(10, 0))

        imagen_tk = self.master.get_image('regresar', '', 80, 80)
        self.imagenes['regresar'] = imagen_tk
        boton_regresar = tk.Button(
            self.frame_izq, image=imagen_tk, command=self.go_to_category_selected_view)
        boton_regresar.config(**btn_image_style)
        boton_regresar.pack(fill=tk.X, padx=50, pady=25)

        label_inferior = tk.Label(
            self.frame_izq, text=self.user)
        label_inferior.pack(side=tk.BOTTOM, padx=40, pady=25)

        if self.user != "invitado":
            self.progress_label = tk.Label(
                self.frame_izq, text=f"{self.progress_category}%\n" + " " + self.nombre_categoria.lower())
            self.progress_label.pack(side=tk.BOTTOM, padx=40, pady=5)

            self.progress_bar = ttk.Progressbar(
                self.frame_izq, orient="horizontal", length=150, mode="determinate")
            self.progress_bar.pack(side=tk.BOTTOM, padx=40, pady=5)
            self.update_progress_bar(self.progress_category)

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()

        style.configure("mystyle.Treeview",
                        highlightthickness=0,
                        bd=0,
                        font=('Calibri', 11))
        style.configure("mystyle.Treeview.Heading",
                        font=('Calibri', 12, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {
                     'sticky': 'nswe'})])

        self.tree = ttk.Treeview(self.frame_der, columns=(
            'Fecha de Aprendizaje', 'Nombre', 'Correctas', 'Incorrectas'), show='headings', style="mystyle.Treeview")

        self.tree.heading('Fecha de Aprendizaje', text='Fecha de Aprendizaje')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Correctas', text='Correctas')
        self.tree.heading('Incorrectas', text='Incorrectas')

        self.tree.column('Fecha de Aprendizaje', anchor=tk.CENTER, width=110)
        self.tree.column('Nombre', anchor=tk.CENTER, width=50)
        self.tree.column('Correctas', anchor=tk.CENTER, width=50)
        self.tree.column('Incorrectas', anchor=tk.CENTER, width=50)

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree_items = []

        for i, user in enumerate(self.progress_by_category):
            tree_id = self.tree.insert('', tk.END, values=user)
            self.tree_items.append(tree_id)

    def update_progress_bar(self, progress_category):
        self.progress_bar['value'] = progress_category

    def go_to_category_selected_view(self):
        self.master.show_category_selected_view(
            self.id_categoria, self.nombre_categoria)
