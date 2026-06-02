import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. KONFIGURASI MASTER DATA & LOGIN STAF
# ==========================================
TARIF_KAMAR = {
    "Standard": 300000,
    "Deluxe": 500000,
    "Suite": 800000
}

TOTAL_KAMAR_HOTEL = 50 

USER_CREDENTIALS = {
    "admin": "admin123",
    "resepsionis": "hotel123"
}

# ==========================================
# 2. INITIALIZATION DATA (ARRAY DI SESSION STATE)
# ==========================================
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
if 'last_invoice' not in st.session_state:
    st.session_state.last_invoice = None

# Struktur Array Awal yang sudah diperbaiki agar tidak KeyError
if 'reservasi' not in st.session_state:
    st.session_state.reservasi = [
        {
            "id_nota": "HTL-001",
            "nama": "Andi",
            "kamar": "101",
            "tipe": "Deluxe",
            "check_in": "01/06/26",
            "check_out": "03/06/26",
            "telepon": "08123456789",
            "total_biaya": 1000000
        },
        {
            "id_nota": "HTL-002",
            "nama": "Budi",
            "kamar": "102",
            "tipe": "Standard",
            "check_in": "02/06/26",
            "check_out": "05/06/26",
            "telepon": "08987654321",
            "total_biaya": 900000
        }
    ]

arr_reservasi = st.session_state.reservasi

# ==========================================
# 3. HELPER FUNCTION (HITUNG HARI)
# ==========================================
def hitung_hari(ci_str, co_str):
    try:
        d1 = datetime.strptime(ci_str, "%d/%m/%y")
        d2 = datetime.strptime(co_str, "%d/%m/%y")
        hari = (d2 - d1).days
        return max(1, hari)
    except:
        return 1

# ==========================================
# 4. HALAMAN LOGIN STAF
# ==========================================
st.set_page_config(page_title="Sistem Reservasi Hotel Berbasis Array", layout="wide", page_icon="🏨")

if not st.session_state.is_logged_in:
    st.markdown("<h2 style='text-align: center;'>🏨 Sistem Internal Reservasi Hotel</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Khusus Hak Akses Staf Resepsionis & Admin Hotel</p>", unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
    with col_l2:
        st.markdown("---")
        with st.form("Form_Login"):
            st.subheader("🔒 Login Autentikasi Staf")
            username_input = st.text_input("Username Staf")
            password_input = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Masuk ke Dashboard Staf", type="primary")
            
            if submit_login:
                if username_input in USER_CREDENTIALS and USER_CREDENTIALS[username_input] == password_input:
                    st.session_state.is_logged_in = True
                    st.session_state.current_user = username_input
                    st.rerun()
                else:
                    st.error("Username atau Password Staf salah.")
        st.info("💡 **Akun Staf untuk Demo:**\n* Username: `admin` | Password: `admin123`")
    st.stop()

# ==========================================
# 5. HALAMAN UTAMA (SETELAH LOGIN)
# ==========================================
col_head_1, col_head_2 = st.columns([4, 1])
with col_head_1:
    st.title("🏨 Sistem Reservasi Hotel Berbasis Array Menggunakan Python dan Streamlit")
with col_head_2:
    st.markdown(f"<div style='text-align: right; padding-top: 20px;'>🔑 Staf: <b>{st.session_state.current_user.upper()}</b></div>", unsafe_allow_html=True)
    if st.button("🚪 Logout Staf", type="secondary", use_container_width=True):
        st.session_state.is_logged_in = False
        st.session_state.current_user = ""
        st.session_state.last_invoice = None
        st.rerun()

st.markdown("---")

menu = st.sidebar.radio("📌 Navigasi Fitur:", [
    "Dashboard Hotel & Laporan",
    "Tambah Reservasi & Struk",
    "Cek Ketersediaan Kamar",
    "Daftar Reservasi",
    "Pencarian Reservasi",
    "Edit Reservasi",
    "Pembatalan Reservasi"
])

# ==========================================
# JALUR FITUR UTAMA SESUAI SPESIFIKASI
# ==========================================

# ------------------------------------------
# FITUR 1 & FITUR 9: DASHBOARD & LAPORAN PENDAPATAN
# ------------------------------------------
if menu == "Dashboard Hotel & Laporan":
    st.header("🏨 1. Dashboard Hotel & Laporan Pendapatan")
    
    total_terisi = len(arr_reservasi)
    total_kosong = TOTAL_KAMAR_HOTEL - total_terisi
    total_reservasi = len(arr_reservasi)
    total_pendapatan = sum(item['total_biaya'] for item in arr_reservasi)
    
    st.subheader("Informasi yang Ditampilkan")
    st.text(f"Total Kamar     : {TOTAL_KAMAR_HOTEL}")
    st.text(f"Kamar Terisi    : {total_terisi}")
    st.text(f"Kamar Kosong    : {total_kosong}")
    st.text(f"Total Reservasi : {total_reservasi}")
    st.text(f"Pendapatan      : Rp {total_pendapatan:,}")
    
    st.markdown("---")
    
    st.subheader("📊 9. Laporan Pendapatan")
    st.text(f"Total Transaksi : {total_reservasi}")
    st.text(f"Pendapatan      : Rp {total_pendapatan:,}")
    if arr_reservasi:
        df_temp = pd.DataFrame(arr_reservasi)
        tipe_terbanyak = df_temp['tipe'].value_counts().idxmax()
        st.text(f"Reservasi terbanyak : Tipe {tipe_terbanyak}")


# ------------------------------------------
# FITUR 2, 8 & 10: TAMBAH RESERVASI, BIAYA OTOMATIS & STRUK NOTA
# ------------------------------------------
elif menu == "Tambah Reservasi & Struk":
    st.header("📝 2. Tambah Reservasi")
    
    col_input, col_struk = st.columns([1.2, 1])
    
    with col_input:
        st.subheader("Input Data")
        nama = st.text_input("Nama Tamu")
        no_kamar = st.text_input("Nomor Kamar")
        tipe_kamar = st.selectbox("Tipe Kamar", ["Standard", "Deluxe", "Suite"])
        check_in = st.text_input("Check In (Format: DD/MM/YY)", value=datetime.today().strftime("%d/%m/%y"))
        check_out = st.text_input("Check Out (Format: DD/MM/YY)", value=datetime.today().strftime("%d/%m/%y"))
        no_telp = st.text_input("Nomor Telepon")
        
        st.markdown("---")
        
        # FITUR 8: Perhitungan Biaya Otomatis
        st.subheader("💰 8. Perhitungan Biaya Otomatis")
        lama_menginap = hitung_hari(check_in, check_out)
        harga_tipe = TARIF_KAMAR[tipe_kamar]
        total_biaya = harga_tipe * lama_menginap
        
        st.text(f"Tarif Tipe {tipe_kamar}: Rp {harga_tipe:,} / Hari")
        st.text(f"Lama Menginap   : {lama_menginap} Hari")
        st.markdown(f"**Total Tagihan : Rp {total_biaya:,}**")
        
        if st.button("Proses Simpan & Cetak Struk", type="primary"):
            kamar_terpakai = [item['kamar'] for item in arr_reservasi]
            
            if not nama or not no_kamar:
                st.error("Nama Tamu dan Nomor Kamar harus diisi!")
            elif no_kamar in kamar_terpakai:
                st.error(f"Kamar {no_kamar} sudah terisi (Double Booking)!")
            else:
                id_nota_baru = f"HTL-{len(arr_reservasi) + 1:03d}"
                
                # OPERASI ARRAY: Append
                data_baru = {
                    "id_nota": id_nota_baru,
                    "nama": nama,
                    "kamar": no_kamar,
                    "tipe": tipe_kamar,
                    "check_in": check_in,
                    "check_out": check_out,
                    "telepon": no_telp,
                    "total_biaya": total_biaya
                }
                st.session_state.reservasi.append(data_baru)
                st.session_state.last_invoice = data_baru
                st.success("Reservasi Berhasil Ditambahkan!")
                st.rerun()

    with col_struk:
        st.subheader("🧾 Struk Bukti Reservasi")
        if st.session_state.last_invoice is not None:
            struk = st.session_state.last_invoice
            st.markdown("""
            <style>
            .struk-box {
                background-color: #f9f9f9;
                padding: 15px;
                border: 1px dashed #333;
                font-family: 'Courier New', Courier, monospace;
                color: #000;
            }
            </style>
            """, unsafe_allow_html=True)
            
            konten_struk = f"""
====================================
         HOTEL RESERVATION          
====================================
No. Nota    : {struk['id_nota']}
Staf Kassa  : {st.session_state.current_user.upper()}
Tanggal     : {datetime.today().strftime('%d/%m/%Y %H:%M')}
------------------------------------
Nama Tamu   : {struk['nama']}
No. Telepon : {struk['telepon']}
No. Kamar   : {struk['kamar']}
Tipe Kamar  : {struk['tipe']}
------------------------------------
Check In    : {struk['check_in']}
Check Out   : {struk['check_out']}
Durasi      : {hitung_hari(struk['check_in'], struk['check_out'])} Hari
------------------------------------
TOTAL BAYAR : Rp {struk['total_biaya']:,}
====================================
    TERIMA KASIH ATAS KUNJUNGANNYA  
====================================
            """
            st.markdown(f'<div class="struk-box"><pre style="color:black;">{konten_struk}</pre></div>', unsafe_allow_html=True)
        else:
            st.info("Silahkan isi formulir di sebelah kiri dan klik simpan untuk menerbitkan struk kasir.")


# ------------------------------------------
# FITUR 3: CEK KETERSEDIAAN KAMAR
# ------------------------------------------
elif menu == "Cek Ketersediaan Kamar":
    st.header("🔍 3. Cek Ketersediaan Kamar")
    st.subheader("Manfaat: Menghindari double booking")
    
    kamar_terisi = [item['kamar'] for item in arr_reservasi]
    simulasi_kamar = ["101", "102", "103", "104", "105", "201", "202", "301"]
    
    st.markdown("### Contoh Status Kamar Saat Ini:")
    for room in simulasi_kamar:
        if room in kamar_terisi:
            st.error(f"Kamar {room} : Terisi")
        else:
            st.success(f"Kamar {room} : Tersedia")


# ------------------------------------------
# FITUR 4: DAFTAR RESERVASI (TRAVERSAL)
# ------------------------------------------
elif menu == "Daftar Reservasi":
    st.header("📋 4. Daftar Reservasi")
    st.subheader("Menampilkan seluruh data reservasi dalam bentuk tabel (Traversal Array).")
    
    if arr_reservasi:
        df_display = pd.DataFrame(arr_reservasi)[['id_nota', 'nama', 'kamar', 'tipe', 'check_in', 'check_out', 'total_biaya']]
        df_display.columns = ['ID Nota', 'Nama', 'Kamar', 'Tipe', 'Check In', 'Check Out', 'Total Biaya (Rp)']
        st.table(df_display)
    else:
        st.warning("Data Reservasi Kosong.")


# ------------------------------------------
# FITUR 5: PENCARIAN RESERVASI (SEARCH)
# ------------------------------------------
elif menu == "Pencarian Reservasi":
    st.header("🔍 5. Pencarian Reservasi")
    st.subheader("Opsi Pencarian")
    
    opsi_cari = st.radio("Cari Berdasarkan:", ["Nama Tamu", "Nomor Kamar"], horizontal=True)
    keyword = st.text_input("Cari :")
    
    if keyword:
        st.markdown("### Hasil:")
        found = False
        
        for item in arr_reservasi:
            if opsi_cari == "Nama Tamu" and keyword.lower() in item['nama'].lower():
                st.text(f"ID Nota: {item['id_nota']}\nNama: {item['nama']}\nNomor Kamar: Kamar {item['kamar']}\nTipe: {item['tipe']}\nTotal Biaya: Rp {item['total_biaya']:,}")
                st.markdown("---")
                found = True
            elif opsi_cari == "Nomor Kamar" and keyword.strip() == item['kamar']:
                st.text(f"ID Nota: {item['id_nota']}\nNama: {item['nama']}\nNomor Kamar: Kamar {item['kamar']}\nTipe: {item['tipe']}\nTotal Biaya: Rp {item['total_biaya']:,}")
                st.markdown("---")
                found = True
                
        if not found:
            st.warning("Data tidak ditemukan.")


# ------------------------------------------
# FITUR 6: EDIT RESERVASI (UPDATE)
# ------------------------------------------
elif menu == "Edit Reservasi":
    st.header("✏️ 6. Edit Reservasi")
    st.subheader("Yang Bisa Diubah: Nama, Nomor kamar, Tanggal check in, Tanggal check out")
    
    if not arr_reservasi:
        st.warning("Belum ada data reservasi.")
    else:
        pilihan_tamu = [f"{i} | {item['id_nota']} - {item['nama']} (Kamar {item['kamar']})" for i, item in enumerate(arr_reservasi)]
        pilih_edit = st.selectbox("Pilih reservasi yang akan diubah:", pilihan_tamu)
        
        idx = int(pilih_edit.split(" | ")[0])
        data_lama = arr_reservasi[idx]
        
        new_nama = st.text_input("Nama", value=data_lama['nama'])
        new_kamar = st.text_input("Nomor Kamar", value=data_lama['kamar'])
        new_ci = st.text_input("Tanggal check in", value=data_lama['check_in'])
        new_co = st.text_input("Tanggal check out", value=data_lama['check_out'])
        
        new_hari = hitung_hari(new_ci, new_co)
        new_biaya = new_hari * TARIF_KAMAR[data_lama['tipe']]
        
        if st.button("Simpan Perubahan (Update Array)"):
            st.session_state.reservasi[idx] = {
                "id_nota": data_lama['id_nota'],
                "nama": new_nama,
                "kamar": new_kamar,
                "tipe": data_lama['tipe'],
                "check_in": new_ci,
                "check_out": new_co,
                "telepon": data_lama['telepon'],
                "total_biaya": new_biaya
            }
            if st.session_state.last_invoice and st.session_state.last_invoice['id_nota'] == data_lama['id_nota']:
                st.session_state.last_invoice = st.session_state.reservasi[idx]
                
            st.success("Data reservasi berhasil diubah!")
            st.rerun()


# ------------------------------------------
# FITUR 7: PEMBATALAN RESERVASI (DELETE)
# ------------------------------------------
elif menu == "Pembatalan Reservasi":
    st.header("❌ 7. Pembatalan Reservasi")
    st.subheader("Menghapus data reservasi dari Array.")
    
    if not arr_reservasi:
        st.warning("Tidak ada data reservasi aktif.")
    else:
        pilihan_batal = [f"{i} | {item['id_nota']} - {item['nama']} (Kamar {item['kamar']})" for i, item in enumerate(arr_reservasi)]
        pilih_batal = st.selectbox("Pilih data yang akan dibatalkan:", pilihan_batal)
        
        idx_batal = int(pilih_batal.split(" | ")[0])
        nama_target = arr_reservasi[idx_batal]['nama']
        id_nota_target = arr_reservasi[idx_batal]['id_nota']
        
        if st.button("Batalkan Reservasi"):
            if st.session_state.last_invoice and st.session_state.last_invoice['id_nota'] == id_nota_target:
                st.session_state.last_invoice = None
                
            st.session_state.reservasi.pop(idx_batal)
            st.success(f"Reservasi {nama_target} berhasil dibatalkan")
            st.rerun()
