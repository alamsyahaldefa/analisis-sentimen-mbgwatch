"""Pemuatan model IndoBERT & inferensi sentimen.

Model dimuat sekali (lazy singleton) dari `model_mbg_indobert/`. Bila folder
model tidak ada atau gagal dimuat, fungsi prediksi memunculkan RuntimeError
dengan pesan jelas — agar endpoint dapat mengembalikan respons error yang rapi
tanpa membuat seluruh server gagal start.
"""

import os
import threading

from config import ID2LABEL, KELAS, MAX_LENGTH, MODEL_DIR

_tokenizer = None
_model = None
_torch = None
_id2label = ID2LABEL
_lock = threading.Lock()
_load_error = None


def load_model():
    """Muat tokenizer + model. Idempotent (aman dipanggil berulang).

    Return True bila berhasil, False bila gagal (pesan tersimpan di _load_error).
    """
    global _tokenizer, _model, _torch, _id2label, _load_error

    if _model is not None:
        return True

    with _lock:
        if _model is not None:
            return True
        try:
            if not os.path.isdir(MODEL_DIR):
                raise FileNotFoundError(
                    f"Folder model tidak ditemukan: {MODEL_DIR}\n"
                    "Letakkan folder 'model_mbg_indobert/' (hasil save_pretrained) "
                    "di root proyek."
                )

            import torch
            from transformers import (AutoModelForSequenceClassification,
                                      AutoTokenizer)

            _torch = torch
            _tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
            _model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
            _model.eval()

            # Gunakan id2label dari config model bila tersedia & valid
            cfg = getattr(_model.config, "id2label", None)
            if cfg:
                try:
                    _id2label = {int(k): str(v).lower() for k, v in cfg.items()}
                except (ValueError, TypeError):
                    _id2label = ID2LABEL

            _load_error = None
            return True
        except Exception as e:  # noqa: BLE001 - simpan pesan untuk endpoint
            _load_error = str(e)
            return False


def model_siap():
    return _model is not None


def pesan_error():
    return _load_error


def predict(teks: str):
    """Klasifikasi sentimen satu teks.

    Return dict: {sentimen, confidence, probabilitas:{negatif,netral,positif}}.
    Memunculkan RuntimeError bila model belum dapat dimuat.
    """
    if not teks or not teks.strip():
        raise ValueError("Teks tidak boleh kosong.")

    if not load_model():
        raise RuntimeError(_load_error or "Model gagal dimuat.")

    inputs = _tokenizer(
        teks,
        truncation=True,
        max_length=MAX_LENGTH,
        padding=True,
        return_tensors="pt",
    )

    with _torch.no_grad():
        logits = _model(**inputs).logits
        probs = _torch.softmax(logits, dim=-1)[0].tolist()

    # Susun probabilitas per nama kelas
    probabilitas = {k: 0.0 for k in KELAS}
    for idx, p in enumerate(probs):
        label = _id2label.get(idx, str(idx))
        probabilitas[label] = round(float(p), 4)

    sentimen = max(probabilitas, key=probabilitas.get)
    return {
        "sentimen": sentimen,
        "confidence": round(float(probabilitas[sentimen]), 4),
        "probabilitas": probabilitas,
    }
