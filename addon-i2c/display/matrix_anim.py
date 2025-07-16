import asyncio
from PIL import Image, ImageDraw, ImageFont
import random

class Matrix:
    def __init__(self, display):
        self.display = display

    async def matrix_rain(self, duration=10, display_lock=None):
        width = self.display.width
        height = self.display.height
        font_path = "/app/fonts/roboto.ttf"
        font = ImageFont.truetype(font_path, 12)
        bbox = font.getbbox("A")
        char_width = bbox[2] - bbox[0]
        char_height = bbox[3] - bbox[1]
        columns = width // char_width
        rows = height // char_height

        charset = list("01abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

        drops = [random.randint(-rows, 0) for _ in range(columns)]

        background = Image.new("1", (width, height))
        bg_draw = ImageDraw.Draw(background)
        for x in range(columns):
            for y in range(rows):
                ch = random.choice(charset)
                bg_draw.text((x * char_width, y * char_height), ch, font=font, fill=64)

        start_time = asyncio.get_event_loop().time()

        while asyncio.get_event_loop().time() - start_time < duration:
            frame = background.copy()
            draw = ImageDraw.Draw(frame)

            for i in range(columns):
                y = drops[i]
                if 0 <= y < rows:
                    draw.rectangle((i * char_width, y * char_height,
                                    (i + 1) * char_width, (y + 1) * char_height),
                                   fill=255)
                    ch = random.choice(charset)
                    draw.text((i * char_width, y * char_height), ch, font=font, fill=0)
                drops[i] += 1
                if drops[i] > rows + random.randint(1, 6):
                    drops[i] = random.randint(-rows, 0)

            if display_lock:
                async with display_lock:
                    self.display.display(frame)
            else:
                self.display.display(frame)

            await asyncio.sleep(0.05)