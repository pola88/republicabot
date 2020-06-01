from .base import Base

class Start(Base):
    """Start commands"""
    name = "Start"
    command = "start"

    @classmethod
    def callbackHandler(cls, bot):
        """Handler the command /start"""
        def callback(update, context):
            update.message.reply_text("🍻")

        return callback
