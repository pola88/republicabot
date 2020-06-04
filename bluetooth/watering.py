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

    def __init__(self, msgid):
        self.name = 'watering'
        super().__init__(self, msgid)

    def on(self, duration):
        try:
            receiver = Receiver(self.id, Status.name)
            receiver.listen(status.send_status)

            sender = Sender(self.id, Status.name)
            sender.send("2_" + str(duration))
        except Exception as e:
            status.report_error("Unexpected error: " + str(e))
        pass

    def off():
        pass

    def send_status(self, msg):
        self.logger.info(msg)
        self.bot.send_message(self.message.chat.id, "Arduino says: " + msg)
