import random
import time
import requests

FOG_NODE_URL = "http://awseb-e-p-AWSEBLoa-IW5SKUJPCTP1-932418002.us-east-1.elb.amazonaws.com/sensor"
SEND_INTERVAL_SECONDS = 2
MIN_VOLTAGE = 210.0
MAX_VOLTAGE = 250.0

def generate_voltage():
    raw_voltage = random.uniform(MIN_VOLTAGE, MAX_VOLTAGE)
    return round(raw_voltage, 2)

def send_sensor_data(voltage_value):
    payload = {
        "sensor_type": "voltage",
        "value": voltage_value
    }
    try:
        response = requests.post(FOG_NODE_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"[SUCCESS] Sent Voltage: {voltage_value}V")
        else:
            print(f"[WARNING] Status code: {response.status_code}")
    except requests.exceptions.RequestException as error:
        print(f"[ERROR] Connection failed: {error}")

def main():
    print("Starting Virtual Voltage Sensor...")
    while True:
        current_voltage = generate_voltage()
        send_sensor_data(current_voltage)
        time.sleep(SEND_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
