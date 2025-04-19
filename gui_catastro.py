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
        # Abrir ventana de log
        self.open_log_window()
        # Inicializa la cola de log
        import queue
        self.log_queue = queue.Queue()
        # Lanzar el script en un hilo para no bloquear la GUI
        Thread(target=self.run_script_with_queue, daemon=True).start()
        self.after(100, self.process_log_queue)

    def run_script_with_queue(self):
        import queue
        args = [sys.executable, os.path.join(os.path.dirname(__file__), "catastro_click.py")]
        args += [self.entries[k].get().strip() for k in ["provincia", "municipio", "via", "numero", "bloque", "escalera", "planta", "puerta"]]
        try:
            proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
            self.proc = proc
            import threading
            def enqueue_output(pipe, q):
                for line in iter(pipe.readline, ''):
                    q.put(line.rstrip())
                pipe.close()
            # Lanza hilos para leer stdout y stderr
            t1 = threading.Thread(target=enqueue_output, args=(proc.stdout, self.log_queue))
            t2 = threading.Thread(target=enqueue_output, args=(proc.stderr, self.log_queue))
            t1.daemon = t2.daemon = True
            t1.start()
            t2.start()
            proc.wait()
            t1.join()
            t2.join()
            if proc.returncode == 0:
                self.log_queue.put("¡Descarga completada!")
                self.status.set("¡Descarga completada!")
                messagebox.showinfo("Éxito", "Descarga completada y archivos movidos.")
            else:
                self.log_queue.put("Error en la descarga")
                self.status.set("Error en la descarga")
                messagebox.showerror("Error", "Ha ocurrido un error. Consulta el log para más detalles.")
        except Exception as e:
            self.log_queue.put(f"Error ejecutando el script: {e}")
            self.status.set("Error ejecutando el script")
            messagebox.showerror("Error", str(e))
        finally:
            self.start_btn.config(state=tk.NORMAL)

    def process_log_queue(self):
        # Procesa la cola y actualiza el log en la ventana
        if hasattr(self, 'log_queue'):
            import queue
            try:
                while True:
                    line = self.log_queue.get_nowait()
                    self.append_log(line)
            except queue.Empty:
                pass
        self.after(100, self.process_log_queue)

    def open_log_window(self):
        # Crea una ventana de log si no existe
        if hasattr(self, 'log_window') and self.log_window.winfo_exists():
            self.log_window.lift()
            return
        self.log_window = tk.Toplevel(self)
        self.log_window.title("Log de descarga Catastro")
        self.log_window.geometry("900x500")
        # Scrollbar
        scrollbar = tk.Scrollbar(self.log_window)
        scrollbar.pack(side="right", fill="y")
        # Text widget con estilo
        self.log_text = tk.Text(
            self.log_window,
            wrap="word",
            font=("Consolas", 16),
            bg="#23272e",
            fg="#ffffff",
            insertbackground="#ffffff",
            yscrollcommand=scrollbar.set
        )
        self.log_text.pack(expand=True, fill="both")
        scrollbar.config(command=self.log_text.yview)
        self.log_text.insert("end", "--- Inicio del log ---\n")
        self.log_text.see("end")
        self.log_window.focus()

    def append_log(self, text):
        # Añade texto al log en la ventana
        if hasattr(self, 'log_text') and self.log_text.winfo_exists():
            self.log_text.insert("end", text + "\n")
            self.log_text.see("end")

    def on_closing(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
        self.destroy()

if __name__ == "__main__":
    app = CatastroGUI()
    app.mainloop()
