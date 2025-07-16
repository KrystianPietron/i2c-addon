ARG BUILD_FROM
FROM python:3.12-slim-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends \
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
 && rm -rf /var/lib/apt/lists/* \

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

RUN chmod a+x /app/run.sh

CMD ["/app/run.sh"]
