# Drone Telemetry + Weather Logger

This project collects telemetry data from a drone via MAVLink over LoRa and logs it to a Google Sheet. It also integrates weather sensor data (from BMP280) via I2C and weather API fallback.

## 📁 Directory Structure

```
serial_drone_data/
├── main.py                # Main script to read MAVLink data, augment with weather, and send to Google Sheets
├── weather.py             # Reads weather data from BMP280 sensor or weather API as fallback
├── google_sheets.py       # Sends telemetry + weather data to Google Sheets using webhook
├── config.py              # Configuration variables like API keys, port, etc.
├── utils/
│   └── __init__.py        # Utility functions (e.g., sensor helpers, debug tools)
├── sensors/
│   ├── __init__.py
│   └── bmp280_driver.py   # I2C communication with BMP280 sensor (temperature, pressure, humidity)
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## ⚙️ Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure `config.py` with:
   - `GOOGLE_SHEET_URL` (webhook)
   - `OPENWEATHER_API_KEY` (optional)
   - `SERIAL_PORT` (e.g., `/dev/ttyUSB0`)
   - I2C address for sensor if changed

3. Run the logger:
   ```bash
   python main.py
   ```

## 🔧 Features

- Reads telemetry (lat, lon, altitude, attitude, battery, etc.) via MAVLink
- Augments with temperature, humidity, pressure (BMP280 sensor)
- Falls back to OpenWeatherMap API if sensor not connected
- Sends combined data to a Google Sheet

---
> Designed for drone field logging via LoRa telemetry and sensor fusion.