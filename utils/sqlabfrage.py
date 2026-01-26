import pandas as pd
import pandasql as psql
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# -------------------------------
# SQL-Analysefunktionen für Streamlit
# -------------------------------

def top_bezirke(df, top_n=10, plot=True):
    query = f"""
        SELECT region3 as bezirk, COUNT(*) as anzahl_wohnungen
        FROM df
        GROUP BY region3
        ORDER BY anzahl_wohnungen DESC
        LIMIT {top_n}
    """
    result = psql.sqldf(query)

    if plot:
        fig, ax = plt.subplots(figsize=(10,6))
        sns.barplot(data=result, x='bezirk', y='anzahl_wohnungen', palette='Blues', ax=ax, dodge=False)
        ax.set_title("Top Bezirke nach Anzahl Wohnungen")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

        # Legende nur entfernen, wenn vorhanden
        leg = ax.get_legend()
        if leg is not None:
            leg.remove()

        st.pyplot(fig)

    return result





def heizung_analysen(df, plot=True):
    query = """
        SELECT heizungstyp, COUNT(*) as anzahl
        FROM df
        GROUP BY heizungstyp
        ORDER BY anzahl DESC
    """
    result = psql.sqldf(query, locals())

    if plot:
        fig, ax = plt.subplots(figsize=(8,5))
        sns.barplot(data=result, x='heizungstyp', y='anzahl', palette='Purples', dodge=False, ax=ax)
        ax.set_title("Verteilung der Heizungsarten")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        st.pyplot(fig)

    return result


def balkon_analysen(df, plot=True):
    query = """
        SELECT balkon, COUNT(*) as anzahl, AVG(gesamt_miete) as durchschn_miete
        FROM df
        GROUP BY balkon
    """
    result = psql.sqldf(query, locals())

    if plot:
        fig, ax = plt.subplots(figsize=(6,5))
        sns.barplot(data=result, x='balkon', y='anzahl', palette='Greens', dodge=False, ax=ax)
        ax.set_title("Wohnungen mit/ohne Balkon")
        st.pyplot(fig)

    return result


def zimmer_verteilung(df, plot=True):
    query = """
        SELECT zimmer, COUNT(*) as anzahl, AVG(gesamt_miete) as durchschn_miete
        FROM df
        GROUP BY zimmer
        ORDER BY anzahl DESC
    """
    result = psql.sqldf(query, locals())

    if plot:
        fig, ax = plt.subplots(figsize=(10,6))
        sns.barplot(data=result, x='zimmer', y='anzahl', palette='Oranges', dodge=False, ax=ax)
        ax.set_title("Zimmeranzahl Verteilung")
        ax.set_xlabel("Zimmer")
        ax.set_ylabel("Anzahl Wohnungen")
        st.pyplot(fig)

    return result





def kueche_analysen(df, plot=True):
    query = """
        SELECT mit_kueche, COUNT(*) as anzahl, AVG(gesamt_miete) as durchschn_miete
        FROM df
        GROUP BY mit_kueche
    """
    result = psql.sqldf(query, locals())

    if plot:
        fig, ax = plt.subplots(figsize=(6,5))
        sns.barplot(data=result, x='mit_kueche', y='durchschn_miete', palette='magma', dodge=False, ax=ax)
        ax.set_title("Wohnungen mit/ohne Küche")
        st.pyplot(fig)

    return result




def haustiere_analysen(df, plot=True):
    query = """
        SELECT haustiere_erlaubt, COUNT(*) as anzahl, AVG(gesamt_miete) as durchschn_miete
        FROM df
        GROUP BY haustiere_erlaubt
    """
    result = psql.sqldf(query, locals())

    if plot:
        fig, ax = plt.subplots(figsize=(6,5))
        sns.barplot(data=result, x='haustiere_erlaubt', y='durchschn_miete', palette='cool', dodge=False, ax=ax)
        ax.set_title("Haustiere erlaubt vs. nicht erlaubt")
        st.pyplot(fig)

    return result

