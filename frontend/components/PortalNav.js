"use client";

import Link from "next/link";

// Top-nav portal publik: logo MBGwatch + menu.
export default function PortalNav() {
  const menu = ["Pengaduan", "Edukasi", "Tentang Kami", "FAQ"];
  return (
    <nav className="portal-nav">
      <div className="container portal-nav__inner">
        <Link href="/" className="portal-logo">
          <span className="portal-logo__icon" aria-hidden>
            {/* ikon garpu-sendok sederhana */}
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <path d="M6 3v7a2 2 0 0 0 4 0V3M8 10v11" />
              <path d="M16 3c-1.5 0-2.5 2-2.5 5S15 13 16 13s2.5-2 2.5-5S17.5 3 16 3zM16 13v8" />
            </svg>
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
