"use client";

import { useState } from "react";

import { hapusArtikel, ubahSentimen } from "../lib/api";
import { KELAS, LABEL_KELAS } from "../lib/constants";
import SentimenBadge from "./SentimenBadge";

// Tabel "Daftar Artikel" dengan paginasi + aksi admin (ubah sentimen / hapus).
export default function ArticleTable({ data, total, page, limit, loading, onPageChange, onDataChanged }) {
  const totalHalaman = Math.max(1, Math.ceil(total / limit));
  const mulai = total === 0 ? 0 : (page - 1) * limit + 1;
  const akhir = Math.min(page * limit, total);

  // Baris yang sedang diedit sentimennya + nilai pilihan sementara
  const [editId, setEditId] = useState(null);
  const [draftSentimen, setDraftSentimen] = useState("");
  const [sibukId, setSibukId] = useState(null); // baris yang sedang diproses
  const [errorAksi, setErrorAksi] = useState("");

  const formatTanggal = (t) => {
    if (!t) return "-";
    const d = new Date(t);
    if (isNaN(d)) return t;
    return d.toLocaleDateString("id-ID", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    });
  };

  function mulaiEdit(a) {
    setErrorAksi("");
    setEditId(a.id);
    setDraftSentimen(a.sentimen || "netral");
  }

  function batalEdit() {
    setEditId(null);
    setDraftSentimen("");
  }

  async function simpanSentimen(a) {
    if (draftSentimen === a.sentimen) {
      batalEdit();
      return;
    }
    setSibukId(a.id);
    setErrorAksi("");
    try {
      await ubahSentimen(a.id, draftSentimen, a.sumber);
      batalEdit();
      if (onDataChanged) onDataChanged();
    } catch (e) {
      setErrorAksi(e.message || "Gagal mengubah sentimen.");
    } finally {
      setSibukId(null);
    }
  }

  async function hapus(a) {
    const yakin = window.confirm(
      `Hapus artikel "${a.judul || "(tanpa judul)"}"?`
    );
    if (!yakin) return;
    setSibukId(a.id);
    setErrorAksi("");
    try {
      await hapusArtikel(a.id, a.sumber);
      if (onDataChanged) onDataChanged();
    } catch (e) {
      setErrorAksi(e.message || "Gagal menghapus artikel.");
    } finally {
      setSibukId(null);
    }
  }

  return (
    <div className="card">
      <h2 className="section-title">Daftar Artikel</h2>

      {errorAksi && (
        <div className="error-box" style={{ marginBottom: 10 }}>
          {errorAksi}
        </div>
      )}

      <div style={{ overflowX: "auto" }}>
        <table>
          <thead>
            <tr>
              <th style={{ width: "46%" }}>Judul</th>
              <th>Portal</th>
              <th>Tanggal</th>
              <th>Sentimen</th>
              <th style={{ textAlign: "right" }}>Aksi</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={5} className="muted" style={{ textAlign: "center" }}>
                  Memuat data...
                </td>
              </tr>
            ) : data.length === 0 ? (
              <tr>
                <td colSpan={5} className="muted" style={{ textAlign: "center" }}>
                  Tidak ada artikel yang cocok dengan filter.
                </td>
              </tr>
            ) : (
              data.map((a) => {
                const sibuk = sibukId === a.id;
                return (
                  <tr key={a.id}>
                    <td>
                      {a.url ? (
                        <a href={a.url} target="_blank" rel="noopener noreferrer">
                          {a.judul || "(tanpa judul)"}
                        </a>
                      ) : (
                        a.judul || "(tanpa judul)"
                      )}
                    </td>
                    <td>
                      {a.portal || "-"}
                      {a.sumber === "upload" && (
                        <span className="tag-upload">upload</span>
                      )}
                    </td>
                    <td>{formatTanggal(a.tanggal_terbit)}</td>
                    <td>
                      {editId === a.id ? (
                        <select
                          className="select-sentimen"
                          value={draftSentimen}
                          onChange={(e) => setDraftSentimen(e.target.value)}
                          disabled={sibuk}
                        >
                          {KELAS.map((k) => (
                            <option key={k} value={k}>
                              {LABEL_KELAS[k]}
                            </option>
                          ))}
                        </select>
                      ) : (
                        <SentimenBadge sentimen={a.sentimen} />
                      )}
                    </td>
                    <td className="td-aksi">
                      {editId === a.id ? (
                        <>
                          <button
                            className="btn-aksi btn-aksi--simpan"
                            title="Simpan sentimen"
                            disabled={sibuk}
                            onClick={() => simpanSentimen(a)}
                          >
                            {sibuk ? "…" : "✓"}
                          </button>
                          <button
                            className="btn-aksi"
                            title="Batal"
                            disabled={sibuk}
                            onClick={batalEdit}
                          >
                            ✕
                          </button>
                        </>
                      ) : (
                        <>
                          <button
                            className="btn-aksi"
                            title="Ubah sentimen"
                            disabled={sibuk}
                            onClick={() => mulaiEdit(a)}
                          >
                            ✎
                          </button>
                          <button
                            className="btn-aksi btn-aksi--hapus"
                            title="Hapus artikel"
                            disabled={sibuk}
                            onClick={() => hapus(a)}
                          >
                            {sibuk ? "…" : "🗑"}
                          </button>
                        </>
                      )}
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      <div className="pagination">
        <span>
          Menampilkan {mulai}–{akhir} dari {total.toLocaleString("id-ID")} artikel
        </span>
        <div className="pages">
          <button
            className="btn btn-ghost"
            disabled={page <= 1 || loading}
            onClick={() => onPageChange(page - 1)}
          >
            ‹ Sebelumnya
          </button>
          <span>
            Halaman {page} / {totalHalaman}
          </span>
          <button
            className="btn btn-ghost"
            disabled={page >= totalHalaman || loading}
            onClick={() => onPageChange(page + 1)}
          >
            Berikutnya ›
          </button>
        </div>
      </div>
    </div>
  );
}
