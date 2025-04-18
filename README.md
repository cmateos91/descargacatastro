# DescargaCatastro

**DescargaCatastro** es una herramienta automática en Python para descargar la cartografía catastral (planos y consulta descriptiva y gráfica) de la Sede Electrónica del Catastro de España, a partir de la dirección de un inmueble.

## Características principales
- Interfaz gráfica sencilla (Tkinter) para introducir los datos del inmueble.
- Automatización completa de la descarga usando Selenium.
- Descarga y mueve automáticamente los archivos PDF generados a una carpeta seleccionada por el usuario.
- Permite introducir los siguientes datos: provincia, municipio, vía (calle), número, bloque, escalera, planta y puerta.

## Requisitos
- Python 3.8 o superior
- Google Chrome instalado
- [ChromeDriver](https://chromedriver.chromium.org/) (se instala automáticamente con `webdriver_manager`)

### Dependencias Python
Instala las dependencias ejecutando:

```bash
pip install -r requirements.txt
```

Si no tienes `pip`, ejecuta primero:
```bash
python get-pip.py
```

#### Dependencias principales
- selenium
- webdriver_manager
- tkinter (incluido en la mayoría de instalaciones de Python)

## Uso

### 1. Ejecutar la interfaz gráfica

```bash
python gui_catastro.py
```

Introduce los datos requeridos y pulsa "Iniciar descarga". El proceso puede tardar unos minutos. Al finalizar, podrás elegir la carpeta destino para los archivos descargados.

### 2. Ejecución por consola (opcional)
También puedes ejecutar el script principal directamente:

```bash
python catastro_click.py
```

Se te pedirá introducir los datos por consola.

## Estructura del proyecto

- `gui_catastro.py`: Interfaz gráfica para el usuario.
- `catastro_click.py`: Script principal que automatiza la descarga usando Selenium.
- `descargas_temp/`: Carpeta temporal de descargas.
- `get-pip.py`: Instalador de pip (opcional, solo si no tienes pip).

## Notas y recomendaciones
- Asegúrate de tener conexión a Internet y permisos para instalar/controlar Chrome.
- El proceso puede fallar si la web del Catastro cambia su estructura o si hay bloqueos por parte de la web.
- Si tienes problemas con la descarga automática, prueba a actualizar Chrome y las dependencias de Python.

## Licencia
Proyecto personal para automatización. Uso bajo responsabilidad del usuario.

---

*Actualizado: 18 de abril de 2025*
