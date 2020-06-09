from .base import Base
import random

BEER_STYLES = ["Albier", "APA", "Barley Wine", "Bock", "Brown Ale",
               "Dorada Pampeana", "English Pale Ale", "IPA", "Irish Red",
               "Kolsh", "Lager", "Honey", "Oatmel stout", "Porter", "Scoth",
               "Stout", "de Trigo"]
class DrinkCommand(Base):
    """Returns what should drink"""
    name = "Drink"
    command = "que_tomo"

    @classmethod
    def callbackHandler(cls, bot):
        """Handler the command /drink <number>"""
        def callback(update, context):
            drinkCommand = DrinkCommand(bot, update.message)
            drinkCommand.send_typing()
            message = update.message.text.replace("/que_tomo", "").split(",")
            if len(message) == 0 or message == ['']:
                drink = random.choice(BEER_STYLES)
            else:
                drink = random.choice(message).strip()

            update.message.reply_text("Hoy esta para tomarte una {}".format(drink))

        return callback
