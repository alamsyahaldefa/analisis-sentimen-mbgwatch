"""Lapisan basis data SQLite.

Bertanggung jawab atas:
- pembuatan tabel `artikel`,
- seeding data dari `mbg_berlabel.csv` (hanya bila tabel masih kosong),
- kueri artikel dengan filter + paginasi,
- agregasi statistik (distribusi sentimen, tren bulanan, daftar portal).
"""

import os
import sqlite3

import pandas as pd

from config import (CSV_PATH, DB_PATH, KATEGORI, KATEGORI_DEFAULT,
                    KATEGORI_KEYWORDS, KELAS)

# Kolom CSV -> kolom tabel
#   clean_text -> teks ; label -> sentimen
CSV_COLUMNS = ["id", "portal", "tanggal_terbit", "url", "judul",
               "clean_text", "label", "confidence"]


def klasifikasi_kategori(judul, teks):
    """Tentukan kategori topik dari kata kunci pada judul + teks.
    Mengembalikan string kategori dipisah '|' (bisa lebih dari satu);
    bila tak ada yang cocok -> KATEGORI_DEFAULT."""
    konten = f"{judul or ''} {teks or ''}".lower()
    cocok = [kat for kat, kws in KATEGORI_KEYWORDS.items()
             if any(kw in konten for kw in kws)]
    if not cocok:
        return KATEGORI_DEFAULT
    # Selalu sertakan "Berita Umum MBG" sebagai tag umum di akhir
    if KATEGORI_DEFAULT not in cocok:
        cocok.append(KATEGORI_DEFAULT)
    # Urutkan sesuai urutan KATEGORI agar konsisten
    cocok = [k for k in KATEGORI if k in cocok]
    return "|".join(cocok)


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Buat tabel `artikel` bila belum ada."""
    conn = get_conn()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS artikel (
            id              TEXT PRIMARY KEY,
            portal          TEXT,
            tanggal_terbit  TEXT,
            url             TEXT,
            judul           TEXT,
            teks            TEXT,
            sentimen        TEXT,
            confidence      REAL,
            kategori        TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def hitung_baris():
    conn = get_conn()
    n = conn.execute("SELECT COUNT(*) FROM artikel").fetchone()[0]
    conn.close()
    return n


def seed_if_empty():
    """Isi tabel dari CSV bila masih kosong.

    Mengembalikan jumlah baris ter-seed. Memunculkan FileNotFoundError dengan
    pesan jelas bila CSV tidak ditemukan, agar dapat ditangani pemanggil.
    """
    init_db()
    if hitung_baris() > 0:
        return 0  # sudah ada data, tidak perlu seed ulang

    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            f"File label tidak ditemukan: {CSV_PATH}\n"
            "Letakkan 'mbg_berlabel.csv' di root proyek, lalu jalankan ulang."
        )

    df = pd.read_csv(CSV_PATH)
    kurang = [c for c in CSV_COLUMNS if c not in df.columns]
    if kurang:
        raise ValueError(
            f"Kolom berikut tidak ada di CSV: {kurang}. "
            f"Kolom yang diperlukan: {CSV_COLUMNS}"
        )

    df = df[CSV_COLUMNS].rename(columns={"clean_text": "teks", "label": "sentimen"})
    df["confidence"] = pd.to_numeric(df["confidence"], errors="coerce")
    # Turunkan kategori topik dari judul + teks (dataset tak punya kolomnya)
    df["kategori"] = df.apply(
        lambda r: klasifikasi_kategori(r["judul"], r["teks"]), axis=1
    )

    conn = get_conn()
    conn.executemany(
        """
        INSERT OR IGNORE INTO artikel
            (id, portal, tanggal_terbit, url, judul, teks, sentimen, confidence, kategori)
        VALUES (:id, :portal, :tanggal_terbit, :url, :judul, :teks, :sentimen,
                :confidence, :kategori)
        """,
        df.to_dict(orient="records"),
    )
    conn.commit()
    n = hitung_baris()
    conn.close()
    return n


# ---------------------------------------------------------------------------
# Kueri artikel dengan filter + paginasi
# ---------------------------------------------------------------------------

def _bangun_where(portal=None, sentimen=None, cari=None, start=None, end=None,
                  kategori=None):
    klausa, params = [], []
    if portal:
        klausa.append("portal = ?")
        params.append(portal)
    if sentimen:
        klausa.append("sentimen = ?")
        params.append(sentimen)
    if kategori:
        # kategori disimpan sebagai daftar dipisah '|'
        klausa.append("('|' || kategori || '|') LIKE ?")
        params.append(f"%|{kategori}|%")
    if cari:
        klausa.append("LOWER(judul) LIKE ?")
        params.append(f"%{cari.lower()}%")
    if start:
        klausa.append("tanggal_terbit >= ?")
        params.append(start)
    if end:
        klausa.append("tanggal_terbit <= ?")
        params.append(end)
    where = (" WHERE " + " AND ".join(klausa)) if klausa else ""
    return where, params


def query_artikel(portal=None, sentimen=None, cari=None, start=None, end=None,
                  kategori=None, page=1, limit=10):
    where, params = _bangun_where(portal, sentimen, cari, start, end, kategori)

    conn = get_conn()
    total = conn.execute(f"SELECT COUNT(*) FROM artikel{where}", params).fetchone()[0]

    page = max(1, int(page))
    limit = max(1, int(limit))
    offset = (page - 1) * limit

    rows = conn.execute(
        f"""
        SELECT id, portal, tanggal_terbit, url, judul, teks, sentimen, confidence,
               kategori
        FROM artikel{where}
        ORDER BY tanggal_terbit DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    ).fetchall()
    conn.close()

    data = [dict(r) for r in rows]
    return {"data": data, "total": total, "page": page, "limit": limit}


# ---------------------------------------------------------------------------
# Statistik
# ---------------------------------------------------------------------------

def get_statistik():
    conn = get_conn()

    total = conn.execute("SELECT COUNT(*) FROM artikel").fetchone()[0]

    # Jumlah per kelas (untuk donut)
    per_kelas = {k: 0 for k in KELAS}
    for row in conn.execute(
        "SELECT sentimen, COUNT(*) AS n FROM artikel GROUP BY sentimen"
    ):
        if row["sentimen"] in per_kelas:
            per_kelas[row["sentimen"]] = row["n"]

    # Tren bulanan: jumlah tiap sentimen per bulan (YYYY-MM)
    bulan_map = {}
    for row in conn.execute(
        """
        SELECT substr(tanggal_terbit, 1, 7) AS bulan, sentimen, COUNT(*) AS n
        FROM artikel
        WHERE tanggal_terbit IS NOT NULL AND tanggal_terbit != ''
        GROUP BY bulan, sentimen
        ORDER BY bulan
        """
    ):
        b = row["bulan"]
        if b not in bulan_map:
            bulan_map[b] = {"bulan": b, "negatif": 0, "netral": 0, "positif": 0}
        if row["sentimen"] in KELAS:
            bulan_map[b][row["sentimen"]] = row["n"]
    tren_bulanan = list(bulan_map.values())

    # Daftar portal unik (untuk dropdown)
    portals = [r["portal"] for r in conn.execute(
        "SELECT DISTINCT portal FROM artikel WHERE portal IS NOT NULL ORDER BY portal"
    )]

    # Jumlah artikel per kategori topik (untuk chip portal user)
    per_kategori = {}
    for kat in KATEGORI:
        n = conn.execute(
            "SELECT COUNT(*) FROM artikel WHERE ('|' || kategori || '|') LIKE ?",
            (f"%|{kat}|%",),
        ).fetchone()[0]
        per_kategori[kat] = n

    conn.close()
    return {
        "total": total,
        "per_kelas": per_kelas,
        "tren_bulanan": tren_bulanan,
        "portals": portals,
        "per_kategori": per_kategori,
    }
