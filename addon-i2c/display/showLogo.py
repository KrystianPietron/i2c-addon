import json
from display.images import Images
import logging
import asyncio
import os


class ShowLogo():
    def __init__(self, device):
        self.device = device
        self.display_lock = asyncio.Lock()
        self.LOGO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'home_assistant.bmp'))

    async def showLogo(self):
        with open('/data/options.json') as f:
            config = json.load(f)


        # Czyszczenie ekranu na start
        self.device.clear()
        self.device.show()

        if config.get('startLogo'):
            try:
                images = Images(self.device)
                logging.info(f"🖼️ Logo {self.device}")
                for _ in range(1):
                    async with self.display_lock:
                        images.display_image(self.LOGO_PATH)
                    await asyncio.sleep(20)

            except Exception as e:
                logging.error(f"Błąd w OledBlueYellow0x3c Start Logo BY: {e}", exc_info=True)