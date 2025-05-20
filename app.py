import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Page config
st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS
st.markdown(
    """ 
    <style>
    .stApp {
        background-color: black;
        color: white;
    } 
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("Data Sweeper Sterling Integrator By Rida Amir")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization. Project for Quarter 3.")

# File uploader
uploaded_files = st.file_uploader(
    "Upload your files (accepts CSV or Excel):",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

# File processing
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read uploaded file
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.warning(f"Unsupported file type: {file_ext}")
            continue

        # Display preview
        st.subheader(f"Preview of {file.name}")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}", key=f"dedup_{file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}", key=f"fillna_{file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing values filled!")

        # Column selection
        st.subheader("Select Columns to Keep")
        selected_columns = st.multiselect(
            f"Choose columns for {file.name}",
            df.columns.tolist(),
            default=df.columns.tolist(),
            key=f"columns_{file.name}"
        )
        df = df[selected_columns]

        # Data visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}", key=f"viz_{file.name}"):
            st.bar_chart(df.select_dtypes(include="number"))

        # File conversion
        st.subheader("Conversion Options")
        conversion_type = st.radio(
            f"Convert {file.name} to:",
            ["CSV", "Excel"],
            key=f"conversion_{file.name}"
        )

        if st.button(f"Convert {file.name}", key=f"convert_{file.name}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                mime_type = "text/csv"
                output_file_name = file.name.replace(file_ext, ".csv")
            elif conversion_type == "Excel":
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Sheet1')
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                output_file_name = file.name.replace(file_ext, ".xlsx")

            buffer.seek(0)
            st.download_button(
                label=f"Download {output_file_name}",
                data=buffer,
                file_name=output_file_name,
                mime=mime_type
            )

# Final status
st.success("All files processed successfully!")
