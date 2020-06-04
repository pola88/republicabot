from .connection import Connection
import time

class Sender(Connection):
    """
        Class to send to arduino a msg
        message_format: {id}_{msg}
    """

    def send(self, msg):
        encoded_msg = str(self.id) + "_" + msg
        self.logging.info("Sending msg: " + encoded_msg)
        self.ser.write(str.encode(encoded_msg))
