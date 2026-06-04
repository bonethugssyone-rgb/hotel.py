import streamlit as st
import pandas as pd
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Hotel Dashboard", layout="wide")

# =========================
# SESSION STATE INIT
# =========================
if "login" not in st.session_state:
    st.session_state.login = False

if "role" not in st.session_state:
    st.session_state.role = None

if "kamar_db" not in st.session_state:
    st.session_state.kamar_db = {
        101: {"tipe": "Standard", "harga": 300000, "status": "🟩 Kosong"},
        102: {"tipe": "Deluxe", "harga": 500000, "status": "🟥 Terisi"},
        103: {"tipe": "Suite", "harga": 800000, "status": "🟨 Booking"},
    }

if "reservasi_db" not in st.session_state:
    st.session_state.reservasi_db = []

if "reviews_db" not in st.session_state:
    st.session_state.reviews_db = []

# =========================
# LOGIN SYSTEM
# =========================
def login_page():
    st.title("🔐 Login Sistem Hotel")

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pw == "admin":
            st.session_state.login = True
            st.session_state.role = "admin"
            st.success("Login Admin berhasil")
            st.rerun()

        elif user == "kasir" and pw == "kasir":
            st.session_state.login = True
            st.session_state.role = "kasir"
            st.success("Login Kasir berhasil")
            st.rerun()

        else:
            st.error("Login gagal")

# =========================
# DASHBOARD
# =========================
def dashboard():
    st.title("📊 Dashboard Hotel")

    kamar_db = st.session_state.kamar_db
    reservasi_db = st.session_state.reservasi_db
    reviews_db = st.session_state.reviews_db

    # =========================
    # HITUNG DATA
    # =========================
    total_kamar = len(kamar_db)

    terisi = sum(1 for k in kamar_db.values() if k["status"] == "🟥 Terisi")
    booking = sum(1 for k in kamar_db.values() if k["status"] == "🟨 Booking")
    kosong = total_kamar - terisi - booking

    pendapatan = sum(r["total"] for r in reservasi_db)

    avg_rating = (
        sum(r["rating"] for r in reviews_db) / len(reviews_db)
        if reviews_db else 0
    )

    okupansi = (terisi / total_kamar * 100) if total_kamar > 0 else 0

    # =========================
    # METRICS
    # =========================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Kamar", total_kamar)
    col2.metric("Terisi", terisi)
    col3.metric("Pendapatan", f"Rp {pendapatan:,}")
    col4.metric("Rating", f"{avg_rating:.1f} ⭐")

    st.divider()

    # =========================
    # CHART
    # =========================
    df = pd.DataFrame({
        "Status": ["Kosong", "Terisi", "Booking"],
        "Jumlah": [kosong, terisi, booking]
    })

    st.subheader("📊 Grafik Status Kamar")
    st.bar_chart(df.set_index("Status"))

    st.subheader("📈 Okupansi")
    st.progress(int(okupansi))

    # =========================
    # ANALISIS
    # =========================
    st.subheader("🧠 Insight")

    if okupansi > 70:
        st.success("🔥 Okupansi tinggi, bisnis bagus!")
    elif okupansi > 40:
        st.warning("⚠️ Okupansi sedang, perlu promo")
    else:
        st.error("❗ Okupansi rendah, perlu strategi marketing")

# =========================
# RESERVASI
# =========================
def reservasi():
    st.title("📝 Reservasi Baru")

    nama = st.text_input("Nama")
    kamar = st.selectbox("Pilih Kamar", list(st.session_state.kamar_db.keys()))
    malam = st.number_input("Jumlah Malam", 1, 30)

    if st.button("Booking"):
        harga = st.session_state.kamar_db[kamar]["harga"]
        total = harga * malam

        st.session_state.reservasi_db.append({
            "nama": nama,
            "kamar": kamar,
            "malam": malam,
            "total": total,
            "tanggal": datetime.now()
        })

        st.session_state.kamar_db[kamar]["status"] = "🟥 Terisi"

        st.success("Reservasi berhasil!")

# =========================
# DATA KAMAR
# =========================
def kamar():
    st.title("🏨 Data Kamar")

    data = []
    for no, info in st.session_state.kamar_db.items():
        data.append({
            "No": no,
            "Tipe": info["tipe"],
            "Harga": info["harga"],
            "Status": info["status"]
        })

    df = pd.DataFrame(data)
    st.dataframe(df)

# =========================
# REVIEW
# =========================
def review():
    st.title("⭐ Review Pelanggan")

    nama = st.text_input("Nama")
    rating = st.slider("Rating", 1, 5)

    if st.button("Kirim"):
        st.session_state.reviews_db.append({
            "nama": nama,
            "rating": rating
        })
        st.success("Terima kasih!")

# =========================
# MAIN APP
# =========================
if not st.session_state.login:
    login_page()
else:
    st.sidebar.title(f"👤 {st.session_state.role}")

    menu = st.sidebar.radio("Menu", [
        "Dashboard",
        "Reservasi",
        "Kamar",
        "Review"
    ])

    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.rerun()

    if menu == "Dashboard":
        dashboard()

    elif menu == "Reservasi":
        reservasi()

    elif menu == "Kamar":
        kamar()

    elif menu == "Review":
        review()
