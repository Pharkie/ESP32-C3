import network
import urequests
import time
import secrets  # Import the secrets module

# WLED controller URL
wled_url = "http://wled-gled2.local/json"

# JSON payload to set preset 2
payload = {"ps": 2}


def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    print("Connecting to Wi-Fi...", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)
    print("\nConnected to Wi-Fi")
    print("\nConnected to Wi-Fi")


def set_wled_preset(url, data):
    try:
        response = urequests.post(url, json=data)
        if response.status_code == 200:
            print("Preset set successfully.")
        else:
            print("Failed to set preset. Status code:", response.status_code)
        response.close()
    except Exception as e:
        print("Error:", e)


# Connect to Wi-Fi using credentials from secrets.py
connect_to_wifi(secrets.ssid, secrets.password)

# Set WLED to preset 2
set_wled_preset(wled_url, payload)
