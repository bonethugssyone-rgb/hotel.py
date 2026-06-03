import streamlit as st
import pandas as pd
from datetime import datetime, date
import random

# ==========================================
# 1. KONFIGURASI ENGINE & DATA UTAMA (TRAVELOKA STYLE)
# ==========================================
st.set_page_config(page_title="Traveloka Smart Hotel Engine", layout="wide", page_icon="✈️")

# Inisialisasi Master Kamar dan Fasilitas (Dinamis)
if 'kamar_db' not in st.session_state:
    st.session_state.kamar_db = {
        "101": {"tipe": "Standard", "harga": 300000, "fasilitas": "Free Wi-Fi, AC", "bintang": 3.8},
        "102": {"tipe": "Standard", "harga": 320000, "fasilitas": "Free Wi-Fi, AC, TV", "bintang": 4.0},
        "201": {"tipe": "Deluxe", "harga": 550000, "fasilitas": "Free Wi-Fi, AC, Bathtub, Breakfast", "bintang": 4.5},
        "202": {"tipe": "Deluxe", "harga": 580000, "fasilitas": "Free Wi-Fi, AC, Minibar, Breakfast", "bintang": 4.6},
        "301": {"tipe": "Suite", "harga": 900000, "fasilitas": "King Bed, Smart TV, Jacuzzi, All-Inclusive", "bintang": 4.9},
        "302": {"tipe": "Suite", "harga": 1250000, "fasilitas": "Private Lounge, Balcony, Jacuzzi, All-Inclusive", "bintang": 5.0},
    }

# Inisialisasi Database Transaksi Reservasi
if 'reservasi_db' not in st.session_state:
    st.session_state.reservasi_db = [
        {
            "booking_id": "TVL-8837109",
            "nama_tamu": "Andi Wijaya",
            "no_kamar": "201",
            "tipe": "Deluxe",
            "check_in": "2026-06-01",
            "check_out": "2026-06-03",
            "metode_bayar": "Traveloka PayLater",
            "status_bayar": "SETTLED",
            "total_biaya": 1100000
        },
        {
            "booking_id": "TVL-1029482",
            "nama_tamu": "Siti Mutia",
            "no_kamar": "101",
            "tipe": "Standard",
            "check_in": "2026-06-10",
            "check_out": "2026-06-12",
            "metode_bayar": "Bank Transfer (Mandiri)",
            "status_bayar": "SETTLED",
            "total_biaya": 600000
        }
    ]

# Inisialisasi Review Pengguna
if 'reviews' not in st.session_state:
    st.session_state.reviews = [
        {"User": "Andi W.", "Rating": 5, "Komentar": "Proses check-in cepat via aplikasi, kamar Deluxe sangat bersih!"},
        {"User": "Budi S.", "Rating": 4, "Komentar": "Kamar Standard worth it banget untuk harga segini."}
    ]

# Autentikasi Staf Akun
if 'staf_login' not in st.session_state:
    st.session_state.staf_login = {"is_in": False, "user": ""}

# ==========================================
# 2. LOGIKA VALIDASI TANGGAL (ANTI DOUBLE-BOOKING REAL TIME)
# ==========================================
def cek_kamar_tersedia(no_kamar, target_in, target_out):
    """Memeriksa apakah nomor kamar bentrok dengan jadwal reservasi yang sudah ada"""
    t_in = datetime.strptime(str(target_in), "%Y-%m-%d").date()
    t_out = datetime.strptime(str(target_out), "%Y-%m-%d").date()
    
    for res in st.session_state.reservasi_db:
        if res['no_kamar'] == no_kamar:
            res_in = datetime.strptime(res['check_in'], "%Y-%m-%d").date()
            res_out = datetime.strptime(res['check_out'], "%Y-%m-%d").date()
            
            # Rumus Logika Aljabar Interval Bentrok Tanggal
            if not (t_out <= res_in or t_in >= res_out):
                return False
    return True

# ==========================================
# 3. SIDEBAR NAVIGATION & LOGIN PORTAL
# ==========================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/a/a7/Traveloka_Logo.png", width=180)
st.sidebar.markdown("### ✈️ Core Hotel Dashboard")

if st.sidebar.checkbox("🔓 Mode Hak Akses Staf Internal"):
    if not st.session_state.staf_login["is_in"]:
        with st.sidebar.form("Login Staf"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Masuk Sistem Back-Office"):
                if u == "admin" and p == "admin123":
                    st.session_state.staf_login["is_in"] = True
                    st.session_state.staf_login["user"] = u
                    st.rerun()
                else:
                    st.sidebar.error("Akses ditolak.")
    else:
        st.sidebar.success(f"Masuk sebagai: {st.session_state.staf_login['user'].upper()}")
        if st.sidebar.button("🚪 Keluar Mode Staf"):
            st.session_state.staf_login["is_in"] = False
            st.rerun()

# Menu Navigasi Sesuai Alur Dinamis Traveloka
menu = st.sidebar.radio("Pilih Layanan:", [
    "🏨 Cari & Pesan Kamar (User Interface)",
    "🧾 Riwayat Pemesanan & E-Voucher",
    "📊 Konsol Kontrol Internal (Khusus Staf)",
    "⭐ Ulasan & Rating Kepuasan"
])

# ==========================================
# FITUR A: CARI & PESAN KAMAR (USER FILTERS)
# ==========================================
if menu == "🏨 Cari & Pesan Kamar (User Interface)":
    st.title("🛏️ Booking Hotel Kamar Pilihan Anda")
    st.caption("Gunakan filter dinamis untuk menemukan kamar terbaik layaknya di sistem Traveloka.")
    
    # Komponen Form Pencarian Traveloka
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        date_in = st.date_input("Tanggal Check-In", date.today())
    with col_s2:
        date_out = st.date_input("Tanggal Check-Out", date.today() + pd.Timedelta(days=1))
    with col_s3:
        max_budget = st.slider("Budget Maksimum per Malam (Rp)", 200000, 2000000, 1500000, step=50000)
        
    durasi = (date_out - date_in).days
    if durasi <= 0:
        st.error("Format tanggal keliru. Tanggal check-out harus setelah check-in.")
        st.stop()

    st.markdown("---")
    st.subheader("💡 Hasil Pencarian Kamar Tersedia")
    
    # Algoritma Filter Dinamis
    for no_kmr, spek in st.session_state.kamar_db.items():
        if spek['harga'] <= max_budget:
            is_ready = cek_kamar_tersedia(no_kmr, date_in, date_out)
            
            # Tampilan Antarmuka Berbentuk Card Box ala Traveloka
            with st.container():
                col_c1, col_c2, col_c3 = st.columns([2, 3, 2])
                with col_c1:
                    st.markdown(f"### Kamar {no_kmr} ({spek['tipe']})")
                    st.markdown(f"⭐ **{spek['bintang']} / 5.0** Excellent")
                with col_c2:
                    st.markdown(f"**Fasilitas:** *{spek['fasilitas']}*")
                    if is_ready:
                        st.markdown("🟢 <font color='green'><b>Tersedia untuk tanggal pilihan Anda</b></font>", unsafe_allow_html=True)
                    else:
                        st.markdown("🔴 <font color='red'><b>Sudah dipesan orang lain pada tanggal ini</b></font>", unsafe_allow_html=True)
                with col_c3:
                    st.markdown(f"### Rp {spek['harga']:,} <font size='2' color='gray'>/ malam</font>", unsafe_allow_html=True)
                    total_pembayaran = spek['harga'] * durasi
                    st.caption(f"Total Biaya ({durasi} Malam): Rp {total_pembayaran:,}")
                    
                    # Logika Pemesanan Langsung
                    if is_ready:
                        if st.button(f"Pesan Kamar {no_kmr}", key=f"btn_{no_kmr}"):
                            st.session_state.booking_proses = {
                                "no_kamar": no_kmr,
                                "tipe": spek['tipe'],
                                "total_biaya": total_pembayaran,
                                "in": str(date_in),
                                "out": str(date_out)
                            }
                            st.success(f"Kamar {no_kmr} masuk keranjang! Silakan selesaikan data pemesan di bawah.")
                st.markdown("<hr style='border-top: 1px dashed #bbb;'>", unsafe_allow_html=True)

    # Form Konfirmasi Pengisian Data Pemesan (Terbuka dinamis)
    if 'booking_proses' in st.session_state:
        st.markdown("### 📝 Pengisian Data Penumpang / Tamu")
        with st.form("Form_Checkout"):
            b_data = st.session_state.booking_proses
            st.info(f"Mengonfirmasi Pemesanan: Kamar {b_data['no_kamar']} ({b_data['tipe']}) untuk {durasi} Malam")
            
            nama_input = st.text_input("Nama Lengkap Tamu (Sesuai KTP/Paspor)")
            telp_input = st.text_input("Nomor Handphone Aktif")
            opsi_bayar = st.selectbox("Pilih Metode Pembayaran:", ["Traveloka PayLater", "Kredit Card Visa/Master", "Bank Transfer (BCA/Mandiri)", "QRIS Dana/Gopay"])
            
            if st.form_submit_button("Bayar & Terbitkan E-Voucher"):
                if not nama_input or not telp_input:
                    st.error("Data kontak tidak boleh kosong!")
                else:
                    # Input Data Baru Ke Database Array Utama
                    new_id = f"TVL-{random.randint(1000000, 9999999)}"
                    transaksi_sukses = {
                        "booking_id": new_id,
                        "nama_tamu": nama_input,
                        "no_kamar": b_data['no_kamar'],
                        "tipe": b_data['tipe'],
                        "check_in": b_data['in'],
                        "check_out": b_data['out'],
                        "metode_bayar": opsi_bayar,
                        "status_bayar": "SETTLED",
                        "total_biaya": b_data['total_biaya']
                    }
                    st.session_state.reservasi_db.append(transaksi_sukses)
                    st.session_state.terakhir_dipesan = new_id
                    del st.session_state.booking_proses
                    st.success("🎉 Pembayaran Berhasil! E-Voucher Anda telah terbit.")
                    st.balloons()


# ==========================================
# FITUR B: RIWAYAT PEMESANAN & E-VOUCHER
# ==========================================
elif menu == "🧾 Riwayat Pemesanan & E-Voucher":
    st.title("🧾 Digital E-Voucher & Riwayat Transaksi")
    st.caption("Gunakan pencarian ID Booking Traveloka Anda untuk memunculkan tiket digital.")
    
    search_id = st.text_input("Masukkan ID Booking Anda (Contoh: TVL-8837109 atau lihat tabel di bawah):")
    
    # Tampilkan Seluruh Riwayat Terlebih Dahulu (Traversal Data Array)
    df_res = pd.DataFrame(st.session_state.reservasi_db)
    st.dataframe(df_res, use_container_width=True)
    
    # Desain Card E-Voucher Khas Traveloka jika ID Cocok
    if search_id:
        target_voucher = next((item for item in st.session_state.reservasi_db if item["booking_id"] == search_id.strip()), None)
        
        if target_voucher:
            st.markdown("---")
            st.subheader("✈️ Traveloka Hotel E-Voucher")
            
            # CSS Box Container Biru khas Traveloka
            st.markdown(f"""
            <div style="background-color: #0194f3; padding: 25px; border-radius: 12px; color: white; font-family: sans-serif;">
                <div style="display: flex; justify-content: space-between;">
                    <h2><b>HOTEL VOUCHER</b></h2>
                    <h3>ID: {target_voucher['booking_id']}</h3>
                </div>
                <hr style="border-color: white;">
                <p style="font-size: 18px; margin-bottom: 5px;">Nama Tamu Utama: <b>{target_voucher['nama_tamu']}</b></p>
                <div style="display: flex; gap: 50px; margin-top: 15px;">
                    <div>
                        <p style="margin: 0; color: #d0e7ff;">NOMOR KAMAR</p>
                        <p style="font-size: 22px; font-weight: bold; margin: 0;">{target_voucher['no_kamar']} ({target_voucher['tipe']})</p>
                    </div>
                    <div>
                        <p style="margin: 0; color: #d0e7ff;">CHECK-IN</p>
                        <p style="font-size: 18px; font-weight: bold; margin: 0;">{target_voucher['check_in']}</p>
                    </div>
                    <div>
                        <p style="margin: 0; color: #d0e7ff;">CHECK-OUT</p>
                        <p style="font-size: 18px; font-weight: bold; margin: 0;">{target_voucher['check_out']}</p>
                    </div>
                </div>
                <hr style="border-color: white; margin-top: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <p style="margin:0;">Status Transaksi: <b>🟢 PAID via {target_voucher['metode_bayar']}</b></p>
                    <p style="font-size: 20px; font-weight: bold; margin:0;">Total: Rp {target_voucher['total_biaya']:,}</p>
                </div>
                <div style="background-color: white; color: black; text-align: center; margin-top: 15px; padding: 5px; letter-spacing: 8px; font-weight: bold;">
                    ||||| BARCODE-{target_voucher['booking_id']} |||||
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("ID Booking tidak ditemukan dalam database.")


# ==========================================
# FITUR C: KONSOL KONTROL INTERNAL (BACK-OFFICE STAF)
# ==========================================
elif menu == "📊 Konsol Kontrol Internal (Khusus Staf)":
    st.title("📊 Back-Office Management Console")
    
    if not st.session_state.staf_login["is_in"]:
        st.warning("⚠️ Fitur ini dikunci. Silakan centang 'Mode Hak Akses Staf Internal' di menu sidebar kiri untuk login.")
        st.stop()
        
    # Perhitungan Metrik Keuangan Hotel Dinamis
    total_omset = sum(item['total_biaya'] for item in st.session_state.reservasi_db)
    total_pemesanan = len(st.session_state.reservasi_db)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Omset Bruto (Pendapatan)", f"Rp {total_omset:,}")
    m2.metric("Total Sukses Reservasi", f"{total_pemesanan} Transaksi")
    m3.metric("Jumlah Kamar Dikelola", f"{len(st.session_state.kamar_db)} Unit")
    
    st.markdown("---")
    
    # Operasi CRUD: Update & Delete Data
    st.subheader("✏️ Manipulasi Data Operasional (Update / Delete Array)")
    
    if st.session_state.reservasi_db:
        list_opsi = [f"{idx} | {res['booking_id']} - {res['nama_tamu']}" for idx, res in enumerate(st.session_state.reservasi_db)]
        pilihan = st.selectbox("Pilih Baris Data Transaksi Terdaftar:", list_opsi)
        
        target_index = int(pilihan.split(" | ")[0])
        data_lama = st.session_state.reservasi_db[target_index]
        
        col_ed1, col_ed2 = st.columns(2)
        with col_ed1:
            nama_baru = st.text_input("Ubah Nama Tamu:", value=data_lama['nama_tamu'])
            kamar_baru = st.text_input("Ubah Nomor Kamar:", value=data_lama['no_kamar'])
        with col_ed2:
            in_baru = st.text_input("Ubah Tanggal Masuk (YYYY-MM-DD):", value=data_lama['check_in'])
            out_baru = st.text_input("Ubah Tanggal Keluar (YYYY-MM-DD):", value=data_lama['check_out'])
            
        col_btn1, col_btn2, _ = st.columns([1, 1, 2])
        with col_btn1:
            if st.button("Simpan Perubahan (Update)", type="primary"):
                st.session_state.reservasi_db[target_index]['nama_tamu'] = nama_baru
                st.session_state.reservasi_db[target_index]['no_kamar'] = kamar_baru
                st.session_state.reservasi_db[target_index]['check_in'] = in_baru
                st.session_state.reservasi_db[target_index]['check_out'] = out_baru
                st.success("Data berhasil diperbarui!")
                st.rerun()
                
        with col_btn2:
            if st.button("Hapus Transaksi (Cancel Booking)", type="secondary"):
                st.session_state.reservasi_db.pop(target_index)
                st.warning("Data transaksi berhasil didelete dari sistem.")
                st.rerun()


# ==========================================
# FITUR D: REVIEW & RATING KEPUASAN (USER REVIEWS)
# ==========================================
elif menu == "⭐ Ulasan & Rating Kepuasan":
    st.title("⭐ Ulasan Pelanggan Traveloka")
    
    # Hitung rata-rata rating
    df_rev = pd.DataFrame(st.session_state.reviews)
    avg_rating = df_rev['Rating'].mean()
    
    st.metric("Rerata Skor Kepuasan Akomodasi Hotel", f"📊 {avg_rating:.1f} / 5.0")
    
    # Tampilkan Ulasan Komentar
    for _, row in df_rev.iterrows():
        st.markdown(f"**{row['User']}** memberikan rating {'⭐' * row['Rating']}")
        st.caption(f"\"{row['Komentar']}\"")
        st.markdown("---")
        
    st.subheader("✍️ Bagikan Pengalaman Menginap Anda")
    with st.form("Form_Review"):
        u_nama = st.text_input("Nama Anda:")
        u_rate = st.slider("Beri Bintang:", 1, 5, 5)
        u_komentar = st.text_area("Tulis Ulasan/Kritik/Saran:")
        
        if st.form_submit_button("Kirim Review"):
            if u_nama and u_komentar:
                st.session_state.reviews.append({
                    "User": u_nama,
                    "Rating": u_rate,
                    "Komentar": u_komentar
                })
                st.success("Terima kasih atas ulasan Anda!")
                st.rerun()
            else:
                st.error("Form mohon diisi lengkap.")