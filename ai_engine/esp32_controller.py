import requests

ESP32_IP = "10.243.165.208"  # REPLACE with your actual ESP32 IP
TIMEOUT = 2

def set_light(state: bool):
    endpoint = "red" if state else "off"
    url = f"http://{ESP32_IP}/{endpoint}"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        print(f"[ESP32] Light {endpoint.upper()} — Status: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"[ESP32] Communication failed: {e}")
        return False