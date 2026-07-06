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
    sumber: Optional[str] = None  # 'dataset' (fase 1) | 'upload' (unggahan admin)


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


# ---------------------------------------------------------------------------
# Upload beberapa artikel (demo pengganti scraping) — masuk DB upload terpisah
# ---------------------------------------------------------------------------

class ArtikelUploadItem(BaseModel):
    judul: str = Field(..., min_length=1)
    teks: str = Field(..., min_length=1, description="Isi/lead artikel")
    portal: Optional[str] = None
    tanggal_terbit: Optional[str] = Field(None, description="YYYY-MM-DD")
    url: Optional[str] = None


class UploadArtikelRequest(BaseModel):
    artikel: List[ArtikelUploadItem] = Field(..., min_length=1)


class UploadGagal(BaseModel):
    judul: str
    error: str


class UploadArtikelResponse(BaseModel):
    berhasil: List[Artikel]
    gagal: List[UploadGagal] = []


class UpdateSentimenRequest(BaseModel):
    sentimen: str = Field(..., description="negatif | netral | positif")


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
