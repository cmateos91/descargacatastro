import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
import sys
import os
import subprocess

class CatastroGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Descarga Catastro Automática")
        self.configure(bg="#f6f6f8")  # Fondo claro estilo Apple
        self.resizable(False, False)
        self.create_widgets()
        self.update_idletasks()
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.proc = None

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        # Apple-like style
        style.configure('TFrame', background="#f6f6f8")
        style.configure('TLabel', background="#f6f6f8", font=("San Francisco", 14))
        style.configure('TEntry', font=("San Francisco", 14), padding=8)
        style.configure('TButton', font=("San Francisco", 16, "bold"), padding=12, relief="flat", foreground="#fff", background="#007aff")
        style.map('TButton', background=[('active', '#0051a8')])

        # Título grande centrado
        title_label = ttk.Label(self, text="Descarga Catastro Automática", font=("San Francisco", 22, "bold"), background="#f6f6f8", foreground="#222")
        title_label.pack(pady=(28, 10), anchor="center")

        # Estado centrado bajo el título
        self.status = tk.StringVar()
        self.status.set("Rellena los campos y pulsa 'Iniciar descarga'")
        self.status_label = ttk.Label(self, textvariable=self.status, font=("San Francisco", 13), foreground="#007aff", background="#f6f6f8")
        self.status_label.pack(pady=(0, 18), anchor="center")

        # Frame central para el formulario y el botón
        form_frame = ttk.Frame(self, padding=24, style='TFrame')
        form_frame.pack(anchor="center", expand=True, pady=(0, 10))
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=2)

        # Etiquetas y campos alineados
        labels = [
            ("Provincia*", "provincia"),
            ("Municipio*", "municipio"),
            ("Vía (calle)*", "via"),
            ("Número*", "numero"),
            ("Bloque", "bloque"),
            ("Escalera", "escalera"),
            ("Planta", "planta"),
            ("Puerta", "puerta"),
        ]
        self.entries = {}
        for i, (label, var) in enumerate(labels):
            l = ttk.Label(form_frame, text=label, font=("San Francisco", 15), anchor="e", padding=(0, 4, 0, 4))
            l.grid(row=i, column=0, sticky=tk.E, pady=7, padx=(0, 10))
            entry = ttk.Entry(form_frame, font=("San Francisco", 15))
            entry.grid(row=i, column=1, pady=7, sticky=tk.EW, ipady=5)
            self.entries[var] = entry
        form_frame.rowconfigure(len(labels), minsize=18)

        # Botón principal centrado bajo los campos
        self.start_btn = ttk.Button(form_frame, text="Iniciar descarga", command=self.start_process, style='TButton')
        self.start_btn.grid(row=len(labels)+1, column=0, columnspan=2, pady=(30, 0), ipadx=30, ipady=6, sticky="ew")
        self.start_btn.configure(cursor="hand2")
        self.update_idletasks()
        # Sombra visual (no nativo, pero mejora el look)
        try:
            self.start_btn.master.configure(highlightbackground="#d3d3d3", highlightcolor="#d3d3d3", highlightthickness=2)
        except Exception:
            pass


    def start_process(self):
        # Validación básica
        for campo in ["provincia", "municipio", "via", "numero"]:
            if not self.entries[campo].get().strip():
                messagebox.showerror("Error", f"El campo '{campo.capitalize()}' es obligatorio.")
                return
        self.status.set("Ejecutando script... espera unos minutos")
        self.start_btn.config(state=tk.DISABLED)
        # Lanzar el script en un hilo para no bloquear la GUI
        Thread(target=self.run_script, daemon=True).start()

    def run_script(self):
        # Construir argumentos
        args = [sys.executable, os.path.join(os.path.dirname(__file__), "catastro_click.py")]
        args += [self.entries[k].get().strip() for k in ["provincia", "municipio", "via", "numero", "bloque", "escalera", "planta", "puerta"]]
        try:
            proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.proc = proc
            while True:
                line = proc.stdout.readline()
                if not line and proc.poll() is not None:
                    break
                if line:
                    self.status.set(line.strip())
            _, err = proc.communicate()
            if proc.returncode == 0:
                self.status.set("¡Descarga completada!")
                messagebox.showinfo("Éxito", "Descarga completada y archivos movidos.")
            else:
                self.status.set("Error en la descarga")
                messagebox.showerror("Error", f"Ha ocurrido un error:\n{err}")
        except Exception as e:
            self.status.set("Error ejecutando el script")
            messagebox.showerror("Error", str(e))
        finally:
            self.start_btn.config(state=tk.NORMAL)

    def on_closing(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
        self.destroy()

if __name__ == "__main__":
    app = CatastroGUI()
    app.mainloop()
