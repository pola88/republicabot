from .base import Base

class PreguntaCommand(Base):
    """Ask a pregunta and you get a random answer"""
    name = "Pregunta"
    command = "pregunta"

    @classmethod
    def callbackHandler(cls, bot):
        """Handler the command /pregunta <string>"""
        def callback(update, context):
            preguntaCommand = PreguntaCommand(bot, update.message)
            preguntaCommand.logger.info(update.message.text)
            preguntaCommand.send_typing()

            update.message.reply_text("Dejame pensarlo")

        return callback
