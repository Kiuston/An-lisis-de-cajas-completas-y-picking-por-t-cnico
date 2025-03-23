import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Resumen por Técnico", layout="wide")
st.title("📦 Análisis de cajas completas y picking por técnico")

uploaded_file = st.file_uploader("📂 Subí tu archivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="LASER", header=None)

    fila_17 = df.iloc[16].fillna("").astype(str).tolist()
    try:
        col_codigo = fila_17.index("CODIGO ADMIN")
        col_cajas = fila_17.index("Cajas")
    except ValueError:
        st.error("No se encontraron las columnas necesarias: 'CODIGO ADMIN' o 'Cajas'.")
        st.stop()

    # Obtener tabla de referencia
    df_referencia = df.iloc[17:, [col_codigo, col_cajas]].copy()
    df_referencia.columns = ["Codigo", "Cajas"]
    df_referencia = df_referencia.dropna(subset=["Codigo"])
    df_referencia["Cajas"] = pd.to_numeric(df_referencia["Cajas"], errors="coerce").fillna(0)
    df_referencia = df_referencia.set_index("Codigo")

    # Detectar técnicos y columnas de defectuosos
    fila_16 = df.iloc[15].fillna("").astype(str).tolist()
    tecnicos = []
    for idx, val in enumerate(fila_16):
        if "(PARTE" in val:
            tecnicos.append((val.strip(), idx))

    for nombre, col in tecnicos:
        col_ini = col
        col_fin = col + 2  # Asumimos que usa 3 columnas consecutivas

        data = df.iloc[17:, col_ini:col_ini+3].copy()
        data.columns = ["Uds1", "Uds2", "Uds3"]
        data = data.apply(pd.to_numeric, errors="coerce").fillna(0)
        data["Unidades buenas"] = data[["Uds1", "Uds2", "Uds3"]].sum(axis=1).astype(int)

        codigos = df.iloc[17:, col_codigo]
        data["Codigo"] = codigos
        data = data.dropna(subset=["Codigo"])
        data = data.merge(df_referencia, on="Codigo", how="left")
        data = data.dropna(subset=["Cajas"])
        data["Cajas completas"] = (data["Unidades buenas"] // data["Cajas"]).astype(int)
        data["Unidades sobrantes"] = (data["Unidades buenas"] % data["Cajas"]).astype(int)
        data["Clasificación"] = data["Cajas completas"].apply(lambda x: "Caja completa" if x > 0 else "Caja sin cantidad")

        total_buenas = data["Unidades buenas"].sum()
        total_cajas = data["Cajas completas"].sum()
        total_sobrantes = data["Unidades sobrantes"].sum()

        st.markdown(f"### 👨‍🔧 Técnico: **{nombre}**")
        st.dataframe(data[["Codigo", "Cajas", "Unidades buenas", "Cajas completas", "Unidades sobrantes", "Clasificación"]], use_container_width=True)

        fig, ax = plt.subplots()
        valores = [total_cajas, total_sobrantes]
        etiquetas = [f"Cajas completas ({total_cajas})", f"Unidades sobrantes ({total_sobrantes})"]
        colores = ["#1f77b4", "#ff7f0e"]
        ax.pie(valores, labels=etiquetas, colors=colores, startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

        with st.expander("📊 Resumen numérico"):
            st.metric("Total de Unidades Buenas", f"{total_buenas:,}")
            st.metric("Cajas Completas", total_cajas)
            st.metric("Unidades Sobrantes", total_sobrantes)
