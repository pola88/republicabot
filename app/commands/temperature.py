from .base import Base
from bluetooth import Temperature

class TemperatureCommand(Base):
    """Class to get the temperature"""
    name = "Temperature"
    command = "temperature"

    @classmethod
    def callbackHandler(cls, bot):
        """Handler the command /temperature"""
        def callback(update, context):
            message = update.message.text.split(" ")

            temperature = TemperatureCommand(bot, update.message)
            update.message.reply_text("Ok, getting info...")

            msgid = temperature.id
            temperature.send_typing()
            try:
                Temperature(msgid).get(callback=temperature.blue_callback, callback_error=temperature.report_error)
            except Exception as e:
                temperature.report_error("Unexpected error: " + str(e))

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
            self.bot.send_message(self.message.chat.id, "There was a problem, Check and try later")

    def report_error(self, msg):
        self.logger.error(msg)
        self.bot.send_message(self.message.chat.id,  msg)
