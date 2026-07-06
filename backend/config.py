"""Konfigurasi path & konstanta backend (versi deploy — Hugging Face Spaces).

Pada folder demo ini, model dan CSV berada DI DALAM folder backend/ (self-
contained), agar backend dapat dijadikan satu repo Space Docker yang utuh.
Semua path dapat ditimpa lewat environment variable bila diperlukan.
"""

import os

# Direktori
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

# Lokasi bahan (default: di dalam backend/; bisa ditimpa via env var)
CSV_PATH = os.environ.get("MBG_CSV", os.path.join(BACKEND_DIR, "mbg_berlabel.csv"))
MODEL_DIR = os.environ.get("MBG_MODEL", os.path.join(BACKEND_DIR, "model_mbg_indobert"))
# DB SQLite ephemeral; di HF Spaces diarahkan ke /tmp lewat env MBG_DB (writable).
DB_PATH = os.environ.get("MBG_DB", os.path.join(BACKEND_DIR, "mbg.db"))
# DB terpisah untuk artikel hasil UPLOAD admin (demo pengganti scraping).
# Sengaja tidak dicampur dengan DB fase 1 di atas.
DB_UPLOAD_PATH = os.environ.get("MBG_DB_UPLOAD", os.path.join(BACKEND_DIR, "mbg_upload.db"))

# Inferensi
MAX_LENGTH = 128
# Pemetaan id -> label (sesuai config model: 0=negatif, 1=netral, 2=positif)
ID2LABEL = {0: "negatif", 1: "netral", 2: "positif"}
KELAS = ["negatif", "netral", "positif"]

# ---------------------------------------------------------------------------
# Kategori topik untuk PORTAL PUBLIK (POV user).
# Dataset tidak memiliki kolom kategori, jadi diturunkan dari kata kunci pada
# judul + teks. Satu artikel bisa punya >1 kategori; bila tak ada yang cocok,
# jatuh ke "Berita Umum MBG".
# Urutan list = urutan tampil chip di portal.
# ---------------------------------------------------------------------------
KATEGORI = [
    "Keracunan & Masalah Kesehatan",
    "Operasional Dapur",
    "Kualitas & Keamanan Pangan",
    "Kebijakan & Anggaran",
    "Implementasi Program",
    "Dampak Sosial & Ekonomi",
    "Berita Umum MBG",
]
KATEGORI_DEFAULT = "Berita Umum MBG"

# Kata kunci (lowercase) per kategori untuk klasifikasi topik sederhana.
KATEGORI_KEYWORDS = {
    "Keracunan & Masalah Kesehatan": [
        "keracunan", "diduga keracunan", "mual", "muntah", "pusing", "dilarikan",
        "puskesmas", "dirawat", "gejala", "stunting", "gizi buruk", "rokok",
    ],
    "Operasional Dapur": [
        "sppg", "dapur", "ipal", "slhs", "suspend", "ditangguhkan", "tangguhkan",
        "moratorium", "operasional", "higiene", "sanitasi", "verifikasi", "mitra",
    ],
    "Kualitas & Keamanan Pangan": [
        "telur dadar", "ayam potong", "potong ayam", "porsi", "lauk", "susu formula",
        "halal", "keamanan pangan", "standar mutu", "kualitas makanan",
        "kualitas menu", "gizi makanan", "ompreng",
    ],
    "Kebijakan & Anggaran": [
        "anggaran", "apbn", "triliun", "efisiensi", "fiskal", "pagu", "realisasi",
        "kebijakan", "target", "evaluasi", "audit", "tata kelola", "moratorium",
    ],
    "Implementasi Program": [
        "tinjau", "meninjau", "kunjungan", "resmikan", "diresmikan", "distribusi",
        "penerima manfaat", "beroperasi", "santap", "uji coba", "konsolidasi",
        "pelaksanaan", "sasaran", "3t", "3b",
    ],
    "Dampak Sosial & Ekonomi": [
        "ekonomi", "petani", "peternak", "lapangan kerja", "umkm", "serap",
        "harga telur", "kesejahteraan", "pasok", "tenaga kerja", "perekonomian",
    ],
}

# CORS — daftar origin frontend yang diizinkan (dipisah koma).
# Default "*" (izinkan semua) agar demo mudah; untuk produksi, set env
# FRONTEND_ORIGIN ke domain Vercel, mis. "https://mbgwatch.vercel.app".
_origins = os.environ.get("FRONTEND_ORIGIN", "*").strip()
CORS_ORIGINS = ["*"] if _origins == "*" else [o.strip() for o in _origins.split(",")]
