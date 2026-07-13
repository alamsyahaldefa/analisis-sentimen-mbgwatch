# 1. Rencana Pengujian Sistem MBG Watch

## 1.1 Tujuan Pengujian

Pengujian sistem bertujuan untuk memastikan bahwa seluruh fungsionalitas
aplikasi web **MBG Watch — Analisis Sentimen Berita Program Makan Bergizi
Gratis (MBG)** berjalan sesuai dengan rancangan dan kebutuhan fungsional,
meliputi:

1. Menyajikan berita MBG beserta label sentimennya kepada publik (portal
   publik) dan kepada admin (dashboard) secara benar;
2. Menyediakan fasilitas penyaringan, pencarian, paginasi, dan visualisasi
   statistik yang konsisten dengan data pada basis data;
3. Melakukan inferensi sentimen (negatif/netral/positif) terhadap teks bebas
   dan terhadap artikel yang diambil dari URL berita menggunakan model
   IndoBERT;
4. Memfasilitasi admin mengoreksi (mengubah) label sentimen dan menghapus
   artikel (CRUD), dengan perubahan yang tersimpan permanen dan tercermin
   pada seluruh tampilan;
5. Menangani masukan yang tidak valid dan kondisi kegagalan (backend tidak
   aktif, URL tidak dapat diakses, dsb.) dengan pesan kesalahan yang jelas
   tanpa membuat aplikasi berhenti bekerja.

## 1.2 Objek Pengujian

| Aspek | Keterangan |
|---|---|
| Nama sistem | MBG Watch — Analisis Sentimen Berita MBG |
| Arsitektur | Frontend **Next.js 14** (React 18) · Backend **FastAPI** (Python) · Model **IndoBERT** (fine-tuned, 3 kelas) · Basis data **SQLite** |
| Halaman | `/` (Portal Publik — sudut pandang pengguna umum) dan `/dashboard` (Dashboard Admin) |
| API backend | `GET /api/artikel`, `GET /api/statistik`, `POST /api/prediksi`, `POST /api/prediksi-url`, `PATCH /api/artikel/{id}`, `DELETE /api/artikel/{id}`, `POST /api/artikel-upload` |
| Data awal | 734 artikel berlabel (negatif 340; netral 226; positif 168) dari 10 portal berita nasional, terbit 7 Jan – 8 Jun 2026 |
| Alamat lokal | Frontend `http://localhost:3000` · Backend `http://localhost:8000` (dokumentasi API di `/docs`) |
| Alamat produksi | Frontend: `https://<nama-proyek>.vercel.app` *(isi sesuai deploy)* · Backend: `https://alam-31-mbg-watch-api.hf.space` |

## 1.3 Ruang Lingkup

### 1.3.1 Fitur yang Diuji

| No | Modul | Kode | Fitur yang dicakup |
|---|---|---|---|
| 1 | Portal Publik | PP | Pemuatan halaman, kartu berita ber-sentimen, chip filter kategori, tombol "Selengkapnya" (muat bertahap), navigasi, penanganan kegagalan backend |
| 2 | Dashboard — Statistik & Visualisasi | DB | Kartu statistik (total & persentase per sentimen), donut distribusi sentimen, grafik tren bulanan, navigasi kembali ke portal |
| 3 | Dashboard — Filter & Tabel Artikel | DF | Filter portal/sentimen/rentang tanggal/pencarian judul, kombinasi filter, reset, tabel artikel, paginasi |
| 4 | CRUD Sentimen | CR | Ubah label sentimen artikel (edit inline), batal edit, hapus artikel dengan konfirmasi, persistensi perubahan, validasi API (nilai tidak valid, id tidak ditemukan) |
| 5 | Analisis Sentimen Teks | AT | Prediksi sentimen teks bebas, tampilan keyakinan & probabilitas, validasi teks kosong, status tombol saat memproses |
| 6 | Analisis Sentimen dari URL | AU | Ekstraksi artikel dari URL + prediksi, validasi format URL, penanganan URL tidak terjangkau / bukan artikel |
| 7 | Antarmuka API | AP | Struktur & kode status respons endpoint, validasi parameter (nilai batas), penanganan masukan tidak valid |
| 8 | Kompatibilitas & Responsivitas | KB | Peramban Chrome/Edge/Firefox, tampilan layar sempit (mobile) |

### 1.3.2 Fitur yang Tidak Diuji (dikecualikan)

| Item | Alasan |
|---|---|
| Menu statis portal (Pengaduan, Edukasi, Tentang Kami, FAQ) | Tautan dekoratif (placeholder, `href="#"`), bukan kebutuhan fungsional |
| **Ketepatan label prediksi model** (akurasi/F1) | Termasuk evaluasi model, dibahas pada subbab evaluasi kinerja model — pengujian black box hanya menilai fungsionalitas (sistem mengembalikan label, keyakinan, dan probabilitas) |
| Panel **Upload Artikel** pada UI dashboard | Fitur sedang dinonaktifkan (disembunyikan) dari antarmuka; endpoint API-nya tetap diuji sebagai **lampiran opsional** (modul UP, 3 kasus) |
| Pengujian white box (struktur kode, unit test internal) | Di luar metode yang dipilih |
| Pengujian beban/kinerja (load testing) | Di luar lingkup tugas akhir |

## 1.4 Metode dan Teknik Pengujian

Pengujian menggunakan metode **Black Box Testing**, yaitu pengujian yang
berfokus pada spesifikasi fungsional perangkat lunak: penguji memberikan
masukan pada antarmuka sistem dan memeriksa apakah keluaran sesuai dengan
yang diharapkan, **tanpa memperhatikan struktur internal kode**. Kasus uji
dirancang dengan tiga teknik:

1. **Equivalence Partitioning (partisi ekivalensi)** — masukan dikelompokkan
   ke kelas-kelas yang diperlakukan sama oleh sistem, lalu diambil wakil dari
   tiap kelas (valid dan tidak valid).
2. **Boundary Value Analysis (analisis nilai batas)** — menguji nilai pada
   batas kelas, mis. `page = 0` dan `page = 1`, `limit = 100` dan
   `limit = 101`.
3. **Negative Testing (pengujian negatif)** — memberikan masukan salah atau
   kondisi gagal yang disengaja (teks kosong, URL tanpa skema, backend
   dimatikan) untuk memastikan sistem menampilkan pesan kesalahan yang
   tepat dan tetap stabil.

### Tabel Partisi Ekivalensi Masukan Utama

| Masukan | Kelas valid | Kelas tidak valid | Kasus uji terkait |
|---|---|---|---|
| Teks analisis | Teks berisi ≥ 1 karakter bermakna | String kosong; hanya spasi | AT-01 / AT-02, AP-04 |
| URL berita | URL lengkap `http(s)://` yang memuat artikel | Kosong; tanpa skema; domain tidak ada; halaman bukan artikel | AU-01 / AU-02, AU-03 |
| Parameter `page` | Bilangan bulat ≥ 1 | 0 atau negatif | AP-03, DF-01 |
| Parameter `limit` | 1 – 100 | 0; > 100 | AP-03 |
| Filter sentimen | `positif`, `netral`, `negatif`, kosong (semua) | — (dropdown membatasi pilihan) | DF-02 |
| Nilai sentimen (PATCH) | `positif`, `netral`, `negatif` | String lain (mis. `bagus`) | CR-01 / CR-05 |
| ID artikel (PATCH/DELETE) | ID yang ada di basis data | ID yang tidak terdaftar | CR-01, CR-03 / CR-06 |
| Filter tanggal & kombinasi | Rentang `YYYY-MM-DD` yang memuat data | Kombinasi filter tanpa hasil (hasil kosong, bukan galat — diuji lewat kata kunci acak) | DF-03 / DF-05 |

## 1.5 Lingkungan dan Alat Pengujian

| Komponen | Spesifikasi |
|---|---|
| Sistem operasi | Windows 11 Home Single Language |
| Perangkat | Laptop *(isi merek/RAM sesuai perangkat Anda)* |
| Peramban utama | Google Chrome versi terbaru |
| Peramban pembanding | Microsoft Edge, Mozilla Firefox |
| Frontend | Next.js dev/production build — `http://localhost:3000` atau URL Vercel |
| Backend | FastAPI + Uvicorn — `http://localhost:8000` atau HF Spaces |
| Alat uji API | **Swagger UI** bawaan FastAPI (`<backend>/docs`) — tanpa alat tambahan |
| Alat uji responsivitas | Chrome DevTools (Device Toolbar) |
| Dokumentasi bukti | Tangkapan layar (folder `bukti/`) |

## 1.6 Kriteria Kelulusan

1. Sebuah kasus uji dinyatakan **Valid** apabila *hasil aktual* sama dengan
   *hasil yang diharapkan*; bila berbeda dinyatakan **Tidak Valid** dan
   dicatat sebagai temuan.
2. Pengujian sistem dinyatakan **berhasil** apabila seluruh kasus uji pada
   suite utama (30 kasus) berstatus Valid, atau temuan yang ada telah
   diperbaiki dan diuji ulang hingga Valid.
3. Kasus dengan hasil bergantung model (label prediksi pada AT-01 dan
   AU-01) dinilai Valid selama sistem mengembalikan label salah satu dari
   tiga kelas beserta keyakinan dan probabilitas yang konsisten
   (jumlah ≈ 100%) — bukan berdasarkan kecocokan label dengan intuisi
   penguji.

## 1.7 Pelaksana dan Jadwal

| Peran | Nama | Tanggal |
|---|---|---|
| Penguji / penyusun | *(nama mahasiswa)* | *(tanggal pelaksanaan)* |
| Perangkat uji | *(laptop pribadi / lab)* | — |

> Isi tabel di atas saat pengujian dilaksanakan. Bila pengujian melibatkan
> responden lain (mis. calon pengguna atau dosen), tambahkan barisnya.
