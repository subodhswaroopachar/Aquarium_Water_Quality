import streamlit as st
import pandas as pd

# Required water quality parameters and ranges
required_params = {
    "pH": (6.5, 8.0),
    "Ammonia (ppm)": (0.0, 0.25),
    "Nitrite (ppm)": (0.0, 0.5),
    "Nitrate (ppm)": (0.0, 40.0),
    "Temperature (°C)": (22, 28),
    "Dissolved Oxygen (mg/L)": (5, 8)
}

st.title("Fish Tank Water Quality Checker")

# Display required columns in tabular format
st.subheader("Required Water Quality Parameters")
req_df = pd.DataFrame(
    [(param, f"{rng[0]} - {rng[1]}") for param, rng in required_params.items()],
    columns=["Parameter", "Ideal Range"]
)
st.table(req_df)

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Data")
    st.write(df)

    # Check for missing columns
    missing_cols = [col for col in required_params.keys() if col not in df.columns]
    if missing_cols:
        st.error(f"Missing required columns: {', '.join(missing_cols)}")
    else:
        st.success("All required columns are present ✅")

        # Validate values
        status = []
        for _, row in df.iterrows():
            row_status = "Green"
            for col, (low, high) in required_params.items():
                if row[col] < low or row[col] > high:
                    row_status = "Red"
                    break
            status.append(row_status)

        df["Status"] = status
        st.subheader("Water Quality Status")
        st.dataframe(df)
import streamlit as st
import pandas as pd

# Required water quality parameters and ranges
required_params = {
    "pH": (6.5, 8.0),
    "Ammonia (ppm)": (0.0, 0.25),
    "Nitrite (ppm)": (0.0, 0.5),
    "Nitrate (ppm)": (0.0, 40.0),
    "Temperature (°C)": (22, 28),
    "Dissolved Oxygen (mg/L)": (5, 8)
}

st.title("🐟 Fish Tank Water Quality Checker")

# Display required columns in tabular format
st.subheader("📋 Required Water Quality Parameters")
req_df = pd.DataFrame(
    [(param, f"{rng[0]} - {rng[1]}") for param, rng in required_params.items()],
    columns=["Parameter", "Ideal Range"]
)
st.table(req_df)

# File uploader
uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Uploaded Data")
    st.write(df)

    # Check for missing columns
    missing_cols = [col for col in required_params.keys() if col not in df.columns]
    if missing_cols:
        st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
    else:
        st.success("✅ All required columns are present")

        # Determine row status and highlight cells
        def highlight_cell(val, col):
            low, high = required_params[col]
            if low <= val <= high:
                return "background-color: lightgreen"
            else:
                return "background-color: salmon"

        # Check each row for overall status
        df["Status"] = df.apply(
            lambda row: "Green" if all(
                required_params[col][0] <= row[col] <= required_params[col][1]
                for col in required_params
            ) else "Red", axis=1
        )

        # Apply highlighting to individual parameter columns
        styled_df = df.style
        for col in required_params.keys():
            styled_df = styled_df.applymap(lambda v: highlight_cell(v, col), subset=[col])

        st.subheader("✅ Water Quality Check (Green = Safe, Red = Unsafe)")
        st.dataframe(styled_df, use_container_width=True)
