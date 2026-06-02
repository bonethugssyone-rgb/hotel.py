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
            st.error("Pendaftaran gagal karena tidak ada kamar tersedia.")
        elif check_in >= check_out:
            st.error("Tanggal Check Out harus lebih lambat dari tanggal Check In!")
        else:
            # OPERASI ARRAY: Menambahkan Dictionary baru ke dalam List Array
            data_baru = {
                "nama": nama,
                "kamar": no_kamar,
                "tipe": tipe_kamar,
                "check_in": str(check_in),
                "check_out": str(check_out),
                "telepon": telepon,
                "total_biaya": total_biaya
            }
            st.session_state.reservasi.append(data_baru)
            st.success(f"🎉 Reservasi Berhasil Ditambahkan! Kamar {no_kamar} resmi dipesan oleh {nama}.")
            st.balloons()


# FITUR 3: CEK KETERSEDIAAN KAMAR
elif menu == "🔍 3. Cek Ketersediaan Kamar":
    st.header("🔎 Panel Pengecekan Status Kamar")
    st.write("Gunakan fitur ini untuk melihat secara real-time kamar mana saja yang sudah terisi dan masih kosong.")
    
    kamar_terisi = [item['kamar'] for item in arr_reservasi]
    
    # Tampilkan Grid Kamar Berdasarkan Tipe
    for tipe, daftar_kamar in MASTER_KAMAR.items():
        st.subheader(f"Tipe Kamar: {tipe} (Tarif: Rp {TARIF_KAMAR[tipe]:,} / malam)")
        cols = st.columns(len(daftar_kamar))
        
        for idx, room in enumerate(daftar_kamar):
            with cols[idx]:
                if room in kamar_terisi:
                    # Cari nama pengisi kamar tersebut
                    nama_tamu = next(item['nama'] for item in arr_reservasi if item['kamar'] == room)
                    st.error(f"🛏️ **{room}**\n\n🔴 Terisi\n\n({nama_tamu})")
                else:
                    st.success(f"🛏️ **{room}**\n\n🟢 Tersedia")


# FITUR 4 & 5: DAFTAR RESERVASI (TRAVERSAL) & PENCARIAN RESERVASI (SEARCH)
elif menu == "📋 4. Daftar & Cari Reservasi":
    st.header("📋 Pusat Data Reservasi Terdaftar")
    
    # Opsi Pencarian Data (Fitur 5)
    st.subheader("🔍 Filter Pencarian Data (Implementasi Linear Search)")
    col_c1, col_c2 = st.columns([1, 2])
    with col_c1:
        opsi_cari = st.selectbox("Cari Berdasarkan Kolom:", ["Nama Tamu", "Nomor Kamar"])
    with col_c2:
        keyword = st.text_input("Ketikkan kata kunci yang ingin dicari (Real-time):")
        
    # Proses Menyaring Array secara Manual (Traversal & Pencarian)
    hasil_pencarian = []
    for item in arr_reservasi:
        if keyword:
            if opsi_cari == "Nama Tamu" and keyword.lower() in item['nama'].lower():
                hasil_pencarian.append(item)
            elif opsi_cari == "Nomor Kamar" and keyword.strip() == item['kamar']:
                hasil_pencarian.append(item)
        else:
            # Jika kolom keyword kosong, tampilkan seluruh isi Array (Traversal)
            hasil_pencarian.append(item)
            
    # Menampilkan Hasil dalam Tampilan Tabel Profesional (Fitur 4)
    st.subheader("📄 Hasil Struktur Data Array Saat Ini")
    if hasil_pencarian:
        df_display = pd.DataFrame(hasil_pencarian)
        # Penamaan ulang kolom tabel agar rapi saat dilihat user
        df_display.columns = ['Nama Tamu', 'No. Kamar', 'Tipe Kamar', 'Tanggal Check In', 'Tanggal Check Out', 'No. Telepon', 'Total Pendapatan (Rp)']
        st.dataframe(df_display, use_container_width=True)
    else:
        st.warning("Data pencarian tidak ditemukan dalam index array kami.")


# FITUR 6: EDIT RESERVASI (UPDATE ARRAY)
elif menu == "✏️ 5. Edit Reservasi":
    st.header("✏️ Modifikasi & Perubahan Data Reservasi (Update Array)")
    
    if not arr_reservasi:
        st.warning("Tidak ada data reservasi yang tersedia untuk diubah.")
    else:
        # Tampilkan opsi berdasarkan indeks array asli
        pilihan_edit = [f"{i} | Kamar {item['kamar']} - Atas Nama: {item['nama']}" for i, item in enumerate(arr_reservasi)]
        pilihan_terpilih = st.selectbox("Pilih data reservasi yang ingin Anda update:", pilihan_edit)
        
        # Ambil indeks asli array dari string pilihan
        indeks_array = int(pilihan_terpilih.split(" | ")[0])
        data_lama = arr_reservasi[indeks_array]
        
        st.markdown("---")
        st.subheader(f"Form Pembaruan Data Index Ke- {indeks_array}")
        
        col_ed1, col_ed2 = st.columns(2)
        with col_ed1:
            new_nama = st.text_input("Ubah Nama Tamu:", value=data_lama['nama'])
            new_tipe = st.selectbox("Ubah Tipe Kamar:", ["Standard", "Deluxe", "Suite"], index=["Standard", "Deluxe", "Suite"].index(data_lama['tipe']))
            new_kamar = st.text_input("Ubah Nomor Kamar:", value=data_lama['kamar'])
            new_telp = st.text_input("Ubah Nomor Telepon:", value=data_lama['telepon'])
            
        with col_ed2:
            ci_date = datetime.strptime(data_lama['check_in'], "%Y-%m-%d")
            co_date = datetime.strptime(data_lama['check_out'], "%Y-%m-%d")
            new_ci = st.date_input("Ubah Tanggal Check In:", value=ci_date)
            new_co = st.date_input("Ubah Tanggal Check Out:", value=co_date)
            
            # Hitung ulang tarif secara otomatis
            new_hari = hitung_hari(new_ci, new_co)
            new_biaya = new_hari * TARIF_KAMAR[new_tipe]
            
            st.write(f"Durasi Tinggal Baru: **{new_hari} Malam**")
            st.write(f"Kalkulasi Biaya Baru: **Rp {new_biaya:,}**")
            
        if st.button("Simpan Pembaruan Data (Update Array Index)"):
            # OPERASI ARRAY: Memperbarui nilai dictionary pada indeks tertentu
            st.session_state.reservasi[indeks_array] = {
                "nama": new_nama,
                "kamar": new_kamar,
                "tipe": new_tipe,
                "check_in": str(new_ci),
                "check_out": str(new_co),
                "telepon": new_telp,
                "total_biaya": new_biaya
            }
            st.success("✅ Data Array berhasil diperbarui (di-update)!")
            st.rerun()


# FITUR 7: PEMBATALAN RESERVASI (DELETE ARRAY)
elif menu == "❌ 6. Pembatalan Reservasi":
    st.header("❌ Pembatalan & Penghapusan Reservasi")
    
    if not arr_reservasi:
        st.warning("Belum ada data reservasi aktif di sistem.")
    else:
        pilihan_batal = [f"{i} | Tamu: {item['nama']} (Kamar {item['kamar']})" for i, item in enumerate(arr_reservasi)]
        batal_terpilih = st.selectbox("Pilih reservasi yang akan dibatalkan secara permanen:", pilihan_batal)
        
        indeks_batal = int(batal_terpilih.split(" | ")[0])
        nama_target = arr_reservasi[indeks_batal]['nama']
        kamar_target = arr_reservasi[indeks_batal]['kamar']
        
        st.warning(f"Apakah Anda yakin ingin menghapus transaksi {nama_target} di Kamar {kamar_target}?")
        
        if st.button("Ya, Batalkan Reservasi (Delete dari Array)", type="primary"):
            # OPERASI ARRAY: Menghapus data dari list menggunakan fungsi pop berdasarkan indeks
            st.session_state.reservasi.pop(indeks_batal)
            st.success(f"💥 Reservasi {nama_target} berhasil dibatalkan. Kamar {kamar_target} sekarang kembali kosong!")
            st.rerun()


# FITUR 10: EXPORT DATA KE EXCEL
elif menu == "📥 7. Export Data ke Excel":
    st.header("📥 Export Laporan Akhir Ke File Excel (.xlsx)")
    st.write("Fitur tambahan nilai plus untuk mengunduh seluruh isi data array lokal sistem ke spreadsheet.")
    
    if arr_reservasi:
        # Mengubah array of dictionary menjadi Pandas DataFrame
        df_excel = pd.DataFrame(arr_reservasi)
        df_excel.columns = ['Nama Penyewa', 'Nomor Kamar', 'Tipe Kamar', 'Tanggal CheckIn', 'Tanggal CheckOut', 'Kontak Telepon', 'Total Transaksi (Rp)']
        
        # Proses ekspor data menggunakan buffer memory IO stream
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_excel.to_excel(writer, index=False, sheet_name='Data_Reservasi_Hotel')
        buffer.seek(0)
        
        st.download_button(
            label="💾 Download Laporan Excel Resmi",
            data=buffer,
            file_name=f"Laporan_Sistem_Hotel_{datetime.today().strftime('%Y-%m-%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        st.success("File Excel berhasil diproduksi secara dinamis! Klik tombol di atas untuk mengunduh.")
    else:
        st.error("Gagal melakukan export karena tidak ada indeks data di dalam Array.")
