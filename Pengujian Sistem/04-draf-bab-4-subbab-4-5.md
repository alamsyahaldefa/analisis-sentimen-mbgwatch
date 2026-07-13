# Draf Naskah — BAB IV, Subbab 4.5 Hasil dan Pembahasan Pengujian Sistem

> **Petunjuk pemakaian draf ini:**
> 1. Salin ke dokumen skripsi, lalu sesuaikan gaya selingkung
>    (penomoran tabel, sitasi, istilah) dengan pedoman penulisan Anda.
> 2. Bagian dalam tanda `[...]` wajib diisi/dikonfirmasi.
> 3. Angka rekap (30 kasus, 100%) mengikuti dokumen `03-hasil-pengujian.md`;
>    perbarui bila hasil eksekusi nyata berbeda.
> 4. Kutipan definisi black box testing perlu sitasi — umumnya Pressman
>    (Software Engineering: A Practitioner's Approach) — sesuaikan dengan
>    daftar pustaka Anda.

---

## 4.5 Hasil dan Pembahasan Pengujian Sistem

### 4.5.1 Metode dan Lingkungan Pengujian

Pengujian sistem dilakukan untuk memastikan seluruh fungsionalitas aplikasi
MBG Watch berjalan sesuai dengan rancangan kebutuhan yang telah ditetapkan.
Metode yang digunakan adalah *black box testing*, yaitu pengujian yang
berfokus pada spesifikasi fungsional perangkat lunak dengan memberikan
masukan pada antarmuka sistem dan membandingkan keluaran yang dihasilkan
terhadap keluaran yang diharapkan, tanpa memeriksa struktur internal kode
program [sitasi]. Metode ini dipilih karena mampu memvalidasi perilaku
sistem dari sudut pandang pengguna akhir — baik pengguna umum pada portal
publik maupun admin pada dashboard — sekaligus menguji ketahanan sistem
terhadap masukan yang tidak valid.

Perancangan kasus uji menggunakan tiga teknik. Pertama, *equivalence
partitioning*, yang mengelompokkan masukan ke dalam kelas-kelas yang
diperlakukan sama oleh sistem sehingga pengujian cukup diwakili satu nilai
per kelas. Kedua, *boundary value analysis*, yang menguji nilai-nilai pada
batas kelas masukan, misalnya parameter halaman `page = 0` (tidak valid)
dan `page = 1` (valid), serta `limit = 100` (valid) dan `limit = 101`
(tidak valid). Ketiga, *negative testing*, yang dengan sengaja memberikan
masukan salah atau kondisi kegagalan — teks kosong, URL tanpa skema,
hingga backend yang dimatikan — untuk memastikan sistem menampilkan pesan
kesalahan yang informatif dan tetap stabil.

Pengujian dilaksanakan pada [tanggal] oleh [nama penguji] dengan lingkungan
sebagai berikut.

**Tabel 4.x Lingkungan Pengujian**

| Komponen | Spesifikasi |
|---|---|
| Sistem operasi | Windows 11 Home Single Language |
| Peramban | Google Chrome [versi]; pembanding: Microsoft Edge, Mozilla Firefox |
| Frontend | Next.js 14 — [http://localhost:3000 / URL Vercel] |
| Backend | FastAPI + model IndoBERT — [http://localhost:8000 / URL HF Spaces] |
| Alat uji API | Swagger UI (`/docs`) |
| Data uji | 734 artikel berlabel (negatif 340; netral 226; positif 168) dari 10 portal berita, periode Januari–Juni 2026 |

### 4.5.2 Skenario Pengujian

Skenario pengujian disusun mencakup seluruh fitur sistem dan dikelompokkan
menjadi delapan modul dengan total **30 kasus uji**, sebagaimana dirangkum
pada Tabel 4.x. Setiap kasus uji memuat kode identitas, prosedur, data
masukan, dan hasil yang diharapkan; daftar lengkapnya disajikan pada
Lampiran [x].

**Tabel 4.x Ringkasan Skenario Pengujian**

| No | Modul Pengujian | Kode | Cakupan | Jumlah Kasus |
|---|---|---|---|---|
| 1 | Portal Publik | PP | Pemuatan halaman & kartu berita ber-sentimen, filter kategori, muat bertahap, navigasi, penanganan kegagalan backend | 5 |
| 2 | Dashboard — Statistik & Visualisasi | DB | Pemuatan dashboard, kartu statistik, donat distribusi & tren bulanan | 3 |
| 3 | Dashboard — Filter & Tabel Artikel | DF | Tabel & paginasi, filter portal/sentimen/tanggal, kombinasi (AND), pencarian, hasil kosong, reset | 6 |
| 4 | Pengelolaan (CRUD) Sentimen | CR | Ubah label + persistensi, batal, hapus dengan konfirmasi, batal hapus, validasi API (400/404) | 6 |
| 5 | Analisis Sentimen Teks | AT | Prediksi tiga kelas sentimen, validasi masukan kosong | 2 |
| 6 | Analisis Sentimen dari URL | AU | Ekstraksi artikel + prediksi, validasi format URL, URL gagal akses/bukan artikel | 3 |
| 7 | Antarmuka API | AP | Struktur respons, kode status, validasi parameter (nilai batas) | 4 |
| 8 | Kompatibilitas & Responsivitas | KB | Chrome/Edge/Firefox, tampilan layar sempit | 1 |
| | **Total** | | | **30** |

Perlu ditegaskan bahwa pengujian *black box* pada modul analisis sentimen
(AT dan AU) menilai **fungsionalitas** sistem — yakni kemampuan sistem
menerima masukan, menjalankan inferensi, dan menyajikan label sentimen
beserta tingkat keyakinan dan distribusi probabilitasnya — dan bukan
ketepatan label prediksi. Evaluasi ketepatan model IndoBERT (akurasi,
*precision*, *recall*, F1-*score*) telah dibahas terpisah pada Subbab
[4.x Evaluasi Model].

### 4.5.3 Hasil Pengujian

Berdasarkan pelaksanaan seluruh skenario, diperoleh hasil sebagaimana
dirangkum pada Tabel 4.x. Contoh rincian hasil untuk beberapa kasus
representatif ditunjukkan pada Tabel 4.x+1, sedangkan rincian lengkap
ke-30 kasus disajikan pada Lampiran [x].

**Tabel 4.x Rekapitulasi Hasil Pengujian**

| No | Modul | Jumlah Kasus | Valid | Tidak Valid | Persentase |
|---|---|---|---|---|---|
| 1 | Portal Publik (PP) | 5 | [5] | [0] | [100%] |
| 2 | Statistik & Visualisasi (DB) | 3 | [3] | [0] | [100%] |
| 3 | Filter & Tabel Artikel (DF) | 6 | [6] | [0] | [100%] |
| 4 | CRUD Sentimen (CR) | 6 | [6] | [0] | [100%] |
| 5 | Analisis Teks (AT) | 2 | [2] | [0] | [100%] |
| 6 | Analisis URL (AU) | 3 | [3] | [0] | [100%] |
| 7 | Antarmuka API (AP) | 4 | [4] | [0] | [100%] |
| 8 | Kompatibilitas (KB) | 1 | [1] | [0] | [100%] |
| | **Total** | **30** | **[30]** | **[0]** | **[100%]** |

**Tabel 4.x Contoh Rincian Hasil Pengujian (kasus representatif)**

| Kode | Skenario | Data Uji | Hasil yang Diharapkan | Hasil Aktual | Kesimpulan |
|---|---|---|---|---|---|
| PP-02 | Menyaring berita berdasarkan kategori | Chip "Keracunan & Masalah Kesehatan" | Daftar dimuat ulang; hanya artikel kategori terpilih | Sesuai harapan | Valid |
| DF-05 | Filter tanpa hasil | Kata kunci `xyzabc123` | Pesan "Tidak ada artikel yang cocok dengan filter." tanpa galat | Sesuai harapan ("Menampilkan 0–0 dari 0 artikel") | Valid |
| CR-01 | Mengubah label sentimen artikel | negatif → positif | Lencana berubah; statistik dan grafik diperbarui otomatis; tetap setelah dimuat ulang | Sesuai harapan (kartu Positif 22.9% → 23.0% tanpa muat ulang; label tetap setelah *reload*) | Valid |
| CR-05 | PATCH dengan nilai sentimen tidak valid | `{"sentimen": "bagus"}` | Kode 400 dan pesan kesalahan yang jelas | Sesuai harapan (400 — "Sentimen tidak valid. Pilihan: negatif, netral, positif.") | Valid |
| AT-01 | Analisis teks tiga kelas sentimen | Teks uji T-POS-1, T-NEG-1, T-NET-1 | Label + keyakinan + probabilitas (total ≈ 100%) tampil | Label: positif (60.7%), negatif (75.8%), netral (64.3%) | Valid |
| AU-02 | URL tanpa skema http/https | `www.detik.com/berita-mbg` | Pesan "Masukkan URL lengkap diawali http:// atau https://" | Sesuai harapan | Valid |
| AP-03 | Nilai batas parameter page & limit | `page=0`; `limit=101` | Kode 422 (batas page ≥ 1, limit ≤ 100) | Sesuai harapan (422 pada keduanya; 200 pada nilai batas valid) | Valid |

> Hasil pada tabel di atas berasal dari eksekusi nyata 9 Juli 2026
> (rincian dan bukti: dokumen 03 dan folder `bukti/`).

> [Sisipkan 2–4 gambar tangkapan layar sebagai bukti, mis. hasil CR-02 dan
> AT-01, dengan keterangan "Gambar 4.x ..." — ambil dari folder `bukti/`.]

### 4.5.4 Pembahasan

Hasil pengujian menunjukkan bahwa dari **30 kasus uji** yang dijalankan,
sebanyak **[30] kasus ([100]%) dinyatakan valid**, artinya hasil aktual
sistem sesuai dengan hasil yang diharapkan pada seluruh modul. Temuan ini
dapat dibahas dari empat sisi berikut.

**Pertama, dari sisi fungsionalitas inti**, seluruh alur utama sistem —
penyajian berita ber-sentimen pada portal publik, penyaringan dan
visualisasi statistik pada dashboard, inferensi sentimen terhadap teks
bebas maupun URL berita, serta pengelolaan label sentimen oleh admin —
berjalan sesuai rancangan. Konsistensi data antartampilan juga terjaga:
perubahan label sentimen yang dilakukan admin (kasus CR-01) langsung
tercermin pada kartu statistik, grafik distribusi, dan portal publik tanpa
perlu memuat ulang halaman, serta bersifat permanen setelah aplikasi
dibuka kembali.

**Kedua, dari sisi ketahanan terhadap masukan tidak valid**, sistem
terbukti menangani seluruh skenario negatif dengan baik. Masukan kosong
ditolak di sisi frontend sebelum permintaan dikirim (AT-02, AU-02),
sedangkan lapisan API menerapkan validasi berlapis: galat validasi skema
(kode 422) untuk masukan yang tidak memenuhi format, dan galat logika
(kode 400/404) dengan pesan berbahasa Indonesia yang informatif untuk
nilai di luar domain atau data yang tidak ditemukan (CR-05, CR-06,
AP-03, AP-04). Ketika backend dihentikan, antarmuka tetap stabil dan
menampilkan arahan pemulihan (PP-05), sehingga kegagalan sebagian komponen
tidak meruntuhkan keseluruhan aplikasi.

**Ketiga, dari sisi pengalaman pengguna**, indikator proses
("Menganalisis...") dan penonaktifan tombol selama pemrosesan (AU-01)
mencegah pengiriman ganda, sementara paginasi bertahap pada portal
publik (PP-03) menjaga performa pemuatan halaman. Tampilan juga
konsisten pada peramban Chrome, Edge, dan Firefox serta beradaptasi pada
layar sempit (KB-01).

**Keempat**, perlu dicatat bahwa hasil pengujian ini terbatas pada aspek
fungsional. Kualitas label sentimen yang dihasilkan bergantung pada
kinerja model IndoBERT yang telah dievaluasi pada Subbab [4.x] dengan
[akurasi/F1 = ...]. Selain itu, pengujian tidak mencakup aspek beban
(banyak pengguna simultan) dan keamanan, yang dapat menjadi saran
pengembangan selanjutnya.

Dengan demikian, dapat disimpulkan bahwa sistem MBG Watch **lolos
pengujian fungsional** dengan tingkat keberhasilan [100]% dan siap
digunakan sesuai tujuan perancangannya, yaitu memantau dan menganalisis
sentimen pemberitaan Program Makan Bergizi Gratis secara otomatis
sekaligus menyediakan kendali koreksi bagi admin.

---

> **[Opsional]** Bila fitur unggah artikel (modul UP) dibahas dalam
> skripsi, tambahkan satu paragraf pada 4.5.3–4.5.4 yang menyatakan bahwa
> tiga kasus uji tambahan pada endpoint `POST /api/artikel-upload` juga
> valid — mencakup penyimpanan ke basis data terpisah (`mbg_upload.db`)
> yang tetap tersaji terpadu pada tampilan pengguna — dan sesuaikan total
> kasus menjadi 33.
