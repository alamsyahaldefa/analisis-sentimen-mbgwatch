"use client";

import { WARNA } from "../lib/constants";

// Empat kartu statistik: Total Artikel, % Positif, % Negatif, % Netral.
export default function StatCards({ statistik }) {
  const total = statistik?.total || 0;
  const per = statistik?.per_kelas || { positif: 0, netral: 0, negatif: 0 };

  const persen = (n) => (total > 0 ? ((n / total) * 100).toFixed(1) + "%" : "0%");

  const kartu = [
    { label: "Total Artikel", value: total.toLocaleString("id-ID"), warna: "var(--teks)" },
    { label: "Positif", value: persen(per.positif), warna: WARNA.positif },
    { label: "Negatif", value: persen(per.negatif), warna: WARNA.negatif },
    { label: "Netral", value: persen(per.netral), warna: WARNA.netral },
  ];

  return (
    <div className="grid grid-4 mb-24">
      {kartu.map((k) => (
        <div key={k.label} className="card stat-card">
          <div className="stat-label">{k.label}</div>
          <div className="stat-value" style={{ color: k.warna }}>
            {k.value}
          </div>
        </div>
      ))}
    </div>
  );
}
