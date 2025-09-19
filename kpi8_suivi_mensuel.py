import streamlit as st
import pandas as pd

def show_kpi8(arrivees: pd.DataFrame):
    st.subheader("Suivi mensuel par type de contrat")

    df = arrivees.copy()
    df["Date d'arrivée"] = pd.to_datetime(df["Date d'arrivée"], errors="coerce", dayfirst=True)
    df["Date de fin (si applicable)"] = pd.to_datetime(df["Date de fin (si applicable)"], errors="coerce", dayfirst=True)

    monthly = df.groupby([df["Date d'arrivée"].dt.to_period("M"), "Type de contrat"]).size().unstack(fill_value=0)
    st.dataframe(monthly)
