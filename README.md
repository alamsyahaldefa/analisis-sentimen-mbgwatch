# MBG Watch — Demo Sidang (Analisis Sentimen Berita MBG)

Clone ringan aplikasi **MBG Watch** untuk demo Sidang Proyek Akhir: berisi
**seluruh fitur** (portal publik + dashboard admin) tanpa berkas berat
(`node_modules`, `venv`, basis data). Siap di-*deploy*.

## Arsitektur deploy

```
  Pengguna ──▶  Frontend (Next.js)          Backend (FastAPI + IndoBERT)
                di  VERCEL          ── API ──▶  di  HUGGING FACE SPACES
                                                 (torch + model 498 MB)
```

> Backend **tidak bisa** di Vercel (model + torch melebihi batas serverless).
> Karena itu: **frontend → Vercel**, **backend + model → Hugging Face Spaces**.

## Struktur

```
mbgwatch-demo/
├── frontend/     # Next.js -> Vercel (portal publik + dashboard admin)
│   ├── app/  components/  lib/
│   ├── package.json  next.config.js
│   └── .env.local.example
└── backend/      # FastAPI -> Hugging Face Spaces (Docker)
    ├── main.py  model.py  database.py  extractor.py  config.py  schemas.py
    ├── requirements.txt  Dockerfile  README.md
    ├── mbg_berlabel.csv            # data seed (734 artikel)
    └── model_mbg_indobert/         # ← TAMBAHKAN sebelum deploy (498 MB)
```

## Fitur (semua tercakup)

- **Portal publik** (`/`): kartu berita ber-sentimen, filter chip kategori.
- **Dashboard admin** (`/dashboard`): filter (portal/sentimen/tanggal/cari),
  kartu statistik, donut distribusi, tren bulanan, tabel artikel + paginasi.
- **Cek kalimat**: analisis sentimen teks bebas.
- **Cek URL**: tempel tautan berita → di-scrape → prediksi otomatis.

---

## Langkah Deploy

### 1) Backend → Hugging Face Spaces

1. **Tambahkan model** ke folder backend:
   ```bash
   cp -r /path/ke/model_mbg_indobert  mbgwatch-demo/backend/model_mbg_indobert
   ```
2. Buat **Space baru** (huggingface.co/new-space) → **SDK: Docker**.
3. `git clone` repo Space, salin **seluruh isi `backend/`** ke dalamnya, lalu:
   ```bash
   git lfs install
   git add . && git commit -m "deploy mbg watch api" && git push
   ```
4. Tunggu build. Catat URL Space, mis. `https://namauser-mbg-watch-api.hf.space`.
   Cek `/(URL)/docs` untuk memastikan API hidup.

Detail ada di [`backend/README.md`](backend/README.md).

### 2) Frontend → Vercel

1. Push folder ini ke sebuah repo GitHub.
2. Di Vercel: **Add New Project** → impor repo → **Root Directory = `frontend`**
   (Vercel otomatis mendeteksi Next.js).
3. **Environment Variables** → tambah:
   ```
   NEXT_PUBLIC_API_URL = https://namauser-mbg-watch-api.hf.space
   ```
   (URL Space dari langkah 1.)
4. **Deploy**. Frontend aktif di `https://<proyek>.vercel.app`
   (`/` = portal publik, `/dashboard` = admin).

### 3) Kunci CORS (opsional, disarankan)

Agar hanya frontend Anda yang boleh mengakses API, pada Space set *Variable*:
```
FRONTEND_ORIGIN = https://<proyek>.vercel.app
```
(Default `*` sudah berfungsi untuk demo.)

---

## Menjalankan lokal (uji sebelum deploy)

```bash
# Backend (perlu model_mbg_indobert/ di dalam backend/)
cd backend
python -m venv venv && venv\Scripts\activate      # Windows
pip install -r requirements.txt
uvicorn main:app --reload                          # http://localhost:8000

# Frontend (terminal lain)
cd frontend
npm install
npm run dev                                        # http://localhost:3000
```

Frontend lokal default menembak `http://localhost:8000`. Untuk menembak backend
di HF Spaces, salin `.env.local.example` → `.env.local` dan isi `NEXT_PUBLIC_API_URL`.
