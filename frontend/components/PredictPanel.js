"use client";

import { useState } from "react";

import { prediksiTeks } from "../lib/api";
import { KELAS, LABEL_KELAS, WARNA } from "../lib/constants";
import SentimenBadge from "./SentimenBadge";

// Panel "Coba Sendiri": textarea + tombol Analisis + hasil prediksi.
export default function PredictPanel() {
  const [teks, setTeks] = useState("");
  const [hasil, setHasil] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function analisis() {
    if (!teks.trim()) {
      setError("Teks tidak boleh kosong.");
      return;
    }
    setLoading(true);
    setError("");
    setHasil(null);
    try {
      const r = await prediksiTeks(teks.trim());
      setHasil(r);
    } catch (e) {
      setError(e.message || "Gagal melakukan prediksi.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">
      <h2 className="section-title">Analisis Teks Baru</h2>
      <p className="muted" style={{ marginTop: 0 }}>
        Tempel potongan teks/berita tentang MBG, lalu klik Analisis untuk melihat
        prediksi sentimennya.
      </p>

      <textarea
        value={teks}
        onChange={(e) => setTeks(e.target.value)}
        placeholder="Contoh: Program Makan Bergizi Gratis dinilai berhasil meningkatkan gizi siswa di sejumlah daerah..."
      />

      <div style={{ marginTop: 12 }}>
        <button className="btn" onClick={analisis} disabled={loading}>
          {loading ? "Menganalisis..." : "Analisis"}
        </button>
      </div>

      {error && (
        <div className="error-box" style={{ marginTop: 12 }}>
          {error}
        </div>
      )}

      {hasil && (
        <div className="hasil-prediksi">
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <span style={{ fontWeight: 600 }}>Hasil:</span>
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
        </div>
      )}
    </div>
  );
}
