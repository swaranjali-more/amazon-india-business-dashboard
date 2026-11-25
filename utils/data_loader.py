import os
import pandas as pd
import streamlit as st

UPLOAD_SAVE_PATH = os.path.join("data", "uploaded_dataset")


def _read_tabular(source):
    name = getattr(source, "name", str(source)).lower()
    if name.endswith(".csv"):
        return pd.read_csv(source)
    xls = pd.ExcelFile(source)
    return pd.read_excel(xls, sheet_name=xls.sheet_names[0])


@st.cache_data(show_spinner=False)
def load_dataset(uploaded_file=None, default_path="Amazon Sales Data India.xlsx"):
    os.makedirs("data", exist_ok=True)
    try:
        if uploaded_file is not None:
            file_bytes = uploaded_file.getvalue()
            ext = ".csv" if uploaded_file.name.lower().endswith(".csv") else ".xlsx"
            persisted_path = f"{UPLOAD_SAVE_PATH}{ext}"
            with open(persisted_path, "wb") as f:
                f.write(file_bytes)
            df = _read_tabular(uploaded_file)
            return df, f"Uploaded: {uploaded_file.name}", None

        for candidate in [f"{UPLOAD_SAVE_PATH}.xlsx", f"{UPLOAD_SAVE_PATH}.csv", default_path]:
            if os.path.exists(candidate):
                df = _read_tabular(candidate)
                return df, f"Active Source: {os.path.basename(candidate)}", None

        return pd.DataFrame(), "No Source", "Default dataset not found. Upload a CSV or XLSX file."
    except Exception as exc:
        return pd.DataFrame(), "Load Error", f"Could not read dataset: {exc}"