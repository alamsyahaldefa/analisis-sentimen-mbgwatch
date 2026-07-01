"use client";

import {
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

import { LABEL_KELAS, WARNA } from "../lib/constants";

// Donut "Distribusi Sentimen".
export default function SentimentDonut({ perKelas }) {
  const per = perKelas || { positif: 0, netral: 0, negatif: 0 };
  const data = [
    { name: LABEL_KELAS.positif, key: "positif", value: per.positif || 0 },
    { name: LABEL_KELAS.netral, key: "netral", value: per.netral || 0 },
    { name: LABEL_KELAS.negatif, key: "negatif", value: per.negatif || 0 },
  ];
  const kosong = data.every((d) => d.value === 0);

  return (
    <div className="card">
      <h2 className="section-title">Distribusi Sentimen</h2>
      {kosong ? (
        <p className="muted">Belum ada data untuk ditampilkan.</p>
      ) : (
        <div className="chart-wrap">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                innerRadius={70}
                outerRadius={105}
                paddingAngle={2}
                label={({ name, percent }) =>
                  `${name} ${(percent * 100).toFixed(0)}%`
                }
              >
                {data.map((d) => (
                  <Cell key={d.key} fill={WARNA[d.key]} />
                ))}
              </Pie>
              <Tooltip formatter={(v) => `${v} artikel`} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
