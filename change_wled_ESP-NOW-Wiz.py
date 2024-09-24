# With thanks to https://github.com/ChuckMash/ESPythoNOW/blob/main/examples/wizmote_send.py#L19-L29

import network
import espnow
import struct
import urandom  # Use urandom for MicroPython

# for WLED controller (Gled2): ec64c9a78c5c
wled_mac = b'\xec\x64\xc9\xa7\x8c\x5c'

class WIZmote:
    def __init__(self):
        self.sequence = 0
        self.button_lookup = {
            "ON": 16,
            "OFF": 17,
            "BRIGHTER": 18,
            "DIMMER": 19
        }
        self.espnow = self.initialize_espnow()

    def initialize_espnow(self):
        # Initialize Wi-Fi in station mode
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        # Initialize ESP-NOW
        e = espnow.ESPNow()
        e.active(True)  # Correct method to activate ESP-NOW
        e.add_peer(wled_mac)
        return e

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
wizmote.send_button("OFF")