import streamlit as st
import pandas as pd

# ✅ Required columns and their safe ranges
required_columns = {
    "pH": (6.5, 8.5),
    "Ammonia (ppm)": (0, 0.02),
    "Nitrite (ppm)": (0, 0.5),
    "Nitrate (ppm)": (0, 50),
    "Temperature (°C)": (20, 30),
    "Dissolved Oxygen (mg/L)": (5, 12)
}

st.title("🐟 Fish Tank Water Quality Checker")

# 📋 Show parameter requirements before upload
st.subheader("Required Parameters & Safe Ranges")
req_df = pd.DataFrame([
    {"Parameter": col, "Safe Range": f"{rng[0]} - {rng[1]}"}
    for col, rng in required_columns.items()
])
st.table(req_df)

uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # ✅ Check required columns
    st.subheader("Required Columns Check")
    col_status = []
    for col in required_columns.keys():
        col_status.append({
            "Column": col,
            "Status": "✅ Present" if col in df.columns else "❌ Missing"
        })
    status_df = pd.DataFrame(col_status)

    # Color code for required columns table
    def color_required(val):
        color = "green" if "Present" in val else "red"
        return f"color: {color}; font-weight: bold"

    st.dataframe(status_df.style.applymap(color_required, subset=["Status"]))

    # ✅ Check if all required columns are present
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        st.error(f"Missing required columns: {', '.join(missing)}")
    else:
        st.subheader("Parameter Value Checks")
        
        # Add Class column based on overall safety
        def classify_row(row):
            for col, (low, high) in required_columns.items():
                if row[col] < low or row[col] > high:
                    return "❌ Unsafe"
            return "✅ Safe"

        df["Class"] = df.apply(classify_row, axis=1)

        # Color-code based on value ranges
        def color_value(val, col):
            if col == "Class":
                return "color: green; font-weight: bold" if "Safe" in val else "color: red; font-weight: bold"
            if col in required_columns:
                min_val, max_val = required_columns[col]
                return "color: green; font-weight: bold" if min_val <= val <= max_val else "color: red; font-weight: bold"
            return ""

        styled_df = df.style.apply(
            lambda col: [color_value(v, col.name) for v in col]
        )

        st.dataframe(styled_df)
