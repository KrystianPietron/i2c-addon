from display.images import Images
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from sensors.tge import TGEPriceDisplay
from sensors.deyeBatteryLevel import BatteryLevel
from display.showLogo import ShowLogo
import asyncio
import logging
import json
import os


class OledWhite0x3c:
    # default port drugiej szyny 13
    def __init__(self, port=1, address=0x3c):
        # Inicjalizacja luma.oled z podaniem numeru bussa i adresu
        serial = i2c(port=port, address=address)
        self.device = ssd1306(serial, width=128, height=64)
        self.address = address
        self.IMG_PATH_RASPBERRY = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'raspberry_logo.bmp'))
        self.IMG_PATH_DEBIAN = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'debian_logo.bmp'))
        self.IMG_PATH_DEYE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'deye.bmp'))
        self.display_lock = asyncio.Lock()


    async def run(self):

        show = ShowLogo(self.device)
        await asyncio.gather(
            show.showLogo()
        )

        with open('/data/options.json') as f:
            config = json.load(f)

        home_assistant_url = "http://192.168.1.226:8123"
        home_assistant_token = config.get("token")

        tge = TGEPriceDisplay(self.device, home_assistant_url, home_assistant_token)
        battery = BatteryLevel(self.device, home_assistant_url, home_assistant_token)
        logging.info("🖼️ Battery level")


        try:
            logging.info(f"📂 Katalog roboczy: {os.getcwd()}")
            images = Images(self.device)

            while True:
                async with self.display_lock:
                    images.display_image(self.IMG_PATH_DEYE)
                await asyncio.sleep(10)
                async with self.display_lock:
                    await battery.draw_battery()
                await asyncio.sleep(10)
                logging.info("🖼️ Wyświetlanie TGE")
                async with self.display_lock:
                    await tge.draw_once()
                await asyncio.sleep(10)

        except Exception as e:
            logging.error(f"Błąd w run_display1 White: {e}", exc_info=True)