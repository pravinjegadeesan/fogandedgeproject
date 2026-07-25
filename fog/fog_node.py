from flask import Flask, request, jsonify
import requests
import processor

import os
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
app = Flask(__name__, static_folder=frontend_dir, static_url_path='')

CLOUD_ENDPOINT = "https://o3g9wp3ss2.execute-api.us-east-1.amazonaws.com/prod/energy"

@app.route('/sensor', methods=['POST'])
def receive_sensor_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload received"}), 400
        
    sensor_type = data.get("sensor_type")
    value = data.get("value")
    
    if sensor_type is None or value is None:
        return jsonify({"error": "Missing sensor_type or value"}), 400
        
    aggregated_payload = processor.add_reading(sensor_type, value)
    
    if aggregated_payload:
        print("\n=== AGGREGATED PAYLOAD FOR CLOUD ===")
        print(aggregated_payload)
        print("====================================\n")
        
        if "CHANGE_ME" not in CLOUD_ENDPOINT and CLOUD_ENDPOINT != "":
            try:
                response = requests.post(CLOUD_ENDPOINT, json=aggregated_payload, timeout=5)
                print(f"[CLOUD_SEND] Status: {response.status_code}, Response: {response.text}")
            except requests.exceptions.RequestException as error:
                print(f"[CLOUD_ERROR] Failed to send: {error}")
        else:
            print("[INFO] Cloud endpoint not configured. Skipping send.")
            
    return jsonify({"status": "processed"}), 200

@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

@app.after_request
def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

if __name__ == "__main__":
    print("Starting Fog Node Server on port 5001...")
    app.run(host="0.0.0.0", port=5001)
