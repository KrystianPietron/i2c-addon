import logging
import requests


class BatteryLevel:
    def __init__(self, ha_url, token, entity_id="sensor.deye_battery"):
        self.ha_url = ha_url.rstrip("/")
        self.token = token
        self.entity_id = entity_id
        # self.oled = display
        self.font_path = "/app/fonts/roboto.ttf"
        # self.font = ImageFont.truetype(self.font_path, 12)

    def get_battery_state(self):
        url = f"{self.ha_url}/api/states/{self.entity_id}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logging.info(f"Battery level: {response.json()}")