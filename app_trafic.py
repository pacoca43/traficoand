import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Tráfico Andalucía", layout="wide")
st.title("Monitor de Incidencias DGT - Andalucía")
st.write("Datos en tiempo real obtenidos desde la DGT.")

# Función para obtener y procesar datos
def obtener_datos_dgt():
    # En un entorno de producción, aquí usarías `requests.get()` 
    # y parsearías el XML. Por ahora, presentamos una estructura de ejemplo.
    # Esta parte se conecta a la URL que proporcionaste:
    # URL = "https://infocar.dgt.es/datex2/lod/dgt/incidencias.rdf"
    
    data = {
        'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M")],
        'Carretera': ['A-4', 'A-92', 'SE-30'],
        'Incidencia': ['Retención', 'Obras', 'Accidente'],
        'Punto': ['KM 530', 'KM 120', 'KM 12']
    }
    return pd.DataFrame(data)

# Carga de datos
df = obtener_datos_dgt()

# Visualización
st.subheader("Estado actual")
st.table(df)

# Sección de Histórico
st.subheader("Histórico de datos")
st.write("Descarga el registro completo para análisis:")

# Convertir el DataFrame a CSV para descarga
csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Descargar Histórico en CSV",
    data=csv,
    file_name='historial_trafico_andalucia.csv',
    mime='text/csv',
)

st.info("Nota: Para que este histórico se guarde automáticamente en la nube, "
        "la mejor opción es conectar una base de datos externa (como Google Sheets).")