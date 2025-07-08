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
    # Usunięcie dos2unix i file - już ich nie potrzebujemy, skoro tworzymy skrypt od nowa
    # dos2unix \
    # file \
    && rm -rf /var/lib/apt/lists/*

# Zainstaluj wymagane pakiety Pythona, zapisując logi do pliku, a następnie wyświetlając go
RUN pip install -v --no-cache-dir -r requirements.txt 2>&1 | tee pip_install_log.txt || true && \
    cat pip_install_log.txt

# Skopiuj resztę kodu dodatku (oprócz run.sh)
# Upewnij się, że Twój lokalny plik run.sh JEST USUNIĘTY z folderu addon-i2c
# po tej zmianie w Dockerfile, bo inaczej skopiujesz go ponownie!
COPY . .

# --- KLUCZOWA ZMIANA: Tworzenie run.sh bezpośrednio w Dockerfile ---
# Używamy instrukcji RUN z heredoc (<<<EOF ... EOF) do utworzenia pliku run.sh.
# To gwarantuje, że plik będzie miał idealne zakończenia linii LF.
# Zmieniamy też shebang na /bin/sh, który jest zawsze dostępny.
RUN <<EOF > /app/run.sh
#!/bin/sh
set -e

echo "Starting my Python add-on..."

# Uruchom Twój skrypt Pythona
python3 main.py

echo "Python add-on finished."
# Kontener zostanie zatrzymany po zakończeniu skryptu.
# Jeśli chcesz, żeby kontener działał w tle, użyj np. tail -f /dev/null
EOF

# Nadaj uprawnienia do wykonania stworzonemu plikowi
RUN chmod +x /app/run.sh

# Definiuje punkt wejścia do kontenera. Standardowo w HA jest to skrypt run.sh
CMD ["/app/run.sh"]