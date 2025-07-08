#!/usr/bin/with-contenv bashio
set -e

echo "Starting my Python add-on..."

# Uruchom Twój skrypt Pythona
python3 addon-i2c/main.py

echo "Python add-on finished."
# Kontener zostanie zatrzymany po zakończeniu skryptu.
# Jeśli chcesz, żeby kontener działał w tle, Twój skrypt Pythona musi być procesem działającym non-stop.