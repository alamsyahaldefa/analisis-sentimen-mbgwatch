# 2. Skenario dan Kasus Uji (Instrumen Pengujian Black Box)

Dokumen ini memuat **30 kasus uji suite utama** (8 modul: PP, DB, DF, CR,
AT, AU, AP, KB) dan **3 kasus lampiran opsional** (modul UP). Kasus dipilih
dan digabungkan agar seluruh fitur tetap tercakup dengan jumlah yang ringkas:
tiap kasus memuat prosedur, data uji, dan hasil yang diharapkan. Data
masukan terinci tersedia di `lampiran/data-uji.md`.

Konvensi kode: `XX-nn` — dua huruf kode modul, dua digit nomor urut.

> **Konvensi angka:** nilai persentase pada antarmuka ditampilkan dengan
> **pemisah desimal titik** (mis. `46.3%`, `keyakinan 97.6%`) karena
> pembulatan dilakukan fungsi JavaScript `toFixed()`. Jangan menandai kasus
> Tidak Valid hanya karena berharap format koma.

---

## 2.1 Modul PP — Portal Publik (halaman `/`) — 5 kasus

| Kode | Skenario Pengujian | Prosedur Pengujian | Data Uji | Hasil yang Diharapkan |
|---|---|---|---|---|
| PP-01 | Memuat portal publik & kelengkapan kartu berita | (1) Jalankan frontend & backend; (2) buka `http://localhost:3000/`; (3) amati 3–5 kartu teratas | — | Halaman termuat: bilah navigasi biru berlogo **MBGwatch**, judul **"Temuan Terbaru"**, chip kategori (**"Semua"** aktif + 7 kategori), kisi kartu berita (maks. 9 kartu awal) dan tombol **"Selengkapnya"**. Setiap kartu menampilkan: label kategori (maks. 2), lencana (pill) sentimen berwarna — Positif hijau / Negatif merah / Netral abu-abu — judul, cuplikan (±120 karakter, diakhiri "…" bila terpotong), **"Sumber: \<portal\>"**, dan tanggal format Indonesia (mis. "07 Jan 2026"). Judul tab peramban "MBG Watch — Analisis Sentimen Berita MBG" |
| PP-02 | Menyaring berita berdasarkan kategori & kembali ke "Semua" | (1) Klik salah satu chip kategori; (2) amati daftar; (3) klik chip **"Semua"** | Chip "Keracunan & Masalah Kesehatan" | Chip yang diklik menjadi aktif (biru tua); daftar dimuat ulang dari awal dan hanya berisi artikel kategori tersebut. Setelah klik "Semua", seluruh artikel kembali ditampilkan seperti kondisi awal |
| PP-03 | Memuat artikel bertahap ("Selengkapnya") hingga habis | (1) Pada salah satu kategori, klik **"Selengkapnya"** satu kali dan amati; (2) klik berulang hingga artikel kategori habis | Kategori dengan artikel sedikit | Setiap klik **menambahkan** 9 kartu berikutnya di bawah kartu lama (append — kartu lama tidak berubah). Setelah seluruh artikel termuat, tombol digantikan teks **"Semua N artikel telah ditampilkan."** |
| PP-04 | Navigasi portal ↔ dashboard | (1) Dari portal, klik tombol **"Dashboard"** pada navigasi (atau tautan "Dashboard Admin" di footer); (2) dari dashboard, klik **"← Portal Publik"** | — | Langkah (1) membawa peramban ke `/dashboard`; langkah (2) mengembalikan ke `/` |
| PP-05 | Penanganan backend tidak aktif *(negatif)* | (1) Hentikan proses backend (Ctrl+C pada uvicorn); (2) muat ulang halaman portal | Backend nonaktif | Aplikasi tidak *crash*: tampil kotak kesalahan merah berisi pesan kegagalan dan arahan **"pastikan backend berjalan di http://localhost:8000"**; tidak ada kartu berita. (Perilaku degradasi serupa berlaku pada dashboard: statistik 0, grafik "Belum ada data untuk ditampilkan.". Nyalakan kembali backend setelah kasus ini) |

## 2.2 Modul DB — Dashboard: Statistik & Visualisasi (halaman `/dashboard`) — 3 kasus

| Kode | Skenario Pengujian | Prosedur Pengujian | Data Uji | Hasil yang Diharapkan |
|---|---|---|---|---|
| DB-01 | Memuat halaman dashboard admin | Buka `http://localhost:3000/dashboard` | — | Halaman termuat lengkap: kepala halaman **"MBG Watch — Dashboard Admin"** + tombol **"← Portal Publik"**; kartu filter; 4 kartu statistik; kartu **"Distribusi Sentimen"** dan **"Tren Sentimen per Bulan"**; kartu **"Daftar Artikel"**; panel **"Analisis dari URL Berita"** dan **"Coba Sendiri — Analisis Teks Baru"** |
| DB-02 | Kebenaran kartu statistik | Amati keempat kartu statistik, bandingkan dengan data awal | Data awal 734 artikel | **Total Artikel: 734**; **Positif: 22.9%**; **Negatif: 46.3%**; **Netral: 30.8%** (warna sesuai sentimen; ketiga persentase berjumlah ≈ 100%) |
| DB-03 | Grafik donat distribusi & tren bulanan | Amati kedua kartu grafik; arahkan kursor ke segmen donat dan titik tren | — | Donat: 3 segmen warna standar (Positif hijau, Netral biru, Negatif merah), label nama + persen per segmen, legenda, *tooltip* **"N artikel"**. Tren: 3 garis Positif/Netral/Negatif, sumbu-X bulan **2026-01 s.d. 2026-06**, sumbu-Y bilangan bulat, *tooltip* nilai ketiga sentimen per bulan |

## 2.3 Modul DF — Dashboard: Filter & Tabel Artikel — 6 kasus

| Kode | Skenario Pengujian | Prosedur Pengujian | Data Uji | Hasil yang Diharapkan |
|---|---|---|---|---|
| DF-01 | Tampilan awal tabel & paginasi | (1) Amati kartu "Daftar Artikel" tanpa filter; (2) klik **"Berikutnya ›"**; (3) klik **"‹ Sebelumnya"** | — | Tabel berkolom **Judul, Portal, Tanggal, Sentimen, Aksi**; 10 baris terurut tanggal terbit terbaru; info **"Menampilkan 1–10 dari 734 artikel"**, **"Halaman 1 / 74"**; tombol "‹ Sebelumnya" **nonaktif** di halaman 1. Setelah (2): "Menampilkan 11–20 dari 734 artikel", halaman 2, isi berbeda. Setelah (3): kembali persis ke halaman 1 |
| DF-02 | Filter berdasarkan portal & sentimen | (1) Pilih **Portal** = "Detik", klik **Terapkan**, amati; (2) tambahkan **Sentimen** = "Negatif", Terapkan | Detik; negatif | Setelah (1): semua baris berkolom Portal = "Detik", total mengecil (< 734). Setelah (2): semua baris juga berlencana **negatif**; total makin kecil; jumlah halaman menyesuaikan |
| DF-03 | Filter rentang tanggal & kombinasi (AND) | (1) Kosongkan filter lain, isi **Dari**/**Sampai tanggal**, Terapkan; (2) gabungkan dengan Portal = Detik dan Sentimen = Negatif, Terapkan | 2026-06-01 s.d. 2026-06-30; lalu Detik + negatif + rentang yang sama | Setelah (1): semua baris bertanggal Juni 2026. Setelah (2): hasil memenuhi **ketiga** kriteria sekaligus (pada data awal ±69 artikel Detik negatif Juni 2026) |
| DF-04 | Pencarian judul | (1) Ketik kata kunci pada **Cari judul**; (2) klik **Terapkan** (atau tekan **Enter** — hasil harus sama) | Kata kunci: `keracunan` | Semua judul yang tampil memuat kata "keracunan" (tidak peka kapital); Enter memberi hasil identik dengan tombol Terapkan tanpa muat ulang penuh |
| DF-05 | Filter tanpa hasil *(negatif)* | (1) Ketik kata kunci acak; (2) Terapkan | Kata kunci: `xyzabc123` | Tabel menampilkan satu baris pesan **"Tidak ada artikel yang cocok dengan filter."**; info **"Menampilkan 0–0 dari 0 artikel"**; aplikasi tidak *error* |
| DF-06 | Mengatur ulang filter (Reset) | Setelah DF-05, klik **Reset** | — | Seluruh isian kembali kosong ("Semua portal", "Semua", tanggal & kata kunci kosong); tabel kembali menampilkan halaman 1 dari 734 artikel |

## 2.4 Modul CR — CRUD Sentimen (kolom Aksi pada tabel) — 6 kasus

| Kode | Skenario Pengujian | Prosedur Pengujian | Data Uji | Hasil yang Diharapkan |
|---|---|---|---|---|
| CR-01 | Mengubah label sentimen + persistensi | (1) Klik **✎** pada salah satu baris; (2) pilih kelas berbeda pada dropdown; (3) klik **✓**; (4) muat ulang halaman (F5) dan cari artikel tsb.; (5) cek kartu artikel yang sama di portal publik | Mis. netral → positif | Setelah (1): lencana berubah menjadi **dropdown** Positif/Netral/Negatif dengan nilai saat ini terpilih; tombol menjadi **✓**/**✕**. Setelah (3): lencana menampilkan sentimen **baru**; kartu statistik & grafik **ter-update otomatis** tanpa muat ulang. Setelah (4)–(5): label tetap baru — tersimpan permanen dan tercermin di portal publik |
| CR-02 | Membatalkan perubahan sentimen | (1) Klik **✎**; (2) pilih kelas berbeda; (3) klik **✕** | — | Mode ubah tertutup; lencana kembali menampilkan sentimen **lama**; tidak ada data berubah |
| CR-03 | Menghapus artikel (konfirmasi OK) | (1) Klik **🗑** pada salah satu baris; (2) pada dialog **'Hapus artikel "\<judul\>"?'** klik OK | Baris uji mana pun | Baris hilang dari tabel; total artikel pada info paginasi dan kartu **Total Artikel** berkurang 1; statistik/donat menyesuaikan |
| CR-04 | Membatalkan penghapusan | (1) Klik **🗑**; (2) pada dialog konfirmasi klik **Cancel/Batal** | — | Tidak ada perubahan: baris tetap ada, total tetap |
| CR-05 | Validasi API: nilai sentimen tidak valid *(negatif)* | Swagger (`/docs`): **PATCH /api/artikel/{id}** dengan id valid dan sentimen di luar 3 kelas | Body `{"sentimen": "bagus"}` | Respons **400** dengan pesan `"Sentimen tidak valid. Pilihan: negatif, netral, positif."`; data tidak berubah |
| CR-06 | Validasi API: id tidak terdaftar *(negatif)* | Swagger: (1) **PATCH /api/artikel/tidak-ada** body `{"sentimen": "netral"}`; (2) **DELETE /api/artikel/tidak-ada** | id `tidak-ada` | Keduanya merespons **404** dengan pesan `"Artikel tidak ditemukan."` |

## 2.5 Modul AT — Analisis Sentimen Teks (panel "Coba Sendiri") — 2 kasus

> Catatan: AT-01 menilai **fungsionalitas** (sistem mengembalikan label +
> keyakinan + probabilitas), bukan ketepatan label. Teks uji tersedia di
> `lampiran/data-uji.md`.

| Kode | Skenario Pengujian | Prosedur Pengujian | Data Uji | Hasil yang Diharapkan |
|---|---|---|---|---|
| AT-01 | Analisis teks tiga kelas sentimen | Untuk masing-masing teks uji: (1) tempel ke textarea; (2) klik **Analisis**; (3) catat label yang muncul | T-POS-1, T-NEG-1, T-NET-1 | Setiap analisis memunculkan kotak hasil: **"Hasil:"** + lencana sentimen, teks **"keyakinan NN.N%"** (pemisah desimal titik), dan 3 bilah probabilitas (Positif/Netral/Negatif) bertotal ≈ 100%. Label dicatat apa adanya (dugaan nada teks: positif / negatif / netral) |
| AT-02 | Validasi teks kosong *(negatif)* | (1) Muat ulang halaman agar panel bersih; (2) kosongkan textarea (atau isi spasi saja); (3) klik **Analisis** | `""` dan `"   "` | Muncul pesan **"Teks tidak boleh kosong."**; tidak ada permintaan yang dikirim ke server; tidak muncul hasil analisis baru |

## 2.6 Modul AU — Analisis Sentimen dari URL — 3 kasus

| Kode | Skenario Pengujian | Prosedur Pengujian | Data Uji | Hasil yang Diharapkan |
|---|---|---|---|---|
| AU-01 | Analisis URL artikel berita valid | (1) Tempel URL artikel berita MBG yang dapat diakses; (2) klik **Analisis URL** (amati tombol selama menunggu); (3) setelah hasil tampil, klik judul pada kotak hasil | URL U-VAL-1 (lihat lampiran) | Selama menunggu, tombol berubah **"Menganalisis..."** dan nonaktif. Kotak hasil menampilkan: **judul artikel** (tautan — saat diklik membuka artikel sumber di tab baru), **portal** dan tanggal terbit, baris **"Sentimen:"** + lencana + "keyakinan NN.N%", 3 bilah probabilitas, dan bagian lipat **"Teks yang dianalisis (judul + kalimat awal)"** |
| AU-02 | Validasi format URL *(negatif)* | (1) Klik **Analisis URL** dengan isian kosong; (2) masukkan URL tanpa `http://`, klik lagi | `""`; lalu `www.detik.com/berita-mbg` | (1) Pesan **"URL tidak boleh kosong."**; (2) pesan **"Masukkan URL lengkap diawali http:// atau https://"** — keduanya tanpa permintaan ke server |
| AU-03 | URL tidak terjangkau / bukan artikel *(negatif)* | (1) Analisis URL berdomain fiktif (tunggu — sistem mencoba ulang); (2) analisis URL halaman non-artikel | `https://situs-tidak-ada-xyz123.com/berita`; lalu `https://example.com` | (1) Kotak kesalahan berisi pesan kegagalan akses dari server (**"Gagal mengakses URL: tidak dapat terhubung ke server (periksa URL/koneksi)."**); (2) pesan kegagalan ekstraksi (**"Isi artikel tidak dapat diekstrak dari URL ini (halaman mungkin dirender JavaScript atau bukan artikel berita)."**). Aplikasi tetap stabil |

## 2.7 Modul AP — Antarmuka API Backend (via Swagger UI `/docs`) — 4 kasus

> Buka `http://localhost:8000/docs`, pilih endpoint, klik **Try it out**,
> isikan parameter/body, klik **Execute**, lalu amati *response code* dan
> *response body*.

| Kode | Skenario Pengujian | Endpoint & Masukan | Data Uji | Hasil yang Diharapkan |
|---|---|---|---|---|
| AP-01 | Daftar artikel: struktur & nilai bawaan | `GET /api/artikel` tanpa parameter | — | Kode **200**; body `{data, total, page, limit}` dengan `data` = 10 objek artikel (id, portal, tanggal_terbit, url, judul, teks, sentimen, confidence, kategori, sumber), `total` = 734, `page` = 1, `limit` = 10 |
| AP-02 | Statistik agregat | `GET /api/statistik` | — | Kode **200**; body memuat `total` (734), `per_kelas` (negatif 340, netral 226, positif 168), `tren_bulanan` (6 objek: 2026-01..2026-06), `portals` (10 portal), `per_kategori` (7 kategori) |
| AP-03 | Nilai batas parameter page & limit *(negatif)* | Buka langsung di peramban (atau cURL): (1) `<backend>/api/artikel?page=0`; (2) `<backend>/api/artikel?limit=101`; pembanding `page=1`/`limit=100`. *(Catatan: lewat Swagger UI, Execute diblokir validasi sisi klien karena batasnya terdokumentasi di skema OpenAPI — itu juga bukti)* | page=0; limit=101 | (1) dan (2) merespons **422** (galat validasi — batas page ≥ 1, limit ≤ 100); nilai pembanding merespons **200** |
| AP-04 | Validasi teks pada prediksi *(negatif)* | (1) `POST /api/prediksi` body `{"teks": ""}`; (2) body `{"teks": "   "}` | `""`; `"   "` | (1) Kode **422** (validasi skema: panjang minimum 1 karakter); (2) kode **400** dengan body `{"detail": "Teks tidak boleh kosong."}` |

## 2.8 Modul KB — Kompatibilitas & Responsivitas — 1 kasus

| Kode | Skenario Pengujian | Prosedur Pengujian | Data Uji | Hasil yang Diharapkan |
|---|---|---|---|---|
| KB-01 | Kompatibilitas peramban & responsivitas layar sempit | (1) Ulangi sampel kasus (PP-01, DB-01, DF-02, AT-01) di **Chrome**, **Edge**, dan **Firefox**; (2) Chrome DevTools → Device Toolbar, lebar ≤ 620 px; buka `/` dan `/dashboard` | Lebar 375–620 px | (1) Fungsi dan tampilan konsisten di ketiga peramban. (2) Portal: kisi berita **1 kolom**, tautan menu teks tersembunyi (tersisa logo + tombol Dashboard); dashboard: kartu statistik 2 kolom, grafik menumpuk 1 kolom, tabel dapat digulir horizontal; tidak ada elemen terpotong |

---

## 2.9 (Lampiran Opsional) Modul UP — Upload Artikel — 3 kasus

> Fitur upload artikel (pengganti scraping untuk demo) saat ini
> **dinonaktifkan pada antarmuka dashboard**, tetapi endpoint API-nya aktif.
> Sertakan dalam skripsi hanya bila fitur ini dibahas. Pengujian pada
> tingkat API via Swagger; data uji: `lampiran/contoh_artikel_upload.json`.

| Kode | Skenario Pengujian | Endpoint & Masukan | Data Uji | Hasil yang Diharapkan |
|---|---|---|---|---|
| UP-01 | Upload artikel valid; tampil terpadu, tersimpan terpisah | (1) `POST /api/artikel-upload` dengan 2 artikel (judul + teks; satu menyertakan portal/tanggal/url); (2) `GET /api/artikel?cari=<judul unggahan>` dan buka portal publik; (3) periksa folder backend | Isi `contoh_artikel_upload.json` | (1) Kode **200**; `berhasil` = 2 objek — `id` berawalan "up-", `sentimen` hasil prediksi model, `confidence`, `kategori` otomatis, `sumber` = "upload"; tanpa tanggal → diberi tanggal hari ini; tanpa portal → "Upload Admin"; `gagal` = []. (2) Artikel ditemukan di API dan tampil di portal; di tabel dashboard bertanda "upload". (3) Tersimpan di berkas terpisah `mbg_upload.db`; `mbg.db` (fase 1) tetap 734 |
| UP-02 | Masukan tidak lengkap / kosong *(negatif)* | (1) `POST /api/artikel-upload` dengan salah satu item tanpa teks di antara item valid; (2) body `{"artikel": []}` | `{"judul": "Uji", "teks": "   "}`; lalu `[]` | (1) Kode **200**; item valid masuk `berhasil`, item tak lengkap masuk `gagal` dengan pesan **"Judul dan teks wajib diisi."**. (2) Kode **422** (validasi minimal 1 artikel) |
| UP-03 | CRUD berlaku untuk artikel upload | (1) **PATCH** sentimen id "up-…" hasil UP-01; (2) **DELETE** id yang sama | id dari UP-01 | (1) 200 — sentimen berubah; (2) 200 — `{"status": "terhapus", ...}`; artikel hilang dari daftar |

---

### Catatan perluasan (opsional, di luar 30 kasus)

Bila diperlukan pendalaman, skenario berikut dapat ditambahkan: (a) respons
**503** ketika model belum dimuat (jalankan backend dengan `MBG_MODEL`
menunjuk folder fiktif → `POST /api/prediksi` merespons 503 dan panel
dashboard menampilkan pesannya); (b) penanganan backend nonaktif khusus
halaman dashboard (statistik 0, grafik "Belum ada data untuk ditampilkan.");
(c) indikator pemuatan "Memuat…"/"Memuat data..." saat berpindah halaman.
