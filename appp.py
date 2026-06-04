# ==========================================
# IMPORT LIBRARY UTAMA
# ==========================================
import streamlit as st
import pandas as pd
from datetime import datetime, date

# Setingan awal layout browser biar melebar
st.set_page_config(
    page_title="Denara Hotel System",
    layout="wide",
    page_icon="🏨"
)

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
# ==========================================
# SIDEBAR MENU (VERSI RAPIH & TERKELOMPOK)
# ==========================================
st.sidebar.markdown("# 🏨 Denara Hotel System")
st.sidebar.caption("Sistem Log Internal Kontrol")
st.sidebar.markdown("---")

menu_utama = st.sidebar.radio("📂 Pilih Kategori", [
    "🏠 Dashboard",
    "🏨 Manajemen Kamar",
    "🍽️ Layanan Hotel",
    "💳 Transaksi & Data",
    "⭐ Customer Experience",
    "📊 Laporan & Bantuan"
])

# Sub menu dinamis
if menu_utama == "🏠 Dashboard":
    pilihan_menu = "Dashboard"

elif menu_utama == "🏨 Manajemen Kamar":
    pilihan_menu = st.sidebar.radio("Menu Kamar", [
        "📝 Reservasi Baru",
        "🏨 Daftar Katalog Kamar",
        "🗺️ Room Map Denah"
    ])

elif menu_utama == "🍽️ Layanan Hotel":
    pilihan_menu = "🍽️ Room Service (DenaraEats)"

elif menu_utama == "💳 Transaksi & Data":
    pilihan_menu = st.sidebar.radio("Menu Transaksi", [
        "💳 Kasir & Pembayaran",
        "🔍 Cari Reservasi",
        "📋 Data Master Log",
        "📜 Histori Transaksi"
    ])

elif menu_utama == "⭐ Customer Experience":
    pilihan_menu = st.sidebar.radio("Menu Customer", [
        "⭐ Ulasan Kepuasan",
        "👤 Poin Loyalitas VIP",
        "🏷️ Info Voucher Promo"
    ])

elif menu_utama == "📊 Laporan & Bantuan":
    pilihan_menu = st.sidebar.radio("Menu Laporan", [
        "📊 Analisis Keuangan",
        "🛟 Pusat Bantuan"
    ])

# ==========================================
# LOGIKA OPERASIONAL PER HALAMAN MENU
# ==========================================

# --- MENU 1: DASHBOARD SUMMARY ---
if pilihan_menu == "Dashboard":
    st.title("🏠 Dashboard Summary")
    
    # Hitung jumlah kondisi kamar saat ini secara realtime dari memori
    total_kmr = len(st.session_state.kamar_data)
    isi = sum(1 for d in st.session_state.kamar_data.values() if d["status"] == "🟥 Terisi")
    book = sum(1 for d in st.session_state.kamar_data.values() if d["status"] == "🟨 Booking")
    kosong = total_kmr - isi - book
    
    # Render tampilan info angka kotak-kotak di atas dashboard
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Kamar Kosong Ready 🟩", kosong)
    c2.metric("Kamar Aktif Terisi 🟥", isi)
    c3.metric("Total Data Transaksi", len(st.session_state.reservasi_log))
    c4.metric("Antrean Dapur 🍽️", len(st.session_state.makanan_log))
    
    st.markdown("---")
    st.subheader("📢 Promo Event Hari Ini")
    st.info("Info kupon aktif: Ketik kode **DENARADEAL** pas kasir buat potong harga Rp 100.000!")

# --- MENU 2: INPUT RESERVASI BARU ---
elif pilihan_menu == "📝 Reservasi Baru":
    st.title("📝 Input Reservasi Tamu Baru")
    # Bagi layar jadi kolom kiri (form) dan kolom kanan (rekomendasi & alokasi)
    col_kiri, col_kanan = st.columns([1.5, 1])
    
    with col_kiri:
        st.subheader("Biodata Isian Tamu")
        nama = st.text_input("Nama Lengkap")
        hp = st.text_input("No HP / WhatsApp")
        email = st.text_input("Email Tamu")
        pilihan_tipe_kamar = st.selectbox("Tipe Kamar", list(TARIF_KAMAR.keys()))
        pilihan_bed = st.selectbox("Jenis Bed Kasur", ["Single Bed", "Double Bed", "Twin Bed"])
        jml_tamu = st.number_input("Jumlah Orang Menginap", min_value=1, max_value=10, value=1)
        tgl_in = st.date_input("Tanggal Check-In", date.today())
        tgl_out = st.date_input("Tanggal Check-Out", date.today() + pd.Timedelta(days=1))
        pilihan_late = st.selectbox("Request Jam Check-Out", ["Normal Check-Out", "Late Check-Out (+Rp 50.000)"])
        
    with col_kanan:
        # Bagian pengecekan aturan otomatis kelayakan kamar
        st.subheader("🤖 Smart Room Recommendation")
        
        valid_rekomendasi = True
        pesan_saran = ""
        
        # Aturan 1: Cek kapasitas orang untuk tipe kamar standard
        if pilihan_tipe_kamar == "Standard Room" and jml_tamu > 2:
            valid_rekomendasi = False
            pesan_saran = "⚠️ Kapasitas Standard Room maks. 2 orang. Disarankan pindah ke Deluxe/Family."
            
        # Aturan 2: Cek ketersediaan tipe kasur twin bed di kamar standard
        elif pilihan_tipe_kamar == "Standard Room" and pilihan_bed == "Twin Bed":
            valid_rekomendasi = False
            pesan_saran = "⚠️ Slot Twin Bed untuk tipe Standard terbatas saat ini. Disarankan memakai Double Bed atau pilih tipe Deluxe."
            
        # Aturan 3: Cek rombongan besar biar ga sumpek di kamar kecil
        elif jml_tamu > 4 and pilihan_tipe_kamar in ["Standard Room", "Deluxe Room"]:
            valid_rekomendasi = False
            pesan_saran = "💡 Jumlah tamu banyak (>4 orang). Direkomendasikan ganti ke Family atau Suite Room."

        # Munculin status notifikasi hasil filter validasi ke layar
        if not valid_rekomendasi:
            st.warning(pesan_saran)
        else:
            st.success("✨ Pilihan kombinasi tipe kamar, kasur, dan kapasitas tamu sudah sesuai standar manufaktur hotel.")

        st.markdown("---")
        st.subheader("⚙️ Alokasi Kamar Fisik (Auto)")
        
        # Proses looping mencari nomor kamar kosong terendah yang tipenya sesuai request
        kamar_cocok = None
        for no, detail in st.session_state.kamar_data.items():
            if detail["tipe"] == pilihan_tipe_kamar and detail["status"] == "🟩 Tersedia":
                kamar_cocok = no
                break
                
        # Kasih feedback status pencarian nomor kamar otomatisnya
        if kamar_cocok:
            st.success(f"Kamar Terkunci Otomatis: **Nomor {kamar_cocok}** ({st.session_state.kamar_data[kamar_cocok]['view']})")
        else:
            st.error("Kamar tipe ini penuh!")
            kamar_cocok = st.text_input("Ketik Manual Nomor Kamar Cadangan:")
            
        st.markdown("---")
        st.subheader("🎁 Layanan Tambahan")
        addons = []
        if st.checkbox("Sarapan Pagi Buffet (+Rp 50.000)"): addons.append("Breakfast")
        if st.checkbox("Jemputan Bandara (+Rp 150.000)"): addons.append("Airport Pickup")

    # Tombol klik buat nge-lock data form bookingan dan dioper ke kasir
    if st.button("Kunci Pemesanan & Lanjut Bayar ➡️", type="primary"):
        if not nama or not kamar_cocok:
            st.error("Nama tamu dan nomor kamar wajib diisi!")
        else:
            # Nyimpan data sementara ke laci temporary 'proses_checkout'
            st.session_state.proses_checkout = {
                "nama": nama, "hp": hp, "email": email, "kamar": kamar_cocok, 
                "tipe": pilihan_tipe_kamar, "bed_type": pilihan_bed,
                "check_in": str(tgl_in), "check_out": str(tgl_out), "add_ons": addons, "late_checkout": pilihan_late
            }
            st.success("Data masuk antrean kasir. Silakan klik menu '💳 Kasir & Pembayaran' di sidebar.")

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

# --- MENU12: DASHBOARD FEEDBACK PELANGGAN ---
elif pilihan_menu == "⭐ Ulasan Kepuasan":
    st.title("📊 Dashboard Feedback Pelanggan")

    # Jika belum ada data
    if not st.session_state.ulasan_log:
        st.info("Belum ada data ulasan pelanggan.")
    else:
        data = st.session_state.ulasan_log

        # ==========================================
        # METRIC RINGKASAN
        # ==========================================
        total_ulasan = len(data)
        rata_rating = sum([u["rating"] for u in data]) / total_ulasan
        rating_tertinggi = max([u["rating"] for u in data])
        rating_terendah = min([u["rating"] for u in data])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Ulasan", total_ulasan)
        col2.metric("Rata-rata Rating", f"{rata_rating:.2f} ⭐")
        col3.metric("Tertinggi", f"{rating_tertinggi} ⭐")
        col4.metric("Terendah", f"{rating_terendah} ⭐")

        st.markdown("---")

        # ==========================================
        # DISTRIBUSI RATING (GRAFIK)
        # ==========================================
        import pandas as pd

        df = pd.DataFrame(data)
        rating_count = df["rating"].value_counts().sort_index()

        st.subheader("📈 Distribusi Rating")
        st.bar_chart(rating_count)

        st.markdown("---")

        # ==========================================
        # ULASAN TERBARU
        # ==========================================
        st.subheader("📝 Ulasan Terbaru")

        for r in reversed(data[-5:]):  # tampilkan 5 terbaru
            st.markdown(f"""
            <div style="background:#1E293B; padding:10px; border-radius:10px; margin-bottom:10px;">
                <b>{r['nama']}</b> — {'⭐'*r['rating']} <br>
                <small>{r['tanggal']}</small><br>
                <i>"{r['komentar']}"</i>
            </div>
            """, unsafe_allow_html=True)

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
