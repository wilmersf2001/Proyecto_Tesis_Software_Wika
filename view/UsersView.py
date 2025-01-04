import tkinter as tk
from tkinter import ttk

from database.query.User import get_all_users, delete_user, delete_progress_by_user, get_user_auth
from database.query.Progress import get_progress_by_user
from styles.Buttons import btn_image_style
from styles.Labels import lb_seleccion_titulo_style
from utils.Modals import Modals
from utils.UtilFuctions import eliminar_user_directorio


class UsersView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.imagenes = {}
        self.users = get_all_users()
        self.user = get_user_auth()[1] if get_user_auth() else "invitado"
        self.progress = get_progress_by_user(
            get_user_auth()[0]) if get_user_auth() else 0

        self.frame_izq = tk.Frame(self, bg='#2196f3', width=180)
        self.frame_izq.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_izq.pack_propagate(False)

        self.frame_der = tk.Frame(self, bg='#fff')
        self.frame_der.pack(side=tk.RIGHT, fill=tk.BOTH,
                            expand=True)

        lb_titulo = tk.Label(self.frame_der,
                             text="LISTA DE USUARIOS REGISTRADOS")
        lb_titulo.config(**lb_seleccion_titulo_style)
        lb_titulo.pack(expand=True, pady=(10, 0))

        imagen_tk = self.master.get_image('regresar', '', 80, 80)
        self.imagenes['regresar'] = imagen_tk
        boton_regresar = tk.Button(
            self.frame_izq, image=imagen_tk, command=self.go_to_categories)
        boton_regresar.config(**btn_image_style)
        boton_regresar.pack(fill=tk.X, padx=50, pady=25)

        label_inferior = tk.Label(
            self.frame_izq, text=self.user)
        label_inferior.pack(side=tk.BOTTOM, padx=40, pady=25)

        if self.user != "invitado":
            self.progress_label = tk.Label(
                self.frame_izq, text=f"{self.progress}% del curso")
            self.progress_label.pack(side=tk.BOTTOM, padx=40, pady=5)

            self.progress_bar = ttk.Progressbar(
                self.frame_izq, orient="horizontal", length=150, mode="determinate")
            self.progress_bar.pack(side=tk.BOTTOM, padx=40, pady=5)
            self.update_progress_bar(self.progress)

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()

        style.configure("mystyle.Treeview",
                        highlightthickness=0,
                        bd=0,
                        font=('Calibri', 11))
        style.configure("mystyle.Treeview.Heading",
                        font=('Calibri', 13, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {
                     'sticky': 'nswe'})])

        self.tree = ttk.Treeview(self.frame_der, columns=(
            'ID', 'Nombre', 'Autenticado'), show='headings', style="mystyle.Treeview")

        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Autenticado', text='Autenticado')

        self.tree.column('ID', anchor=tk.CENTER)
        self.tree.column('Nombre', anchor=tk.CENTER)
        self.tree.column('Autenticado', anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree_items = []

        for i, user in enumerate(self.users):
            tree_id = self.tree.insert('', tk.END, values=user)
            self.tree_items.append(tree_id)

        self.tree.bind('<ButtonRelease-1>', self.show_modal_optiones)

    def show_modal_optiones(self, event):
        modals = Modals(self)
        selected_item = self.tree.selection()[0]
        item_values = self.tree.item(selected_item, 'values')
        user = {
            'id': item_values[0],
            'name': item_values[1],
            'authenticated': item_values[2]
        }
        result = modals.alert_options(user)

        if result:
            self.delete_usuario(selected_item, user)

    def delete_usuario(self, item, user):
        self.tree.delete(item)
        delete_user(user['id'])
        eliminar_user_directorio(user['name'])
        delete_progress_by_user(user['id'])

    def go_to_categories(self):
        self.master.show_categories_view()

    def update_progress_bar(self, progress):
        self.progress_bar['value'] = progress
