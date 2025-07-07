FROM ubuntu:latest
LABEL authors="krystianpietron"

# Użyj oficjalnego obrazu bazowego Home Assistant OS dla Pythona
# Wybierz wersję Pythona, która Ci odpowiada. Poniżej przykład z 3.12
FROM ghcr.io/home-assistant/amd64-base-python:3.12

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj plik requirements.txt (jeśli istnieje) i zainstaluj zależności
COPY requirements.txt .
RUN pip install -r requirements.txt || true

# Skopiuj wszystkie pliki z katalogu dodatku do katalogu roboczego w kontenerze
COPY . .

# Ustaw uprawnienia dla skryptu startowego
RUN chmod +x run.sh

# Użyj skryptu run.sh jako punktu wejścia (entrypoint) kontenera
ENTRYPOINT ["/bin/bash", "run.sh"]