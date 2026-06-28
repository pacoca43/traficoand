import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET

st.set_page_config(page_title="Tráfico Andalucía", layout="wide")
st.title("📍 Estado actual del tráfico en Andalucía")

URL = "https://infocar.dgt.es/datex2/lod/dgt/incidencias.rdf"

@st.cache_data(ttl=600)  # La app cacheará los datos 10 minutos para ser rápida
def obtener_datos():
    try:
        response = requests.get(URL, timeout=10)
        # Aquí procesarías el XML. 
        # Como ejemplo, simulamos la estructura que obtendrías:
        data = [
            {"Carretera": "A-4", "Incidencia": "Retención", "Punto": "KM 530", "Estado": "Activo"},
            {"Carretera": "A-92", "Incidencia": "Obras", "Punto": "KM 120", "Estado": "En curso"},
            {"Carretera": "SE-30", "Incidencia": "Accidente", "Punto": "KM 12", "Estado": "Pendiente"}
        ]
        return pd.DataFrame(data)
    except Exception as e:
        return pd.DataFrame({"Error": [f"No se pudieron cargar los datos: {e}"]})

# Mostrar datos
df = obtener_datos()
st.table(df)

st.caption(f"Última actualización: {pd.Timestamp.now().strftime('%H:%M:%S')}")
