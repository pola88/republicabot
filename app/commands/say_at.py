from telegram import ChatAction
from .base import Base
import os
import schedule

class SayAtCommand(Base):
    """Send a message to the group"""
    name = "SayAt"
    command = "say_at"

    @classmethod
    def callbackHandler(cls, bot):
        """Handler the command /SayAt <msg>"""
        def callback(update, context):
            sayAtCommand = SayAtCommand(bot, update.message)
            sayAtCommand.send_typing()

            msg = update.message.text.replace("/say_at ", "").split("-")
            sayAtCommand.job = schedule.every().day.at(msg[0].strip()).do(sayAtCommand.send_msg, msg[1].strip())

            update.message.reply_text("Listo a las " + msg[0].strip() + " mando el mensasje")

        return callback

    def send_msg(self, msg):
      self.bot.sendChatAction(chat_id=int(os.getenv("LA_35_GROUP")) , action=ChatAction.TYPING)
      self.bot.send_message(int(os.getenv("LA_35_GROUP")), msg)
      schedule.cancel_job(self.job)