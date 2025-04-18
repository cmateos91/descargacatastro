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
        self.geometry("400x390")
        self.resizable(False, False)
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.proc = None

    def create_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Etiquetas y campos
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
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=3)
            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1, pady=3, sticky=tk.EW)
            self.entries[var] = entry
        frame.columnconfigure(1, weight=1)

        # Estado
        self.status = tk.StringVar()
        self.status.set("Rellena los campos y pulsa 'Iniciar descarga'")
        self.status_label = ttk.Label(self, textvariable=self.status, foreground="blue")
        self.status_label.pack(pady=(5, 0))

        # Botón principal
        self.start_btn = ttk.Button(self, text="Iniciar descarga", command=self.start_process)
        self.start_btn.pack(pady=15)

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
