
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Resumen por Técnico", layout="wide")
st.title("📦 Análisis Técnico: Cajas vs Picking")

df = pd.DataFrame([
    {"Técnico": "Max", "Unidades Buenas": 1671, "Unidades Defectuosas": 37, "Cajas Completas": 11, "Unidades Sobrantes": 805},
    {"Técnico": "Antonio", "Unidades Buenas": 5362, "Unidades Defectuosas": 128, "Cajas Completas": 86, "Unidades Sobrantes": 3110},
    {"Técnico": "Oscar L.", "Unidades Buenas": 6619, "Unidades Defectuosas": 63, "Cajas Completas": 53, "Unidades Sobrantes": 5333},
    {"Técnico": "Kilian", "Unidades Buenas": 667, "Unidades Defectuosas": 27, "Cajas Completas": 0, "Unidades Sobrantes": 667},
    {"Técnico": "Teixeira", "Unidades Buenas": 2838, "Unidades Defectuosas": 122, "Cajas Completas": 20, "Unidades Sobrantes": 1990},
    {"Técnico": "Andrys", "Unidades Buenas": 1103, "Unidades Defectuosas": 25, "Cajas Completas": 10, "Unidades Sobrantes": 893},
])

for _, row in df.iterrows():
    with st.container():
        st.subheader(f"Técnico: {row['Técnico']}")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.metric("Unidades Buenas", int(row["Unidades Buenas"]))
            st.metric("Unidades Defectuosas", int(row["Unidades Defectuosas"]))
            st.metric("Cajas Completas", int(row["Cajas Completas"]))
            st.metric("Unidades a Picking", int(row["Unidades Sobrantes"]))

        with col2:
            fig, ax = plt.subplots()
            ax.pie(
                [row["Cajas Completas"], row["Unidades Sobrantes"]],
                labels=["Cajas Completas", "Va a Picking"],
                colors=["#4CAF50", "#FFC107"],
                startangle=90,
                wedgeprops={"edgecolor": "white"}
            )
            ax.axis("equal")
            st.pyplot(fig)
