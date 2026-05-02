import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
import re

# Configuración visual
st.set_page_config(page_title="Lauro Hyper-Monitor", page_icon="🏆")

st.title("🏆 Ranking de Precios: FGG MAD 60")
st.write("Buscando el mejor precio para el setup...")

def limpiar_precio(texto_precio):
    # Deja solo los números
    numeros = re.sub(r'[^\d]', '', texto_precio)
    if numeros:
        # Si termina en 00 (centavos), se los sacamos para comparar bien
        return int(numeros[:-2]) if numeros.endswith('00') else int(numeros)
    return 999999999

def configurar_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
    except:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Diccionario de tiendas (agregá o sacá según necesites)
TIENDAS = {
    "Portal Tech": {"url": "https://portaltech.com.ar/productos/teclado-fgg-mad60-60-magnetic-switch-amber-pro-black/", "clase": "js-price-display"},
    "Gamer 24hs": {"url": "https://gamer24hs.com.ar/productos/teclado-fgg-mad60-magnetic-switch/", "clase": "js-price-display"},
    "Venex": {"url": "https://www.venex.com.ar/index.php?query=MAD60", "clase": "current-price"},
    "Mexx": {"url": "https://www.mexx.com.ar/buscar/?p=MAD60", "clase": "price-main"}
}

if st.button('Generar Ranking de Precios'):
    resultados = []
    bar = st.progress(0)
    status = st.empty()
    driver = configurar_driver()
    
    for i, (nombre, info) in enumerate(TIENDAS.items()):
        status.text(f"Consultando en {nombre}...")
        try:
            driver.set_page_load_timeout(20)
            driver.get(info["url"])
            time.sleep(5)
            
            texto_precio = driver.find_element(By.CLASS_NAME, info["clase"]).text
            precio_num = limpiar_precio(texto_precio)
            
            resultados.append({
                "Tienda": nombre,
                "Precio": texto_precio,
                "Valor": precio_num,
                "Link": info["url"]
            })
        except:
            continue
        
        bar.progress((i + 1) / len(TIENDAS))
    
    driver.quit()
    status.text("¡Ranking listo!")
    
    if resultados:
        df = pd.DataFrame(resultados)
        # Ordenar del más barato al más caro
        df = df.sort_values(by="Valor", ascending=True)
        st.table(df[["Tienda", "Precio", "Link"]])
        st.balloons()
    else:
        st.warning("No se pudo obtener ningún precio. Probá más tarde.")

# SECCIÓN DE MÚSICA
st.divider()

if st.button('Nati'):
    try:
        audio_file = open('manteca.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
        st.success("Sonando: Manteca - Shinzo 🎶")
    except FileNotFoundError:
        st.error("Error: Tenés que subir el archivo 'manteca.mp3' a tu GitHub para que esto funcione.")