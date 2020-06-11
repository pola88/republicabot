from .base import Base
from bluetooth import Watering

class WateringCommand(Base):
    """Class to turn on/off watering"""
    name = "Watering"
    command = "watering"

    @classmethod
    def callbackHandler(cls, bot):
        """Handler the command /watering"""
        def callback(update, context):
            message = update.message.text.split(" ")

            watering = WateringCommand(bot, update.message)
            update.message.reply_text("Ok, sending msg...")

            msgid = watering.id
            watering.send_typing()
            try:
                if message[1] == "on":
                    Watering(msgid).on(duration=message[2], callback=watering.callback_on, callback_error=watering.report_error)
                else:
                    Watering(msgid).off(callback=watering.callback_off)
            except Exception as e:
                watering.report_error("Unexpected error: " + str(e))

        return callback

    # response:
    #     0: Error
    #     1: Ok
    #     2: Running

    def callback_on(self, msg):
        result = int(msg)
        self.logger.info(msg)
        if result == 1:
            self.bot.send_message(self.message.chat.id, "Watering on!")
        elif result == 2:
            self.bot.send_message(self.message.chat.id, "Watering was already running!")
        else:
            self.bot.send_message(self.message.chat.id, "There was a problem, Check and try later")

    def callback_off(self, msg):
        result = int(msg)
        self.logger.info(msg)
        if result == 1:
            self.bot.send_message(self.message.chat.id, "Watering off! ")
        else:
            self.bot.send_message(self.message.chat.id, "There was a problem, Check and try later")

    def report_error(self, msg):
        self.logger.error(msg)
        self.bot.send_message(self.message.chat.id,  msg)
