# ── Stage 1: build ────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# System deps (libgmp-dev needed by pycryptodome)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgmp-dev gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# Runtime system lib only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgmp10 && \
    rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy app source
COPY . .

# Default port (Render/Railway override via $PORT)
ENV PORT=5000

EXPOSE $PORT

# Single entry-point: starts bot thread + Flask
CMD ["python", "main.py"]
