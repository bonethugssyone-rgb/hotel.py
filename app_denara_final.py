
# ==========================================================
# DENARA HOTEL SYSTEM (SINGLE FILE)
# Struktur Data Array (List Python)
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
# CSS PASTEL
# ==========================================================
st.markdown("""
<style>
.main{background:#FFF9FC;}
section[data-testid="stSidebar"]{background:#FCE7F3;}
[data-testid="metric-container"]{
background:white;
border:2px solid #FFD6E7;
border-radius:15px;
}
.stButton button{
background:#FF5C8A;
color:white;
border:none;
border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# SESSION STATE (ARRAY DINAMIS)
# ==========================================================
if "login" not in st.session_state:
    st.session_state.login = False

if "reservasi" not in st.session_state:
    st.session_state.reservasi = []

if "transaksi" not in st.session_state:
    st.session_state.transaksi = []

if "review" not in st.session_state:
    st.session_state.review = []

if "vip" not in st.session_state:
    st.session_state.vip = []

if "room_service" not in st.session_state:
    st.session_state.room_service = []

if "voucher" not in st.session_state:
    st.session_state.voucher = [
        {"kode":"DENARA10","diskon":10,"aktif":True},
        {"kode":"VIP30","diskon":30,"aktif":True}
    ]

# ==========================================================
# LOGIN ADMIN
# ==========================================================
if not st.session_state.login:

    st.title("🏨 Denara Hotel Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "123":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Login gagal")

    st.stop()

# ==========================================================
# ARRAY KAMAR
# ==========================================================
rooms = [
{"nomor":"101","tipe":"Standard","harga":300000,"kapasitas":"1-2 Orang","status":"Kosong"},
{"nomor":"102","tipe":"Standard","harga":300000,"kapasitas":"1-2 Orang","status":"Terisi"},
{"nomor":"201","tipe":"Deluxe","harga":500000,"kapasitas":"2-3 Orang","status":"Kosong"},
{"nomor":"202","tipe":"Deluxe","harga":500000,"kapasitas":"2-3 Orang","status":"Kosong"},
{"nomor":"301","tipe":"Family","harga":800000,"kapasitas":"4-5 Orang","status":"Kosong"},
{"nomor":"302","tipe":"Suite","harga":1200000,"kapasitas":"2-4 Orang","status":"Terisi"}
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

    kosong = len([x for x in rooms if x["status"]=="Kosong"])
    terisi = len([x for x in rooms if x["status"]=="Terisi"])

    pendapatan = sum(
        [x["total"] for x in st.session_state.transaksi]
    ) if st.session_state.transaksi else 0

    occupancy = (terisi / len(rooms))*100

    st.title("🏨 Dashboard")

    c1,c2,c3,c4,c5 = st.columns(5)

    c1.metric("Kosong", kosong)
    c2.metric("Terisi", terisi)
    c3.metric("Reservasi", len(st.session_state.reservasi))
    c4.metric("Pendapatan", f"Rp {pendapatan:,.0f}")
    c5.metric("Occupancy", f"{occupancy:.1f}%")

# ==========================================================
# RESERVASI
# ==========================================================
elif menu == "📝 Reservasi":

    st.title("📝 Reservasi")

    nama = st.text_input("Nama")
    hp = st.text_input("No HP")

    tipe = st.selectbox(
        "Tipe Kamar",
        ["Standard","Deluxe","Family","Suite"]
    )

    checkin = st.date_input("Check In", date.today())
    checkout = st.date_input("Check Out", date.today())

    if st.button("Tambah Reservasi"):

        st.session_state.reservasi.append({
            "nama":nama,
            "hp":hp,
            "tipe":tipe,
            "checkin":str(checkin),
            "checkout":str(checkout),
            "status":"Booked"
        })

    if st.session_state.reservasi:

        st.subheader("Data Reservasi")

        st.dataframe(
            pd.DataFrame(st.session_state.reservasi),
            use_container_width=True
        )

        cari = st.text_input("Cari Nama")

        if cari:
            hasil = [
                x for x in st.session_state.reservasi
                if cari.lower() in x["nama"].lower()
            ]
            st.write(hasil)

        idx = st.number_input(
            "Index Data",
            0,
            len(st.session_state.reservasi)-1,
            0
        )

        nama_baru = st.text_input("Nama Baru")

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            if st.button("Update"):
                st.session_state.reservasi[idx]["nama"] = nama_baru

        with col2:
            if st.button("Check In"):
                st.session_state.reservasi[idx]["status"] = "Check In"

        with col3:
            if st.button("Check Out"):
                st.session_state.reservasi[idx]["status"] = "Check Out"

        with col4:
            if st.button("Hapus"):
                del st.session_state.reservasi[idx]
                st.rerun()

# ==========================================================
# MANAJEMEN KAMAR
# ==========================================================
elif menu == "🏨 Manajemen Kamar":

    st.title("🏨 Katalog Kamar")

    st.dataframe(pd.DataFrame(rooms))

    st.subheader("🗺 Room Map")

    cols = st.columns(3)

    for i,r in enumerate(rooms):

        icon = "🟩" if r["status"]=="Kosong" else "🟥"

        cols[i%3].markdown(
            f"### {icon} {r['nomor']}"
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

    total = sum(
        menu_makanan[x]
        for x in pesanan
    )

    st.metric("Total", f"Rp {total:,.0f}")

    if st.button("Pesan"):
        st.session_state.room_service.append({
            "menu":pesanan,
            "total":total
        })

# ==========================================================
# PEMBAYARAN + MULTI VOUCHER
# ==========================================================
elif menu == "💳 Pembayaran":

    st.title("💳 Pembayaran")

    tab1,tab2 = st.tabs(
        ["Kasir","Voucher"]
    )

    with tab1:

        nama = st.text_input("Nama Customer")
        total = st.number_input("Tagihan",0)

        kode = st.text_input("Kode Voucher")

        diskon = 0

        for v in st.session_state.voucher:

            if (
                v["kode"] == kode
                and
                v["aktif"]
            ):
                diskon = v["diskon"]

        total_bayar = total - (
            total * diskon / 100
        )

        st.metric(
            "Total Bayar",
            f"Rp {total_bayar:,.0f}"
        )

        if st.button("Bayar"):
            st.session_state.transaksi.append({
                "nama":nama,
                "total":total_bayar
            })

    with tab2:

        kode_baru = st.text_input("Kode Baru")
        diskon_baru = st.number_input(
            "Diskon",
            0,
            100,
            10
        )

        if st.button("Tambah Voucher"):
            st.session_state.voucher.append({
                "kode":kode_baru,
                "diskon":diskon_baru,
                "aktif":True
            })

        st.dataframe(
            pd.DataFrame(st.session_state.voucher)
        )

# ==========================================================
# CUSTOMER CENTER
# ==========================================================
elif menu == "💎 Customer Center":

    st.title("💎 Customer Center")

    tab1,tab2 = st.tabs(
        ["VIP","Review"]
    )

    with tab1:

        nama = st.text_input("Nama VIP")

        kunjungan = st.number_input(
            "Kunjungan",
            0,
            100,
            0
        )

        if st.button("Simpan VIP"):

            if kunjungan >= 10:
                level = "Platinum"
            elif kunjungan >= 6:
                level = "Gold"
            elif kunjungan >= 3:
                level = "Silver"
            else:
                level = "Regular"

            st.session_state.vip.append({
                "nama":nama,
                "kunjungan":kunjungan,
                "level":level,
                "point":kunjungan*10
            })

        if st.session_state.vip:
            st.dataframe(pd.DataFrame(st.session_state.vip))

    with tab2:

        nama_review = st.text_input("Nama Reviewer")
        rating = st.slider("Rating",1,5,5)
        komentar = st.text_area("Komentar")

        if st.button("Kirim Review"):
            st.session_state.review.append({
                "nama":nama_review,
                "rating":rating,
                "komentar":komentar
            })

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

    prediksi = data["Pendapatan"].mean()*1.1

    st.success(
        f"Prediksi Bulan Depan : Rp {prediksi:.2f} Juta"
    )

    if st.session_state.vip:

        st.subheader("Top Customer")

        top = sorted(
            st.session_state.vip,
            key=lambda x:x["kunjungan"],
            reverse=True
        )

        st.dataframe(pd.DataFrame(top))

# ==========================================================
# SISTEM
# ==========================================================
elif menu == "⚙ Sistem":

    st.title("⚙ Sistem")

    if st.button("Logout"):
        st.session_state.login = False
        st.rerun()

    if st.button("Reset Semua Data"):
        st.session_state.reservasi = []
        st.session_state.transaksi = []
        st.session_state.review = []
        st.session_state.vip = []
