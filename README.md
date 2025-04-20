# DescargaCatastro

**DescargaCatastro** es una herramienta automática y accesible en Python para descargar la cartografía catastral (planos y consulta descriptiva y gráfica) de la Sede Electrónica del Catastro de España, a partir de la dirección o la referencia catastral de un inmueble.

---

## 🐍 Instalación de Python y dependencias (para principiantes)

### 1. Instalar Python y pip
- Ve a la web oficial: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- Haz clic en el botón amarillo **Download Python** (elige la versión recomendada).
- Haz doble clic en el archivo descargado.
- **¡IMPORTANTE!** Marca la casilla `Add Python to PATH` antes de pulsar "Install Now".
  - ![add python to path](https://docs.python.org/3/_images/win_installer.png)
- Pulsa "Install Now" y espera a que termine.

#### Comprobar instalación
Abre el menú Inicio, busca "cmd" y ábrelo. Escribe:
```bash
python --version
```
Deberías ver algo como `Python 3.10.0` (el número puede variar).

Ahora prueba pip:
```bash
pip --version
```
Si ves un número de versión, ¡ya tienes pip!

#### ¿No tienes pip?
- Descarga este archivo: [get-pip.py](https://bootstrap.pypa.io/get-pip.py)
- Guárdalo en tu escritorio.
- Abre la consola (cmd), navega hasta el escritorio y ejecuta:
```bash
python get-pip.py
```

### 2. Instalar las dependencias del programa
Abre la consola y ejecuta, una a una:
```bash
pip install selenium
pip install webdriver_manager
pip install customtkinter
pip install darkdetect
```
> **Nota:** `tkinter` ya viene incluido en la mayoría de instalaciones de Python. Si tienes problemas, busca cómo instalarlo según tu sistema operativo.

### 3. Otros requisitos
- Google Chrome instalado
- [ChromeDriver](https://chromedriver.chromium.org/) (se instala automáticamente con `webdriver_manager`)

---

## Características principales
- Interfaz gráfica moderna y accesible (CustomTkinter), con fuentes grandes y diseño adaptado para personas mayores.
- Permite buscar por **referencia catastral** (con botón "Pegar" para copiar fácilmente) o por dirección completa.
- Automatización completa de la descarga usando Selenium.
- Descarga y mueve automáticamente los archivos PDF generados a una carpeta seleccionada por el usuario.
- Manejo inteligente de errores: solo se borran los campos relevantes según el tipo de error.
- Botones y diálogos grandes, siempre visibles y en primer plano.
- Soporte completo para campos: provincia, municipio, vía (calle), número, bloque, escalera, planta, puerta y referencia catastral.

## Requisitos
- Python 3.8 o superior
- Google Chrome instalado
- [ChromeDriver](https://chromedriver.chromium.org/) (se instala automáticamente con `webdriver_manager`)

### Dependencias Python
- selenium
- webdriver_manager
- customtkinter
- darkdetect
- tkinter (incluido en la mayoría de instalaciones de Python)

## Uso

### 1. Ejecutar la interfaz gráfica

```bash
python gui_catastro.py
```

- Introduce la **referencia catastral** o los datos de dirección.
- Pulsa "Iniciar descarga". El proceso puede tardar unos minutos.
- Al finalizar, podrás elegir la carpeta destino para los archivos descargados.
- Si ocurre un error, la ventana de aviso aparecerá en primer plano y solo tendrás que corregir los campos relevantes.

### 2. Ejecución por consola (opcional)
También puedes ejecutar el script principal directamente:

```bash
python catastro_click.py
```

Se te pedirá introducir los datos por consola.

## Estructura del proyecto

- `gui_catastro.py`: Interfaz gráfica moderna y accesible para el usuario.
- `catastro_click.py`: Script principal que automatiza la descarga usando Selenium.
- `descargas_temp/`: Carpeta temporal de descargas.
- `requirements.txt`: Lista de dependencias Python.
- `get-pip.py`: Instalador de pip (opcional, solo si no tienes pip).

## Notas y recomendaciones
- Asegúrate de tener conexión a Internet y permisos para instalar/controlar Chrome.
- El proceso puede fallar si la web del Catastro cambia su estructura o si hay bloqueos por parte de la web.
- Si tienes problemas con la descarga automática, prueba a actualizar Chrome y las dependencias de Python.
- Si usas Windows y tienes problemas con la ventana, asegúrate de tener los drivers de gráficos actualizados.

## Licencia
Proyecto personal para automatización. Uso bajo responsabilidad del usuario.

---

*Actualizado: 20 de abril de 2025*
