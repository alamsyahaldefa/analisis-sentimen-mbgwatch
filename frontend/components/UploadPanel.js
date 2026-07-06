"use client";

import { useRef, useState } from "react";

import { uploadArtikel } from "../lib/api";
import SentimenBadge from "./SentimenBadge";

// Panel "Upload Artikel" (demo pengganti scraping): admin mengunggah file
// CSV/JSON berisi beberapa artikel, tiap artikel langsung dianalisis model
// IndoBERT lalu disimpan ke database upload (terpisah dari data fase 1) dan
// tampil di portal publik.

// Alias nama kolom -> field baku, agar file dari berbagai sumber tetap terbaca.
const ALIAS = {
  judul: ["judul", "title"],
  teks: ["teks", "isi", "konten", "content", "body", "clean_text"],
  portal: ["portal", "media", "sumber"],
  tanggal_terbit: ["tanggal_terbit", "tanggal", "date"],
  url: ["url", "link", "tautan"],
};

// Parser CSV kecil yang mendukung kutip ganda (koma/baris-baru di dalam sel).
function parseCsv(text) {
  const rows = [];
  let row = [], sel = "", dalamKutip = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (dalamKutip) {
      if (c === '"') {
        if (text[i + 1] === '"') { sel += '"'; i++; }
        else dalamKutip = false;
      } else sel += c;
    } else if (c === '"') {
      dalamKutip = true;
    } else if (c === ",") {
      row.push(sel); sel = "";
    } else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(sel); sel = "";
      if (row.some((s) => s.trim() !== "")) rows.push(row);
      row = [];
    } else sel += c;
  }
  row.push(sel);
  if (row.some((s) => s.trim() !== "")) rows.push(row);
  return rows;
}

// Normalisasi satu objek artikel sesuai ALIAS (kunci dicocokkan lowercase).
function normalisasi(obj) {
  const kecil = {};
  Object.entries(obj || {}).forEach(([k, v]) => {
    kecil[String(k).trim().toLowerCase()] = v;
  });
  const hasil = {};
  Object.entries(ALIAS).forEach(([baku, aliasList]) => {
    for (const a of aliasList) {
      if (kecil[a] !== undefined && kecil[a] !== null && String(kecil[a]).trim() !== "") {
        hasil[baku] = String(kecil[a]).trim();
        break;
      }
    }
  });
  return hasil;
}

// Baca isi file (CSV / JSON) menjadi daftar {judul, teks, portal?, ...}.
function parseFile(nama, text) {
  if (/\.json$/i.test(nama)) {
    let data = JSON.parse(text);
    if (data && !Array.isArray(data) && Array.isArray(data.artikel)) {
      data = data.artikel;
    }
    if (!Array.isArray(data)) {
      throw new Error("JSON harus berupa array artikel, atau objek {artikel: [...]}.");
    }
    return data.map(normalisasi);
  }
  // CSV: baris pertama = header
  const rows = parseCsv(text);
  if (rows.length < 2) {
    throw new Error("CSV kosong atau hanya berisi header.");
  }
  const header = rows[0].map((h) => h.trim().toLowerCase());
  return rows.slice(1).map((r) => {
    const obj = {};
    header.forEach((h, i) => { obj[h] = r[i]; });
    return normalisasi(obj);
  });
}

const CONTOH_CSV = `judul,teks,portal,tanggal_terbit,url
"Program MBG Jangkau 1 Juta Siswa","Pemerintah mengumumkan program MBG kini menjangkau lebih dari satu juta siswa di seluruh Indonesia. Distribusi berjalan lancar di sebagian besar daerah.",Kompas,2026-07-01,https://contoh.com/berita-1
"Puluhan Siswa Diduga Keracunan Menu MBG","Puluhan siswa dilarikan ke puskesmas setelah menyantap menu MBG. Dinas kesehatan masih menyelidiki penyebabnya.",Detik,2026-07-02,`;

export default function UploadPanel({ onSelesai }) {
  const fileRef = useRef(null);
  const [namaFile, setNamaFile] = useState("");
  const [items, setItems] = useState([]);
  const [hasil, setHasil] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function resetInput() {
    setNamaFile("");
    setItems([]);
    if (fileRef.current) fileRef.current.value = "";
  }

  async function pilihFile(e) {
    const f = e.target.files?.[0];
    setError("");
    setHasil(null);
    if (!f) {
      resetInput();
      return;
    }
    try {
      const text = await f.text();
      const data = parseFile(f.name, text).filter((a) => a.judul || a.teks);
      if (data.length === 0) {
        throw new Error("Tidak ada artikel yang terbaca dari file ini.");
      }
      const lengkap = data.filter((a) => a.judul && a.teks);
      if (lengkap.length === 0) {
        throw new Error("Setiap artikel butuh kolom 'judul' dan 'teks' (atau 'isi').");
      }
      setNamaFile(f.name);
      setItems(lengkap);
      if (lengkap.length < data.length) {
        setError(`${data.length - lengkap.length} baris dilewati karena judul/teks kosong.`);
      }
    } catch (err) {
      resetInput();
      setError(err.message || "File tidak dapat dibaca.");
    }
  }

  async function analisis() {
    if (items.length === 0) return;
    setLoading(true);
    setError("");
    setHasil(null);
    try {
      const r = await uploadArtikel(items);
      setHasil(r);
      resetInput();
      if (r.berhasil.length > 0 && onSelesai) onSelesai();
    } catch (e) {
      setError(e.message || "Gagal mengunggah artikel.");
    } finally {
      setLoading(false);
    }
  }

  function unduhContoh() {
    const blob = new Blob([CONTOH_CSV], { type: "text/csv;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "contoh_artikel_mbg.csv";
    a.click();
    URL.revokeObjectURL(a.href);
  }

  return (
    <div className="card">
      <h2 className="section-title">Upload Artikel (Pengganti Scraping)</h2>
      <p className="muted" style={{ marginTop: 0 }}>
        Unggah file <strong>CSV</strong> atau <strong>JSON</strong> berisi beberapa
        artikel sekaligus. Setiap artikel langsung dianalisis model IndoBERT dan
        disimpan ke database upload (terpisah dari data fase 1), lalu tampil di
        portal publik.
      </p>

      <div className="upload-row">
        <input
          ref={fileRef}
          type="file"
          accept=".csv,.json,application/json,text/csv"
          onChange={pilihFile}
          className="upload-file"
        />
        <button className="btn" onClick={analisis} disabled={loading || items.length === 0}>
          {loading
            ? "Menganalisis..."
            : items.length > 0
            ? `Analisis & Simpan ${items.length} Artikel`
            : "Analisis & Simpan"}
        </button>
      </div>

      <details style={{ marginTop: 10 }}>
        <summary className="muted" style={{ cursor: "pointer" }}>
          Format file yang diterima
        </summary>
        <div className="muted" style={{ fontSize: 13, marginTop: 6, lineHeight: 1.6 }}>
          Kolom wajib: <code>judul</code> dan <code>teks</code> (alias{" "}
          <code>isi</code>). Kolom opsional: <code>portal</code>,{" "}
          <code>tanggal_terbit</code> (YYYY-MM-DD, default hari ini), <code>url</code>.
          JSON berupa array objek dengan kunci yang sama.{" "}
          <button className="btn-link" onClick={unduhContoh} type="button">
            Unduh contoh CSV
          </button>
        </div>
      </details>

      {namaFile && items.length > 0 && (
        <div className="hasil-prediksi" style={{ marginTop: 12 }}>
          <strong>{namaFile}</strong> — {items.length} artikel siap dianalisis:
          <ul className="upload-daftar">
            {items.slice(0, 5).map((a, i) => (
              <li key={i}>{a.judul}</li>
            ))}
            {items.length > 5 && (
              <li className="muted">… dan {items.length - 5} artikel lainnya</li>
            )}
          </ul>
        </div>
      )}

      {error && (
        <div className="error-box" style={{ marginTop: 12 }}>
          {error}
        </div>
      )}

      {hasil && (
        <div className="hasil-prediksi">
          <strong>
            {hasil.berhasil.length} artikel dianalisis &amp; disimpan.
          </strong>{" "}
          <span className="muted">
            Artikel kini tampil di portal publik dan tabel di atas.
          </span>
          <ul className="upload-daftar">
            {hasil.berhasil.map((a) => (
              <li key={a.id}>
                <SentimenBadge sentimen={a.sentimen} />{" "}
                <span style={{ marginLeft: 6 }}>{a.judul}</span>{" "}
                <span className="muted">
                  ({((a.confidence || 0) * 100).toFixed(1)}%)
                </span>
              </li>
            ))}
          </ul>
          {hasil.gagal.length > 0 && (
            <div className="error-box" style={{ marginTop: 10 }}>
              {hasil.gagal.length} artikel gagal:{" "}
              {hasil.gagal.map((g) => `${g.judul} (${g.error})`).join("; ")}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
