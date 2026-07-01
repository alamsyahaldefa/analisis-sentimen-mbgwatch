"""Ekstraksi isi artikel dari URL berita untuk analisis sentimen on-demand.

Dipakai endpoint POST /api/prediksi-url: diberi sebuah URL berita, modul ini
mengunduh halaman, mengekstrak judul + isi + tanggal + portal, lalu membentuk
unit analisis `clean_text` (judul + 2 kalimat awal) — IDENTIK dengan praproses
Fase 2 — agar masukan model sama dengan saat pelatihan.

Strategi ekstraksi: trafilatura (bila tersedia) lebih dulu, lalu fallback ke
BeautifulSoup. Hanya butuh requests + beautifulsoup4 + lxml; trafilatura opsional.
"""

import re
import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

try:
    from dateutil import parser as _dateparser
    _HAS_DATEUTIL = True
except ImportError:
    _HAS_DATEUTIL = False

try:
    import trafilatura
    _HAS_TRAFILATURA = True
except ImportError:
    _HAS_TRAFILATURA = False


# ---------------------------------------------------------------- Konfigurasi
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 "
    "(MBG Watch - Analisis Sentimen)"
)
REQUEST_TIMEOUT = 20
MAX_RETRIES = 2
N_LEAD = 2  # unit analisis = judul + 2 kalimat awal (sesuai Fase 2)
MIN_ISI = 120  # ambang minimum panjang isi agar dianggap berhasil

# Pemetaan domain -> nama portal (selaras dengan korpus Fase 1).
PORTAL_DOMAIN = {
    "antaranews.com": "Antara",
    "detik.com": "Detik",
    "tempo.co": "Tempo",
    "liputan6.com": "Liputan6",
    "suara.com": "Suara",
    "republika.co.id": "Republika",
    "kompas.com": "Kompas",
    "cnnindonesia.com": "CNN Indonesia",
    "tribunnews.com": "Tribunnews",
    "kumparan.com": "Kumparan",
}


# ------------------------------------------------------------------ Utilitas
def _validasi_url(url):
    p = urlparse(url)
    if p.scheme not in ("http", "https") or not p.netloc:
        raise ValueError(
            "URL tidak valid. Masukkan tautan lengkap, mis. "
            "https://www.detik.com/..."
        )
    return url


def nama_portal(url):
    """Tebak nama portal dari domain; fallback ke host tanpa 'www.'."""
    host = urlparse(url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    for domain, nama in PORTAL_DOMAIN.items():
        if host == domain or host.endswith("." + domain):
            return nama
    return host or "Tidak diketahui"


def bersihkan(teks):
    """Pembersihan ringan: buang sisa tag HTML, URL, dan spasi berlebih."""
    t = str(teks)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"http\S+|www\.\S+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def ambil_lead(isi, n=N_LEAD):
    """Ambil n kalimat awal dari isi (lead) sebagai konteks ringkas."""
    isi = bersihkan(isi)
    kalimat = re.split(r"(?<=[.!?])\s+", isi)
    return " ".join(kalimat[:n]).strip()


def _parse_tanggal(nilai):
    if not nilai:
        return None
    if _HAS_DATEUTIL:
        try:
            dt = _dateparser.parse(str(nilai), fuzzy=True)
            return dt.date().isoformat() if dt else None
        except (ValueError, OverflowError, TypeError):
            return None
    return str(nilai)[:10] or None


def _fetch(url):
    """Unduh HTML dengan User-Agent wajar + retry sederhana."""
    headers = {"User-Agent": USER_AGENT, "Accept-Language": "id-ID,id;q=0.9,en;q=0.8"}
    last_err = "tidak diketahui"
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                return resp.text
            if resp.status_code in (401, 403, 429):
                raise ValueError(
                    f"Situs menolak permintaan (HTTP {resp.status_code}). "
                    "Portal ini mungkin memblokir akses otomatis."
                )
            last_err = f"server membalas HTTP {resp.status_code}"
        except requests.Timeout:
            last_err = "permintaan melebihi batas waktu"
            time.sleep(0.6 * attempt)
        except requests.ConnectionError:
            last_err = "tidak dapat terhubung ke server (periksa URL/koneksi)"
            time.sleep(0.6 * attempt)
        except requests.RequestException:
            last_err = "terjadi kesalahan saat mengakses URL"
            time.sleep(0.6 * attempt)
    raise ValueError(f"Gagal mengakses URL: {last_err}.")


# --------------------------------------------------------- Ekstraksi konten
def _ekstrak_trafilatura(html, url):
    if not _HAS_TRAFILATURA:
        return None
    try:
        import json
        raw = trafilatura.extract(
            html, url=url, output_format="json",
            with_metadata=True, favor_recall=True,
        )
        if not raw:
            return None
        data = json.loads(raw)
        return {
            "judul": (data.get("title") or "").strip(),
            "isi": (data.get("text") or "").strip(),
            "tanggal_terbit": _parse_tanggal(data.get("date")),
        }
    except Exception:
        return None


def _ekstrak_bs4(html):
    soup = BeautifulSoup(html, "lxml")

    # Judul: og:title -> <h1> -> <title>
    judul = ""
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        judul = og["content"].strip()
    if not judul:
        h1 = soup.find("h1")
        if h1:
            judul = h1.get_text(strip=True)
    if not judul and soup.title and soup.title.string:
        judul = soup.title.string.strip()

    # Tanggal: meta umum -> <time datetime>
    tanggal = None
    for prop in ("article:published_time", "og:article:published_time"):
        m = soup.find("meta", property=prop)
        if m and m.get("content"):
            tanggal = _parse_tanggal(m["content"]); break
    if not tanggal:
        m = soup.find("meta", attrs={"name": "publishdate"}) or \
            soup.find("meta", attrs={"name": "date"})
        if m and m.get("content"):
            tanggal = _parse_tanggal(m["content"])
    if not tanggal:
        t = soup.find("time")
        if t:
            tanggal = _parse_tanggal(t.get("datetime") or t.get_text(strip=True))

    # Isi: kumpulkan <p> dari <article>/<main>, fallback seluruh <p>.
    wadah = soup.find("article") or soup.find("main") or soup
    for buang in wadah.select("script, style, figure, figcaption, aside, nav, .baca-juga, .ads"):
        buang.decompose()
    paragraf = [p.get_text(" ", strip=True) for p in wadah.find_all("p")]
    isi = " ".join(p for p in paragraf if len(p) > 30).strip()

    return {"judul": judul, "isi": isi, "tanggal_terbit": tanggal}


def ekstrak_artikel(url):
    """Ekstrak artikel dari URL. Mengembalikan dict:
    {judul, isi, tanggal_terbit, portal, url, clean_text}.
    Memunculkan ValueError dengan pesan jelas bila gagal."""
    url = _validasi_url((url or "").strip())
    html = _fetch(url)

    hasil = _ekstrak_trafilatura(html, url)
    if not hasil or len(hasil.get("isi", "")) < MIN_ISI:
        bs = _ekstrak_bs4(html)
        # Pilih sumber dengan isi terpanjang; lengkapi judul/tanggal bila kosong.
        if not hasil or len(bs.get("isi", "")) > len(hasil.get("isi", "")):
            hasil = {
                "judul": hasil.get("judul") if hasil and hasil.get("judul") else bs["judul"],
                "isi": bs["isi"],
                "tanggal_terbit": (hasil.get("tanggal_terbit") if hasil else None) or bs["tanggal_terbit"],
            }

    judul = (hasil.get("judul") or "").strip()
    isi = (hasil.get("isi") or "").strip()
    if len(isi) < MIN_ISI:
        raise ValueError(
            "Isi artikel tidak dapat diekstrak dari URL ini "
            "(halaman mungkin dirender JavaScript atau bukan artikel berita)."
        )

    clean_text = bersihkan(judul) + ". " + ambil_lead(isi)
    clean_text = re.sub(r"\s+", " ", clean_text).strip()

    return {
        "judul": judul or "(tanpa judul)",
        "isi": isi,
        "tanggal_terbit": hasil.get("tanggal_terbit"),
        "portal": nama_portal(url),
        "url": url,
        "clean_text": clean_text,
    }
