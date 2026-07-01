"use client";

import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { WARNA } from "../lib/constants";

// Line "Tren Sentimen per Bulan" (3 garis: positif/negatif/netral).
export default function TrendLine({ tren }) {
  const data = tren || [];

  return (
    <div className="card">
      <h2 className="section-title">Tren Sentimen per Bulan</h2>
      {data.length === 0 ? (
        <p className="muted">Belum ada data untuk ditampilkan.</p>
      ) : (
        <div className="chart-wrap">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ top: 10, right: 20, bottom: 0, left: -10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#eef2f7" />
              <XAxis dataKey="bulan" fontSize={12} />
              <YAxis allowDecimals={false} fontSize={12} />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="positif"
                name="Positif"
                stroke={WARNA.positif}
                strokeWidth={2}
                dot={{ r: 3 }}
              />
              <Line
                type="monotone"
                dataKey="netral"
                name="Netral"
                stroke={WARNA.netral}
                strokeWidth={2}
                dot={{ r: 3 }}
              />
              <Line
                type="monotone"
                dataKey="negatif"
                name="Negatif"
                stroke={WARNA.negatif}
                strokeWidth={2}
                dot={{ r: 3 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
