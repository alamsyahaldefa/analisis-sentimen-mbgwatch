"""API FastAPI — MBG Watch (Analisis Sentimen Berita MBG).

Endpoint:
- GET    /api/artikel        : daftar artikel gabungan (fase 1 + upload)
- GET    /api/statistik      : agregasi untuk dashboard (donut, tren, dropdown)
- POST   /api/prediksi       : prediksi sentimen teks baru via model IndoBERT
- POST   /api/prediksi-url   : scrape artikel dari URL lalu prediksi sentimennya
- POST   /api/artikel-upload : upload beberapa artikel (pengganti scraping),
                               diprediksi model lalu disimpan ke DB upload
- PATCH  /api/artikel/{id}   : admin mengganti label sentimen sebuah artikel
- DELETE /api/artikel/{id}   : admin menghapus sebuah artikel

Jalankan:  uvicorn main:app --reload
"""

from contextlib import asynccontextmanager
from datetime import date
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

import database
import extractor
import model
from config import CORS_ORIGINS, KELAS
from schemas import (Artikel, ArtikelResponse, PrediksiRequest,
                     PrediksiResponse, PrediksiUrlRequest, PrediksiUrlResponse,
                     StatistikResponse, UpdateSentimenRequest,
                     UploadArtikelRequest, UploadArtikelResponse)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: seed DB dari CSV + muat model (keduanya toleran terhadap
    file yang belum tersedia — server tetap bisa start)."""
    # 1. Seed database
    try:
        n = database.seed_if_empty()
        if n > 0:
            print(f"[startup] Database di-seed: {n} artikel dimuat dari CSV.")
        else:
            print(f"[startup] Database sudah berisi {database.hitung_baris()} artikel.")
    except (FileNotFoundError, ValueError) as e:
        print("[startup][PERINGATAN] Gagal seed database:")
        print(f"  {e}")
        print("  -> Endpoint /api/artikel & /api/statistik akan mengembalikan data kosong.")
        database.init_db()  # tetap siapkan tabel kosong

    # 2. Muat model
    if model.load_model():
        print("[startup] Model IndoBERT berhasil dimuat.")
    else:
        print("[startup][PERINGATAN] Model belum dapat dimuat:")
        print(f"  {model.pesan_error()}")
        print("  -> Endpoint /api/prediksi akan mengembalikan error 503 sampai model tersedia.")

    yield


app = FastAPI(title="MBG Watch API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,  # API tanpa cookie; kompatibel dengan origin "*"
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"app": "MBG Watch API", "status": "ok", "docs": "/docs"}


@app.get("/api/artikel", response_model=ArtikelResponse)
def get_artikel(
    portal: Optional[str] = None,
    sentimen: Optional[str] = None,
    kategori: Optional[str] = Query(None, description="Kategori topik (portal user)"),
    cari: Optional[str] = None,
    start: Optional[str] = Query(None, description="Tanggal mulai (YYYY-MM-DD)"),
    end: Optional[str] = Query(None, description="Tanggal akhir (YYYY-MM-DD)"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    return database.query_artikel(
        portal=portal, sentimen=sentimen, cari=cari,
        start=start, end=end, kategori=kategori, page=page, limit=limit,
    )


@app.get("/api/statistik", response_model=StatistikResponse)
def get_statistik():
    return database.get_statistik()


@app.post("/api/prediksi", response_model=PrediksiResponse)
def post_prediksi(req: PrediksiRequest):
    try:
        return model.predict(req.teks)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        # Model belum tersedia / gagal dimuat
        raise HTTPException(status_code=503, detail=str(e))


@app.post("/api/prediksi-url", response_model=PrediksiUrlResponse)
def post_prediksi_url(req: PrediksiUrlRequest):
    """Ekstrak artikel dari URL lalu prediksi sentimennya dengan model IndoBERT.

    Alur: unduh halaman -> ekstrak judul+isi+tanggal -> bentuk unit analisis
    (judul + lead, sama seperti pelatihan) -> prediksi.
    """
    try:
        artikel = extractor.ekstrak_artikel(req.url)
    except ValueError as e:
        # URL tidak valid / gagal diakses / isi tak terekstrak
        raise HTTPException(status_code=400, detail=str(e))

    try:
        hasil = model.predict(artikel["clean_text"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

    return {
        **hasil,
        "judul": artikel["judul"],
        "portal": artikel["portal"],
        "tanggal_terbit": artikel["tanggal_terbit"],
        "url": artikel["url"],
        "teks_dianalisis": artikel["clean_text"],
    }


@app.post("/api/artikel-upload", response_model=UploadArtikelResponse)
def post_artikel_upload(req: UploadArtikelRequest):
    """Upload beberapa artikel sekaligus (demo pengganti scraping).

    Tiap artikel dibentuk unit analisisnya (judul + lead, sama seperti
    pelatihan), diprediksi model IndoBERT, lalu disimpan ke DB upload —
    terpisah dari DB fase 1 — sehingga langsung tampil di portal publik.
    """
    berhasil, gagal, baris_baru = [], [], []
    for item in req.artikel:
        judul = (item.judul or "").strip()
        teks = (item.teks or "").strip()
        if not judul or not teks:
            gagal.append({"judul": judul or "(tanpa judul)",
                          "error": "Judul dan teks wajib diisi."})
            continue

        clean_text = extractor.bersihkan(judul) + ". " + extractor.ambil_lead(teks)
        try:
            hasil = model.predict(clean_text)
        except ValueError as e:
            gagal.append({"judul": judul, "error": str(e)})
            continue
        except RuntimeError as e:
            raise HTTPException(status_code=503, detail=str(e))

        baris = {
            "id": f"up-{uuid4().hex[:12]}",
            "portal": (item.portal or "").strip() or "Upload Admin",
            "tanggal_terbit": (item.tanggal_terbit or "").strip()[:10]
                or date.today().isoformat(),
            "url": (item.url or "").strip() or None,
            "judul": judul,
            "teks": teks,
            "sentimen": hasil["sentimen"],
            "confidence": hasil["confidence"],
            "kategori": database.klasifikasi_kategori(judul, teks),
        }
        baris_baru.append(baris)
        berhasil.append({**baris, "sumber": "upload"})

    if baris_baru:
        database.insert_artikel_upload(baris_baru)
    return {"berhasil": berhasil, "gagal": gagal}


@app.patch("/api/artikel/{artikel_id}", response_model=Artikel)
def patch_artikel(artikel_id: str, req: UpdateSentimenRequest,
                  sumber: Optional[str] = Query(None, description="dataset | upload")):
    """Admin mengganti label sentimen sebuah artikel (koreksi manual)."""
    sentimen = (req.sentimen or "").strip().lower()
    if sentimen not in KELAS:
        raise HTTPException(
            status_code=400,
            detail=f"Sentimen tidak valid. Pilihan: {', '.join(KELAS)}.",
        )
    row = database.update_sentimen(artikel_id, sentimen, sumber)
    if row is None:
        raise HTTPException(status_code=404, detail="Artikel tidak ditemukan.")
    return row


@app.delete("/api/artikel/{artikel_id}")
def delete_artikel(artikel_id: str,
                   sumber: Optional[str] = Query(None, description="dataset | upload")):
    """Admin menghapus sebuah artikel."""
    if not database.hapus_artikel(artikel_id, sumber):
        raise HTTPException(status_code=404, detail="Artikel tidak ditemukan.")
    return {"status": "terhapus", "id": artikel_id}
