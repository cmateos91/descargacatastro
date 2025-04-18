from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import shutil
import glob
import tkinter as tk
from tkinter import filedialog

# Configuración de Selenium
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--headless=new')  # Navegador en segundo plano

# Carpeta de descargas temporal
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), 'descargas_temp')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
}
options.add_experimental_option("prefs", prefs)

# Opcional: para que el navegador no muestre mensajes innecesarios
chrome_options = options
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

import sys
# Permitir entrada por argumentos o por consola
if len(sys.argv) >= 9:
    provincia, municipio, via, numero, bloque, escalera, planta, puerta = sys.argv[1:9]
    print(f"Datos recibidos por argumentos: provincia={provincia}, municipio={municipio}, via={via}, numero={numero}, bloque={bloque}, escalera={escalera}, planta={planta}, puerta={puerta}")
else:
    print("Introduce los datos para la consulta catastral:")
    provincia = input("Provincia: ").strip()
    municipio = input("Municipio: ").strip()
    via = input("Vía (solo nombre, sin tipo): ").strip()
    numero = input("Número: ").strip()
    bloque = input("Bloque (vacío si no aplica): ").strip()
    escalera = input("Escalera (vacío si no aplica): ").strip()
    planta = input("Planta (vacío si no aplica): ").strip()
    puerta = input("Puerta (vacío si no aplica): ").strip()
print("\n--- Iniciando consulta automática... ---\n")

try:
    # Abre la web del catastro
    driver.get("https://www.sedecatastro.gob.es/")

    # Espera hasta que el elemento con la clase 'top-post-details' esté presente
    wait = WebDriverWait(driver, 15)
    elemento = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.top-post-details"))
    )

    # Haz clic en el elemento
    elemento.click()

    # Espera un poco para que el DOM se actualice tras el primer clic
    import time
    time.sleep(2)

    # Tras el primer clic, busca directamente en el primer iframe
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if len(iframes) > 0:
        driver.switch_to.frame(iframes[0])
        try:
            enlace_calle_numero = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[normalize-space(text())='CALLE/NÚMERO']"))
            )
            enlace_calle_numero.click()
            print("Hecho clic en CALLE/NÚMERO (primer iframe)")

            # Paso: escribir la provincia y pulsar ENTER
            from selenium.webdriver.common.keys import Keys
            campo_provincia = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ctl00_Contenido_provinceSelector"))
            )
            campo_provincia.clear()
            if provincia:
                for letra in provincia:
                    campo_provincia.send_keys(letra)
                    time.sleep(0.1)
                time.sleep(1)
                campo_provincia.send_keys(Keys.ENTER)
                print(f"Escrito '{provincia}' y pulsado ENTER para seleccionar la provincia.")
            else:
                print("Provincia vacía, campo limpiado.")

            # Paso: escribir municipio
            campo_municipio = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ctl00_Contenido_municipioSelector"))
            )
            campo_municipio.clear()
            if municipio:
                for letra in municipio:
                    campo_municipio.send_keys(letra)
                    time.sleep(0.1)
                time.sleep(1)
                campo_municipio.send_keys(Keys.ENTER)
                print(f"Escrito '{municipio}' y pulsado ENTER para seleccionar el municipio.")
            else:
                print("Municipio vacío, campo limpiado.")

            # Paso: escribir vía
            campo_via = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ctl00_Contenido_viaSelector"))
            )
            campo_via.clear()
            if via:
                for letra in via:
                    campo_via.send_keys(letra)
                    time.sleep(0.1)
                time.sleep(1)
                campo_via.send_keys(Keys.ENTER)
                print(f"Escrito '{via}' y pulsado ENTER para seleccionar la vía.")
            else:
                print("Vía vacía, campo limpiado.")

            # Paso: escribir número
            campo_numero = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ctl00_Contenido_txtNum"))
            )
            campo_numero.clear()
            if numero:
                for letra in numero:
                    campo_numero.send_keys(letra)
                    time.sleep(0.1)
                print(f"Escrito '{numero}' en el campo número.")
            else:
                print("Número vacío, campo limpiado.")
            time.sleep(1)

            # Paso: escribir bloque
            campo_bloque = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ctl00_Contenido_txtBlq"))
            )
            campo_bloque.clear()
            if bloque:
                for letra in bloque:
                    campo_bloque.send_keys(letra)
                    time.sleep(0.1)
                print(f"Escrito '{bloque}' en el campo bloque.")
            else:
                print("Bloque vacío, campo limpiado.")
            time.sleep(0.5)

            # Paso: escribir escalera
            campo_escalera = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ctl00_Contenido_txtEsc"))
            )
            campo_escalera.clear()
            if escalera:
                for letra in escalera:
                    campo_escalera.send_keys(letra)
                    time.sleep(0.1)
                print(f"Escrito '{escalera}' en el campo escalera.")
            else:
                print("Campo escalera dejado vacío.")
            time.sleep(0.5)

            # Paso: escribir planta
            campo_planta = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ctl00_Contenido_txtPlt"))
            )
            campo_planta.clear()
            if planta:
                for letra in planta:
                    campo_planta.send_keys(letra)
                    time.sleep(0.1)
                print(f"Escrito '{planta}' en el campo planta.")
            else:
                print("Campo planta dejado vacío.")
            time.sleep(0.5)

            # Paso: escribir puerta
            campo_puerta = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ctl00_Contenido_txtPrt"))
            )
            campo_puerta.clear()
            if puerta:
                for letra in puerta:
                    campo_puerta.send_keys(letra)
                    time.sleep(0.1)
                print(f"Escrito '{puerta}' en el campo puerta.")
            else:
                print("Campo puerta dejado vacío.")
            time.sleep(0.5)

            # Paso: pulsar el botón DATOS
            boton_datos = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ctl00_Contenido_btnDatos"))
            )
            boton_datos.click()
            print("Botón DATOS pulsado.")
            time.sleep(2)

            # Paso: hacer clic en 'Consulta Descriptiva y Gráfica' para descargar el archivo
            try:
                # Buscar el enlace <a> cuyo <span> tiene id 'ctl00_Contenido_lblConsulta'
                driver.switch_to.default_content()
                encontrado = False
                print("Buscando el enlace de 'Consulta Descriptiva y Gráfica' en el documento principal...")
                try:
                    # Busca el <a> que contiene el <span> con id 'ctl00_Contenido_lblConsulta'
                    enlace = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[span[@id='ctl00_Contenido_lblConsulta']]") )
                    )
                    driver.execute_script("arguments[0].scrollIntoView();", enlace)
                    driver.execute_script("arguments[0].click();", enlace)
                    print("¡Enlace 'Consulta Descriptiva y Gráfica' pulsado correctamente!")
                    encontrado = True
                    time.sleep(3)
                except Exception as e:
                    print("No se pudo hacer clic en el enlace 'Consulta Descriptiva y Gráfica' en el documento principal:", e)
                if not encontrado:
                    print("No se pudo encontrar ni pulsar el enlace 'Consulta Descriptiva y Gráfica' tras pulsar DATOS.")

                # Paso: pulsar en 'Cartografía'
                try:
                    enlace_cartografia = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[span[@id='ctl00_Contenido_lblCartografia']]"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView();", enlace_cartografia)
                    driver.execute_script("arguments[0].click();", enlace_cartografia)
                    print("¡Enlace 'Cartografía' pulsado correctamente!")
                    time.sleep(2)
                except Exception as e:
                    print("No se pudo hacer clic en el enlace 'Cartografía':", e)

                # Paso: pulsar en 'Cartografía Catastral'
                try:
                    enlace_carto_catastral = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[span[@id='ctl00_Contenido_lblMostrarCarto']]"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView();", enlace_carto_catastral)
                    driver.execute_script("arguments[0].click();", enlace_carto_catastral)
                    print("¡Enlace 'Cartografía Catastral' pulsado correctamente! (se abrirá una nueva pestaña)")
                    import time
                    time.sleep(2)

                    # Esperar hasta 5 segundos para detectar si se abre una nueva pestaña
                    ventanas_antes = driver.window_handles
                    for _ in range(5):
                        time.sleep(1)
                        ventanas_despues = driver.window_handles
                        if len(ventanas_despues) > len(ventanas_antes):
                            break
                    ventanas = driver.window_handles

                    if len(ventanas) > 1:
                        driver.switch_to.window(ventanas[-1])
                        print("Cambiado a la nueva pestaña del visor cartográfico.")
                    else:
                        print("No se detectó una nueva pestaña tras pulsar 'Cartografía Catastral'. Intentando abrir manualmente...")
                        try:
                            enlace_carto_catastral = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, "//a[span[@id='ctl00_Contenido_lblMostrarCarto']]"))
                            )
                            href = enlace_carto_catastral.get_attribute('href')
                            if href and href != 'javascript:void(0)' and href != '#':
                                driver.execute_script("window.open(arguments[0]);", href)
                                time.sleep(2)
                                ventanas = driver.window_handles
                                driver.switch_to.window(ventanas[-1])
                                print("Nueva pestaña abierta manualmente con href de Cartografía Catastral.")
                            else:
                                print("No se pudo obtener un href válido para abrir la pestaña manualmente.")
                        except Exception as e:
                            print("No se pudo abrir manualmente la pestaña de Cartografía Catastral:", e)

                    # Denegar cookies si aparece el botón
                    import time
                    try:
                        t0 = time.time()
                        boton_denegar = WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.cc-btn.cc-deny"))
                        )
                        driver.execute_script("arguments[0].click();", boton_denegar)
                        t1 = time.time()
                        print(f"Botón 'Denegar cookies' pulsado correctamente en la nueva pestaña. Tiempo de espera: {t1-t0:.2f} segundos.")
                        time.sleep(1)
                        # Pulsar el botón de imprimir
                        try:
                            boton_imprimir = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.ID, "IBImprimir"))
                            )
                            driver.execute_script("arguments[0].click();", boton_imprimir)
                            print("Botón de imprimir pulsado correctamente en el visor cartográfico.")
                            # Cambiar la escala a 1500
                            try:
                                campo_escala = WebDriverWait(driver, 5).until(
                                    EC.element_to_be_clickable((By.ID, "txtEscala"))
                                )
                                campo_escala.clear()
                                for letra in "1500":
                                    campo_escala.send_keys(letra)
                                    time.sleep(0.05)
                                print("Escala cambiada a 1500 en el visor cartográfico.")
                                print("Esperando un segundo para que se guarde la escala...")
                                time.sleep(1)
                                # Comprobar que la escala es 1500 antes de imprimir
                                valor_escala = campo_escala.get_attribute("value")
                                if valor_escala == "1500":
                                    print("¡Escala correctamente establecida en 1500!")
                                else:
                                    print(f"Advertencia: el valor de la escala es '{valor_escala}', no '1500'")
                                # Pulsar el botón de imprimir final para descargar
                                try:
                                    boton_imprimir_final = WebDriverWait(driver, 5).until(
                                        EC.element_to_be_clickable((By.ID, "ctl00_Contenido_bImprimir"))
                                    )
                                    driver.execute_script("arguments[0].click();", boton_imprimir_final)
                                    print("Botón de imprimir final pulsado correctamente para descargar el archivo.")
                                except Exception as e:
                                    print("No se pudo hacer clic en el botón de imprimir final:", e)
                            except Exception as e:
                                print("No se pudo cambiar la escala en el visor cartográfico:", e)
                        except Exception as e:
                            print("No se pudo hacer clic en el botón de imprimir en el visor cartográfico:", e)
                    except Exception as e:
                        print("No se pudo hacer clic en 'Denegar cookies' en la nueva pestaña:", e)
                except Exception as e:
                    print("No se pudo hacer clic en el enlace 'Cartografía Catastral':", e)
            except Exception as e:
                print("No se pudo hacer clic en 'Consulta Descriptiva y Gráfica':", e)
        except Exception as e:
            print("No se pudo hacer clic en CALLE/NÚMERO o escribir provincia/municipio/vía/número/bloque/escalera/planta/puerta o pulsar DATOS en el primer iframe:", e)
        finally:
            driver.switch_to.default_content()
    else:
        print("No se encontró ningún iframe tras el primer clic.")

    # Espera unos segundos para ver el resultado
    # Esperar a que terminen las descargas (máximo 15 segundos)
    print("Esperando a que terminen las descargas...")
    for _ in range(30):
        pdfs = glob.glob(os.path.join(DOWNLOAD_DIR, '*.pdf'))
        crdownload = glob.glob(os.path.join(DOWNLOAD_DIR, '*.crdownload'))
        if crdownload:
            time.sleep(0.5)
        else:
            if pdfs:
                break
            time.sleep(0.5)
    print(f"Descargas encontradas en '{DOWNLOAD_DIR}': {[os.path.basename(f) for f in glob.glob(os.path.join(DOWNLOAD_DIR, '*.pdf'))]}")

    # Pedir carpeta destino al usuario
    print("Abriendo ventana de selección de carpeta...")
    root = tk.Tk()
    root.withdraw()
    root.lift()
    root.attributes('-topmost', True)
    destino = filedialog.askdirectory(title="Selecciona la carpeta donde guardar los archivos descargados")
    root.destroy()
    print("Ventana de selección cerrada.")
    if destino:
        print(f"Moviendo archivos PDF a: {destino}")
        for pdf in glob.glob(os.path.join(DOWNLOAD_DIR, '*.pdf')):
            shutil.move(pdf, os.path.join(destino, os.path.basename(pdf)))
        print("¡Archivos movidos correctamente!")
    else:
        print("No se seleccionó carpeta destino. Los archivos permanecen en:", DOWNLOAD_DIR)
finally:
    driver.quit()
