import os
import logging
from dotenv import load_dotenv
load_dotenv()

from telegram import Bot
from telegram.ext import Updater, CommandHandler
from telegram.ext.filters import Filters

from commands import Status

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    logger.info(update.message['chat'])
    update.message.reply_text(' 🍻')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Si no sabes como usarlo, no deberias estar jugando conmigo!!!')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def message(update, context):
    logger.info(update);

def main():
    #Instance bot to send msg for response when it needed
    # bot = Bot(os.getenv("TELEGRAM_KEY"))

    # Create the Updater and pass it your bot's token.
    updater = Updater(os.getenv("TELEGRAM_KEY"), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, Filters.chat(-225411390) | Filters.chat(21667736)))
    dp.add_handler(CommandHandler("help", help, Filters.chat(-225411390) | Filters.chat(21667736)))
    dp.add_handler(Status.handler(updater.bot))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    #
    # bot.send_message(21667736, "Hola")

    logger.info("RepublicaBeerBot up and running")
    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
