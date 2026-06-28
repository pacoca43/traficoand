import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET

# Configuración inicial
st.set_page_config(page_title="Monitor DGT", layout="wide")
st.title("📍 Monitor de Tráfico DGT (Datos en Tiempo Real)")

# URL del feed de incidencias real
URL = "https://infocar.dgt.es/datex2/lod/dgt/incidencias.xml"

@st.cache_data(ttl=300)
def obtener_datos():
    try:
        response = requests.get(URL, timeout=15)
        if response.status_code != 200:
            return None, f"Error de conexión: {response.status_code}"
        
        root = ET.fromstring(response.content)
        
        incidencias = []
        # En el XML de infocar, los datos están bajo 'situationRecord'
        for record in root.findall('.//situationRecord'):
            # Extracción de campos clave
            road_node = record.find('.//roadNumber')
            type_node = record.find('.//situationRecordType')
            
            # Algunos registros pueden no tener carretera, gestionamos el error
            incidencias.append({
                "Carretera": road_node.text if road_node is not None else "N/A",
                "Tipo": type_node.text if type_node is not None else "Sin tipo"
            })
            
        return pd.DataFrame(incidencias), None
    except Exception as e:
        return None, str(e)

# Ejecución del monitor
df, error = obtener_datos()

if error:
    st.error(f"Error al cargar datos: {error}")
elif df is None or df.empty:
    st.warning("No se pudieron extraer incidencias en este momento.")
else:
    st.success(f"Se han cargado {len(df)} incidencias en todo el territorio.")
    
    # Filtro opcional por Andalucía
    st.subheader("Filtrar incidencias en Andalucía")
    filtro_andalucia = st.checkbox("Mostrar solo carreteras de Andalucía (A-4, A-92, A-49, A-7, etc.)")
    
    if filtro_andalucia:
        # Filtro basado en las principales autovías andaluzas
        patron = 'A-4|A-92|A-49|A-7|A-381|A-357|A-45|A-44|A-384|A-382'
        df_filtrado = df[df['Carretera'].str.contains(patron, na=False)]
        st.table(df_filtrado)
    else:
        st.table(df)

st.caption(f"Última actualización: {pd.Timestamp.now().strftime('%H:%M:%S')}")
