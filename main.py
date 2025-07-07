import asyncio

import logging

from sensors.oledBlueYellow0x3C import OledBlueYellow0x3c
from sensors.oledBueYellow0x3D import OledBlueYellow0x3d
from sensors.oledWhite0x3c import OledWhite0x3c

logging.basicConfig(
    filename="/home/pi/oled/log.txt",
    filemode="a",
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.DEBUG
)

async def main():
    oled_blue_yellow_0x3d = OledBlueYellow0x3d()
    oled_blue_yellow_0x3c = OledBlueYellow0x3c()
    oled_white_0x3c = OledWhite0x3c()
    await asyncio.gather(
        oled_blue_yellow_0x3c.run(),
        oled_blue_yellow_0x3d.run(),
        oled_white_0x3c.run()
    )

asyncio.run(main())