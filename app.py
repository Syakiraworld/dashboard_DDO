import streamlit as st
import pandas as pd
import os
from PIL import Image
import mammoth
from docx import Document

st.set_page_config(page_title="Dashboard Dealer", layout="wide")

st.title("📊 Dashboard Dealer")

BASE_PATH = "data_dealer"

# ===============================
# VALIDASI PATH
# ===============================
if not os.path.exists(BASE_PATH):
    st.error(f"Folder '{BASE_PATH}' tidak ditemukan!")
    st.stop()

# ===============================
# AMBIL FOLDER DEALER
# ===============================
dealers = [
    d for d in os.listdir(BASE_PATH)
    if os.path.isdir(os.path.join(BASE_PATH, d))
]

if not dealers:
    st.warning("Tidak ada folder dealer")
    st.stop()

selected_dealer = st.selectbox("Pilih Dealer", dealers)

dealer_path = os.path.join(BASE_PATH, selected_dealer)

# ===============================
# AMBIL FILE DALAM FOLDER
# ===============================
files = os.listdir(dealer_path)

if not files:
    st.warning("Folder kosong")
    st.stop()

selected_file = st.selectbox("Pilih File", files)

file_path = os.path.join(dealer_path, selected_file)

st.subheader(f"📁 {selected_dealer} → {selected_file}")

# ===============================
# HANDLE BERDASARKAN TIPE FILE
# ===============================

# CSV
if selected_file.endswith(".csv"):
    df = pd.read_csv(file_path)
    st.dataframe(df)

    if len(df.columns) >= 2:
        col1 = st.selectbox("Kolom X", df.columns, key="csv_x")
        col2 = st.selectbox("Kolom Y", df.columns, key="csv_y")
        st.line_chart(df[[col1, col2]])

# EXCEL
elif selected_file.endswith(".xlsx"):
    df = pd.read_excel(file_path)
    st.dataframe(df)

    if len(df.columns) >= 2:
        col1 = st.selectbox("Kolom X", df.columns, key="xls_x")
        col2 = st.selectbox("Kolom Y", df.columns, key="xls_y")
        st.bar_chart(df[[col1, col2]])

# GAMBAR
elif selected_file.lower().endswith((".png", ".jpg", ".jpeg")):
    image = Image.open(file_path)
    st.image(image, caption=selected_file, use_container_width=True)

# PDF
elif selected_file.endswith(".pdf"):
    with open(file_path, "rb") as f:
        st.download_button(
            label="📥 Download PDF",
            data=f,
            file_name=selected_file,
            mime="application/pdf"
        )

# DOCX (pakai mammoth → HTML)
elif selected_file.endswith(".docx"):
    with open(file_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value

    st.markdown(html, unsafe_allow_html=True)

    # opsi download juga
    with open(file_path, "rb") as f:
        st.download_button(
            label="📥 Download DOCX",
            data=f,
            file_name=selected_file
        )

# FORMAT LAIN
else:
    st.warning("Format file tidak didukung")