from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
import os
import asyncio
import logging
from sensors.tge import TGEPriceDisplay


class OledWhite0x3c:
    def __init__(self, port=15, address=0x3c):
        # Inicjalizacja luma.oled z podaniem numeru bussa i adresu
        serial = i2c(port=port, address=address)
        self.device = ssd1306(serial, width=128, height=64)

        self.IMG_PATH_RASPBERRY = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'raspberry_logo.bmp'))
        self.IMG_PATH_DEBIAN = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'debian_logo.bmp'))

        self.display_lock = asyncio.Lock()


    async def run(self):
        home_assistant_url = "http://192.168.1.226:8123"
        home_assistant_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4OWM5MTQ2YmM1OGI0NDVhYWNlYzU2ODI5MjdjZDIzOSIsImlhdCI6MTc1MTA0ODAxMSwiZXhwIjoyMDY2NDA4MDExfQ.4Kl4IsLzu0ou8sdW45q5ydzRg6Vi6a9wz5VzzhXVK3s"

        # Czyszczenie ekranu na start
        async with self.display_lock:
            self.device.clear()
            self.device.show()
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
