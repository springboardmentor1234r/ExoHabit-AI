import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# --- 1. SET UP PAGE ---
st.set_page_config(page_title="Exoplanet Habitability Dashboard", layout="wide")

# Corrected parameter: unsafe_allow_html
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { color: #00CC96; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌌 Exoplanet Habitability Analysis")
st.markdown("Exploring candidate worlds using NASA Exoplanet Archive parameters.")

# --- 2. DATA LOADING ---
@st.cache_data
def load_data():
    path = r"D:\Exo_Habit-AI\processed_exoplanets.csv"
    data = pd.read_csv(path)
    
    # Logic to ensure habitability_score exists
    if 'habitability_score' not in data.columns:
        # Fallback scoring: Normalized proximity to Earth-like conditions
        # Earth eq_temp approx 255K, Earth radius = 1.0
        temp_score = 1 / (1 + (data['pl_eqt'] - 255).abs())
        rad_score = 1 / (1 + (data['pl_rade'] - 1).abs())
        data['habitability_score'] = (temp_score + rad_score) / 2
        # Scale 0 to 1
        data['habitability_score'] = (data['habitability_score'] - data['habitability_score'].min()) / (data['habitability_score'].max() - data['habitability_score'].min())
    
    return data

try:
    df = load_data()
    
    # --- 3. SIDEBAR / FILTERS ---
    st.sidebar.header("Filter Candidates")
    score_range = st.sidebar.slider("Habitability Score Range", 0.0, 1.0, (0.5, 1.0))
    
    filtered_df = df[
        (df['habitability_score'] >= score_range[0]) & 
        (df['habitability_score'] <= score_range[1])
    ].sort_values('habitability_score', ascending=False)

    # --- 4. TOP METRICS ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Planets Analyzed", len(df))
    m2.metric("High Potential Candidates", len(filtered_df))
    m3.metric("Avg Stellar Temp", f"{int(df['st_teff'].mean())} K")

    # --- 5. DASHBOARD LAYOUT ---
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("Habitability Score Distribution")
        fig_dist = px.histogram(df, x="habitability_score", 
                                 nbins=30, 
                                 color_discrete_sequence=['#00CC96'],
                                 template="plotly_dark",
                                 labels={'habitability_score': 'Habitability Score'})
        st.plotly_chart(fig_dist, use_container_width=True)

    with row1_col2:
        st.subheader("Star Temp vs. Planet Radius")
        # Visualizing the 'Goldilocks' relationship
        fig_scatter = px.scatter(filtered_df, x="st_teff", y="pl_rade",
                                 size="pl_insol" if "pl_insol" in df.columns else None,
                                 color="habitability_score",
                                 hover_name="pl_name" if "pl_name" in df.columns else None,
                                 template="plotly_dark",
                                 labels={'st_teff': 'Star Temp (K)', 'pl_rade': 'Planet Radius (Earth=1)'},
                                 color_continuous_scale='Viridis')
        st.plotly_chart(fig_scatter, use_container_width=True)

    

    st.divider()

    # --- 6. DATA TABLE & EXPORT ---
    st.subheader("📋 Top Candidate Explorer")
    
    # Select specific columns for the display table
    display_cols = ['habitability_score', 'sy_dist', 'pl_rade', 'pl_eqt', 'pl_orbper']
    if 'pl_name' in df.columns:
        display_cols.insert(0, 'pl_name')

    st.dataframe(filtered_df[display_cols].head(20), use_container_width=True)

    # Excel Export Logic
    def to_excel(data):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            data.to_excel(writer, index=False, sheet_name='Habitability_Results')
        return output.getvalue()

    st.download_button(
        label="📥 Export These Candidates to Excel",
        data=to_excel(filtered_df),
        file_name="habitability_report.xlsx",
        mime="application/vnd.ms-excel"
    )

except Exception as e:
    st.error(f"Dashboard Error: {e}")