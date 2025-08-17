# 🛰️ Drone Telemetry + Weather Logger

A lightweight Python project for logging real-time **drone telemetry** over MAVLink (via LoRa) and **environmental weather data** (via I2C BMP280 or online API) to a **Google Sheet**.

---

## 📁 Project Structure

```
serial_drone_data/
├── main.py                # Core script: reads telemetry, adds weather, pushes to Google Sheet
├── weather.py             # Handles BMP280 sensor & weather API fallback
├── google_sheets.py       # Sends data to Google Sheet via webhook
├── config.py              # User config: ports, keys, API settings
├── requirements.txt       # Project dependencies
├── README.md              # Project overview and usage guide
├── utils/
│   └── __init__.py        # Shared utilities, debug tools, helpers
└── sensors/
    ├── __init__.py
    └── bmp280_driver.py   # I2C communication with BMP280 (temp, pressure, humidity)
```

---

## ⚙️ Setup Instructions

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure `config.py` with the following:**

   * `GOOGLE_SHEET_URL`: Webhook endpoint for your sheet
   * `OPENWEATHER_API_KEY`: (Optional) for API fallback
   * `SERIAL_PORT`: e.g., `/dev/ttyUSB0`
   * `BMP280_ADDRESS`: (Optional) I2C address override

3. **Start logging:**

   ```bash
   python main.py
   ```

---

## 🔧 Features

✅ MAVLink Telemetry via Serial (LoRa)
✅ BMP280 Sensor via I2C:
 • Temperature
 • Humidity
 • Pressure
✅ Weather API fallback (OpenWeatherMap)
✅ Sends data to Google Sheet for live logging
✅ Modular, extensible, field-friendly design

---

## 💡 Use Case

> Ideal for **field missions**, **aerial surveys**, or **remote drone ops**, where logging telemetry + environmental data in one place is crucial. Proper battery prediction with considering environment influence on battery has been implemented.

---

Let me know if you'd like:

* A badge-based header (Python version, license, etc.)
* Example Google Sheets integration or setup
* Example log entry/output
* System diagram (ASCII or visual)

We can also turn this into a web dashboard if you're planning to visualize live data.
