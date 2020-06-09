from .base import Base
from bluetooth import Status

class StatusCommand(Base):
    """Class to check the connection"""
    name = "Status"
    command = "status"

    @classmethod
    def callbackHandler(cls, bot):
        """Handler the command /status"""
        def callback(update, context):
            status = StatusCommand(bot, update.message)
            update.message.reply_text("Checking...")
            status.logger.info("Checking Arduino")
            msgid = status.id
            status.send_typing()
            try:
                Status(msgid).check(status.send_status)
            except Exception as e:
                status.report_error("Unexpected error: " + str(e))

        return callback

    def send_status(self, msg):
        result = int(msg)
        self.logger.info(msg)
        if result == 1:
            self.bot.send_message(self.message.chat.id, "Arduino says: I'm ok! ")
        else:
            self.bot.send_message(self.message.chat.id, "Arduino says: I don't feel well, Could you check me?" + msg)

    def report_error(self, msg):
        self.logger.error(msg)
        self.bot.send_message(self.message.chat.id,  msg)
