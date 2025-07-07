import logging
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import asyncio

class TGEPriceDisplay:
    def __init__(self, display, ha_url, token, entity_id="sensor.tge_fixing_1_rate"):
        self.ha_url = ha_url.rstrip("/")
        self.token = token
        self.entity_id = entity_id
        self.oled = display
        self.font = ImageFont.load_default()

    def get_ha_state(self):
        url = f"{self.ha_url}/api/states/{self.entity_id}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_prices(self):
        now = datetime.now()
        try:
            state = self.get_ha_state()
            attributes = state.get("attributes", {})
            if now.hour < 23:
                prices = attributes.get("prices_today", [])
                label_day = "Dzis"
            else:
                prices = attributes.get("prices_tomorrow", [])
                label_day = "Jutro"
            return prices, label_day
        except Exception as e:
            logging.error("Błąd podczas pobierania danych:", exc_info=True)
            return [], ""

    def draw_chart(self, draw, prices):
        if len(prices) < 2:
            return

        min_price = min(p["price"] for p in prices)
        max_price = max(p["price"] for p in prices)

        if min_price > 0:
            min_price = 0
        if max_price < 0:
            max_price = 0

        scale = max_price - min_price or 0.01

        chart_height = 48
        bottom_y = 63

        points = []
        for i, p in enumerate(prices):
            x = int(i * 128 / (len(prices) - 1))
            y = bottom_y - int((p["price"] - min_price) / scale * chart_height)
            points.append((x, y))

        draw.line(points, fill=255)

        zero_y = bottom_y - int((0.0 - min_price) / scale * chart_height)
        draw.line([(0, zero_y), (127, zero_y)], fill=128)
        draw.text((0, zero_y - 6), "0", font=self.font, fill=128)

        now_hour = datetime.now().hour
        idx = min(now_hour, len(points) - 1)

        highlight_x, highlight_y = points[idx]
        radius = 2
        draw.ellipse(
            [(highlight_x - radius, highlight_y - radius),
             (highlight_x + radius, highlight_y + radius)],
            fill=255, outline=0
        )

    def draw_display(self, prices, label_day):
        now = datetime.now()
        hour = now.hour
        price_str = "Brak danych"

        if hour < len(prices):
            try:
                price = prices[hour]["price"]
                price_str = f"{price:.4f} zl"
            except Exception:
                pass

        image = Image.new("1", (128, 64))
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), f"{label_day} {hour:02d}:00 - {price_str}", font=self.font, fill=255)
        self.draw_chart(draw, prices)

        # Tu zamiast oled.image + oled.show
        self.oled.display(image)

    async def draw_once(self, display_lock=None):
        prices, label_day = self.get_prices()
        if display_lock:
            async with display_lock:
                self.draw_display(prices, label_day)
        else:
            self.draw_display(prices, label_day)
