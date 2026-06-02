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
    st.markdown(f"<div style='text-align: right; padding-top: 20px;'>🔑 Staf: <b>{st.session}
