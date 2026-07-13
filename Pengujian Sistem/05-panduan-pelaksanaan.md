# 5. Panduan Pelaksanaan Pengujian

Panduan langkah demi langkah untuk mengeksekusi seluruh kasus uji pada
`02-skenario-dan-kasus-uji.md` dan mengisi `03-hasil-pengujian.md`.

## 5.1 Persiapan Sistem

### Pilihan A — Lokal (disarankan: hasil deterministik & bisa mematikan backend)

```bash
# Terminal 1 — Backend (perlu folder model_mbg_indobert/ di dalam backend/)
cd backend
venv\Scripts\activate          # atau: python -m venv venv lalu pip install -r requirements.txt
uvicorn main:app --reload      # aktif di http://localhost:8000

# Terminal 2 — Frontend
cd frontend
npm run dev                    # aktif di http://localhost:3000
```

Tunggu hingga log backend menampilkan "Database di-seed / sudah berisi ...
artikel" dan "Model IndoBERT berhasil dimuat".

> Catatan: proses build/dev Next.js membutuhkan memori bebas ± 1 GB.
> Tutup aplikasi lain bila perangkat kekurangan RAM.

### Pilihan B — Produksi

- Frontend: URL Vercel Anda; Backend: `https://alam-31-mbg-watch-api.hf.space`.
- Kasus **PP-05** (mematikan backend) tidak dapat dilakukan di produksi —
  jalankan kasus itu di lingkungan lokal, atau simulasikan dengan mengubah
  `NEXT_PUBLIC_API_URL` ke alamat mati saat menjalankan frontend lokal.
- HF Spaces yang lama tidak diakses akan *sleep*; buka `/docs`-nya dahulu
  dan tunggu hingga aktif sebelum menguji.

### Kondisi awal data

Pastikan basis data dalam kondisi awal **734 artikel** (hapus `backend/mbg.db`
lalu restart backend bila sebelumnya sudah dipakai coba-coba; seed ulang
berjalan otomatis dari CSV). Modul **CR** (ubah/hapus) mengubah data —
**jalankan modul CR paling akhir**, atau kembalikan kondisi awal sesudahnya
dengan menghapus `mbg.db` + restart.

## 5.2 Urutan Eksekusi yang Disarankan

1. **AP** (API via Swagger) — memastikan backend sehat sebelum uji UI.
2. **PP** (portal publik) — sisakan PP-05 (matikan backend) paling akhir
   kelompok ini, lalu nyalakan backend lagi.
3. **DB**, lalu **DF** (dashboard: statistik → filter/tabel).
4. **AT**, lalu **AU** (panel analisis).
5. **KB** (kompatibilitas — ulangi sampel kasus di Edge/Firefox/mobile).
6. **CR** terakhir (mengubah data). Setelah selesai, pulihkan data awal.
7. *(Opsional)* **UP** via Swagger, memakai `lampiran/contoh_artikel_upload.json`.

## 5.3 Cara Menguji API lewat Swagger UI

1. Buka `http://localhost:8000/docs` (atau `<URL-HF>/docs`).
2. Klik endpoint yang dituju → **Try it out**.
3. Isi parameter/body sesuai kolom *Data Uji* kasus terkait. Contoh body:
   - `POST /api/prediksi` → `{"teks": "   "}`  (kasus AP-04)
   - `PATCH /api/artikel/{id}` → path `id` diisi id artikel; body
     `{"sentimen": "bagus"}` (kasus CR-05). Ambil id valid dari respons
     `GET /api/artikel` (field `id` pada salah satu item `data`).
   - `POST /api/artikel-upload` → salin seluruh isi
     `lampiran/contoh_artikel_upload.json` (kasus UP-01).
4. Klik **Execute**; catat **Code** (kode status) dan **Response body**.
5. Tangkap layar bagian respons untuk bukti (`bukti/ap-xx.png`).

## 5.4 Tips per Kasus Tertentu

| Kasus | Tips |
|---|---|
| PP-03 | Gunakan kategori berjumlah artikel sedikit agar cepat habis; jumlah artikel per kategori bisa dilihat dari respons `GET /api/statistik` (field `per_kategori`) |
| PP-05 | Cukup tekan `Ctrl+C` pada terminal uvicorn lalu *refresh* portal; setelah tangkapan layar, jalankan lagi uvicorn |
| DF-03 | Kombinasi Detik + negatif + Juni 2026 pada data awal menghasilkan ±69 artikel — bila 0, periksa format tanggal yang terisi |
| CR-01 | Pilih artikel di halaman 1 agar mudah dipantau; catat judulnya untuk langkah persistensi (muat ulang + cek portal publik) |
| AU-01 | Pilih URL artikel teks biasa (detik/kompas/antara). Bila portal menolak scraping (HTTP 403), itu bukan kegagalan sistem — ganti URL lain. Tombol "Menganalisis..." mudah diamati saat menembak backend HF (lebih lambat); di lokal gunakan rekam layar bila perlu |
| AU-03 | Respons untuk domain fiktif butuh belasan detik karena sistem mencoba ulang — tunggu sampai kotak kesalahan muncul |
| KB-01 | Chrome DevTools → ikon perangkat (Ctrl+Shift+M) → pilih iPhone SE / atur lebar 375–620 px |

## 5.5 Dokumentasi Bukti

1. Simpan tangkapan layar di folder `bukti/` dengan nama sesuai kolom
   *Bukti* pada dokumen 03 (mis. `pp-01.png`, `cr-07.png`).
2. Satu kasus cukup satu gambar yang memperlihatkan bukti inti (mis. pesan
   kesalahan, atau kondisi sebelum–sesudah digabung berdampingan).
3. Untuk skripsi, pilih 2–4 bukti paling representatif sebagai "Gambar 4.x"
   di naskah; sisanya masuk lampiran.

## 5.6 Mengisi Lembar Hasil

1. Buka `03-hasil-pengujian.md`, isi tanggal/penguji/lingkungan.
2. Untuk tiap kasus: bandingkan kenyataan dengan kolom *Hasil yang
   Diharapkan* di dokumen 02 → koreksi *Hasil Aktual* bila perlu →
   tetapkan *Kesimpulan* Valid/Tidak Valid.
3. Kasus Tidak Valid dicatat di tabel 3.11 (temuan) beserta tindak lanjut;
   setelah diperbaiki, uji ulang dan catat hasilnya.
4. Perbarui rekapitulasi 3.10, lalu salin angkanya ke draf naskah
   (`04-draf-bab-4-subbab-4-5.md`).
