# Dockerfile
ARG BUILD_FROM=debian:bookworm-slim
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
RUN DEBIAN_FRONTEND=noninteractive /usr/bin/apt-get update && \
    DEBIAN_FRONTEND=noninteractive /usr/bin/apt-get install -y --no-install-recommends \
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
    dos2unix \
    file \
    && rm -rf /var/lib/apt/lists/*

# Zainstaluj wymagane pakiety Pythona, zapisując logi do pliku, a następnie wyświetlając go
RUN pip install -v --no-cache-dir -r requirements.txt 2>&1 | tee pip_install_log.txt || true && \
    cat pip_install_log.txt

# --- KLUCZOWE ZMIANY DLA run.sh ---

# 1. Agresywne kopiowanie i usuwanie:
# Upewniamy się, że kopiujemy odpowiedni plik i resetujemy jego stan
COPY run.sh /app/run.sh.tmp # Kopiuj do tymczasowego pliku
RUN rm -f /app/run.sh # Usuń wszelkie stare wersje
RUN mv /app/run.sh.tmp /app/run.sh # Zastąp prawidłowym plikiem

# 2. Diagnostyka przed konwersją:
RUN echo "--- Diagnostyka run.sh PRZED konwersją ---" && \
    ls -la /app/run.sh && \
    file /app/run.sh && \
    head -n 2 /app/run.sh | cat -v # Pokaż początek pliku z widocznymi znakami kontrolnymi

# 3. Agresywna konwersja i uprawnienia:
# Użyj sed, żeby usunąć znak powrotu karetki (CR) - to jest najbardziej niezawodne
RUN sed -i 's/\r$//' /app/run.sh && \
    dos2unix /app/run.sh && \
    chmod +x /app/run.sh

# 4. Diagnostyka po konwersji:
RUN echo "--- Diagnostyka run.sh PO konwersji ---" && \
    ls -la /app/run.sh && \
    file /app/run.sh && \
    head -n 2 /app/run.sh | cat -v && \
    echo "--- Koniec diagnostyki run.sh ---"
# --- KONIEC KLUCZOWYCH ZMIAN ---

# Skopiuj resztę kodu dodatku (oprócz run.sh, który już skopiowaliśmy)
COPY . .

# Definiuje punkt wejścia do kontenera. Standardowo w HA jest to skrypt run.sh
CMD ["/app/run.sh"]