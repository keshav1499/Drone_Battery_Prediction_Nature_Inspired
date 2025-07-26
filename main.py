from pymavlink import mavutil
import time

from config import SERIAL_PORT, BAUD_RATE, SEND_TO_GOOGLE, SEND_INTERVAL, WEATHER_UPDATE_INTERVAL
from weather import get_weather_data
from battery_prediction import calculate_battery_prediction
from google_sheets import send_to_google

def main():
    print(f"Connecting to {SERIAL_PORT} at {BAUD_RATE} baud...")
    try:
        mav = mavutil.mavlink_connection(SERIAL_PORT, baud=BAUD_RATE, autoreconnect=True)
        print("Waiting for heartbeat...")
        mav.wait_heartbeat()
        print(f"Heartbeat from system {mav.target_system} component {mav.target_component}")
        mav.mav.request_data_stream_send(mav.target_system, mav.target_component,
                                         mavutil.mavlink.MAV_DATA_STREAM_ALL, 2, 1)
    except Exception as e:
        print(f"[ERROR] Could not connect: {e}")
        return

    data = {k: '' for k in (
        'lat', 'lon', 'alt', 'roll', 'pitch', 'yaw', 'airspeed', 'groundspeed',
        'heading', 'voltage', 'current', 'battery', 'error_rp', 'error_yaw',
        'xacc', 'yacc', 'zacc', 'temp', 'feels_like', 'humidity', 'pressure',
        'wind_speed', 'wind_deg', 'wind_gust', 'clouds', 'visibility',
        'weather_main', 'weather_desc', 'rain_1h', 'snow_1h'
    )}

    last_sent_time = time.time()
    last_weather_update = 0
    last_prediction_time = 0
    prediction_interval = 15

    while True:
        try:
            msg = mav.recv_match(blocking=True)
            if not msg:
                continue

            msg_type = msg.get_type()

            if msg_type == 'GLOBAL_POSITION_INT':
                data['lat'] = msg.lat / 1e7
                data['lon'] = msg.lon / 1e7
                data['alt'] = msg.alt / 1000.0

                current_time = time.time()
                if current_time - last_weather_update >= WEATHER_UPDATE_INTERVAL and data['lat'] and data['lon']:
                    weather = get_weather_data(data['lat'], data['lon'])
                    if weather:
                        data.update(weather)
                        last_weather_update = current_time
                        print("Updated weather data")

            elif msg_type == 'ATTITUDE':
                data['roll'], data['pitch'], data['yaw'] = round(msg.roll, 3), round(msg.pitch, 3), round(msg.yaw, 3)
            elif msg_type == 'VFR_HUD':
                data['airspeed'], data['groundspeed'], data['heading'] = round(msg.airspeed, 2), round(msg.groundspeed, 2), msg.heading
            elif msg_type == 'SYS_STATUS':
                data['voltage'], data['current'], data['battery'] = msg.voltage_battery / 1000.0, msg.current_battery / 100.0, msg.battery_remaining
            elif msg_type == 'AHRS':
                data['error_rp'], data['error_yaw'] = round(msg.error_rp, 4), round(msg.error_yaw, 4)
            elif msg_type == 'RAW_IMU':
                data['xacc'], data['yacc'], data['zacc'] = msg.xacc, msg.yacc, msg.zacc

            if time.time() - last_prediction_time >= prediction_interval:
                calculate_battery_prediction(data)
                last_prediction_time = time.time()

            if time.time() - last_sent_time >= SEND_INTERVAL:
                if all(str(data[k]) != '' for k in ['lat', 'lon', 'alt']):
                    if SEND_TO_GOOGLE:
                        send_to_google(data)
                    last_sent_time = time.time()

        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            print(f"[Loop Error] {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
