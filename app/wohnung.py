import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.style import css
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

from modeling.KNN_1 import load_data, train_model, predict_rent, plot_knn_with_new
from utils.sqlabfrage import ( 
    top_bezirke,  heizung_analysen,
    balkon_analysen, zimmer_verteilung, 
    kueche_analysen, haustiere_analysen,

)

st.set_page_config(
    page_title="Berlin Rent Predictor",
    layout="wide"
)
st.markdown(css, unsafe_allow_html=True)
st.title("Berlin Miete Vorhersage")

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2 ,tab3 = st.tabs([" Prediction","visualisierung", "SQL Abfragen und analyse"])

# -----------------------------
# TAB 1: Prediction
# -----------------------------
with tab1:
    try:
        df = load_data()
        df, model, X_train, y_train, X_test, y_test = train_model(df)

        st.sidebar.header("Wohnung Details")
        bezirk_options = sorted(df['region3'].unique())
        wohnungstyp_options = sorted(df['wohnungstyp'].unique())
        boolean_options = ['TRUE', 'FALSE']

        wohnflaeche = st.sidebar.slider("Wohnfläche (m²)",
            min_value=int(df['wohnflaeche'].min()),
            max_value=int(df['wohnflaeche'].max()),
            value=75
        )
        zimmer = st.sidebar.slider("Zimmer",
            min_value=int(df['zimmer'].min()),
            max_value=int(df['zimmer'].max()),
            value=3
        )
        baujahr = st.sidebar.slider("Baujahr",
            min_value=int(df['baujahr'].min()),
            max_value=int(df['baujahr'].max()),
            value=1995
        )
        bezirk = st.sidebar.selectbox("Bezirk", bezirk_options)
        wohnungstyp = st.sidebar.selectbox("Wohnungstyp", wohnungstyp_options)
        balkon = st.sidebar.selectbox("Balkon", boolean_options, index=0)
        aufzug = st.sidebar.selectbox("Aufzug", boolean_options, index=0)
        garten = st.sidebar.selectbox("Garten", boolean_options, index=1)

        if st.sidebar.button("Predict Rent"):
            neue_wohnung = pd.DataFrame([{
                "wohnflaeche": wohnflaeche,
                "zimmer": zimmer,
                "baujahr": baujahr,
                "bezirk": bezirk,
                "wohnungstyp": wohnungstyp,
                "balkon": balkon,
                "aufzug": aufzug,
                "garten": garten
            }])

            prediction = predict_rent(model, neue_wohnung)
            st.subheader("Wohnung Miete")
            st.metric(label="Vorhersage (Grundmiete)", value=f"{prediction:.2f} €")

            st.subheader("Model Performance")
            col1, col2 = st.columns(2)
            with col1:
                y_pred = model.predict(X_test)
                mse = mean_squared_error(y_test, y_pred)
                st.metric("Mean Squared Error", f"{mse:.2f}")
            with col2:
                r2 = r2_score(y_test, y_pred)
                st.metric("R² Score", f"{r2:.3f}")

            st.subheader("Rent Prediction Visualization")
            fig, pred_value = plot_knn_with_new(model, X_train, y_train, neue_wohnung)
            st.pyplot(fig)

        if st.checkbox("Show sample data"):
            st.subheader("Sample Data")
            st.dataframe(df.head(10))

    except FileNotFoundError:
        st.error("Data file not found. Please make sure 'data/berlin_data_clean.csv' exists.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


with tab2:
    import eda.plots as plot
    st.subheader("Analyse")
    plot.run_plots()
    
with tab3:
    st.subheader(" SQL-basierte Analysen")
    option = st.selectbox("Wähle eine Analyse:", [
        "Top Bezirke",
        "Heizungstypen",
        "Balkon",
        "Zimmerverteilung",
        "Küche",
        "Haustiere",
  
    ])

    if option == "Top Bezirke":
        st.dataframe(top_bezirke(df, plot=True))
    elif option == "Heizungstypen":
        st.dataframe(heizung_analysen(df, plot=True))
    elif option == "Balkon":
        st.dataframe(balkon_analysen(df, plot=True))
    elif option == "Zimmerverteilung":
        st.dataframe(zimmer_verteilung(df, plot=True))
    elif option == "Küche":
        st.dataframe(kueche_analysen(df, plot=True))
    elif option == "Haustiere":
        st.dataframe(haustiere_analysen(df, plot=True))
