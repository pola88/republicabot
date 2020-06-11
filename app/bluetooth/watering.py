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

    def on(self, duration, callback, callback_error):
        receiver = Receiver(self.id, self.name)
        receiver.listen(callback, callback_error)

        sender = Sender(self.id, self.name)
        sender.send("2_" + str(duration))

    def off(self, callback, callback_error):
        receiver = Receiver(self.id, self.name)
        receiver.listen(callback, callback_error)

        sender = Sender(self.id, self.name)
        sender.send("3")
