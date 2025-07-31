from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont
import requests

class BatteryLevel:
    def __init__(self,display , ha_url, token, entity_id="sensor.deye_battery"):
        self.ha_url = ha_url.rstrip("/")
        self.token = token
        self.entity_id = entity_id
        self.oled = display
        self.font_path = "/app/fonts/roboto.ttf"
        self.font = ImageFont.truetype(self.font_path, 12)

    def get_battery_state(self):
        url = f"{self.ha_url}/api/states/{self.entity_id}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        battery_state = int(data['state'])
        friendly_name = data['attributes'].get('friendly_name', 'Brak nazwy')
        unit = data['attributes'].get('unit_of_measurement', '')
        with canvas(self.oled) as draw:
            x, y = 0, 20  # pozycja startowa
            battery_width = 90
            battery_height = 30

            # Obudowa baterii
            draw.rectangle((x, y, x + battery_width, y + battery_height), outline="white", fill="black")

            # Biegun baterii (po prawej)
            pole_width = 4
            pole_height = 10
            draw.rectangle((
                x + battery_width,
                y + (battery_height // 2 - pole_height // 2),
                x + battery_width + pole_width,
                y + (battery_height // 2 + pole_height // 2)
            ), outline="white", fill="black")

            # Liczba "bloków" zależna od szerokości
            block_count = 10
            block_spacing = 2
            block_width = (battery_width - (block_count + 1) * block_spacing) // block_count
            block_height = battery_height - 6

            if battery_state >= 90:
                level = 10
            else:
                level = battery_state // 10

            for i in range(level):
                bx = x + block_spacing + i * (block_width + block_spacing)
                by = y + 3
                draw.rectangle((bx, by, bx + block_width, by + block_height), outline="white", fill="white")

            # Nazwa (prawy górny róg)
            draw.text((32, 0), 'DEYE stan baterii', fill="white")

            # Stan baterii (poniżej)
            draw.text((96, 29), f"{battery_state}{unit}", fill="white")

    async def draw_battery(self, display_lock=None):
        if display_lock:
            async with display_lock:
                self.get_battery_state()
        else:
            self.get_battery_state()