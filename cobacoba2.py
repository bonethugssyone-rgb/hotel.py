import streamlit as st
import pandas as pd
from datetime import datetime, date
import random

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(page_title="Smart Hotel System PRO", layout="wide")

# ==========================================
# DATABASE (SESSION)
# ==========================================

if 'kamar_db' not in st.session_state:
    st.session_state.kamar_db = {
        "101": {"tipe": "Standard", "harga": 300000, "fasilitas": "WiFi, AC", "bintang": 3.8, "status_kamar": "READY"},
        "201": {"tipe": "Deluxe", "harga": 550000, "fasilitas": "WiFi, AC, Bathtub", "bintang": 4.5, "status_kamar": "READY"},
        "301": {"tipe": "Suite", "harga": 900000, "fasilitas": "Jacuzzi, Smart TV", "bintang": 5.0, "status_kamar": "READY"},
    }

if 'reservasi_db' not in st.session_state:
    st.session_state.reservasi_db = []

if 'reviews' not in st.session_state:
    st.session_state.reviews = []

if 'login' not in st.session_state:
    st.session_state.login = False

# ==========================================
# FUNCTION
# ==========================================

def cek_kamar(no, t_in, t_out):
    for r in st.session_state.reservasi_db:
        if r['no_kamar'] == no:
            rin = datetime.strptime(r['check_in'], "%Y-%m-%d").date()
            rout = datetime.strptime(r['check_out'], "%Y-%m-%d").date()
            if not (t_out <= rin or t_in >= rout):
                return False
    return True

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🏨 Hotel System")

if st.sidebar.checkbox("Login Admin"):
    u = st.sidebar.text_input("User")
    p = st.sidebar.text_input("Pass", type="password")
    if st.sidebar.button("Login"):
        if u == "admin" and p == "admin":
            st.session_state.login = True

menu = st.sidebar.radio("Menu", [
    "Booking",
    "Riwayat",
    "Admin",
    "Review"
])

# ==========================================
# BOOKING
# ==========================================

if menu == "Booking":

    st.title("Booking Hotel")

    col1, col2 = st.columns(2)
    with col1:
        t_in = st.date_input("Check-in", date.today())
    with col2:
        t_out = st.date_input("Check-out", date.today())

    durasi = (t_out - t_in).days

    for no, k in st.session_state.kamar_db.items():

        ready = cek_kamar(no, t_in, t_out)

        st.subheader(f"Kamar {no} - {k['tipe']}")

        # STATUS KAMAR
        if k['status_kamar'] == "DIRTY":
            st.warning("🧹 Dibersihkan")
        elif k['status_kamar'] == "MAINTENANCE":
            st.error("🔧 Maintenance")
        else:
            st.success("✅ Ready")

        st.write(f"Harga: {k['harga']}")

        if ready:
            if st.button(f"Pesan {no}"):
                st.session_state.temp = {
                    "no": no,
                    "tipe": k['tipe'],
                    "total": k['harga'] * durasi,
                    "in": str(t_in),
                    "out": str(t_out)
                }

    # FORM
    if 'temp' in st.session_state:
        st.subheader("Isi Data")

        nama = st.text_input("Nama")

        if st.button("Bayar"):
            data = {
                "booking_id": f"HTL-{random.randint(1000,9999)}",
                "nama_tamu": nama,
                "no_kamar": st.session_state.temp['no'],
                "tipe": st.session_state.temp['tipe'],
                "check_in": st.session_state.temp['in'],
                "check_out": st.session_state.temp['out'],
                "status_bayar": "PENDING",
                "status_tamu": "BOOKED",
                "total_biaya": st.session_state.temp['total']
            }
            st.session_state.reservasi_db.append(data)
            del st.session_state.temp
            st.success("Booking berhasil!")

# ==========================================
# RIWAYAT
# ==========================================

elif menu == "Riwayat":

    st.title("Riwayat")

    df = pd.DataFrame(st.session_state.reservasi_db)

    search = st.text_input("Cari Nama")

    if search != "":
        df = df[df['nama_tamu'].str.contains(search, case=False)]

    st.dataframe(df)

    # EXPORT
    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "data.csv")

# ==========================================
# ADMIN
# ==========================================

elif menu == "Admin":

    st.title("Admin Panel")

    if not st.session_state.login:
        st.warning("Login dulu")
        st.stop()

    df = pd.DataFrame(st.session_state.reservasi_db)

    st.metric("Total Booking", len(df))

    if not df.empty:

        # GRAFIK
        df['check_in'] = pd.to_datetime(df['check_in'])
        chart = df.groupby(df['check_in'].dt.date)['total_biaya'].sum()
        st.line_chart(chart)

        # CHECK-IN / OUT
        st.subheader("Check-in / Check-out")

        for i, d in enumerate(st.session_state.reservasi_db):

            st.write(d['booking_id'], d['nama_tamu'])

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(d['status_tamu'])

            with col2:
                if st.button(f"Checkin {i}"):
                    st.session_state.reservasi_db[i]['status_tamu'] = "CHECKED-IN"
                    st.rerun()

            with col3:
                if st.button(f"Checkout {i}"):
                    st.session_state.reservasi_db[i]['status_tamu'] = "CHECKED-OUT"
                    st.rerun()

        # PEMBAYARAN
        st.subheader("Pembayaran")

        for i, d in enumerate(st.session_state.reservasi_db):
            if d['status_bayar'] == "PENDING":
                if st.button(f"Bayar {d['booking_id']}"):
                    st.session_state.reservasi_db[i]['status_bayar'] = "PAID"
                    st.rerun()

# ==========================================
# REVIEW
# ==========================================

elif menu == "Review":

    st.title("Review")

    for r in st.session_state.reviews:
        st.write(r['nama'], "⭐" * r['rating'])
        st.caption(r['komen'])

    nama = st.text_input("Nama")
    rating = st.slider("Rating", 1, 5)
    komen = st.text_area("Komentar")

    if st.button("Kirim"):
        st.session_state.reviews.append({
            "nama": nama,
            "rating": rating,
            "komen": komen
        })
        st.success("Tersimpan")