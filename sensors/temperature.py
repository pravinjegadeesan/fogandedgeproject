import random
import time

import requests

FOG_NODE_URL = "http://awseb-e-p-AWSEBLoa-IW5SKUJPCTP1-932418002.us-east-1.elb.amazonaws.com/sensor"
SEND_INTERVAL_SECONDS = 3
MIN_TEMP = 18.0
MAX_TEMP = 35.0

def generate_temperature():
    raw_temp = random.uniform(MIN_TEMP, MAX_TEMP)
    return round(raw_temp, 2)

def send_sensor_data(temperature_value):
    payload = {
        "sensor_type": "temperature",
        "value": temperature_value
    }
    try:
        response = requests.post(FOG_NODE_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"[SUCCESS] Sent Temperature: {temperature_value}°C")
        else:
            print(f"[WARNING] Status code: {response.status_code}")
    except requests.exceptions.RequestException as error:
        print(f"[ERROR] Connection failed: {error}")

def main():
    print("Starting Virtual Temperature Sensor...")
    while True:
        current_temp = generate_temperature()
        send_sensor_data(current_temp)
        time.sleep(SEND_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
