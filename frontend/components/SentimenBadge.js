// Badge sentimen berwarna (positif=hijau, negatif=merah, netral=biru).
export default function SentimenBadge({ sentimen }) {
  const s = (sentimen || "netral").toLowerCase();
  const kelas =
    s === "positif" ? "badge-positif" : s === "negatif" ? "badge-negatif" : "badge-netral";
  return <span className={`badge ${kelas}`}>{s}</span>;
}
