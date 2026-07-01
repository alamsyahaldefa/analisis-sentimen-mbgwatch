"""API FastAPI — MBG Watch (Analisis Sentimen Berita MBG).

Endpoint:
- GET  /api/artikel      : daftar artikel berlabel (filter + paginasi)
- GET  /api/statistik    : agregasi untuk dashboard (donut, tren, dropdown)
- POST /api/prediksi     : prediksi sentimen teks baru via model IndoBERT
- POST /api/prediksi-url : scrape artikel dari URL lalu prediksi sentimennya

Jalankan:  uvicorn main:app --reload
"""

from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

import database
import extractor
import model
from config import CORS_ORIGINS
from schemas import (ArtikelResponse, PrediksiRequest, PrediksiResponse,
                     PrediksiUrlRequest, PrediksiUrlResponse, StatistikResponse)


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
