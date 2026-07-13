# Pengujian Sistem — MBG Watch (Black Box Testing)

Folder ini berisi dokumentasi lengkap pengujian sistem **MBG Watch — Analisis
Sentimen Berita Program Makan Bergizi Gratis (MBG)** menggunakan metode
**Black Box Testing**. Dokumen disusun sebagai dasar penulisan **BAB IV,
Subbab 4.5 — Hasil dan Pembahasan Pengujian Sistem** pada Tugas Akhir.

## Isi Folder

| Berkas | Isi | Kegunaan |
|---|---|---|
| `01-rencana-pengujian.md` | Rencana pengujian: tujuan, ruang lingkup, metode, teknik perancangan kasus uji, lingkungan, kriteria kelulusan | Dasar Subbab 4.5.1 (metode & lingkungan) |
| `02-skenario-dan-kasus-uji.md` | Instrumen pengujian: **30 kasus uji utama** (8 modul) — kode, skenario, prosedur, data uji, hasil yang diharapkan | Dasar Subbab 4.5.2 (skenario) & lampiran skripsi |
| `03-hasil-pengujian.md` | Lembar hasil pengujian (draf terisi) + rekapitulasi per modul | Dasar Subbab 4.5.3 (hasil) — **wajib dikonfirmasi dengan eksekusi nyata** |
| `04-draf-bab-4-subbab-4-5.md` | Draf naskah Subbab 4.5 siap adaptasi (4.5.1 s.d. 4.5.4) | Kerangka tulisan skripsi |
| `05-panduan-pelaksanaan.md` | Langkah menjalankan sistem, mengeksekusi tiap kelompok kasus uji, dan mendokumentasikan bukti | Pegangan saat melakukan pengujian |
| `lampiran/data-uji.md` | Data uji: teks positif/negatif/netral, URL uji, nilai filter | Bahan masukan saat eksekusi |
| `lampiran/kasus-uji-rekap.csv` | Rekap seluruh kasus uji (pemisah `;`, siap dibuka di Excel) | Impor cepat ke tabel Word/Excel |
| `lampiran/contoh_artikel_upload.csv` / `.json` | Data uji fitur upload artikel (lampiran opsional) | Pengujian modul UP (tingkat API) |
| `bukti/` | Tempat menyimpan tangkapan layar bukti pengujian | Lampiran skripsi |

## Ringkasan Kasus Uji

| Kode | Modul | Jumlah |
|---|---|---|
| PP | Portal Publik | 5 |
| DB | Dashboard — Statistik & Visualisasi | 3 |
| DF | Dashboard — Filter & Tabel Artikel | 6 |
| CR | CRUD Sentimen (kolom Aksi) | 6 |
| AT | Analisis Sentimen Teks | 2 |
| AU | Analisis Sentimen dari URL | 3 |
| AP | Antarmuka API (backend) | 4 |
| KB | Kompatibilitas & Responsivitas | 1 |
| **Total suite utama** | | **30** |
| UP | *(Lampiran/opsional)* Upload Artikel — fitur nonaktif di UI, diuji tingkat API | 3 |

Kasus dipilih yang paling penting per fitur (skenario serumpun digabung);
ide perluasan tercantum di bagian "Catatan perluasan" pada dokumen 02.

## Cara Menggunakan

1. Baca `01-rencana-pengujian.md` untuk memahami metode dan lingkup.
2. Siapkan sistem sesuai `05-panduan-pelaksanaan.md` (lokal atau produksi).
3. Eksekusi kasus uji pada `02-skenario-dan-kasus-uji.md` satu per satu,
   memakai masukan dari `lampiran/data-uji.md`.
4. Isi/koreksi kolom **Hasil Aktual** dan **Kesimpulan** pada
   `03-hasil-pengujian.md`; simpan tangkapan layar ke folder `bukti/`.
5. Salin/adaptasi `04-draf-bab-4-subbab-4-5.md` ke naskah skripsi, sesuaikan
   angka rekap dengan hasil eksekusi Anda.

## Catatan Penting (baca sebelum dipakai di skripsi)

1. **Kolom "Hasil Aktual" pada dokumen 03 adalah draf** yang ditulis
   berdasarkan perilaku yang dirancang pada kode dan (untuk sebagian kasus
   API) hasil pengujian otomatis pengembang. **Anda tetap wajib mengeksekusi
   setiap kasus pada sistem yang berjalan** dan menyesuaikan isi kolom bila
   hasil nyata berbeda — kejujuran data pengujian dinilai penguji sidang.
2. **Pengujian black box menilai fungsionalitas, bukan akurasi model.**
   Pada kasus AT-01 dan AU-01, yang diuji adalah *sistem mengembalikan label
   sentimen beserta tingkat keyakinan dan probabilitas* — bukan apakah label
   itu benar secara linguistik. Evaluasi ketepatan model (akurasi, F1-score,
   confusion matrix) dibahas pada subbab evaluasi model, terpisah dari subbab
   ini. Bila model memberi label di luar dugaan pada teks uji, catat apa
   adanya; itu bukan kegagalan fungsional.
3. Angka acuan dataset awal: **734 artikel** (negatif 340 = 46,3%; netral
   226 = 30,8%; positif 168 = 22,9%), 10 portal, rentang terbit
   7 Januari – 8 Juni 2026. Angka ini berubah bila Anda menghapus/mengubah
   artikel saat menguji modul CR — jalankan modul CR paling akhir, atau
   catat selisihnya.

---
*Disusun: 9 Juli 2026 · Sistem: MBG Watch (Next.js + FastAPI + IndoBERT)*
