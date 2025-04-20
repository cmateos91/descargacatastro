import customtkinter as ctk
import subprocess
import os
import sys
import queue
import threading
from threading import Thread
from tkinter import messagebox
import webbrowser

class CatastroAppModern(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Descarga Catastro Automática")
        # No establecer geometry fijo
        ctk.set_appearance_mode("system")  # Claro/Oscuro automático
        ctk.set_default_color_theme("blue")

        self.entries = {}
        self.proc = None

        self.build_ui()
        self.update_idletasks()  # Asegura que todo está renderizado
        # Ajusta la ventana al tamaño mínimo necesario para mostrar todo
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        self.geometry(f"{width}x{height}")
        self.minsize(width, height)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def build_ui(self):
        # Logo decorativo (🇪🇸)
        ctk.CTkLabel(self, text="🇪🇸", font=("Arial", 60)).pack(pady=(10, 0))

        # Título
        ctk.CTkLabel(self, text="Descarga Catastro Automática",
                     font=("Arial Rounded MT Bold", 34)).pack(pady=(10, 16))

        self.status = ctk.StringVar(value="Rellena los campos y pulsa 'Iniciar descarga'")
        ctk.CTkLabel(self, textvariable=self.status, font=("Arial", 22), text_color="gray").pack(pady=(0, 8))

        self.form = ctk.CTkFrame(self, corner_radius=16)
        self.form.pack(padx=30, pady=20, fill="both", expand=False)

        campos_obligatorios = [("Provincia*", "provincia"),
                               ("Municipio*", "municipio"),
                               ("Vía (calle)*", "via"),
                               ("Número*", "numero")]

        for label, key in campos_obligatorios:
            self.add_entry(self.form, label, key, font_size=22)

        ctk.CTkLabel(self.form, text="Dirección interna (opcional)", font=("Arial", 20, "bold")).pack(pady=(26, 14))

        campos_internos = [("Bloque", "bloque"),
                           ("Escalera", "escalera"),
                           ("Planta", "planta"),
                           ("Puerta", "puerta")]

        for label, key in campos_internos:
            self.add_entry(self.form, label, key, font_size=20)

        # Botón principal
        self.btn = ctk.CTkButton(self, text="⬇️ Iniciar descarga", font=("Arial Rounded MT Bold", 28),
                                 height=70, command=self.start_process)
        self.btn.pack(pady=35)

    def add_entry(self, parent, label, key, font_size=22):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=10, padx=14)
        ctk.CTkLabel(frame, text=label, width=170, anchor="w", font=("Arial", font_size)).pack(side="left")
        entry = ctk.CTkEntry(frame, font=("Arial", font_size), height=38)
        entry.pack(side="left", fill="x", expand=True, padx=(10, 0))
        self.entries[key] = entry

    def start_process(self):
        for campo in ["provincia", "municipio", "via", "numero"]:
            if not self.entries[campo].get().strip():
                messagebox.showerror("Error", f"El campo '{campo.capitalize()}' es obligatorio.")
                return

        self.status.set("⏳ Ejecutando script... espera unos minutos")
        self.btn.configure(state="disabled")
        self.open_log_window()
        self.log_queue = queue.Queue()
        Thread(target=self.run_script_with_queue, daemon=True).start()
        self.after(100, self.process_log_queue)

    def run_script_with_queue(self):
        args = [sys.executable, os.path.join(os.path.dirname(__file__), "catastro_click.py")]
        args += [self.entries[k].get().strip() for k in ["provincia", "municipio", "via", "numero", "bloque", "escalera", "planta", "puerta"]]
        try:
            proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
            self.proc = proc

            def enqueue_output(pipe, q):
                for line in iter(pipe.readline, ''):
                    q.put(line.rstrip())
                pipe.close()

            t1 = threading.Thread(target=enqueue_output, args=(proc.stdout, self.log_queue))
            t2 = threading.Thread(target=enqueue_output, args=(proc.stderr, self.log_queue))
            t1.daemon = t2.daemon = True
            t1.start()
            t2.start()
            proc.wait()
            t1.join()
            t2.join()

            if proc.returncode == 0:
                self.log_queue.put("✅ ¡Descarga completada!")
                self.status.set("✅ ¡Descarga completada!")
                messagebox.showinfo("Éxito", "Descarga completada y archivos movidos.")
            else:
                self.log_queue.put("❌ Error en la descarga")
                self.status.set("❌ Error. Pulsa ENTER o acepta para reintentar.")
                self.show_error_dialog()

        except Exception as e:
            self.log_queue.put(f"⚠️ Error ejecutando el script: {e}")
            self.status.set("⚠️ Error ejecutando el script")
            messagebox.showerror("Error", str(e))
        finally:
            self.btn.configure(state="normal")

    def show_error_dialog(self):
        win = ctk.CTkToplevel(self)
        win.title("Error Catastro")
        win.geometry("700x340")
        win.lift()
        win.focus_force()
        win.attributes("-topmost", True)
        error_msg = "Ha ocurrido un error. Consulta el log.\nPulsa ENTER o acepta para reintentar."
        ctk.CTkLabel(
            win,
            text=error_msg,
            wraplength=660,
            font=("Arial", 28, "bold"),
            justify="center"
        ).pack(pady=(38, 22), padx=32)
        btns = ctk.CTkFrame(win, fg_color="transparent")
        btns.pack(pady=24)
        ctk.CTkButton(
            btns,
            text="🌐 Ir al Catastro",
            font=("Arial", 24, "bold"),
            height=60,
            width=240,
            command=lambda: [webbrowser.open("https://www1.sedecatastro.gob.es/Cartografia/mapa.aspx?buscar=S"), win.destroy()]
        ).pack(side="left", padx=30)
        ctk.CTkButton(
            btns,
            text="🔁 Reintentar",
            font=("Arial", 24, "bold"),
            height=60,
            width=240,
            command=win.destroy
        ).pack(side="left", padx=30)
        self.wait_window(win)

        # --- Restaurar lógica de borrado inteligente tras error ---
        borrar_internos = False
        try:
            # Busca en el log si hay alguna línea con 'direccion interna' o 'dirección interna' (con/sin acento)
            if hasattr(self, 'log_box') and self.log_box.winfo_exists():
                log = self.log_box.get("1.0", "end").lower()
                if ("direccion interna" in log) or ("dirección interna" in log):
                    borrar_internos = True
            # También busca en el mensaje de error mostrado
            if ("direccion interna" in error_msg.lower()) or ("dirección interna" in error_msg.lower()):
                borrar_internos = True
        except Exception:
            pass
        if borrar_internos:
            for campo in ["bloque", "escalera", "planta", "puerta"]:
                self.entries[campo].delete(0, "end")
        else:
            for campo in ["provincia", "municipio", "via", "numero"]:
                self.entries[campo].delete(0, "end")

    def open_log_window(self):
        self.log_win = ctk.CTkToplevel(self)
        self.log_win.title("Log de descarga Catastro")
        self.log_win.geometry("980x600")
        self.log_box = ctk.CTkTextbox(self.log_win, font=("Consolas", 22), wrap="word")
        self.log_box.pack(expand=True, fill="both", padx=20, pady=20)
        self.log_box.insert("end", "--- Inicio del log ---\n")
        self.log_box.configure(state="disabled")

    def append_log(self, line):
        if hasattr(self, "log_box") and self.log_box.winfo_exists():
            self.log_box.configure(state="normal")
            self.log_box.insert("end", line + "\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")

    def process_log_queue(self):
        try:
            while True:
                line = self.log_queue.get_nowait()
                self.append_log(line)
        except queue.Empty:
            pass
        self.after(100, self.process_log_queue)

    def on_closing(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
        self.destroy()


if __name__ == "__main__":
    app = CatastroAppModern()
    app.mainloop()
