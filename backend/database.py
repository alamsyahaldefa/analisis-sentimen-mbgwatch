"""Lapisan basis data SQLite.

Ada DUA basis data terpisah dengan skema tabel `artikel` yang sama:
- DB fase 1 (`DB_PATH`, alias `main`)      : hasil scraping berlabel dari CSV;
- DB upload (`DB_UPLOAD_PATH`, alias `up`) : artikel yang diunggah admin lewat
  fitur upload (demo pengganti scraping), diprediksi model saat masuk.

Keduanya di-ATTACH pada satu koneksi sehingga kueri portal/dashboard dapat
menggabungkannya (UNION ALL) tanpa mencampur penyimpanannya.

Bertanggung jawab atas:
- pembuatan tabel `artikel` di kedua DB,
- seeding data fase 1 dari `mbg_berlabel.csv` (hanya bila tabel masih kosong),
- penyimpanan artikel upload + CRUD sentimen (update/delete) oleh admin,
- kueri artikel gabungan dengan filter + paginasi,
- agregasi statistik (distribusi sentimen, tren bulanan, daftar portal).
"""

import os
import sqlite3

import pandas as pd

from config import (CSV_PATH, DB_PATH, DB_UPLOAD_PATH, KATEGORI,
                    KATEGORI_DEFAULT, KATEGORI_KEYWORDS, KELAS)

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


_DDL_ARTIKEL = """
    CREATE TABLE IF NOT EXISTS {tabel} (
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

_KOLOM = ("id, portal, tanggal_terbit, url, judul, teks, sentimen, "
          "confidence, kategori")

# Subkueri gabungan kedua DB; tiap baris membawa kolom `sumber` agar frontend
# tahu artikel berasal dari dataset fase 1 atau upload admin.
_GABUNGAN = (f"(SELECT {_KOLOM}, 'dataset' AS sumber FROM main.artikel "
             f"UNION ALL SELECT {_KOLOM}, 'upload' AS sumber FROM up.artikel)")

# Nama tabel fisik per nilai `sumber` (untuk operasi tulis/CRUD).
_TABEL_SUMBER = {"dataset": "main.artikel", "upload": "up.artikel"}

# Portal yang tautannya mengarah ke HALAMAN TAG portal (bukan artikel asli),
# mis. Liputan6 ("...Kabar Terbaru Terkini | Liputan6.com"). Artikel dari
# portal ini diberi "tanggal semu" = tanggal tengah daftar pada tampilan
# default, sehingga terselip di tengah dan tidak muncul di halaman depan.
# Bisa ditimpa/dimatikan lewat env MBG_PORTAL_SELIP (dipisah koma; kosongkan
# untuk menonaktifkan penyelipan).
_PORTAL_SELIP = [p.strip() for p in
                 os.environ.get("MBG_PORTAL_SELIP", "Liputan6").split(",")
                 if p.strip()]


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Attach DB upload (file terpisah) + pastikan tabel di kedua DB ada.
    conn.execute("ATTACH DATABASE ? AS up", (DB_UPLOAD_PATH,))
    conn.execute(_DDL_ARTIKEL.format(tabel="main.artikel"))
    conn.execute(_DDL_ARTIKEL.format(tabel="up.artikel"))
    return conn


def init_db():
    """Buat tabel `artikel` di kedua DB bila belum ada."""
    get_conn().close()


def hitung_baris():
    """Jumlah baris DB fase 1 (untuk cek perlunya seeding)."""
    conn = get_conn()
    n = conn.execute("SELECT COUNT(*) FROM main.artikel").fetchone()[0]
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
        INSERT OR IGNORE INTO main.artikel
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


def _tanggal_tengah(conn):
    """Tanggal pada posisi tengah daftar seluruh artikel (urut terbaru →
    terlama). Dipakai sebagai kunci semu penempatan artikel _PORTAL_SELIP.
    Dihitung atas seluruh set (bukan hasil terfilter) agar konsisten."""
    total = conn.execute(
        f"SELECT COUNT(*) FROM {_GABUNGAN} "
        "WHERE tanggal_terbit IS NOT NULL AND tanggal_terbit != ''"
    ).fetchone()[0]
    if total == 0:
        return None
    row = conn.execute(
        f"SELECT tanggal_terbit FROM {_GABUNGAN} "
        "WHERE tanggal_terbit IS NOT NULL AND tanggal_terbit != '' "
        "ORDER BY tanggal_terbit DESC LIMIT 1 OFFSET ?",
        (total // 2,),
    ).fetchone()
    return row[0] if row else None


def _urutan_default(conn):
    """Klausa ORDER BY tampilan default. Artikel dari _PORTAL_SELIP diberi
    tanggal semu = tanggal tengah, sehingga terselip di tengah daftar (tidak
    di halaman depan). Return (klausa_sql, params)."""
    tgl_tengah = _tanggal_tengah(conn)
    if not _PORTAL_SELIP or tgl_tengah is None:
        return "ORDER BY tanggal_terbit DESC, id", []
    ph = ",".join("?" * len(_PORTAL_SELIP))
    klausa = (
        f"ORDER BY CASE WHEN portal IN ({ph}) THEN ? "
        "ELSE tanggal_terbit END DESC, tanggal_terbit DESC, id"
    )
    return klausa, list(_PORTAL_SELIP) + [tgl_tengah]


def query_artikel(portal=None, sentimen=None, cari=None, start=None, end=None,
                  kategori=None, page=1, limit=10):
    where, params = _bangun_where(portal, sentimen, cari, start, end, kategori)

    conn = get_conn()
    total = conn.execute(
        f"SELECT COUNT(*) FROM {_GABUNGAN}{where}", params
    ).fetchone()[0]

    page = max(1, int(page))
    limit = max(1, int(limit))
    offset = (page - 1) * limit

    order_sql, order_params = _urutan_default(conn)
    rows = conn.execute(
        f"""
        SELECT {_KOLOM}, sumber
        FROM {_GABUNGAN}{where}
        {order_sql}
        LIMIT ? OFFSET ?
        """,
        params + order_params + [limit, offset],
    ).fetchall()
    conn.close()

    data = [dict(r) for r in rows]
    return {"data": data, "total": total, "page": page, "limit": limit}


# ---------------------------------------------------------------------------
# Statistik
# ---------------------------------------------------------------------------

def get_statistik():
    conn = get_conn()

    total = conn.execute(f"SELECT COUNT(*) FROM {_GABUNGAN}").fetchone()[0]

    # Jumlah per kelas (untuk donut)
    per_kelas = {k: 0 for k in KELAS}
    for row in conn.execute(
        f"SELECT sentimen, COUNT(*) AS n FROM {_GABUNGAN} GROUP BY sentimen"
    ):
        if row["sentimen"] in per_kelas:
            per_kelas[row["sentimen"]] = row["n"]

    # Tren bulanan: jumlah tiap sentimen per bulan (YYYY-MM)
    bulan_map = {}
    for row in conn.execute(
        f"""
        SELECT substr(tanggal_terbit, 1, 7) AS bulan, sentimen, COUNT(*) AS n
        FROM {_GABUNGAN}
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
        f"SELECT DISTINCT portal FROM {_GABUNGAN} "
        "WHERE portal IS NOT NULL ORDER BY portal"
    )]

    # Jumlah artikel per kategori topik (untuk chip portal user)
    per_kategori = {}
    for kat in KATEGORI:
        n = conn.execute(
            f"SELECT COUNT(*) FROM {_GABUNGAN} WHERE ('|' || kategori || '|') LIKE ?",
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


# ---------------------------------------------------------------------------
# Artikel upload (DB terpisah) + CRUD sentimen oleh admin
# ---------------------------------------------------------------------------

def insert_artikel_upload(rows):
    """Simpan artikel hasil upload (sudah berlabel model) ke DB upload."""
    conn = get_conn()
    conn.executemany(
        """
        INSERT OR REPLACE INTO up.artikel
            (id, portal, tanggal_terbit, url, judul, teks, sentimen,
             confidence, kategori)
        VALUES (:id, :portal, :tanggal_terbit, :url, :judul, :teks, :sentimen,
                :confidence, :kategori)
        """,
        rows,
    )
    conn.commit()
    conn.close()


def _cari_artikel(conn, artikel_id, sumber=None):
    """Cari artikel di kedua DB. Return (sumber, dict baris) atau (None, None).
    Bila `sumber` diberikan, hanya DB itu yang diperiksa."""
    kandidat = [sumber] if sumber in _TABEL_SUMBER else ["upload", "dataset"]
    for s in kandidat:
        row = conn.execute(
            f"SELECT {_KOLOM} FROM {_TABEL_SUMBER[s]} WHERE id = ?",
            (artikel_id,),
        ).fetchone()
        if row:
            return s, dict(row)
    return None, None


def update_sentimen(artikel_id, sentimen, sumber=None):
    """Ganti label sentimen sebuah artikel (koreksi manual admin).
    Return dict artikel terbaru, atau None bila id tidak ditemukan."""
    conn = get_conn()
    s, row = _cari_artikel(conn, artikel_id, sumber)
    if s is None:
        conn.close()
        return None
    conn.execute(
        f"UPDATE {_TABEL_SUMBER[s]} SET sentimen = ? WHERE id = ?",
        (sentimen, artikel_id),
    )
    conn.commit()
    conn.close()
    row["sentimen"] = sentimen
    row["sumber"] = s
    return row


def hapus_artikel(artikel_id, sumber=None):
    """Hapus artikel. Return True bila ada baris yang terhapus."""
    conn = get_conn()
    s, _ = _cari_artikel(conn, artikel_id, sumber)
    if s is None:
        conn.close()
        return False
    conn.execute(f"DELETE FROM {_TABEL_SUMBER[s]} WHERE id = ?", (artikel_id,))
    conn.commit()
    conn.close()
    return True
