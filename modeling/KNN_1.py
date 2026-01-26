# KNN_1.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsRegressor
from sklearn.impute import SimpleImputer

# -----------------------------
# 1. Daten laden
# -----------------------------
def load_data(path="data/berlin_data_clean.csv"):
    """
    Lädt die Berlin-Daten aus CSV und gibt ein DataFrame zurück.
    """
    df = pd.read_csv(path)
    return df

#################################################################################
def remove_outliers(df, column_list):
    """
    Entfernt Ausreißer aus df basierend auf IQR für die angegebenen Spalten.
    """
    df_clean = df.copy()
    for col in column_list:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df_clean = df_clean[(df_clean[col] >= lower) & (df_clean[col] <= upper)]
    return df_clean

######################################################################################
# 2. Modell trainieren
def train_model(df):
    """
    Trainiert ein KNN-Modell auf den Daten und gibt Trainings- und Testdaten zurück.
    """
    numerical_features = ["wohnflaeche", "zimmer", "baujahr"]
    categorical_features = ["bezirk", "wohnungstyp", "balkon", "aufzug", "garten"]

    # Ausreißer entfernen
    df_clean = remove_outliers(df, numerical_features + ["grundmiete"])  # besser auch grundmiete prüfen

    y = df_clean["grundmiete"]
    X = df_clean[numerical_features + categorical_features]

    # Preprocessing Pipelines
    num_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    cat_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])
    preprocessor = ColumnTransformer([
        ("num", num_transformer, numerical_features),
        ("cat", cat_transformer, categorical_features)
    ])

    # Modell-Pipeline
    model = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", KNeighborsRegressor(n_neighbors=5))
    ])

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Modell trainieren
    model.fit(X_train, y_train)

    return df_clean, model, X_train, y_train, X_test, y_test

def predict_rent(model, apartment_df):
    """ Gibt die vorhergesagte Grundmiete für eine neue Wohnung zurück. """ 
    return model.predict(apartment_df)[0]



# -----------------------------
# 4. Visualisierung
# -----------------------------
def plot_knn_with_new(model, X, y, new_apartment, feature_x="wohnflaeche", feature_y="zimmer"):
    """
    Visualisierung der KNN-Vorhersage für zwei Features mit einer neuen Wohnung als Marker.
    Gibt die matplotlib-Figur und die vorhergesagte Miete zurück.
    """
    import matplotlib.pyplot as plt

    # Nur die zwei Features für die Visualisierung
    X_vis = X[[feature_x, feature_y]].copy()
    y_vis = y.copy()

    # KNN auf zwei Features trainieren
    knn_vis = KNeighborsRegressor(n_neighbors=5)
    knn_vis.fit(X_vis, y_vis)

    # Meshgrid für Hintergrundvorhersage
    h = 1
    x_min, x_max = X_vis[feature_x].min() - 5, X_vis[feature_x].max() + 5
    y_min, y_max = X_vis[feature_y].min() - 1, X_vis[feature_y].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    Z = knn_vis.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

    # Plot erstellen
    fig, ax = plt.subplots(figsize=(12,8))
    contour = ax.contourf(xx, yy, Z, cmap="coolwarm", alpha=0.4)
    scatter = ax.scatter(X_vis[feature_x], X_vis[feature_y], c=y_vis, cmap="coolwarm",
                         s=50, edgecolor="k", label="Bestehende Wohnungen")

    # Neue Wohnung markieren
    new_x = new_apartment[feature_x].values[0]
    new_y = new_apartment[feature_y].values[0]
    new_pred = model.predict(new_apartment)[0]
    ax.scatter(new_x, new_y, c='yellow', s=200, edgecolor='k', marker='*', label=f"Neue Wohnung: {new_pred:.2f} €")

    plt.colorbar(scatter, ax=ax, label="Grundmiete (€)")
    ax.set_xlabel(feature_x)
    ax.set_ylabel(feature_y)
    ax.set_title("KNN Regression: Vorhersage der Grundmiete mit neuer Wohnung")
    ax.legend()

    return fig, new_pred

'''
    plt.show()
    # Vorhersage im Terminal ausgeben
    print(f"🔮 Vorhergesagte Grundmiete für die neue Wohnung: {new_pred:.2f} €")
# -----------------------------
# 6. Neue Wohnung Beispiel
# -----------------------------
neue_wohnung = pd.DataFrame([{
    "wohnflaeche": 75,
    "zimmer": 3,
    "baujahr": 1995,
    "bezirk": "Charlottenburg",
    "wohnungstyp": "apartment",
    "balkon": "TRUE",
    "aufzug": "TRUE",
    "garten": "FALSE"
}])

# Plot erstellen
plot_knn_with_new(model, X_train, y_train, neue_wohnung)
'''