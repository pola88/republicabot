from .base import Base

class HelpCommand(Base):
    """List help of commands"""
    name = "Help"
    command = "help"

    @classmethod
    def callbackHandler(cls, bot):
        """Handler the command /help"""
        def callback(update, context):
            update.message.reply_text("Si no sabes como usarlo, no deberias estar jugando conmigo!!!")

        return callback
