import streamlit as st
import pandas as pd

# Safe thresholds
SAFE_LIMITS = {
    "pH": (6.5, 7.5),
    "Ammonia (NH3)": (0, 0.02),
    "Nitrite (NO2-)": (0, 0.5),
    "Nitrate (NO3-)": (0, 40),
    "Temperature (°C)": (22, 28),
    "Dissolved Oxygen (mg/L)": (5, float('inf'))
}

st.title("🐟 Aquarium Water Quality Checker")

uploaded_file = st.file_uploader("Upload your water quality CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    def check_safety(param, value):
        if param in SAFE_LIMITS:
            low, high = SAFE_LIMITS[param]
            return "✅ Safe" if low <= value <= high else "❌ Unsafe"
        return "Unknown"

    df["Status"] = df.apply(lambda row: check_safety(row["Parameter"], row["Value"]), axis=1)

    def color_status(val):
        return f"color: {'green' if val == '✅ Safe' else 'red'}; font-weight: bold"

    st.dataframe(df.style.applymap(color_status, subset=["Status"]))
else:
    st.info("Please upload a CSV file.")
