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
    # Este User-Agent hace que el bot parezca una persona navegando
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        # Intento para Streamlit Cloud
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
    except:
        # Intento para tu PC (Vivobook)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

if st.button('Buscar Precios Ahora'):
    with st.spinner('Escaneando tiendas...'):
        driver = configurar_driver()
        # URL de búsqueda en HardGamers (el mejor agregador de Argentina)
        url = "https://www.hardgamers.com.ar/search?text=FGG+MAD+60"
        
        try:
            driver.get(url)
            time.sleep(5) # Tiempo para que cargue el JavaScript de la web
            
            # Buscamos los productos usando la clase que usa HardGamers
            items = driver.find_elements(By.CLASS_NAME, "product-list__item")
            
            results = []
            for item in items:
                try:
                    nombre = item.find_element(By.TAG_NAME, "h3").text
                    # Filtramos para que solo aparezca el MAD 60 y no cualquier cosa
                    if "MAD 60" in nombre.upper():
                        precio = item.find_element(By.CLASS_NAME, "actual-price").text
                        tienda = item.find_element(By.CLASS_NAME, "store-name").text
                        link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
                        
                        results.append({
                            "Tienda": tienda,
                            "Precio (Efec/Trans)": precio,
                            "Producto": nombre,
                            "Link": link
                        })
                except:
                    continue
            
            if results:
                df = pd.DataFrame(results)
                # Mostramos la tabla pro
                st.success(f"¡Se encontraron {len(results)} resultados!")
                st.dataframe(df, use_container_width=True)
                st.info("Nota: Los precios suelen ser por transferencia o efectivo.")
            else:
                st.warning("No se encontraron resultados exactos. Probá buscando más tarde.")
                
        except Exception as e:
            st.error(f"Hubo un error: {e}")
        finally:
            driver.quit()

st.divider()
st.caption("Hecho por Lauro para el setup de los pibes.")