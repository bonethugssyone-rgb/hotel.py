import streamlit as st
import pandas as pd
from datetime import datetime, date 

# Seting awal tampilan web hotelnya biar dapet icon dan nama di tab browser
st.set_page_config(page_title="Denara Hotel", layout="wide", page_icon="🏨")

# ==========================================
# GAYA-GAYAAN INTERFACE (BIAR PINK ESTETIK)
# ==========================================
# Di sini kita mainan CSS dikit biar warna aplikasinya serba pink gemes dan gak ngebosenin
st.markdown("""
<style>
    .main { background-color: #FFF6F9; }
    section[data-testid="stSidebar"] { background-color: #FFE3EC; }
    .card { background-color: white; padding: 25px; border-radius: 15px; box-shadow: 0px 4px 15px rgba(0,0,0,0.04); margin-bottom: 20px; border: 1px solid #FFE3EC; }
    .title { font-size: 32px; font-weight: bold; color: #E91E63; margin-bottom: 10px; }
    .promo { background-color: #E3F0FF; padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 5px solid #2196F3; }
    .stButton>button { background-color: #FF4D8D; color: white; border-radius: 10px; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #E91E63; color: white; }
    .review-box { background-color: #FFF6F9; padding: 12px; border-radius: 12px; margin-bottom: 10px; border: 1px solid #FFE3EC; }
    .facility-tag { background-color: #FFE3EC; color: #E91E63; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 500; margin-right: 5px; display: inline-block; margin-bottom: 5px;}
    .price-text { font-size: 22px; font-weight: bold; color: #E91E63; }
    .promo-box { border: 2px dashed #FF4D8D; padding: 10px; border-radius: 8px; background-color: #FFF0F5; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA MASTER & KONDISI AWAL DATABASE
# ==========================================
# Daftar harga kamar per malamnya, silakan diubah kalau mau naik haji eh naik harga
TARIF_KAMAR = {
    "Standard Room": 650000, 
    "Superior Room": 1000000, 
    "Deluxe Room": 5000000, 
    "Suite Room": 9500000
}

# List fasilitas bawaan buat masing-masing tipe kamar biar tamu tau mereka dapet apa aja
FASILITAS_KAMAR = {
    "Standard Room": ["Free Wi-Fi", "Air Conditioning", "Smart TV 32\"", "Shower Bathroom", "Complimentary Water"],
    "Superior Room": ["Free Wi-Fi", "Air Conditioning", "Smart TV 43\"", "Water Heater", "Mini Refrigerator", "Coffee & Tea Maker"],
    "Deluxe Room": ["Free Wi-Fi", "Air Conditioning", "Smart TV 55\"", "Luxury Bathtub", "Mini Bar", "Safety Deposit Box", "Private Balcony"],
    "Suite Room": ["Free Wi-Fi", "Air Conditioning", "Smart TV 65\"", "Private Jacuzzi", "Premium Mini Bar", "Separate Living Room", "24/7 Butler Service", "Private Swimming Pool"]
}

# Menu makanan buat room service beserta harganya yang ramah kantong
MENU_MAKANAN = {
    "Nasi Goreng Kampung": 35000, 
    "Mie Goreng Cabe Ijo": 30000, 
    "Ayam Goreng Serundeng": 40000, 
    "Es Teh Manis Premium": 12000, 
    "Kopi Susu Aren": 20000
}

# Tempat nyimpen status kamar biar datanya gak ilang pas aplikasinya di-refresh
if "kamar_data" not in st.session_state:
    st.session_state.kamar_data = [
        {"No Kamar": "101", "Tipe Kamar": "Standard Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "102", "Tipe Kamar": "Standard Room", "Status": "🟨 Direservasi"}, 
        {"No Kamar": "103", "Tipe Kamar": "Standard Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "104", "Tipe Kamar": "Standard Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "105", "Tipe Kamar": "Standard Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "201", "Tipe Kamar": "Superior Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "202", "Tipe Kamar": "Superior Room", "Status": "🟨 Direservasi"}, 
        {"No Kamar": "203", "Tipe Kamar": "Superior Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "204", "Tipe Kamar": "Superior Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "301", "Tipe Kamar": "Deluxe Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "302", "Tipe Kamar": "Deluxe Room", "Status": "🟨 Direservasi"}, 
        {"No Kamar": "303", "Tipe Kamar": "Deluxe Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "401", "Tipe Kamar": "Suite Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "402", "Tipe Kamar": "Suite Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "403", "Tipe Kamar": "Suite Room", "Status": "🟨 Direservasi"}, 
    ]

# Data awal tamu yang ceritanya udah duluan booking biar aplikasi gak keliatan sepi
if "reservasi_log" not in st.session_state: 
    st.session_state.reservasi_log = [
        {"id": "RSV-102202", "nama": "Budi Santoso", "hp": "+62 8123444", "email": "budi@gmail.com", "kamar": "102", "tipe": "Standard Room", "check_in": "2026-06-01", "check_out": "2026-06-05", "total_biaya": 2600000, "sudah_dibayar": 2600000, "status_bayar": "Lunas (100%)", "metode": "Transfer BCA", "status": "🟨 Direservasi", "food_charge": 0},
        {"id": "RSV-202202", "nama": "Siti Rahma", "hp": "+62 8125555", "email": "siti@gmail.com", "kamar": "202", "tipe": "Superior Room", "check_in": "2026-06-03", "check_out": "2026-06-07", "total_biaya": 4000000, "sudah_dibayar": 2000000, "status_bayar": "Bayar Setengah (DP 50%)", "metode": "Mandiri Virtual Account", "status": "🟨 Direservasi", "food_charge": 65000},
        {"id": "RSV-403202", "nama": "Rayyanza", "hp": "+62 8129999", "email": "rayyanza@gmail.com", "kamar": "403", "tipe": "Suite Room", "check_in": "2026-06-05", "check_out": "2026-06-12", "total_biaya": 66500000, "sudah_dibayar": 66500000, "status_bayar": "Lunas (100%)", "metode": "Dana", "status": "🟨 Direservasi", "food_charge": 0},
    ]

# Inisialisasi tempat penampungan riwayat transaksi, pembatalan, pesanan makanan, voucher, dan review tamu
if "histori_transaksi" not in st.session_state: 
    st.session_state.histori_transaksi = [
        {"id": "RSV-101000", "nama": "Joko Widodo", "kamar": "101", "tipe": "Standard Room", "grand_total": 1300000, "status": "✅ Selesai (Check-Out)"}
    ]
if "log_pembatalan" not in st.session_state: st.session_state.log_pembatalan = []
if "makanan_log" not in st.session_state: st.session_state.makanan_log = []
if "kode_voucher_input" not in st.session_state: st.session_state.kode_voucher_input = ""
if "voucher_terpasang" not in st.session_state: st.session_state.voucher_terpasang = ""
if "ulasan_log" not in st.session_state: 
    st.session_state.ulasan_log = [{"nama": "Andi Pratama", "rating": 5, "komentar": "Keren bgt, nginep di lantai 4 berasa eksklusif!"}]

# ==========================================
# SIDEBAR MENUS
# ==========================================
# Bikin struktur menu utama di samping kiri pakai radio button
st.sidebar.title("🏨 Denara Hotel")
menu_utama = st.sidebar.radio("Menu Utama", [
    "🏠 Dashboard", 
    "🏨 Manajemen Kamar", 
    "💳 Area Transaksi Tamu", 
    "🍽️ Room Service", 
    "⭐ Penilaian Hotel", 
    "🛟 Bantuan"
])

# Logika percabangan buat nampilin sub-menu berdasarkan menu utama yang dipilih
if menu_utama == "🏠 Dashboard": pilihan_menu = "🏠 Dashboard"
elif menu_utama == "🏨 Manajemen Kamar":
    pilihan_menu = st.sidebar.radio("Sub-Menu Kamar", ["📝 Reservasi Baru", "🏨 Katalog Kamar", "🗺️ Denah Kamar"])
elif menu_utama == "💳 Area Transaksi Tamu":
    pilihan_menu = st.sidebar.radio("Sub-Menu Transaksi", ["💳 Pembayaran Tiket", "🔍 Cek Detail & Check-Out", "📜 Histori & Pembatalan"])
elif menu_utama == "🍽️ Room Service":
    pilihan_menu = st.sidebar.radio("Sub-Menu Room Service", ["🍽️ Pesan Makanan", "💳 Bayar Room Service"])
elif menu_utama == "⭐ Penilaian Hotel": pilihan_menu = "⭐ Ulasan Kepuasan"
elif menu_utama == "🛟 Bantuan":
    pilihan_menu = st.sidebar.radio("Sub-Menu Bantuan", ["❓ Pusat Bantuan", "📞 Kontak Layanan Service"])

# ==========================================
# PROSES LOGIKA TIAP SUB-MENU
# ==========================================

# --- 1. DASHBOARD ---
if pilihan_menu == "🏠 Dashboard":
    st.markdown('<div class="title">🏠 Selamat Datang di Denara Hotel</div>', unsafe_allow_html=True)
    
    # Hitung jumlah kamar yang statusnya masih ijo alias tersedia
    kamar_kosong = len([k for k in st.session_state.kamar_data if k["Status"] == "🟩 Tersedia"])
    st.metric("Kamar Kosong Yang Siap Dipesan (Lantai 1-4)", f"{kamar_kosong} Kamar")
    
    # Kotak info buat nampilin kode promo biar tamu tergiur buat transaksi
    st.markdown("""
    <div class="promo">
    <h4>📢 Info Promo Buat Kamu</h4>
    <p>Gunakan Kode Voucher spesial <b>DISC10%</b> pada menu pembayaran tiket untuk diskon maksimal!</p>
    </div>
    """, unsafe_allow_html=True)

    # Bagi layout jadi 2 kolom buat naruh info kamar terlaris dan ulasan terbaru
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>👑 Kamar Paling Laris</h3>', unsafe_allow_html=True)
        st.write("**Suite Room (Lantai 4 VIP)**")
        st.caption("Fasilitas Andalan: Private Jacuzzi & Premium Services")
        st.progress(0.95)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h3>⭐ Kata Tamu Yang Udah Nginep</h3>', unsafe_allow_html=True)
        for u in st.session_state.ulasan_log[-2:]:
            st.markdown(f'<div class="review-box"><b>{u["nama"]}</b> (⭐ {u["rating"]})<br><small>"{u["komentar"]}"</small></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 2. RESERVASI BARU ---
elif pilihan_menu == "📝 Reservasi Baru":
    st.title("📝 Form Reservasi Hotel")
    col_kiri, col_kanan = st.columns([1.5, 1])

    # Kolom kiri diisi inputan biodata tamu dan tanggal booking
    with col_kiri:
        st.subheader("Isi Data Diri Dulu Yuk")
        nama = st.text_input("Nama Lengkap (Sesuai KTP)")
        
        # Di sini format no HP otomatis langsung dikasih '+62 ', jadi tamu tinggal lanjutin ngetik aja
        hp = st.text_input("Nomor WhatsApp Aktif", value="+62 ")
        email = st.text_input("Alamat Email", value="@gmail.com")
        pilihan_tipe = st.selectbox("Mau Kamar Tipe Apa?", list(TARIF_KAMAR.keys()))
        
        # Looping buat nampilin tag fasilitas otomatis sesuai tipe kamar yang dipilih
        st.markdown("**Fasilitas Yang Bakal Kamu Dapet:**")
        for fas in FASILITAS_KAMAR[pilihan_tipe]:
            st.markdown(f'<span class="facility-tag">✔️ {fas}</span>', unsafe_allow_html=True)
            
        jml_tamu = st.number_input("Buat Berapa Orang?", min_value=1, max_value=8, value=2)
        tgl_in = st.date_input("Tanggal Check-In", date.today())
        tgl_out = st.date_input("Tanggal Check-Out", date.today() + pd.Timedelta(days=1))
        pilihan_late = st.selectbox("Mau Keluar Jam Berapa?", ["Normal Check-Out", "Late Check-Out (+Rp 50.000)"])

    # Kolom kanan isinya rekomendasi cerdas dari bot dan pilihan add-on (fasilitas tambahan)
    with col_kanan:
        st.subheader("🤖 Saran Kamar Dari Bot")
        saran = "Standard Room" if jml_tamu <= 2 else ("Superior Room" if jml_tamu <= 4 else "Suite Room")
        st.info(f"Karena kamu bawa {jml_tamu} orang, cocoknya pilih **{saran}**.")
        
        # Nyari kamar yang cocok di lantai yang sesuai (Lantai 1-4) dan statusnya harus ijo (Tersedia)
        pemetaan_lantai = {"Standard Room": "1", "Superior Room": "2", "Deluxe Room": "3", "Suite Room": "4"}
        lantai_target = pemetaan_lantai[pilihan_tipe]
        kamar_cocok = next((k for k in st.session_state.kamar_data if k["Tipe Kamar"] == pilihan_tipe and k["Status"] == "🟩 Tersedia" and k["No Kamar"].startswith(lantai_target)), None)
        
        if kamar_cocok:
            st.success(f"Kamar Ready! Kamu mendapatkan tipe **{pilihan_tipe}** dengan **No. {kamar_cocok['No Kamar']}** di Lantai {lantai_target}.")
        else:
            st.error(f"Waduh, tipe kamar {pilihan_tipe} di Lantai {lantai_target} saat ini sedang penuh.")

        st.markdown("---")
        st.subheader("🎁 Mau Tambah Fasilitas Ekstra?")
        addons = []
        # Berbagai macam checkbox fasilitas tambahan, kalau dicentang otomatis nambah biaya
        if st.checkbox("Sarapan Pagi Sepuasnya (+Rp 50.000)"): addons.append("Breakfast")
        if st.checkbox("Antar Jemput Bandara (+Rp 150.000)"): addons.append("Airport Pickup")
        if st.checkbox("Ekstra Kasur / Extra Bed (+Rp 200.000)"): addons.append("Extra Bed")
        if st.checkbox("Akses VIP Executive Lounge (+Rp 250.000)"): addons.append("VIP Lounge")
        if st.checkbox("Floating Breakfast di Kolam Renang (+Rp 120.000)"): addons.append("Floating Breakfast")
        if st.checkbox("Paket Dekorasi Kamar (Birthday/Honeymoon) (+Rp 350.000)"): addons.append("Room Decoration")
        if st.checkbox("Akses Layanan Netflix & Disney+ Premium (+Rp 30.000)"): addons.append("Streaming Apps")
        if st.checkbox("Rental Skuter Listrik Seharian (+Rp 75.000)"): addons.append("Electric Scooter")

        # Tombol submit buat mindahin data ke antrian checkout billing
        if st.button("Booking & Lanjut Ke Pembayaran ➡️", type="primary"):
            if not nama or not kamar_cocok or tgl_out <= tgl_in or email == "@gmail.com" or hp == "+62 ":
                st.error("Isi formnya yang bener dong, pastikan semua kolom data dan nomor handphone sudah terisi lengkap.")
            else:
                # Kalkulasi total harga seluruh fasilitas tambahan yang dipilih tamu
                biaya_extra_awal = (
                    (50000 if "Late" in pilihan_late else 0) + 
                    (50000 if "Breakfast" in addons else 0) + 
                    (150000 if "Airport Pickup" in addons else 0) + 
                    (200000 if "Extra Bed" in addons else 0) + 
                    (250000 if "VIP Lounge" in addons else 0) +
                    (120000 if "Floating Breakfast" in addons else 0) +
                    (350000 if "Room Decoration" in addons else 0) +
                    (30000 if "Streaming Apps" in addons else 0) +
                    (75000 if "Electric Scooter" in addons else 0)
                )
                
                # Masukin data ke temporary session state biar bisa dibaca di menu pembayaran
                st.session_state.proses_checkout = {
                    "id_invoice": f"RSV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "nama": nama, "hp": hp, "email": email, "kamar": kamar_cocok,
                    "tipe": pilihan_tipe, "check_in": str(tgl_in), "check_out": str(tgl_out),
                    "add_on": addons, "late_checkout": pilihan_late, "biaya_ekstra_total": biaya_extra_awal
                }
                st.session_state.voucher_terpasang = "" 
                st.success("Sip! Data udah kesimpen, gass ke sub-menu 'Pembayaran Tiket' buat memilih opsi pembayaran.")

# --- 3. KATALOG KAMAR ---
elif pilihan_menu == "🏨 Katalog Kamar":
    st.title("🏨 Katalog Pilihan & Spesifikasi Eksklusif Kamar")
    st.write("Temukan kenyamanan terbaik selama menginap di Denara Hotel:")
    
    # Looping buat nampilin kartu katalog untuk setiap tipe kamar beserta harganya
    for tipe, harga in TARIF_KAMAR.items():
        with st.container():
            st.markdown(f"""
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <span style="font-size: 24px; font-weight: bold; color: #E91E63;">✨ {tipe}</span>
                    <span class="price-text">Rp {harga:,} <small style="color: #777; font-size: 14px; font-weight: normal;">/ Malam</small></span>
                </div>
                <hr style="border: 0; border-top: 1px solid #FFE3EC; margin: 12px 0;">
                <p style="margin-bottom: 8px; font-weight: bold; color: #555;">Fasilitas Utama Bawaan Kamar:</p>
            """, unsafe_allow_html=True)
            
            for fas in FASILITAS_KAMAR[tipe]:
                st.markdown(f'<span class="facility-tag">⭐ {fas}</span>', unsafe_allow_html=True)
                
            st.markdown('</div>', unsafe_allow_html=True)

# --- 4. DENAH KAMAR ---
elif pilihan_menu == "🗺️ Denah Kamar":
    st.title("🗺️ Map Letak Kamar Hotel Lantai 1 s/d 4")
    
    # Nampilin visualisasi denah grid kamar dari lantai 1 sampai lantai 4
    for lt in range(1, 5):
        if lt == 1: st.subheader("🏢 Lantai 1 — ROOM STANDARD")
        elif lt == 2: st.subheader("🏢 Lantai 2 — SUPERIOR ROOM")
        elif lt == 3: st.subheader("🏢 Lantai 3 — DELUXE ROOM")
        elif lt == 4: st.subheader("🏢 Lantai 4 — SUITE ROOM")
            
        # Filter kamar berdasarkan digit awal nomor kamar (mewakili lantai)
        kamar_lantai = [k for k in st.session_state.kamar_data if k["No Kamar"].startswith(str(lt))]
        cols = st.columns(6)
        for idx, detail in enumerate(kamar_lantai):
            with cols[idx % 6]:
                # Warnanya otomatis ijo kalau kosong, merah kalau udah di-booking orang
                if detail["Status"] == "🟩 Tersedia": 
                    st.success(f"🚪 {detail['No Kamar']}\n(Masih tersedia)")
                else: 
                    st.error(f"🟨 {detail['No Kamar']}\n(Ada yang booking)")

# --- 5. PEMBAYARAN TIKET RESERVASI ---
elif pilihan_menu == "💳 Pembayaran Tiket":
    st.title("💳 Menu Pembayaran Billing Kamar")
    # Validasi biar gak ada tamu ilegal yang masuk menu ini tanpa ngisi form reservasi dulu
    if "proses_checkout" not in st.session_state:
        st.warning("Belum ada antrian kamar yang mau dibayar nih. Buka menu 'Reservasi Baru' dulu ya.")
        st.stop()

    dt = st.session_state.proses_checkout
    # Ngitung berapa malam durasi menginap berdasarkan selisih tanggal check-in & check-out
    malam = max(1, (datetime.strptime(dt["check_out"], "%Y-%m-%d") - datetime.strptime(dt["check_in"], "%Y-%m-%d")).days)
    
    harga_pokok = TARIF_KAMAR.get(dt["tipe"], 0) * malam
    biaya_extra = dt["biaya_ekstra_total"]
    subtotal = harga_pokok + biaya_extra

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎟️ Kupon Promo & Diskon")
    
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.markdown('<div class="promo-box"><b>🔥 DISC10%</b><br><small>Diskon potongan 10% dari total transaksi kamu!</small></div>', unsafe_allow_html=True)
    with p_col2:
        st.markdown('<div class="promo-box"><b>🎁 DENARADEAL</b><br><small>Potongan langsung Rp 100.000 tanpa minimum transaksi.</small></div>', unsafe_allow_html=True)
        
    vc_input_col, vc_btn_col = st.columns([3, 1])
    with vc_input_col:
        kode_input = st.text_input("Masukkan kode voucher di sini:", value=st.session_state.voucher_terpasang, placeholder="Contoh: DISC10%").strip()
    with vc_btn_col:
        st.write("##") 
        if st.button("Terapkan Kupon"):
            if kode_input.upper() in ["DISC10%", "DENARADEAL"]:
                st.session_state.voucher_terpasang = kode_input.upper()
                st.toast(f"🎉 Voucher {st.session_state.voucher_terpasang} berhasil dipasang!", icon="✅")
            elif kode_input == "":
                st.session_state.voucher_terpasang = ""
            else:
                st.error("Kode kupon salah.")
                
    # Logika hitung potongan harga diskon kupon voucher
    diskon = 100000 if st.session_state.voucher_terpasang == "DENARADEAL" else (subtotal * 0.1 if st.session_state.voucher_terpasang == "DISC10%" else 0)
    pajak = subtotal * 0.11
    total_tagihan = (subtotal + pajak) - diskon

    # Pilihan Metode Pembayaran
    metode = st.selectbox("Mau Bayar Lewat Mana?", ["Transfer BCA", "Mandiri Virtual Account", "GoPay", "OVO", "Dana"])
    
    # --- FITUR TAMBAHAN REKENING / NO E-WALLET ---
    if "Transfer" in metode or "Account" in metode:
        no_sumber_bayar = st.text_input(f"Masukkan Nomor Rekening Bank Anda ({metode}):", placeholder="Contoh: 8012345xxx")
    else:
        no_sumber_bayar = st.text_input(f"Masukkan Nomor HP Akun {metode} Anda:", placeholder="Contoh: 08123456xxx")
    # ---------------------------------------------

    # Fitur andalan: Bisa milih bayar lunas langsung atau bayar setengah (DP 50%) dulu
    status_bayar = st.selectbox("Opsi Ketentuan Pembayaran", ["Lunas (100%)", "Bayar Setengah (DP 50%)"])
    
    # Kalau pilih bayar setengah, tagihan sekarang langsung dibagi dua otomatis oleh sistem
    jumlah_dibayar_sekarang = total_tagihan if status_bayar == "Lunas (100%)" else (total_tagihan / 2)
    st.info(f"Nominal yang harus dibayarkan sekarang: **Rp {int(jumlah_dibayar_sekarang):,}**")

    # Nampilin struk rincian yang lebih detail untuk opsi DP dan info nomor pengirim
    struk_text = f"""
    ================================================
               DENARA HOTEL - NOTA BOOKING
    ================================================
    ID Booking   : {dt['id_invoice']}
    Nama Tamu    : {dt['nama']}
    Nomor Kamar  : Kamar No. {dt['kamar']['No Kamar']} ({dt['tipe']})
    Durasi       : {malam} Malam ({dt['check_in']} s/d {dt['check_out']})
    ------------------------------------------------
    Harga Kamar  : Rp {harga_pokok:,}
    Biaya Ekstra : Rp {biaya_extra:,}
    Pajak PPN 11%: Rp {int(pajak):,}
    Potongan     : -Rp {int(diskon):,}
    ------------------------------------------------
    TOTAL BILL   : Rp {int(total_tagihan):,}
    ------------------------------------------------
    Ketentuan    : {status_bayar}
    Metode Bayar : {metode}
    No. Rek/HP   : {no_sumber_bayar if no_sumber_bayar else '-'}
    """
    
    if status_bayar == "Bayar Setengah (DP 50%)":
        struk_text += f"\n    DP 50%       : Rp {int(jumlah_dibayar_sekarang):,}"
        struk_text += f"\n    Sisa Tagihan : Rp {int(total_tagihan - jumlah_dibayar_sekarang):,}"
        
    struk_text += "\n    ================================================"
    st.code(struk_text, language="text")

    # Tombol buat nge-deal pembayaran dan ngerubah status kamar jadi "Direservasi" (Kuning)
    if st.button("Konfirmasi Bayar & Ambil Kode Kamar ✔️", type="primary"):
        if not no_sumber_bayar:
            st.error(f"Mohon isi Nomor Rekening atau Nomor HP {metode} Anda terlebih dahulu untuk validasi transaksi!")
        else:
            st.session_state.reservasi_log.append({
                "id": dt["id_invoice"], "nama": dt["nama"], "hp": dt["hp"], "email": dt["email"],
                "kamar": dt["kamar"]["No Kamar"], "tipe": dt["tipe"], "check_in": dt["check_in"],
                "check_out": dt["check_out"], "total_biaya": total_tagihan, "sudah_dibayar": jumlah_dibayar_sekarang,
                "status_bayar": status_bayar, "metode": f"{metode} ({no_sumber_bayar})", "status": "🟨 Direservasi", "food_charge": 0
            })
            for kamar in st.session_state.kamar_data:
                if kamar["No Kamar"] == dt["kamar"]["No Kamar"]:
                    kamar["Status"] = "🟨 Direservasi"
            del st.session_state.proses_checkout # Hapus data temporary biar bersih
            st.success("Pembayaran Berhasil Diterima! Kamar aman dipesan. Sisa tagihan (jika ada) akan dilunasi saat check-out.")
            st.rerun()

# --- 6. CEK DETAIL & CHECK-OUT MANDIRI ---
elif pilihan_menu == "🔍 Cek Detail & Check-Out":
    st.title("🔍 Menu Cek Data & Check-Out Mandiri (Akses Tamu)")
    st.write("Silakan masukkan salah satu data identitas booking Anda untuk memuat rincian billing kamar.")
    
    input_pencarian = st.text_input("Masukkan Nomor Kamar / Nama Tamu / ID Booking Anda:", placeholder="Contoh: 102 atau Budi Santoso atau RSV-102202").strip()
    
    if input_pencarian:
        # Cari data tamu di log reservasi aktif berdasarkan keyword inputan
        tamu = next((d for d in st.session_state.reservasi_log if 
                     d["kamar"] == input_pencarian or 
                     input_pencarian.lower() in d["nama"].lower() or 
                     d["id"] == input_pencarian), None)
        
        if tamu:
            sisa_bayar_kamar = tamu["total_biaya"] - tamu["sudah_dibayar"]
            grand_total_checkout = sisa_bayar_kamar + tamu["food_charge"]
            
            st.markdown(f"""
            <div class="card">
                <h4>🧾 ID Booking: {tamu['id']}</h4>
                <p>👤 <b>Nama Tamu:</b> {tamu['nama']}<br>
                💰 <b>Total Tarif Kamar:</b> Rp {int(tamu['total_biaya']):,}<br>
                💳 <b>Sudah Dibayar (DP/Lunas):</b> Rp {int(tamu['sudah_dibayar']):,}</p>
                <hr>
                <h4><b>📋 Rincian Pelunasan Akhir:</b></h4>
            </div>
            """, unsafe_allow_html=True)

            # Struk pelunasan yang sangat jelas untuk tamu
            struk_pelunasan = f"""
    ================================================
            STRUK PELUNASAN & CHECK-OUT
    ================================================
    Sisa Kamar    : Rp {int(sisa_bayar_kamar):,}
    Tagihan Makan : Rp {int(tamu['food_charge']):,}
    ------------------------------------------------
    TOTAL HARUS DIBAYAR SEKARANG: Rp {int(grand_total_checkout):,}
    ================================================
            Terima Kasih Atas Kunjungan Anda!
    """
            st.code(struk_pelunasan, language="text")
            
            # Tombol eksekusi check-out, balikin kamar jadi ijo (Tersedia) dan pindahin data ke arsip histori
            if st.button(f"Konfirmasi Pelunasan & Proses Check-Out Selesai", type="primary"):
                for k in st.session_state.kamar_data:
                    if k["No Kamar"] == tamu["kamar"]:
                        k["Status"] = "🟩 Tersedia"
                
                st.session_state.histori_transaksi.append({
                    "id": tamu["id"], "nama": tamu["nama"], "kamar": tamu["kamar"], "tipe": tamu["tipe"],
                    "grand_total": tamu["total_biaya"] + tamu["food_charge"], "status": "✅ Selesai (Check-Out & Lunas)"
                })
                
                st.session_state.reservasi_log.remove(tamu) # Hapus dari daftar tamu aktif
                st.success("Proses Pelunasan Kamar & Check-Out Berhasil! Kamar Anda sudah siap dipesan kembali.")
                st.rerun()
        else:
            st.error("Data reservasi aktif dengan keyword tersebut tidak ditemukan di sistem kami.")

# --- 7. HISTORI & PEMBATALAN SAYA ---
elif pilihan_menu == "📜 Histori & Pembatalan":
    st.title("📜 Menu Riwayat & Pembatalan Mandiri Tamu")
    tab_riwayat, tab_batal = st.tabs(["Arsip Histori Menginap", "Ajukan Pembatalan Kamar"])
    
    with tab_riwayat:
        st.subheader("📋 Buku Riwayat Selesai")
        cari_nama = st.text_input("Ketik nama Anda / No Kamar / ID Booking untuk mencari riwayat arsip pesanan lama:")
        if cari_nama:
            df_histori = pd.DataFrame(st.session_state.histori_transaksi)
            if not df_histori.empty:
                # Filter data tabel pake pandas biar pencariannya cepet dan akurat
                hasil_cari = df_histori[
                    df_histori['nama'].str.lower().str.contains(cari_nama.lower()) | 
                    df_histori['kamar'].astype(str).str.contains(cari_nama) | 
                    df_histori['id'].str.lower().str.contains(cari_nama.lower())
                ]
                if not hasil_cari.empty:
                    st.dataframe(hasil_cari, use_container_width=True)
                else:
                    st.info("Tidak ada riwayat menginap yang cocok.")
            else:
                st.info("Tidak ada riwayat menginap atas nama tersebut.")
        else:
            if st.session_state.histori_transaksi:
                st.dataframe(pd.DataFrame(st.session_state.histori_transaksi), use_container_width=True)

    with tab_batal:
        st.subheader("❌ Ajukan Pembatalan Kamar Mandiri")
        input_batal = st.text_input("Masukkan ID Booking / Nama Tamu / No Kamar Kamu untuk Mengajukan Pembatalan:")
        
        if input_batal:
            rsv = next((d for d in st.session_state.reservasi_log if 
                         d["id"] == input_batal or 
                         input_batal.lower() in d["nama"].lower() or 
                         d["kamar"] == input_batal), None)
                         
            if rsv:
                st.warning(f"Apakah Anda benar-benar yakin ingin membatalkan pesanan Kamar No. {rsv['kamar']}?")
                if st.button("Ya, Batalkan Pesanan Saja"):
                    for k in st.session_state.kamar_data:
                        if k["No Kamar"] == rsv["kamar"]: 
                            k["Status"] = "🟩 Tersedia" # Kosongkan status kamar lagi
                    
                    st.session_state.log_pembatalan.append({
                        "id": rsv["id"], "nama": rsv["nama"], "kamar": rsv["kamar"], "waktu_batal": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.session_state.reservasi_log.remove(rsv)
                    st.success("Pembatalan Sukses! Kamar otomatis dilepas kembali.")
                    st.rerun()
            else:
                st.error("Data booking aktif tidak ditemukan.")

# --- 8. ROOM SERVICE: PESAN MAKANAN ---
elif pilihan_menu == "🍽️ Pesan Makanan":
    st.title("🍽️ Room Service Kuliner - Kirim Ke Kamar")
    st.subheader("Verifikasi Hunian Kamar")
    input_verifikasi = st.text_input("Konfirmasi Nomor Kamar / Nama Tamu / ID Booking Anda Saat Ini:")
    
    if not input_verifikasi:
        st.info("Silakan konfirmasi identitas menginap kamu dulu di atas untuk memesan makanan.")
        st.stop()
        
    tamu_menginap = next((t for t in st.session_state.reservasi_log if 
                          t["kamar"] == input_verifikasi or 
                          input_verifikasi.lower() in t["nama"].lower() or 
                          t["id"] == input_verifikasi), None)
    
    if not tamu_menginap:
        st.error("Data hunian kamar tidak ditemukan.")
        st.stop()
        
    no_kmr = tamu_menginap["kamar"]
    st.success(f"Terverifikasi! Kamar No. {no_kmr} atas nama Kak **{tamu_menginap['nama']}** siap memesan hidangan.")
    st.write("### Pilih Menu Makanan Di Bawah:")
    
    total_order = 0
    items_dipesan = []
    
    # Loop dinamis buat nampilin form input jumlah (quantity) untuk tiap menu makanan
    for menu, harga in MENU_MAKANAN.items():
        qty = st.number_input(f"{menu} (Rp {harga:,})", min_value=0, step=1, key=f"food_{menu}")
        if qty > 0:
            total_order += (qty * harga)
            items_dipesan.append({"item": menu, "qty": qty, "subtotal": qty * harga})
            
    st.markdown(f"### Total Belanjaan Kuliner Baru: **Rp {total_order:,}**")
    
    if st.button("Pesan Sekarang & Kirim Ke Dapur 🛒"):
        if total_order > 0:
            # Cek apakah kamar tersebut udah punya orderan makanan aktif yang belum dibayar sebelumnya
            kamar_exist = next((m for m in st.session_state.makanan_log if m["kamar"] == no_kmr and m["status"] == "Belum Bayar"), None)
            
            if kamar_exist:
                # Kalau udah ada, gabungin atau tambahin item baru ke list yang lama
                for item_baru in items_dipesan:
                    idx_makanan = next((idx for idx, s in enumerate(kamar_exist["pesanan_detail"]) if s["item"] == item_baru["item"]), -1)
                    if idx_makanan != -1:
                        kamar_exist["pesanan_detail"][idx_makanan]["qty"] += item_baru["qty"]
                        kamar_exist["pesanan_detail"][idx_makanan]["subtotal"] += item_baru["subtotal"]
                    else:
                        kamar_exist["pesanan_detail"].append(item_baru)
                kamar_exist["total"] = sum(x["subtotal"] for x in kamar_exist["pesanan_detail"])
                st.success(f"Pesanan tambahan berhasil masuk ke list Kamar {no_kmr}!")
            else:
                # Kalau bener-bener baru pesan, buat lembaran log baru di dapur
                st.session_state.makanan_log.append({
                    "id_order": f"FS-{datetime.now().strftime('%M%S')}",
                    "kamar": no_kmr, "pesanan_detail": items_dipesan, "total": total_order, "status": "Belum Bayar"
                })
                st.success("Pesanan dikirim! Chef kami bakal langsung masak pesananmu.")
        else:
            st.warning("Pilih dulu makanannya dong, porsi tidak boleh kosong.")

# --- 9. ROOM SERVICE: BAYAR FOOD SERVICE ---
elif pilihan_menu == "💳 Bayar Room Service":
    st.title("💳 Kasir Tagihan Room Service Kuliner Mandiri")
    input_kasir = st.text_input("Input Nomor Kamar / Nama Tamu / ID Booking Kamu untuk Mengecek Bill Makanan:")
    if not input_kasir:
        st.info("Masukkan identitas Anda untuk memuat tagihan hidangan makanan.")
        st.stop()
        
    tamu_terkait = next((t for t in st.session_state.reservasi_log if 
                         t["kamar"] == input_kasir or 
                         input_kasir.lower() in t["nama"].lower() or 
                         t["id"] == input_kasir), None)
                         
    kamar_tamu_input = tamu_terkait["kamar"] if tamu_terkait else input_kasir
    order = next((m for m in st.session_state.makanan_log if m["kamar"] == kamar_tamu_input and m["status"] == "Belum Bayar"), None)
    
    if not order:
        st.success("Mantap! Semua tagihan makanan untuk kamar ini sudah bersih / lunas semua.")
    else:
        with st.container():
            st.markdown(f'<div class="card"><h4>🛎️ Bill Room Service Kamar No: {order["kamar"]}</h4>', unsafe_allow_html=True)
            st.write("**Rincian Pesanan Kuliner:**")
            for item in order["pesanan_detail"]:
                st.write(f"- {item['item']} ({item['qty']} Porsi) — Rp {item['subtotal']:,}")
                
            st.markdown(f"Total Yang Harus Dibayar: **Rp {order['total']:,}**")
            pilihan_metode = st.selectbox("Pilih Jenis Pembayaran Kuliner", ["Room Charge (Masuk Bill Kamar Utama)", "GoPay", "OVO", "Dana", "Debit Card"])
            
            if st.button(f"Proses & Cetak Struk Kamar {order['kamar']}"):
                # Opsi Room Charge: Biaya makanan dimasukin ke tagihan kamar utama biar dibayar pas checkout bareng sisa DP
                if pilihan_metode == "Room Charge (Masuk Bill Kamar Utama)":
                    tamu_aktif = next((d for d in st.session_state.reservasi_log if d["kamar"] == order["kamar"]), None)
                    if tamu_aktif:
                        tamu_aktif["food_charge"] += order["total"] 
                        order["status"] = "Selesai PAID (Masuk Bill Kamar)"
                        st.success("Sukses! Biaya makanan dimasukkan ke billing kamar utama.")
                    else:
                        st.error("Gagal menyambungkan ke billing kamar utama.")
                else:
                    order["status"] = "Selesai PAID"
                    st.success(f"Pembayaran kuliner sukses terverifikasi!")
                st.rerun()

# --- 10. PENILAIAN HOTEL ---
elif pilihan_menu == "⭐ Ulasan Kepuasan":
    st.title("⭐ Kotak Kepuasan & Review Tamu")
    # Form input ulasan kepuasan pelanggan/tamu hotel biar ada interaksi feedback
    with st.form("form_ulasan"):
        nama_tamu = st.text_input("Nama Kamu / No Kamar")
        skor_rating = st.slider("Kasih Rating Bintang Berapa? (1 - 5)", 1, 5, 5)
        komentar_tamu = st.text_area("Tulis Kesan Pesan Selama Liburan Di Sini")
        
        if st.form_submit_button("Kirim Review"):
            if nama_tamu and komentar_tamu:
                st.session_state.ulasan_log.append({
                    "nama": nama_tamu, "rating": skor_rating, "komentar": komentar_tamu
                })
                st.success("Makasih banyak ya ulasannya!")
                st.rerun()
            else:
                st.error("Isi dulu review-nya.")
                
    st.subheader("Semua Kumpulan Review Tamu")
    st.dataframe(pd.DataFrame(st.session_state.ulasan_log), use_container_width=True)

# --- 11. PUSAT BANTUAN ---
elif pilihan_menu == "❓ Pusat Bantuan":
    st.title("🛟 FAQ - Pusat Bantuan Informasi")
    # Pertanyaan populer seputar kebijakan hotel yang dikemas rapi pakai fitur expander Streamlit
    with st.expander("⏱️ Jam Berapa Batas Waktu Check-In & Check-Out Standard?"):
        st.write("Masuk kamar jam 14:00 WIB yaa, kalau keluar maksimal jam 12:00 WIB.")
    with st.expander("💳 Bisa Bayar Pake QRIS Atau E-Wallet Gak?"):
        st.write("Bisa bgt! Kita nerima Dana, Gopay, Ovo, ShopeePay, sama Transfer VA Bank.")

# --- 12. KONTAK LAYANAN SERVICE ---
elif pilihan_menu == "📞 Kontak Layanan Service":
    st.title("📞 Kontak Hubung & Layanan Fast Respon")
    # Informasi kontak darurat hotel buat kenyamanan dan rasa aman tamu selama menetap
    st.markdown("""
    <div class="card">
        <h3>Layanan Operator Resepsionis (24 Jam Nonstop)</h3>
        <p>Hubungi kontak di bawah kalau ada masalah darurat di kamar atau butuh bantuan teknisi.</p>
        <ul>
            <li><b>Telpon Kamar:</b> Pencet angka 0 langsung ke resepsionis</li>
            <li><b>WhatsApp Chat:</b> 0812-3456-7890</li>
            <li><b>Email Support:</b> care@denarahotel.com</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)