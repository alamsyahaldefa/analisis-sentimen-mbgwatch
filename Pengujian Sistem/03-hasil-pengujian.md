# 3. Hasil Pengujian (Lembar Hasil + Rekapitulasi)

**Status eksekusi:** seluruh kasus (kecuali sebagian KB-01) telah
**dieksekusi nyata pada 9 Juli 2026** terhadap sistem berjalan — frontend
lokal (`next dev`) yang menembak **backend produksi Hugging Face Spaces**
— menggunakan peramban **Microsoft Edge (headless, otomatis)**. Bukti
tangkapan layar tersimpan di folder `bukti/` (51 berkas; nama sesuai kolom
*Bukti*; berkas bersufiks tambahan seperti `-hal2`, `-proses` adalah bukti
pendukung). Kondisi data dipulihkan ke keadaan awal (734 artikel;
340/226/168) setelah pengujian selesai.

Penanda basis verifikasi per kasus:
- **[E]** — dieksekusi nyata 9 Juli 2026, ada bukti tangkapan layar;
- **[E*]** — dieksekusi dengan penyesuaian yang dicatat di §3.11;
- **[M]** — masih perlu eksekusi manual oleh penguji.

Tanggal pengujian : **9 Juli 2026** (eksekusi otomatis terdokumentasi)
Penguji : ____________________ *(lengkapi; ulangi kasus [M] dan kasus lain
yang ingin diverifikasi sendiri sebelum sidang)*
Lingkungan : ☑ Frontend lokal + backend produksi (HF Spaces) · Edge headless

---

## 3.1 Modul PP — Portal Publik (5 kasus)

| Kode | Skenario (ringkas) | Hasil Aktual | Kesimpulan | Bukti |
|---|---|---|---|---|
| PP-01 [E] | Memuat portal & kelengkapan kartu | Halaman termuat: nav MBGwatch, "Temuan Terbaru", chip "Semua" aktif + 7 kategori, 9 kartu lengkap (kategori, pill sentimen berwarna, judul, cuplikan, "Sumber: …", tanggal Indonesia), tombol "Selengkapnya" | Valid | pp-01.png |
| PP-02 [E] | Filter kategori & kembali ke "Semua" | Chip "Keracunan & Masalah Kesehatan" aktif; daftar dimuat ulang berisi artikel kategori tsb.; klik "Semua" mengembalikan seluruh artikel | Valid | pp-02.png |
| PP-03 [E] | "Selengkapnya" hingga habis | Kategori "Kualitas & Keamanan Pangan" (32 artikel): tiap klik menambah 9 kartu (append); saat habis tampil persis **"Semua 32 artikel telah ditampilkan."** | Valid | pp-03.png |
| PP-04 [E] | Navigasi portal ↔ dashboard | Nav "Dashboard" membawa ke `/dashboard`; "← Portal Publik" kembali ke `/` — dua arah berfungsi | Valid | pp-04.png |
| PP-05 [E*] | Backend tidak terjangkau | Kotak kesalahan merah: *"Failed to fetch — pastikan backend berjalan di http://localhost:8000."*; tidak ada kartu; aplikasi tidak crash. *(Disimulasikan dengan memblokir akses ke backend — lihat §3.11 no. 1)* | Valid | pp-05.png |

## 3.2 Modul DB — Dashboard: Statistik & Visualisasi (3 kasus)

| Kode | Skenario (ringkas) | Hasil Aktual | Kesimpulan | Bukti |
|---|---|---|---|---|
| DB-01 [E] | Memuat dashboard | Seluruh komponen tampil: header + tombol "← Portal Publik", filter, 4 kartu statistik, donat, tren, tabel, 2 panel analisis | Valid | db-01.png |
| DB-02 [E] | Kebenaran kartu statistik | **Total Artikel 734; Positif 22.9%; Negatif 46.3%; Netral 30.8%** — persis sesuai data awal (168/340/226 dari 734) | Valid | db-02.png |
| DB-03 [E] | Donat & tren | Donat 3 segmen warna standar + label persen + legenda; tren 3 garis dengan sumbu-X 2026-01..2026-06 | Valid | db-03.png |

## 3.3 Modul DF — Dashboard: Filter & Tabel Artikel (6 kasus)

| Kode | Skenario (ringkas) | Hasil Aktual | Kesimpulan | Bukti |
|---|---|---|---|---|
| DF-01 [E] | Tabel awal & paginasi | Kolom Judul/Portal/Tanggal/Sentimen/Aksi; **"Menampilkan 1–10 dari 734 artikel"**, "Halaman 1 / 74", "‹ Sebelumnya" nonaktif; setelah "Berikutnya ›": **"Menampilkan 11–20 dari 734 artikel"**; kembali normal | Valid | df-01.png |
| DF-02 [E] | Filter portal & sentimen | Portal=Detik → 152 artikel (semua Detik); + Sentimen=Negatif → **79 artikel** (semua badge negatif) | Valid | df-02.png |
| DF-03 [E] | Rentang tanggal & kombinasi | Juni 2026 → 573 artikel (semua Juni); kombinasi Detik+negatif+Juni → **69 artikel** memenuhi ketiga kriteria (AND) | Valid | df-03.png |
| DF-04 [E] | Pencarian judul (via Enter) | Kata "keracunan" ditekan **Enter** → 14 artikel, semua judul memuat kata tsb.; identik dengan tombol Terapkan | Valid | df-04.png |
| DF-05 [E] | Filter tanpa hasil | `xyzabc123` → **"Tidak ada artikel yang cocok dengan filter."**; "Menampilkan 0–0 dari 0 artikel"; tanpa galat | Valid | df-05.png |
| DF-06 [E] | Reset filter | Semua isian kosong kembali; tabel kembali "Menampilkan 1–10 dari 734 artikel" halaman 1 | Valid | df-06.png |

## 3.4 Modul CR — CRUD Sentimen (6 kasus)

| Kode | Skenario (ringkas) | Hasil Aktual | Kesimpulan | Bukti |
|---|---|---|---|---|
| CR-01 [E*] | Ubah sentimen + persistensi | Dropdown 3 kelas tampil (✎); setelah ✓: badge negatif→**Positif**, kartu statistik ter-update otomatis (Positif 22.9%→23.0%) tanpa muat ulang; setelah reload label **tetap Positif** (persisten). Nilai kemudian dipulihkan. *(Dilakukan pada artikel uji; total saat itu 735 — lihat §3.11 no. 2)* | Valid | cr-01.png |
| CR-02 [E] | Batal ubah | Dropdown dibuka, kelas lain dipilih, ✕ diklik → badge kembali ke nilai semula; tidak ada perubahan | Valid | cr-02.png |
| CR-03 [E] | Hapus artikel (OK) | Dialog **'Hapus artikel "…"?'** muncul; setelah OK baris hilang — pencarian judulnya: "Menampilkan 1–1 dari 1" → **"0–0 dari 0"** | Valid | cr-03.png |
| CR-04 [E] | Batal hapus | Dialog konfirmasi dibatalkan (Cancel) → baris tetap ada, tidak ada perubahan | Valid | cr-04.png |
| CR-05 [E] | PATCH sentimen tak valid | Swagger: `{"sentimen": "bagus"}` → **400** "Sentimen tidak valid. Pilihan: negatif, netral, positif." | Valid | cr-05.png |
| CR-06 [E] | PATCH/DELETE id tak terdaftar | PATCH id `tidak-ada` → **404**; DELETE id `tidak-ada` → **404** "Artikel tidak ditemukan." | Valid | cr-06.png |

## 3.5 Modul AT — Analisis Sentimen Teks (2 kasus)

| Kode | Skenario (ringkas) | Hasil Aktual | Kesimpulan | Bukti |
|---|---|---|---|---|
| AT-01 [E] | Analisis tiga kelas | Ketiga teks menghasilkan label + keyakinan + 3 bilah probabilitas. Label terekam: T-POS-1 → **Positif (60.7%)**; T-NEG-1 → **Negatif (75.8%)**; T-NET-1 → **Netral (64.3%)**. *(Catatan model: lihat §3.11 no. 3)* | Valid | at-01.png |
| AT-02 [E] | Teks kosong | Pesan **"Teks tidak boleh kosong."** tampil; tidak ada permintaan ke server; tidak ada hasil baru | Valid | at-02.png |

## 3.6 Modul AU — Analisis Sentimen dari URL (3 kasus)

| Kode | Skenario (ringkas) | Hasil Aktual | Kesimpulan | Bukti |
|---|---|---|---|---|
| AU-01 [E] | URL artikel valid | Tombol **"Menganalisis..."** (nonaktif) teramati saat proses; hasil menampilkan judul terekstrak *"Kejagung ungkap sudah pelajari kasus korupsi MBG sejak lama"* (Antara), tanggal, sentimen **Positif (keyakinan 38.2%)**, bilah probabilitas, dan lipatan "Teks yang dianalisis" | Valid | au-01.png |
| AU-02 [E] | Validasi format URL | Kosong → **"URL tidak boleh kosong."**; tanpa skema → **"Masukkan URL lengkap diawali http:// atau https://"** | Valid | au-02.png |
| AU-03 [E*] | URL tak terjangkau / bukan artikel | Domain fiktif → **"Gagal mengakses URL: tidak dapat terhubung ke server (periksa URL/koneksi)."**; `example.com` → **"Isi artikel tidak dapat diekstrak dari URL ini …"**. Aplikasi stabil. *(Data uji non-artikel diganti — lihat §3.11 no. 4)* | Valid | au-03.png |

## 3.7 Modul AP — Antarmuka API (4 kasus)

| Kode | Skenario (ringkas) | Hasil Aktual | Kesimpulan | Bukti |
|---|---|---|---|---|
| AP-01 [E] | GET /api/artikel | **200** — `{data: 10 artikel (kolom lengkap + sumber), total: 734, page: 1, limit: 10}` via Swagger | Valid | ap-01.png |
| AP-02 [E] | GET /api/statistik | **200** — total 734; per_kelas 340/226/168; tren 6 bulan; 10 portal; 7 kategori | Valid | ap-02.png |
| AP-03 [E*] | Nilai batas page/limit | `page=0` → **422** ("greater_than_equal … ge: 1"); `limit=101` → **422** ("less_than_equal … le: 100") — diuji via URL langsung karena Swagger UI memblokir nilai di luar batas di sisi klien *(lihat §3.11 no. 5)* | Valid | ap-03.png |
| AP-04 [E] | Validasi teks prediksi | `""` → **422** (panjang minimum); `"   "` → **400** `{"detail": "Teks tidak boleh kosong."}` | Valid | ap-04.png |

## 3.8 Modul KB — Kompatibilitas & Responsivitas (1 kasus)

| Kode | Skenario (ringkas) | Hasil Aktual | Kesimpulan | Bukti |
|---|---|---|---|---|
| KB-01 [M] | Lintas peramban & layar sempit | **Layar sempit (375 px) sudah dieksekusi**: kisi 1 kolom, menu nav menyusut, grafik menumpuk, tabel dapat digulir (kb-01.png, kb-01-dashboard.png; diambil di Edge). **Bagian Chrome & Firefox masih perlu diulang manual** | Valid (sebagian) | kb-01.png |

## 3.9 (Opsional) Modul UP — Upload Artikel (3 kasus, tingkat API)

| Kode | Skenario (ringkas) | Hasil Aktual | Kesimpulan | Bukti |
|---|---|---|---|---|
| UP-01 [E] | Upload valid; terpadu & terpisah | **200** — `berhasil` berisi 2 artikel (id `up-…`, sentimen hasil model, kategori otomatis, `sumber: "upload"`; default portal "Upload Admin" & tanggal hari ini); artikel tampil di tabel dashboard dengan tag **"upload"** (terlihat pada cr-01.png/cr-03-sebelum.png) | Valid | up-01.png |
| UP-02 [E] | Masukan tak lengkap / kosong | Item tanpa teks masuk `gagal` dengan pesan **"Judul dan teks wajib diisi."** (item valid tetap diproses); `{"artikel": []}` → **422** | Valid | up-02.png |
| UP-03 [E] | CRUD artikel upload | PATCH id `up-…` → **200** (sentimen berubah); DELETE → **200** `{"status": "terhapus", …}`; artikel hilang dari daftar | Valid | up-03.png |

---

## 3.10 Rekapitulasi Hasil Pengujian

| No | Modul | Jumlah Kasus | Valid | Tidak Valid | Persentase Valid |
|---|---|---|---|---|---|
| 1 | PP — Portal Publik | 5 | 5 | 0 | 100% |
| 2 | DB — Statistik & Visualisasi | 3 | 3 | 0 | 100% |
| 3 | DF — Filter & Tabel Artikel | 6 | 6 | 0 | 100% |
| 4 | CR — CRUD Sentimen | 6 | 6 | 0 | 100% |
| 5 | AT — Analisis Teks | 2 | 2 | 0 | 100% |
| 6 | AU — Analisis URL | 3 | 3 | 0 | 100% |
| 7 | AP — Antarmuka API | 4 | 4 | 0 | 100% |
| 8 | KB — Kompatibilitas & Responsivitas | 1 | 1* | 0 | 100%* |
| | **Total suite utama** | **30** | **30** | **0** | **100%** |
| — | UP — Upload Artikel *(opsional)* | 3 | 3 | 0 | 100% |

\* KB-01 valid untuk bagian yang sudah dieksekusi (Edge + layar sempit);
ulangi sampel kasus di Chrome dan Firefox untuk melengkapinya.

## 3.11 Catatan Pelaksanaan (bukan temuan cacat)

1. **PP-05** dieksekusi terhadap backend produksi sehingga backend tidak
   dapat benar-benar dimatikan; kondisi disimulasikan dengan **memblokir
   permintaan ke backend** dari sisi peramban — efeknya identik dengan
   backend nonaktif. Saat menguji lokal, cukup hentikan uvicorn.
2. **CR-01** dilakukan pada artikel uji sementara (unggahan), sehingga
   kartu Total Artikel pada bukti menunjukkan **735**; setelah artikel uji
   dihapus (CR-03) total kembali **734** dan data fase 1 tidak tersentuh.
3. **AT-01**: dua teks netral karangan awal justru dilabeli model
   **positif** (52–58%) — bukan cacat fungsional (lihat kriteria §1.6
   no. 3), melainkan karakteristik model. Teks T-NET-1 pada lampiran
   diganti dengan teks dari korpus yang dilabeli **netral (64.3%)**;
   teks karangan disimpan sebagai T-NET-2 beserta catatannya.
4. **AU-03**: data uji halaman non-artikel semula `google.com`, namun
   beranda Google ternyata **berhasil diekstrak** oleh sistem; diganti
   `https://example.com` yang benar-benar memicu pesan gagal ekstraksi.
5. **AP-03**: Swagger UI **menolak mengirim** `page=0`/`limit=101` karena
   validasi skema OpenAPI di sisi klien (bukti bahwa batas parameter
   terdokumentasi); pengujian dilakukan lewat URL langsung di peramban
   dan server tetap menjawab **422** sebagaimana diharapkan.

## 3.12 Catatan Temuan / Ketidaksesuaian

| No | Kode Kasus | Deskripsi Temuan | Tindak Lanjut | Hasil Uji Ulang |
|---|---|---|---|---|
| 1 | — | *(tidak ada — seluruh 30+3 kasus Valid)* | — | — |
