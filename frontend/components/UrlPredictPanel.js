"use client";

import { useState } from "react";

import { prediksiUrl } from "../lib/api";
import { KELAS, LABEL_KELAS, WARNA } from "../lib/constants";
import SentimenBadge from "./SentimenBadge";

// Panel "Analisis dari URL": admin menempel tautan berita, backend men-scrape
// isinya lalu model IndoBERT memprediksi sentimennya.
export default function UrlPredictPanel() {
  const [url, setUrl] = useState("");
  const [hasil, setHasil] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function analisis() {
    const u = url.trim();
    if (!u) {
      setError("URL tidak boleh kosong.");
      return;
    }
    if (!/^https?:\/\//i.test(u)) {
      setError("Masukkan URL lengkap diawali http:// atau https://");
      return;
    }
    setLoading(true);
    setError("");
    setHasil(null);
    try {
      const r = await prediksiUrl(u);
      setHasil(r);
    } catch (e) {
      setError(e.message || "Gagal menganalisis URL.");
    } finally {
      setLoading(false);
    }
  }

  function onKeyDown(e) {
    if (e.key === "Enter") analisis();
  }

  return (
    <div className="card">
      <h2 className="section-title">Analisis dari URL Berita</h2>
      <p className="muted" style={{ marginTop: 0 }}>
        Tempel tautan artikel berita MBG. Sistem akan mengambil judul dan isinya
        secara otomatis, lalu memprediksi sentimennya dengan model IndoBERT.
      </p>

      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        <input
          type="url"
          className="url-input"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder="https://www.detik.com/.../artikel-mbg"
          style={{ flex: "1 1 320px", minWidth: 0 }}
        />
        <button className="btn" onClick={analisis} disabled={loading}>
          {loading ? "Menganalisis..." : "Analisis URL"}
        </button>
      </div>

      {error && (
        <div className="error-box" style={{ marginTop: 12 }}>
          {error}
        </div>
      )}

      {hasil && (
        <div className="hasil-prediksi">
          {/* Metadata artikel hasil ekstraksi */}
          <div style={{ marginBottom: 12 }}>
            <a
              href={hasil.url}
              target="_blank"
              rel="noopener noreferrer"
              style={{ fontWeight: 600, textDecoration: "none" }}
            >
              {hasil.judul}
            </a>
            <div className="muted" style={{ fontSize: 13, marginTop: 4 }}>
              {hasil.portal}
              {hasil.tanggal_terbit ? ` · ${hasil.tanggal_terbit}` : ""}
            </div>
          </div>

          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <span style={{ fontWeight: 600 }}>Sentimen:</span>
            <SentimenBadge sentimen={hasil.sentimen} />
            <span className="muted">
              keyakinan {(hasil.confidence * 100).toFixed(1)}%
            </span>
          </div>

          <div style={{ marginTop: 12 }}>
            {KELAS.map((k) => {
              const nilai = hasil.probabilitas?.[k] || 0;
              return (
                <div className="prob-row" key={k}>
                  <span className="prob-label">{LABEL_KELAS[k]}</span>
                  <span className="prob-bar-track">
                    <span
                      className="prob-bar-fill"
                      style={{
                        width: `${(nilai * 100).toFixed(1)}%`,
                        background: WARNA[k],
                      }}
                    />
                  </span>
                  <span className="prob-val">{(nilai * 100).toFixed(1)}%</span>
                </div>
              );
            })}
          </div>

          {hasil.teks_dianalisis && (
            <details style={{ marginTop: 12 }}>
              <summary className="muted" style={{ cursor: "pointer" }}>
                Teks yang dianalisis (judul + kalimat awal)
              </summary>
              <p className="muted" style={{ fontSize: 13, marginTop: 6 }}>
                {hasil.teks_dianalisis}
              </p>
            </details>
          )}
        </div>
      )}
    </div>
  );
}
