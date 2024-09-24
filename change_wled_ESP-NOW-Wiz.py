# Wizmote code derived from
# https://github.com/ChuckMash/ESPythoNOW/blob/main/examples/wizmote_send.py#L19-L29
# With thanks to Kilrah and Dedehai on the WLED Discord for their help and support.

import network
import espnow
import struct
import urandom  # Use urandom for MicroPython
import os
import secrets

wled_mac = secrets.wled_mac
SEQUENCE_FILE = "sequence.txt"

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
        self.sequence = self.load_sequence()

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

    def load_sequence(self):
        if SEQUENCE_FILE in os.listdir():
            with open(SEQUENCE_FILE, "r") as f:
                return int(f.read().strip())
        return 1

    def save_sequence(self):
        with open(SEQUENCE_FILE, "w") as f:
            f.write(str(self.sequence))

    def send_button(self, button):
        msg = b""
        msg += struct.pack('<B',  0x91 if button == "ON" else 0x81) # Type
        msg += struct.pack('<I',  self.sequence)                    # Sequence
        msg += struct.pack('<B',  32)                               # Data type
        msg += struct.pack('<B',  self.button_lookup[button])       # Button
        msg += struct.pack('<B',  1)                                # Data type
        msg += struct.pack('<B',  100)                              # Battery level
        msg += struct.pack('<4B', *[urandom.getrandbits(8) for _ in range(4)])  # Random bytes

        print(f"Sending message with sequence number: {self.sequence}")

        try:
            for channel in range(1, 14):  # Iterate through Wi-Fi channels 1 to 13
                network.WLAN(network.STA_IF).config(channel=channel)
                self.espnow.send(wled_mac, msg)
            print("Message sent successfully on all channels.")
        except Exception as e:
            print("Error sending message:", e)
        
        self.sequence += 1
        self.save_sequence()

# Test
wizmote = WIZmote()
wizmote.send_button("ON")