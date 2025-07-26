import serial
import time
from datetime import datetime

SERIAL_PORT = '/dev/ttyUSB0'  # Same port as your MAVLink connection
BAUD_RATE = 115200

def parse_dht_data(line):
    """Parse DHT11 data from custom format: <DHT11:TEMP=23.5,HUM=45.0>"""
    try:
        if line.startswith('<DHT11:TEMP=') and line.endswith('>'):
            # Extract the content between the brackets
            content = line[12:-1]
            # Split into temperature and humidity parts
            temp_part, hum_part = content.split(',')
            # Extract numeric values
            temp = float(temp_part.split('=')[1])
            hum = float(hum_part.split('=')[1])
            return temp, hum
    except Exception as e:
        print(f"Error parsing DHT data: {e}")
    return None, None

def main():
    print(f"Connecting to {SERIAL_PORT} at {BAUD_RATE} baud...")
    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print("Waiting for DHT11 data...")
        
        # Clear any existing data in buffers
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        while True:
            if ser.in_waiting:
                try:
                    # Read a line from serial
                    line = ser.readline().decode('ascii', errors='ignore').strip()
                    
                    if line:
                        print(f"Raw received: {line}")  # Debug output
                        
                        # Try to parse DHT data
                        temp, hum = parse_dht_data(line)
                        
                        if temp is not None and hum is not None:
                            timestamp = datetime.now().strftime("%H:%M:%S")
                            print(f"[{timestamp}] DHT11 - Temp: {temp}°C, Humidity: {hum}%")
                        else:
                            print(f"Ignored: {line}")
                            
                except UnicodeDecodeError:
                    print("Received binary data (possibly MAVLink)")
                except Exception as e:
                    print(f"Error processing data: {e}")
            
            time.sleep(0.1)  # Small delay to prevent CPU overload

    except serial.SerialException as e:
        print(f"Serial connection error: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()
