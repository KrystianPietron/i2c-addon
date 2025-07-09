#!/usr/bin/with-contenv bashio
set -e

echo "Starting my Python add-on..."

# Aktywuj virtualenv (jeśli korzystasz)
source /app/venv/bin/activate

# Odpal główny skrypt Pythona
python3 /main.py

echo "Python add-on finished."