import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET

st.set_page_config(page_title="Monitor DGT", layout="wide")
st.title("📍 Monitor de Tráfico DGT (Datos V3.7)")

URL = "https://nap.dgt.es/datex2/v3/dgt/SituationPublication/datex2_v37.xml"

@st.cache_data(ttl=300)
def obtener_datos():
    try:
        response = requests.get(URL, timeout=15)
        if response.status_code != 200:
            return None, f"Error de conexión: {response.status_code}"
        
        root = ET.fromstring(response.content)
        # Namespace necesario para DATEX II V3
        ns = {'d2': 'http://datex2.eu/schema/3/d2LogicalModel'}
        
        incidencias = []
        # Buscamos los registros
        for record in root.findall('.//d2:situationRecord', ns):
            # Extraemos info (ajustamos a las etiquetas estándar)
            road_node = record.find('.//d2:roadNumber', ns)
            type_node = record.find('.//d2:situationRecordType', ns)
            
            incidencias.append({
                "Carretera": road_node.text if road_node is not None else "N/A",
                "Tipo": type_node.text if type_node is not None else "Sin tipo"
            })
            
        return pd.DataFrame(incidencias), None
    except Exception as e:
        return None, str(e)

# Ejecución
df, error = obtener_datos()

if error:
    st.error(f"Error al cargar datos: {error}")
elif df.empty:
    st.warning("El archivo se leyó correctamente pero no contiene incidencias en este momento.")
else:
    st.success(f"Se encontraron {len(df)} incidencias en total.")
    
    # Filtro opcional por Andalucía (A-4, A-92, A-49, A-7, etc)
    st.subheader("Filtrar por Andalucía")
    filtro = st.checkbox("Mostrar solo carreteras andaluzas (A-4, A-92, A-49, A-7, A-381, A-357)")
    
    if filtro:
        # Lista de prefijos de carreteras andaluzas
        df = df[df['Carretera'].str.contains('A-4|A-92|A-49|A-7|A-381|A-357', na=False)]
    
    st.table(df)
