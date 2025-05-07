import streamlit as st
import pandas as pd
import os
from io import BytesIO
st.set_page_config(page_title="Data Sweeper",layout="wide")
# custom css
st.markdown(
    """ 
<style>
.stApp{
    background-color:black;
    color:white;
    } 
    </style>
    """,
    unsafe_allow_html=True
)
# Title and Description
st.title("Data Sweeper Sterling Integrator By Rida Amir")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and Visualization creating the project for quarter 3")
# file uploader
uploaded_files=st.file_uploader("Upload you files (accepts CSV or Excel):",type=["cvs","xlsx"],accept_multiple_files=(True))
if uploaded_files:
    for file in uploaded_files:
        files_ext=os.path.splitext(file.name)[-1].lower()
        if files_ext==".csv":
            df=pd.read_csv(file)
        elif files_ext==".xlsx":
            df=pd.read_excel(file)
        else:
            st.write(f"Unsupported File Type:{files_ext}")
            continue
        # file details
        st.write("Preview the head of the Dataframe")
        st.dataframe(df.head())
        # data cleaning options
        st.subheader("Data Cleaning options")
        if st.checkbox(f"clean data for{file.name}"):
            col1,col2=st.columns(2)
            with col1:
                st.button(f"Remove duplicates from file:{file.name}")
                df.drop_duplicates(inplace=True)
                st.write("duplicates removed!")
            with col2:
                st.button(f"Fill missing values for{file.name}");
                numeric_cols=df.select_dtypes(include=['number']).columns
                df[numeric_cols]=df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("missing values have been filled!")
        st.subheader("Select Colnumns to Keep")
        columns=st.multiselect(f"Choose columns for{file.name}",df.columns,default=df.columns)
        df=df[columns]
        # Data Visualization

st.subheader("Data Visualization")
if st.checkbox(f"Show Visualization for {file.name}"):
        st.bar_chart(df.select_dtypes(include="number").iloc[:,:])
        # conversion options
        st.subheader("Conversion Options")
        conversion_type=st.radio(f"Convert{file.name} to;"["CVS","Excel"],key=file.name)
        if st.button("Convert {file.name}"):
            buffer=BytesIO()
            if conversion_type=="CSV":
                df.to.csv(buffer,index=False)
                file_name=file.name.replace(files_ext,"xlsx")
                mime_type="text/csv"
            elif conversion_type=="Excel":
                df.to.to.excel(buffer,index=False)
                file_name=file.name.replace(files_ext,"xlsx")
                mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            st.download_button(
                label=f"Download{file_name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
st.succes("All files processed Successfuly!")
