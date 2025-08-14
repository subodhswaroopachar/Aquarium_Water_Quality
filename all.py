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
        
        # Color-code based on value ranges
        def color_value(val, col):
            min_val, max_val = required_columns[col]
            if min_val <= val <= max_val:
                return "color: green; font-weight: bold"
            else:
                return "color: red; font-weight: bold"

        styled_df = df.copy()
        styled_df = styled_df.style.apply(
            lambda col: [
                color_value(v, col.name) if col.name in required_columns else ""
                for v in col
            ]
        )

        st.dataframe(styled_df)
