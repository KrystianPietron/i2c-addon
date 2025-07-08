# Dockerfile

# Domyślna wartość, jeśli nie podasz BUILD_FROM w build args
ARG BUILD_FROM=debian:bookworm-slim

# Użyj platformy z BuildKit
FROM --platform=$BUILDPLATFORM ${BUILD_FROM}

# Ustaw powłokę sh
SHELL ["/bin/sh", "-c"]

# Ustaw katalog roboczy
WORKDIR /app

# Kopiuj pliki (np. skrypty, rootfs)
COPY rootfs /  # jeśli nie masz — możesz usunąć
COPY requirements.txt .

# Instaluj zależności systemowe
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
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

# Instaluj pip dependencies
RUN pip install -v --no-cache-dir -r requirements.txt

# Skopiuj całość kodu
COPY . .

# Upewnij się, że run.sh jest wykonywalny
RUN chmod +x /app/run.sh

# Domyślny entrypoint
CMD ["/app/run.sh"]
