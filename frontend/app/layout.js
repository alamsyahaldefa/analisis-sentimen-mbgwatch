import "./globals.css";

export const metadata = {
  title: "MBG Watch — Analisis Sentimen Berita MBG",
  description:
    "Dashboard analisis sentimen berita Program Makan Bergizi Gratis (MBG) " +
    "menggunakan model IndoBERT.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="id">
      <body>{children}</body>
    </html>
  );
}
