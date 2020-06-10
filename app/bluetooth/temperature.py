from .receiver import Receiver
from .sender import Sender
from .base import Base

class Temperature(Base):
    """
        Class to send to arduino to get the current temperature and humidity
        messages:
            get: {id}_4
    """

    def __init__(self, id):
        self.name = 'watering'
        super(self.__class__, self).__init__(id)

    def get(self, callback):
        receiver = Receiver(self.id, self.name)
        receiver.listen(callback)

        sender = Sender(self.id, self.name)
        sender.send("4")
