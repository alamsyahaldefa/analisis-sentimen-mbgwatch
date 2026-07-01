"use client";

import Link from "next/link";
import { useState } from "react";

// Top-nav portal publik: logo MBGwatch + menu.
export default function PortalNav() {
  const menu = ["Pengaduan", "Edukasi", "Tentang Kami", "FAQ"];
  // Logo utama dari file: frontend/public/logo.png.
  // Bila file belum ada (onError), otomatis fallback ke rekonstruksi SVG
  // agar tidak muncul ikon gambar rusak.
  const [logoError, setLogoError] = useState(false);

  return (
    <nav className="portal-nav">
      <div className="container portal-nav__inner">
        <Link href="/" className="portal-logo">
          <span className="portal-logo__icon" aria-hidden>
            {logoError ? (
              /* Fallback: rekonstruksi SVG (piring/jam biru + sendok-garpu merah) */
              <svg width="26" height="26" viewBox="0 0 48 48" role="img">
                <circle cx="24" cy="24" r="18" fill="none"
                        stroke="#004788" strokeWidth="4" />
                <g transform="rotate(20 24 24)">
                  <line x1="24" y1="41" x2="24" y2="19"
                        stroke="#e23b2e" strokeWidth="3.2" strokeLinecap="round" />
                  <ellipse cx="24" cy="14" rx="4.2" ry="5.6" fill="#e23b2e" />
                </g>
                <g transform="rotate(-20 24 24)" stroke="#e23b2e"
                   strokeLinecap="round" fill="none">
                  <line x1="24" y1="41" x2="24" y2="16" strokeWidth="3.2" />
                  <line x1="20.5" y1="7" x2="20.5" y2="15" strokeWidth="2.2" />
                  <line x1="24" y1="7" x2="24" y2="15" strokeWidth="2.2" />
                  <line x1="27.5" y1="7" x2="27.5" y2="15" strokeWidth="2.2" />
                  <line x1="20.5" y1="15" x2="27.5" y2="15" strokeWidth="2.2" />
                </g>
              </svg>
            ) : (
              /* eslint-disable-next-line @next/next/no-img-element */
              <img
                src="/logo.png"
                alt="Logo MBG Watch"
                width={30}
                height={30}
                style={{ objectFit: "contain" }}
                onError={() => setLogoError(true)}
              />
            )}
          </span>
          <span className="portal-logo__text">
            MBG<span className="portal-logo__accent">watch</span>
          </span>
        </Link>

        <div className="portal-nav__menu">
          {menu.map((m) => (
            <a key={m} href="#" className="portal-nav__link">
              {m}
            </a>
          ))}
          <Link href="/dashboard" className="portal-nav__cta">
            Dashboard
          </Link>
        </div>
      </div>
    </nav>
  );
}
