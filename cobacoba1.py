# ==============================================================================
# IMPORT LIBRARY YANG DI BUTUHKAN
# ==============================================================================
import streamlit as st  # Library utama untuk membangun antarmuka (UI) web dashboard secara interaktif
import pandas as pd     # Library manipulasi data untuk menyusun tabel (DataFrame) dan merender grafik/chart
from datetime import datetime, date  # Library bawaan Python untuk mengolah data penanggalan (waktu check-in/out)

# Mengonfigurasi properti dasar halaman web Streamlit (Judul tab browser, tata letak melebar, dan ikon hotel)
st.set_page_config(page_title="SmartStay Hotel System", layout="wide", page_icon="🏨")

# ==============================================================================
# 1. INISIALISASI DATA AWAL (MOCK DATA) DI MEMORI RUNTIME STREAMLIT (SESSION STATE)
# ==============================================================================

# Memeriksa apakah database master kamar sudah ada di memori. Jika belum, buat data replika awal (Mock Data).
if "kamar_db" not in st.session_state:
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

# Memeriksa apakah log riwayat reservasi sudah ada. Jika belum, buat data simulasi agar dashboard langsung terisi grafik.
if "reservasi_db" not in st.session_state:
    st.session_state.reservasi_db = [
        {
            "id": "INV2026001", "nama": "Andi", "hp": "0812345678", "email": "andi@mail.com", "alamat": "Jakarta",
            "kamar": "102", "tipe": "Standard Room", "bed_type": "Double Bed", "layout_type": "Standard Layout",
            "check_in": "2026-06-01", "check_out": "2026-06-03", "tujuan": "Liburan", "status": "Check-In", 
            "total_biaya": 600000, "status_bayar": "PAID", "metode": "Transfer BCA", 
            "deposit_tipe": "Full Payment", "add_ons": ["Breakfast"]
        },
        {
            "id": "INV2026002", "nama": "Siti Mutia", "hp": "089876543", "email": "siti@mail.com", "alamat": "Bandung",
            "kamar": "103", "tipe": "Deluxe Room", "bed_type": "Twin Bed", "layout_type": "Standard Layout",
            "check_in": "2026-06-10", "check_out": "2026-06-12", "tujuan": "Bisnis", "status": "Booking", 
            "total_biaya": 1150000, "status_bayar": "🟠 Deposit Paid", "metode": "DANA", 
            "deposit_tipe": "Deposit 30%", "add_ons": ["Breakfast", "Airport Pickup"]
        }
    ]

# Memeriksa apakah penyimpanan ulasan hotel sudah ada. Jika belum, buat beberapa contoh ulasan awal.
if "reviews_db" not in st.session_state:
    st.session_state.reviews_db = [
        {"nama": "Andi", "rating": 5, "komentar": "Pelayanan sangat baik, proses check-in lancar!", "tanggal": "2026-06-03"},
        {"nama": "Budi", "rating": 4, "komentar": "Kamar bersih dan dekat pusat kota.", "tanggal": "2026-06-02"}
    ]

# Tabel referensi harga statis untuk menghitung biaya sewa kamar pokok per malam berdasarkan tipenya
TARIF_KAMAR = {
    "Standard Room": 300000,
    "Deluxe Room": 500000,
    "Family Room": 800000,
    "Suite Room": 1200000
}

# ==============================================================================
# 2. SIDEBAR NAVIGASI UTAMA APLIKASI
# ==============================================================================
st.sidebar.markdown("# 🏨 SmartStay Hotel")  # Menampilkan judul utama aplikasi di komponen sidebar sebelah kiri
st.sidebar.caption("Modern Hotel Management System (Session Memory)")  # Sub-judul kecil di bawah judul utama
st.sidebar.markdown("---")  # Membuat garis pembatas horizontal di sidebar

# Membuat menu navigasi radio button untuk mengontrol halaman mana yang aktif di layar utama
menu = st.sidebar.radio("🏠 MENU UTAMA APLIKASI", [
    "Dashboard", "📝 Reservasi Baru", "🏨 Daftar Kamar", "🗺️ Room Map",
    "🔍 Cari Reservasi", "📋 Data Reservasi", "💳 Pembayaran",
    "📜 Riwayat Pembayaran", "👤 Customer VIP", "⭐ Review Hotel", "📊 Analytics Center"
])

# ==============================================================================
# MENU 1: DASHBOARD UTAMA (REAL-TIME METRICS & GRAPHICS)
# ==============================================================================
if menu == "Dashboard":
    st.title("🏠 Dashboard Real-Time")  # Menampilkan judul halaman dashboard utama
    
    # Menghitung metrik ketersediaan kamar secara dinamis dari dictionary 'kamar_db'
    total_kmr = len(st.session_state.kamar_db)  # Total kapasitas seluruh kamar hotel
    terisi = sum(1 for k in st.session_state.kamar_db.values() if k["status"] == "🟥 Terisi")  # Jumlah kamar berstatus terisi
    booking = sum(1 for k in st.session_state.kamar_db.values() if k["status"] == "🟨 Booking")  # Jumlah kamar berstatus di-booking
    kosong = total_kmr - terisi - booking  # Kamar sisa yang masih kosong (tersedia)
    
    # Menghitung agregasi data transaksi keuangan keuangan
    total_rev = len(st.session_state.reservasi_db)  # Total transaksi reservasi yang pernah dibuat
    pendapatan_total = sum(r["total_biaya"] for r in st.session_state.reservasi_db)  # Akumulasi omset kotor pendapatan hotel
    # Menghitung nilai rata-rata rating review (menghindari error pembagian nol jika data kosong)
    avg_rating = sum(rev["rating"] for rev in st.session_state.reviews_db) / len(st.session_state.reviews_db) if st.session_state.reviews_db else 5.0
    
    total_cust = len(set(r["nama"] for r in st.session_state.reservasi_db))  # Menghitung total nama unik pelanggan (Loyalty Check)

    # Membagi area dashboard utama menjadi 4 buah kolom visual metrik ringkasan angka
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Total Kamar", total_kmr)
    col_m1.metric("Kamar Terisi 🟥", terisi)
    col_m2.metric("Kamar Kosong 🟩", kosong)
    col_m2.metric("Total Reservasi", total_rev)
    col_m3.metric("Total Customer (Unik)", total_cust)
    col_m3.metric("Pendapatan Total", f"Rp {int(pendapatan_total):,}")
    col_m4.metric("Rating Hotel", f"⭐ {avg_rating:.1f} / 5.0")
    # Mengalkulasi persentase tingkat keterisian hotel (Occupancy Rate)
    col_m4.metric("Occupancy Rate", f"{(terisi/total_kmr)*100:.1f}%" if total_kmr > 0 else "0%")

    st.markdown("---")
    st.subheader("📊 Analisis Grafik Pendapatan Tipe Kamar")
    
    # Mengonversi list transaksi reservasi ke struktur Pandas DataFrame agar bisa dipetakan ke dalam grafik batang
    df_rev = pd.DataFrame(st.session_state.reservasi_db)
    if not df_rev.empty:
        # Mengelompokkan total omset biaya berdasarkan pengelompokan (grouping) kategori Tipe Kamar
        df_chart = df_rev.groupby('tipe')['total_biaya'].sum()
        st.bar_chart(df_chart)  # Merender chart grafik batang bawaan Streamlit ke layar
    else:
        st.info("Belum ada data transaksi untuk memuat grafik pendapatan.")

# ==============================================================================
# MENU 2: INPUT RESERVASI BARU (AUTOMATED SMART RECOMMENDATION & AUTO ASSIGN)
# ==============================================================================
elif menu == "📝 Reservasi Baru":
    st.title("📝 Input Reservasi Baru")
    
    # Membagi layout: col_form (sisi kiri untuk input manual) & col_recom (sisi kanan untuk deteksi otomatis AI system)
    col_form, col_recom = st.columns([1.5, 1])
    
    with col_form:
        st.subheader("Data Diri Tamu")
        nama = st.text_input("Nama Lengkap")
        hp = st.text_input("Nomor HP")
        email = st.text_input("Email")
        alamat = st.text_area("Alamat")
        
        st.markdown("---")
        st.subheader("Detail Preferensi Kamar")
        col_f1, col_f2 = st.columns(2)  # Membagi sub-form detail preferensi menjadi 2 sub-kolom kecil
        
        with col_f1:
            # INPUT UTAMA PINTAR 1: Dropdown pemilihan tipe kamar dasar oleh resepsionis/user
            pilihan_tipe_kamar = st.selectbox("🏨 Pilih Tipe Kamar", [
                "Standard Room", "Deluxe Room", "Family Room", "Suite Room"
            ])
            # INPUT UTAMA PINTAR 2: Dropdown konfigurasi kasur yang diinginkan tamu
            pilihan_bed = st.selectbox("🛏️ Jenis Tempat Tidur (Bed Type)", [
                "Single Bed", "Double Bed", "Twin Bed"
            ])
            check_in = st.date_input("Tanggal Check In", date.today())  # Input penanggalan check-in (Default: Hari ini)
            
        with col_f2:
            jml_tamu = st.number_input("Jumlah Tamu", min_value=1, max_value=10, value=2)  # Batasi jumlah pengisi kamar
            pilihan_layout = st.selectbox("🚪 Tata Letak Ruangan (Room Layout)", [
                "Standard Layout (Kamar Biasa)", 
                "Connecting Room (Pintu Penghubung Internal)", 
                "Family Room Layout (Spesial Rombongan)"
            ])
            check_out = st.date_input("Tanggal Check Out", date.today() + pd.Timedelta(days=1))  # Default check-out: besok hari
            
        tujuan = st.selectbox("Tujuan Menginap", ["Liburan", "Bisnis", "Honeymoon", "Keluarga", "Staycation"])

    with col_recom:
        st.subheader("🤖 Smart Room Recommendation")
        
        # LOGIKA VALIDASI OTOMATIS: Memeriksa kelayakan kombinasi input secara cerdas (Real-time Filtering)
        valid_rekomendasi = True
        pesan_saran = ""
        
        # Aturan otomatis 1: Memeriksa batas over-capacity untuk kamar standard
        if pilihan_tipe_kamar == "Standard Room" and jml_tamu > 2:
            valid_rekomendasi = False
            pesan_saran = "⚠️ Kapasitas Standard Room maks. 2 orang. Disarankan pindah ke Deluxe/Family."
        # Aturan otomatis 2: Memberi peringatan ketersediaan stok kasur khusus tipe standard
        elif pilihan_tipe_kamar == "Standard Room" and pilihan_bed == "Twin Bed":
            pesan_saran = "💡 Catatan: Ketersediaan Twin Bed untuk tipe Standard sangat terbatas."
        # Aturan otomatis 3: Memberikan saran optimasi keuangan (budget saving) kepada tamu secara otomatis
        elif pilihan_tipe_kamar == "Family Room" and jml_tamu <= 2:
            pesan_saran = "💡 Tips: Kamar ini terlalu besar untuk 2 orang. Anda bisa menghemat dengan memilih Deluxe Room."

        # Menampilkan indikator UI warna hijau jika kombinasi cocok, atau merah/kuning jika ada kendala kecocokan
        if valid_rekomendasi:
            st.success(f"🟩 Pilihan Cocok: **{pilihan_tipe_kamar}** ({pilihan_bed})")
            if pesan_saran: st.info(pesan_saran)
        else:
            st.error(f"❌ Kurang Sesuai: **{pilihan_tipe_kamar}**")
            st.warning(pesan_saran)
        
        st.markdown("---")
        st.subheader("🎲 Auto Room Assignment")
        
        # ALGORITMA ALOKASI KAMAR OTOMATIS: Memindai memori state kamar untuk mencari nomor kamar kosong terdekat yang tipenya sesuai
        kamar_assign = None
        for no_kmr, spek in st.session_state.kamar_db.items():
            # Kamar harus berstatus 'Tersedia' DAN tipenya wajib klop dengan pilihan dropdown kiri pengguna
            if spek["tipe"] == pilihan_tipe_kamar and spek["status"] == "🟩 Tersedia":
                kamar_assign = no_kmr  # Kunci nomor kamar pertama yang lolos seleksi filter
                break  # Hentikan perulangan (loop) pencarian jika sudah berhasil menemukan 1 kamar kosong
                
        # Menampilkan status penugasan kamar otomatis ke layar panel kanan
        if kamar_assign:
            st.info(f"Sistem Mengalokasikan: ✨ **Kamar {kamar_assign}** ✨\n\n*(Status: Kosong & Siap Ditempati)*")
        else:
            # Jika seluruh kamar dengan tipe tersebut penuh, sistem meminta resepsionis mengetik manual kamar cadangan
            st.error(f"Maaf, Semua Kamar tipe **{pilihan_tipe_kamar}** saat ini penuh!")
            kamar_assign = st.text_input("Ketik Manual Nomor Kamar Cadangan:")

        st.markdown("---")
        st.subheader("🎁 Additional Services (Add-Ons)")
        # Menyediakan fitur tambahan layanan hotel (Add-ons) yang nilainya dinamis berupa list checkbox
        addons_pilihan = []
        if st.checkbox("🍳 Breakfast Tambahan (Rp 50.000)"): addons_pilihan.append("Breakfast")
        if st.checkbox("🛏️ Extra Bed (Rp 100.000)"): addons_pilihan.append("Extra Bed")
        if st.checkbox("🚗 Airport Pickup (Rp 150.000)"): addons_pilihan.append("Airport Pickup")
        if st.checkbox("🧺 Laundry Service (Rp 75.000)"): addons_pilihan.append("Laundry")
        if st.checkbox("🎮 Gaming Package PS5 (Rp 100.000)"): addons_pilihan.append("Gaming Package")

    st.markdown("---")
    # Tombol eksekusi utama penguncian form reservasi baru sebelum masuk ke billing area
    if st.button("Lanjutkan ke Pembayaran ➡️", type="primary"):
        if not nama or not kamar_assign:
            st.error("Nama Tamu dan Alokasi Nomor Kamar wajib tersedia sebelum checkout!")
        else:
            # Mengunci seluruh variabel form input ke session_state penampung sementara bernama 'proses_checkout'
            st.session_state.proses_checkout = {
                "nama": nama, "hp": hp, "email": email, "alamat": alamat,
                "kamar": kamar_assign, "tipe": pilihan_tipe_kamar,
                "bed_type": pilihan_bed, "layout_type": pilihan_layout,
                "check_in": str(check_in), "check_out": str(check_out),
                "tujuan": tujuan, "add_ons": addons_pilihan
            }
            # Memberikan instruksi kepada user untuk membuka menu Pembayaran
            st.success(f"Data Kamar {kamar_assign} Berhasil Dikunci! Silakan buka menu '💳 Pembayaran'.")

# ==============================================================================
# MENU 3: DAFTAR KAMAR (KLASIFIKASI KATEGORI RESMI HOTEL)
# ==============================================================================
elif menu == "🏨 Daftar Kamar":
    st.title("🏨 Klasifikasi & Spesifikasi Kamar")
    st.markdown("---")
    # Membuat komponen tab navigasi horizontal untuk memisahkan katalog informasi agar rapi (scannable)
    tab1, tab2, tab3 = st.tabs(["✨ Berdasarkan Fasilitas & Ukuran", "🛏️ Berdasarkan Jenis Tempat Tidur", "🚪 Berdasarkan Tata Letak Ruangan"])
    
    with tab1:
        st.subheader("Kategori Kamar Sesuai Fasilitas & Dimensi")
        # Menggunakan komponen expander agar deskripsi detail bisa disembunyikan/ditampilkan secara fleksibel
        with st.expander("🔹 Standard Room (Rp 300.000 / Malam)"):
            st.markdown("* **Deskripsi:** Kelas kamar paling dasar dengan fasilitas esensial seperti tempat tidur, AC, TV, dan kamar mandi.")
        with st.expander("🔹 Deluxe Room (Rp 500.000 / Malam)"):
            st.markdown("* **Deskripsi:** Kamar yang berukuran lebih luas dengan desain elegan dan fasilitas lebih lengkap.")
        with st.expander("🔹 Suite Room (Rp 1.200.000 / Malam)"):
            st.markdown("* **Deskripsi:** Kategori mewah di mana kamar tidur terpisah secara fisik dari ruang tamu.")
    with tab2:
        st.subheader("Pilihan Konfigurasi Tempat Tidur (Bed)")
        col_b1, col_b2, col_b3 = st.columns(3)  # Memecah visual menjadi 3 box informasi sejajar
        col_b1.info("### 🧍 Single Bed\nSatu tempat tidur ukuran single.")
        col_b2.info("### 👥 Double Bed\nSatu tempat tidur berukuran besar untuk dua orang.")
        col_b3.info("### 👥 Twin Bed\nDua tempat tidur single terpisah.")
    with tab3:
        st.subheader("Arsitektur & Tata Letak Interior Kamar")
        col_t1, col_t2 = st.columns(2)
        col_t1.success("### 🚪 Connecting Room\nDua kamar terpisah yang memiliki pintu penghubung di bagian dalam.")
        col_t2.success("### 👨‍👩‍👧 Family Room (Rp 800.000 / Malam)\nKamar berukuran besar dirancang khusus rombongan keluarga.")

# ==============================================================================
# MENU 4: ROOM MAP (PETA VISUAL STATUS DIGITAL REAL-TIME)
# ==============================================================================
elif menu == "🗺️ Room Map":
    st.title("🗺️ Visual Room Map Status")
    cols = st.columns(4)  # Menyusun grid denah peta kamar menjadi formasi 4 kolom kesamping
    # Melakukan perulangan untuk mengambil nomor kamar dan datanya dari session state
    for idx, (no_kmr, data) in enumerate(st.session_state.kamar_db.items()):
        with cols[idx % 4]:  # Mendistribusikan penempatan kartu kamar secara merata di dalam grid 4 kolom
            # Memberikan warna box dinamis: Hijau (Tersedia), Merah (Terisi), Kuning (Sudah dibooking)
            if "Tersedia" in data["status"]:
                st.success(f"### {no_kmr}\n🟢 Available\n\n*{data['tipe']}*")
            elif "Terisi" in data["status"]:
                st.error(f"### {no_kmr}\n🟥 Occupied\n\n*{data['tipe']}*")
            else:
                st.warning(f"### {no_kmr}\n🟨 Booked\n\n*{data['tipe']}*")

# ==============================================================================
# MENU 5: CARI DATA RESERVASI TAMU (REAL-TIME ENGINE SEARCH)
# ==============================================================================
elif menu == "🔍 Cari Reservasi":
    st.title("🔍 Cari Data Reservasi Aktif")
    # Membuat filter penentu metode pencarian berdasarkan 3 kategori berbeda melalui radio button
    kategori_cari = st.radio("Cari Berdasarkan:", ["Nama", "Nomor Kamar", "Nomor HP"], horizontal=True)
    kunci_keyword = st.text_input("Ketik Kata Kunci Pencarian:")  # Kolom isian teks keyword pencarian
    
    if kunci_keyword:
        hasil_cari = []  # List kosong untuk mengumpulkan records data yang cocok dengan kriteria filter
        for r in st.session_state.reservasi_db:
            # Memeriksa kecocokan teks keyword (diubah ke lowercase agar pencarian bersifat case-insensitive)
            if kategori_cari == "Nama" and kunci_keyword.lower() in r["nama"].lower():
                hasil_cari.append(r)
            elif kategori_cari == "Nomor Kamar" and kunci_keyword == r["kamar"]:
                hasil_cari.append(r)
            elif kategori_cari == "Nomor HP" and kunci_keyword in r["hp"]:
                hasil_cari.append(r)
                
        # Jika data hasil pencarian ditemukan, render datanya ke dalam bentuk tabel representatif
        if hasil_cari:
            st.success(f"Ditemukan {len(hasil_cari)} Data!")
            st.table(pd.DataFrame(hasil_cari)[["id", "nama", "kamar", "tipe", "check_in", "check_out", "status"]])
        else:
            st.warning("Data tidak ditemukan.")

# ==============================================================================
# MENU 6: DATA RESERVASI LOG (CRUD ENGINE MURNI MEMORI - TANPA SQL/JSON FILE)
# ==============================================================================
elif menu == "📋 Data Reservasi":
    st.title("📋 Master Log Data Reservasi (CRUD Runtime)")
    
    # Memastikan tabel master log hanya dirender jika list data reservasi di memori memiliki isi
    if st.session_state.reservasi_db:
        df_master = pd.DataFrame(st.session_state.reservasi_db)
        # Menampilkan representasi seluruh data transaksi hotel dalam bentuk tabel grid interaktif (bisa di-sort)
        st.dataframe(df_master[["id", "nama", "kamar", "tipe", "bed_type", "layout_type", "check_in", "status"]], use_container_width=True)
        
        st.markdown("---")
        st.subheader("🛠️ Aksi Resepsionis")
        list_id = df_master["id"].tolist()  # Membaca seluruh deretan ID Invoice unik untuk opsi dropdown penargetan aksi CRUD
        pilih_id = st.selectbox("Pilih ID Transaksi target:", list_id)
        # Mencari urutan indeks keberadaan baris data di dalam list asli berdasarkan ID yang dipilih di dropdown
        idx_target = next((i for i, item in enumerate(st.session_state.reservasi_db) if item["id"] == pilih_id), None)
        
        if idx_target is not None:
            c1, c2, c3 = st.columns(3)  # Membagi tombol aksi operasional manajemen status menjadi 3 kolom terpisah
            
            # A. OPERASI UPDATE STATUS: TAMU DATANG & CHECK-IN (MERUBAH LOG RESERVASI & MASTER STATUS KAMAR DI RAM)
            if c1.button("Set Status: CHECK-IN 🟥"):
                st.session_state.reservasi_db[idx_target]["status"] = "Check-In"  # Update status di transaksi log
                kmr = st.session_state.reservasi_db[idx_target]["kamar"]
                st.session_state.kamar_db[kmr]["status"] = "🟥 Terisi"  # Mengubah status master kamar fisik hotel menjadi Terisi
                st.success("Tamu Berhasil Check-In!")
                st.rerun()  # Memaksa Streamlit merender ulang halaman agar indikator warna terbaru langsung muncul
                
            # B. OPERASI UPDATE STATUS: TAMU PULANG & CHECK-OUT (MENGOSONGKAN KAMAR KEMBALI SECARA OTOMATIS)
            if c2.button("Set Status: CHECK-OUT 🟩"):
                st.session_state.reservasi_db[idx_target]["status"] = "Check-Out"  # Update status di transaksi log
                kmr = st.session_state.reservasi_db[idx_target]["kamar"]
                st.session_state.kamar_db[kmr]["status"] = "🟩 Tersedia"  # Mengembalikan status master kamar fisik hotel jadi Kosong
                st.success("Tamu Berhasil Check-Out! Kamar dikosongkan.")
                st.rerun()  # Refresh halaman web
                
            # C. OPERASI DELETE: MENGHAPUS REKORD BUKTI TRANSAKSI DARI LOG MEMORI RUNTIME APLIKASI
            if c3.button("Hapus Bukti Transaksi ❌"):
                st.session_state.reservasi_db.pop(idx_target)  # Mengeluarkan data dictionary dari list array berdasarkan indeks target
                st.error("Data transaksi berhasil dihapus.")
                st.rerun()  # Refresh halaman web
    else:
        st.warning("Data transaksi kosong.")

# ==============================================================================
# MENU 7: BILLING AREA & PEMBAYARAN (AUTOMATED INVOICE CALCULATION ENGINE)
# ==============================================================================
elif menu == "💳 Pembayaran":
    st.title("💳 Payment Management System")
    
    # Memeriksa proteksi pengisian data; jika user lompat langsung ke menu bayar tanpa isi form, kunci akses halaman ini
    if "proses_checkout" not in st.session_state:
        st.info("Silakan isi formulir pemesanan terlebih dahulu di Menu '📝 Reservasi Baru'.")
    else:
        ck = st.session_state.proses_checkout  # Membuat alias variabel penyingkat data checkout sementara
        
        # LOGIKA MATEMATIS KALKULASI DURASI MENGINAP (Mengonversi string tanggal ke objek waktu nyata)
        d1 = datetime.strptime(ck["check_in"], "%Y-%m-%d")
        d2 = datetime.strptime(ck["check_out"], "%Y-%m-%d")
        durasi = max(1, (d2 - d1).days)  # Menghitung selisih hari menginap (minimal dihitung 1 malam)
        
        tarif_per_malam = TARIF_KAMAR.get(ck["tipe"], 300000)  # Mengambil tarif pokok per malam berdasarkan tipe kamar
        biaya_kamar = tarif_per_malam * durasi  # Total nominal murni biaya kamar pokok
        
        # LOGIKA ITERASI PENGHITUNGAN BIAYA TAMBAHAN LAYANAN (ADD-ONS)
        biaya_addons = 0
        mapping_addon_harga = {"Breakfast": 50000, "Extra Bed": 100000, "Airport Pickup": 150000, "Laundry": 75000, "Gaming Package": 100000}
        for item in ck["add_ons"]:
            biaya_addons += mapping_addon_harga.get(item, 0)  # Menambahkan akumulasi harga item layanan yang dicentang user
            
        subtotal = biaya_kamar + biaya_addons  # Kalkulasi nilai kotor subtotal gabungan
        
        # FITUR MARKETING VOUCHER DISKON OTOMATIS
        voucher_input = st.text_input("Masukkan Kode Voucher (Opsional):")
        diskon_voucher = 0
        if voucher_input.strip() == "SMART10": 
            diskon_voucher = 0.10 * subtotal  # Jika mengetik kode SMART10, otomatis pangkas harga sebesar 10%
            
        ppn = 0.11 * (subtotal - diskon_voucher)  # Menghitung tarif pajak pertambahan nilai (PPN resmi sebesar 11%)
        total_akhir = (subtotal - diskon_voucher) + ppn  # Menghitung hasil rumus nominal final total tagihan bersih akhir
        
        # Pemilihan opsi skema cicilan/pembayaran dan jenis platform transaksi keuangan hotel
        pilihan_skema = st.radio("Skema Pembayaran:", ["Full Payment (Bayar 100%)", "Deposit 30%"])
        metode_pilih = st.selectbox("Metode Pembayaran:", ["Transfer BCA", "Transfer Mandiri", "E-Wallet DANA"])
        
        st.markdown("### 📋 Payment Summary")
        # Menyusun struktur layout teks struk nota kuitansi (E-Receipt) digital siap print out
        summary_text = f"""
================================================
                PAYMENT SUMMARY                 
================================================
Tipe Kamar                      : {ck['tipe']}
Jenis Kasur (Bed Type)          : {ck['bed_type']}
Tata Letak (Layout)             : {ck['layout_type']}
Durasi Menginap                 : {durasi} Malam
------------------------------------------------
Biaya Kamar Pokok               : Rp {biaya_kamar:,}
Total Layanan Tambahan (Add-On) : Rp {biaya_addons:,}
Subtotal                        : Rp {subtotal:,}
Diskon Voucher                  : Rp {diskon_voucher:,}
PPN 11%                         : Rp {ppn:,}
------------------------------------------------
TOTAL TAGIHAN                   : Rp {total_akhir:,}
================================================
        """
        st.code(summary_text, language="text")  # Menampilkan nota dengan format font monospaced code yang rapi scannable
        
        # Mengecek apakah tamu memilih sistem cicilan DP deposit awal saja
        if pilihan_skema == "Deposit 30%":
            nilai_depo = total_akhir * 0.3  # Menghitung tagihan wajib uang muka nominal 30% dari total invoice bersih
            st.warning(f"Wajib Bayar Deposit (30%): Rp {nilai_depo:,}")
            status_bayar_tag = "🟠 Deposit Paid"
        else:
            status_bayar_tag = "PAID"
            
        # PROSES CRITICAL INSERT DATA: Menyisipkan data pesanan baru dari ram temporary ke dalam list log history utama di state RAM
        if st.button("Finalisasi Transaksi & Terbitkan Invoice 🚀", type="primary"):
            new_inv_id = f"INV2026{len(st.session_state.reservasi_db) + 1:03d}"  # Auto-generate nomor invoice urut berkode tahun
            
            # Melakukan pemanggilan fungsi append untuk menyisipkan bundle dictionary baru ke database reservasi ram utama
            st.session_state.reservasi_db.append({
                "id": new_inv_id, "nama": ck["nama"], "hp": ck["hp"], "email": ck["email"], "alamat": ck["alamat"],
                "kamar": ck["kamar"], "tipe": ck["tipe"], "bed_type": ck["bed_type"], "layout_type": ck["layout_type"],
                "check_in": ck["check_in"], "check_out": ck["check_out"], "tujuan": ck["tujuan"], "status": "Booking", 
                "total_biaya": total_akhir, "status_bayar": status_bayar_tag, "metode": metode_pilih, 
                "deposit_tipe": pilihan_skema, "add_ons": ck["add_ons"]
            })
            
            # Otomatis mengunci status kamar master teralokasi dari status awal 'Hijau Tersedia' berubah menguning menjadi '🟨 Booking'
            st.session_state.kamar_db[ck["kamar"]]["status"] = "🟨 Booking"
            
            del st.session_state.proses_checkout  # Menghapus berkas sampah temporary checkout agar state bersih kembali
            st.success(f"Invoice {new_inv_id} sukses ditambahkan!")  # Pengumuman sukses penerbitan nota transaksi baru
            st.rerun()  # Refresh halaman web aplikasi

# ==============================================================================
# MENU 8: RIWAYAT PEMBAYARAN KASIR (AUDIT LOG TABULAR DATA REVENUE)
# ==============================================================================
elif menu == "📜 Riwayat Pembayaran":
    st.title("📜 Auto Invoice & E-Receipt Center")
    # Memeriksa data historis pembayaran log transaksi
    if st.session_state.reservasi_db:
        df_pay = pd.DataFrame(st.session_state.reservasi_db)
        # Menampilkan tabel khusus rangkuman pembayaran untuk kebutuhan peninjauan arus kas oleh finance/kasir hotel
        st.table(df_pay[["id", "nama", "metode", "status_bayar", "total_biaya"]])
    else: 
        st.warning("Belum ada riwayat pembayaran.")

# ==============================================================================
# MENU 9: CUSTOMER VIP LEADERBOARD (BUSINESS LOYALTY AGGREGATION ENGINE)
# ==============================================================================
elif menu == "👤 Customer VIP":
    st.title("👤 Customer VIP Leaderboard")
    if st.session_state.reservasi_db:
        df_res = pd.DataFrame(st.session_state.reservasi_db)
        # MATEMATIKA AGREGASI: Menghitung kemunculan (frekuensi) pemesanan yang dilakukan oleh nama customer yang sama
        df_vip = df_res.groupby('nama').size().reset_index(name='kunjungan')
        df_vip = df_vip.sort_values(by="kunjungan", ascending=False)  # Mengurutkan daftar nama dari pengunjung paling sering (loyal)
        
        # Fungsi penentu tingkatan tingkatan member kustomer loyalitas bisnis hotel secara otomatis
        def tentukan_level(k):
            if k >= 5: return "Gold/VIP"  # Berkunjung 5 kali atau lebih naik kasta menjadi VIP member
            if k >= 3: return "Silver"    # Berkunjung 3-4 kali berstatus silver tier
            return "Regular"              # Di bawah itu berstatus member reguler biasa
            
        df_vip['level'] = df_vip['kunjungan'].apply(tentukan_level)  # Menerapkan rumus klasifikasi otomatis ke kolom baru dataframe
        st.table(df_vip)  # Cetak visual tabel loyalitas kustomer
    else:
        st.info("Belum ada riwayat customer.")

# ==============================================================================
# MENU 10: ULASAN REVIEW & FEEDBACK USER INTERACTION SYSTEM
# ==============================================================================
elif menu == "⭐ Review Hotel":
    st.title("⭐ Review & Rating Kepuasan")
    # Membuka penampung komponen UI interaktif berbasis form
    with st.form("Form_Review"):
        r_nama = st.text_input("Nama Anda:")
        r_star = st.slider("Beri Bintang:", 1, 5, 5)  # Komponen slider geser interaktif untuk penentuan skala skor bintang 1 s.d 5
        r_msg = st.text_area("Tulis Komentar:")
        # Tombol khusus untuk men-submit isian form ulasan kepuasan tamu hotel
        if st.form_submit_button("Kirim Ulasan"):
            if r_nama and r_msg:
                # Memasukkan objek data ulasan teranyar ke list array review_db di memori session_state
                st.session_state.reviews_db.append({"nama": r_nama, "rating": r_star, "komentar": r_msg, "tanggal": str(date.today())})
                st.success("Review berhasil ditulis!"); st.rerun()  # Refresh halaman agar review teranyar langsung dirender di bawah
                
    st.markdown("---")
    # Melakukan teknik iterasi looping terbalik (reversed) agar ulasan paling baru dikirim posisinya bertengger paling atas
    for row in reversed(st.session_state.reviews_db):
        st.markdown(f"**{row['nama']}** — {'⭐' * row['rating']} ({row['tanggal']})")  # Teknik multiplikasi string untuk merender visual ikon bintang emas
        st.caption(f"\"{row['komentar']}\"")  # Mencetak teks ulasan kritik dan saran dalam format teks miring berukuran kecil

# ==============================================================================
# MENU 11: ANALYTICS CENTER & ESTIMATED FORECASTING MARKETING ENGINE
# ==============================================================================
elif menu == "📊 Analytics Center":
    st.title("📊 Analytics Center & Prediksi Omset")
    if st.session_state.reservasi_db:
        total_omset = sum(r["total_biaya"] for r in st.session_state.reservasi_db)  # Menghitung omset nyata saat ini
        st.metric("Total Pendapatan Saat Ini", f"Rp {total_omset:,.0f}")
        # PREDIKSI BISNIS (FORECASTING SIMULATION): Menghitung asumsi potensi kenaikan omset bulan depan sebesar 25% (Faktor kelipatan multiplier 1.25)
        st.metric("🔮 Prediksi Pendapatan Bulan Depan", f"Rp {total_omset * 1.25:,.0f}")
    else: 
        st.warning("Data transaksi belum cukup untuk melakukan analisis.")
