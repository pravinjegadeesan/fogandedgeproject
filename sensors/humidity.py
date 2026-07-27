import random
import time

import requests

FOG_NODE_URL = "http://awseb-e-p-AWSEBLoa-IW5SKUJPCTP1-932418002.us-east-1.elb.amazonaws.com/sensor"
SEND_INTERVAL_SECONDS = 5
MIN_HUMIDITY = 30.0
MAX_HUMIDITY = 80.0

def generate_humidity():
    raw_humidity = random.uniform(MIN_HUMIDITY, MAX_HUMIDITY)
    return round(raw_humidity, 2)

def send_sensor_data(humidity_value):
    payload = {
        "sensor_type": "humidity",
        "value": humidity_value
    }
    try:
        response = requests.post(FOG_NODE_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"[SUCCESS] Sent Humidity: {humidity_value}%")
        else:
            print(f"[WARNING] Status code: {response.status_code}")
    except requests.exceptions.RequestException as error:
        print(f"[ERROR] Connection failed: {error}")

def main():
    print("Starting Virtual Humidity Sensor...")
    while True:
        current_humidity = generate_humidity()
        send_sensor_data(current_humidity)
        time.sleep(SEND_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
