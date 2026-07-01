"use client";

import SentimenBadge from "./SentimenBadge";

// Tabel "Daftar Artikel" dengan paginasi.
export default function ArticleTable({ data, total, page, limit, loading, onPageChange }) {
  const totalHalaman = Math.max(1, Math.ceil(total / limit));
  const mulai = total === 0 ? 0 : (page - 1) * limit + 1;
  const akhir = Math.min(page * limit, total);

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

  return (
    <div className="card">
      <h2 className="section-title">Daftar Artikel</h2>

      <div style={{ overflowX: "auto" }}>
        <table>
          <thead>
            <tr>
              <th style={{ width: "52%" }}>Judul</th>
              <th>Portal</th>
              <th>Tanggal</th>
              <th>Sentimen</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={4} className="muted" style={{ textAlign: "center" }}>
                  Memuat data...
                </td>
              </tr>
            ) : data.length === 0 ? (
              <tr>
                <td colSpan={4} className="muted" style={{ textAlign: "center" }}>
                  Tidak ada artikel yang cocok dengan filter.
                </td>
              </tr>
            ) : (
              data.map((a) => (
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
                  <td>{a.portal || "-"}</td>
                  <td>{formatTanggal(a.tanggal_terbit)}</td>
                  <td>
                    <SentimenBadge sentimen={a.sentimen} />
                  </td>
                </tr>
              ))
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
