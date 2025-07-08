# Dockerfile
ARG BUILD_FROM=debian:bookworm-slim
FROM --platform=$BUILDPLATFORM ${BUILD_FROM}

# Ustawienie powłoki dla wszystkich kolejnych komend RUN
SHELL ["/bin/sh", "-c"]

# Ustaw katalog roboczy
WORKDIR /app

# Kopiowanie plików rootfs (jeśli istnieją i utworzyłeś ten folder)
COPY rootfs /

# Kopiowanie requirements.txt
COPY requirements.txt .

# Instalacja zależności systemowych
RUN DEBIAN_FRONTEND=noninteractive /usr/bin/apt-get update && \
    DEBIAN_FRONTEND=noninteractive /usr/bin/apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libusb-1.0-0-dev \
    libgpiod-dev \
    python3 python3-pip \
    libjpeg-dev \
    zlib1g-dev \
    libtiff-dev \
    libfreetype6-dev \
    i2c-tools \
    python3-smbus \
    pkg-config \
    libxml2-dev \
    libxslt1-dev \
    automake \
    autoconf \
    libtool \
    ca-certificates \
    curl \
    gnupg \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Zainstaluj wymagane pakiety Pythona, zapisując logi do pliku, a następnie wyświetlając go
RUN pip install -v --no-cache-dir -r requirements.txt 2>&1 | tee pip_install_log.txt || true && \
    cat pip_install_log.txt

# Skopiuj resztę kodu dodatku (oprócz run.sh, który już usunąłeś ze swojego repo)
COPY . .

# --- TYMCZASOWA ZMIANA: Bardzo prosty skrypt run.sh i weryfikacja ---
# Cel: Sprawdzić, czy najprostszy możliwy skrypt sh działa
RUN <<EOF > /app/run.sh
#!/bin/sh
echo "Prosty testowy skrypt dziala!"
exit 0
EOF

# Nadaj uprawnienia do wykonania stworzonemu plikowi
RUN chmod +x /app/run.sh

# --- Weryfikacja formatu i uprawnień run.sh (po raz ostatni) ---
RUN echo "--- Weryfikacja run.sh po stworzeniu i chmod +x ---" && \
    ls -la /app/run.sh && \
    file /app/run.sh && \
    head -n 2 /app/run.sh | cat -v && \
    echo "--- Koniec weryfikacji run.sh ---"
# --- KONIEC TYMCZASOWEJ ZMIANY ---

# Definiuje punkt wejścia do kontenera. Standardowo w HA jest to skrypt run.sh
CMD ["/app/run.sh"]