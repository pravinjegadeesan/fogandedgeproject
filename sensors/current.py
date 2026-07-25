import random
import time
import requests

FOG_NODE_URL = "http://awseb-e-p-AWSEBLoa-IW5SKUJPCTP1-932418002.us-east-1.elb.amazonaws.com/sensor"
SEND_INTERVAL_SECONDS = 2
MIN_CURRENT = 0.0
MAX_CURRENT = 20.0

def generate_current():
    raw_current = random.uniform(MIN_CURRENT, MAX_CURRENT)
    return round(raw_current, 2)

def send_sensor_data(current_value):
    payload = {
        "sensor_type": "current",
        "value": current_value
    }
    try:
        response = requests.post(FOG_NODE_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"[SUCCESS] Sent Current: {current_value}A")
        else:
            print(f"[WARNING] Status code: {response.status_code}")
    except requests.exceptions.RequestException as error:
        print(f"[ERROR] Connection failed: {error}")

def main():
    print("Starting Virtual Current Sensor...")
    while True:
        current_current = generate_current()
        send_sensor_data(current_current)
        time.sleep(SEND_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
