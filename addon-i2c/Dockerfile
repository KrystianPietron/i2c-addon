# Dockerfile (przykład z Debianem)
ARG BUILD_FROM="debian:stable-slim" # Ustaw domyślny obraz bazowy na Debiana
ARG TARGETARCH

# Zmiana obrazu bazowego
FROM --platform=$BUILDPLATFORM ${BUILD_FROM}

SHELL ["/bin/sh", "-o", "pipefail", "-c"]

WORKDIR /app

COPY rootfs /
COPY requirements.txt .

# Instalacja zależności systemowych
# To powinno zadziałać na debian:stable-slim
RUN DEBIAN_FRONTEND=noninteractive /usr/bin/apt-get update && \
    DEBIAN_FRONTEND=noninteractive /usr/bin/apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libusb-1.0-0-dev \
    libgpiod-dev \
    # Dodaj pythona i pip, jeśli nie są domyślnie w stable-slim
    python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Zainstaluj wymagane pakiety Pythona
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]