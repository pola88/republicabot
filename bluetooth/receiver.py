from .base import Base
from time import sleep
import logging
import threading

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class Receiver(Base):

    def __listener(self):
        self.is_waiting = True
        logging.info("Waiting msg");
        while self.is_waiting:
            if(self.ser.in_waiting > 0):
                self.msg = self.ser.readline().decode()
                logging.info(self.msg)
                self.is_waiting = False
            sleep(1)
        self.callback(self.msg)

    def listen(self, callback):
        self.callback = callback
        self.worker = threading.Thread(name=self.name, target=self.__listener)
        self.worker.start()
