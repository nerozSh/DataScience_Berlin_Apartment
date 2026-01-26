import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


# 1. Daten einlesen
df = pd.read_csv('data/berlin_data_clean.csv')

# Balkone, Aufzug, Garten in numerische Werte umwandeln
df['balkon_num'] = df['balkon'].astype(int)
df['aufzug_num'] = df['aufzug'].astype(int)
df['garten_num'] = df['garten'].astype(int)

# Neue Feature: Wohnfläche pro Zimmer
df['wohnflaeche_pro_zimmer'] = df['wohnflaeche'] / df['zimmer'].replace(0,1)

# Neue Spalte "Lage": Innenstadt vs. Rand
innenstadt = ["Mitte", "Kreuzberg", "Charlottenburg", "Prenzlauer_Berg"]
df['lage'] = df['region3'].apply(lambda x: "Innenstadt" if any(i in str(x) for i in innenstadt) else "Rand")


# 2. Features vorbereiten

features = ['wohnflaeche_pro_zimmer', 'baujahr', 'balkon_num', 'aufzug_num', 'garten_num']
X = df[features].fillna(0)
y = df['grundmiete'].fillna(0)


# 3. Features skalieren

scaler = StandardScaler()#1.Alle Features werden auf denselben Maßstab gebracht (Mittelwert = 0, Standardabweichung = 1).
                         #2.Vorteil: Die Koeffizienten sind vergleichbarer, und Algorithmen  funktionieren stabiler.
X_scaled = scaler.fit_transform(X)

# 4. Trainings- und Testdaten

X_train, X_test, y_train, y_test, df_train, df_test = train_test_split(
    X_scaled, y, df[['lage', 'wohnflaeche']], test_size=0.2, random_state=42
)


# 5. Lineares Regressionsmodell trainieren

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)


# 6. Scatterplot: Vorhersage vs. Realität

plt.figure(figsize=(12,7))

# Scatterplot mit Farbe nach Lage und Größe nach Wohnfläche
sns.scatterplot(
    x=y_test, 
    y=y_pred, 
    hue=df_test['lage'], 
    size=df_test['wohnflaeche'], 
    sizes=(20, 200),      # kleinster und größter Punkt
    palette=['blue','green'], 
    alpha=0.6
)

# Perfekte Vorhersage-Linie
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', linewidth=2)
plt.xlabel("Echte Grundmiete (€)")
plt.ylabel("Vorhergesagte Grundmiete (€)")
plt.title("Mehrdimensionale Regression: Vorhersage vs. Realität")
plt.legend(title='Lage', loc='upper left')
plt.show()


# 7. Modellleistung

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")
print(f"R² Score: {r2:.2f}")
print(df.columns)
#LinearRegression ist sehr schlecht für meine daten
#Modell nur 23 % der Varianz und die Fehler (MSE) sind immer noch sehr hoch.  das ist sehr schlecht weil Die gewählten Features (wohnflaeche, zimmer, baujahr, balkon, evtl. aufzug, garten) nicht stark genug die Miete erklären.