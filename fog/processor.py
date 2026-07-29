import datetime

voltage_buffer = []
current_buffer = []
power_buffer = []

latest_temp = None
latest_humidity = None

def is_valid(sensor_type, value):
    if sensor_type == "temperature":
        return 0 <= value <= 60
    elif sensor_type == "voltage":
        return 150 <= value <= 300
    elif sensor_type == "current":
        return value >= 0
    elif sensor_type == "humidity":
        return 0 <= value <= 100
    elif sensor_type == "power":
        return value >= 0
    return False

def add_reading(sensor_type, value):
    global latest_temp, latest_humidity
    
    if not is_valid(sensor_type, value):
        print(f"[FOG PROCESSOR] Ignored invalid {sensor_type}: {value}")
        return None

    if sensor_type == "temperature":
        latest_temp = value
    elif sensor_type == "humidity":
        latest_humidity = value
    elif sensor_type == "voltage":
        voltage_buffer.append(value)
    elif sensor_type == "current":
        current_buffer.append(value)
    elif sensor_type == "power":
        power_buffer.append(value)

    if (len(voltage_buffer) >= 1 and 
        len(current_buffer) >= 1 and 
        len(power_buffer) >= 1 and 
        latest_temp is not None and 
        latest_humidity is not None):
        
        avg_voltage = round(voltage_buffer[0], 2)
        avg_current = round(current_buffer[0], 2)
        avg_power = round(power_buffer[0], 2)
        
        status = "High Energy Consumption" if avg_power > 3500 else "Normal"
        
        payload = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
            "temperature": latest_temp,
            "humidity": latest_humidity,
            "voltage": avg_voltage,
            "current": avg_current,
            "power": avg_power,
            "status": status
        }
        del voltage_buffer[:1]
        del current_buffer[:1]
        del power_buffer[:1]
        return payload
    return None
