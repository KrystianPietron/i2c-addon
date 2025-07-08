# Argument BUILD_FROM jest dostarczany przez Home Assistant Supervisor
ARG BUILD_FROM
# Bazowy obraz dostarczony przez Home Assistant
FROM ${BUILD_FROM}

# Ustaw katalog roboczy (zwykle /app lub /)
WORKDIR /app

# Zainstaluj zależności systemowe (jeśli nie są już w bazowym obrazie HA)
# Te pakiety mogą być potrzebne do kompilacji niektórych bibliotek Pythona (np. RPi.GPIO, smbus)
# Pakiet libgpiod-dev może być potrzebny dla GPIO w nowszych systemach
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libusb-1.0-0-dev \
    libgpiod-dev \
    && rm -rf /var/lib/apt/lists/*

# Skopiuj plik z zależnościami Pythona
# PAMIĘTAJ: ścieżki są względne do kontekstu budowania, który powinien być katalogiem addon-i2c
COPY requirements.txt .

# Zainstaluj wymagane pakiety Pythona
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj cały kod dodatku do kontenera
# Skopiuje wszystkie pliki z katalogu addon-i2c do /app w kontenerze
COPY . .

# Upewnij się, że skrypt run.sh jest wykonywalny
RUN chmod +x /app/run.sh

# Definiuje punkt wejścia do kontenera. Standardowo w HA jest to skrypt run.sh
CMD ["/app/run.sh"]