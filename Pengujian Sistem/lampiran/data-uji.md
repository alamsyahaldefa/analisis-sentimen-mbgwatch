# Lampiran — Data Uji

## A. Teks Uji untuk Modul AT (Analisis Sentimen Teks)

> Salin-tempel apa adanya ke textarea "Coba Sendiri". Label pada tanda
> kurung adalah **dugaan** nada teks; hasil prediksi model dicatat apa
> adanya (lihat catatan fungsional vs akurasi pada README).

**T-POS-1 (positif)**
```
Program Makan Bergizi Gratis dinilai berhasil meningkatkan gizi siswa di
sejumlah daerah. Para orang tua menyambut baik program ini karena anak-anak
menjadi lebih semangat belajar dan angka kehadiran sekolah meningkat.
```

**T-POS-2 (positif, cadangan)**
```
Petani dan peternak lokal mengaku terbantu oleh program MBG karena hasil
panen dan telur mereka terserap dapur gizi setiap hari, sehingga pendapatan
mereka meningkat dan perekonomian desa ikut bergerak.
```

**T-NEG-1 (negatif)**
```
Puluhan siswa sekolah dasar dilarikan ke puskesmas karena diduga keracunan
usai menyantap menu makan bergizi gratis. Orang tua murid mengeluhkan
lambannya penanganan dan menuntut program dihentikan sementara.
```

**T-NEG-2 (negatif, cadangan)**
```
Operasional dapur SPPG kembali ditangguhkan setelah ditemukan pelanggaran
standar higiene dan sanitasi. Kualitas lauk yang dibagikan juga dikeluhkan
karena porsinya menyusut dan tidak layak konsumsi.
```

**T-NET-1 (netral)** — diambil dari korpus; pada uji 9 Juli 2026 model
melabelinya netral (keyakinan 64%)
```
Profil Nanik S Deyang, Kepala BGN Baru yang Gantikan Dadan Hindayana.
Struktur pimpinan Badan Gizi Nasional (BGN) resmi dirombak. Presiden RI
Prabowo Subianto menunjuk Nanik S Deyang sebagai Kepala BGN yang baru,
menggantikan posisi Dadan Hindayana.
```

**T-NET-2 (netral, cadangan)** — catatan jujur: pada uji 9 Juli 2026 model
justru melabeli teks karangan ini **positif** (keyakinan 52–58%); tetap sah
secara fungsional, catat label apa adanya
```
Pemerintah daerah meninjau pelaksanaan program makan bergizi gratis di
beberapa sekolah pekan ini. Kunjungan dilakukan untuk memeriksa kesiapan
dapur dan jadwal distribusi menu kepada penerima manfaat.
```

**T-KOSONG (untuk AT-02):** string kosong `""` dan string spasi `"   "`.

## B. URL Uji untuk Modul AU (Analisis dari URL)

| Kode | Nilai | Untuk kasus |
|---|---|---|
| U-VAL-1 | *(pilih sendiri saat pengujian)* URL artikel berita MBG terbaru dari portal teks, mis. `https://www.antaranews.com/berita/...` atau `https://news.detik.com/berita/...` — buka dulu di peramban untuk memastikan dapat diakses | AU-01 |
| U-KOSONG | `` (kosong) | AU-02 |
| U-TANPA-SKEMA | `www.detik.com/berita-mbg` | AU-02 |
| U-MATI | `https://situs-tidak-ada-xyz123.com/berita` | AU-03 |
| U-NON-ARTIKEL | `https://example.com` (halaman minim teks — gagal ekstraksi; jangan pakai google.com: beranda Google justru berhasil diekstrak) | AU-03 |

> Tips U-VAL-1: portal yang bersahabat untuk ekstraksi antara lain Antara,
> Detik, Kompas, Liputan6. Bila sebuah portal menolak akses otomatis
> (HTTP 403), sistem menampilkan pesan "Situs menolak permintaan…" — itu
> bukan kegagalan sistem; gunakan URL dari portal lain untuk AU-01.

## C. Nilai Filter untuk Modul DF

| Isian | Nilai uji | Keterangan |
|---|---|---|
| Portal | `Detik` | Pilihan lain: Antara, CNN Indonesia, Kompas, Kumparan, Liputan6, Republika, Suara, Tempo, Tribunnews |
| Sentimen | `Negatif` | Data awal: negatif 340, netral 226, positif 168 |
| Rentang tanggal | `2026-06-01` s.d. `2026-06-30` | Dataset terbit 2026-01-07 s.d. 2026-06-08; kombinasi Detik + negatif + Juni 2026 menghasilkan ±69 artikel (untuk DF-03) |
| Cari judul (ada hasil) | `keracunan` | Kata sering muncul pada dataset |
| Cari judul (tanpa hasil) | `xyzabc123` | Untuk DF-05 |

## D. Data untuk Modul CR (via Swagger)

| Kebutuhan | Cara memperoleh / nilai | Untuk kasus |
|---|---|---|
| `id` artikel valid | Jalankan `GET /api/artikel?limit=1` → salin field `id` pada item pertama | CR-05 |
| `id` fiktif | `tidak-ada` | CR-06 |
| Body PATCH valid | `{"sentimen": "netral"}` (atau positif/negatif) | — |
| Body PATCH tidak valid | `{"sentimen": "bagus"}` | CR-05 |

## E. Data untuk Modul UP (opsional)

Gunakan `contoh_artikel_upload.json` (untuk Swagger) atau
`contoh_artikel_upload.csv` (bila panel upload pada UI diaktifkan kembali).
Item tidak lengkap untuk UP-02:

```json
{"judul": "Artikel uji tanpa isi", "teks": "   "}
```
