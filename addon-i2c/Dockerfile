ARG BUILD_FROM
FROM ${BUILD_FROM}

RUN apt-get update && apt-get install -y --no-install-recommends \
    i2c-tools \
    python3-dev \
    python3-pip \
    build-essential \
    libffi-dev \
    libusb-1.0-0-dev \
    libgpiod-dev \
 && rm -rf /var/lib/apt/lists/* \

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
COPY rootfs/ /
RUN chmod a+x /etc/services.d/i2c/run
