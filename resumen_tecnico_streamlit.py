import streamlit as st
import pandas as pd

st.set_page_config(page_title="Análisis de cajas completas y picking por técnico", layout="wide")
st.title("📦 Análisis de cajas completas y picking por técnico")

uploaded_file = st.file_uploader("📂 Subí tu archivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        # MOSTRAR LAS HOJAS DISPONIBLES
        xls = pd.ExcelFile(uploaded_file)
        st.write("📄 Hojas detectadas en el archivo:", xls.sheet_names)

        # VERIFICAR SI EXISTE 'LASER'
        if "LASER" not in xls.sheet_names:
            st.error("❌ No se encontró la hoja 'LASER' en el archivo. Verificá el nombre exacto de la pestaña.")
        else:
            df = pd.read_excel(xls, sheet_name="LASER", header=None)
            st.success("✅ Hoja 'LASER' encontrada correctamente.")
            st.write("📊 Vista previa de los primeros datos:")
            st.dataframe(df.head(10))
    except Exception as e:
        st.error(f"💥 Ocurrió un error al leer el archivo: {e}")
else:
    st.info("📌 Esperando que subas un archivo Excel...")
