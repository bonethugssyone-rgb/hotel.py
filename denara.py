import streamlit as st

# ==============================================================================
# 🎨 CONFIG
# ==============================================================================
st.set_page_config(page_title="Hotel System", layout="wide")

# ==============================================================================
# 🎨 STYLE (BIAR BAGUS)
# ==============================================================================
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.metric-card {
    padding: 15px;
    border-radius: 10px;
    background-color: #1c1f26;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 🔐 SESSION
# ==============================================================================
if "user" not in st.session_state:
    st.session_state.user = None

if "kamar_db" not in st.session_state:
    st.session_state.kamar_db = {
        "101": {"status": "Tersedia"},
        "102": {"status": "Tersedia"},
        "103": {"status": "Tersedia"},
        "104": {"status": "Tersedia"},
    }

if "transaksi" not in st.session_state:
    st.session_state.transaksi = []

# ==============================================================================
# 🔐 LOGIN
# ==============================================================================
users = {
    "admin": {"password": "123", "role": "admin"},
    "kasir": {"password": "123", "role": "kasir"}
}

def login():
    st.title("🔐 Login Hotel System")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            if user in users and users[user]["password"] == pw:
                st.session_state.user = user
                st.session_state.role = users[user]["role"]
                st.rerun()
            else:
                st.error("Login gagal!")

def logout():
    st.session_state.user = None
    st.rerun()

if st.session_state.user is None:
    login()
    st.stop()

# ==============================================================================
# 🧭 SIDEBAR
# ==============================================================================
st.sidebar.title("🏨 Hotel App")
st.sidebar.write(f"👤 {st.session_state.user} ({st.session_state.role})")

if st.sidebar.button("Logout"):
    logout()

menu_admin = ["Dashboard", "Reservasi", "Kasir", "Data", "Analisis"]
menu_kasir = ["Dashboard", "Kasir"]

menu = st.sidebar.radio(
    "Menu",
    menu_admin if st.session_state.role == "admin" else menu_kasir
)

# ==============================================================================
# 📊 DASHBOARD
# ==============================================================================
if menu == "Dashboard":
    st.title("📊 Dashboard Hotel")

    kamar = st.session_state.kamar_db
    transaksi = st.session_state.transaksi

    total = len(kamar)
    terisi = sum(1 for k in kamar.values() if "Terisi" in k["status"])
    kosong = total - terisi
    pendapatan = sum(t["total"] for t in transaksi)

    # KPI
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Kamar", total)
    col2.metric("Terisi", terisi)
    col3.metric("Kosong", kosong)
    col4.metric("Pendapatan", f"Rp {pendapatan:,}")

    st.divider()

    colA, colB = st.columns(2)

    with colA:
        st.subheader("📈 Status Kamar")

        data_chart = [
            {"status": "Terisi", "jumlah": terisi},
            {"status": "Kosong", "jumlah": kosong}
        ]
    with colB:
        st.subheader("🛏️ Detail Kamar")

        for no, k in kamar.items():
            if "Terisi" in k["status"]:
                st.error(f"Kamar {no} → {k['status']}")
            else:
                st.success(f"Kamar {no} → {k['status']}")

    st.divider()

    st.subheader("🧠 Insight")

    occ = (terisi / total) * 100 if total > 0 else 0

    if occ > 80:
        st.error("🔥 Hampir penuh!")
    elif occ > 50:
        st.warning("⚠️ Okupansi sedang")
    else:
        st.success("🟢 Banyak kamar kosong")

    st.info(f"Occupancy Rate: {occ:.1f}%")

# ==============================================================================
# 🛏️ RESERVASI
# ==============================================================================
if menu == "Reservasi":
    st.title("🛏️ Reservasi")

    kamar = st.session_state.kamar_db

    pilih = st.selectbox("Pilih Kamar", list(kamar.keys()))
    nama = st.text_input("Nama Tamu")

    if st.button("Check-in"):
        if kamar[pilih]["status"] == "Tersedia":
            kamar[pilih]["status"] = f"Terisi ({nama})"
            st.success("Check-in berhasil")
        else:
            st.error("Sudah terisi")

    if st.button("Check-out"):
        kamar[pilih]["status"] = "Tersedia"
        st.success("Check-out berhasil")

# ==============================================================================
# 💰 KASIR
# ==============================================================================
if menu == "Kasir":
    st.title("💰 Kasir")

    nama = st.text_input("Nama")
    total = st.number_input("Total Bayar", min_value=0)

    if st.button("Simpan"):
        st.session_state.transaksi.append({
            "nama": nama,
            "total": total
        })
        st.success("Tersimpan")

    st.subheader("Riwayat")
    st.write(st.session_state.transaksi)

# ==============================================================================
# 📂 DATA
# ==============================================================================
if menu == "Data":
    st.title("📂 Data")

    st.write(st.session_state.kamar_db)
    st.write(st.session_state.transaksi)

# ==============================================================================
# 📊 ANALISIS
# ==============================================================================
if menu == "Analisis":
    st.title("📊 Analysis Center")

    kamar = st.session_state.kamar_db

    total = len(kamar)
    terisi = sum(1 for k in kamar.values() if "Terisi" in k["status"])
    kosong = total - terisi
    st.subheader("Insight")

    occ = (terisi / total) * 100 if total > 0 else 0

    if occ > 80:
        st.error("🔥 Hampir penuh")
    elif occ > 50:
        st.warning("⚠️ Sedang")
    else:
        st.success("🟢 Sepi")

    st.info(f"Occupancy Rate: {occ:.1f}%")

    st.subheader("Rekomendasi")

    if kosong > terisi:
        st.write("➡️ Perbanyak promo")
    else:
        st.write("➡️ Maksimalkan profit")  
    st.subheader("Insight")

    occ = (terisi / total) * 100 if total > 0 else 0

    if occ > 80:
        st.error("🔥 Hampir penuh")
    elif occ > 50:
        st.warning("⚠️ Sedang")
    else:
        st.success("🟢 Sepi")

    st.info(f"Occupancy Rate: {occ:.1f}%")

    st.subheader("Rekomendasi")

    if kosong > terisi:
        st.write("➡️ Perbanyak promo")
    else:
        st.write("➡️ Maksimalkan profit")
