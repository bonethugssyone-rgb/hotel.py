import streamlit as st
from datetime import date

# ================= DATA =================
users = [{"username": "admin", "password": "123"}]

rooms = [
    {"no": 101, "tipe": "Standard", "harga": 200000, "status": "Kosong"},
    {"no": 102, "tipe": "Deluxe", "harga": 300000, "status": "Kosong"},
]

customers = []
reservations = []

# ================= LOGIN =================
st.sidebar.title("Login")
user = st.sidebar.text_input("Username")
pw = st.sidebar.text_input("Password", type="password")

login = any(u["username"] == user and u["password"] == pw for u in users)

# ================= FUNCTION =================
def harga_dinamis(harga):
    if date.today().day % 2 == 0:
        return harga + 50000
    return harga

def tambah_poin(nama, total):
    for c in customers:
        if c["nama"] == nama:
            poin = total // 10000
            c["poin"] += poin
            return poin

def get_customer(nama):
    for c in customers:
        if c["nama"] == nama:
            return c
    customers.append({"nama": nama, "poin": 0})
    return customers[-1]

# ================= MENU =================
if login:
    menu = st.sidebar.selectbox("Menu", [
        "Dashboard",
        "Kamar",
        "Reservasi",
        "Pembayaran",
        "Loyalty",
        "Riwayat"
    ])

    # ================= DASHBOARD =================
    if menu == "Dashboard":
        st.title("📊 Dashboard")

        total_kamar = len(rooms)
        terisi = len([r for r in rooms if r["status"] == "Terisi"])
        total_res = len(reservations)

        st.metric("Total Kamar", total_kamar)
        st.metric("Kamar Terisi", terisi)
        st.metric("Total Reservasi", total_res)

    # ================= KAMAR =================
    elif menu == "Kamar":
        st.title("🏨 Daftar Kamar")

        filter_tipe = st.selectbox("Filter Tipe", ["All", "Standard", "Deluxe"])

        for r in rooms:
            harga = harga_dinamis(r["harga"])

            if filter_tipe == "All" or r["tipe"] == filter_tipe:
                st.write(f"Kamar {r['no']} | {r['tipe']} | Rp{harga} | {r['status']}")

    # ================= RESERVASI =================
    elif menu == "Reservasi":
        st.title("📝 Reservasi")

        nama = st.text_input("Nama")
        kamar = st.selectbox("Kamar", [r["no"] for r in rooms])
        hari = st.number_input("Durasi Menginap (hari)", 1, 30)

        if st.button("Booking"):
            for r in rooms:
                if r["no"] == kamar and r["status"] == "Kosong":
                    r["status"] = "Terisi"

                    cust = get_customer(nama)
                    harga = harga_dinamis(r["harga"]) * hari

                    reservations.append({
                        "nama": nama,
                        "kamar": kamar,
                        "hari": hari,
                        "total": harga
                    })

                    st.success("Berhasil booking!")

    # ================= PEMBAYARAN =================
    elif menu == "Pembayaran":
        st.title("💳 Pembayaran")

        for i, res in enumerate(reservations):
            if st.button(f"Bayar {res['nama']} ({res['kamar']})", key=i):
                poin = tambah_poin(res["nama"], res["total"])

                st.success("Pembayaran berhasil!")
                st.write("===== STRUK =====")
                st.write(res)
                st.write(f"Poin: {poin}")

    # ================= LOYALTY =================
    elif menu == "Loyalty":
        st.title("🎮 Loyalty")

        nama = st.text_input("Nama")

        if st.button("Cek"):
            c = get_customer(nama)
            st.success(f"Poin: {c['poin']}")

        if st.button("Redeem"):
            c = get_customer(nama)
            if c["poin"] >= 50:
                c["poin"] -= 50
                st.success("Reward didapat!")
            else:
                st.error("Poin kurang")

    # ================= RIWAYAT =================
    elif menu == "Riwayat":
        st.title("📜 Riwayat")

        search = st.text_input("Cari nama")

        for r in reservations:
            if search.lower() in r["nama"].lower():
                st.write(r)

else:
    st.warning("Login dulu!")