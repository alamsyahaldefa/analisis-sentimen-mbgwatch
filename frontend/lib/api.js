// Klien API ke backend FastAPI.
const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/** Ambil statistik agregat untuk dashboard. */
export async function fetchStatistik() {
  const res = await fetch(`${BASE}/api/statistik`);
  if (!res.ok) throw new Error("Gagal memuat statistik dari server.");
  return res.json();
}

/** Ambil daftar artikel dengan filter + paginasi. */
export async function fetchArtikel(params = {}) {
  const q = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== "") q.append(k, v);
  });
  const res = await fetch(`${BASE}/api/artikel?${q.toString()}`);
  if (!res.ok) throw new Error("Gagal memuat daftar artikel dari server.");
  return res.json();
}

async function postJson(path, body, pesanDefault) {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    let pesan = pesanDefault;
    try {
      const e = await res.json();
      if (e.detail) pesan = typeof e.detail === "string" ? e.detail : pesan;
    } catch (_) {
      /* abaikan */
    }
    throw new Error(pesan);
  }
  return res.json();
}

/** Prediksi sentimen teks baru. */
export async function prediksiTeks(teks) {
  return postJson("/api/prediksi", { teks }, "Gagal melakukan prediksi.");
}

/** Prediksi sentimen dari URL berita (di-scrape lalu dianalisis). */
export async function prediksiUrl(url) {
  return postJson(
    "/api/prediksi-url",
    { url },
    "Gagal menganalisis URL. Pastikan tautan benar dan dapat diakses."
  );
}
