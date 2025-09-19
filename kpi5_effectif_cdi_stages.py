import streamlit as st
import pandas as pd

def show_kpi5(arrivees: pd.DataFrame):
    st.subheader("KPI5 : Effectif CDI moyens + stagiaires par an")

    df = arrivees[arrivees["Type de contrat"].isin(["CDI", "Stage"])].copy()
    df["Date d'arrivée"] = pd.to_datetime(df["Date d'arrivée"], errors="coerce", dayfirst=True)
    df["Date de fin (si applicable)"] = pd.to_datetime(df["Date de fin (si applicable)"], errors="coerce", dayfirst=True)

    records = []
    for year in df["Date d'arrivée"].dt.year.dropna().unique():
        subset = df[(df["Date d'arrivée"].dt.year <= year) & (
            df["Date de fin (si applicable)"].isna() | (df["Date de fin (si applicable)"].dt.year >= year)
        )]
        records.append({"Année": year, "Effectif moyen CDI+Stagiaires": subset.shape[0]})
    
    kpi5 = pd.DataFrame(records)
    st.dataframe(kpi5)
