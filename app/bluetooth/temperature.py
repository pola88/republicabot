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
        self.name = 'temperature'
        super(self.__class__, self).__init__(id)

    def get(self, callback, callback_error):
        receiver = Receiver(self.id, self.name)
        receiver.listen(callback, callback_error)

        sender = Sender(self.id, self.name)
        sender.send("4")
