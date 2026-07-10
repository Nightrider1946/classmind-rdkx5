import requests

ESP32_IP = "10.139.104.208"  # REPLACE with your actual ESP32 IP
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
    
def attendance_start_beep():
    try:
        response = requests.get(
            f"http://{ESP32_IP}/attendance-start",
            timeout=2
        )

        if response.status_code == 200:
            print("[ESP32] Attendance start beep sent")

    except requests.RequestException as e:
        print(
            f"[ESP32] Start beep communication failed: {e}"
        )


def attendance_end_beep():
    try:
        response = requests.get(
            f"http://{ESP32_IP}/attendance-end",
            timeout=2
        )

        if response.status_code == 200:
            print("[ESP32] Attendance end beep sent")

    except requests.RequestException as e:
        print(
            f"[ESP32] End beep communication failed: {e}"
        )    