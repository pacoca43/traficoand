import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Tráfico Andalucía", layout="wide")
st.title("📍 Monitor de Tráfico - Andalucía")

# Usamos una API que sirve los datos de la DGT de forma abierta
# Esto evita errores de conexión 404 o bloqueos por servidor
API_URL = "https://datos.dgt.es/api/explore/v2.1/catalog/datasets/incidencias-dgt/records?limit=100"

@st.cache_data(ttl=300)
def obtener_datos():
    try:
        response = requests.get(API_URL, timeout=10)
        data = response.json()
        
        # Procesamos la lista de resultados
        records = data.get('results', [])
        df = pd.DataFrame(records)
        
        # Filtramos columnas relevantes si existen
        columnas = ['carretera', 'tipoincidencia', 'pk_final', 'provincia']
        # Solo tomamos las columnas que existan en el dataset
        df = df[[c for c in columnas if c in df.columns]]
        return df
    except Exception as e:
        return pd.DataFrame({"Error": [f"No se pudieron cargar los datos: {e}"]})

df = obtener_datos()

# Filtro por provincias de Andalucía
st.subheader("Filtrar por Andalucía")
provincias_andaluzas = ['Sevilla', 'Málaga', 'Córdoba', 'Granada', 'Jaén', 'Almería', 'Cádiz', 'Huelva']
if 'provincia' in df.columns:
    df_andalucia = df[df['provincia'].isin(provincias_andaluzas)]
    st.table(df_andalucia)
else:
    st.write("Datos cargados. Mostrando tabla completa:")
    st.table(df)

st.caption("Fuente: Portal de Datos Abiertos DGT")
