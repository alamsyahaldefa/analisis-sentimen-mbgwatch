"use client";

import { LABEL_KELAS } from "../lib/constants";

// Kartu berita di portal publik.
export default function NewsCard({ artikel }) {
  const { judul, teks, sentimen, kategori, portal, tanggal_terbit, url } = artikel;

  const s = (sentimen || "netral").toLowerCase();
  const badgeKelas =
    s === "positif" ? "pill--positif" : s === "negatif" ? "pill--negatif" : "pill--netral";

  // kategori disimpan dipisah '|', tampilkan maksimal 2 agar rapi
  const kats = (kategori || "").split("|").filter(Boolean).slice(0, 2);

  const tanggal = (() => {
    if (!tanggal_terbit) return "";
    const d = new Date(tanggal_terbit);
    return isNaN(d)
      ? tanggal_terbit
      : d.toLocaleDateString("id-ID", { day: "2-digit", month: "short", year: "numeric" });
  })();

  const snippet = (teks || "").slice(0, 120).trim();

  return (
    <article className="news-card">
      <div className="news-card__top">
        <span className="news-card__kats">{kats.join(", ")}</span>
        <span className={`pill ${badgeKelas}`}>{LABEL_KELAS[s] || s}</span>
      </div>

      <h3 className="news-card__title">
        {url ? (
          <a href={url} target="_blank" rel="noopener noreferrer">
            {judul || "(tanpa judul)"}
          </a>
        ) : (
          judul || "(tanpa judul)"
        )}
      </h3>

      <p className="news-card__snippet">{snippet}{snippet.length >= 120 ? "…" : ""}</p>

      <div className="news-card__footer">
        <span>Sumber: {portal || "-"}</span>
        {tanggal && <span>{tanggal}</span>}
      </div>
    </article>
  );
}
