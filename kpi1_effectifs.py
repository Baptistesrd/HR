import pandas as pd
import datetime as dt
import plotly.express as px
import streamlit as st

def show_kpi1(arrivees: pd.DataFrame):
    st.subheader("Effectifs par contrat et par an, avec vue par pôle")

    today = dt.date.today()
    df = arrivees.copy()

    # Nettoyage des dates
    df["Date d'arrivée"] = pd.to_datetime(df["Date d'arrivée"], errors="coerce", dayfirst=True)
    df["Date de fin (si applicable)"] = pd.to_datetime(df["Date de fin (si applicable)"], errors="coerce", dayfirst=True)

    # Filtrer uniquement les arrivées valides
    df = df.dropna(subset=["Date d'arrivée"])

    # ==================================================
    # 1️⃣ Effectifs bruts par année (par type de contrat)
    # ==================================================
    records = []
    for year in range(df["Date d'arrivée"].dt.year.min(), today.year + 1):
        for contrat in df["Type de contrat"].dropna().unique():
            actifs = df[
                (df["Type de contrat"] == contrat)
                & (df["Date d'arrivée"].dt.year <= year)
                & (
                    df["Date de fin (si applicable)"].isna()
                    | (df["Date de fin (si applicable)"].dt.year >= year)
                )
            ]
            records.append({"Année": year, "Type de contrat": contrat, "Effectif": len(actifs)})

    kpi1 = pd.DataFrame(records)

    st.write("### Effectif , par type de contrat)")
    st.dataframe(kpi1.pivot_table(index="Année", columns="Type de contrat", values="Effectif", fill_value=0))

    fig = px.bar(kpi1, x="Année", y="Effectif", color="Type de contrat", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    # ==================================================
    # 2️⃣ Effectif moyen annuel pondéré (par type de contrat)
    # ==================================================
    weighted_records = []
    for year in range(df["Date d'arrivée"].dt.year.min(), today.year + 1):
        year_start = pd.Timestamp(f"{year}-01-01")
        year_end = pd.Timestamp(f"{year}-12-31")

        for _, row in df.iterrows():
            start = max(row["Date d'arrivée"], year_start)
            end = row["Date de fin (si applicable)"] if pd.notnull(row["Date de fin (si applicable)"]) else year_end
            end = min(end, year_end)

            if start <= end:  # personne présente au moins un peu dans l’année
                months = (end - start).days / 365.25  # fraction d'année
                weighted_records.append({
                    "Année": year,
                    "Type de contrat": row["Type de contrat"],
                    "Pondération": months
                })

    kpi1_weighted = pd.DataFrame(weighted_records)
    kpi1_weighted = kpi1_weighted.groupby(["Année", "Type de contrat"])["Pondération"].sum().reset_index()

    st.write("### Effectif moyen annuel pondéré (par type de contrat)")
    st.dataframe(
        kpi1_weighted.pivot_table(index="Année", columns="Type de contrat", values="Pondération", fill_value=0).round(2)
    )

    # ==================================================
    # 3️⃣ Effectif par pôle AVEC et SANS stagiaires
    # ==================================================
    for include_interns, label in [(True, "Avec stagiaires"), (False, "Sans stagiaires")]:
        df_filtered = df.copy()
        if not include_interns:
            df_filtered = df_filtered[df_filtered["Type de contrat"].str.lower() != "stage"]

        pole_records = []
        for year in range(df_filtered["Date d'arrivée"].dt.year.min(), today.year + 1):
            for pole in df_filtered["Pôle associé"].dropna().unique():
                actifs = df_filtered[
                    (df_filtered["Pôle associé"] == pole)
                    & (df_filtered["Date d'arrivée"].dt.year <= year)
                    & (
                        df_filtered["Date de fin (si applicable)"].isna()
                        | (df_filtered["Date de fin (si applicable)"].dt.year >= year)
                    )
                ]
                pole_records.append({"Année": year, "Pôle": pole, "Effectif": len(actifs)})

        kpi1_pole = pd.DataFrame(pole_records)

        st.write(f"### Effectif par pôle (fin d’année) — {label}")
        st.dataframe(
            kpi1_pole.pivot_table(index="Année", columns="Pôle", values="Effectif", fill_value=0)
        )

    # ==================================================
    # 4️⃣ Effectif pondéré par pôle AVEC et SANS stagiaires
    # ==================================================
    for include_interns, label in [(True, "Avec stagiaires"), (False, "Sans stagiaires")]:
        df_filtered = df.copy()
        if not include_interns:
            df_filtered = df_filtered[df_filtered["Type de contrat"].str.lower() != "stage"]

        weighted_pole_records = []
        for year in range(df_filtered["Date d'arrivée"].dt.year.min(), today.year + 1):
            year_start = pd.Timestamp(f"{year}-01-01")
            year_end = pd.Timestamp(f"{year}-12-31")

            for _, row in df_filtered.dropna(subset=["Pôle associé"]).iterrows():
                start = max(row["Date d'arrivée"], year_start)
                end = row["Date de fin (si applicable)"] if pd.notnull(row["Date de fin (si applicable)"]) else year_end
                end = min(end, year_end)

                if start <= end:
                    months = (end - start).days / 365.25
                    weighted_pole_records.append({
                        "Année": year,
                        "Pôle": row["Pôle associé"],
                        "Pondération": months
                    })

        kpi1_pole_weighted = pd.DataFrame(weighted_pole_records)
        kpi1_pole_weighted = kpi1_pole_weighted.groupby(["Année", "Pôle"])["Pondération"].sum().reset_index()

        st.write(f"### Effectif moyen annuel pondéré par pôle — {label}")
        st.dataframe(
            kpi1_pole_weighted.pivot_table(index="Année", columns="Pôle", values="Pondération", fill_value=0).round(2)
        )
