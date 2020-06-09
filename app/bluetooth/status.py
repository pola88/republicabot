from .receiver import Receiver
from .sender import Sender
from .base import Base

class Status(Base):
    """
        Class to send to arduino to turn on/off the watering
        messages format: {id}_1
    """

    def __init__(self, id):
        self.name = 'Status'
        super(self.__class__, self).__init__(id)

    def check(self, callback):
        receiver = Receiver(self.id, self.name)
        receiver.listen(callback)

        sender = Sender(self.id, self.name)
        sender.send("1")
