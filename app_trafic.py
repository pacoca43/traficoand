import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Monitor DGT", layout="wide")
st.title("📍 Monitor de Tráfico DGT (Seguro)")

# Intentaremos obtener el feed desde la página pública de datos
URL_BASE = "https://infocar.dgt.es/datex2/lod/dgt/"

@st.cache_data(ttl=300)
def obtener_datos():
    try:
        # Primero obtenemos el contenido de la carpeta principal
        response = requests.get(URL_BASE, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscamos el link que termina en .xml
        links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.xml')]
        
        if not links:
            return None, "No se encontraron archivos XML en la ruta base."
        
        # Usamos el primer archivo encontrado
        url_feed = URL_BASE + links[0]
        
        # Leemos el XML
        r = requests.get(url_feed, timeout=15)
        return r.content, None
    except Exception as e:
        return None, str(e)

# Ejecución
contenido, error = obtener_datos()

if error:
    st.error(f"Error: {error}")
    st.write("Verifica si la URL base es accesible desde el entorno de la nube.")
else:
    st.success("¡Conexión establecida con éxito!")
    # Aquí procesarías el contenido XML con ET.fromstring(contenido)
    st.write("Archivo recibido correctamente.")
