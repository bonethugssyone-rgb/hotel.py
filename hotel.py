import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Reservasi Hotel", layout="wide")

st.title("🏨 Sistem Reservasi Hotel Modern")

# ========================
# LOAD DATA (CSV)
# ========================
file = "data_reservasi.csv"

if os.path.exists(file):
    df = pd.read_csv(file)
else:
    df = pd.DataFrame(columns=["nama", "kamar", "tipe", "lama", "total"])

# ========================
# SIDEBAR MENU
# ========================
menu = st.sidebar.selectbox("Menu", [
    "Booking",
    "Data Reservasi",
    "Cari",
    "Hapus",
    "Statistik"
])

harga_kamar = {
    "Standard": 100000,
    "Deluxe": 150000,
    "VIP": 250000
}

# ========================
# BOOKING
# ========================
if menu == "Booking":
    st.subheader("➕ Booking Hotel")

    col1, col2 = st.columns(2)

    with col1:
        nama = st.text_input("Nama")
        tipe = st.selectbox("Tipe Kamar", list(harga_kamar.keys()))

    with col2:
        kamar = st.number_input("Nomor Kamar", 1, 100)
        lama = st.number_input("Lama Inap (hari)", 1, 30)

    # rekomendasi kamar
    semua_kamar = list(range(1, 21))
    terpakai = df["kamar"].tolist()
    tersedia = [k for k in semua_kamar if k not in terpakai]

    st.info(f"💡 Rekomendasi kamar kosong: {tersedia[:5]}")

    if st.button("Booking"):
        if kamar in terpakai:
            st.error("❌ Kamar sudah terisi!")
        else:
            total = harga_kamar[tipe] * lama

            data_baru = {
                "nama": nama,
                "kamar": kamar,
                "tipe": tipe,
                "lama": lama,
                "total": total
            }

            df = pd.concat([df, pd.DataFrame([data_baru])], ignore_index=True)
            df.to_csv(file, index=False)

            st.success("✅ Booking berhasil!")

            st.write("### 🧾 Invoice")
            st.write(data_baru)

# ========================
# DATA
# ========================
elif menu == "Data Reservasi":
    st.subheader("📋 Data Reservasi")

    if not df.empty:
        st.dataframe(df)
    else:
        st.warning("Belum ada data")

# ========================
# CARI
# ========================
elif menu == "Cari":
    st.subheader("🔍 Cari Data")

    keyword = st.text_input("Masukkan nama")

    hasil = df[df["nama"].str.contains(keyword, case=False, na=False)]

    if not hasil.empty:
        st.dataframe(hasil)
    else:
        st.warning("Data tidak ditemukan")

# ========================
# HAPUS
# ========================
elif menu == "Hapus":
    st.subheader("❌ Hapus Data")

    nama = st.text_input("Nama yang dihapus")

    if st.button("Hapus"):
        df = df[df["nama"] != nama]
        df.to_csv(file, index=False)
        st.success("Data berhasil dihapus")

# ========================
# STATISTIK
# ========================
elif menu == "Statistik":
    st.subheader("📊 Statistik")

    total_user = len(df)
    total_uang = df["total"].sum()

    col1, col2 = st.columns(2)

    col1.metric("Total Reservasi", total_user)
    col2.metric("Total Pendapatan", f"Rp {total_uang}")

    if not df.empty:
        st.subheader("Grafik Tipe Kamar")
        chart = df["tipe"].value_counts()
        st.bar_chart(chart)