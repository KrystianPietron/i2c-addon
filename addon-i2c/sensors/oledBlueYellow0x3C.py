from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
import os
import asyncio
import logging

from display.images import Images
from display.matrix_anim import Matrix


class OledBlueYellow0x3c:
    def __init__(self, port=14, address=0x3c):
        # Inicjalizacja luma.oled z podaniem numeru bussa i adresu
        serial = i2c(port=port, address=address)
        self.device = ssd1306(serial, width=128, height=64)

        self.IMG_PATH_RASPBERRY = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'raspberry_logo.bmp'))
        self.IMG_PATH_DEBIAN = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'debian_logo.bmp'))

        self.display_lock = asyncio.Lock()


    async def run(self):
        # Czyszczenie ekranu na start
        async with self.display_lock:
            self.device.clear()
            self.device.show()

        matrix = Matrix(self.device)
        images = Images(self.device)

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
