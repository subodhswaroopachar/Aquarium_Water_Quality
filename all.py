import streamlit as st
import pandas as pd

# Required columns and acceptable ranges
REQUIRED_COLUMNS = {
    "pH": (6.5, 8.5),
    "Ammonia (ppm)": (0, 0.5),
    "Nitrite (ppm)": (0, 0.3),
    "Nitrate (ppm)": (0, 50),
    "Temperature (°C)": (0, 35),
    "Dissolved Oxygen (mg/L)": (4, 8)
}

st.title("Water Quality Validation Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Check missing columns
    missing_cols = [col for col in REQUIRED_COLUMNS.keys() if col not in df.columns]
    if missing_cols:
        st.error(f"Missing required columns: {', '.join(missing_cols)}")
    else:
        st.success("✅ All required columns are present.")

        # Function to color cells
        def highlight_cells(val, col_name):
            min_val, max_val = REQUIRED_COLUMNS[col_name]
            if pd.isna(val):
                color = "gray"
            elif min_val <= val <= max_val:
                color = "lightgreen"
            else:
                color = "lightcoral"
            return f"background-color: {color}"

        # Apply styling for each required column
        styled_df = df.style
        for col in REQUIRED_COLUMNS.keys():
            styled_df = styled_df.applymap(lambda v: highlight_cells(v, col), subset=[col])

        st.write("### Validated Dataset")
        st.dataframe(styled_df, use_container_width=True)
else:
    st.info("📂 Please upload a CSV file with the required parameters.")
