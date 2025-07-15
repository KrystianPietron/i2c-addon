ARG BUILD_FROM
FROM ${BUILD_FROM}

RUN apk add --no-cache \
    i2c-tools \
    python3-dev \
    py3-pip \
    build-base \
    libffi-dev \
    libusb-dev \
    libgpiod-dev

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

RUN chmod a+x /etc/services.d/i2c/run