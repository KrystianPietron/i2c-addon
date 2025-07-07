# Bazowy obraz z Pythonem 3.12 (lekkie slim)
FROM python:3.12-slim

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libusb-1.0-0-dev \
    && rm -rf /var/lib/apt/lists/*
# Skopiuj plik z zależnościami (jeśli masz)
COPY requirements.txt .

# Zainstaluj wymagane pakiety Pythona
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj cały kod dodatku do kontenera
COPY . .

# Domyślne polecenie uruchamiające (zmień na swój skrypt lub komendę)
CMD ["python", "main.py"]