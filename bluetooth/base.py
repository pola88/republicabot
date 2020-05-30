import serial
import os
# # Serial port parameters
serial_speed = os.getenv("BlUETOOTH_SPEED")
serial_port = os.getenv("BlUETOOTH_PORT") # bluetooth shield hc-06


class Base:
    def __init__(self, msgid, name):
        self.msgid = msgid
        self.ser = serial.Serial(serial_port, serial_speed, timeout=1)
        self.name = name
