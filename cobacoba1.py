import streamlit as st
import pandas as pd
from datetime import datetime, date

# ==========================================
# 1. INITIALIZATION DATA & MOCK DATABASE (ARRAY-BASED)
# ==========================================
st.set_page_config(page_title="SmartStay Hotel System", layout="wide", page_icon="🏨")

# Master Kamar (Dinamis)
if 'kamar_db' not in st.session_state:
    st.session_state.kamar_db = {
        "101": {"tipe": "Standard Room", "harga": 300000, "status": "🟩 Tersedia"},
        "102": {"tipe": "Standard Room", "harga": 300000, "status": "🟥 Terisi"},
        "103": {"tipe": "Deluxe Room", "harga": 500000, "status": "🟨 Booking"},
        "104": {"tipe": "Deluxe Room", "harga": 500000, "status": "🟩 Tersedia"},
        "201": {"tipe": "Family Room", "harga": 800000, "status": "🟩 Tersedia"},
        "202": {"tipe": "Family Room", "harga": 800000, "status": "🟥 Terisi"},
        "301": {"tipe": "Suite Room", "harga": 1200000, "status": "🟩 Tersedia"},
        "302": {"tipe": "Suite Room", "harga": 1200000, "status": "🟩 Tersedia"},
    }

# Database Reservasi Utama (Array List of Dict)
if 'reservasi_db' not in st.session_state:
    st.session_state.reservasi_db = [
        {
            "id": "INV2026001", "nama": "Andi", "hp": "0812345678", "email": "andi@mail.com", "alamat": "Jakarta",
            "kamar": "102", "tipe": "Standard Room", "check_in": "2026-06-01", "check_out": "2026-06-03",
            "tujuan": "Liburan", "status": "Check-In", "total_biaya": 600000, "status_bayar": "PAID",
            "metode": "Transfer BCA", "deposit_tipe": "Full Payment", "add_ons": ["Breakfast"]
        },
        {
            "id": "INV2026002", "nama": "Siti Mutia", "hp": "089876543", "email": "siti@mail.com", "alamat": "Bandung",
            "kamar": "103", "tipe": "Deluxe Room", "check_in": "2026-06-10", "check_out": "2026-06-12",
            "tujuan": "Bisnis", "status": "Booking", "total_biaya": 1150000, "status_bayar": "🟠 Deposit Paid",
            "metode": "DANA", "deposit_tipe": "Deposit 30%", "add_ons": ["Breakfast", "Airport Pickup"]
        }
    ]

# Database Review & Feedback
if 'reviews_db' not in st.session_state:
    st.session_state.reviews_db = [
        {"nama": "Andi", "rating": 5, "komentar": "Pelayanan sangat baik, proses check-in lancar!", "tanggal": "2026-06-03"},
        {"nama": "Budi", "rating": 4, "komentar": "Kamar bersih dan dekat pusat kota.", "tanggal": "2026-06-02"}
    ]

# History Kunjungan untuk Loyalty Program (Sorting & VIP System)
if 'customer_history' not in st.session_state:
    st.session_state.customer_history = [
        {"nama": "Andi", "kunjungan": 12, "level": "Platinum"},
        {"nama": "Siti Mutia", "kunjungan": 4, "level": "Silver"},
        {"nama": "Budi", "kunjungan": 1, "level": "Regular"},
        {"nama": "Denara", "kunjungan": 7, "level": "Gold"}
    ]

# Tarif Kamar Kamus Referensi
TARIF_KAMAR = {
    "Standard Room": 300000,
    "Deluxe Room": 500000,
    "Family Room": 800000,
    "Suite Room": 1200000
}

# ==========================================
# 2. SIDEBAR NAVIGASI UTAMA
# ==========================================
st.sidebar.markdown("# 🏨 SmartStay Hotel")
st.sidebar.caption("Modern Hotel Management System")
st.sidebar.markdown("---")

menu = st.sidebar.radio("🏠 MENU UTAMA APLIKASI", [
    "Dashboard", "📝 Reservasi Baru", "🏨 Daftar Kamar", "🗺️ Room Map",
    "🔍 Cari Reservasi", "📋 Data Reservasi", "💳 Pembayaran",
    "📜 Riwayat Pembayaran", "👤 Customer VIP", "⭐ Review Hotel", "📊 Analytics Center"
])

# ==========================================
# MENU 1: DASHBOARD
# ==========================================
if menu == "Dashboard":
    st.title("🏠 Dashboard Real-Time")
    
    total_kmr = len(st.session_state.kamar_db)
    terisi = sum(1 for k in st.session_state.kamar_db.values() if k["status"] == "🟥 Terisi")
    booking = sum(1 for k in st.session_state.kamar_db.values() if k["status"] == "🟨 Booking")
    kosong = total_kmr - terisi - booking
    
    total_rev = len(st.session_state.reservasi_db)
    total_cust = len(st.session_state.customer_history)
    pendapatan_total = sum(r["total_biaya"] for r in st.session_state.reservasi_db)
    avg_rating = sum(rev["rating"] for rev in st.session_state.reviews_db) / len(st.session_state.reviews_db) if st.session_state.reviews_db else 5.0

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Total Kamar", total_kmr)
    col_m1.metric("Kamar Terisi 🟥", terisi)
    col_m2.metric("Kamar Kosong 🟩", kosong)
    col_m2.metric("Total Reservasi", total_rev)
    col_m3.metric("Total Customer", total_cust)
    col_m3.metric("Pendapatan Total", f"Rp {pendapatan_total:,}")
    col_m4.metric("Rating Hotel", f"⭐ {avg_rating:.1f} / 5.0")
    col_m4.metric("Occupancy Rate", f"{(terisi/total_kmr)*100:.1f}%" if total_kmr > 0 else "0%")

    st.markdown("---")
    st.subheader("📊 Analisis Grafik Pendapatan Tipe Kamar")
    
    # Mengganti Matplotlib dengan Grafik Bawaan Streamlit (Bebas Error)
    df_rev = pd.DataFrame(st.session_state.reservasi_db)
    if not df_rev.empty:
        df_chart = df_rev.groupby('tipe')['total_biaya'].sum()
        st.bar_chart(df_chart)
    else:
        st.info("Belum ada data transaksi untuk memuat grafik pendapatan.")

# ==========================================
# MENU 2: RESERVASI BARU
# ==========================================
elif menu == "📝 Reservasi Baru":
    st.title("📝 Input Reservasi Baru")
    
    col_form, col_recom = st.columns([1.5, 1])
    
    with col_form:
        st.subheader("Data Diri Tamu")
        nama = st.text_input("Nama Lengkap")
        hp = st.text_input("Nomor HP")
        email = st.text_input("Email")
        alamat = st.text_area("Alamat")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            jml_tamu = st.number_input("Jumlah Tamu", min_value=1, max_value=10, value=2)
            check_in = st.date_input("Tanggal Check In", date.today())
        with col_f2:
            budget_max = st.number_input("Budget Maksimal Anda (Rp)", min_value=100000, value=1000000, step=50000)
            check_out = st.date_input("Tanggal Check Out", date.today() + pd.Timedelta(days=1))
            
        tujuan = st.selectbox("Tujuan Menginap", ["Liburan", "Bisnis", "Honeymoon", "Keluarga", "Staycation"])

    with col_recom:
        st.subheader("🤖 Smart Room Recommendation")
        
        rekomendasi_tipe = "Standard Room"
        if jml_tamu >= 4 or tujuan == "Keluarga":
            rekomendasi_tipe = "Family Room"
        elif budget_max >= 1200000 and (tujuan == "Honeymoon" or tujuan == "Bisnis"):
            rekomendasi_tipe = "Suite Room"
        elif budget_max >= 500000 or jml_tamu == 3:
            rekomendasi_tipe = "Deluxe Room"
            
        st.success(f"💡 Rekomendasi Terbaik: **{rekomendasi_tipe}**")
        
        st.markdown("---")
        st.subheader("🎲 Auto Room Assignment")
        
        kamar_assign = None
        for no_kmr, spek in st.session_state.kamar_db.items():
            if spek["tipe"] == rekomendasi_tipe and spek["status"] == "🟩 Tersedia":
                kamar_assign = no_kmr
                break
                
        if kamar_assign:
            st.info(f"Sistem Menentukan: **Kamar {kamar_assign}** otomatis dialokasikan.")
        else:
            st.warning("⚠️ Kamar rekomendasi penuh. Ketik nomor kamar manual:")
            kamar_assign = st.text_input("Nomor Kamar Pilihan:", value="101")

        st.markdown("---")
        st.subheader("🎁 Additional Services (Add-Ons)")
        addons_pilihan = []
        if st.checkbox("🍳 Breakfast Tambahan (Rp 50.000)"): addons_pilihan.append("Breakfast")
        if st.checkbox("🛏️ Extra Bed (Rp 100.000)"): addons_pilihan.append("Extra Bed")
        if st.checkbox("🚗 Airport Pickup (Rp 150.000)"): addons_pilihan.append("Airport Pickup")
        if st.checkbox("🧺 Laundry Service (Rp 75.000)"): addons_pilihan.append("Laundry")
        if st.checkbox("🎮 Gaming Package PS5 (Rp 100.000)"): addons_pilihan.append("Gaming Package")

    st.markdown("---")
    if st.button("Lanjutkan ke Pembayaran ➡️", type="primary"):
        if not nama or not kamar_assign:
            st.error("Nama Tamu dan Alokasi Kamar wajib dilengkapi!")
        else:
            st.session_state.proses_checkout = {
                "nama": nama, "hp": hp, "email": email, "alamat": alamat,
                "kamar": kamar_assign, "tipe": rekomendasi_tipe,
                "check_in": str(check_in), "check_out": str(check_out),
                "tujuan": tujuan, "add_ons": addons_pilihan
            }
            st.success("Data Tersimpan! Silakan klik Menu '💳 Pembayaran' di sidebar untuk bayar.")

# ==========================================
# MENU 3: DAFTAR KAMAR
# ==========================================
elif menu == "🏨 Daftar Kamar":
    st.title("🏨 Daftar Spesifikasi & Informasi Kamar")
    
    tipe_cards = {
        "Standard Room": {"harga": "Rp 300.000", "kap": "1-2 Orang", "f": "AC, TV LED, WiFi, Air Mineral"},
        "Deluxe Room": {"harga": "Rp 500.000", "kap": "2-3 Orang", "f": "Smart TV, WiFi, Breakfast, Hair Dryer"},
        "Family Room": {"harga": "Rp 800.000", "kap": "4-5 Orang", "f": "2 Queen Bed, Smart TV, Sofa, Breakfast"},
        "Suite Room": {"harga": "Rp 1.200.000", "kap": "2-4 Orang", "f": "Living Room, Mini Bar, Bathtub, Balkon"}
    }
    
    for tk, val in tipe_cards.items():
        with st.expander(f"⚙️ {tk} — {val['harga']} / Malam"):
            st.write(f"**Kapasitas:** {val['kap']}")
            st.write(f"**Fasilitas:** {val['f']}")

# ==========================================
# MENU 4: ROOM MAP
# ==========================================
elif menu == "🗺️ Room Map":
    st.title("🗺️ Visual Room Map Status")
    
    cols = st.columns(4)
    idx = 0
    for no_kmr, data in st.session_state.kamar_db.items():
        with cols[idx % 4]:
            if "Tersedia" in data["status"]:
                st.success(f"### {no_kmr}\n🟢 Available\n\n*{data['tipe']}*")
            elif "Terisi" in data["status"]:
                st.error(f"### {no_kmr}\n🟥 Occupied\n\n*{data['tipe']}*")
            else:
                st.warning(f"### {no_kmr}\n🟨 Booked\n\n*{data['tipe']}*")
        idx += 1

# ==========================================
# MENU 5: CARI RESERVASI
# ==========================================
elif menu == "🔍 Cari Reservasi":
    st.title("🔍 Cari Data Reservasi Aktif")
    
    kategori_cari = st.radio("Cari Berdasarkan:", ["Nama", "Nomor Kamar", "Nomor HP"], horizontal=True)
    kunci_keyword = st.text_input("Ketik Kata Kunci Pencarian:")
    
    if kunci_keyword:
        hasil_cari = []
        for r in st.session_state.reservasi_db:
            if kategori_cari == "Nama" and kunci_keyword.lower() in r["nama"].lower():
                hasil_cari.append(r)
            elif kategori_cari == "Nomor Kamar" and kunci_keyword == r["kamar"]:
                hasil_cari.append(r)
            elif kategori_cari == "Nomor HP" and kunci_keyword in r["hp"]:
                hasil_cari.append(r)
                
        if hasil_cari:
            st.success(f"Ditemukan {len(hasil_cari)} Data!")
            st.table(pd.DataFrame(hasil_cari)[["id", "nama", "kamar", "tipe", "check_in", "check_out", "status"]])
        else:
            st.warning("Data tidak ditemukan.")

# ==========================================
# MENU 6: DATA RESERVASI (CRUD)
# ==========================================
elif menu == "📋 Data Reservasi":
    st.title("📋 Master Log Data Reservasi (CRUD)")
    
    if st.session_state.reservasi_db:
        df_master = pd.DataFrame(st.session_state.reservasi_db)
        st.dataframe(df_master[["id", "nama", "kamar", "check_in", "check_out", "status", "total_biaya"]], use_container_width=True)
        
        st.markdown("---")
        st.subheader("🛠️ Aksi Resepsionis")
        
        list_id = [r["id"] for r in st.session_state.reservasi_db]
        pilih_id = st.selectbox("Pilih ID Transaksi target:", list_id)
        
        idx_target = next((i for i, item in enumerate(st.session_state.reservasi_db) if item["id"] == pilih_id), None)
        
        if idx_target is not None:
            c1, c2, c3 = st.columns(3)
            
            if c1.button("Set Status: CHECK-IN 🟥"):
                st.session_state.reservasi_db[idx_target]["status"] = "Check-In"
                kmr = st.session_state.reservasi_db[idx_target]["kamar"]
                if kmr in st.session_state.kamar_db:
                    st.session_state.kamar_db[kmr]["status"] = "🟥 Terisi"
                st.success("Tamu Berhasil Check-In!")
                st.rerun()
                
            if c2.button("Set Status: CHECK-OUT 🟩"):
                st.session_state.reservasi_db[idx_target]["status"] = "Check-Out"
                kmr = st.session_state.reservasi_db[idx_target]["kamar"]
                if kmr in st.session_state.kamar_db:
                    st.session_state.kamar_db[kmr]["status"] = "🟩 Tersedia"
                st.success("Tamu Berhasil Check-Out!")
                st.rerun()
                
            if c3.button("Hapus Bukti Transaksi ❌"):
                st.session_state.reservasi_db.pop(idx_target)
                st.error("Data terhapus dari array!")
                st.rerun()
    else:
        st.warning("Database transaksi kosong.")

# ==========================================
# MENU 7: PEMBAYARAN & SUMMARY
# ==========================================
elif menu == "💳 Pembayaran":
    st.title("💳 Payment Management System")
    
    if "proses_checkout" not in st.session_state:
        st.info("Silakan isi formulir pemesanan terlebih dahulu di Menu '📝 Reservasi Baru'.")
    else:
        ck = st.session_state.proses_checkout
        
        d1 = datetime.strptime(ck["check_in"], "%Y-%m-%d")
        d2 = datetime.strptime(ck["check_out"], "%Y-%m-%d")
        durasi = max(1, (d2 - d1).days)
        
        tarif_per_malam = TARIF_KAMAR.get(ck["tipe"], 300000)
        biaya_kamar = tarif_per_malam * durasi
        
        biaya_addons = 0
        mapping_addon_harga = {"Breakfast": 50000, "Extra Bed": 100000, "Airport Pickup": 150000, "Laundry": 75000, "Gaming Package": 100000}
        for item in ck["add_ons"]:
            biaya_addons += mapping_addon_harga.get(item, 0)
            
        subtotal = biaya_kamar + biaya_addons
        
        voucher_input = st.text_input("Masukkan Kode Voucher (Opsional, Contoh: SMART10):")
        diskon_voucher = 0
        if voucher_input.strip() == "SMART10":
            diskon_voucher = 0.10 * subtotal
            
        ppn = 0.11 * (subtotal - diskon_voucher)
        total_akhir = (subtotal - diskon_voucher) + ppn
        
        pilihan_skema = st.radio("Skema Pembayaran:", ["Full Payment (Bayar 100%)", "Deposit 30%"])
        metode_pilih = st.selectbox("Metode Pembayaran:", ["Transfer BCA", "Transfer Mandiri", "E-Wallet DANA", "OVO", "GoPay"])
        
        st.markdown("### 📋 Payment Summary")
        summary_text = f"""
================================================
                PAYMENT SUMMARY                 
================================================
{ck['tipe']} ({durasi} Malam)    : Rp {biaya_kamar:,}
Total Layanan Tambahan (Add-On) : Rp {biaya_addons:,}
------------------------------------------------
Subtotal                        : Rp {subtotal:,}
Diskon Voucher                  : Rp {diskon_voucher:,}
PPN 11%                         : Rp {ppn:,}
------------------------------------------------
TOTAL TAGIHAN                   : Rp {total_akhir:,}
================================================
        """
        st.code(summary_text, language="text")
        
        if pilihan_skema == "Deposit 30%":
            nilai_depo = total_akhir * 0.3
            st.warning(f"Wajib Bayar Deposit (30%): Rp {nilai_depo:,}")
            status_bayar_tag = "🟠 Deposit Paid"
        else:
            status_bayar_tag = "PAID"
            
        if st.button("Finalisasi Transaksi & Terbitkan Invoice 🚀", type="primary"):
            new_inv_id = f"INV2026{len(st.session_state.reservasi_db) + 1:03d}"
            
            st.session_state.reservasi_db.append({
                "id": new_inv_id, "nama": ck["nama"], "hp": ck["hp"], "email": ck["email"], "alamat": ck["alamat"],
                "kamar": ck["kamar"], "tipe": ck["tipe"], "check_in": ck["check_in"], "check_out": ck["check_out"],
                "tujuan": ck["tujuan"], "status": "Booking", "total_biaya": total_akhir, "status_bayar": status_bayar_tag,
                "metode": metode_pilih, "deposit_tipe": pilihan_skema, "add_ons": ck["add_ons"]
            })
            
            if ck["kamar"] in st.session_state.kamar_db:
                st.session_state.kamar_db[ck["kamar"]]["status"] = "🟨 Booking"
            
            del st.session_state.proses_checkout
            st.success(f"Invoice {new_inv_id} Berhasil Disimpan!")
            st.rerun()

# ==========================================
# MENU 8: RIWAYAT PEMBAYARAN
# ==========================================
elif menu == "📜 Riwayat Pembayaran":
    st.title("📜 Auto Invoice & E-Receipt Center")
    
    if st.session_state.reservasi_db:
        df_pay = pd.DataFrame(st.session_state.reservasi_db)
        st.table(df_pay[["id", "nama", "metode", "status_bayar", "total_biaya"]])
    else:
        st.warning("Belum ada riwayat pembayaran.")

# ==========================================
# MENU 9: CUSTOMER VIP
# ==========================================
elif menu == "👤 Customer VIP":
    st.title("👤 Customer VIP Leaderboard")
    
    df_vip = pd.DataFrame(st.session_state.customer_history)
    df_sorted = df_vip.sort_values(by="kunjungan", ascending=False)
    
    st.subheader("🏆 Papan Peringkat Loyalty Member (Sorted)")
    st.table(df_sorted)

# ==========================================
# MENU 10: REVIEW HOTEL
# ==========================================
elif menu == "⭐ Review Hotel":
    st.title("⭐ Review & Rating Kepuasan")
    
    with st.form("Form_Review"):
        r_nama = st.text_input("Nama Anda:")
        r_star = st.slider("Beri Bintang:", 1, 5, 5)
        r_msg = st.text_area("Tulis Komentar:")
        if st.form_submit_button("Kirim Ulasan"):
            if r_nama and r_msg:
                st.session_state.reviews_db.append({
                    "nama": r_nama, "rating": r_star, "komentar": r_msg, "tanggal": str(date.today())
                })
                st.success("Review berhasil ditambahkan!")
                st.rerun()
                
    st.markdown("---")
    for row in st.session_state.reviews_db:
        st.markdown(f"**{row['nama']}** — {'⭐' * row['rating']} ({row['tanggal']})")
        st.caption(f"\"{row['komentar']}\"")

# ==========================================
# MENU 11: ANALYTICS CENTER
# ==========================================
elif menu == "📊 Analytics Center":
    st.title("📊 Analytics Center & Prediksi Omset")
    
    if st.session_state.reservasi_db:
        total_omset = sum(r["total_biaya"] for r in st.session_state.reservasi_db)
        prediksi_omset = total_omset * 1.25
        
        st.metric("Total Pendapatan Saat Ini", f"Rp {total_omset:,}")
        st.metric("🔮 Prediksi Pendapatan Bulan Depan", f"Rp {prediksi_omset:,.0f}")
        st.caption("Prediksi dihitung otomatis dengan faktor tren okupansi 125%.")
    else:
        st.warning("Data transaksi belum cukup untuk melakukan analisis.")
