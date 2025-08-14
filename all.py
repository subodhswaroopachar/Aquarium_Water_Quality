import streamlit as st
import pandas as pd

st.title("🐟 Fish Tank Water Quality Checker")

st.subheader("📋 Required Water Quality Parameters")

# Create the parameter table
params = [
    ["pH", "6.5 - 8.0"],
    ["Ammonia (ppm)", "0.0 - 0.25"],
    ["Nitrite (ppm)", "0.0 - 0.5"],
    ["Nitrate (ppm)", "0.0 - 40.0"],
    ["Temperature (°C)", "22 - 28"],
    ["Dissolved Oxygen (mg/L)", "5 - 8"],
]

df_params = pd.DataFrame(params, columns=["Parameter", "Ideal Range"])
st.table(df_params)  # ✅ Only one table now

# File uploader
uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])
