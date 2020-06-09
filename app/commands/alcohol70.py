from .base import Base

class Alcohol70Command(Base):
    """Returns how many water add to get alcohol 70"""
    name = "Alcohol70"
    command = "alcohol70"

    @classmethod
    def callbackHandler(cls, bot):
        """Handler the command /alcohol70 <number>"""
        def callback(update, context):
            alcohol70 = Alcohol70Command(bot, update.message)
            alcohol70.send_typing()
            message = update.message.text.split(" ")
            if len(message) != 2:
                update.message.reply_text("Tenes que pasarme cuanto de alcohol 96 tenes")
                return

            cant = int(message[1]) * 200 / 500
            update.message.reply_text("Necesitas agregar {} ml de agua".format(cant))

        return callback
