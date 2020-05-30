from .base import Base
from bluetooth import Sender, Receiver

class Status(Base):
    """Class to check the connection"""
    name = "status"
    @classmethod
    def handler(cls, bot):
        return super(Status, cls).handler(bot, cls.__callback)

    @classmethod
    def __callback(cls, bot):
        def callback(update, context):
            status = Status(bot, update.message)
            update.message.reply_text("Checking...")
            msgid = status.id
            status.send_typing()
            try:
                receiver = Receiver(msgid, "status")
                receiver.listen(status.send_status)

                sender = Sender(msgid, "status")
                sender.send("1")
            except:
                status.report_error(sys.exc_info()[0])

        return callback

    def send_status(self, msg):
        self.logger.info(msg)
        self.bot.send_message(self.message.chat.id, "Arduino says: " + msg)

    def report_error(self, msg):
        self.logger.error(msg)
        self.bot.send_message(self.message.chat.id, "Unexpected error: " + msg)
