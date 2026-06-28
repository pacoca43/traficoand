import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuración de Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Historial_Trafico').sheet1

def guardar_en_sheets(data):
    # Añade los datos como una nueva fila en Google Sheets
    sheet.append_row(data)

st.title("Monitor de Tráfico en Directo")

# Ejemplo de datos capturados
if st.button("Registrar Incidencia Actual"):
    nueva_fila = ["2026-06-28 13:40", "A-4", "Retención", "KM 530"]
    guardar_en_sheets(nueva_fila)
    st.success("¡Guardado en Google Sheets!")

# Mostrar histórico desde Sheets
data = sheet.get_all_records()
st.table(pd.DataFrame(data))
