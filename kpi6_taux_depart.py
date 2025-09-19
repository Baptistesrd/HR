import streamlit as st
import pandas as pd

def show_kpi6(sorties: pd.DataFrame):
    st.subheader("KPI6 : Taux de départ CDI par type de sortie")

    df = sorties.copy()
    df["Date de départ prévue"] = pd.to_datetime(df["Date de départ prévue"], errors="coerce", dayfirst=True)
    df = df[df["Type de contrat"] == "CDI"]

    kpi6 = df.groupby([df["Date de départ prévue"].dt.year, "Type de départ"]).size().unstack(fill_value=0)
    st.dataframe(kpi6)

