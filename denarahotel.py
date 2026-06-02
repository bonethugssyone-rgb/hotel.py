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
        if "total" in r:
            total += r["total"]
    return total

def cek_kamar(no_kamar):
    for r in st.session_state.reservasi:
        if r["kamar"] == no_kamar:
            return False
    return True

# =========================
# MENU
# =========================
menu = st.sidebar.selectbox("Menu", [
    "Dashboard",
    "Tambah Reservasi",
    "Cek Kamar",
    "Daftar Reservasi",
    "Cari Reservasi",
    "Edit Reservasi",
    "Hapus Reservasi",
    "Pembayaran & Struk"
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
                "total": total,
                "status": "Belum Lunas"
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

                # hitung ulang
                hari = hitung_hari(checkin, checkout)
                total = hitung_biaya(r["tipe"], hari)

                r["hari"] = hari
                r["total"] = total

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
# 8. PEMBAYARAN & STRUK
# =========================
elif menu == "Pembayaran & Struk":
    st.title("💳 Pembayaran & Struk")

    if not st.session_state.reservasi:
        st.warning("Belum ada reservasi")
    else:
        kamar = st.number_input("Masukkan Nomor Kamar")

        data_ditemukan = None
        for r in st.session_state.reservasi:
            if r["kamar"] == kamar:
                data_ditemukan = r
                break

        if data_ditemukan:
            st.subheader("Detail Reservasi")
            st.write(f"Nama : {data_ditemukan['nama']}")
            st.write(f"Kamar : {data_ditemukan['kamar']}")
            st.write(f"Tipe : {data_ditemukan['tipe']}")
            st.write(f"Lama Inap : {data_ditemukan['hari']} hari")
            st.write(f"Total : Rp {data_ditemukan['total']:,}")
            st.write(f"Status : {data_ditemukan.get('status','Belum Lunas')}")

            metode = st.selectbox("Metode Pembayaran", ["Cash", "Transfer"])
            bayar = st.number_input("Jumlah Bayar", min_value=0)

            if st.button("Bayar"):
                if bayar < data_ditemukan["total"]:
                    st.error("Uang kurang!")
                else:
                    kembalian = bayar - data_ditemukan["total"]

                    data_ditemukan["metode"] = metode
                    data_ditemukan["bayar"] = bayar
                    data_ditemukan["kembalian"] = kembalian
                    data_ditemukan["status"] = "Lunas"

                    st.success("Pembayaran berhasil")

                    struk = f"""
==============================
        HOTEL PYTHON
==============================
Nama        : {data_ditemukan['nama']}
Kamar       : {data_ditemukan['kamar']}
Tipe        : {data_ditemukan['tipe']}
Check In    : {data_ditemukan['checkin']}
Check Out   : {data_ditemukan['checkout']}
Lama Inap   : {data_ditemukan['hari']} hari

------------------------------
Total       : Rp {data_ditemukan['total']:,}
Bayar       : Rp {bayar:,}
Kembalian   : Rp {kembalian:,}
Metode      : {metode}
Status      : LUNAS
==============================
   TERIMA KASIH 🙏
==============================
"""

                    st.text(struk)

                    st.download_button(
                        label="Download Struk",
                        data=struk,
                        file_name=f"struk_kamar_{kamar}.txt"
                    )

        else:
            st.error("Data tidak ditemukan")
