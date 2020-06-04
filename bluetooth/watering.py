from .receiver import Receiver
from .sender import Sender
from .base import Base

class Watering(Base):
    """
        Class to send to arduino to turn on/off the watering
        messages:
            on: {id}_2_{duration}
            off: {id}_3
    """

    def __init__(self, id):
        self.name = 'watering'
        super(self.__class__, self).__init__(id)

    def on(self, duration, callback):
        receiver = Receiver(self.id, self.name)
        receiver.listen(callback)

        sender = Sender(self.id, self.name)
        sender.send("2_" + str(duration))

    def off(self, callback):
        receiver = Receiver(self.id, self.name)
        receiver.listen(callback)

        sender = Sender(self.id, self.name)
        sender.send("3")
