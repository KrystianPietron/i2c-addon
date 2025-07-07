from PIL import Image
import logging


class Images:
    def __init__(self, display):
        self.display = display

    def show_image(self, image):
        self.display.display(image)
        self.display.show()

    def display_image(self, img_address):
        try:
            logging.info(f"🔍 Próba załadowania obrazu: {img_address}")
            image = Image.open(img_address).convert("1")
            image = image.resize((self.display.width, self.display.height))
            self.display.display(image)
            self.display.show()
            logging.info("✅ Obraz wyświetlony")
        except Exception as e:
            logging.error(f"❌ Błąd podczas wczytywania obrazu '{img_address}': {e}", exc_info=True)
