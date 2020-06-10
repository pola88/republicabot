from .base import Base
from bluetooth import Temperature

class TemperatureCommand(Base):
    """Class to turn on/off watering"""
    name = "Temperature"
    command = "temperature"

    @classmethod
    def callbackHandler(cls, bot):
        """Handler the command /watering"""
        def callback(update, context):
            message = update.message.text.split(" ")

            watering = TemperatureCommand(bot, update.message)
            update.message.reply_text("Ok, getting info...")

            msgid = watering.id
            watering.send_typing()
            try:
                Temperature(msgid).get(callback=watering.blue_callback)
            except Exception as e:
                watering.report_error("Unexpected error: " + str(e))

        return callback

    # response:
    #     0: Error
    #     1: Ok

    def blue_callback(self, msg):
        status, temperature, humidity = msg.split("_")
        status = int(status)
        if status == 1:
            self.bot.send_message(self.message.chat.id, "Temperature: {} C \nHumidity: {} %".format(temperature, int(humidity)))
        else:
            self.bot.send_message(self.message.chat.id, "Arduino says: I don't feel well, Could you check me?")

    def report_error(self, msg):
        self.logger.error(msg)
        self.bot.send_message(self.message.chat.id,  msg)
