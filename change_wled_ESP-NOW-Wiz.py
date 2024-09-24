# Wizmote code derived from
# https://github.com/ChuckMash/ESPythoNOW/blob/main/examples/wizmote_send.py#L19-L29

import network
import espnow
import struct
import urandom  # Use urandom for MicroPython

# MAC for WLED controller (Gled2): ec64c9a78c5c
wled_mac = b'\xec\x64\xc9\xa7\x8c\x5c'

class WIZmote:
    def __init__(self):
        self.button_lookup = {
            "ON": 1,
            "OFF": 2,
            "SLEEP": 3,
            "1": 16,
            "2": 17,
            "3": 18,
            "4": 19,
            "-": 8,
            "+": 9
        }
        self.espnow = self.initialize_espnow()
        self.sequence = 1

    def initialize_espnow(self):
        # Initialize Wi-Fi in station mode
        interface = network.STA_IF
        wlan = network.WLAN(interface)
        wlan.active(True)

        # Initialize ESP-NOW
        espnow_instance = espnow.ESPNow()
        espnow_instance.active(True)
        espnow_instance.add_peer(wled_mac)
        return espnow_instance

    def send_button(self, button):
        msg = b""
        msg += struct.pack('<B',  0x91 if button == "ON" else 0x81) # Type
        msg += struct.pack('<I',  self.sequence)                    # Sequence
        msg += struct.pack('<B',  32)                               # Data type
        msg += struct.pack('<B',  self.button_lookup[button])       # Button
        msg += struct.pack('<B',  1)                                # Data type
        msg += struct.pack('<B',  100)                              # Battery level
        msg += struct.pack('<4B', *[urandom.getrandbits(8) for _ in range(4)])  # Random bytes

        try:
            self.espnow.send(wled_mac, msg)
            print("Message sent successfully.")
        except Exception as e:
            print("Error sending message:", e)
        
        self.sequence += 1

# Example usage
wizmote = WIZmote()
wizmote.send_button("2")