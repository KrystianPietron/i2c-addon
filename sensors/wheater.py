import requests
import logging

class MyWeather:

    @staticmethod
    def get_weather():
        key = "2d6d7a30a101b28083dc20a148a6d47d"
        city = "Lublin"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric&lang=pl"
        try:
            response = requests.get(url)
            data = response.json()

            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"]

            return [
                f"Pogoda: {city}",
                f"Temp: {temperature:.1f} °C",
                f"Wilg: {humidity}%",
                f"{description.capitalize()}"
            ]
        except Exception as e:
            logging.error('Błąd pobierania danych pogodowych')
            return ["Brak danych pogodowych"]