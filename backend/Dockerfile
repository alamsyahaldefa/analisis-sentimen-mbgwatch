# Backend MBG Watch — Hugging Face Spaces (Docker SDK)
FROM python:3.11-slim

# Lokasi cache & DB yang selalu writable di HF Spaces
ENV HF_HOME=/tmp/hf \
    MBG_DB=/tmp/mbg.db \
    MBG_DB_UPLOAD=/tmp/mbg_upload.db \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Pasang PyTorch versi CPU dulu (jauh lebih ringan daripada default CUDA)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Dependensi lain
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kode + model + CSV (pastikan model_mbg_indobert/ sudah ada, lihat README)
COPY . .

# HF Spaces mengharapkan aplikasi mendengarkan di port 7860
EXPOSE 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
