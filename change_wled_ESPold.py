import network
import espnow

# WLED controller MAC address (replace with the actual MAC address of the WLED controller)
# MAC address for WLED controller (Gled2): ec64c9a78c5c
# MAC address of the ESP32-C3: ecda3b32fa88
wled_mac = b'\xec\x64\xc9\xa7\x8c\x5c'

# JSON payload to set preset 2
payload = b'{"ps": 2}'

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
    espnow_instance = espnow.ESPNow()
    espnow_instance.active(True)
    espnow_instance.add_peer(wled_mac)
    return espnow_instance

def send_espnow_message(espnow_instance, wled_mac, payload):
    espnow_instance.add_peer(wled_mac)
    
    try:
        espnow_instance.send(wled_mac, payload)
        print("Message sent successfully.")
    except Exception as some_error:
        print("Error sending message:", some_error)

# Print the MAC address
print("MAC Address:", get_mac_address())

# Initialize ESP-NOW
espnow_instance = initialize_espnow()

# Define the WLED MAC address
wled_mac = b'\xec\xda\x3b\x32\xfa\x88'

# Send the ESP-NOW message to set WLED to preset 2
send_espnow_message(espnow_instance, wled_mac, payload)