import "./globals.css";

export const metadata = {
  title: "MBG Watch — Analisis Sentimen Berita MBG",
  description:
    "Dashboard analisis sentimen berita Program Makan Bergizi Gratis (MBG) " +
    "menggunakan model IndoBERT.",
  // Favicon memakai file yang sama dengan logo: frontend/public/logo.png
  icons: { icon: "/logo.png" },
};

export default function RootLayout({ children }) {
  return (
    <html lang="id">
      <body>{children}</body>
    </html>
  );
}
