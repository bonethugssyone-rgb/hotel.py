
# ==========================================================
# DENARA HOTEL SYSTEM
# Sistem Reservasi Hotel Berbasis Array (List Python)
# Streamlit Project - Single File Version
# ==========================================================

import streamlit as st
import pandas as pd
from datetime import date

# ==========================================================
# KONFIGURASI HALAMAN
# ==========================================================
st.set_page_config(
    page_title="Denara Hotel",
    page_icon="🏨",
    layout="wide"
)

# ==========================================================
# TEMA PASTEL
# ==========================================================
st.markdown("""
<style>
.main {background-color:#FFF9FC;}
section[data-testid="stSidebar"]{background:#FCE7F3;}
[data-testid="metric-container"]{
    background:white;
    border:2px solid #FFD6E7;
    border-radius:16px;
}
.stButton button{
    background:#FF5C8A;
    color:white;
    border-radius:10px;
    border:none;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# SESSION STATE (ARRAY)
# ==========================================================
if "login" not in st.session_state:
    st.session_state.login = False

if "reservasi" not in st.session_state:
    st.session_state.reservasi = []

if "transaksi" not in st.session_state:
    st.session_state.transaksi = []

if "review" not in st.session_state:
    st.session_state.review = []

# ==========================================================
# LOGIN ADMIN
# ==========================================================
if not st.session_state.login:

    st.title("🏨 Denara Hotel Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "123":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Login gagal")

    st.stop()

# ==========================================================
# DATA KAMAR (ARRAY)
# ==========================================================
kamar = [
    {"nomor":"101","tipe":"Standard","harga":300000,"status":"Kosong"},
    {"nomor":"102","tipe":"Standard","harga":300000,"status":"Terisi"},
    {"nomor":"201","tipe":"Deluxe","harga":500000,"status":"Kosong"},
    {"nomor":"202","tipe":"Deluxe","harga":500000,"status":"Kosong"},
    {"nomor":"301","tipe":"Family","harga":800000,"status":"Terisi"},
    {"nomor":"302","tipe":"Suite","harga":1200000,"status":"Kosong"},
]

# ==========================================================
# SIDEBAR
# ==========================================================
st.sidebar.title("🏨 Denara Hotel")

menu = st.sidebar.radio(
    "Menu",
    [
        "🏠 Dashboard",
        "📝 Reservasi",
        "🏨 Manajemen Kamar",
        "🍔 Denara Eats",
        "💳 Pembayaran",
        "💎 Customer Center",
        "📊 Analytics",
        "⚙ Sistem"
    ]
)

# ==========================================================
# DASHBOARD
# ==========================================================
if menu == "🏠 Dashboard":

    st.title("🏨 Denara Hotel Dashboard")

    kosong = len([k for k in kamar if k["status"] == "Kosong"])
    terisi = len([k for k in kamar if k["status"] == "Terisi"])

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("🛏 Kamar Kosong", kosong)
    c2.metric("🏨 Kamar Terisi", terisi)
    c3.metric("📄 Reservasi", len(st.session_state.reservasi))

    total_pendapatan = sum(
        [t["total"] for t in st.session_state.transaksi]
    ) if st.session_state.transaksi else 0

    c4.metric("💰 Pendapatan", f"Rp {total_pendapatan:,.0f}")

    st.subheader("🎟 Promo Aktif")
    st.success("DENARA10 = Diskon 10%")
    st.success("VIP30 = Diskon 30%")

# ==========================================================
# RESERVASI (CRUD)
# ==========================================================
elif menu == "📝 Reservasi":

    st.title("📝 Reservasi Hotel")

    with st.expander("➕ Tambah Reservasi", expanded=True):

        nama = st.text_input("Nama Tamu")
        hp = st.text_input("No HP")

        tipe = st.selectbox(
            "Tipe Kamar",
            ["Standard","Deluxe","Family","Suite"]
        )

        checkin = st.date_input("Check In", date.today())
        checkout = st.date_input("Check Out", date.today())

        if st.button("Simpan Reservasi"):

            data = {
                "nama": nama,
                "hp": hp,
                "tipe": tipe,
                "checkin": str(checkin),
                "checkout": str(checkout)
            }

            # INSERT ARRAY
            st.session_state.reservasi.append(data)

            st.success("Reservasi berhasil ditambahkan")

    st.subheader("📋 Data Reservasi")

    if st.session_state.reservasi:

        df = pd.DataFrame(st.session_state.reservasi)
        st.dataframe(df, use_container_width=True)

        cari = st.text_input("🔍 Cari Nama")

        if cari:
            hasil = [
                x for x in st.session_state.reservasi
                if cari.lower() in x["nama"].lower()
            ]
            st.write(hasil)

        idx = st.number_input(
            "Index Edit/Hapus",
            0,
            len(st.session_state.reservasi)-1,
            0
        )

        nama_baru = st.text_input("Nama Baru")

        col1,col2 = st.columns(2)

        with col1:
            if st.button("✏ Update"):

                # UPDATE ARRAY
                st.session_state.reservasi[idx]["nama"] = nama_baru
                st.success("Data diperbarui")

        with col2:
            if st.button("🗑 Hapus"):

                # DELETE ARRAY
                del st.session_state.reservasi[idx]
                st.success("Data dihapus")
                st.rerun()

# ==========================================================
# MANAJEMEN KAMAR
# ==========================================================
elif menu == "🏨 Manajemen Kamar":

    st.title("🏨 Manajemen Kamar")

    st.dataframe(pd.DataFrame(kamar))

    st.subheader("🗺 Room Map")

    cols = st.columns(3)

    for i,k in enumerate(kamar):

        ikon = "🟩" if k["status"]=="Kosong" else "🟥"

        cols[i % 3].markdown(
            f"### {ikon} Kamar {k['nomor']}"
        )

# ==========================================================
# DENARA EATS
# ==========================================================
elif menu == "🍔 Denara Eats":

    st.title("🍔 Denara Eats")

    menu_makanan = {
        "Nasi Goreng":35000,
        "Mie Goreng":30000,
        "Pizza":85000,
        "Steak":65000,
        "Matcha":25000
    }

    pesanan = st.multiselect(
        "Pilih Menu",
        list(menu_makanan.keys())
    )

    total = sum(menu_makanan[p] for p in pesanan)

    st.metric("Total", f"Rp {total:,.0f}")

# ==========================================================
# PEMBAYARAN
# ==========================================================
elif menu == "💳 Pembayaran":

    st.title("💳 Pembayaran")

    nama = st.text_input("Nama Customer")
    total = st.number_input("Total Tagihan", 0)

    voucher = st.text_input("Voucher")

    diskon = 0

    if voucher == "DENARA10":
        diskon = 10

    if voucher == "VIP30":
        diskon = 30

    total_akhir = total - (total * diskon / 100)

    st.metric("Total Bayar", f"Rp {total_akhir:,.0f}")

    if st.button("Bayar"):

        st.session_state.transaksi.append(
            {
                "nama": nama,
                "total": total_akhir
            }
        )

        st.success("Pembayaran berhasil")

# ==========================================================
# CUSTOMER CENTER
# ==========================================================
elif menu == "💎 Customer Center":

    st.title("💎 Customer Center")

    nama = st.text_input("Nama Customer")
    rating = st.slider("Rating",1,5,5)
    komentar = st.text_area("Komentar")

    if st.button("Kirim Review"):

        st.session_state.review.append(
            {
                "nama": nama,
                "rating": rating,
                "komentar": komentar
            }
        )

        st.success("Review tersimpan")

# ==========================================================
# ANALYTICS
# ==========================================================
elif menu == "📊 Analytics":

    st.title("📊 Analytics")

    data = pd.DataFrame({
        "Bulan":["Jan","Feb","Mar","Apr","Mei","Jun"],
        "Pendapatan":[12,18,15,22,25,30]
    })

    st.line_chart(
        data.set_index("Bulan")
    )

    prediksi = data["Pendapatan"].mean() * 1.1

    st.success(
        f"Prediksi Pendapatan Bulan Depan : Rp {prediksi:.2f} Juta"
    )

# ==========================================================
# SISTEM
# ==========================================================
elif menu == "⚙ Sistem":

    st.title("⚙ Sistem")

    if st.button("Logout"):
        st.session_state.login = False
        st.rerun()

    st.info("Denara Hotel System - Single File Version")
