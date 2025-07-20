from display.display_text import DisplayText
from display.images import Images
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from sensors.cpu_temp import Cpu
from sensors.folders import Folders
from sensors.networks import Networks
from sensors.ram import RamUsage
from sensors.timer import Timer
from display.showLogo import ShowLogo
import asyncio
import os


class OledBlueYellow0x3d:
    def __init__(self):
        self.base_lines = []  # dane systemowe
        self.display_text = None
        self.LOGO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'home_assistant.bmp'))
        self.display_lock = asyncio.Lock()


    async def update_clock(self):
        while True:
            current_time = Timer.get_time()
            lines = [f"{current_time}"] + self.base_lines
            self.display_text.show_text(lines[:6])
            await asyncio.sleep(0,5)

    async def update_data(self):

        while True:
            try:
                self.base_lines = Networks.network_usage() + Folders.get_disk_usage()
                await asyncio.sleep(4)

                self.base_lines = Networks.network_usage() + RamUsage.get_ram_usage()
                await asyncio.sleep(4)

                self.base_lines = Networks.network_usage() + Cpu.get_cpu_usage()
                await asyncio.sleep(4)

                # self.base_lines = Networks.network_usage() + Folders.get_disk_folder_usage('krystek')
                # await asyncio.sleep(4)
                #
                # self.base_lines = Networks.network_usage() + Folders.get_disk_folder_usage('ilona')
                # await asyncio.sleep(4)
                #
                # self.base_lines = Networks.network_usage() + Folders.get_disk_folder_usage('backup')
                # await asyncio.sleep(4)
                #
                # self.base_lines = Networks.network_usage() + Folders.get_disk_folder_usage('shared')
                # await asyncio.sleep(4)

            except Exception as e:
                print(f"Błąd w update_data: {e}")
                await asyncio.sleep(4)

    async def run(self):
        # ✅ Użyj luma.oled I2C
        serial = i2c(port=1, address=0x3D)  # port=13 jeśli chcesz inny bus
        device = ssd1306(serial, width=128, height=64)

        # Opcjonalnie: czyść ekran
        device.clear()
        device.show()  # show() to alias w luma.oled

        show = ShowLogo(device)
        await asyncio.gather(
            show.showLogo()
        )

        # ✅ Przekazujemy urządzenie Luma
        self.display_text = DisplayText(device)

        await asyncio.gather(
            self.update_clock(),
            self.update_data()
        )
