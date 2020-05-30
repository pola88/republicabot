from .base import Base
import time
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class Sender(Base):

    def send(self, msg):
        logger.info('Sending msg')
        self.ser.write(str.encode(msg))
