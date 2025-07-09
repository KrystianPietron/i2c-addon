#!/usr/bin/with-contenv bashio
set -e

echo "Starting my Python add-on..."

python3 /addon-i2c/main.py

echo "Python add-on finished."