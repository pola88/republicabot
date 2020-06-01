from .base import Base
from bluetooth import Sender, Receiver

class Status(Base):
    """Class to check the connection"""
    name = "Status"
    command = "status"

    @classmethod
    def callbackHandler(cls, bot):
        """Handler the command /status"""
        def callback(update, context):
            status = Status(bot, update.message)
            update.message.reply_text("Checking...")
            status.logger.info("Checking Arduino")
            msgid = status.id
            status.send_typing()
            try:
                receiver = Receiver(msgid, Status.name)
                receiver.listen(status.send_status)

                sender = Sender(msgid, Status.name)
                sender.send("1")
            except Exception as e:
                status.report_error("Unexpected error: " + str(e))

        return callback

    def send_status(self, msg):
        self.logger.info(msg)
        self.bot.send_message(self.message.chat.id, "Arduino says: " + msg)

    def report_error(self, msg):
        self.logger.error(msg)
        self.bot.send_message(self.message.chat.id,  msg)
