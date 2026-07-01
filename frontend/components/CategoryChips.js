"use client";

// Baris chip kategori topik. "Semua" + daftar kategori dari statistik.
export default function CategoryChips({ kategoriList, aktif, onPilih }) {
  const semua = [{ nama: "", label: "Semua" }].concat(
    kategoriList.map((k) => ({ nama: k, label: k }))
  );

  return (
    <div className="chips">
      {semua.map((c) => (
        <button
          key={c.label}
          className={`chip ${aktif === c.nama ? "chip--aktif" : ""}`}
          onClick={() => onPilih(c.nama)}
        >
          {c.label}
        </button>
      ))}
    </div>
  );
}
