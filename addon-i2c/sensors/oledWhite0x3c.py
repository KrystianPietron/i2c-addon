from display.images import Images
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from sensors.tge import TGEPriceDisplay
from display.showLogo import ShowLogo
import asyncio
import logging
import json
import os


class OledWhite0x3c:
    def __init__(self, port=13, address=0x3c):
        # Inicjalizacja luma.oled z podaniem numeru bussa i adresu
        serial = i2c(port=port, address=address)
        self.device = ssd1306(serial, width=128, height=64)
        self.address = address
        self.IMG_PATH_RASPBERRY = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'raspberry_logo.bmp'))
        self.IMG_PATH_DEBIAN = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'debian_logo.bmp'))
        self.display_lock = asyncio.Lock()


    async def run(self):

        show = ShowLogo()
        await asyncio.gather(show.showLogo(self.device))

        with open('/data/options.json') as f:
            config = json.load(f)

        home_assistant_url = "http://192.168.1.226:8123"
        home_assistant_token = config.get("token")

        tge = TGEPriceDisplay(self.device, home_assistant_url, home_assistant_token)

        try:
            logging.info(f"📂 Katalog roboczy: {os.getcwd()}")

            while True:
                logging.info("🖼️ Wyświetlanie TGE")
                async with self.display_lock:
                    await tge.draw_once()
                await asyncio.sleep(60)

        except Exception as e:
            logging.error(f"Błąd w run_display1 White: {e}", exc_info=True)