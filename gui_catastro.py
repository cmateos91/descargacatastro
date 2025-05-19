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
        
        # Configuración de apariencia y tema
        ctk.set_appearance_mode("system")  # Claro/Oscuro automático
        ctk.set_default_color_theme("blue")
        
        # Variables necesarias
        self.entries = {}
        self.proc = None
        
        # Construir la interfaz
        self.build_ui()
        
        # Hacer responsive la ventana
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Ajustar el tamaño inicial de la ventana
        app_width = min(900, int(screen_width * 0.7))
        app_height = min(700, int(screen_height * 0.8))
        
        # Centrar en la pantalla
        x = (screen_width - app_width) // 2
        y = (screen_height - app_height) // 2
        self.geometry(f"{app_width}x{app_height}+{x}+{y}")
        
        # Tamaño mínimo para evitar problemas de visualización
        self.minsize(600, 550)
        
        # Configurar el manejador para cerrar la ventana
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def build_ui(self):
        # Crear un marco principal con padding
        main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cabecera con logo y título
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Logo decorativo con tamaño adaptativo
        logo_label = ctk.CTkLabel(header_frame, text="🇪🇸", font=("Arial", 40))
        logo_label.pack(side="left", padx=(0, 15))
        
        # Título principal
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Descarga Catastro Automática",
            font=("Arial Rounded MT Bold", 26)
        )
        title_label.pack(side="left", fill="x", expand=True)
        
        # Marco con capacidad de scroll para el contenido
        self.content_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, pady=10)
        
        # Mensaje de estado
        self.status = ctk.StringVar(value="Rellena los campos y pulsa 'Iniciar descarga'")
        status_label = ctk.CTkLabel(
            self.content_frame, 
            textvariable=self.status, 
            font=("Arial", 16), 
            text_color="gray"
        )
        status_label.pack(pady=(0, 15), fill="x")
        
        # Sección para Referencia Catastral
        rc_section = ctk.CTkFrame(self.content_frame, corner_radius=10)
        rc_section.pack(fill="x", pady=(0, 15), padx=5)
        
        # Título de sección de referencia catastral
        ctk.CTkLabel(
            rc_section, 
            text="Búsqueda por Referencia Catastral", 
            font=("Arial", 18, "bold"),
            anchor="w"
        ).pack(fill="x", padx=15, pady=(15, 10))
        
        # Descripción de uso
        ctk.CTkLabel(
            rc_section,
            text="Si conoces la Referencia Catastral, puedes buscar directamente con ella\ny se ignorarán los demás campos.", 
            font=("Arial", 14),
            justify="left"
        ).pack(fill="x", padx=15, pady=(0, 10))
        
        # Campo de referencia catastral
        self.add_entry(rc_section, "Referencia", "ref_catastral", font_size=16)
        
        # Sección de campos obligatorios
        obligatory_section = ctk.CTkFrame(self.content_frame, corner_radius=10)
        obligatory_section.pack(fill="x", pady=(0, 15), padx=5)
        
        # Título de sección obligatoria
        ctk.CTkLabel(
            obligatory_section, 
            text="Búsqueda por Dirección - Datos obligatorios", 
            font=("Arial", 18, "bold"),
            anchor="w"
        ).pack(fill="x", padx=15, pady=(15, 10))
        
        # Descripción de uso
        ctk.CTkLabel(
            obligatory_section,
            text="O si prefieres, busca por dirección postal rellenando estos campos:", 
            font=("Arial", 14),
            justify="left"
        ).pack(fill="x", padx=15, pady=(0, 10))
        
        # Campos obligatorios
        campos_obligatorios = [
            ("Provincia*", "provincia"),
            ("Municipio*", "municipio"),
            ("Vía (calle)*", "via"),
            ("Número*", "numero")
        ]
        
        for label, key in campos_obligatorios:
            self.add_entry(obligatory_section, label, key, font_size=16)
        
        # Sección de campos opcionales
        optional_section = ctk.CTkFrame(self.content_frame, corner_radius=10)
        optional_section.pack(fill="x", pady=(0, 15), padx=5)
        
        # Título de sección opcional
        ctk.CTkLabel(
            optional_section, 
            text="Dirección interna (opcional)", 
            font=("Arial", 18, "bold"),
            anchor="w"
        ).pack(fill="x", padx=15, pady=(15, 10))
        
        # Campos opcionales
        campos_internos = [
            ("Bloque", "bloque"),
            ("Escalera", "escalera"),
            ("Planta", "planta"),
            ("Puerta", "puerta")
        ]
        
        for label, key in campos_internos:
            self.add_entry(optional_section, label, key, font_size=16)
        
        # Sección de botones en un marco inferior
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 10))
        
        # Botón principal
        self.btn = ctk.CTkButton(
            button_frame, 
            text="⬇️ Iniciar descarga", 
            font=("Arial Rounded MT Bold", 18),
            height=50, 
            command=self.start_process,
            corner_radius=8
        )
        self.btn.pack(pady=5, fill="x")

    def add_entry(self, parent, label, key, font_size=16):
        # Marco para cada entrada con un diseño responsive
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=8, padx=10)
        
        # Etiqueta a la izquierda con ancho fijo
        label_widget = ctk.CTkLabel(
            frame, 
            text=label, 
            width=100, 
            anchor="w", 
            font=("Arial", font_size)
        )
        label_widget.pack(side="left")
        
        # Campo de entrada a la derecha, expandible
        entry = ctk.CTkEntry(
            frame, 
            font=("Arial", font_size), 
            height=35,
            corner_radius=6
        )
        entry.pack(side="left", fill="x", expand=True, padx=(10, 5))
        
        # Almacenar referencia al campo
        self.entries[key] = entry

    def start_process(self):
        # Determinar el modo de búsqueda
        ref_catastral = self.entries["ref_catastral"].get().strip()
        
        if ref_catastral:
            # Si hay referencia catastral, usarla para la búsqueda
            pass
        else:
            # Si no hay referencia catastral, validar campos para búsqueda por dirección
            for campo in ["provincia", "municipio", "via", "numero"]:
                if not self.entries[campo].get().strip():
                    messagebox.showerror("Error", f"Debe rellenar el campo '{campo.capitalize()}' o proporcionar una Referencia Catastral.")
                    return
        
        # Actualizar estado y desactivar botón
        self.status.set("⏳ Ejecutando script... espera unos minutos")
        self.btn.configure(state="disabled")
        
        # Mostrar ventana de log
        self.open_log_window()
        
        # Configurar cola de logs y empezar el proceso
        self.log_queue = queue.Queue()
        Thread(target=self.run_script_with_queue, daemon=True).start()
        self.after(100, self.process_log_queue)

    def run_script_with_queue(self):
        # Construir argumentos para el script
        args = [sys.executable, os.path.join(os.path.dirname(__file__), "catastro_click.py")]
        
        # Añadir referencia catastral como primer argumento adicional
        args.append(self.entries["ref_catastral"].get().strip())
        
        # Añadir el resto de los campos
        args += [self.entries[k].get().strip() for k in ["provincia", "municipio", "via", "numero", "bloque", "escalera", "planta", "puerta"]]
        
        try:
            # Ejecutar el proceso
            proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
            self.proc = proc

            # Función para capturar la salida del proceso
            def enqueue_output(pipe, q):
                for line in iter(pipe.readline, ''):
                    q.put(line.rstrip())
                pipe.close()

            # Lanzar hilos para capturar stdout y stderr
            t1 = threading.Thread(target=enqueue_output, args=(proc.stdout, self.log_queue))
            t2 = threading.Thread(target=enqueue_output, args=(proc.stderr, self.log_queue))
            t1.daemon = t2.daemon = True
            t1.start()
            t2.start()
            
            # Esperar a que termine el proceso
            proc.wait()
            t1.join()
            t2.join()

            # Actualizar interfaz según el resultado
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
            # Reactivar el botón
            self.btn.configure(state="normal")

    def show_error_dialog(self):
        # Crear ventana emergente de error
        win = ctk.CTkToplevel(self)
        win.title("Error Catastro")
        
        # Hacer que la ventana sea adaptable a diferentes tamaños de pantalla
        screen_width = self.winfo_screenwidth()
        error_width = min(700, int(screen_width * 0.8))
        error_height = 340
        
        # Centrar la ventana de error
        x = (screen_width - error_width) // 2
        y = (self.winfo_screenheight() - error_height) // 2
        win.geometry(f"{error_width}x{error_height}+{x}+{y}")
        
        # Asegurar que la ventana esté sobre otras
        win.lift()
        win.focus_force()
        win.attributes("-topmost", True)
        
        # Mensaje de error
        error_msg = "Ha ocurrido un error. Consulta el log.\nPulsa ENTER o acepta para reintentar."
        ctk.CTkLabel(
            win,
            text=error_msg,
            wraplength=error_width-60,
            font=("Arial", 22, "bold"),
            justify="center"
        ).pack(pady=(30, 20), padx=30)
        
        # Marco para botones
        btns = ctk.CTkFrame(win, fg_color="transparent")
        btns.pack(pady=20)
        
        # Botón para ir al Catastro
        ctk.CTkButton(
            btns,
            text="🌐 Ir al Catastro",
            font=("Arial", 18, "bold"),
            height=50,
            width=200,
            corner_radius=8,
            command=lambda: [webbrowser.open("https://www1.sedecatastro.gob.es/Cartografia/mapa.aspx?buscar=S"), win.destroy()]
        ).pack(side="left", padx=15)
        
        # Botón para reintentar
        ctk.CTkButton(
            btns,
            text="🔁 Reintentar",
            font=("Arial", 18, "bold"),
            height=50,
            width=200,
            corner_radius=8,
            command=win.destroy
        ).pack(side="left", padx=15)
        
        # Esperar hasta que se cierre la ventana
        self.wait_window(win)

        # Borrado inteligente de campos tras error
        borrar_internos = False
        try:
            # Busca en el log si hay alguna línea con 'direccion interna' o 'dirección interna' (con/sin acento)
            if hasattr(self, 'log_box') and self.log_box.winfo_exists():
                log = self.log_box.get("1.0", "end").lower()
                if ("direccion interna" in log) or ("dirección interna" in log):
                    borrar_internos = True
                if "referencia catastral" in log.lower():
                    self.entries["ref_catastral"].delete(0, "end")
                    return
            # También busca en el mensaje de error mostrado
            if ("direccion interna" in error_msg.lower()) or ("dirección interna" in error_msg.lower()):
                borrar_internos = True
        except Exception:
            pass
        
        # Borrar campos según el tipo de error
        if borrar_internos:
            for campo in ["bloque", "escalera", "planta", "puerta"]:
                self.entries[campo].delete(0, "end")
        else:
            # Si hay referencia catastral, limpiarla
            if self.entries["ref_catastral"].get().strip():
                self.entries["ref_catastral"].delete(0, "end")
            else:
                for campo in ["provincia", "municipio", "via", "numero"]:
                    self.entries[campo].delete(0, "end")

    def open_log_window(self):
        # Crear ventana de log
        self.log_win = ctk.CTkToplevel(self)
        self.log_win.title("Log de descarga Catastro")
        
        # Hacer la ventana de log adaptable
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        log_width = min(980, int(screen_width * 0.8))
        log_height = min(600, int(screen_height * 0.7))
        
        # Centrar la ventana de log
        x = (screen_width - log_width) // 2
        y = (screen_height - log_height) // 2
        self.log_win.geometry(f"{log_width}x{log_height}+{x}+{y}")
        
        # Área de texto para el log con scrollbar integrado
        self.log_box = ctk.CTkTextbox(self.log_win, font=("Consolas", 16), wrap="word")
        self.log_box.pack(expand=True, fill="both", padx=15, pady=15)
        self.log_box.insert("end", "--- Inicio del log ---\n")
        self.log_box.configure(state="disabled")

    def append_log(self, line):
        # Añadir líneas al log si la ventana existe
        if hasattr(self, "log_box") and self.log_box.winfo_exists():
            self.log_box.configure(state="normal")
            self.log_box.insert("end", line + "\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")

    def process_log_queue(self):
        # Procesar mensajes en la cola de log
        try:
            while True:
                line = self.log_queue.get_nowait()
                self.append_log(line)
        except queue.Empty:
            pass
        self.after(100, self.process_log_queue)

    def on_closing(self):
        # Manejar el cierre de la ventana
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
        self.destroy()


if __name__ == "__main__":
    app = CatastroAppModern()
    app.mainloop()