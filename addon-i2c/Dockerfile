# Dockerfile
ARG BUILD_FROM

# Standardowa deklaracja FROM z użyciem BUILD_FROM
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
# KLUCZOWA ZMIANA: Dodano więcej pakietów deweloperskich i bibliotek graficznych/hardware
RUN DEBIAN_FRONTEND=noninteractive /usr/bin/apt-get update && \
    DEBIAN_FRONTEND=noninteractive /usr/bin/apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libusb-1.0-0-dev \
    libgpiod-dev \
    python3 python3-pip \
    # Dodatkowe biblioteki dla Pillow i ogólnej obsługi obrazów
    libjpeg-dev \
    zlib1g-dev \
    libtiff-dev \
    libfreetype6-dev \
    # Dodatkowe biblioteki często potrzebne dla luma.oled i interakcji z hardware
    i2c-tools \
    python3-smbus \
    # Często potrzebne do kompilacji pakietów Pythona z rozszerzeniami C
    pkg-config \
    libxml2-dev \
    libxslt1-dev \
    # Dalsze pakiety deweloperskie dla różnych scenariuszy kompilacji
    automake \
    autoconf \
    libtool \
    # Usuwamy listy pakietów APT, aby zmniejszyć rozmiar obrazu
    && rm -rf /var/lib/apt/lists/*

# Zainstaluj wymagane pakiety Pythona
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj cały kod dodatku do kontenera
COPY . .

# Upewnij się, że skrypt run.sh jest wykonywalny
RUN chmod +x /app/run.sh

# Definiuje punkt wejścia do kontenera. Standardowo w HA jest to skrypt run.sh
CMD ["/app/run.sh"]