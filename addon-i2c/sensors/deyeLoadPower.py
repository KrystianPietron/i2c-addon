from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont
import requests

class LoadPower:
    def __init__(self,display , ha_url, token, entity_id="sensor.deye_load_power"):
        self.ha_url = ha_url.rstrip("/")
        self.token = token
        self.entity_id = entity_id
        self.oled = display
        self.font_path = "/app/fonts/roboto.ttf"
        self.font = ImageFont.truetype(self.font_path, 12)

    def draw_home_with_bolt(self, power_value: int = None, unit: str = "W"):
        """
        Rysuje ikonę DOM z błyskawicą (zużycie energii) na OLED.
        :param power_value: chwilowe zużycie energii
        :param unit: jednostka (np. W, kW)
        """
        with canvas(self.oled) as draw:
            x, y = 0, 0  # pozycja startowa ikony

            # Dach (trójkąt)
            draw.polygon([
                (x + 20, y),  # szczyt
                (x, y + 20),  # lewy dół
                (x + 40, y + 20)  # prawy dół
            ], outline="white", fill="black")

            # Ściany domu (prostokąt)
            draw.rectangle((x + 5, y + 20, x + 35, y + 40), outline="white", fill="black")

            # Błyskawica (stylizowana Z)
            bolt_x, bolt_y = x + 15, y + 20
            draw.line([
                (bolt_x + 5, bolt_y + 2),
                (bolt_x, bolt_y + 15),
                (bolt_x + 10, bolt_y + 15),
                (bolt_x + 5, bolt_y + 28)
            ], fill="white", width=2)

            # Opcjonalny podpis pod ikoną (zużycie)
            if power_value is not None:
                draw.text((50, 10), f"{power_value}{unit}", fill="white")
            else:
                draw.text((50, 10), "Zużycie", fill="white")

    async def draw_loadPower(self, display_lock=None):
        if display_lock:
            async with display_lock:
                self.draw_home_with_bolt()
        else:
            self.draw_home_with_bolt()