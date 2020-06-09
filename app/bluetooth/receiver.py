from .connection import Connection
from time import sleep
import threading
import serial

class Receiver(Connection):
    """
        Class to start listen msg from bluetooth in a new thread until get the correct msg
        It will check the id to see if the callback should be run
    """

    def __listener(self):
        self.is_waiting = True
        self.logging.info("Waiting msg");
        while self.is_waiting:
            if(self.ser.in_waiting > 0):
                try:
                    msg = self.ser.readline().decode()
                    msgId = msg.split("_")[0]
                    self.msg = msg.split("_")[1]

                    if (self.id == int(msgId)):
                        self.logging.info(self.msg)
                        self.is_waiting = False
                except serial.SerialTimeoutException as serialTimeout:
                        self.loggin.error("Serial timeout")
                        self.is_waiting = False
                except Exception as e:
                    self.loggin.error(str(e))
                    self.is_waiting = False
            sleep(1)
        self.callback(self.msg)

    def listen(self, callback):
        self.callback = callback
        self.worker = threading.Thread(name=self.name, target=self.__listener)
        self.worker.start()
