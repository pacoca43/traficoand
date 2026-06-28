import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Monitor de Tráfico", layout="wide")
st.title("📍 Monitor de Tráfico - Andalucía")

# URL directa del archivo XML de incidencias (infocar es el servidor más estable)
URL = "https://infocar.dgt.es/datex2/lod/dgt/incidencias.xml"

@st.cache_data(ttl=300)
def obtener_datos():
    try:
        # Usamos una sesión con timeout y headers de navegador
        session = requests.Session()
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = session.get(URL, headers=headers, timeout=10)
        
        # Como es XML, usaremos pandas para leerlo directamente si el formato lo permite
        # O un parseo simple si el XML es directo
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Intentamos obtener el texto
contenido = obtener_datos()

if "Error" in contenido:
    st.error(contenido)
    st.write("Si el error persiste, la red de la DGT está bloqueando el acceso desde Streamlit.")
else:
    st.success("¡Datos recibidos correctamente!")
    st.text_area("Contenido bruto del archivo:", value=contenido[:1000] + "...", height=200)
    st.write("El archivo ha sido descargado. Ahora puedes procesarlo con XML.fromstring()")
