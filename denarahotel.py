import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# ==========================================
# 1. KONFIGURASI MASTER DATA HOTEL
# ==========================================
TARIF_KAMAR = {
    "Standard": 300000,
    "Deluxe": 500000,
    "Suite": 800000
}

# Membuat daftar nomor kamar statis berdasarkan tipe (Master Room List)
MASTER_KAMAR = {
    "Standard": [f"10{i}" for i in range(1, 10)],  # 101 - 109
    "Deluxe": [f"20{i}" for i in range(1, 10)],    # 201 - 209
    "Suite": [f"30{i}" for i in range(1, 6)]       # 301 - 305
}

TOTAL_KAMAR_HOTEL = sum(len(kamar) for kamar in MASTER_KAMAR.values())

# ==========================================
# 2. INITIALIZATION DATA AWAL (ARRAY DI SESSION STATE)
# ==========================================
if 'reservasi' not in st.session_state:
    # Seeding data awal agar dashboard langsung terlihat dinamis saat presentasi
    st.session_state.reservasi = [
        {
            "nama": "Andi",
            "kamar": "201",
            "tipe": "Deluxe",
            "check_in": "2026-06-01",
            "check_out": "2026-06-03",
            "telepon": "08123456789",
            "total_biaya": 1000000
        },
        {
            "nama": "Budi",
            "kamar": "101",
            "tipe": "Standard",
            "check_in": "2026-06-02",
            "check_out": "2026-06-05",
            "telepon": "08987654321",
            "total_biaya": 900000
        },
        {
            "nama": "Citra",
            "kamar": "301",
            "tipe": "Suite",
            "check_in": "2026-06-04",
            "check_out": "2026-06-06",
            "telepon": "08566778899",
            "total_biaya": 1600000
        }
    ]

# Mengambil array aktif dari session state
arr_reservasi = st.session_state.reservasi

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def hitung_hari(ci, co):
    if ci >= co:
        return 1
    return (co - ci).days

# ==========================================
# 4. STREAMLIT UI & INTERFACE
# ==========================================
st.set_page_config(page_title="Sistem Reservasi Hotel Profesional", layout="wide", page_icon="🏨")

st.title("🏨 Sistem Reservasi Hotel Berbasis Array")
st.caption("Aplikasi Sistem Hotel Dinamis Menggunakan Struktur Data Array (List of Dictionaries) - Python & Streamlit")
st.markdown("---")

# Menu Navigasi di Sidebar
menu = st.sidebar.radio("📌 Navigasi Fitur / Menu:", [
    "🏨 1. Dashboard Hotel & Laporan",
    "➕ 2. Tambah Reservasi",
    "🔍 3. Cek Ketersediaan Kamar",
    "📋 4. Daftar & Cari Reservasi",
    "✏️ 5. Edit Reservasi",
    "❌ 6. Pembatalan Reservasi",
    "📥 7. Export Data ke Excel"
])

# --- LOGIKA KODE TIAP FITUR ---

# FITUR 1 & 9: DASHBOARD HOTEL & LAPORAN PENDAPATAN
if menu == "🏨 1. Dashboard Hotel & Laporan":
    st.header("📊 Dashboard Utama Hotel & Analisis Pendapatan")
    
    total_terisi = len(arr_reservasi)
    total_kosong = TOTAL_KAMAR_HOTEL - total_terisi
    total_reservasi = len(arr_reservasi)
    total_pendapatan = sum(item['total_biaya'] for item in arr_reservasi)
    
    # Tampilan Informasi Ringkas Utama (Metrik Utama)
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Kamar Tersedia", f"{TOTAL_KAMAR_HOTEL} Kamar")
    col2.metric("Kamar Terisi 🔴", f"{total_terisi} Kamar")
    col3.metric("Kamar Kosong 🟢", f"{total_kosong} Kamar")
    col4.metric("Total Reservasi", f"{total_reservasi} Transaksi")
    col5.metric("Total Pendapatan", f"Rp {total_pendapatan:,}")
    
    st.markdown("---")
    st.subheader("📈 Laporan Statistik & Analisis Bisnis")
    
    if arr_reservasi:
        df_laporan = pd.DataFrame(arr_reservasi)
        
        col_lap1, col_lap2 = st.columns(2)
        with col_lap1:
            st.info("📊 **Metrik Favorit Tamu:**")
            # Menghitung tipe kamar terlaris secara dinamis
            tipe_terbanyak = df_laporan['tipe'].value_counts().idxmax()
            jumlah_terbanyak = df_laporan['tipe'].value_counts().max()
            st.write(f"* **Kategori Kamar Terlaris:** Kamar Tipe *{tipe_terbanyak}* ({jumlah_terbanyak} kali dipesan)")
            st.write(f"* **Rata-rata Pendapatan per Transaksi:** Rp {int(total_pendapatan / total_reservasi):,}")
            
        with col_lap2:
            st.success("💰 **Rincian Pendapatan per Tipe Kamar:**")
            rincian_biaya = df_laporan.groupby('tipe')['total_biaya'].sum()
            for tipe, nominal in rincian_biaya.items():
                st.write(f"* Tipe **{tipe}**: Rp {nominal:,}")
    else:
        st.warning("Belum ada data transaksi masuk di dalam sistem.")


# FITUR 2 & 8: TAMBAH RESERVASI & PERHITUNGAN BIAYA OTOMATIS
elif menu == "➕ 2. Tambah Reservasi":
    st.header("📝 Formulir Pendaftaran Tamu Baru")
    
    # Ambil list kamar yang saat ini sedang dipakai/terisi
    kamar_terisi = [item['kamar'] for item in arr_reservasi]
    
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        nama = st.text_input("Nama Lengkap Tamu:")
        tipe_kamar = st.selectbox("Pilih Tipe Kamar:", ["Standard", "Deluxe", "Suite"])
        
        # Saring nomor kamar secara dinamis berdasarkan Tipe Kamar dan Kamar yang belum terisi
        kamar_tersedia_pilihan = [k for k in MASTER_KAMAR[tipe_kamar] if k not in kamar_terisi]
        
        if kamar_tersedia_pilihan:
            no_kamar = st.selectbox("Pilih Nomor Kamar yang Tersedia:", kamar_tersedia_pilihan)
        else:
            no_kamar = None
            st.error(f"Maaf, semua kamar tipe {tipe_kamar} sudah penuh!")
            
        telepon = st.text_input("Nomor Telepon / WA Active:")

    with col_f2:
        check_in = st.date_input("Tanggal Mulai Check In:", datetime.today())
        # Check out otomatis minimal besoknya hari dari tanggal check in
        check_out = st.date_input("Tanggal Rencana Check Out:", datetime.today() + timedelta(days=1))
        
        # Perhitungan Otomatis Hari dan Tarif Kamar
        lama_menginap = hitung_hari(check_in, check_out)
        tarif_per_malam = TARIF_KAMAR[tipe_kamar]
        total_biaya = lama_menginap * tarif_per_malam
        
        st.markdown("### 💰 Rincian Biaya Otomatis:")
        st.write(f"Durasi Menginap : **{lama_menginap} Malam**")
        st.write(f"Tarif per Malam : **Rp {tarif_per_malam:,}**")
        st.subheader(f"Total Tagihan: Rp {total_biaya:,}")
        st.caption(f"Rumus Perhitungan: {lama_menginap} Hari × Rp {tarif_per_malam:,}")

    # Tombol submit untuk menambahkan data ke dalam array (Append)
    if st.button("Simpan Data Pemesanan (Append Array)", type="primary"):
        if not nama:
            st.error("Nama tamu tidak boleh kosong!")
        elif no_kamar is None:
            st.error("Pendaftaran