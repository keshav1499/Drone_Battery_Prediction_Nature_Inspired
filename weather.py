import requests
from config import OPENWEATHER_API_KEY

def get_weather_data(lat, lon, override_temp=None, override_humidity=None):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()

        if override_temp is not None or override_humidity is not None:
            print(f"[Weather] Using LoRa DHT11 sensor override: Temp={override_temp}, Humidity={override_humidity}")
        else:
            print(f"[Weather] Using OpenWeatherMap API values: Temp={weather_data['main']['temp']}, Humidity={weather_data['main']['humidity']}")

        return {
            'temp': override_temp if override_temp is not None else weather_data['main']['temp'],
            'feels_like': weather_data['main']['feels_like'],
            'humidity': override_humidity if override_humidity is not None else weather_data['main']['humidity'],
            'pressure': weather_data['main']['pressure'],
            'wind_speed': weather_data['wind']['speed'],
            'wind_deg': weather_data['wind'].get('deg', 0),
            'wind_gust': weather_data['wind'].get('gust', 0),
            'clouds': weather_data['clouds']['all'],
            'visibility': weather_data.get('visibility', 'N/A'),
            'weather_main': weather_data['weather'][0]['main'],
            'weather_desc': weather_data['weather'][0]['description'],
            'rain_1h': weather_data.get('rain', {}).get('1h', 0),
            'snow_1h': weather_data.get('snow', {}).get('1h', 0)
        }
    except Exception as e:
        print(f"[Weather API Error] {e}")
        return None

