from PIL import Image, ImageDraw, ImageFont

class DisplayText:
    def __init__(self, display):
        self.display = display

    def show_text(self, lines):
        # font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
        font_path = "/app/fonts/roboto.ttf"
        font = ImageFont.truetype(font_path, 12)

        # Utwórz nowy obraz monochromatyczny
        image = Image.new("1", (self.display.width, self.display.height))
        draw = ImageDraw.Draw(image)

        # Wyczyść tło
        draw.rectangle((0, 0, self.display.width, self.display.height), outline=0, fill=0)

        line_height = 14
        for i, line in enumerate(lines):
            draw.text((0, i * line_height), line, font=font, fill=255)

        # WYSYŁKA OBRAZU BEZPOŚREDNIO NA LUMA.OLED
        self.display.display(image)
