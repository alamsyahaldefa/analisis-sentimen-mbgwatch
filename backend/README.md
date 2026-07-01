---
title: MBG Watch API
emoji: 🍚
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# MBG Watch — Backend API (Hugging Face Spaces)

Backend FastAPI untuk analisis sentimen berita **Makan Bergizi Gratis (MBG)**
menggunakan model IndoBERT. Space ini melayani data dashboard dan inferensi
sentimen (teks & URL) untuk frontend yang di-*deploy* di Vercel.

## Endpoint

| Metode | Endpoint | Fungsi |
|--------|----------|--------|
| GET | `/api/artikel` | Daftar artikel (filter + paginasi) |
| GET | `/api/statistik` | Statistik: total, per kelas, tren bulanan, kategori |
| POST | `/api/prediksi` | Prediksi sentimen dari teks |
| POST | `/api/prediksi-url` | Scrape artikel dari URL lalu prediksi |

Dokumentasi interaktif tersedia di `/docs`.

## ⚠️ Sebelum deploy: tambahkan model

Folder ini **belum berisi model** (498 MB) agar tetap ringan. Salin model ke
dalam folder backend sebelum membuat Space:

```bash
cp -r /path/ke/model_mbg_indobert  ./model_mbg_indobert
```

(Atau ambil dari folder serah-terima `serahterima_model_mbg/model_mbg_indobert`.)
Saat `git push` ke Space, berkas `model.safetensors` otomatis lewat **git-lfs**.

> Alternatif tanpa menyertakan bobot: unggah model ke sebuah *model repo* di
> Hugging Face Hub, lalu set *Variable* `MBG_MODEL` = `namauser/mbg-indobert`.

## Variabel lingkungan (opsional)

| Variabel | Default | Guna |
|----------|---------|------|
| `FRONTEND_ORIGIN` | `*` | Origin CORS; set ke domain Vercel untuk produksi |
| `MBG_MODEL` | `./model_mbg_indobert` | Lokasi/nama model |
| `MBG_CSV` | `./mbg_berlabel.csv` | Data seed dashboard |
| `MBG_DB` | `/tmp/mbg.db` | Lokasi SQLite (writable) |

## Cara membuat Space

1. Buat Space baru → **SDK: Docker** (Blank).
2. `git clone` Space, salin seluruh isi folder `backend/` ini ke dalamnya
   (termasuk `Dockerfile`, `README.md`, dan `model_mbg_indobert/`).
3. `git add . && git commit -m "deploy" && git push`.
4. Tunggu *build*; API aktif di `https://<user>-<space>.hf.space`.
