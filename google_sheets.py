import requests
from config import GOOGLE_SHEET_URL

def send_to_google(data):
    try:
        payload = {
            'lat': data['lat'], 'lon': data['lon'], 'alt': data['alt'],
            'roll': data['roll'], 'pitch': data['pitch'], 'yaw': data['yaw'],
            'airspeed': data['airspeed'], 'groundspeed': data['groundspeed'], 'heading': data['heading'],
            'voltage': data['voltage'], 'current': data['current'], 'battery': data['battery'],
            'error_rp': data['error_rp'], 'error_yaw': data['error_yaw'],
            'xacc': data['xacc'], 'yacc': data['yacc'], 'zacc': data['zacc'],
            'temp': data.get('temp', ''), 'feels_like': data.get('feels_like', ''),
            'humidity': data.get('humidity', ''), 'pressure': data.get('pressure', ''),
            'wind_speed': data.get('wind_speed', ''), 'wind_deg': data.get('wind_deg', ''),
            'wind_gust': data.get('wind_gust', ''), 'clouds': data.get('clouds', ''),
            'visibility': data.get('visibility', ''), 'weather_main': data.get('weather_main', ''),
            'weather_desc': data.get('weather_desc', ''), 'rain_1h': data.get('rain_1h', ''),
            'snow_1h': data.get('snow_1h', '')
        }
        response = requests.post(GOOGLE_SHEET_URL, json=payload)
        print(f"[Google Sheets] Status: {response.status_code} | Response: {response.text}")
    except Exception as e:
        print(f"[Google Sheets Error] {e}")
