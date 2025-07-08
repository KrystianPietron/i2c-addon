ARG BUILD_FROM=debian:bookworm-slim
FROM --platform=$BUILDPLATFORM ${BUILD_FROM}

WORKDIR /app

COPY rootfs /
COPY requirements.txt .

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential gcc python3-dev libffi-dev libusb-1.0-0-dev libgpiod-dev \
    python3 python3-pip \
    libjpeg-dev zlib1g-dev libtiff-dev libfreetype6-dev i2c-tools \
    python3-smbus pkg-config libxml2-dev libxslt1-dev automake autoconf \
    libtool ca-certificates curl gnupg libopenblas-dev liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -v --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "/app/main.py"]
