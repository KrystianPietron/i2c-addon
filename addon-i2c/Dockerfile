# Dockerfile
ARG BUILD_FROM
ARG TARGETARCH

FROM --platform=$BUILDPLATFORM ${BUILD_FROM}

# WAŻNA ZMIANA: Zmieniamy powłokę na 'sh' i dodajemy DEBIAN_FRONTEND
SHELL ["/bin/sh", "-o", "pipefail", "-c"]

# Ustaw katalog roboczy
WORKDIR /app

# Kopiowanie plików rootfs (jeśli istnieją)
COPY rootfs /

COPY requirements.txt .
# Instalacja zależności
# WAŻNA ZMIANA: Używamy pełnej ścieżki do apt-get!
RUN DEBIAN_FRONTEND=noninteractive /usr/bin/apt-get update && \
    DEBIAN_FRONTEND=noninteractive /usr/bin/apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libusb-1.0-0-dev \
    libgpiod-dev \
    && rm -rf /var/lib/apt/lists/*

# Zainstaluj wymagane pakiety Pythona
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj cały kod dodatku do kontenera
# Skopiuje wszystkie pliki z katalogu addon-i2c do /app w kontenerze
COPY . .

# Upewnij się, że skrypt run.sh jest wykonywalny
RUN chmod +x /app/run.sh

# Definiuje punkt wejścia do kontenera. Standardowo w HA jest to skrypt run.sh
CMD ["/app/run.sh"]