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
        battery_state = data['state']
        friendly_name = data['attributes'].get('friendly_name', 'Brak nazwy')
        unit = data['attributes'].get('unit_of_measurement', '')
        with canvas(self.oled) as draw:
            # Ikona baterii (lewa strona)
            x, y = 0, 20
            draw.rectangle((x, y, x + 20, y + 30), outline="white", fill="black")  # Obudowa
            draw.rectangle((x + 20, y + 10, x + 22, y + 20), outline="white", fill="black")  # Biegun

            # Wypełnienie poziomem na podstawie % (będzie max 4 bloki)
            level = battery_state // 25  # 0–4
            for i in range(level):
                draw.rectangle((x + 3 + i * 4, y + 3, x + 6 + i * 4, y + 27), outline="white", fill="white")

            # Nazwa (prawy górny róg)
            draw.text((32, 0), friendly_name, fill="white")

            # Stan baterii (poniżej)
            draw.text((32, 20), f"{battery_state}{unit}", fill="white")

    async def draw_battery(self, display_lock=None):
        if display_lock:
            async with display_lock:
                self.get_battery_state()
        else:
            self.get_battery_state()