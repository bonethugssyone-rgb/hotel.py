# ==========================================
# IMPORT LIBRARY UTAMA
# ==========================================
import streamlit as st
import pandas as pd
from datetime import datetime, date

# Setingan awal layout browser biar melebar
st.markdown("""
<style>
/* Base Theme */
.main { background-color: #FDF2F8; }
section[data-testid="stSidebar"] { background-color: #FCE7F3; }

/* Styling Card */
.card {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #FBCFE8;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* Typography */
h1, h2, h3 { color: #831843; }
p, label { color: #9D174D; }

/* Buttons & Inputs */
.stButton>button {
    background-color: #DB2777;
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: bold;
}
.stTextInput > div > div > input, .stSelectbox > div > div {
    background-color: #FFF1F2 !important;
    border: 1px solid #FECDD3 !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# INISIALISASI DATA SIMULASI (SESSION STATE)
# ==========================================

# Penampung data master seluruh kamar dari lantai 1 sampai 5 (di RAM)
if "kamar_data" not in st.session_state:
    st.session_state.kamar_data = {
        # Lantai 1
        "101": {"tipe": "Standard Room", "harga": 300000, "status": "🟩 Tersedia", "view": "No View"},
        "102": {"tipe": "Standard Room", "harga": 300000, "status": "🟥 Terisi", "view": "Garden View"},
        "103": {"tipe": "Standard Room", "harga": 300000, "status": "🟩 Tersedia", "view": "Garden View"},
        "104": {"tipe": "Standard Room", "harga": 300000, "status": "🟩 Tersedia", "view": "No View"},
        "105": {"tipe": "Deluxe Room", "harga": 500000, "status": "🟨 Booking", "view": "City View"},
        "106": {"tipe": "Deluxe Room", "harga": 500000, "status": "🟩 Tersedia", "view": "City View"},
        # Lantai 2
        "201": {"tipe": "Deluxe Room", "harga": 500000, "status": "🟩 Tersedia", "view": "Pool View"},
        "202": {"tipe": "Deluxe Room", "harga": 500000, "status": "🟩 Tersedia", "view": "Pool View"},
        "203": {"tipe": "Deluxe Room", "harga": 500000, "status": "🟩 Tersedia", "view": "Garden View"},
        "204": {"tipe": "Family Room", "harga": 800000, "status": "🟥 Terisi", "view": "City View"},
        "205": {"tipe": "Family Room", "harga": 800000, "status": "🟩 Tersedia", "view": "Pool View"},
        "206": {"tipe": "Family Room", "harga": 800000, "status": "🟩 Tersedia", "view": "Garden View"},
        # Lantai 3
        "301": {"tipe": "Family Room", "harga": 800000, "status": "🟩 Tersedia", "view": "City View"},
        "302": {"tipe": "Family Room", "harga": 800000, "status": "🟩 Tersedia", "view": "Pool View"},
        "303": {"tipe": "Suite Room", "harga": 1200000, "status": "🟩 Tersedia", "view": "Ocean View"},
        "304": {"tipe": "Suite Room", "harga": 1200000, "status": "🟩 Tersedia", "view": "Ocean View"},
        "305": {"tipe": "Suite Room", "harga": 1200000, "status": "🟩 Tersedia", "view": "City View"},
        # Lantai 4
        "401": {"tipe": "Standard Room", "harga": 300000, "status": "🟩 Tersedia", "view": "No View"},
        "402": {"tipe": "Standard Room", "harga": 300000, "status": "🟩 Tersedia", "view": "Garden View"},
        "403": {"tipe": "Deluxe Room", "harga": 500000, "status": "🟩 Tersedia", "view": "City View"},
        "404": {"tipe": "Deluxe Room", "harga": 500000, "status": "🟩 Tersedia", "view": "Pool View"},
        "405": {"tipe": "Family Room", "harga": 800000, "status": "🟩 Tersedia", "view": "Garden View"},
        # Lantai 5
        "501": {"tipe": "Suite Room", "harga": 1200000, "status": "🟩 Tersedia", "view": "Skyline View"},
        "502": {"tipe": "Suite Room", "harga": 1200000, "status": "🟩 Tersedia", "view": "Skyline View"},
        "503": {"tipe": "Suite Room", "harga": 1200000, "status": "🟩 Tersedia", "view": "Ocean View"}
    }

# Array dinamis untuk nyimpan riwayat bookingan transaksi tamu
if "reservasi_log" not in st.session_state:
    st.session_state.reservasi_log = [
        {
            "id": "INV2026001", "nama": "Andi", "hp": "0812345678", "email": "andi@mail.com",
            "kamar": "102", "tipe": "Standard Room", "bed_type": "Double Bed",
            "check_in": "2026-06-01", "check_out": "2026-06-03", "status": "Check-In", 
            "total_biaya": 600000, "status_bayar": "PAID", "metode": "Transfer BCA", 
            "late_checkout": "Normal Check-Out", "poin_earned": 60
        }
    ]

# Array dinamis untuk antrean pesanan makanan room service
if "makanan_log" not in st.session_state:
    st.session_state.makanan_log = [
        {"kamar": "102", "pesanan": "Nasi Goreng Spesial + Es Teh Manis", "total": 65000, "status": "Diproses"}
    ]

# Array dinamis untuk nampung review atau rating dari tamu
if "ulasan_log" not in st.session_state:
    st.session_state.ulasan_log = [
        {"nama": "Andi", "rating": 5, "komentar": "Kamarnya bersih, pelayanan mantap!", "tanggal": "2026-06-03"}
    ]

# Kamus harga sewa per malam masing-masing tipe kamar
TARIF_KAMAR = {
    "Standard Room": 300000, 
    "Deluxe Room": 500000, 
    "Family Room": 800000, 
    "Suite Room": 1200000
}

# ==========================================
# SIDEBAR MENU NAVIGATION
# ==========================================
st.sidebar.markdown("# 🏨 Denara Hotel System")
st.sidebar.caption("Sistem Log Internal Kontrol")
st.sidebar.markdown("---")

# Mengelompokkan pilihan menu di sidebar biar rapi
st.sidebar.markdown("### 🔑 OPERASIONAL KAMAR")
menu_kamar = ["Dashboard", "📝 Reservasi Baru", "🏨 Daftar Katalog Kamar", "🗺️ Room Map Denah"]

st.sidebar.markdown("### 🍽️ LAYANAN TAMBAHAN")
menu_layanan = ["🍽️ Room Service (DenaraEats)"]

st.sidebar.markdown("### 💼 BACKOFFICE ADM")
menu_admin = ["🔍 Cari Reservasi", "📋 Data Master Log", "💳 Kasir & Pembayaran", "📜 Histori Transaksi"]

st.sidebar.markdown("### 💎 INTERAKSI & LOYALITAS")
menu_loyalty = ["👤 Poin Loyalitas VIP", "🏷️ Info Voucher Promo", "⭐ Ulasan Kepuasan", "📊 Analisis Keuangan", "🛟 Pusat Bantuan"]

# Satukan semua menu dan pasang ke widget pilihan radio sidebar
semua_menu = menu_kamar + menu_layanan + menu_admin + menu_loyalty
pilihan_menu = st.sidebar.radio("🧭 NAVIGASI PANEL", semua_menu)

# ==========================================
# LOGIKA OPERASIONAL PER HALAMAN MENU
# ==========================================
# --- MENU 1: DASHBOARD SUMMARY ---
if pilihan_menu == "Dashboard":

    total_kmr = len(st.session_state.kamar_data)
    isi = sum(1 for k in st.session_state.kamar_data.values() if "Terisi" in k["status"])
    kosong = total_kmr - isi

    st.markdown("## 🏨 Denara Hotel Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    def card(title, value, color):
        st.markdown(f"""
        <div class="card">
            <h4>{title}</h4>
            <h2 style='color:{color}'>{value}</h2>
        </div>
        """, unsafe_allow_html=True)

    with c1:
        card("Kamar Kosong", kosong, "#22C55E")

    with c2:
        card("Kamar Terisi", isi, "#EF4444")

    with c3:
        card("Transaksi", len(st.session_state.reservasi_log), "#3B82F6")

    with c4:
        card("Room Service", len(st.session_state.makanan_log), "#F59E0B")

    st.markdown("---")
    st.subheader("📢 Promo Event Hari Ini")
    st.info("Info kupon aktif: Ketik kode **DENARADEAL** pas kasir buat potong harga Rp 100.000!")
elif pilihan_menu == "📝 Reservasi Baru":

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        nama = st.text_input("Nama")
        hp = st.text_input("No HP")
        email = st.text_input("Email")

        pilihan_tipe_kamar = st.selectbox("Tipe Kamar", list(TARIF_KAMAR.keys()))
        pilihan_bed = st.selectbox("Tipe Kasur", ["Single Bed","Double Bed","Twin Bed"])

        jml_tamu = st.number_input("Jumlah Tamu",1,10)

        tgl_in = st.date_input("Check-in")
        tgl_out = st.date_input("Check-out")

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("🤖 AI Recommendation")

        if jml_tamu <= 2:
            st.success("Cocok untuk Standard Room")
        elif jml_tamu <=4:
            st.info("Cocok untuk Deluxe")
        else:
            st.warning("Gunakan Family / Suite")

        st.markdown('</div>', unsafe_allow_html=True)

    # VALIDASI
    valid_rekomendasi = True
    pesan_saran = ""

    if pilihan_tipe_kamar == "Standard Room" and jml_tamu > 2:
        valid_rekomendasi = False
        pesan_saran = "⚠️ Maks 2 orang"

    elif jml_tamu > 4 and pilihan_tipe_kamar in ["Standard Room","Deluxe Room"]:
        valid_rekomendasi = False
        pesan_saran = "💡 Gunakan Family/Suite"

    if not valid_rekomendasi:
        st.warning(pesan_saran)
    else:
        st.success("Pilihan sesuai")

    # AUTO KAMAR
    kamar_cocok = None
    for no, detail in st.session_state.kamar_data.items():
        if detail["tipe"] == pilihan_tipe_kamar and detail["status"] == "🟩 Tersedia":
            kamar_cocok = no
            break

    if kamar_cocok:
        st.success(f"Kamar: {kamar_cocok}")
    else:
        st.error("Penuh")

    # BUTTON
    if st.button("Lanjut Kasir"):
        if not nama or not kamar_cocok:
            st.error("Data belum lengkap")
        else:
            st.session_state.proses_checkout = {
                "nama": nama,
                "hp": hp,
                "email": email,
                "kamar": kamar_cocok,
                "tipe": pilihan_tipe_kamar,
                "bed_type": pilihan_bed,
                "check_in": str(tgl_in),
                "check_out": str(tgl_out),
                "add_ons": [],
                "late_checkout": "Normal"
            }
            st.success("Masuk kasir")

# --- MENU 3: KATALOG INFO KAMAR ---
elif pilihan_menu == "🏨 Daftar Katalog Kamar":
    st.title("🏨 Katalog Info Kamar")
    # Looping tampilin harga dan deskripsi sewa kamar hotel
    for tipe, harga in TARIF_KAMAR.items():
        with st.expander(f"Kategori: {tipe} — Rp {harga:,} / Malam"):
            st.write("Fasilitas standar: AC, Smart TV, Free Wifi, air mineral, serta daily cleaning service.")

# --- MENU 4: DENAH VISUAL KAMAR PER LANTAI ---
elif pilihan_menu == "🗺️ Room Map Denah":
    st.title("🗺️ Denah Status Blok Kamar")
    
    # Looping rapi membagi blok visual kotak per lantai (Lantai 1-5)
    for lt in range(1, 6):
        st.subheader(f"🏢 Lantai {lt}")
        # Nyaring nomor kamar yang angka depannya sama dengan tingkat lantai
        kamar_lantai = {no: det for no, det in st.session_state.kamar_data.items() if no.startswith(str(lt))}
        
        cols = st.columns(6)
        for idx, (nomor, detail) in enumerate(kamar_lantai.items()):
            with cols[idx % 6]:
                # Warnai kotak sesuai indikator status kamarnya saat ini
                if "Tersedia" in detail["status"]: 
                    st.success(f"**{nomor}**\n🟩 Ready\n*{detail['view']}*")
                elif "Terisi" in detail["status"]: 
                    st.error(f"**{nomor}**\n🟥 Terisi\n*{detail['tipe']}*")
                else: 
                    st.warning(f"**{nomor}**\n🟨 Booked\n*{detail['tipe']}*")
        st.markdown("---")

# --- MENU 5: ROOM SERVICE FOOD ORDER ---
elif pilihan_menu == "🍽️ Room Service (DenaraEats)":
    st.title("🍽️ Room Service Order")
    k1, k2 = st.columns(2)
    
    with k1:
        st.subheader("Input Menu Makanan")
        no_kmr = st.selectbox("Nomor Kamar Pemesan:", list(st.session_state.kamar_data.keys()))
        pilih_makanan = st.multiselect("Pilih Menu:", ["Nasi Goreng Gila (Rp 35.000)", "Mie Goreng Kampung (Rp 30.000)", "Es Teh Manis (Rp 10.000)", "Kopi Susu Aren (Rp 20.000)"])
        
        # Rumus manual kalkulasi hitung belanja makanan-minuman
        nota_makanan = 0
        for m in pilih_makanan:
            if "Gila" in m: nota_makanan += 35000
            elif "Mie" in m: nota_makanan += 30000
            elif "Teh" in m: nota_makanan += 10000
            elif "Kopi" in m: nota_makanan += 20000
            
        if st.button("Kirim Orderan ke Dapur 🍳"):
            if pilih_makanan:
                # Masukin data belanjaan baru ke ujung index array makanan_log (.append)
                st.session_state.makanan_log.append({
                    "kamar": no_kmr, "pesanan": ", ".join(pilih_makanan), "total": nota_makanan, "status": "Diproses"
                })
                st.success("Orderan berhasil dikirim ke dapur!")
            else:
                st.warning("Pilih menu makanan dulu!")
                
    with k2:
        st.subheader("📋 Status Pengantaran Dapur")
        df_rs = pd.DataFrame(st.session_state.makanan_log)
        if not df_rs.empty:
            st.dataframe(df_rs, use_container_width=True)

# --- MENU 6: PENCARIAN DATA TAMU ---
elif pilihan_menu == "🔍 Cari Reservasi":
    st.title("🔍 Cari Data Booking Tamu")
    cari = st.text_input("Ketik Nama Tamu atau Nomor Kamar:")
    if cari:
        # Melakukan scan / pencarian manual mencocokan kata kunci di dalam list array
        ketemu = [r for r in st.session_state.reservasi_log if cari.lower() in r["nama"].lower() or cari == r["kamar"]]
        if ketemu: 
            st.table(pd.DataFrame(ketemu)[["id", "nama", "kamar", "tipe", "check_in", "status"]])
        else: 
            st.warning("Data tidak ketemu!")

# --- MENU 7: KENDALI DATA MASTER LOG (CRUD OPERASIONAL) ---
elif pilihan_menu == "📋 Data Master Log":
    st.title("📋 Log Kendali Master Data")
    if st.session_state.reservasi_log:
        df_log = pd.DataFrame(st.session_state.reservasi_log)
        st.dataframe(df_log[["id", "nama", "kamar", "tipe", "check_in", "check_out", "status"]], use_container_width=True)
        
        st.markdown("---")
        st.subheader("Ubah Status Tamu")
        id_target = st.selectbox("Pilih ID Invoice:", df_log["id"].tolist())
        # Nyari posisi baris index data di dalam array list berdasarkan ID nota invoice
        idx = next((i for i, item in enumerate(st.session_state.reservasi_log) if item["id"] == id_target), None)
        
        b1, b2 = st.columns(2)
        if b1.button("Set CHECK-IN 🟥") and idx is not None:
            # Ubah log reservasi jadi check-in dan ubah warna fisik kamar jadi merah terisi
            st.session_state.reservasi_log[idx]["status"] = "Check-In"
            st.session_state.kamar_data[st.session_state.reservasi_log[idx]["kamar"]]["status"] = "🟥 Terisi"
            st.rerun()
            
        if b2.button("Set CHECK-OUT 🟩") and idx is not None:
            # Ubah log reservasi jadi check-out dan balikkan warna fisik kamar jadi hijau ready kosong
            st.session_state.reservasi_log[idx]["status"] = "Check-Out"
            st.session_state.kamar_data[st.session_state.reservasi_log[idx]["kamar"]]["status"] = "🟩 Tersedia"
            st.rerun()

# --- MENU 8: BILLING STRUK & HITUNGAN KASIR ---
elif pilihan_menu == "💳 Kasir & Pembayaran":
    st.title("💳 Billing Kasir Pembayaran")
    # Cek ketersediaan antrean form booking
    if "proses_checkout" not in st.session_state:
        st.info("Antrean kasir kosong. Silakan isi dulu form di menu '📝 Reservasi Baru'.")
    else:
        dt = st.session_state.proses_checkout
        # Ambil objek datetime buat kalkulasi jumlah selisih hari menginap
        in_dt = datetime.strptime(dt["check_in"], "%Y-%m-%d")
        out_dt = datetime.strptime(dt["check_out"], "%Y-%m-%d")
        malam = max(1, (out_dt - in_dt).days)
        
        # Hitung kalkulasi perkalian tarif total biaya rincian
        harga_pokok = TARIF_KAMAR.get(dt["tipe"], 300000) * malam
        biaya_late = 50000 if "Late" in dt["late_checkout"] else 0
        biaya_addon = len(dt["add_ons"]) * 50000
        
        subtotal = harga_pokok + biaya_late + biaya_addon
        
        kode_kupon = st.text_input("Ketik Kode Kupon Voucher:")
        diskon = 100000 if kode_kupon.strip() == "DENARADEAL" else 0
        
        total_tagihan = max(0, subtotal - diskon)
        poin = int(total_tagihan / 10000) # Kasih bonus loyalty reward poin per kelipatan transaksi 10 ribu
        
        # Cetak tampilan teks nota kuitansi manual
        st.code(f"""
        ================================================
                      DENARA HOTEL SYSTEM               
                        E-RECEIPT STRUK                 
        ================================================
        Nama Tamu       : {dt['nama']}
        Kamar           : No. {dt['kamar']} ({dt['tipe']})
        Durasi          : {malam} Malam
        ------------------------------------------------
        Biaya Kamar     : Rp {harga_pokok:,}
        Biaya Addons    : Rp {biaya_late + biaya_addon:,}
        Diskon Voucher  : -Rp {diskon:,}
        ------------------------------------------------
        TOTAL BAYAR     : Rp {total_tagihan:,}
        Bonus Poin      : +{poin} DenaraPoints
        ================================================
        """, language="text")
        
        cara_bayar = st.selectbox("Pilih Metode Bank Transaksi:", ["BCA Transfer Direct", "Mandiri Virtual Account", "DenaraPay"])
        
        if st.button("Finalisasi Transaksi & Cetak 📑", type="primary"):
            # Append / masukin record baru ke dalam data riwayat log pembayaran transaksi
            st.session_state.reservasi_log.append({
                "id": f"INV2026{len(st.session_state.reservasi_log)+1:03d}",
                "nama": dt["nama"], "hp": dt["hp"], "email": dt["email"],
                "kamar": dt["kamar"], "tipe": dt["tipe"], "bed_type": dt["bed_type"],
                "check_in": dt["check_in"], "check_out": dt["check_out"], "status": "Booking",
                "total_biaya": total_tagihan, "status_bayar": "PAID", "metode": cara_bayar,
                "add_ons": dt["add_ons"], "late_checkout": dt["late_checkout"], "poin_earned": poin
            })
            # Ganti warna denah kamar jadi kuning (booked)
            st.session_state.kamar_data[dt["kamar"]]["status"] = "🟨 Booking"
            # Bersihkan isi laci temporary kasir
            del st.session_state.proses_checkout
            st.success("Pembayaran lunas disimpan!")
            st.rerun()

# --- MENU 9: HISTORI TRANSAKSI SELESAI ---
elif pilihan_menu == "📜 Histori Transaksi":
    st.title("📜 Riwayat Cetak Invoice Pembayaran")
    if st.session_state.reservasi_log:
        st.table(pd.DataFrame(st.session_state.reservasi_log)[["id", "nama", "metode", "total_biaya", "status_bayar"]])

# --- MENU 10: REPORT POIN REWARD LOYALITAS VIP ---
elif pilihan_menu == "👤 Poin Loyalitas VIP":
    st.title("👤 Akumulasi Poin Reward Pelanggan")
    if st.session_state.reservasi_log:
        df_res = pd.DataFrame(st.session_state.reservasi_log)
        # Kelompokkan total akumulasi perolehan poin berdasarkan nama pelanggan
        df_poin = df_res.groupby("nama")["poin_earned"].sum().reset_index()
        
        def hitung_tier(p):
            if p >= 100: return "💎 VIP Member"
            if p >= 50: return "🥇 Gold Member"
            return "🥈 Silver Member"
            
        df_poin["Kategori Tier"] = df_poin["poin_earned"].apply(hitung_tier)
        st.table(df_poin.rename(columns={"nama": "Nama Tamu", "poin_earned": "Total Poin"}))

# --- MENU 11: INFO KODE PROMO AKTIF ---
elif pilihan_menu == "🏷️ Info Voucher Promo":
    st.title("🏷️ Kode Promo Aktif")
    st.markdown("---")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.info("### Code: DENARADEAL\nPotongan instan Rp 100.000 tanpa batas minimum.")
    with col_p2:
        st.warning("### Code: SMART10\nDiskon potongan hemat 10% khusus pengguna kartu kredit.")

# --- MENU 12: ULASAN DAN TESTIMONI TAMU ---
elif pilihan_menu == "⭐ Ulasan Kepuasan":
    st.title("⭐ Feedback & Ulasan Tamu")
    with st.form("Form_Ulasan"):
        u_nama = st.text_input("Nama Pengulas:")
        u_skor = st.slider("Bintang Kepuasan:", 1, 5, 5)
        u_teks = st.text_area("Isi Ulasan:")
        if st.form_submit_button("Kirim Review"):
            if u_nama and u_teks:
                # Masukin data feedback baru ke array ulasan_log
                st.session_state.ulasan_log.append({
                    "nama": u_nama, "rating": u_skor, "komentar": u_teks, "tanggal": str(date.today())
                })
                st.success("Ulasan berhasil dikirim!")
                st.rerun()
                
    st.markdown("---")
    # Looping tampilin ulasan terbalik (ulasan terbaru muncul paling atas)
    for r in reversed(st.session_state.ulasan_log):
        st.markdown(f"**{r['nama']}** — {'⭐' * r['rating']} ({r['tanggal']})")
        st.caption(f"\"{r['komentar']}\"")

# --- MENU 13: GRAFIK FINANSIAL OMSET ---
elif pilihan_menu == "📊 Analisis Keuangan":
    st.title("📊 Grafik Omset Finansial")
    if st.session_state.reservasi_log:
        df_an = pd.DataFrame(st.session_state.reservasi_log)
        total_omset = df_an["total_biaya"].sum()
        st.metric("Total Omset Masuk RAM", f"Rp {total_omset:,}")
        st.metric("Target Omset Estimasi Next Month (+20%)", f"Rp {int(total_omset * 1.20):,}")
        # Gambar grafik batang pendapatan dari pembagian kategori tipe sewaan kamar
        st.bar_chart(df_an.groupby("tipe")["total_biaya"].sum())

# --- MENU 14: FAQ PUSAT BANTUAN ---
elif pilihan_menu == "🛟 Pusat Bantuan":
    st.title("🛟 FAQ Layanan")
    with st.expander("Bagaimana cara cancel status kamar?"):
        st.write("Akses menu '📋 Data Master Log', pilih ID Invoice target, lalu lakukan update perubahan status check-out.")
    with st.expander("Apakah data hilang kalau browser ditutup?"):
        st.write("Iya, karena program ini murni berjalan di memori lokal runtime RAM web (session state) tanpa database eksternal.")
