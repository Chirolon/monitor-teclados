import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
import re

st.set_page_config(page_title="Lauro Ranking", page_icon="🏆")
st.title("🏆 Ranking de Precios: FGG MAD 60")
st.write("Ordenado del más barato al más caro.")

def limpiar_precio(texto_precio):
    # Borra todo lo que no sea un número
    numeros = re.sub(r'[^\d]', '', texto_precio)
    if numeros:
        # Si el precio trae centavos al final (00), se los sacamos para no inflar el número
        return int(numeros[:-2]) if numeros.endswith('00') else int(numeros)
    return 999999999 # Si no hay precio, lo manda al final del ranking

def configurar_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    try:
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
    except:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

TIENDAS = {
    "Portal Tech": {"url": "https://portaltech.com.ar/productos/teclado-fgg-mad60-60-magnetic-switch-amber-pro-black/", "clase": "js-price-display"},
    "Full H4rd": {"url": "https://www.fullh4rd.com.ar/prod/28555/teclado-fgg-mad60-60-magnetic-switch-amber-pro-black", "clase": "price-main"},
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
        status.text(f"Verificando {nombre}...")
        try:
            driver.get(info["url"])
            time.sleep(5)
            texto_precio = driver.find_element(By.CLASS_NAME, info["clase"]).text
            precio_limpio = limpiar_precio(texto_precio)
            
            resultados.append({
                "Tienda": nombre,
                "Precio Texto": texto_precio,
                "Precio Num": precio_limpio,
                "Link": info["url"]
            })
        except:
            continue # Si falla una tienda, sigue con la otra
        
        bar.progress((i + 1) / len(TIENDAS))
    
    driver.quit()
    status.text("¡Ranking generado!")
    
    if resultados:
        df = pd.DataFrame(resultados)
        # ACÁ ESTÁ LA MAGIA: Ordena por la columna numérica
        df = df.sort_values(by="Precio Num", ascending=True)
        
        # Mostramos solo las columnas que importan para que quede pro
        st.table(df[["Tienda", "Precio Texto", "Link"]])
        st.balloons()
    else:
        st.error("No se pudo obtener ningún precio. Chequeá los links manuales.")