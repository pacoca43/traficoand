import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET

URL = "https://nap.dgt.es/datex2/v3/dgt/SituationPublication/datex2_v37.xml"

@st.cache_data(ttl=600)
def obtener_datos():
    try:
        response = requests.get(URL, timeout=15)
        root = ET.fromstring(response.content)
        
        # El espacio de nombres (namespace) es necesario para encontrar las etiquetas
        ns = {'d2': 'http://datex2.eu/schema/3/d2LogicalModel'}
        
        incidencias = []
        # Buscamos los registros de situación en el XML
        for record in root.findall('.//d2:situationRecord', ns):
            # Extraemos datos básicos (esto puede variar según la estructura exacta)
            carretera = record.find('.//d2:roadNumber', ns)
            tipo = record.find('.//d2:situationRecordType', ns)
            
            incidencias.append({
                "Carretera": carretera.text if carretera is not None else "N/A",
                "Tipo": tipo.text if tipo is not None else "Desconocido"
            })
            
        return pd.DataFrame(incidencias)
    except Exception as e:
        return pd.DataFrame({"Error": [f"Error al procesar el XML v3.7: {e}"]})

# Mostrar los datos
st.title("📍 Tráfico: Datos V3.7 DGT")
df = obtener_datos()
st.table(df)
