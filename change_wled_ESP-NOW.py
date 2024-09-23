import network
import espnow
import time

# WLED controller MAC address (replace with the actual MAC address of the WLED controller)
wled_mac = b'\xec\x64\xc9\xa7\x8c\x5c'

# JSON payload to set preset 2
payload = b'{"ps": 2}'

def get_mac_address():
    wlan = network.WLAN(network.STA_IF)
    mac = wlan.config('mac')
    mac_address = ':'.join(['{:02x}'.format(b) for b in mac])
    return mac_address

def send_espnow_message(peer_mac, message):
    e = espnow.ESPNow()
    e.add_peer(peer_mac)
    
    try:
        e.send(peer_mac, message)
        print("Message sent successfully.")
    except Exception as e:
        print("Error sending message:", e)

# Print the MAC address
print("MAC Address:", get_mac_address())

# Initialize Wi-Fi in station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Initialize ESP-NOW
e = espnow.ESPNow()

# Send the ESP-NOW message to set WLED to preset 2
send_espnow_message(wled_mac, payload)