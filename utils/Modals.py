import tkinter as tk
from styles.Buttons import btn_cerrar_style, btn_cancel_style, btn_eliminar_style


class Modals:
    def __init__(self, ventana):
        self.ventana = ventana

    def alert(self, mensaje, tipo="error"):
        modal_window = tk.Toplevel(self.ventana)
        modal_window.title("Advertencia")
        modal_window.configure(bg="#2196f3")

        # Obtener el tamaño de la pantalla
        screen_width = self.ventana.winfo_screenwidth()
        screen_height = self.ventana.winfo_screenheight()

        # Obtener el tamaño de la ventana modal
        modal_width = 300
        modal_height = 150
        modal_window.overrideredirect(True)

        # Calcular la posición para centrar la ventana modal
        x = (screen_width - modal_width) // 2
        y = (screen_height - modal_height) // 2

        # Definir la geometría de la ventana modal
        modal_window.geometry(f"{modal_width}x{modal_height}+{x}+{y}")

        modal_frame = tk.Frame(modal_window, bg="#2196f3", padx=20, pady=20)
        modal_frame.pack()

        modal_label = tk.Label(
            modal_frame, text=mensaje, font=("Arial", 12, "bold"), bg="#2196f3", fg="white")
        modal_label.grid(row=0, column=0, padx=10, pady=10)

        close_button = tk.Button(
            modal_frame, text="Cerrar", command=modal_window.destroy)
        close_button.config(**btn_cerrar_style)
        close_button.grid(row=1, column=0, pady=10, sticky="ew")

    def alert_options(self, user):
        self.result = tk.BooleanVar()

        modal_window = tk.Toplevel(self.ventana)
        modal_window.title("Advertencia")
        modal_window.configure(bg="#2196f3")

        # Obtener el tamaño de la pantalla
        screen_width = self.ventana.winfo_screenwidth()
        screen_height = self.ventana.winfo_screenheight()

        # Obtener el tamaño de la ventana modal
        modal_width = 300
        modal_height = 150
        modal_window.overrideredirect(True)

        # Calcular la posición para centrar la ventana modal
        x = (screen_width - modal_width) // 2
        y = (screen_height - modal_height) // 2

        # Definir la geometría de la ventana modal
        modal_window.geometry(f"{modal_width}x{modal_height}+{x}+{y}")

        modal_frame = tk.Frame(modal_window, bg="#2196f3", padx=20, pady=20)
        modal_frame.pack()

        modal_label = tk.Label(
            modal_frame, text=f"¿Estás seguro de eliminar\n al usuario: {user['name']}?", font=("Arial", 12, "bold"), bg="#2196f3", fg="white")
        modal_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        close_button = tk.Button(
            modal_frame, text="Cerrar", command=lambda: self.set_result(modal_window, False))
        close_button.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="ew")

        delete_button = tk.Button(
            modal_frame, text="Eliminar", command=lambda: self.set_result(modal_window, True))
        delete_button.grid(row=1, column=1, padx=(5, 10), pady=10, sticky="ew")

        close_button.config(**btn_cancel_style)
        delete_button.config(**btn_eliminar_style)

        modal_window.wait_window(modal_window)
        return self.result.get()

    def set_result(self, window, value):
        self.result.set(value)
        window.destroy()
