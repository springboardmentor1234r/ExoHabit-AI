# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Load model and scaler
# -----------------------------
scaler = joblib.load("scaler_10feat.pkl")          # your 10-feature scaler
model = joblib.load("habitability_model_10feat.pkl")  # your 10-feature RandomForest

# -----------------------------
# Sidebar for navigation
# -----------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Prediction", "Dashboard"])

# -----------------------------
# Prediction Page
# -----------------------------
if page == "Prediction":
    st.title("🌍 Exoplanet Habitability Prediction")
    st.write("Enter exoplanet and star parameters to predict habitability:")

    # 10 input fields
    pl_rade = st.number_input("Planet Radius (Earth radii)", min_value=0.0)
    pl_bmasse = st.number_input("Planet Mass (Earth mass)", min_value=0.0)
    pl_orbper = st.number_input("Orbital Period (days)", min_value=0.0)
    pl_eqt = st.number_input("Equilibrium Temperature (K)", min_value=0.0)
    st_teff = st.number_input("Star Temperature (K)", min_value=0.0)
    st_mass = st.number_input("Star Mass (Solar mass)", min_value=0.0)
    st_rad = st.number_input("Star Radius (Solar radius)", min_value=0.0)
    sy_dist = st.number_input("System Distance (pc)", min_value=0.0)
    pl_insol = st.number_input("Planet Insolation Flux (Earth flux)", min_value=0.0)
    st_met = st.number_input("Star Metallicity", value=0.0)

    if st.button("Predict"):
        # Assemble input array
        X = np.array([[pl_rade, pl_bmasse, pl_orbper, pl_eqt,
                       st_teff, st_mass, st_rad, sy_dist,
                       pl_insol, st_met]])
        # Scale features
        X_scaled = scaler.transform(X)
        # Predict
        pred = model.predict(X_scaled)
        result = "Habitable ✅" if pred[0]==1 else "Not Habitable ❌"
        st.success(f"Prediction Result: {result}")

# -----------------------------
# Dashboard Page
# -----------------------------
if page == "Dashboard":
    st.title("🌌 Exoplanet Habitability Dashboard")

    # Load dataset
    df = pd.read_csv("exoplanet_full_dataset.csv", comment='#', low_memory=False)

    # Select the same 10 features + create habitable column
    selected_cols = ["pl_rade","pl_bmasse","pl_orbper","pl_eqt",
                     "st_teff","st_mass","st_rad","sy_dist",
                     "pl_insol","st_met"]
    df_selected = df[selected_cols].copy()

    # Create 'habitable' column
    df_selected['habitable'] = ((df_selected["pl_rade"]>=0.5) & 
                                (df_selected["pl_rade"]<=2.0) & 
                                (df_selected["pl_eqt"]>=180) & 
                                (df_selected["pl_eqt"]<=310)).astype(int)

    # Dataset preview
    st.subheader("Dataset Preview")
    st.dataframe(df_selected.head())

    # Habitable vs Non-Habitable Bar Chart
    st.subheader("Habitable vs Non-Habitable Count")
    fig, ax = plt.subplots()
    df_selected['habitable'].value_counts().plot(kind='bar', ax=ax, color=['orange','green'])
    ax.set_xticklabels(['Not Habitable','Habitable'], rotation=0)
    ax.set_ylabel("Count")
    st.pyplot(fig)

    # Pie Chart
    st.subheader("Habitable vs Non-Habitable Pie Chart")
    fig2, ax2 = plt.subplots()
    df_selected['habitable'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['orange','green'], labels=['Not Habitable','Habitable'])
    st.pyplot(fig2)

    # Scatter Plots
    st.subheader("Scatter Plots of Planet Radius vs Other Features")
    fig3, ax3 = plt.subplots(figsize=(8,5))
    scatter = ax3.scatter(df_selected['pl_rade'], df_selected['pl_bmasse'], c=df_selected['habitable'], cmap='coolwarm', alpha=0.7)
    ax3.set_xlabel("Planet Radius (Earth radii)")
    ax3.set_ylabel("Planet Mass (Earth mass)")
    st.pyplot(fig3)

    # Histogram
    st.subheader("Histogram of Planet Radius")
    fig4, ax4 = plt.subplots()
    ax4.hist(df_selected['pl_rade'], bins=20, color='skyblue', edgecolor='black')
    ax4.set_xlabel("Planet Radius")
    ax4.set_ylabel("Count")
    st.pyplot(fig4)

    # Correlation Heatmap
    st.subheader("Feature Correlation Heatmap")
    fig5, ax5 = plt.subplots(figsize=(10,6))
    sns.heatmap(df_selected.corr(), annot=True, cmap="coolwarm", ax=ax5)
    st.pyplot(fig5)
