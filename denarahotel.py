import streamlit as st
import pandas as pd
from datetime import datetime

# =========================
# DATA (ARRAY / LIST)
# =========================
if "reservasi" not in st.session_state:
    st.session_state.reservasi = []

# Tarif kamar
harga_kamar = {
    "Standard": 300000,
    "Deluxe": 500000,
    "Suite": 800000
}

TOTAL_KAMAR = 50

# =========================
# FUNGSI
# =========================
def hitung_hari(checkin, checkout):
    return (checkout - checkin).days

def hitung_biaya(tipe, hari):
    return harga_kamar[tipe] * hari

def kamar_terisi():
    return len(st.session_state.reservasi)

def kamar_kosong():
    return TOTAL_KAMAR - kamar_terisi()

def total_pendapatan():
    total = 0
    for r in st.session_state.reservasi:
        total += r["total"]
    return total

def cek_kamar(no_kamar):
    for r in st.session_state.reservasi:
        if r["kamar"] == no_kamar:
            return False
    return True

# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.selectbox("Menu", [
    "Dashboard",
    "Tambah Reservasi",
    "Cek Kamar",
    "Daftar Reservasi",
    "Cari Reservasi",
    "Edit Reservasi",
    "Hapus Reservasi",
    "Laporan & Export"
])

# =========================
# 1. DASHBOARD
# =========================
if menu == "Dashboard":
    st.title("🏨 Dashboard Hotel")

    st.metric("Total Kamar", TOTAL_KAMAR)
    st.metric("Kamar Terisi", kamar_terisi())
    st.metric("Kamar Kosong", kamar_kosong())
    st.metric("Total Reservasi", len(st.session_state.reservasi))
    st.metric("Pendapatan", f"Rp {total_pendapatan():,}")

# =========================
# 2. TAMBAH RESERVASI
# =========================
elif menu == "Tambah Reservasi":
    st.title("➕ Tambah Reservasi")

    nama = st.text_input("Nama Tamu")
    kamar = st.number_input("Nomor Kamar", min_value=1, max_value=TOTAL_KAMAR)
    tipe = st.selectbox("Tipe Kamar", ["Standard", "Deluxe", "Suite"])
    checkin = st.date_input("Check In")
    checkout = st.date_input("Check Out")
    telp = st.text_input("Nomor Telepon")

    if st.button("Simpan"):
        if not cek_kamar(kamar):
            st.error("Kamar sudah terisi!")
        else:
            hari = hitung_hari(checkin, checkout)
            total = hitung_biaya(tipe, hari)

            data = {
                "nama": nama,
                "kamar": kamar,
                "tipe": tipe,
                "checkin": checkin,
                "checkout": checkout,
                "telp": telp,
                "hari": hari,
                "total": total
            }

            st.session_state.reservasi.append(data)
            st.success("Reservasi berhasil ditambahkan")

# =========================
# 3. CEK KAMAR
# =========================
elif menu == "Cek Kamar":
    st.title("🔍 Cek Ketersediaan Kamar")

    for i in range(1, TOTAL_KAMAR + 1):
        status = "Tersedia" if cek_kamar(i) else "Terisi"
        st.write(f"Kamar {i} : {status}")

# =========================
# 4. DAFTAR RESERVASI
# =========================
elif menu == "Daftar Reservasi":
    st.title("📋 Daftar Reservasi")

    if st.session_state.reservasi:
        df = pd.DataFrame(st.session_state.reservasi)
        st.dataframe(df)
    else:
        st.info("Belum ada data")

# =========================
# 5. CARI RESERVASI
# =========================
elif menu == "Cari Reservasi":
    st.title("🔎 Cari Reservasi")

    keyword = st.text_input("Masukkan Nama / Nomor Kamar")

    if keyword:
        hasil = []
        for r in st.session_state.reservasi:
            if keyword.lower() in r["nama"].lower() or keyword == str(r["kamar"]):
                hasil.append(r)

        if hasil:
            st.write(pd.DataFrame(hasil))
        else:
            st.warning("Data tidak ditemukan")

# =========================
# 6. EDIT RESERVASI
# =========================
elif menu == "Edit Reservasi":
    st.title("✏️ Edit Reservasi")

    kamar_edit = st.number_input("Masukkan Nomor Kamar")

    for r in st.session_state.reservasi:
        if r["kamar"] == kamar_edit:
            nama = st.text_input("Nama Baru", r["nama"])
            checkin = st.date_input("Check In Baru", r["checkin"])
            checkout = st.date_input("Check Out Baru", r["checkout"])

            if st.button("Update"):
                r["nama"] = nama
                r["checkin"] = checkin
                r["checkout"] = checkout
                st.success("Data berhasil diupdate")

# =========================
# 7. HAPUS RESERVASI
# =========================
elif menu == "Hapus Reservasi":
    st.title("❌ Hapus Reservasi")

    kamar_hapus = st.number_input("Masukkan Nomor Kamar")

    for r in st.session_state.reservasi:
        if r["kamar"] == kamar_hapus:
            if st.button("Hapus"):
                st.session_state.reservasi.remove(r)
                st.success("Reservasi berhasil dihapus")

# =========================
# 8. LAPORAN & EXPORT
# =========================
elif menu == "Laporan & Export":
    st.title("📊 Laporan")

    total_res = len(st.session_state.reservasi)
    total_uang = total_pendapatan()

    st.write(f"Total Reservasi : {total_res}")
    st.write(f"Pendapatan : Rp {total_uang:,}")

    if st.session_state.reservasi:
        df = pd.DataFrame(st.session_state.reservasi)

        # Export Excel
        file = "laporan_hotel.xlsx"
        df.to_excel(file, index=False)

        with open(file, "rb") as f:
            st.download_button(
                label="Download Excel",
                data=f,
                file_name="laporan_hotel.xlsx"
            )
