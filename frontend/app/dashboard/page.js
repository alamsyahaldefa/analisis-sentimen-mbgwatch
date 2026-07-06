"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";

import ArticleTable from "../../components/ArticleTable";
import FilterBar from "../../components/FilterBar";
import PredictPanel from "../../components/PredictPanel";
// import UploadPanel from "../../components/UploadPanel"; // fitur upload sementara disembunyikan
import UrlPredictPanel from "../../components/UrlPredictPanel";
import SentimentDonut from "../../components/SentimentDonut";
import StatCards from "../../components/StatCards";
import TrendLine from "../../components/TrendLine";
import { fetchArtikel, fetchStatistik } from "../../lib/api";

const FILTER_KOSONG = { portal: "", sentimen: "", start: "", end: "", cari: "" };
const LIMIT = 10;

export default function Dashboard() {
  const [statistik, setStatistik] = useState(null);
  const [draft, setDraft] = useState(FILTER_KOSONG); // nilai input belum diterapkan
  const [filter, setFilter] = useState(FILTER_KOSONG); // filter yang diterapkan

  const [artikel, setArtikel] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);

  const [loadingTabel, setLoadingTabel] = useState(false);
  const [errorGlobal, setErrorGlobal] = useState("");

  const muatStatistik = useCallback(async () => {
    try {
      const s = await fetchStatistik();
      setStatistik(s);
    } catch (e) {
      setErrorGlobal(e.message);
    }
  }, []);

  const muatArtikel = useCallback(async (halaman, f) => {
    setLoadingTabel(true);
    try {
      const res = await fetchArtikel({ ...f, page: halaman, limit: LIMIT });
      setArtikel(res.data);
      setTotal(res.total);
    } catch (e) {
      setErrorGlobal(e.message);
      setArtikel([]);
      setTotal(0);
    } finally {
      setLoadingTabel(false);
    }
  }, []);

  useEffect(() => {
    muatStatistik();
    muatArtikel(1, FILTER_KOSONG);
  }, [muatStatistik, muatArtikel]);

  function terapkanFilter() {
    setErrorGlobal("");
    setFilter(draft);
    setPage(1);
    muatStatistik();
    muatArtikel(1, draft);
  }

  function resetFilter() {
    setErrorGlobal("");
    setDraft(FILTER_KOSONG);
    setFilter(FILTER_KOSONG);
    setPage(1);
    muatArtikel(1, FILTER_KOSONG);
  }

  function gantiHalaman(halaman) {
    setPage(halaman);
    muatArtikel(halaman, filter);
  }

  // Segarkan statistik + tabel setelah admin mengubah/menghapus sentimen (CRUD).
  function segarkanData() {
    muatStatistik();
    muatArtikel(page, filter);
  }

  return (
    <>
      <header className="header">
        <div className="container header-bar">
          <div>
            <h1>MBG Watch — Dashboard Admin</h1>
            <p>
              Analisis sentimen berita MBG (IndoBERT: negatif · netral · positif).
            </p>
          </div>
          <Link href="/" className="btn btn-ghost">
            ← Portal Publik
          </Link>
        </div>
      </header>

      <main className="container">
        {errorGlobal && (
          <div className="error-box mb-24">
            {errorGlobal} — pastikan backend berjalan di{" "}
            <code>http://localhost:8000</code>.
          </div>
        )}

        <FilterBar
          portals={statistik?.portals || []}
          draft={draft}
          setDraft={setDraft}
          onApply={terapkanFilter}
          onReset={resetFilter}
        />

        <StatCards statistik={statistik} />

        <div className="grid grid-2 mb-24">
          <SentimentDonut perKelas={statistik?.per_kelas} />
          <TrendLine tren={statistik?.tren_bulanan} />
        </div>

        {/* Fitur upload artikel sementara disembunyikan (aktifkan kembali
            dengan meng-uncomment import UploadPanel, handler selesaiUpload,
            dan blok <UploadPanel /> di sini). */}

        <div className="mb-24">
          <ArticleTable
            data={artikel}
            total={total}
            page={page}
            limit={LIMIT}
            loading={loadingTabel}
            onPageChange={gantiHalaman}
            onDataChanged={segarkanData}
          />
        </div>

        <div className="grid grid-2 mb-24">
          <UrlPredictPanel />
          <PredictPanel />
        </div>

        <footer className="muted" style={{ padding: "8px 0 40px" }}>
          MBG Watch · Tugas Akhir Analisis Sentimen · FastAPI + Next.js + IndoBERT.
        </footer>
      </main>
    </>
  );
}
