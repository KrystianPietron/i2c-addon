#!/usr/bin/env bash
echo "Starting I2C add-on..."
echo "Loading configuration..."
#CONFIG_PATH=/data/options.json

#TOKEN=$(jq -r '.token' "$CONFIG_PATH")
#DISPLAY1_ON=$(jq -r '.display1' "$CONFIG_PATH")
#DISPLAY2_ON=$(jq -r '.display2' "$CONFIG_PATH")
echo "Config loaded..."

python3 /app/main.py
echo "I2C add-on finished."