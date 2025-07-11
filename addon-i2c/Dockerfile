# Dockerfile
ARG BUILD_FROM=debian:bookworm-slim
FROM --platform=$BUILDPLATFORM ${BUILD_FROM}

COPY requirements.txt /

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      gcc \
      python3-dev \
      python3-pip \
      python3-venv \
      libffi-dev \
      libusb-1.0-0-dev \
      libgpiod-dev \
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

RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy data for add-on
COPY run.sh /
COPY main.py /
RUN chmod a+x /run.sh

CMD ["/run.sh"]