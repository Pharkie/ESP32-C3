import network
import espnow

# WLED controller MAC address (replace with the actual MAC address of the WLED controller)
wled_mac = b'\xec\x64\xc9\xa7\x8c\x5c'

# Example payloads for WIZmote button presses
payload_button_1 = b'{"bssid": "ecda3b32fa88", "button": 16, "sequence": 1}'
payload_button_2 = b'{"bssid": "ecda3b32fa88", "button": 17, "sequence": 1}'
payload_button_3 = b'{"bssid": "ecda3b32fa88", "button": 18, "sequence": 1}'
payload_button_4 = b'{"bssid": "ecda3b32fa88", "button": 19, "sequence": 1}'

def get_mac_address():
    wlan = network.WLAN(network.STA_IF)
    mac = wlan.config('mac')
    mac_address = ''.join(['{:02x}'.format(b) for b in mac])
    return mac_address

def initialize_espnow():
    # Initialize Wi-Fi in station mode
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Initialize ESP-NOW
    e = espnow.ESPNow()
    e.active(True)
    e.add_peer(wled_mac)
    return e

def send_espnow_message(e, message):
    try:
        e.send(wled_mac, message)
        print("Message sent successfully.")
    except Exception as prob:
        print("Error sending message:", prob)

# Print the MAC address
print("ESP32-C3 MAC Address:", get_mac_address())

# Initialize ESP-NOW
espnow_instance = initialize_espnow()

# Send the ESP-NOW message for button 1 press
send_espnow_message(espnow_instance, payload_button_1)