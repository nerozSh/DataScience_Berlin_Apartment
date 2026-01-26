

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# eda/plots.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pandas.plotting import scatter_matrix


def run_plots():
    st.header(" Analyse Berliner Stadtteile")

    # Datei einlesen (bereinigte Daten)
    df = pd.read_csv("data/berlin_data_clean.csv")

  
    # 1. Feature: Miete pro m²
 
    df["miete_pro_m2"] = df["grundmiete"] / df["wohnflaeche"]

    numerische_spalten = ["miete_pro_m2","grundmiete","gesamt_miete","wohnflaeche","zimmer","nebenkosten"]

    st.subheader("Scatter-Matrix der numerischen Variablen")
    fig = plt.figure(figsize=(12,12))
    scatter_matrix(df[numerische_spalten],
                   alpha=0.6,
                   diagonal='kde',
                   marker='o',
                   color='blue',
                   ax=fig.add_subplot(111))
    st.pyplot(fig)
    plt.clf()

  
    # 2. Durchschnittliche Miete pro m² pro Stadtteil

    avg_miete_stadtteil = df.groupby("region3")["miete_pro_m2"].mean().sort_values()
    st.subheader("Durchschnittliche Miete pro m² pro Stadtteil")
    st.dataframe(avg_miete_stadtteil)

    fig, ax = plt.subplots(figsize=(18,6))
    avg_miete_stadtteil.plot(kind="bar", color="skyblue", ax=ax)
    ax.set_ylabel("Miete pro m² (€)")
    ax.set_title("Durchschnittliche Miete pro m² nach Stadtteil (Berlin)")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha="right")
    st.pyplot(fig)

    
    # 3. Jointplot Wohnfläche vs. Gesamtmiete

    st.subheader("Wohnfläche vs. Gesamtmiete")
    g = sns.jointplot(data=df, x="wohnflaeche", y="gesamt_miete", kind="scatter", height=6)
    st.pyplot(g.fig)



    # 5. Ausreißer
 
    st.subheader("Ausreißer bei Miete pro m²")
    fig, ax = plt.subplots(figsize=(8,6))
    sns.boxplot(data=df, y="miete_pro_m2", ax=ax)
    ax.set_title("Ausreißer bei Miete pro m²")
    st.pyplot(fig)

  
    # 6. Korrelationen
   
    st.subheader("Korrelationsmatrix")
    corr = df[["grundmiete","gesamt_miete","wohnflaeche","zimmer","nebenkosten"]].corr()
    st.dataframe(corr)

    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    ax.set_title("Korrelationsmatrix")
    st.pyplot(fig)


'''
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Projektpfad hinzufügen
sys.path.append(os.path.abspath(".."))
# Datei einlesen (bereinigte Daten)
df = pd.read_csv("data/berlin_data_clean.csv")

from pandas.plotting import scatter_matrix


# -------------------------------
# 2.Durchschnittliche Miete pro m² pro Stadtteil (region3)
# -------------------------------
df["miete_pro_m2"] = df["grundmiete"] / df["wohnflaeche"]
#
numerische_spalten = ["miete_pro_m2","grundmiete","gesamt_miete","wohnflaeche","zimmer","nebenkosten"]

scatter_matrix(df[numerische_spalten],
               alpha=0.6,      # Transparenz der Punkte
               figsize=(12,12), # Größe der Matrix
               diagonal='kde',  # KDE statt Histogramm auf Diagonale
               marker='o',      # Punktform
               color='blue')
plt.suptitle("Scatter-Matrix der numerischen Variablen", fontsize=14)
plt.show()
# Gruppieren nach region3 (Stadtteile)
avg_miete_stadtteil = df.groupby("region3")["miete_pro_m2"].mean().sort_values()
print("\n📊 Durchschnittliche Miete pro m² pro Stadtteil:\n")
print(avg_miete_stadtteil)

# Balkendiagramm
plt.figure(figsize=(18, 6))
avg_miete_stadtteil.plot(kind="bar", color="skyblue")
plt.ylabel("Miete pro m² (€)")
plt.title("Durchschnittliche Miete pro m² nach Stadtteil (Berlin)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


#oder


sns.jointplot(
    data=df,
    x="wohnflaeche",
    y="gesamt_miete",
    kind="scatter",   # scatter, kde, reg, hex
    height=6,

)
plt.show()
# -------------------------------
# 2. Einfluss der Wohnfläche auf die Miete
    #wie Wohnfläche die Grundmiete beeinflusst.
    # Unterschiede zwischen Stadtteilen.
    #Ausreißer (sehr teure oder sehr große Wohnungen) werden sichtbar.
    #die Stadtteile filtert, z. B. nur Innenstadt vs. Randbezirke, direkt in diesem Scatterplot.
# -------------------------------
# Definieren der Innenstadt-Bezirke
innenstadt = ["Mitte", "Kreuzberg", "Charlottenburg", "Prenzlauer_Berg"]

# Neue Spalte 'lage' erstellen: "Innenstadt" oder "Rand"
df["lage"] = df["region3"].apply(lambda x: "Innenstadt" if any(i in str(x) for i in innenstadt) else "Rand")

# Scatterplot mit Farbunterscheidung nach Lage

sns.lmplot(
    data=df,
    x="wohnflaeche",
    y="grundmiete",
    hue="lage",          # Farbe nach Lage (Innenstadt / Rand)
    height=6,
    aspect=2,
    scatter_kws={"alpha":0.6, "s":50},
    markers="o",
    ci=None
)

plt.title("Wohnfläche vs. Grundmiete: Innenstadt vs. Randbezirke")
plt.xlabel("Wohnfläche (m²)")
plt.ylabel("Grundmiete (€)")
plt.show()
# -------------------------------
#  Innenstadt vs. Randbezirke
# -------------------------------

#  Innenstadt vs. Randbezirke definieren
innenstadt = ["Mitte", "Kreuzberg", "Charlottenburg", "Prenzlauer_Berg"]
df["lage"] = df["region3"].apply(lambda x: "Innenstadt" if x in innenstadt else "Rand")

#  Plot erstellen
plt.figure(figsize=(12, 6))

# Boxplot (Verteilung der Mieten)
sns.boxplot(data=df, x="lage", y="miete_pro_m2", palette="Set2", showfliers=False)

# Einzelne Datenpunkte hinzufügen
sns.stripplot(data=df, x="lage", y="miete_pro_m2", color="gray", alpha=0.5, jitter=True)

# Mittelwert pro Gruppe berechnen und hinzufügen
group_means = df.groupby("lage")["miete_pro_m2"].mean().reset_index()
sns.scatterplot(data=group_means, x="lage", y="miete_pro_m2", color="red", s=100, marker="D", label="Mittelwert")

# Titel und Achsenbeschriftungen
plt.title("Vergleich: Innenstadt vs. Randbezirke", fontsize=16)
plt.ylabel("Miete pro m² (€)", fontsize=12)
plt.xlabel("Lage", fontsize=12)
plt.legend()
plt.show()

# Kategorie in numerische Werte umwandeln
df["lage_num"] = df["lage"].map({"Innenstadt": 1, "Rand": 2})




#  Ausreißer bei Miete pro m²
# -------------------------------
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, y="miete_pro_m2")
plt.title("Ausreißer bei Miete pro m²")
plt.show()

# -------------------------------
#  Korrelationen
# -------------------------------
corr = df[["grundmiete", "gesamt_miete", "wohnflaeche", "zimmer", "nebenkosten"]].corr()
print("\n🔗 Korrelationen:\n", corr)

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Korrelationsmatrix")
plt.show()




'''