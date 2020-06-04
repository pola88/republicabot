import serial
import os
import logging

# # Serial port parameters
serial_speed = os.getenv("BlUETOOTH_SPEED")
serial_port = os.getenv("BlUETOOTH_PORT") # bluetooth shield hc-06

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class Connection:
    def __init__(self, msgid, name):
        self.logging = logger.getChild( self.__class__.__name__ + ": "+ name)
        self.id = msgid
        self.ser = serial.Serial(serial_port, serial_speed, timeout=1)
        self.name = name
