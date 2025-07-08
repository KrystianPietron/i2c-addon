# Argument BUILD_FROM jest dostarczany przez Home Assistant Supervisor
ARG BUILD_FROM
# Bazowy obraz dostarczony przez Home Assistant
FROM ${BUILD_FROM}

# Ustaw katalog roboczy (zwykle /app lub /)
ARG BUILD_FROM
ARG TARGETARCH

# Ustawienie domyślnego obrazu bazowego
FROM --platform=$BUILDPLATFORM ${BUILD_FROM}

# WAŻNA ZMIANA: Ustawienie powłoki dla wszystkich kolejnych komend RUN
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Ustaw katalog roboczy
WORKDIR /app

# Kopiowanie plików rootfs (jeśli istnieją)
COPY rootfs /

# Instalacja zależności
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libusb-1.0-0-dev \
    libgpiod-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Zainstaluj wymagane pakiety Pythona
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj cały kod dodatku do kontenera
# Skopiuje wszystkie pliki z katalogu addon-i2c do /app w kontenerze
COPY . .

# Upewnij się, że skrypt run.sh jest wykonywalny
RUN chmod +x /app/run.sh

# Definiuje punkt wejścia do kontenera. Standardowo w HA jest to skrypt run.sh
CMD ["/app/run.sh"]