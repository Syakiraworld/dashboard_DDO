import streamlit as st
import pandas as pd
import os
import zipfile
from PIL import Image
import mammoth

st.set_page_config(page_title="Dashboard Dealer", layout="wide")

st.title("📊 Dashboard Dealer")

BASE_PATH = "data_dealer"

# ===============================
# BUAT FOLDER JIKA BELUM ADA
# ===============================
if not os.path.exists(BASE_PATH):
    os.makedirs(BASE_PATH)

# ===============================
# MENU
# ===============================
menu = st.sidebar.radio("Menu", ["📁 Data Dealer", "📦 Upload ZIP"])

# ===============================
# MENU 1: DATA DEALER
# ===============================
if menu == "📁 Data Dealer":

    dealers = [d for d in os.listdir(BASE_PATH)
               if os.path.isdir(os.path.join(BASE_PATH, d))]

    if not dealers:
        st.warning("Belum ada data dealer")
        st.stop()

    selected_dealer = st.selectbox("Pilih Dealer", dealers)

    dealer_path = os.path.join(BASE_PATH, selected_dealer)
    files = os.listdir(dealer_path)

    if not files:
        st.warning("Folder kosong")
        st.stop()

    selected_file = st.selectbox("Pilih File", files)
    file_path = os.path.join(dealer_path, selected_file)

# ===============================
# MENU 2: UPLOAD ZIP
# ===============================
else:
    uploaded_zip = st.file_uploader("Upload ZIP", type=["zip"])

    if uploaded_zip:
        with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
            zip_ref.extractall(BASE_PATH)

        st.success("ZIP berhasil diupload & diextract ke data_dealer ✅")

        st.info("Silakan pindah ke menu 'Data Dealer' untuk melihat data")
        st.stop()
    else:
        st.info("Upload file ZIP berisi folder dealer")
        st.stop()

# ===============================
# FUNCTION TAMPILKAN FILE
# ===============================
def tampilkan_file(path, nama_file):

    # CSV
    if nama_file.endswith(".csv"):
        df = pd.read_csv(path)
        st.dataframe(df)

        if len(df.columns) >= 2:
            col1 = st.selectbox("Kolom X", df.columns)
            col2 = st.selectbox("Kolom Y", df.columns)
            st.line_chart(df[[col1, col2]])

    # EXCEL
    elif nama_file.endswith(".xlsx"):
        df = pd.read_excel(path)
        st.dataframe(df)

    # GAMBAR
    elif nama_file.lower().endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(path)
        st.image(image, use_container_width=True)

    # PDF
    elif nama_file.endswith(".pdf"):
        with open(path, "rb") as f:
            st.download_button("📥 Download PDF", f, file_name=nama_file)

    # DOCX
    elif nama_file.endswith(".docx"):
        with open(path, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            st.markdown(result.value, unsafe_allow_html=True)

    else:
        st.warning("Format file tidak didukung")

# ===============================
# TAMPILKAN FILE
# ===============================
st.subheader(f"📄 {selected_file}")
tampilkan_file(file_path, selected_file)