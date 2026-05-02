import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Configuración de la página
st.set_page_config(page_title="Lauro Price Monitor", page_icon="🚀")

st.title("🚀 Monitor de Teclados: FGG MAD 60")
st.write("Buscando el mejor precio en tiempo real...")

def configurar_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    # User-Agent más real para evitar bloqueos
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
    except:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

if st.button('Buscar Precios Ahora'):
    with st.spinner('Escaneando tiendas de Argentina...'):
        driver = configurar_driver()
        # Buscamos en HardGamers
        url = "https://www.hardgamers.com.ar/search?text=FGG+MAD+60"
        
        try:
            driver.get(url)
            # Aumentamos el tiempo a 10 segundos porque la nube es más lenta
            time.sleep(10) 
            
            # Buscamos los elementos de los productos
            items = driver.find_elements(By.CLASS_NAME, "product-list__item")
            
            results = []
            for item in items:
                try:
                    nombre = item.find_element(By.TAG_NAME, "h3").text
                    # Filtro menos estricto para encontrar más variantes
                    if "MAD" in nombre.upper():
                        precio = item.find_element(By.CLASS_NAME, "actual-price").text
                        tienda = item.find_element(By.CLASS_NAME, "store-name").text
                        link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
                        
                        results.append({
                            "Tienda": tienda,
                            "Precio (Efectivo)": precio,
                            "Producto": nombre,
                            "Link": link
                        })
                except:
                    continue
            
            if results:
                df = pd.DataFrame(results)
                st.success(f"¡Se encontraron {len(results)} resultados!")
                st.dataframe(df, use_container_width=True)
                st.info("Nota: Hacé clic en los links para ir a la tienda.")
            else:
                st.warning("No se encontraron resultados. Puede que HardGamers esté bloqueando el bot o no haya stock.")
                # Botón de auxilio: link directo
                st.markdown(f"[Hacé clic acá para ver la búsqueda manual]({url})")
                
        except Exception as e:
            st.error(f"Hubo un error técnico: {e}")
        finally:
            driver.quit()

st.divider()
st.caption("Desarrollado por Paola Leal - 2026")