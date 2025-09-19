import streamlit as st
import pandas as pd

def show_kpi7(arrivees: pd.DataFrame):
    st.subheader("⏳ Ancienneté moyenne des CDI par pôle")

    today = pd.Timestamp.today()
    df = arrivees.copy()

    # Nettoyage des dates
    df["Date d'arrivée"] = pd.to_datetime(df["Date d'arrivée"], errors="coerce", dayfirst=True)
    df["Date de fin (si applicable)"] = pd.to_datetime(df["Date de fin (si applicable)"], errors="coerce", dayfirst=True)

    # Ne garder que les CDI
    df = df[df["Type de contrat"].str.upper() == "CDI"]

    # Calcul ancienneté (en années)
    anciennetes = []
    for _, row in df.iterrows():
        if pd.isna(row["Date d'arrivée"]):
            continue
        start = row["Date d'arrivée"]
        end = row["Date de fin (si applicable)"] if pd.notnull(row["Date de fin (si applicable)"]) else today
        delta_years = (end - start).days / 365.25
        anciennetes.append({
            "Pôle": row["Pôle associé"],
            "Ancienneté (années)": delta_years
        })

    df_anciennete = pd.DataFrame(anciennetes)

    if df_anciennete.empty:
        st.warning("⚠️ Aucune donnée disponible pour calculer l’ancienneté CDI.")
        return

    # Moyenne par pôle
    kpi7 = df_anciennete.groupby("Pôle")["Ancienneté (années)"].mean().reset_index()
    kpi7["Ancienneté (années)"] = kpi7["Ancienneté (années)"].round(2)

    # =======================
    # Affichage
    # =======================
    st.write("### Ancienneté moyenne par pôle (en années)")
    st.dataframe(kpi7, use_container_width=True)

    st.write("### Histogramme d'ancienneté par pôle")
    st.bar_chart(kpi7.set_index("Pôle")["Ancienneté (années)"])
