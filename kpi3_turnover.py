import streamlit as st
import pandas as pd
import plotly.express as px

def show_kpi3(arrivees: pd.DataFrame):
    st.subheader("Turnover par grand pôle et par an")

    df = arrivees.copy()
    df["Date d'arrivée"] = pd.to_datetime(df["Date d'arrivée"], errors="coerce", dayfirst=True)
    df["Date de fin (si applicable)"] = pd.to_datetime(df["Date de fin (si applicable)"], errors="coerce", dayfirst=True)

    # On garde uniquement les CDI
    df = df[df["Type de contrat"] == "CDI"].dropna(subset=["Pôle associé"])

    results = []

    for year in sorted(df["Date d'arrivée"].dt.year.dropna().unique()):
        year = int(year)
        for pole in df["Pôle associé"].dropna().unique():
            subset = df[df["Pôle associé"] == pole]

            # bornes année
            year_start = pd.Timestamp(f"{year}-01-01")
            year_end = pd.Timestamp(f"{year}-12-31")

            # personnes présentes au moins une partie de l'année
            present = subset[
                (subset["Date d'arrivée"] <= year_end) &
                (
                    subset["Date de fin (si applicable)"].isna()
                    | (subset["Date de fin (si applicable)"] >= year_start)
                )
            ]

            # Effectif moyen (pondéré)
            effectif_moyen = 0
            for _, row in present.iterrows():
                start = max(row["Date d'arrivée"], year_start)
                end = row["Date de fin (si applicable)"] if pd.notnull(row["Date de fin (si applicable)"]) else year_end
                end = min(end, year_end)
                if start <= end:
                    effectif_moyen += (end - start).days / 365.25

            # Départs cette année
            departs = subset[subset["Date de fin (si applicable)"].dt.year == year].shape[0]

            turnover = (departs / effectif_moyen * 100) if effectif_moyen > 0 else 0

            results.append({
                "Année": year,
                "Pôle": pole,
                "Effectif_moyen": round(effectif_moyen, 2),
                "Départs": departs,
                "Turnover %": round(turnover, 2)
            })

    kpi3 = pd.DataFrame(results)

    # ===========================
    # Tableau
    # ===========================
    st.write("### Tableau Turnover (par pôle et par an)")
    st.write("L'effectif total qu'on divise choisi ici est l'effectif moyen pondéré.")
    st.dataframe(kpi3)

    # ===========================
    # Graphique
    # ===========================
    st.write("### Histogramme du Turnover (%)")
    fig = px.bar(
        kpi3,
        x="Année",
        y="Turnover %",
        color="Pôle",
        barmode="group",
        text="Turnover %",
        title="Turnover par pôle et par an"
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(yaxis_title="Turnover %", xaxis_title="Année")

    st.plotly_chart(fig, use_container_width=True)
