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
    dos2unix \
    # Dodatkowe narzędzia diagnostyczne
    file \
    && rm -rf /var/lib/apt/lists/*

# Zainstaluj wymagane pakiety Pythona, zapisując logi do pliku, a następnie wyświetlając go
RUN pip install -v --no-cache-dir -r requirements.txt 2>&1 | tee pip_install_log.txt || true && \
    cat pip_install_log.txt

# Skopiuj cały kod dodatku do kontenera
COPY . .

# --- KLUCZOWE ZMIANY DLA DIAGNOSTYKI run.sh ---
# 1. Sprawdź format pliku przed konwersją
RUN echo "--- Diagnostyka run.sh przed dos2unix ---" && \
    file /app/run.sh && \
    echo "--- Zawartość run.sh przed dos2unix ---" && \
    cat -v /app/run.sh

# 2. Skonwertuj znaki końca linii i ustaw uprawnienia
RUN dos2unix /app/run.sh && \
    chmod +x /app/run.sh

# 3. Sprawdź format pliku po konwersji
RUN echo "--- Diagnostyka run.sh po dos2unix ---" && \
    file /app/run.sh && \
    echo "--- Zawartość run.sh po dos2unix (po konwersji) ---" && \
    cat -v /app/run.sh && \
    echo "--- Koniec diagnostyki run.sh ---"
# --- KONIEC KLUCZOWYCH ZMIAN DLA DIAGNOSTYKI run.sh ---

# Definiuje punkt wejścia do kontenera. Standardowo w HA jest to skrypt run.sh
CMD ["/app/run.sh"]