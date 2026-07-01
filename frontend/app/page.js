"use client";

import { useCallback, useEffect, useState } from "react";

import CategoryChips from "../components/CategoryChips";
import NewsCard from "../components/NewsCard";
import PortalNav from "../components/PortalNav";
import { fetchArtikel, fetchStatistik } from "../lib/api";

const LIMIT = 9;

export default function PortalPublik() {
  const [kategoriList, setKategoriList] = useState([]);
  const [kategoriAktif, setKategoriAktif] = useState("");

  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Ambil daftar kategori untuk chip
  useEffect(() => {
    fetchStatistik()
      .then((s) => setKategoriList(Object.keys(s.per_kategori || {})))
      .catch((e) => setError(e.message));
  }, []);

  // Muat artikel (replace bila halaman 1, append bila lebih)
  const muat = useCallback(async (halaman, kategori) => {
    setLoading(true);
    setError("");
    try {
      const res = await fetchArtikel({ kategori, page: halaman, limit: LIMIT });
      setTotal(res.total);
      setItems((prev) => (halaman === 1 ? res.data : prev.concat(res.data)));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  // Muat ulang saat kategori berubah
  useEffect(() => {
    setPage(1);
    muat(1, kategoriAktif);
  }, [kategoriAktif, muat]);

  function pilihKategori(nama) {
    setKategoriAktif(nama);
  }

  function selengkapnya() {
    const next = page + 1;
    setPage(next);
    muat(next, kategoriAktif);
  }

  const adaLagi = items.length < total;

  return (
    <>
      <PortalNav />

      <main className="portal-main">
        <div className="container">
          <h1 className="portal-title">Temuan Terbaru</h1>
          <p className="portal-subtitle">
            Pantauan berita Program Makan Bergizi Gratis (MBG) beserta analisis
            sentimennya.
          </p>

          <CategoryChips
            kategoriList={kategoriList}
            aktif={kategoriAktif}
            onPilih={pilihKategori}
          />

          {error && (
            <div className="error-box" style={{ marginTop: 16 }}>
              {error} — pastikan backend berjalan di{" "}
              <code>http://localhost:8000</code>.
            </div>
          )}

          <div className="news-grid">
            {items.map((a) => (
              <NewsCard key={a.id} artikel={a} />
            ))}
          </div>

          {!loading && items.length === 0 && !error && (
            <p className="muted" style={{ textAlign: "center", padding: "40px 0" }}>
              Belum ada artikel pada kategori ini.
            </p>
          )}

          <div className="portal-more">
            {loading ? (
              <span className="muted">Memuat…</span>
            ) : adaLagi ? (
              <button className="btn-pill" onClick={selengkapnya}>
                Selengkapnya
              </button>
            ) : (
              items.length > 0 && (
                <span className="muted">Semua {total} artikel telah ditampilkan.</span>
              )
            )}
          </div>
        </div>
      </main>

      <footer className="portal-footer">
        <div className="container">
          MBG Watch · Analisis Sentimen Berita Makan Bergizi Gratis ·
          <a href="/dashboard"> Dashboard Admin</a>
        </div>
      </footer>
    </>
  );
}
