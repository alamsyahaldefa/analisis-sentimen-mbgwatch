"""Skema Pydantic untuk request & response API."""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Artikel(BaseModel):
    id: str
    portal: Optional[str] = None
    tanggal_terbit: Optional[str] = None
    url: Optional[str] = None
    judul: Optional[str] = None
    teks: Optional[str] = None
    sentimen: Optional[str] = None
    confidence: Optional[float] = None
    kategori: Optional[str] = None


class ArtikelResponse(BaseModel):
    data: List[Artikel]
    total: int
    page: int
    limit: int


class TrenBulan(BaseModel):
    bulan: str
    negatif: int = 0
    netral: int = 0
    positif: int = 0


class StatistikResponse(BaseModel):
    total: int
    per_kelas: Dict[str, int]
    tren_bulanan: List[TrenBulan]
    portals: List[str]
    per_kategori: Dict[str, int] = {}


class PrediksiRequest(BaseModel):
    teks: str = Field(..., min_length=1, description="Teks berita yang akan dianalisis")


class PrediksiResponse(BaseModel):
    sentimen: str
    confidence: float
    probabilitas: Dict[str, float]


class PrediksiUrlRequest(BaseModel):
    url: str = Field(..., min_length=8, description="URL artikel berita MBG")


class PrediksiUrlResponse(BaseModel):
    sentimen: str
    confidence: float
    probabilitas: Dict[str, float]
    # Metadata artikel hasil ekstraksi
    judul: str
    portal: str
    tanggal_terbit: Optional[str] = None
    url: str
    teks_dianalisis: str = Field(..., description="Unit analisis (judul + lead) yang diberikan ke model")
