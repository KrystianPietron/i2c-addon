# Dockerfile
# Zmieniamy obraz bazowy na Alpine Linux
ARG BUILD_FROM=alpine:latest
FROM --platform=$BUILDPLATFORM ${BUILD_FROM}

# Ustawienie powłoki dla wszystkich kolejnych komend RUN
SHELL ["/bin/sh", "-c"]

# Ustaw katalog roboczy
WORKDIR /app

# Kopiowanie plików rootfs (jeśli istnieją i utworzyłeś ten folder)
COPY rootfs /

# Kopiowanie requirements.txt
COPY requirements.txt .

# --- KLUCZOWA ZMIANA: ROZDZIELENIE apk update i apk add ---
# Krok 1: Wykonaj tylko aktualizację indeksu pakietów
RUN apk update

# Krok 2: Zainstaluj pakiety
RUN apk add --no-cache \
    build-base \
    python3 \
    py3-pip \
    libffi-dev \
    libusb-dev \
    libgpiod-dev \
    jpeg-dev \
    zlib-dev \
    tiff-dev \
    freetype-dev \
    i2c-tools \
    python3-dev \
    bash \
    && rm -rf /var/cache/apk/*
# --- KONIEC KLUCZOWEJ ZMIANY ---

# Zainstaluj wymagane pakiety Pythona, zapisując logi do pliku, a następnie wyświetlając go
RUN pip install -v --no-cache-dir -r requirements.txt 2>&1 | tee pip_install_log.txt || true && \
    cat pip_install_log.txt

# Skopiuj resztę kodu dodatku
COPY . .

# Tworzenie run.sh bezpośrednio w Dockerfile
RUN <<EOF > /app/run.sh
#!/bin/sh
set -e

echo "Starting my Python add-on..."

# Uruchom Twój skrypt Pythona
python3 main.py

echo "Python add-on finished."
EOF

# Nadaj uprawnienia do wykonania stworzonemu plikowi
RUN chmod +x /app/run.sh

# Definiuje punkt wejścia do kontenera. Standardowo w HA jest to skrypt run.sh
CMD ["/app/run.sh"]