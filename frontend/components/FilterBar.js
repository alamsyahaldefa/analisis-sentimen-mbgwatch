"use client";

// Baris filter: dropdown Portal, rentang Tanggal, kotak Cari, tombol Terapkan.
export default function FilterBar({ portals, draft, setDraft, onApply, onReset }) {
  const ubah = (key) => (e) => setDraft({ ...draft, [key]: e.target.value });

  return (
    <div className="card mb-24">
      <form
        className="filter-row"
        onSubmit={(e) => {
          e.preventDefault();
          onApply();
        }}
      >
        <div className="field">
          <label>Portal</label>
          <select value={draft.portal} onChange={ubah("portal")}>
            <option value="">Semua portal</option>
            {portals.map((p) => (
              <option key={p} value={p}>
                {p}
              </option>
            ))}
          </select>
        </div>

        <div className="field">
          <label>Sentimen</label>
          <select value={draft.sentimen} onChange={ubah("sentimen")}>
            <option value="">Semua</option>
            <option value="positif">Positif</option>
            <option value="netral">Netral</option>
            <option value="negatif">Negatif</option>
          </select>
        </div>

        <div className="field">
          <label>Dari tanggal</label>
          <input type="date" value={draft.start} onChange={ubah("start")} />
        </div>

        <div className="field">
          <label>Sampai tanggal</label>
          <input type="date" value={draft.end} onChange={ubah("end")} />
        </div>

        <div className="field" style={{ flex: 1 }}>
          <label>Cari judul</label>
          <input
            type="text"
            placeholder="mis. keracunan, anggaran, SPPG..."
            value={draft.cari}
            onChange={ubah("cari")}
            style={{ minWidth: 200 }}
          />
        </div>

        <button type="submit" className="btn">
          Terapkan
        </button>
        <button type="button" className="btn btn-ghost" onClick={onReset}>
          Reset
        </button>
      </form>
    </div>
  );
}
