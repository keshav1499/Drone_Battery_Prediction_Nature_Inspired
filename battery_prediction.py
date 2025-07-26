import math
from config import STANDARD_TEMP, BASE_DRAIN_RATE

def calculate_battery_prediction(data):
    if not data.get('battery') or not data.get('temp') or not data.get('wind_speed') or not data.get('wind_deg') or not data.get('heading'):
        return None

    current_battery = data['battery']
    temp = data['temp']
    wind_speed = data['wind_speed']
    wind_deg = data['wind_deg']
    heading = data['heading']

    temp_diff = abs(temp - STANDARD_TEMP)
    temp_factor = 1 + (temp_diff ** 2) * 0.0005

    wind_rad = math.radians(wind_deg)
    heading_rad = math.radians(heading)
    relative_wind_angle = (wind_rad - heading_rad) % (2 * math.pi)

    wind_factor = 1 + (wind_speed * 0.02 * math.cos(relative_wind_angle))
    drain_rate = BASE_DRAIN_RATE * temp_factor * wind_factor

    if drain_rate <= 0:
        return None

    predicted_time_left = current_battery / drain_rate

    print("\n--- Battery Prediction ---")
    print(f"Current battery: {current_battery}%")
    print(f"Temperature: {temp}°C (Deviation: {temp_diff}°C)")
    print(f"Wind speed: {wind_speed} m/s, Direction: {wind_deg}°")
    print(f"Drone heading: {heading}°")
    print(f"Relative wind angle: {math.degrees(relative_wind_angle):.1f}°")
    print(f"Temperature factor: {temp_factor:.3f}")
    print(f"Wind factor: {wind_factor:.3f}")
    print(f"Calculated drain rate: {drain_rate:.2f}%/min")
    print(f"Predicted time left: {predicted_time_left:.1f} minutes")
    print("-------------------------\n")

    return predicted_time_left
