from display.images import Images
from display.matrix_anim import Matrix
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
import asyncio
import json
import logging
import os


class OledBlueYellow0x3c:
    def __init__(self, port=1, address=0x3c):
        # Inicjalizacja luma.oled z podaniem numeru bussa i adresu
        serial = i2c(port=port, address=address)
        self.address = address

        self.device = ssd1306(serial, width=128, height=64)

        self.IMG_PATH_RASPBERRY = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'raspberry_logo.bmp'))
        self.IMG_PATH_DEBIAN = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'debian_logo.bmp'))
        self.LOGO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'home_assistant.bmp'))


        self.display_lock = asyncio.Lock()


    async def run(self):
        with open('/data/options.json') as f:
            config = json.load(f)

        # Czyszczenie ekranu na start
        async with self.display_lock:
            self.device.clear()
            self.device.show()

        matrix = Matrix(self.device)
        images = Images(self.device)
        if config.get('startLogo'):
            try:
                logging.info(f"🖼️ Witamy w i2c wyświetlacz YB: {self.address}")
                for _ in range(1):
                    async with self.display_lock:
                        images.display_image(self.LOGO_PATH)
                    await asyncio.sleep(20)

            except Exception as e:
                logging.error(f"Błąd w OledBlueYellow0x3c Start Logo BY: {e}", exc_info=True)

        try:
            logging.info(f"📂 Katalog roboczy: {os.getcwd()}")

            while True:
                logging.info("🖼️ Wyświetlanie Matrix")
                await matrix.matrix_rain(duration=10, display_lock=self.display_lock)

                logging.info("🖼️ Wyświetlanie Raspberry logo")
                async with self.display_lock:
                    # images.display_image powinno robić device.display(image)
                    images.display_image(self.IMG_PATH_RASPBERRY)
                await asyncio.sleep(10)

                logging.info("🖼️ Wyświetlanie Debian logo")
                async with self.display_lock:
                    images.display_image(self.IMG_PATH_DEBIAN)
                await asyncio.sleep(10)

        except Exception as e:
            logging.error(f"Błąd w run_display2 BY: {e}", exc_info=True)
