import random
import time
import requests

FOG_NODE_URL = "http://awseb-e-p-AWSEBLoa-IW5SKUJPCTP1-932418002.us-east-1.elb.amazonaws.com/sensor"
SEND_INTERVAL_SECONDS = 2

def generate_power():
    voltage = random.uniform(210.0, 250.0)
    current = random.uniform(0.0, 20.0)
    power = voltage * current
    return round(power, 2)

def send_sensor_data(power_value):
    payload = {
        "sensor_type": "power",
        "value": power_value
    }
    try:
        response = requests.post(FOG_NODE_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"[SUCCESS] Sent Power: {power_value}W")
        else:
            print(f"[WARNING] Status code: {response.status_code}")
    except requests.exceptions.RequestException as error:
        print(f"[ERROR] Connection failed: {error}")

def main():
    print("Starting Virtual Power Sensor...")
    while True:
        current_power = generate_power()
        send_sensor_data(current_power)
        time.sleep(SEND_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
