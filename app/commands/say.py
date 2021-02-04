from telegram import ChatAction
from .base import Base
import os

class SayCommand(Base):
    """Send a message to the group"""
    name = "Say"
    command = "say"

    @classmethod
    def callbackHandler(cls, bot):
        """Handler the command /say <msg>"""
        def callback(update, context):
            sayCommand = SayCommand(bot, update.message)
            sayCommand.bot.sendChatAction(chat_id=int(os.getenv("LA_35_GROUP")) , action=ChatAction.TYPING)

            sayCommand.bot.send_message(int(os.getenv("LA_35_GROUP")), update.message.text.replace("/say ", ""))

        return callback
