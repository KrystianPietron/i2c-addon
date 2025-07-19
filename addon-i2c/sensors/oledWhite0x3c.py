from display.images import Images
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from sensors.tge import TGEPriceDisplay
import asyncio
import json
import logging
import os


class OledWhite0x3c:
    def __init__(self, port=13, address=0x3c):
        # Inicjalizacja luma.oled z podaniem numeru bussa i adresu
        serial = i2c(port=port, address=address)
        self.device = ssd1306(serial, width=128, height=64)
        self.address = address
        self.IMG_PATH_RASPBERRY = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'raspberry_logo.bmp'))
        self.IMG_PATH_DEBIAN = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'debian_logo.bmp'))
        self.LOGO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'home_assistant.bmp'))
        self.display_lock = asyncio.Lock()


    async def run(self):
        with open('/data/options.json') as f:
            config = json.load(f)
        home_assistant_url = "http://192.168.1.226:8123"
        home_assistant_token = config.get("token")

        # Czyszczenie ekranu na start
        self.device.clear()
        self.device.show()
        if config.get('startLogo'):
            try:
                images = Images(self.device)
                logging.info(f"🖼️ Witamy w i2c wyświetlacz YB: {self.address}")
                for _ in range(1):
                    async with self.display_lock:
                        images.display_image(self.LOGO_PATH)
                    await asyncio.sleep(10)

            except Exception as e:
                logging.error(f"Błąd w OledBlueYellow0x3c Start Logo BY: {e}", exc_info=True)

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
