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
    col_m3.metric("Total Customer", total_cust
