import network
import espnow
import struct

# WLED controller MAC address (replace with the actual MAC address of the WLED controller)
# MAC address for WLED controller (Gled2): ec64c9a78c5c
# MAC address of the ESP32-C3: ecda3b32fa88
wled_mac = b'\xec\x64\xc9\xa7\x8c\x5c'

# Function to create the payload
def create_payload(button, sequence):
    program = 0x91 if button == 1 else 0x81
    seq_bytes = struct.pack('<I', sequence)  # Little-endian 4-byte sequence number
    payload = struct.pack('B4sB3B4B', program, seq_bytes, 32, button, 1, 100, 0, 0, 0, 0)
    return payload

# Example payloads for WIZmote button presses
payload_button_1 = create_payload(16, 1)
payload_button_2 = create_payload(17, 2)
payload_button_3 = create_payload(18, 3)
payload_button_4 = create_payload(19, 4)

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

# Send the ESP-NOW message for button 2 press
send_espnow_message(espnow_instance, payload_button_2)