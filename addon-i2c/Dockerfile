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

# Instalacja zależności systemowych (składnia Debiana)
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
RUN pip install -v --no-cache-dir -r requirements.txt

# Skopiuj cały kod dodatku (teraz bez run.sh)
COPY . .

RUN <<EOF > /app/run.sh
#!/bin/sh
set -e

echo "Starting my Python add-on..."

# Uruchom Twój skrypt Pythona
python3 main.py

echo "Python add-on finished."
EOF

# Nadaj uprawnienia do wykonania stworzonemu plikowi
RUN chmod a+x /run.sh

# --- KLUCZOWA ZMIANA: Bezpośrednie wywołanie Pythona ---
# Definiuje punkt wejścia do kontenera. Zamiast skryptu shell, uruchamiamy Pythona bezpośrednio.
CMD [ "/run.sh" ]