import streamlit as st
from mobile_number_service import process_uploaded_file
import pandas as pd
st.title("Customer Mobile Number Processing")
st.write(
    """
    This application processes customer mobile numbers from uploaded CSV or Excel files.
    It matches the mobile numbers with the customer master data and returns the processed file.
    """
)

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xls", "xlsx"])

if uploaded_file:
    st.success("File uploaded successfully.")
    if st.button("Process File"):
        try:
            processed_io, download_name, mime_type = process_uploaded_file(
                uploaded_file,
                uploaded_file.name
            )
            st.download_button(
                label="📥 Download Processed File",
                data=processed_io,
                file_name=download_name,
                mime=mime_type
            )
        except Exception as e:
            st.error(f"❌ Error: {e}")
