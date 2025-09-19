import streamlit as st
import pandas as pd
import calendar

def show_kpi2(arrivees: pd.DataFrame, sorties: pd.DataFrame):
    st.subheader("Entrées et sorties par mois et par an (hors stagiaires)")

    # Nettoyage des dates
    arrivees["Date d'arrivée"] = pd.to_datetime(arrivees["Date d'arrivée"], errors="coerce", dayfirst=True)
    arrivees["Date de fin (si applicable)"] = pd.to_datetime(arrivees["Date de fin (si applicable)"], errors="coerce", dayfirst=True)

    # Exclure les stagiaires
    arrivees = arrivees[arrivees["Type de contrat"].str.lower() != "stage"]

    # ===========================
    # Entrées globales
    # ===========================
    entrees = (
        arrivees
        .dropna(subset=["Date d'arrivée"])
        .assign(Année=lambda x: x["Date d'arrivée"].dt.year,
                Mois=lambda x: x["Date d'arrivée"].dt.month)
        .groupby(["Année", "Mois"])
        .size()
        .unstack(fill_value=0)
    )
    entrees.columns = [calendar.month_abbr[m] for m in entrees.columns]

    # ===========================
    # Sorties globales
    # ===========================
    sorties_clean = (
        arrivees
        .dropna(subset=["Date de fin (si applicable)"])
        .assign(Année=lambda x: x["Date de fin (si applicable)"].dt.year,
                Mois=lambda x: x["Date de fin (si applicable)"].dt.month)
        .groupby(["Année", "Mois"])
        .size()
        .unstack(fill_value=0)
    )
    sorties_clean.columns = [calendar.month_abbr[m] for m in sorties_clean.columns]

    # ===========================
    # Entrées / sorties par pôle
    # ===========================
    entrees_pole = (
        arrivees
        .dropna(subset=["Date d'arrivée"])
        .assign(Année=lambda x: x["Date d'arrivée"].dt.year)
        .groupby(["Année", "Pôle associé"])
        .size()
        .unstack(fill_value=0)
    )

    sorties_pole = (
        arrivees
        .dropna(subset=["Date de fin (si applicable)"])
        .assign(Année=lambda x: x["Date de fin (si applicable)"].dt.year)
        .groupby(["Année", "Pôle associé"])
        .size()
        .unstack(fill_value=0)
    )

    # ===========================
    # Affichage Streamlit
    # ===========================
    st.write("### Entrées (par mois et par an, hors stagiaires)")
    st.dataframe(entrees)

    st.write("### Sorties (par mois et par an, hors stagiaires)")
    st.dataframe(sorties_clean)

    st.write("### Entrées par pôle et par an")
    st.dataframe(entrees_pole)

    st.write("### Sorties par pôle et par an")
    st.dataframe(sorties_pole)
