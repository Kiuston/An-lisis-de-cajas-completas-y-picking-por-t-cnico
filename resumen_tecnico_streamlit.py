# resumen_tecnico_streamlit.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl

st.set_page_config(layout="wide")
st.title("📦 Análisis de cajas completas y picking por técnico")
st.markdown("#### 📂 Subí tu archivo Excel (.xlsx)")

uploaded_file = st.file_uploader(" ", type=["xlsx"])

if uploaded_file:
    try:
        df_excel = pd.read_excel(uploaded_file, sheet_name=None, header=None)
        sheet_names = list(df_excel.keys())

        if "LASER" in sheet_names:
            st.success("✅ Hoja 'LASER' encontrada correctamente.")
            df_laser = df_excel["LASER"]

            # Detectar columnas de técnicos (colores)
            header_row = df_laser.iloc[16]
            tecnicos = {}
            for col in df_laser.columns:
                nombre = str(df_laser.iloc[16, col])
                if nombre.strip() != "" and "PARTE" in nombre:
                    tecnicos[nombre.strip()] = col

            # Leer cantidades por cartucho desde la valoración anterior
            archivo_valoracion = pd.read_excel("Recyling and ecology diciembre.xlsx", sheet_name="LASER", header=16)
            cantidades_por_codigo = archivo_valoracion.set_index("CODIGO ADMIN")["Cajas"].to_dict()

            st.markdown("---")
            st.subheader("📊 Resultados por Técnico")

            for tecnico, col_index in tecnicos.items():
                st.markdown(f"### 👤 Técnico: **{tecnico}**")

                columna_datos = df_laser.iloc[17:, col_index].dropna()
                columna_datos = pd.to_numeric(columna_datos, errors="coerce").fillna(0)

                # Identificar columnas de defectuosos (color igual)
                cols_defectuosos = [i for i in range(col_index + 1, col_index + 6)]
                defectuosos = df_laser.iloc[17:, cols_defectuosos].fillna(0)
                defectuosos = defectuosos.apply(pd.to_numeric, errors="coerce").fillna(0)
                total_defectuosos = int(defectuosos.sum().sum())

                total_buenos = int(columna_datos.sum())
                total_general = total_buenos + total_defectuosos

                # Determinar cajas completas
                cajas_completas = 0
                unidades_sobrantes = 0

                for fila in columna_datos.index:
                    codigo = str(df_laser.iloc[fila, 0]).strip()
                    if codigo in cantidades_por_codigo:
                        cantidad_caja = cantidades_por_codigo[codigo]
                        unidades = columna_datos[fila]
                        cajas = unidades // cantidad_caja
                        sobrante = unidades % cantidad_caja
                        cajas_completas += int(cajas)
                        unidades_sobrantes += int(sobrante)

                # Resumen
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.metric("📦 Cajas Completas", f"{cajas_completas}")
                    st.metric("📦 Unidades sobrantes", f"{unidades_sobrantes}")
                    st.metric("📦 Unidades buenas", f"{total_buenos}")
                    st.metric("🧨 Unidades defectuosas", f"{total_defectuosos}")
                    st.metric("🔢 Total general", f"{total_general}")

                with col2:
                    fig, ax = plt.subplots()
                    etiquetas = ['Cajas completas', 'Unidades sobrantes']
                    valores = [cajas_completas, unidades_sobrantes]
                    colores = ['#1f77b4', '#ff7f0e']
                    ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', colors=colores, startangle=90)
                    ax.axis('equal')
                    ax.set_title("Distribución de trabajo")
                    st.pyplot(fig)

                st.markdown("---")

        else:
            st.error("❌ La hoja 'LASER' no se encuentra en el archivo Excel.")

    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
